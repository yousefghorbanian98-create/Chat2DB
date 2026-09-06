"""Phase 6 backup encrypt/restore — success metric: row counts match."""

from __future__ import annotations

import pytest
from sqlalchemy import text

from app.core.backup import (
    BackupError,
    create_backup,
    restore_backup,
    verify_row_counts,
)


def _counts(engine) -> dict[str, int]:
    from sqlalchemy import inspect

    out = {}
    with engine.connect() as conn:
        for t in inspect(engine).get_table_names():
            if t == "alembic_version":
                continue
            out[t] = int(conn.execute(text(f'SELECT COUNT(*) FROM "{t}"')).scalar_one())
    return out


def test_backup_is_encrypted_not_plaintext(engine) -> None:
    blob = create_backup(engine, "correct horse battery staple")
    assert blob.startswith(b"MPBK1\x00")
    # No table name or column should leak in the ciphertext.
    assert b"members" not in blob and b"first_name" not in blob


def test_restore_roundtrip_row_counts_match(engine) -> None:
    # Seed a gym + staff + member.
    from app.repo import members as members_repo
    from app.repo import staff as staff_repo

    gym_id = staff_repo.ensure_gym(engine, "Muscle Paradise")
    staff_repo.create_staff(engine, gym_id=gym_id, username="owner", role="OWNER", pin="1111")
    members_repo.create_member(
        engine, gym_id,
        {"membership_code": "MP-0001", "first_name": "Sara", "last_name": "Azad",
         "sex": "female", "birth_date": None, "phone": None, "membership_exp": None},
    )
    before = _counts(engine)
    blob = create_backup(engine, "s3cret")

    # Wipe, then restore into the same engine.
    with engine.begin() as conn:
        for t in sorted(before, reverse=True):
            conn.execute(text(f'DELETE FROM "{t}"'))
    assert _counts(engine)["members"] == 0

    counts = restore_backup(engine, blob, "s3cret")
    assert counts["members"] == before["members"] == 1
    verify_row_counts(engine, before)  # raises on any mismatch


def test_wrong_password_is_rejected(engine) -> None:
    from app.repo import staff as staff_repo

    staff_repo.ensure_gym(engine, "Muscle Paradise")
    blob = create_backup(engine, "right-password")
    with pytest.raises(BackupError, match="wrong password"):
        restore_backup(engine, blob, "wrong-password")


def test_bad_magic_is_rejected(engine) -> None:
    with pytest.raises(BackupError, match="bad magic"):
        restore_backup(engine, b"NOPE\x00garbage", "x")


def test_empty_password_rejected(engine) -> None:
    with pytest.raises(BackupError, match="password is required"):
        create_backup(engine, "")
