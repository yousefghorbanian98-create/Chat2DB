"""Nutrition plan persistence (map §3 #9)."""

from __future__ import annotations

from typing import Any

from sqlalchemy import text
from sqlalchemy.engine import Engine

_COLS = "id, member_id, bmr_kcal, tdee_kcal, protein_g, carbs_g, fat_g, payload, created_at"


def save_plan(engine: Engine, gym_id: int, member_id: int, plan, payload: str) -> int:
    with engine.begin() as conn:
        cur = conn.execute(
            text(
                "INSERT INTO nutrition_plans (gym_id, member_id, bmr_kcal, tdee_kcal, "
                "protein_g, carbs_g, fat_g, payload) VALUES (:g, :m, :b, :t, :p, :c, :f, :pl)"
            ),
            {
                "g": gym_id,
                "m": member_id,
                "b": plan.bmr_kcal,
                "t": plan.tdee_kcal,
                "p": plan.protein_g,
                "c": plan.carbs_g,
                "f": plan.fat_g,
                "pl": payload,
            },
        )
        return int(cur.lastrowid or 0)


def latest(engine: Engine, gym_id: int, member_id: int) -> dict[str, Any] | None:
    with engine.connect() as conn:
        row = conn.execute(
            text(
                f"SELECT {_COLS} FROM nutrition_plans "
                "WHERE gym_id = :g AND member_id = :m AND deleted_at IS NULL "
                "ORDER BY created_at DESC, id DESC LIMIT 1"
            ),
            {"g": gym_id, "m": member_id},
        ).mappings().first()
    return dict(row) if row else None
