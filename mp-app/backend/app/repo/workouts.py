"""Athlete workout session log (map §5, migration 0003).

One row per completed session. The session itself is JSON (`payload`) because a
set/rep ladder is a list, not a column — but every query is parameterized and
every read is scoped by `gym_id` + `member_id`, so an athlete can never reach
another member's log.
"""

from __future__ import annotations

import json
from typing import Any

from sqlalchemy import text
from sqlalchemy.engine import Engine

_COLS = (
    "id, member_id, program_id, session_date, payload, athlete_note, created_at"
)


def add_log(
    engine: Engine,
    gym_id: int,
    member_id: int,
    *,
    session_date: str,
    payload: str,
    program_id: int | None = None,
    athlete_note: str | None = None,
) -> int:
    """Insert one session log and return its id."""
    with engine.begin() as conn:
        result = conn.execute(
            text(
                "INSERT INTO workout_logs "
                "(gym_id, member_id, program_id, session_date, payload, athlete_note) "
                "VALUES (:g, :m, :p, :d, :payload, :note)"
            ),
            {
                "g": gym_id,
                "m": member_id,
                "p": program_id,
                "d": session_date,
                "payload": payload,
                "note": athlete_note,
            },
        )
        return int(result.lastrowid or 0)


def list_for_member(
    engine: Engine, gym_id: int, member_id: int, *, limit: int = 20
) -> list[dict[str, Any]]:
    """Newest sessions first, soft-deleted rows excluded."""
    with engine.connect() as conn:
        rows = conn.execute(
            text(
                f"SELECT {_COLS} FROM workout_logs "
                "WHERE gym_id = :g AND member_id = :m AND deleted_at IS NULL "
                "ORDER BY session_date DESC, id DESC LIMIT :lim"
            ),
            {"g": gym_id, "m": member_id, "lim": limit},
        ).mappings().all()
    return [dict(r) for r in rows]


def count_for_member(engine: Engine, gym_id: int, member_id: int) -> int:
    """How many sessions this member has logged (used for streaks/summaries)."""
    with engine.connect() as conn:
        row = conn.execute(
            text(
                "SELECT COUNT(*) FROM workout_logs "
                "WHERE gym_id = :g AND member_id = :m AND deleted_at IS NULL"
            ),
            {"g": gym_id, "m": member_id},
        ).scalar_one()
    return int(row)


def encode_session(exercises: list[dict[str, Any]]) -> str:
    """Serialize a session to the compact, key-sorted envelope the app stores."""
    return json.dumps(
        {"schema": "mp.workout/v1", "exercises": exercises},
        separators=(",", ":"),
        sort_keys=True,
    )


def decode_session(payload: str) -> list[dict[str, Any]]:
    """Read the exercise list back; a malformed envelope yields no exercises."""
    try:
        parsed = json.loads(payload)
    except json.JSONDecodeError:
        return []
    exercises = parsed.get("exercises") if isinstance(parsed, dict) else None
    return list(exercises) if isinstance(exercises, list) else []
