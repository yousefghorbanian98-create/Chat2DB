"""Phase 3: rule-based programs — generation, dry-run, apply, lifecycle."""

from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from app.repo import exercises as exercises_repo
from app.repo import staff as staff_repo
from app.state import get_engine


@pytest.fixture
def gym_and_seed(seeded: TestClient, owner_auth) -> TestClient:
    """Seed exercises + a token-based equipment inventory."""
    engine = get_engine()
    gym_id = staff_repo.ensure_gym(engine)
    exercises_repo.seed_exercises(engine, gym_id)

    from sqlalchemy import text

    with engine.begin() as conn:
        for name, cat in [
            ("Rack + barbell", "barbell"),
            ("Dumbbells", "dumbbell"),
            ("Trap bar", "trap_bar"),
            ("Landmine", "landmine"),
            ("Cable stack", "cable"),
        ]:
            conn.execute(
                text(
                    "INSERT INTO gym_equipment (gym_id, name, category, count) "
                    "VALUES (:g, :n, :c, 1)"
                ),
                {"g": gym_id, "n": name, "c": cat},
            )
    return seeded


def _injure(seeded: TestClient, owner_auth, member_id: int) -> None:
    seeded.post(
        f"/api/v1/members/{member_id}/injuries",
        headers=owner_auth,
        json={
            "body_region": "lumbar",
            "label": "disc bulge",
            "status": "active",
            "contraindicated_patterns": ["heavy_deadlift"],
        },
    )


class TestGenerate:
    def test_generated_program_never_includes_hard_blocked_exercise(
        self, gym_and_seed, owner_auth, member_id
    ) -> None:
        _injure(gym_and_seed, owner_auth, member_id)
        res = gym_and_seed.post(
            f"/api/v1/members/{member_id}/programs/generate",
            headers=owner_auth,
            json={"template": "ul"},
        )
        assert res.status_code == 201, res.text
        body = res.json()
        all_keys = [k for day in body["days"] for k in day["exercises"]]
        # ex003 = conventional deadlift (heavy_deadlift hard block)
        assert "ex003" not in all_keys
        assert body["meta"]["blocked_patterns"] == ["heavy_deadlift"]

    def test_blocked_hinge_is_swapped_to_trap_bar(self, gym_and_seed, owner_auth, member_id) -> None:
        _injure(gym_and_seed, owner_auth, member_id)
        body = gym_and_seed.post(
            f"/api/v1/members/{member_id}/programs/generate",
            headers=owner_auth,
            json={"template": "ul"},
        ).json()
        all_keys = [k for day in body["days"] for k in day["exercises"]]
        assert "ex004" in all_keys, "trap bar deadlift is the safe hinge swap"

    def test_healthy_member_gets_conventional_deadlift(self, gym_and_seed, owner_auth, member_id) -> None:
        body = gym_and_seed.post(
            f"/api/v1/members/{member_id}/programs/generate",
            headers=owner_auth,
            json={"template": "ul"},
        ).json()
        all_keys = [k for day in body["days"] for k in day["exercises"]]
        assert "ex003" in all_keys
        assert body["meta"]["corrective_block_added"] is False

    def test_injured_member_gets_corrective_block(self, gym_and_seed, owner_auth, member_id) -> None:
        _injure(gym_and_seed, owner_auth, member_id)
        body = gym_and_seed.post(
            f"/api/v1/members/{member_id}/programs/generate",
            headers=owner_auth,
            json={"template": "fb"},
        ).json()
        assert body["meta"]["corrective_block_added"] is True

    def test_unknown_template_is_422(self, gym_and_seed, owner_auth, member_id) -> None:
        res = gym_and_seed.post(
            f"/api/v1/members/{member_id}/programs/generate",
            headers=owner_auth,
            json={"template": "bro-split"},
        )
        assert res.status_code == 422


class TestLifecycle:
    def _generate(self, seeded, owner_auth, member_id, template="ul") -> int:
        return seeded.post(
            f"/api/v1/members/{member_id}/programs/generate",
            headers=owner_auth,
            json={"template": template},
        ).json()["id"]

    def test_dry_run_then_apply_moves_draft_to_approved(
        self, gym_and_seed, owner_auth, member_id
    ) -> None:
        pid = self._generate(gym_and_seed, owner_auth, member_id)

        dry = gym_and_seed.post(f"/api/v1/programs/{pid}/dry-run", headers=owner_auth)
        assert dry.status_code == 200
        assert dry.json()["safe_to_apply"] is True

        applied = gym_and_seed.post(f"/api/v1/programs/{pid}/apply", headers=owner_auth)
        assert applied.status_code == 200
        assert applied.json()["status"] == "trainer_approved"
        assert applied.json()["applied_at"] is not None

    def test_apply_is_refused_when_a_new_injury_blocks_an_op(
        self, gym_and_seed, owner_auth, member_id
    ) -> None:
        """C8: dry-run/apply must re-check the CURRENT filters, not trust stale ops."""
        pid = self._generate(gym_and_seed, owner_auth, member_id)  # healthy -> has ex003
        _injure(gym_and_seed, owner_auth, member_id)  # now heavy_deadlift blocked

        dry = gym_and_seed.post(f"/api/v1/programs/{pid}/dry-run", headers=owner_auth).json()
        assert dry["safe_to_apply"] is False
        assert "ex003" in dry["newly_blocked"]

        res = gym_and_seed.post(f"/api/v1/programs/{pid}/apply", headers=owner_auth)
        assert res.status_code == 409

    def test_archive_after_apply_and_no_revive_from_archive(
        self, gym_and_seed, owner_auth, member_id
    ) -> None:
        pid = self._generate(gym_and_seed, owner_auth, member_id)
        gym_and_seed.post(f"/api/v1/programs/{pid}/apply", headers=owner_auth)
        archived = gym_and_seed.post(f"/api/v1/programs/{pid}/archive", headers=owner_auth)
        assert archived.json()["status"] == "archived"

        # archived is terminal: applying again must be a 409
        again = gym_and_seed.post(f"/api/v1/programs/{pid}/apply", headers=owner_auth)
        assert again.status_code == 409

    def test_reception_cannot_generate_programs(self, gym_and_seed, reception_auth, member_id) -> None:
        res = gym_and_seed.post(
            f"/api/v1/members/{member_id}/programs/generate",
            headers=reception_auth,
            json={"template": "ul"},
        )
        assert res.status_code == 403
