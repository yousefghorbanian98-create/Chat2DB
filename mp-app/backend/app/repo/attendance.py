"""Attendance check-in/out data access (map §3 #10, DoD #5)."""

from __future__ import annotations

from typing import Any

from sqlalchemy import text
from sqlalchemy.engine import Engine

_COLS = "id, member_id, checked_in, checked_out, method, staff_id, created_at"


class AttendanceNotFound(LookupError):
    """No open attendance row with that id."""


def open_visit(engine: Engine, gym_id: int, member_id: int) -> dict[str, Any] | None:
    """The member's currently-open visit (checked_out IS NULL), if any."""
    with engine.connect() as conn:
        row = conn.execute(
            text(
                f"SELECT {_COLS} FROM attendance "
                "WHERE gym_id = :g AND member_id = :m AND checked_out IS NULL "
                "AND deleted_at IS NULL ORDER BY id DESC LIMIT 1"
            ),
            {"g": gym_id, "m": member_id},
        ).mappings().first()
    return dict(row) if row else None


def check_in(
    engine: Engine,
    gym_id: int,
    member_id: int,
    *,
    method: str = "qr",
    qr_sig: str | None = None,
    staff_id: int | None = None,
) -> int:
    """Open a visit. Returns the attendance id."""
    with engine.begin() as conn:
        cur = conn.execute(
            text(
                "INSERT INTO attendance (gym_id, member_id, checked_in, method, "
                "qr_sig, staff_id) "
                "VALUES (:g, :m, strftime('%Y-%m-%dT%H:%M:%fZ', 'now'), :method, "
                ":sig, :staff)"
            ),
            {
                "g": gym_id,
                "m": member_id,
                "method": method,
                "sig": qr_sig,
                "staff": staff_id,
            },
        )
        return int(cur.lastrowid or 0)


def check_out(engine: Engine, gym_id: int, attendance_id: int) -> dict[str, Any]:
    """Close an open visit."""
    with engine.begin() as conn:
        cur = conn.execute(
            text(
                "UPDATE attendance SET checked_out = strftime('%Y-%m-%dT%H:%M:%fZ', 'now'), "
                "rev = rev + 1 WHERE id = :id AND gym_id = :g AND deleted_at IS NULL"
            ),
            {"id": attendance_id, "g": gym_id},
        )
        if cur.rowcount == 0:
            raise AttendanceNotFound(f"attendance {attendance_id} not found")
        row = conn.execute(
            text(f"SELECT {_COLS} FROM attendance WHERE id = :id"), {"id": attendance_id}
        ).mappings().one()
    return dict(row)


def count_today(engine: Engine, gym_id: int, today_prefix: str) -> int:
    """Visits that started on the given UTC date (YYYY-MM-DD)."""
    with engine.connect() as conn:
        return int(
            conn.execute(
                text(
                    "SELECT count(*) FROM attendance "
                    "WHERE gym_id = :g AND checked_in LIKE :p AND deleted_at IS NULL"
                ),
                {"g": gym_id, "p": f"{today_prefix}%"},
            ).scalar()
            or 0
        )
