"""Injury & limitation dossier data access (map §7).

Contraindicated patterns / allowed modifications are stored as JSON arrays in
TEXT columns — SQLite has no array type, and the program filter needs them
verbatim.
"""

from __future__ import annotations

import json
from typing import Any

from sqlalchemy import text
from sqlalchemy.engine import Engine

_COLS = (
    "id, member_id, body_region, side, label, status, pain_0_10, onset, cleared, "
    "clinician_note, member_visible_note, requires_clearance, created_at"
)


class InjuryNotFound(LookupError):
    """No live injury row with that id for this member."""


def _decode(row: dict[str, Any]) -> dict[str, Any]:
    out = dict(row)
    out["requires_clearance"] = bool(out.get("requires_clearance"))
    return out


def list_patterns(engine: Engine, gym_id: int, member_id: int) -> dict[str, Any]:
    """Everything the program filter needs: hard blocks + swap hints."""
    with engine.connect() as conn:
        rows = conn.execute(
            text(
                """
                SELECT l.contraindicated_pattern, l.allowed_modification,
                       i.status, i.body_region
                  FROM member_limitations l
                  LEFT JOIN member_injuries i ON i.id = l.member_id
                 WHERE l.gym_id = :g AND l.member_id = :m AND l.deleted_at IS NULL
                """
            ),
            {"g": gym_id, "m": member_id},
        ).mappings().all()

    blocked: set[str] = set()
    mods: set[str] = set()
    for row in rows:
        pattern = row["contraindicated_pattern"]
        if not pattern:
            continue
        if row["status"] in ("cleared",) or row["status"] is None:
            continue
        blocked.add(pattern)
        if row["allowed_modification"]:
            mods.add(row["allowed_modification"])

    return {"blocked_patterns": sorted(blocked), "allowed_modifications": sorted(mods)}


def list_injuries(engine: Engine, gym_id: int, member_id: int) -> list[dict[str, Any]]:
    """All live injuries for a member, with JSON list columns decoded."""
    with engine.connect() as conn:
        rows = conn.execute(
            text(
                f"""
                SELECT {_COLS},
                       (SELECT group_concat(l.contraindicated_pattern, '|')
                          FROM member_limitations l
                         WHERE l.member_id = i.member_id
                           AND l.gym_id = i.gym_id
                           AND l.deleted_at IS NULL) AS patterns,
                       (SELECT group_concat(l.allowed_modification, '|')
                          FROM member_limitations l
                         WHERE l.member_id = i.member_id
                           AND l.gym_id = i.gym_id
                           AND l.deleted_at IS NULL) AS mods
                  FROM member_injuries i
                 WHERE i.gym_id = :g AND i.member_id = :m AND i.deleted_at IS NULL
                 ORDER BY i.created_at DESC
                """
            ),
            {"g": gym_id, "m": member_id},
        ).mappings().all()

    out: list[dict[str, Any]] = []
    for row in rows:
        item = _decode(dict(row))
        item["contraindicated_patterns"] = [
            p for p in (item.pop("patterns", None) or "").split("|") if p
        ]
        item["allowed_modifications"] = [
            m for m in (item.pop("mods", None) or "").split("|") if m
        ]
        out.append(item)
    return out


def create_injury(
    engine: Engine,
    gym_id: int,
    member_id: int,
    data: dict[str, Any],
    *,
    staff_id: int | None = None,
) -> int:
    """Insert an injury plus its contraindication/modification rows."""
    patterns = list(data.get("contraindicated_patterns") or [])
    mods = list(data.get("allowed_modifications") or [])

    with engine.begin() as conn:
        cur = conn.execute(
            text(
                """
                INSERT INTO member_injuries (gym_id, member_id, body_region, side,
                        label, status, pain_0_10, onset, cleared, clinician_note,
                        member_visible_note, requires_clearance, created_by)
                VALUES (:g, :m, :body_region, :side, :label, :status, :pain_0_10,
                        :onset, :cleared, :clinician_note, :member_visible_note,
                        :requires_clearance, :created_by)
                """
            ),
            {
                "g": gym_id,
                "m": member_id,
                "body_region": data["body_region"],
                "side": data.get("side"),
                "label": data["label"],
                "status": data.get("status", "active"),
                "pain_0_10": data.get("pain_0_10"),
                "onset": data.get("onset"),
                "cleared": data.get("cleared"),
                "clinician_note": data.get("clinician_note"),
                "member_visible_note": data.get("member_visible_note"),
                "requires_clearance": int(bool(data.get("requires_clearance"))),
                "created_by": staff_id,
            },
        )
        injury_id = int(cur.lastrowid or 0)

        # member_limitations has no injury_id column in 0001_core, so patterns
        # are keyed by member (map §8 shape). One row per pattern.
        for pattern in patterns or [None]:
            conn.execute(
                text(
                    """
                    INSERT INTO member_limitations (gym_id, member_id,
                            contraindicated_pattern, allowed_modification, note)
                    VALUES (:g, :m, :p, :a, :n)
                    """
                ),
                {
                    "g": gym_id,
                    "m": member_id,
                    "p": pattern or data["label"],
                    "a": mods[0] if mods else None,
                    "n": json.dumps({"injury_id": injury_id}, separators=(",", ":")),
                },
            )
    return injury_id


def soft_delete_injury(engine: Engine, gym_id: int, injury_id: int) -> None:
    with engine.begin() as conn:
        cur = conn.execute(
            text(
                """
                UPDATE member_injuries
                   SET deleted_at = strftime('%Y-%m-%dT%H:%M:%fZ', 'now'), rev = rev + 1
                 WHERE id = :id AND gym_id = :g AND deleted_at IS NULL
                """
            ),
            {"id": injury_id, "g": gym_id},
        )
        if cur.rowcount == 0:
            raise InjuryNotFound(f"injury {injury_id} not found")
