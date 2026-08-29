"""MP Core application factory.

Phase 0 surface on purpose is tiny — but the plumbing it establishes (CORS
allowlist, migrations on startup, structured error envelope, request ids) is
what every later module hangs off.
"""

from __future__ import annotations

import logging
import time
import uuid
from collections.abc import Awaitable, Callable
from typing import Any

from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware

from app import __version__
from app.config import API_PREFIX, Settings
from app.routers import (
    ai,
    assessments,
    attendance,
    auth,
    backup,
    client,
    equipment,
    exercises,
    health,
    injuries,
    members,
    nutrition,
    payments,
    programs,
    reports,
    sync,
)
from app.state import AppState, set_state

logger = logging.getLogger("mp.core")

_REQUEST_ID_HEADER = "x-request-id"
_START_TIME = time.monotonic()


class RequestIdMiddleware(BaseHTTPMiddleware):
    """Attach/propagate a request id so logs and ERRORS.log can be correlated."""

    async def dispatch(
        self,
        request: Request,
        call_next: Callable[[Request], Awaitable[Any]],
    ):
        request_id = request.headers.get(_REQUEST_ID_HEADER) or uuid.uuid4().hex[:12]
        request.state.request_id = request_id
        response = await call_next(request)
        response.headers[_REQUEST_ID_HEADER] = request_id
        return response


def create_app(settings: Settings, *, run_migrations: bool = True) -> FastAPI:
    """Build the FastAPI app and open its database.

    Args:
        settings: resolved runtime settings.
        run_migrations: set False only for tests that assert on a raw database.
    """
    state = AppState.open(settings.db_path, secret_key=settings.secret_key, gym_name=settings.gym_name) if run_migrations else None
    if state is not None:
        set_state(state)

    @asynccontextmanager
    async def lifespan(_: FastAPI):
        try:
            yield
        finally:
            if state is not None:
                state.dispose()

    app = FastAPI(
        title="Muscle Paradise Core",
        version=__version__,
        description="Local-first Gym OS core API (offline-capable).",
        docs_url="/docs",
        openapi_url="/openapi.json",
        lifespan=lifespan,
    )

    # MP is single-machine; allow only the known local shells. No wildcard.
    app.add_middleware(
        CORSMiddleware,
        allow_origins=list(settings.cors_origins),
        allow_credentials=False,
        allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE"],
        allow_headers=["authorization", "content-type", _REQUEST_ID_HEADER],
    )
    app.add_middleware(RequestIdMiddleware)
    app.state.settings = settings

    @app.middleware("http")
    async def _log_requests(request: Request, call_next):
        started = time.monotonic()
        response = await call_next(request)
        elapsed_ms = (time.monotonic() - started) * 1000
        response.headers["x-response-ms"] = f"{elapsed_ms:.1f}"
        logger.info(
            "%s %s -> %s (%.1fms)",
            request.method,
            request.url.path,
            response.status_code,
            elapsed_ms,
        )
        return response

    @app.exception_handler(Exception)
    async def _unhandled(request: Request, exc: Exception) -> JSONResponse:
        """Never swallow: log with context, return a structured envelope."""
        request_id = getattr(request.state, "request_id", "-")
        logger.exception("unhandled error on %s (request_id=%s)", request.url.path, request_id)
        return JSONResponse(
            status_code=500,
            content={
                "error": {"type": type(exc).__name__, "request_id": request_id},
            },
        )

    # Map contract: GET /health at root, everything else under /api/v1.
    app.include_router(health.router)
    app.include_router(health.router, prefix=API_PREFIX)
    for module in (
        auth,
        members,
        assessments,
        injuries,
        attendance,
        payments,
        equipment,
        exercises,
        programs,
        nutrition,
        ai,
        client,
        sync,
        backup,
        reports,
    ):
        app.include_router(module.router, prefix=API_PREFIX)

    @app.get("/meta", include_in_schema=False)
    def meta() -> dict[str, object]:
        return {
            "service": "muscle-paradise-core",
            "version": __version__,
            "uptime_s": round(time.monotonic() - _START_TIME, 3),
            "db_path": str(settings.db_path),
            "gym": settings.gym_name,
        }

    return app


def create_app_from_env() -> FastAPI:
    """uvicorn ``--factory`` entry point: build the app from the environment.

    Kept separate from a module-level ``app = ...`` on purpose — importing this
    module (tests, OpenAPI export, linters) must never touch the gym database.
    """
    return create_app(Settings.from_env())
