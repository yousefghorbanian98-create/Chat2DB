"""SQLite engine/session plumbing.

Foreign keys are enforced per-connection (SQLite default is OFF, which would
silently allow orphan rows — unacceptable for sync tombstones).
"""

from __future__ import annotations

from collections.abc import Iterator
from pathlib import Path

from sqlalchemy import create_engine, event, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker


def make_engine(db_path: Path, *, echo: bool = False) -> Engine:
    """Create a SQLite engine, ensuring the parent directory exists."""
    if str(db_path) != ":memory:":
        db_path.parent.mkdir(parents=True, exist_ok=True)

    engine = create_engine(
        f"sqlite:///{db_path}",
        echo=echo,
        future=True,
        connect_args={"check_same_thread": False},
    )

    @event.listens_for(engine, "connect")
    def _pragmas(dbapi_conn, _record):  # pragma: no cover - driver callback
        cur = dbapi_conn.cursor()
        cur.execute("PRAGMA foreign_keys = ON")
        cur.execute("PRAGMA journal_mode = WAL")
        # Peak hour puts the kiosk scanner and the reception till on the same
        # file. Without a busy timeout the loser of that race gets an immediate
        # SQLITE_BUSY (a 500 for a paying member), instead of waiting 5ms.
        cur.execute("PRAGMA busy_timeout = 5000")
        # Safe with WAL (a crash can lose the last commit, not corrupt the DB)
        # and several times faster on the spinning disks gym PCs still ship.
        cur.execute("PRAGMA synchronous = NORMAL")
        cur.close()

    return engine


def make_session_factory(engine: Engine) -> sessionmaker[Session]:
    """Session factory bound to ``engine``."""
    return sessionmaker(bind=engine, expire_on_commit=False, future=True)


def session_scope(factory: sessionmaker[Session]) -> Iterator[Session]:
    """FastAPI dependency yielding a session that always closes."""
    session = factory()
    try:
        yield session
    finally:
        session.close()


def table_names(engine: Engine) -> list[str]:
    """All user tables in the connected database, sorted."""
    with engine.connect() as conn:
        rows = conn.execute(
            text("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        ).all()
    return [r[0] for r in rows]


def foreign_keys_enabled(engine: Engine) -> bool:
    """True when the PRAGMA really took effect on a live connection."""
    with engine.connect() as conn:
        return bool(conn.execute(text("PRAGMA foreign_keys")).scalar())
