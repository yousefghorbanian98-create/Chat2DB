"""Schema + migration runner tests (map §8 audit-column contract)."""

from __future__ import annotations

import pytest
from sqlalchemy import text

from app.db import foreign_keys_enabled, table_names
from app.migrations import (
    MIGRATIONS,
    Migration,
    MigrationDriftError,
    applied_migrations,
    migrate,
    schema_version,
)
from app.migrations.v001_core import EXPECTED_TABLES

AUDIT_COLUMNS = {"id", "gym_id", "created_at", "updated_at", "deleted_at", "rev"}


@pytest.mark.schema
def test_foreign_keys_are_actually_on(engine) -> None:
    """SQLite ships with FKs OFF; our PRAGMA must take effect."""
    assert foreign_keys_enabled(engine) is True


@pytest.mark.schema
def test_every_mapped_table_was_created(engine) -> None:
    present = set(table_names(engine))
    missing = EXPECTED_TABLES - present
    assert not missing, f"tables missing after migration: {sorted(missing)}"
    assert len(EXPECTED_TABLES) == 24


@pytest.mark.schema
@pytest.mark.parametrize("table", sorted(EXPECTED_TABLES))
def test_every_table_has_audit_columns(engine, table: str) -> None:
    """Map rule: id, gym_id, created_at, updated_at, deleted_at, rev."""
    with engine.connect() as conn:
        cols = {row[1] for row in conn.execute(text(f"PRAGMA table_info({table})"))}
    assert AUDIT_COLUMNS <= cols, f"{table} missing {sorted(AUDIT_COLUMNS - cols)}"


@pytest.mark.schema
def test_migration_is_idempotent(engine) -> None:
    """Re-running must apply nothing and change no version."""
    before = schema_version(engine)
    assert migrate(engine) == []
    assert schema_version(engine) == before == "0003_workout_logs"


@pytest.mark.schema
def test_migrations_run_in_version_order_on_fresh_db(raw_engine) -> None:
    assert schema_version(raw_engine) is None
    applied = migrate(raw_engine)
    assert applied == sorted(m.version for m in MIGRATIONS)
    assert applied_migrations(raw_engine)["0001_core"] == MIGRATIONS[0].checksum


@pytest.mark.schema
def test_checksum_drift_is_detected_not_silently_applied(engine) -> None:
    """Two gyms must never end up on different definitions of '0001_core'."""
    tampered = Migration(
        version="0001_core",
        label="tampered",
        statements=("CREATE TABLE drift_canary (id INTEGER PRIMARY KEY)",),
    )
    with pytest.raises(MigrationDriftError, match="0001_core"):
        migrate(engine, migrations=(tampered,))


@pytest.mark.schema
def test_gym_row_is_its_own_tenant_via_trigger(engine) -> None:
    """gyms.gym_id is filled from id by trg_gyms_self_tenant."""
    with engine.begin() as conn:
        conn.execute(text("INSERT INTO gyms (name) VALUES ('Muscle Paradise')"))
        row = conn.execute(text("SELECT id, gym_id FROM gyms")).one()
    assert row[1] == row[0]


@pytest.mark.schema
def test_gyms_rows_seed_and_soft_delete_columns_work(engine) -> None:
    """deleted_at/rev exist and behave — the sync fabric depends on it."""
    with engine.begin() as conn:
        conn.execute(text("INSERT INTO gyms (name) VALUES ('Muscle Paradise')"))
        gym_id = conn.execute(text("SELECT id FROM gyms")).scalar()
        conn.execute(
            text(
                "INSERT INTO members (gym_id, membership_code, first_name, "
                "last_name, sex) VALUES (:g, 'MP-0001', 'Sara', 'Azad', 'female')"
            ),
            {"g": gym_id},
        )
        conn.execute(
            text("UPDATE members SET deleted_at = '2026-08-29', rev = 2 WHERE gym_id = :g"),
            {"g": gym_id},
        )
        row = conn.execute(
            text("SELECT deleted_at, rev FROM members WHERE gym_id = :g"), {"g": gym_id}
        ).one()
    assert row[0] == "2026-08-29"
    assert row[1] == 2


@pytest.mark.schema
def test_foreign_key_violation_is_rejected(engine) -> None:
    """Orphan members (no gym) must be impossible."""
    from sqlalchemy.exc import IntegrityError

    with engine.begin() as conn, pytest.raises(IntegrityError):
        conn.execute(
            text(
                "INSERT INTO members (gym_id, membership_code, first_name, "
                "last_name, sex) VALUES (999, 'X', 'A', 'B', 'male')"
            )
        )


@pytest.mark.schema
def test_role_check_constraint_enforces_rbac_vocab(engine) -> None:
    from sqlalchemy.exc import IntegrityError

    with engine.begin() as conn:
        conn.execute(text("INSERT INTO gyms (name) VALUES ('G')"))
        gym_id = conn.execute(text("SELECT id FROM gyms")).scalar()
        with pytest.raises(IntegrityError):
            conn.execute(
                text(
                    "INSERT INTO staff (gym_id, username, role) "
                    "VALUES (:g, 'x', 'SUPERUSER')"
                ),
                {"g": gym_id},
            )
