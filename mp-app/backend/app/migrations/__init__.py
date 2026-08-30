"""Tiny deterministic migration runner.

Alembic is deliberately not a Phase 0 dependency: MP needs migrations that run
on an air-gapped gym PC from a plain ``pip install -r requirements.txt``. The
contract is small and tested:

* each migration has an ordered ``version`` and a content checksum;
* applying is idempotent (re-running is a no-op);
* re-applying a migration whose SQL changed raises ``MigrationDriftError``
  instead of silently diverging two gyms' schemas.
"""

from __future__ import annotations

from collections.abc import Iterable

from sqlalchemy import text
from sqlalchemy.engine import Engine

from app.migrations.base import (
    Migration,
    MigrationDriftError,
    MigrationError,
)
from app.migrations.v001_core import MIGRATION as V001
from app.migrations.v002_member_pin import MIGRATION as V002
from app.migrations.v003_workout_logs import MIGRATION as V003

__all__ = [
    "MIGRATIONS",
    "Migration",
    "MigrationDriftError",
    "MigrationError",
    "applied_migrations",
    "migrate",
    "schema_version",
]


MIGRATIONS: tuple[Migration, ...] = (V001, V002, V003)

_TRACKING_TABLE = "schema_migrations"


def _ensure_tracking(conn) -> None:
    conn.execute(
        text(
            f"""
            CREATE TABLE IF NOT EXISTS {_TRACKING_TABLE} (
                version     TEXT PRIMARY KEY,
                label       TEXT NOT NULL,
                checksum    TEXT NOT NULL,
                applied_at  TEXT NOT NULL
                    DEFAULT (strftime('%Y-%m-%dT%H:%M:%fZ', 'now'))
            )
            """
        )
    )


def applied_migrations(engine: Engine) -> dict[str, str]:
    """``{version: checksum}`` for everything already applied."""
    with engine.begin() as conn:
        _ensure_tracking(conn)
        rows = conn.execute(
            text(f"SELECT version, checksum FROM {_TRACKING_TABLE}")
        ).all()
    return {r[0]: r[1] for r in rows}


def migrate(engine: Engine, migrations: Iterable[Migration] = MIGRATIONS) -> list[str]:
    """Apply pending migrations in order. Returns versions applied this run.

    Raises:
        MigrationDriftError: a recorded checksum differs from the code's SQL.
    """
    applied_now: list[str] = []
    with engine.begin() as conn:
        _ensure_tracking(conn)
        known = {
            r[0]: r[1]
            for r in conn.execute(
                text(f"SELECT version, checksum FROM {_TRACKING_TABLE}")
            ).all()
        }
        for mig in sorted(migrations, key=lambda m: m.version):
            if mig.version in known:
                if known[mig.version] != mig.checksum:
                    raise MigrationDriftError(
                        f"migration {mig.version} changed after being applied "
                        f"(recorded {known[mig.version][:12]}..., "
                        f"now {mig.checksum[:12]}...)"
                    )
                continue
            for stmt in mig.statements:
                conn.execute(text(stmt))
            conn.execute(
                text(
                    f"INSERT INTO {_TRACKING_TABLE} (version, label, checksum) "
                    "VALUES (:v, :l, :c)"
                ),
                {"v": mig.version, "l": mig.label, "c": mig.checksum},
            )
            applied_now.append(mig.version)
    return applied_now


def schema_version(engine: Engine) -> str | None:
    """Highest applied migration version, or ``None`` on a fresh database."""
    versions = applied_migrations(engine)
    return max(versions) if versions else None
