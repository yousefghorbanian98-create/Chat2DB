"""Gym + staff data access (bootstrap and PIN login)."""

from __future__ import annotations

from typing import Any

from sqlalchemy import text
from sqlalchemy.engine import Engine

from app.core.security import hash_secret

_STAFF_COLUMNS = (
    "id, gym_id, username, pin_hash, role, full_name, active, created_at"
)


def ensure_gym(engine: Engine, name: str = "Muscle Paradise") -> int:
    """Create the single local gym row if absent; return its id."""
    with engine.begin() as conn:
        row = conn.execute(text("SELECT id FROM gyms ORDER BY id LIMIT 1")).first()
        if row is not None:
            return int(row[0])
        cur = conn.execute(
            text("INSERT INTO gyms (name) VALUES (:n)"), {"n": name}
        )
        gym_id = cur.lastrowid or conn.execute(text("SELECT last_insert_rowid()")).scalar()
    return int(gym_id)


def create_staff(
    engine: Engine,
    *,
    gym_id: int,
    username: str,
    role: str,
    pin: str,
    full_name: str | None = None,
) -> int:
    """Insert a staff account with a hashed PIN. Returns the new id."""
    with engine.begin() as conn:
        cur = conn.execute(
            text(
                "INSERT INTO staff (gym_id, username, pin_hash, role, full_name) "
                "VALUES (:g, :u, :p, :r, :f)"
            ),
            {
                "g": gym_id,
                "u": username,
                "p": hash_secret(pin),
                "r": role,
                "f": full_name,
            },
        )
        return int(cur.lastrowid or 0)


def find_staff_by_username(engine: Engine, gym_id: int, username: str) -> dict[str, Any] | None:
    """Fetch an active staff row (pin_hash included) for login checks."""
    with engine.connect() as conn:
        row = conn.execute(
            text(
                f"SELECT {_STAFF_COLUMNS} FROM staff "
                "WHERE gym_id = :g AND username = :u AND active = 1 AND deleted_at IS NULL"
            ),
            {"g": gym_id, "u": username},
        ).mappings().first()
    return dict(row) if row else None


def staff_can_see_member(engine: Engine, *, staff_id: int, member_id: int) -> bool:
    """TRAINER scope: only assigned members (map §2.4)."""
    with engine.connect() as conn:
        row = conn.execute(
            text(
                "SELECT 1 FROM member_trainer "
                "WHERE trainer_id = :s AND member_id = :m AND deleted_at IS NULL LIMIT 1"
            ),
            {"s": staff_id, "m": member_id},
        ).first()
    return row is not None
