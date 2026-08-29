"""Member data access. Parameterized SQL, soft-delete only (map §8)."""

from __future__ import annotations

from typing import Any

from sqlalchemy import text
from sqlalchemy.engine import Engine

_OUT_COLUMNS = (
    "id, membership_code, first_name, last_name, sex, birth_date, phone, "
    "membership_exp, guardian_consent, created_at"
)


class MemberNotFound(LookupError):
    """No live member with that id in this gym."""


def _live_filter() -> str:
    return "deleted_at IS NULL"


def list_members(
    engine: Engine,
    gym_id: int,
    *,
    limit: int = 100,
    offset: int = 0,
    trainer_id: int | None = None,
) -> list[dict[str, Any]]:
    """List live members with an active-injury count for the safety badge.

    Args:
        trainer_id: when set, restrict to members assigned to that trainer
            (map §2.4 — a TRAINER never sees the whole registry).
    """
    scope = (
        "AND m.id IN (SELECT member_id FROM member_trainer "
        "WHERE trainer_id = :t AND deleted_at IS NULL)"
        if trainer_id is not None
        else ""
    )
    with engine.connect() as conn:
        rows = conn.execute(
            text(
                f"""
                SELECT m.{_OUT_COLUMNS.replace(', ', ', m.')},
                       (SELECT count(*) FROM member_injuries i
                          WHERE i.member_id = m.id
                            AND i.status IN ('active','chronic')
                            AND i.deleted_at IS NULL) AS active_injuries
                FROM members m
                WHERE m.gym_id = :g AND m.{_live_filter()} {scope}
                ORDER BY m.first_name, m.last_name
                LIMIT :limit OFFSET :offset
                """
            ),
            {"g": gym_id, "limit": limit, "offset": offset, "t": trainer_id},
        ).mappings().all()
    return [dict(r) for r in rows]


def get_member(engine: Engine, gym_id: int, member_id: int) -> dict[str, Any]:
    """One live member, or raise MemberNotFound (never leak another gym)."""
    with engine.connect() as conn:
        row = conn.execute(
            text(
                f"SELECT {_OUT_COLUMNS} FROM members "
                f"WHERE id = :id AND gym_id = :g AND {_live_filter()}"
            ),
            {"id": member_id, "g": gym_id},
        ).mappings().first()
    if row is None:
        raise MemberNotFound(f"member {member_id} not found")
    return dict(row)


def create_member(engine: Engine, gym_id: int, data: dict[str, Any]) -> int:
    """Insert a member. Returns the new id."""
    with engine.begin() as conn:
        cur = conn.execute(
            text(
                """
                INSERT INTO members (gym_id, membership_code, first_name, last_name,
                                     sex, birth_date, phone, membership_exp,
                                     guardian_consent)
                VALUES (:gym_id, :membership_code, :first_name, :last_name, :sex,
                        :birth_date, :phone, :membership_exp, :guardian_consent)
                """
            ),
            {**data, "gym_id": gym_id, "guardian_consent": int(bool(data.get("guardian_consent")))},
        )
        return int(cur.lastrowid or 0)


def update_member(
    engine: Engine, gym_id: int, member_id: int, patch: dict[str, Any]
) -> dict[str, Any]:
    """Apply a partial update, bump ``rev`` and touch ``updated_at``."""
    if not patch:
        return get_member(engine, gym_id, member_id)

    assignments = ", ".join(f"{col} = :{col}" for col in patch)
    params = {**patch, "id": member_id, "g": gym_id}
    if "guardian_consent" in patch:
        params["guardian_consent"] = int(bool(patch["guardian_consent"]))

    with engine.begin() as conn:
        cur = conn.execute(
            text(
                f"""
                UPDATE members SET {assignments}, rev = rev + 1,
                       updated_at = strftime('%Y-%m-%dT%H:%M:%fZ', 'now')
                WHERE id = :id AND gym_id = :g AND deleted_at IS NULL
                """
            ),
            params,
        )
        if cur.rowcount == 0:
            raise MemberNotFound(f"member {member_id} not found")
    return get_member(engine, gym_id, member_id)


def soft_delete_member(engine: Engine, gym_id: int, member_id: int) -> None:
    """Tombstone, never hard-delete (the sync fabric needs it)."""
    with engine.begin() as conn:
        cur = conn.execute(
            text(
                """
                UPDATE members
                   SET deleted_at = strftime('%Y-%m-%dT%H:%M:%fZ', 'now'),
                       rev = rev + 1
                 WHERE id = :id AND gym_id = :g AND deleted_at IS NULL
                """
            ),
            {"id": member_id, "g": gym_id},
        )
        if cur.rowcount == 0:
            raise MemberNotFound(f"member {member_id} not found")
