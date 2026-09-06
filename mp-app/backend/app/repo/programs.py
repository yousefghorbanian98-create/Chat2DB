"""Training-program persistence + lifecycle (map §7 lifecycle)."""

from __future__ import annotations

from typing import Any

from sqlalchemy import text
from sqlalchemy.engine import Engine

_COLS = (
    "id, member_id, title, status, source, payload, judge_score, generated_by, "
    "approved_by, applied_at, created_at"
)

VALID_TRANSITIONS = {
    "draft": {"trainer_approved", "archived"},
    "trainer_approved": {"client_ack", "needs_review", "archived"},
    "client_ack": {"needs_review", "archived"},
    "needs_review": {"trainer_approved", "archived"},
    "archived": set(),
}


class ProgramNotFound(LookupError):
    """No live program with that id."""


class InvalidTransition(ValueError):
    """Lifecycle move not allowed by the map's state machine."""


def create_program(
    engine: Engine,
    gym_id: int,
    *,
    member_id: int,
    title: str,
    payload: str,
    source: str = "rules",
    generated_by: int | None = None,
) -> int:
    with engine.begin() as conn:
        cur = conn.execute(
            text(
                "INSERT INTO training_programs (gym_id, member_id, title, status, "
                "source, payload, generated_by) VALUES (:g, :m, :t, 'draft', :src, "
                ":p, :by)"
            ),
            {"g": gym_id, "m": member_id, "t": title, "src": source, "p": payload, "by": generated_by},
        )
        return int(cur.lastrowid or 0)


def get_program(engine: Engine, gym_id: int, program_id: int) -> dict[str, Any]:
    with engine.connect() as conn:
        row = conn.execute(
            text(
                f"SELECT {_COLS} FROM training_programs "
                "WHERE id = :i AND gym_id = :g AND deleted_at IS NULL"
            ),
            {"i": program_id, "g": gym_id},
        ).mappings().first()
    if row is None:
        raise ProgramNotFound(f"program {program_id} not found")
    return dict(row)


def list_for_member(engine: Engine, gym_id: int, member_id: int) -> list[dict[str, Any]]:
    with engine.connect() as conn:
        rows = conn.execute(
            text(
                f"SELECT {_COLS} FROM training_programs "
                "WHERE gym_id = :g AND member_id = :m AND deleted_at IS NULL "
                "ORDER BY created_at DESC"
            ),
            {"g": gym_id, "m": member_id},
        ).mappings().all()
    return [dict(r) for r in rows]


def set_status(
    engine: Engine,
    gym_id: int,
    program_id: int,
    new_status: str,
    *,
    by: int | None = None,
) -> dict[str, Any]:
    """Move through the lifecycle state machine; raise on illegal moves."""
    current = get_program(engine, gym_id, program_id)
    allowed = VALID_TRANSITIONS.get(current["status"], set())
    if new_status not in allowed:
        raise InvalidTransition(
            f"cannot move program {program_id} from {current['status']} to {new_status}"
        )

    extra = ""
    params: dict[str, Any] = {"i": program_id, "g": gym_id, "s": new_status, "by": by}
    if new_status == "trainer_approved":
        extra = ", approved_by = :by, applied_at = strftime('%Y-%m-%dT%H:%M:%fZ', 'now')"

    with engine.begin() as conn:
        conn.execute(
            text(
                f"UPDATE training_programs SET status = :s, rev = rev + 1 {extra} "
                "WHERE id = :i AND gym_id = :g AND deleted_at IS NULL"
            ),
            params,
        )
    return get_program(engine, gym_id, program_id)
