#!/usr/bin/env python3
"""بار پله‌ای + اندازه‌گیری «زمان بازیابی» — گروه کنترل برای A1.

برای هر پلهٔ همزمانی (۲۰/۴۰/۶۰/۸۰/۱۲۰/۲۰۰) اندازه می‌گیرد:
  • شمار پاسخ‌ها بر اساس status (۲xx/۴xx/۵xx/timeout)
  • p50/p95/p99/max تأخیر و توان عملیاتی (rps)
  • زنده بودن `/health` **در حین بار** (هر ۵۰۰ms)
  • پس از پایان بار: **زمان بازیابی** = مدت تا نخستین `/health` با ۲۰۰
  • اگر سرور ابزارِ pool داشته باشد: بیشترین `checkedout` دیده‌شده

شاهد پس از هر پله روی دیسک نوشته می‌شود (تا اگر پروسه قفل کرد، داده از دست نرود).

اجرا:  /tmp/run/venv/bin/python audit/probe_load.py [tag] [workers...]
مثال:  /tmp/run/venv/bin/python audit/probe_load.py plain-dev 20 40 60 80 120 200
"""
from __future__ import annotations

import json
import statistics
import sys
import threading
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import httpx

sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness_common import BASE, write_evidence  # noqa: E402

STEP_SECONDS = float(sys.argv[3]) if len(sys.argv) > 3 and sys.argv[3].replace(".", "").isdigit() else 12.0
TAG = sys.argv[1] if len(sys.argv) > 1 else "run"
WORKERS = [int(x) for x in sys.argv[2].split(",")] if len(sys.argv) > 2 and "," in sys.argv[2] else (
    [int(x) for x in sys.argv[2:]] if len(sys.argv) > 2 else [20, 40, 60, 80, 120, 200]
)

READ_TASKS = [
    ("GET", "/api/v1/admin/analytics/churn-risk"),
    ("GET", "/api/v1/admin/analytics/leaderboards"),
    ("GET", "/api/v1/members"),
    ("GET", "/api/v1/reports/financial/summary"),
    ("GET", "/api/v1/payments"),
    ("GET", "/api/v1/shop/products"),
    ("GET", "/api/v1/exercises"),
    ("GET", "/api/v1/nutrition/foods"),
]


def pct(vals: list[float], p: float) -> float:
    if not vals:
        return 0.0
    s = sorted(vals)
    return round(s[max(0, min(len(s) - 1, int(round(p / 100 * (len(s) - 1)))))], 1)


def snapshot(url: str) -> dict | None:
    try:
        r = httpx.get(url, timeout=5)
        return r.json() if r.status_code == 200 else None
    except Exception:  # noqa: BLE001
        return None


def classify_error(text: str) -> str:
    t = (text or "").lower()
    if "queuepool" in t:
        return "queuepool_timeout"
    if "database is locked" in t:
        return "sqlite_locked"
    if "internal_error" in t:
        return "unhandled_500"
    if "timeout" in t:
        return "timeout"
    if "rate limit" in t or "too many" in t:
        return "rate_limited"
    return "other"


