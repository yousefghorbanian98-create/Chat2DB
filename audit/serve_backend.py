#!/usr/bin/env python3
"""MP live-audit launcher — بک‌اند Muscle Paradise را **بدون تغییر مخزن** بالا می‌آورد.

چرا این فایل:
  مخزن `MP` برای ما فقط‌خواندنی است. پس به‌جای ویرایش کدشان، اینجا در زمان اجرا
  (runtime) سه چیز به اپ **تزریق** می‌شود:

  ۱) مشاهده‌پذیری استخر اتصال SQLAlchemy (checkout/checkin/overflow/timeout)
     → همان چیزی که در مخزن وجود ندارد و ریشه‌یابی حادثهٔ «قفل‌شدگی استخر»
       را غیرممکن کرده بود (یافتهٔ A1).
  ۲) یک مسیر فقط‌ harness ‏`GET /audit/pool` برای خواندن زندهٔ همان آمارها
     (فقط در این پروسه ثبت می‌شود؛ هیچ فایلی در مخزن عوض نمی‌شود).
  ۳) در صورت `AUDIT_OTEL=1`: ردیابی OpenTelemetry برای FastAPI + SQLAlchemy
     با صادرکنندهٔ JSONL محلی (بدون نیاز به Jaeger/کانتینر).

خروجی‌ها: `evidence/pool-events.jsonl` و `evidence/otel-spans.jsonl`.
"""
from __future__ import annotations

import json
import os
import sys
import threading
import time
from pathlib import Path

BACKEND = "/tmp/run/MP/mp-app/backend"
EVIDENCE = Path(os.environ.get("AUDIT_EVIDENCE", "/home/user/Chat2DB/audit/evidence"))
EVIDENCE.mkdir(parents=True, exist_ok=True)
HOST = os.environ.get("AUDIT_HOST", "0.0.0.0")
PORT = int(os.environ.get("AUDIT_PORT", "8010"))

# --- پیکربندی محیط (development تا اعتبارسنج production جلوی بالا آمدن را نگیرد) ---
os.environ.setdefault("MP_ENVIRONMENT", "development")
os.environ.setdefault("MP_DATABASE_URL", "sqlite:////tmp/run/data/mp.db")
os.environ.setdefault("MP_SECRET_KEY", "audit-harness-only-secret-0123456789abcdef")
os.environ.setdefault("MP_PUBLIC_BASE_URL", f"http://127.0.0.1:{PORT}")
os.environ.setdefault("MP_SMS_PROVIDER", "dev")
os.environ.setdefault("MP_PAYMENT_GATEWAY", "manual")
os.environ.setdefault("MP_RECEIPTS_DIR", "/tmp/run/data/receipts")
os.environ.setdefault("MP_TRUSTED_PROXIES", "")
Path("/tmp/run/data/receipts").mkdir(parents=True, exist_ok=True)

sys.path.insert(0, BACKEND)

import db.base as dbbase  # noqa: E402
from sqlalchemy import event  # noqa: E402

# --------------------------------------------------------------------------
# ۱) مشاهده‌پذیری استخر اتصال
# --------------------------------------------------------------------------
POOL_LOG = EVIDENCE / "pool-events.jsonl"
_lock = threading.Lock()
STATS = {
    "checkout": 0,
    "checkin": 0,
    "connect": 0,
    "close": 0,
    "detach": 0,
    "checkout_wait_ms_max": 0.0,
    "checkout_wait_ms_sum": 0.0,
    "held_ms_max": 0.0,
    "held_over_1s": 0,
    "checked_out_now": 0,
    "overflow_now": 0,
    "started_at": time.time(),
}
_wait_start: dict[int, float] = {}


def _rec(kind: str, **extra) -> None:
    row = {"t": round(time.time(), 4), "kind": kind, **extra}
    row.update(
        checked_out=STATS["checked_out_now"],
        overflow=STATS["overflow_now"],
        pool_size=ENGINE.pool.size(),
        pool_checkedout=ENGINE.pool.checkedout(),
        pool_overflow=ENGINE.pool.overflow(),
    )
    with _lock:
        with POOL_LOG.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(row, ensure_ascii=False) + "\n")


ENGINE = dbbase.get_engine()


# امضای رویدادها در نسخه‌های مختلف SQLAlchemy فرق می‌کند ⇒ *args
@event.listens_for(ENGINE.pool, "checkout")
def _on_checkout(*a, **k):
    with _lock:
        STATS["checkout"] += 1
        STATS["checked_out_now"] = ENGINE.pool.checkedout()
        STATS["overflow_now"] = ENGINE.pool.overflow()
    if len(a) >= 2:
        a[1]._audit_out = time.time()


@event.listens_for(ENGINE.pool, "checkin")
def _on_checkin(*a, **k):
    with _lock:
        STATS["checkin"] += 1
        STATS["checked_out_now"] = ENGINE.pool.checkedout()
        STATS["overflow_now"] = ENGINE.pool.overflow()
    if len(a) >= 2:
        out = getattr(a[1], "_audit_out", None)
        if out is not None:
            held_ms = (time.time() - out) * 1000.0
            with _lock:
                STATS["held_ms_max"] = max(STATS["held_ms_max"], held_ms)
                if held_ms > 1000:
                    STATS["held_over_1s"] += 1
            if held_ms > 1000:
                _rec("held_over_1s", held_ms=round(held_ms, 1))


@event.listens_for(ENGINE.pool, "connect")
def _on_connect(*a, **k):
    with _lock:
        STATS["connect"] += 1


