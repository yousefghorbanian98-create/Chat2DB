"""Exercise seed + contraindication queries (Phase 2, feeds Phase 3 filter)."""

from __future__ import annotations

import pytest

from app.repo import exercises as exercises_repo
from app.repo import staff as staff_repo


@pytest.fixture
def gym_id(engine) -> int:
    return staff_repo.ensure_gym(engine, "Muscle Paradise")


def test_seed_loads_30_exercises_with_fa_names(engine, gym_id: int) -> None:
    inserted = exercises_repo.seed_exercises(engine, gym_id)
    assert inserted == 30
    rows = exercises_repo.list_exercises(engine, gym_id)
    assert len(rows) == 30
    assert all(r["name_fa"] for r in rows), "every exercise must have a FA name"
    names = {r["name_en"] for r in rows}
    assert "Barbell Back Squat" in names
    assert "Trap Bar Deadlift" in names


def test_seed_is_idempotent(engine, gym_id: int) -> None:
    first = exercises_repo.seed_exercises(engine, gym_id)
    second = exercises_repo.seed_exercises(engine, gym_id)
    assert first == 30
    assert second == 0, "re-seed must not duplicate"
    assert len(exercises_repo.list_exercises(engine, gym_id)) == 30


def test_contraindications_are_stored_per_exercise(engine, gym_id: int) -> None:
    exercises_repo.seed_exercises(engine, gym_id)
    contra = exercises_repo.contraindications_for(engine, gym_id, "ex003")  # deadlift
    assert any(c["pattern"] == "heavy_deadlift" and c["severity"] == "hard_block" for c in contra)

    none = exercises_repo.contraindications_for(engine, gym_id, "ex009")  # landmine
    assert none == []


def test_injury_filter_blocks_contraindicated_exercise(engine, gym_id: int) -> None:
    """Integration: a lumbar hard-block injury must drop the conventional
    deadlift (the exact input Phase 3's program builder consumes)."""
    from app.repo import injuries as injuries_repo

    exercises_repo.seed_exercises(engine, gym_id)

    with engine.begin() as conn:
        from sqlalchemy import text

        conn.execute(text("INSERT INTO gyms (name) SELECT 'x' WHERE 0"))
        cur = conn.execute(
            text(
                "INSERT INTO members (gym_id, membership_code, first_name, last_name, sex) "
                "VALUES (:g, 'M1', 'A', 'B', 'male')"
            ),
            {"g": gym_id},
        )
        member_id = int(cur.lastrowid)

    injuries_repo.create_injury(
        engine,
        gym_id,
        member_id,
        {"body_region": "lumbar", "label": "disc", "status": "active",
         "contraindicated_patterns": ["heavy_deadlift"]},
    )
    blocked = injuries_repo.list_patterns(engine, gym_id, member_id)["blocked_patterns"]
    assert "heavy_deadlift" in blocked

    # The deadlift's hard_block pattern matches the injury's blocked pattern.
    deadlift_contra = exercises_repo.contraindications_for(engine, gym_id, "ex003")
    assert deadlift_contra[0]["pattern"] in blocked


def test_exercises_endpoint_is_staff_gated(seeded, owner_auth, kiosk_auth) -> None:
    # seed via repo so the endpoint has data
    from app.repo import exercises as repo
    from app.state import get_engine

    repo.seed_exercises(get_engine(), 1)
    assert seeded.get("/api/v1/exercises", headers=owner_auth).status_code == 200
    assert len(seeded.get("/api/v1/exercises", headers=owner_auth).json()) == 30
    assert seeded.get("/api/v1/exercises", headers=kiosk_auth).status_code == 403
