"""Phase 4 API: nutrition plan from LBM + AI runtime detection."""

from __future__ import annotations

JP7_SITES = {
    "chest": 12, "midaxillary": 10, "triceps": 14, "subscapular": 16,
    "abdominal": 20, "suprailiac": 15, "thigh": 18,
}


class TestNutritionApi:
    def test_nutrition_requires_an_assessment_first(
        self, seeded, owner_auth, member_id
    ) -> None:
        res = seeded.post(
            f"/api/v1/nutrition/members/{member_id}/plan",
            headers=owner_auth,
            json={"goal": "maintain"},
        )
        assert res.status_code == 422  # no assessment with LBM yet

    def test_nutrition_computed_from_latest_lbm(
        self, seeded, owner_auth, member_id
    ) -> None:
        seeded.post(
            f"/api/v1/members/{member_id}/assessments",
            headers=owner_auth,
            json={"weight_kg": 62.5, "age_years": 30, "sites_mm": JP7_SITES},
        )
        res = seeded.post(
            f"/api/v1/nutrition/members/{member_id}/plan",
            headers=owner_auth,
            json={"goal": "maintain", "activity": "moderate"},
        )
        assert res.status_code == 201, res.text
        body = res.json()
        # LBM 49.1088 -> BMR = 370 + 21.6*49.1088 = 1430.7 (independent math)
        assert body["bmr_kcal"] == 1430.8 or abs(body["bmr_kcal"] - 1430.8) < 0.2
        assert body["target_kcal"] > 0
        assert body["protein_g"] > 0

        got = seeded.get(f"/api/v1/nutrition/members/{member_id}/plan", headers=owner_auth)
        assert got.status_code == 200

    def test_reception_cannot_build_nutrition(self, seeded, reception_auth, member_id) -> None:
        res = seeded.post(
            f"/api/v1/nutrition/members/{member_id}/plan",
            headers=reception_auth,
            json={},
        )
        assert res.status_code == 403


class TestAiRuntimeApi:
    def test_runtime_reports_unavailable_without_ollama(self, seeded, owner_auth) -> None:
        """No Ollama in the sandbox -> available False, and the note holds (C7)."""
        res = seeded.get("/api/v1/ai/runtime", headers=owner_auth)
        assert res.status_code == 200
        body = res.json()
        assert body["available"] is False
        assert "C7" in body["note"]

    def test_runtime_is_staff_gated(self, seeded, kiosk_auth) -> None:
        assert seeded.get("/api/v1/ai/runtime", headers=kiosk_auth).status_code == 403
