#!/usr/bin/env python3
"""بازتولید حداقلی `SystemError: AST constructor recursion depth mismatch`.

زنجیرهٔ علّی که در بارِ زنده دیده شد:
  `app/deps.py:135 _guard` → `security/rbac.py:264 enforce` →
  casbin → `compile()`/`eval()` روی **هر درخواست** →
  در عمق پشتهٔ middleware (بالاتر از ۳۰ فریم) و با ده‌ها نخ همزمان،
  CPython در ساخت AST خطای `SystemError` می‌دهد ⇒ ۵۰۰.

این اسکریپت همان شرایط را بدون HTTP بازسازی می‌کند:
  • عمق پشتهٔ قابل تنظیم (شبیه‌سازی زنجیرهٔ middleware)
  • تعداد نخ‌های همزمان قابل تنظیم
  • شمارش SystemError / RecursionError و زمان هر enforce

اجرا: /tmp/run/venv/bin/python audit/repro_rbac_systemerror.py [threads] [depth] [calls]
"""
from __future__ import annotations

import json
import os
import statistics
import sys
import threading
import time
from collections import Counter
from pathlib import Path

os.environ.setdefault("MP_ENVIRONMENT", "development")
os.environ.setdefault("MP_DATABASE_URL", "sqlite:////tmp/run/data/mp.db")
sys.path.insert(0, "/tmp/run/MP/mp-app/backend")
EVIDENCE = Path(os.environ.get("AUDIT_EVIDENCE", "/home/user/Chat2DB/audit/evidence"))

from security.rbac import enforce, get_enforcer  # noqa: E402

PATHS = [
    ("GET", "/api/v1/shop/products"),
    ("GET", "/api/v1/members"),
    ("GET", "/api/v1/admin/analytics/churn-risk"),
    ("GET", "/api/v1/payments"),
    ("POST", "/api/v1/expenses"),
]


def deep_call(depth: int, fn):
    """پشتهٔ عمیق مصنوعی — معادل زنجیرهٔ middleware + routing فست‌آی‌پی."""
    if depth <= 0:
        return fn()
    return deep_call(depth - 1, fn)


def main() -> None:
    threads = int(sys.argv[1]) if len(sys.argv) > 1 else 80
    depth = int(sys.argv[2]) if len(sys.argv) > 2 else 40
    calls = int(sys.argv[3]) if len(sys.argv) > 3 else 400

    get_enforcer()
    errors: Counter = Counter()
    lat: list[float] = []
    lock = threading.Lock()
    samples: list[str] = []

    def work(tid: int) -> None:
        local: Counter = Counter()
        local_lat: list[float] = []
        for i in range(calls):
            method, path = PATHS[(tid + i) % len(PATHS)]
            t0 = time.perf_counter()
            try:
                deep_call(depth, lambda: enforce("super_admin", path, method))
            except SystemError as exc:
                local["SystemError"] += 1
                with lock:
                    if len(samples) < 5:
                        samples.append(f"SystemError: {exc}")
            except RecursionError as exc:
                local["RecursionError"] += 1
                with lock:
                    if len(samples) < 5:
                        samples.append(f"RecursionError: {exc}")
            except BaseException as exc:  # noqa: BLE001
                local[type(exc).__name__] += 1
                with lock:
                    if len(samples) < 5:
                        samples.append(f"{type(exc).__name__}: {exc}")
            local_lat.append((time.perf_counter() - t0) * 1000)
        with lock:
            errors.update(local)
            lat.extend(local_lat)

    print(f"threads={threads} stack_depth={depth} calls_per_thread={calls} "
          f"recursionlimit={sys.getrecursionlimit()}")
    t0 = time.time()
    ts = [threading.Thread(target=work, args=(i,)) for i in range(threads)]
    for t in ts:
        t.start()
    for t in ts:
        t.join()
    elapsed = time.time() - t0

    out = {
        "threads": threads, "stack_depth": depth, "calls_per_thread": calls,
        "total_calls": threads * calls,
        "elapsed_s": round(elapsed, 1),
        "throughput_calls_per_s": round(threads * calls / elapsed, 1),
        "errors": dict(errors),
        "error_samples": samples,
        "latency_ms": {
            "p50": round(statistics.median(lat), 3) if lat else None,
            "p95": round(sorted(lat)[int(0.95 * (len(lat) - 1))], 3) if lat else None,
            "max": round(max(lat), 3) if lat else None,
        },
        "note": "casbin روی هر enforce عبارت را compile/eval می‌کند؛ "
                "enable_cache در security/rbac.py فعال نشده است.",
    }
    print(json.dumps(out, ensure_ascii=False, indent=1))
    prev = EVIDENCE / "rbac-systemerror-repro.json"
    rows = []
    if prev.exists():
        rows = json.loads(prev.read_text(encoding="utf-8"))
        if isinstance(rows, dict):
            rows = [rows]
    rows.append(out)
    prev.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"→ {prev}")


if __name__ == "__main__":
    main()