def run_step(workers: int, headers: dict, duration: float) -> dict:
    lat: list[float] = []
    codes: Counter = Counter()
    errs: Counter = Counter()
    samples: list[dict] = []
    health: list[tuple[float, int | None]] = []
    lock = threading.Lock()
    deadline = time.time() + duration

    def sampler() -> None:
        while time.time() < deadline:
            snap = snapshot(f"{BASE}/audit/pool")
            if snap:
                samples.append({"checkedout": snap.get("pool_checkedout"),
                                "overflow": snap.get("pool_overflow"),
                                "leak": snap.get("leak_suspect")})
            time.sleep(0.15)

    def health_probe() -> None:
        while time.time() < deadline + 30:
            t0 = time.perf_counter()
            try:
                r = httpx.get(f"{BASE}/health", timeout=5)
                code: int | None = r.status_code
            except Exception:  # noqa: BLE001
                code = None
            ms = (time.perf_counter() - t0) * 1000
            with lock:
                health.append((round(ms, 1), code))
            time.sleep(0.5)

    def worker(i: int) -> None:
        local_lat: list[float] = []
        local_codes: Counter = Counter()
        local_errs: Counter = Counter()
        method, path = READ_TASKS[i % len(READ_TASKS)]
        try:
            with httpx.Client(base_url=BASE, timeout=30.0) as c:
                while time.time() < deadline:
                    t0 = time.perf_counter()
                    try:
                        r = c.request(method, path, headers=headers)
                        code: int | None = r.status_code
                        body = r.text[:200]
                    except Exception as exc:  # noqa: BLE001
                        code, body = None, f"{type(exc).__name__}"
                    local_lat.append((time.perf_counter() - t0) * 1000)
                    local_codes[code] += 1
                    if code is None or code >= 500:
                        local_errs[classify_error(body)] += 1
        except Exception as exc:  # noqa: BLE001
            local_errs[f"client_dead:{type(exc).__name__}"] += 1
        with lock:
            lat.extend(local_lat)
            codes.update(local_codes)
            errs.update(local_errs)

    st = threading.Thread(target=sampler, daemon=True)
    hp = threading.Thread(target=health_probe, daemon=True)
    st.start()
    hp.start()
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=workers) as ex:
        list(ex.map(worker, range(workers)))
    elapsed = time.time() - t0

    # زمان بازیابی: از پایان بار تا نخستین /health موفق
    recovery_t0 = time.time()
    recovered: float | None = None
    while time.time() - recovery_t0 < 240:
        try:
            r = httpx.get(f"{BASE}/health", timeout=5)
            if r.status_code == 200:
                recovered = round(time.time() - recovery_t0, 2)
                break
        except Exception:  # noqa: BLE001
            pass
        time.sleep(0.25)
    hp.join(timeout=2)

    checked = [s["checkedout"] for s in samples if s.get("checkedout") is not None]
    out = {
        "tag": TAG,
        "workers": workers,
        "step_seconds": round(elapsed, 1),
        "requests": len(lat),
        "rps": round(len(lat) / elapsed, 1) if elapsed else 0,
        "status_counts": {str(k): v for k, v in codes.most_common()},
        "error_kinds": dict(errs.most_common()),
        "p50_ms": pct(lat, 50), "p95_ms": pct(lat, 95),
        "p99_ms": pct(lat, 99), "max_ms": round(max(lat), 1) if lat else None,
        "client_timeouts": codes.get(None, 0),
        "server_errors_5xx": sum(v for k, v in codes.items() if isinstance(k, int) and k >= 500),
        "max_pool_checkedout_observed": max(checked) if checked else None,
        "pool_samples": len(samples),
        "health_during_load": {
            "probes": len(health),
            "failed_probes": sum(1 for _, c in health if c != 200),
            "max_health_ms": max((h[0] for h in health), default=None),
        },
        "recovery_seconds": recovered if recovered is not None else ">240 (بازیابی نکرد)",
    }
    return out


def main() -> None:
    from harness_common import Principals

    pr = Principals()
    headers = pr.headers("super_admin")
    print(f"[{TAG}] BASE={BASE} steps={WORKERS} step_seconds={STEP_SECONDS}")
    all_rows: list[dict] = []
    for w in WORKERS:
        row = run_step(w, headers, STEP_SECONDS)
        all_rows.append(row)
        print(json.dumps(row, ensure_ascii=False))
        write_evidence(f"load-{TAG}.json", {"tag": TAG, "rows": all_rows,
                                            "updated_at": time.strftime("%H:%M:%S")})
        time.sleep(4)
    print(f"\n→ evidence/load-{TAG}.json")


if __name__ == "__main__":
    main()
