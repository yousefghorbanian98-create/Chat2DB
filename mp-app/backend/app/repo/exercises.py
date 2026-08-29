"""Exercise library data access + seed loader (map §3 #6, §12.2)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from sqlalchemy import text
from sqlalchemy.engine import Engine

DEFAULT_SEED = Path(__file__).resolve().parents[3] / "packs" / "exercises_seed.json"


def seed_exercises(engine: Engine, gym_id: int, seed_path: Path = DEFAULT_SEED) -> int:
    """Idempotently load the exercise seed. Returns rows inserted.

    Re-running never duplicates: exercises are keyed by ``key``.
    """
    rows = json.loads(seed_path.read_text(encoding="utf-8"))
    inserted = 0
    with engine.begin() as conn:
        for row in rows:
            existing = conn.execute(
                text("SELECT id FROM exercises WHERE gym_id = :g AND key = :k"),
                {"g": gym_id, "k": row["key"]},
            ).scalar()
            if existing is not None:
                exercise_id = int(existing)
            else:
                cur = conn.execute(
                    text(
                        "INSERT INTO exercises (gym_id, key, name_en, name_fa, "
                        "category, equipment, pattern, primary_muscles, source, "
                        "source_license) VALUES (:g, :k, :en, :fa, :cat, :eq, "
                        ":pat, :mus, :src, :lic)"
                    ),
                    {
                        "g": gym_id,
                        "k": row["key"],
                        "en": row["name_en"],
                        "fa": row["name_fa"],
                        "cat": row.get("pattern"),
                        "eq": row.get("equipment"),
                        "pat": row.get("pattern"),
                        "mus": row.get("primary_muscles"),
                        "src": row.get("source", "curated"),
                        "lic": row.get("source_license", "MIT"),
                    },
                )
                exercise_id = int(cur.lastrowid or 0)
                inserted += 1

            # Replace contraindications for determinism on re-seed.
            conn.execute(
                text("DELETE FROM exercise_contraindications WHERE exercise_id = :e"),
                {"e": exercise_id},
            )
            for c in row.get("contraindications", []):
                conn.execute(
                    text(
                        "INSERT INTO exercise_contraindications (gym_id, exercise_id, "
                        "body_region, pattern, severity) VALUES (:g, :e, :r, :p, :s)"
                    ),
                    {
                        "g": gym_id,
                        "e": exercise_id,
                        "r": c["body_region"],
                        "p": c["pattern"],
                        "s": c["severity"],
                    },
                )
    return inserted


def list_exercises(engine: Engine, gym_id: int) -> list[dict[str, Any]]:
    with engine.connect() as conn:
        rows = conn.execute(
            text(
                "SELECT id, key, name_en, name_fa, equipment, pattern, "
                "primary_muscles FROM exercises "
                "WHERE gym_id = :g AND deleted_at IS NULL ORDER BY name_en"
            ),
            {"g": gym_id},
        ).mappings().all()
    return [dict(r) for r in rows]


def contraindications_for(
    engine: Engine, gym_id: int, exercise_key: str
) -> list[dict[str, Any]]:
    """Hard blocks / swaps / cautions attached to one exercise."""
    with engine.connect() as conn:
        rows = conn.execute(
            text(
                """
                SELECT c.body_region, c.pattern, c.severity
                  FROM exercise_contraindications c
                  JOIN exercises e ON e.id = c.exercise_id
                 WHERE e.gym_id = :g AND e.key = :k AND e.deleted_at IS NULL
                """
            ),
            {"g": gym_id, "k": exercise_key},
        ).mappings().all()
    return [dict(r) for r in rows]
