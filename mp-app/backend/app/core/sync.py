"""Delta sync (map §14 Phase 6). Cursor = max ``updated_at`` seen, per gym.

A client stores the cursor from its last sync and passes it back; the server
returns only rows whose ``updated_at`` (or ``created_at``) is newer. Tombstoned
rows (``deleted_at`` set) are included so clients can mirror deletions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from sqlalchemy import inspect, text
from sqlalchemy.engine import Engine

#: Tables that participate in sync and carry a timestamp column.
_SYNCABLE_HINT = ("updated_at", "created_at")


@dataclass(frozen=True)
class Delta:
    cursor: str
    changes: dict[str, list[dict[str, Any]]] = field(default_factory=dict)

    @property
    def total(self) -> int:
        return sum(len(v) for v in self.changes.values())


def _timestamp_column(engine: Engine, table: str) -> str | None:
    cols = {c["name"] for c in inspect(engine).get_columns(table)}
    for cand in _SYNCABLE_HINT:
        if cand in cols:
            return cand
    return None


def delta_since(
    engine: Engine, gym_id: int, since: str | None = None
) -> Delta:
    """Rows changed after ``since`` (ISO-8601); empty cursor = full snapshot."""
    changes: dict[str, list[dict[str, Any]]] = {}
    cursor = since or ""
    with engine.connect() as conn:
        for table in sorted(inspect(engine).get_table_names()):
            ts = _timestamp_column(engine, table)
            if ts is None:
                continue
            has_gym = "gym_id" in {c["name"] for c in inspect(engine).get_columns(table)}
            where = f'WHERE "{ts}" > :since' if since else ""
            if has_gym:
                where = f"{where} AND gym_id = :gym" if where else "WHERE gym_id = :gym"
            params: dict[str, Any] = {"gym": gym_id} if has_gym else {}
            if since:
                params["since"] = since
            rows = conn.execute(
                text(f'SELECT * FROM "{table}" {where} ORDER BY "{ts}"'), params
            ).mappings().all()
            if rows:
                changes[table] = [dict(r) for r in rows]
                last = str(rows[-1][ts])
                if last > cursor:
                    cursor = last
    return Delta(cursor=cursor, changes=changes)
