"""Equipment inventory data access (map §3 #5). Filters AI exercises later."""

from __future__ import annotations

from typing import Any

from sqlalchemy import text
from sqlalchemy.engine import Engine

_COLS = "id, name, category, count, available, created_at"


class EquipmentNotFound(LookupError):
    """No live equipment row with that id."""


def list_equipment(engine: Engine, gym_id: int) -> list[dict[str, Any]]:
    with engine.connect() as conn:
        rows = conn.execute(
            text(
                f"SELECT {_COLS} FROM gym_equipment "
                "WHERE gym_id = :g AND deleted_at IS NULL ORDER BY name"
            ),
            {"g": gym_id},
        ).mappings().all()
    return [dict(r) for r in rows]


def create_equipment(
    engine: Engine, gym_id: int, *, name: str, category: str | None, count: int = 1
) -> int:
    with engine.begin() as conn:
        cur = conn.execute(
            text(
                "INSERT INTO gym_equipment (gym_id, name, category, count) "
                "VALUES (:g, :n, :c, :count)"
            ),
            {"g": gym_id, "n": name, "c": category, "count": count},
        )
        return int(cur.lastrowid or 0)


def set_availability(engine: Engine, gym_id: int, equipment_id: int, available: bool) -> None:
    with engine.begin() as conn:
        cur = conn.execute(
            text(
                "UPDATE gym_equipment SET available = :a, rev = rev + 1 "
                "WHERE id = :i AND gym_id = :g AND deleted_at IS NULL"
            ),
            {"a": int(available), "i": equipment_id, "g": gym_id},
        )
        if cur.rowcount == 0:
            raise EquipmentNotFound(f"equipment {equipment_id} not found")
