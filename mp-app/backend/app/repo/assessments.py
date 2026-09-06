"""Body-assessment persistence. The math lives in app/core/jp7.py."""

from __future__ import annotations

import json
from typing import Any

from sqlalchemy import text
from sqlalchemy.engine import Engine

from app.core.jp7 import Jp7Result

_COLS = (
    "id, member_id, protocol, equation, age_years, weight_kg, sum_mm, "
    "body_density, body_fat_pct, fat_mass_kg, lean_mass_kg, classification, "
    "created_at"
)


class AssessmentNotFound(LookupError):
    """No live assessment row with that id."""


def save_assessment(
    engine: Engine,
    *,
    gym_id: int,
    member_id: int,
    result: Jp7Result,
    weight_kg: float,
    height_cm: float | None,
    staff_id: int | None,
) -> int:
    """Persist a computed assessment (numbers come from code, never an LLM)."""
    payload = json.dumps(
        {
            "schema": "mp.assessment/v1",
            "sites_mm": result.sites_mm,
            "height_cm": height_cm,
        },
        separators=(",", ":"),
    )
    with engine.begin() as conn:
        cur = conn.execute(
            text(
                """
                INSERT INTO body_assessments (gym_id, member_id, protocol, equation,
                        weight_kg, height_cm, age_years, sites_mm, sum_mm,
                        body_density, body_fat_pct, fat_mass_kg, lean_mass_kg,
                        classification, measured_by, payload)
                VALUES (:g, :m, :protocol, :equation, :weight_kg, :height_cm,
                        :age_years, :sites_mm, :sum_mm, :body_density,
                        :body_fat_pct, :fat_mass_kg, :lean_mass_kg,
                        :classification, :measured_by, :payload)
                """
            ),
            {
                "g": gym_id,
                "m": member_id,
                "protocol": result.protocol,
                "equation": result.equation,
                "weight_kg": weight_kg,
                "height_cm": height_cm,
                "age_years": result.age_years,
                "sites_mm": json.dumps(result.sites_mm, separators=(",", ":")),
                "sum_mm": result.sum_mm,
                "body_density": result.body_density,
                "body_fat_pct": result.body_fat_pct,
                "fat_mass_kg": result.fat_mass_kg,
                "lean_mass_kg": result.lean_mass_kg,
                "classification": result.classification,
                "measured_by": staff_id,
                "payload": payload,
            },
        )
        return int(cur.lastrowid or 0)


def get_assessment(engine: Engine, gym_id: int, assessment_id: int) -> dict[str, Any]:
    with engine.connect() as conn:
        row = conn.execute(
            text(
                f"SELECT {_COLS} FROM body_assessments "
                "WHERE id = :id AND gym_id = :g AND deleted_at IS NULL"
            ),
            {"id": assessment_id, "g": gym_id},
        ).mappings().first()
    if row is None:
        raise AssessmentNotFound(f"assessment {assessment_id} not found")
    return dict(row)


def history(engine: Engine, gym_id: int, member_id: int, *, limit: int = 50) -> list[dict[str, Any]]:
    """Newest first — the BF% trend chart reads this."""
    with engine.connect() as conn:
        rows = conn.execute(
            text(
                f"SELECT {_COLS} FROM body_assessments "
                "WHERE gym_id = :g AND member_id = :m AND deleted_at IS NULL "
                "ORDER BY created_at DESC, id DESC LIMIT :limit"
            ),
            {"g": gym_id, "m": member_id, "limit": limit},
        ).mappings().all()
    return [dict(r) for r in rows]
