#!/usr/bin/env python3
"""سرور کنترل (بدون هیچ ابزار دقیق) — برای جدا کردن اثر instrumentation.

`serve_backend.py` در هر رویداد `checkout`/`checkin` یک ردیف JSONL روی دیسک
می‌نویسد و همهٔ آن نوشتن‌ها زیر یک `threading.Lock` سراسری است. برای اینکه
معلوم شود اشباع استخر **واقعاً** خاصیت خودِ اپ است نه سربارِ ابزارِ ممیزی،
این لانچر هیچ listener‌ای ثبت نمی‌کند و فقط `uvicorn.run(app)` است.

`AUDIT_LOG_FORMAT=json` ⇒ پیکربندی لاگِ production (برای آزمون کنترل‌شدهٔ دوم).
"""
from __future__ import annotations

import os
import sys
from pathlib import Path

PORT = int(os.environ.get("AUDIT_PORT", "8010"))
HOST = os.environ.get("AUDIT_HOST", "0.0.0.0")
BACKEND = "/tmp/run/MP/mp-app/backend"

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

from app.main import app  # noqa: E402

if os.environ.get("AUDIT_LOG_FORMAT", "dev") == "json":
    from app.logging import configure_logging

    configure_logging(json_logs=True)
    print("[plain] log format = JSON", flush=True)
else:
    print("[plain] log format = ConsoleRenderer+rich (development default)", flush=True)

if __name__ == "__main__":
    import uvicorn

    print(f"[plain] no pool instrumentation — listening on {HOST}:{PORT}", flush=True)
    uvicorn.run(app, host=HOST, port=PORT, log_level="warning", workers=1)