@event.listens_for(ENGINE.pool, "close")
def _on_close(*a, **k):
    with _lock:
        STATS["close"] += 1


@event.listens_for(ENGINE.pool, "detach")
def _on_detach(*a, **k):
    with _lock:
        STATS["detach"] += 1


# --------------------------------------------------------------------------
# ۲) اپ + مسیر harness
# --------------------------------------------------------------------------
from app.main import app  # noqa: E402
from fastapi.responses import JSONResponse  # noqa: E402

# --- آزمون کنترل‌شده: قالب لاگ را مستقل از MP_ENVIRONMENT انتخاب کن ---
# `AUDIT_LOG_FORMAT=json` ⇒ همان رفتار production (JSONRenderer).
# `AUDIT_LOG_FORMAT=dev`  ⇒ ConsoleRenderer+rich (پیش‌فرض خودِ اپ در development).
_LOG_FORMAT = os.environ.get("AUDIT_LOG_FORMAT", "dev")
if _LOG_FORMAT == "json":
    from app.logging import configure_logging as _cfg

    _cfg(json_logs=True)
    print("[harness] log format = JSON (production-style)", flush=True)
else:
    print("[harness] log format = ConsoleRenderer+rich (development default)", flush=True)


@app.get("/audit/threads", include_in_schema=False)
async def audit_threads():  # noqa: ANN201
    """ظرفیت واقعی همزمانی: سقف threadpool در برابر سقف استخر اتصال."""
    import os as _os
    import threading as _th
    from collections import Counter as _Counter

    import anyio.to_thread as _to_thread

    limiter = _to_thread.current_default_thread_limiter()
    names = _Counter(t.name for t in _th.enumerate())
    try:
        fds = len(_os.listdir(f"/proc/{_os.getpid()}/fd"))
    except OSError:
        fds = None
    with _lock:
        snap = dict(STATS)
    return JSONResponse({
        "anyio_threadpool_total_tokens": limiter.total_tokens,
        "anyio_threads_borrowed_now": limiter.borrowed_tokens,
        "python_threads_alive": _th.active_count(),
        "thread_names": dict(names),
        "open_fds": fds,
        "pool_size": ENGINE.pool.size(),
        "pool_checkedout": ENGINE.pool.checkedout(),
        "pool_overflow": ENGINE.pool.overflow(),
        "pool_capacity": ENGINE.pool.size() + max(ENGINE.pool.overflow(), 0),
        "capacity_verdict": (
            "POOL_TOO_SMALL: threadpool می‌تواند بیشتر از ظرفیت استخر درخواست همزمان بدهد"
            if limiter.total_tokens > ENGINE.pool.size() + max(ENGINE.pool.overflow(), 0)
            else "pool ظرفیت کافی برای سقف threadpool دارد"
        ),
        "events": {k: snap[k] for k in ("checkout", "checkin", "connect", "close", "detach")},
    })


@app.get("/audit/pool", include_in_schema=False)
def audit_pool():  # noqa: ANN201
    """فقط در همین پروسهٔ harness — در مخزن ثبت نمی‌شود."""
    with _lock:
        snap = dict(STATS)
    size = ENGINE.pool.size()
    overflow = ENGINE.pool.overflow()
    snap.update(
        pool_size=size,
        pool_checkedout=ENGINE.pool.checkedout(),
        pool_overflow=overflow,
        pool_capacity=size + max(overflow, 0),
        uptime_s=round(time.time() - snap["started_at"], 1),
        leak_suspect=snap["checkout"] - snap["checkin"],
    )
    return JSONResponse(snap)


@app.post("/audit/pool-log", include_in_schema=False)
def audit_pool_log():  # noqa: ANN201
    _rec("manual_marker")
    return JSONResponse({"ok": True})


# --------------------------------------------------------------------------
# ۳) ردیابی OpenTelemetry (اختیاری)
# --------------------------------------------------------------------------
if os.environ.get("AUDIT_OTEL") == "1":
    from opentelemetry import trace
    from opentelemetry.sdk.resources import Resource
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor, SpanExporter, SpanExportResult
    from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    from opentelemetry.instrumentation.sqlalchemy import SQLAlchemyInstrumentor

    SPANS = EVIDENCE / "otel-spans.jsonl"

    class JsonlExporter(SpanExporter):
        def export(self, spans):
            with SPANS.open("a", encoding="utf-8") as fh:
                for s in spans:
                    fh.write(json.dumps(json.loads(s.to_json()), ensure_ascii=False) + "\n")
            return SpanExportResult.SUCCESS

        def shutdown(self):
            return None

    provider = TracerProvider(resource=Resource.create({"service.name": "mp-audit-harness"}))
    provider.add_span_processor(BatchSpanProcessor(JsonlExporter(), max_export_batch_size=64,
                                                   schedule_delay_millis=1000))
    trace.set_tracer_provider(provider)
    FastAPIInstrumentor.instrument_app(app)
    SQLAlchemyInstrumentor().instrument(engine=ENGINE)
    print("[harness] OpenTelemetry ON → evidence/otel-spans.jsonl", flush=True)

# --------------------------------------------------------------------------
if __name__ == "__main__":
    import uvicorn

    print(f"[harness] pool_size={ENGINE.pool.size()} max_overflow={ENGINE.pool._max_overflow} "
          f"pool_timeout={ENGINE.pool._timeout} db={os.environ['MP_DATABASE_URL']}", flush=True)
    print(f"[harness] openapi_paths={len(app.openapi()['paths'])} listening on {HOST}:{PORT}", flush=True)
    uvicorn.run(app, host=HOST, port=PORT, log_level="warning", workers=1)
