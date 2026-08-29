"""Persian demo seed: coherent, deterministic, idempotent (map C4)."""

from __future__ import annotations

from app.core.jp7 import assess
from app.repo import members as members_repo
from app.repo import staff as staff_repo
from app.seed_demo import DEMO_CODE, seed_demo


def test_seed_demo_builds_a_coherent_persian_member(engine) -> None:
    gym_id = staff_repo.ensure_gym(engine, "Muscle Paradise")
    counts = seed_demo(engine, gym_id)

    assert counts["assessment"] > 0 and counts["payment"] > 0 and counts["checkin"] > 0
    member = members_repo.find_member_by_code(engine, gym_id, DEMO_CODE)
    assert member is not None
    # The stored assessment must equal the deterministic core, not a guess.
    row = members_repo.get_member(engine, gym_id, member["id"])
    assert row["first_name"] == "نسیم"

    from app.repo import assessments as assessments_repo

    history = assessments_repo.history(engine, gym_id, member["id"])
    assert len(history) == 1
    expected = assess(sex="female", age_years=25,
                      sites_mm={"chest": 10, "midaxillary": 10, "triceps": 10,
                                "subscapular": 10, "abdominal": 10,
                                "suprailiac": 5, "thigh": 5},
                      weight_kg=58.0)
    assert history[0]["body_fat_pct"] == expected.body_fat_pct


def test_seed_demo_is_idempotent(engine) -> None:
    gym_id = staff_repo.ensure_gym(engine, "Muscle Paradise")
    first = seed_demo(engine, gym_id)
    second = seed_demo(engine, gym_id)
    assert second["assessment"] == 0
    assert second["payment"] == 0
    assert second["checkin"] == 0
    assert second["member"] == first["member"]
