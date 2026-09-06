"""Liveness/readiness probe.

``/health`` is the Phase 0 contract: the Studio shell polls it to decide
whether the local core is up before it renders anything but the loader.
"""

from __future__ import annotations

from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.engine import Engine

from app import __version__
from app.config import SERVICE_NAME
from app.migrations import schema_version
from app.state import get_engine

router = APIRouter(tags=["health"])


@router.get("/health", summary="Core liveness + schema readiness")
def health(engine: Engine = Depends(get_engine)) -> dict[str, Any]:
    """Report process, database and schema-migration state.

    Returns:
        ``{"status": "ok"|"degraded", "service", "version", "db": {...}}``.
        Never raises: a broken database is reported as ``degraded`` so the
        Studio shell can show a recovery action instead of a blank screen.
    """
    db_info: dict[str, Any] = {"ok": False}
    status = "ok"

    try:
        with engine.connect() as conn:
            sqlite_version = conn.execute(text("select sqlite_version()")).scalar()
            table_count = conn.execute(
                text(
                    "SELECT count(*) FROM sqlite_master "
                    "WHERE type='table' AND name NOT LIKE 'sqlite_%'"
                )
            ).scalar()
        db_info = {
            "ok": True,
            "sqlite_version": sqlite_version,
            "table_count": table_count,
            "schema_version": schema_version(engine),
        }
    except Exception as exc:  # pragma: no cover - defensive, surfaced as degraded
        status = "degraded"
        db_info = {"ok": False, "error": f"{type(exc).__name__}: {exc}"}

    return {
        "status": status,
        "service": SERVICE_NAME,
        "version": __version__,
        "api_prefix": "/api/v1",
        "db": db_info,
    }
