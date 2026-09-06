"""Read-side reports that feed the optional n8n bridge (map §12.8).

Only the fields an automation needs to *notify* are returned — no clinician
notes, no national IDs, no raw skinfolds (PHI minimization, C11).
"""

from __future__ import annotations

from datetime import datetime, timedelta
from typing import Any

from sqlalchemy import text
from sqlalchemy.engine import Engine

_MEMBER_COLS = "id, membership_code, first_name, last_name, phone, membership_exp"


def _parse(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00"))


def _now() -> datetime:
    return datetime.utcnow()


def list_expiring(engine: Engine, gym_id: int, days: int = 7) -> list[dict[str, Any]]:
    """Members whose membership expires within `days` (or already has)."""
    with engine.connect() as conn:
        rows = conn.execute(
            text(
                f"SELECT {_MEMBER_COLS} FROM members "
                "WHERE gym_id = :g AND deleted_at IS NULL AND membership_exp IS NOT NULL "
                "ORDER BY membership_exp ASC"
            ),
            {"g": gym_id},
        ).mappings().all()

    out = []
    cutoff = _now() + timedelta(days=days)
    for r in rows:
        try:
            exp = _parse(str(r["membership_exp"]))
        except ValueError:
            continue
        if exp > cutoff:
            continue
        days_left = (exp - _now()).days
        out.append(
            {
                "id": r["id"],
                "membership_code": r["membership_code"],
                "display_name": f"{r['first_name']} {r['last_name']}",
                "phone": r["phone"],
                "membership_exp": r["membership_exp"],
                "days_left": days_left,
            }
        )
    return out


def list_inactive(engine: Engine, gym_id: int, days: int = 7) -> list[dict[str, Any]]:
    """Members with no attendance in the last `days` (retention digests)."""
    cutoff = (_now() - timedelta(days=days)).strftime("%Y-%m-%dT%H:%M:%S")
    with engine.connect() as conn:
        rows = conn.execute(
            text(
                "SELECT m.id, m.membership_code, m.first_name, m.last_name, m.phone, "
                "       (SELECT MAX(a.created_at) FROM attendance a "
                "        WHERE a.member_id = m.id AND a.deleted_at IS NULL) AS last_seen "
                "FROM members m "
                "WHERE m.gym_id = :g AND m.deleted_at IS NULL "
                "ORDER BY m.id"
            ),
            {"g": gym_id},
        ).mappings().all()

    return [
        {
            "id": r["id"],
            "membership_code": r["membership_code"],
            "display_name": f"{r['first_name']} {r['last_name']}",
            "phone": r["phone"],
            "last_seen": r["last_seen"],
        }
        for r in rows
        if r["last_seen"] is None or str(r["last_seen"]) < cutoff
    ]
