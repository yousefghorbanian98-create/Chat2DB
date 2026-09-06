"""Per-app mutable state (engine + session factory) held off the module level.

A module-global engine makes tests order-dependent and makes it impossible to
run two gyms in one process; this keeps the dependency explicit and injectable.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.security import load_or_create_secret_key
from app.db import make_engine, make_session_factory
from app.migrations import migrate


@dataclass
class AppState:
    """Container handed to ``create_app`` and exposed via dependencies."""

    engine: Engine
    session_factory: sessionmaker[Session]
    secret_key: str = ""
    gym_name: str = "Muscle Paradise"

    @classmethod
    def open(
        cls, db_path: Path, *, echo: bool = False, secret_key: str = "", gym_name: str = "Muscle Paradise"
    ) -> "AppState":
        """Open the database, run pending migrations, return ready state."""
        engine = make_engine(db_path, echo=echo)
        migrate(engine)
        key = secret_key or load_or_create_secret_key(db_path.parent / "secret.key")
        return cls(
            engine=engine,
            session_factory=make_session_factory(engine),
            secret_key=key,
            gym_name=gym_name,
        )

    def dispose(self) -> None:
        """Release pooled connections (used by tests and shutdown hooks)."""
        self.engine.dispose()


_STATE: AppState | None = None


def set_state(state: AppState) -> None:
    """Install the process-wide state (called once by ``create_app``)."""
    global _STATE  # noqa: PLW0603 - single intentional process-wide slot
    _STATE = state


def get_state() -> AppState:
    """Current state, or a clear error if the app was never created."""
    if _STATE is None:
        raise RuntimeError("AppState not initialised — call create_app() first")
    return _STATE


def get_engine() -> Engine:
    """FastAPI dependency: the shared SQLAlchemy engine."""
    return get_state().engine


def get_secret_key() -> str:
    """Machine-local key used for session tokens and QR signatures."""
    return get_state().secret_key


def get_gym_name() -> str:
    """Display name used in reports and the /meta endpoint."""
    return get_state().gym_name


def get_session() -> Session:
    """FastAPI dependency: a request-scoped session."""
    state = get_state()
    session = state.session_factory()
    try:
        yield session
    finally:
        session.close()
