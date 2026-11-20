#!/usr/bin/env python3
"""میکروبنچمارک: هزینهٔ `logger.exception` در دو پیکربندی لاگِ خودِ پروژه.

چرا لازم است؟ در آزمون بار، پشتهٔ اصلی (py-spy) نشان داد event loop در
`structlog.dev.ConsoleRenderer → RichTracebackFormatter → rich.Table._render`
گیر کرده بود. این اسکریپت همان مسیر را با عمق پشتهٔ قابل تنظیم اندازه می‌گیرد:

  • زمان هر فراخوانی (ms) — این زمان **روی نخ event loop** صرف می‌شود
  • بایت خروجی تولیدشده برای هر خطا
  • مقایسه با `JSONRenderer` (پیکربندی production)

خروجی: evidence/logging-cost.json
اجرا: /tmp/run/venv/bin/python audit/bench_logging.py
"""
from __future__ import annotations

import io
import json
import os
import statistics
import sys
import time
from contextlib import redirect_stdout
from pathlib import Path

os.environ.setdefault("MP_ENVIRONMENT", "development")
os.environ.setdefault("MP_DATABASE_URL", "sqlite:////tmp/run/data/mp.db")
sys.path.insert(0, "/tmp/run/MP/mp-app/backend")
EVIDENCE = Path(os.environ.get("AUDIT_EVIDENCE", "/home/user/Chat2DB/audit/evidence"))


def make_deep_error(depth: int) -> BaseException:
    """خطایی با پشتهٔ عمیق — همان شکلِ TimeoutErrorِ QueuePool زیر بار."""
    from sqlalchemy.exc import TimeoutError as SATimeoutError

    def nest(i: int) -> None:
        if i <= 0:
            raise SATimeoutError(
                "QueuePool limit of size 40 overflow 20 reached, "
                "connection timed out, timeout 5.00"
            )
        nest(i - 1)

    try:
        nest(depth)
    except BaseException as exc:  # noqa: BLE001
        return exc
    raise AssertionError("unreachable")


def bench(json_logs: bool, depth: int, repeats: int = 5) -> dict:
    from app.logging import configure_logging, get_logger

    configure_logging(json_logs=json_logs)
    log = get_logger("mp.errors")
    exc = make_deep_error(depth)
    times: list[float] = []
    buf = io.StringIO()
    with redirect_stdout(buf):
        for _ in range(repeats):
            t0 = time.perf_counter()
            try:
                raise exc
            except BaseException:  # noqa: BLE001
                log.exception(
                    "unhandled_error",
                    method="GET",
                    path="/api/v1/admin/analytics/churn-risk",
                    error_type=type(exc).__name__,
                )
            times.append((time.perf_counter() - t0) * 1000)
    out = buf.getvalue()
    return {
        "renderer": "JSONRenderer (production)" if json_logs else "ConsoleRenderer+rich (development)",
        "traceback_depth": depth,
        "repeats": repeats,
        "mean_ms": round(statistics.mean(times), 2),
        "median_ms": round(statistics.median(times), 2),
        "max_ms": round(max(times), 2),
        "bytes_per_error": round(len(out.encode("utf-8")) / repeats),
        "lines_per_error": round(out.count("\n") / repeats),
    }


def main() -> None:
    rows = []
    for depth in (10, 25, 40, 60):
        for json_logs in (False, True):
            r = bench(json_logs, depth)
            rows.append(r)
            print(f"  depth={depth:>3} {r['renderer']:<42} "
                  f"mean={r['mean_ms']:>8}ms  bytes/err={r['bytes_per_error']:>9}  "
                  f"lines/err={r['lines_per_error']:>7}")
    payload = {
        "note": "زمان‌ها روی نخ event loop صرف می‌شوند؛ یعنی در همان مدت هیچ "
                "درخواست دیگری (حتی /health) سرو نمی‌شود.",
        "rows": rows,
    }
    p = EVIDENCE / "logging-cost.json"
    p.write_text(json.dumps(payload, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\n→ {p}")


if __name__ == "__main__":
    main()
