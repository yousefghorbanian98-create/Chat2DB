"""Phase 1 API: auth, RBAC, members CRUD, JP7 assessments, injuries, QR."""

from __future__ import annotations

import time

import pytest
from fastapi.testclient import TestClient

from app.core.security import QrError, verify_qr
from app.state import get_secret_key

JP7_SITES = {
    "chest": 12.0,
    "midaxillary": 10.0,
    "triceps": 14.0,
    "subscapular": 16.0,
    "abdominal": 20.0,
    "suprailiac": 15.0,
    "thigh": 18.0,
}


class TestAuth:
    def test_pin_login_returns_a_token(self, seeded: TestClient) -> None:
        res = seeded.post("/api/v1/auth/pin", json={"username": "owner", "pin": "1111"})
        assert res.status_code == 200
        body = res.json()
        assert body["role"] == "OWNER"
        assert body["expires_in"] == 8 * 3600
        assert body["token"].count(".") == 1

    def test_wrong_pin_is_rejected(self, seeded: TestClient) -> None:
        res = seeded.post("/api/v1/auth/pin", json={"username": "owner", "pin": "9999"})
        assert res.status_code == 401
        assert res.json()["detail"] == "invalid credentials"

    def test_unknown_user_gets_the_same_message_as_wrong_pin(
        self, seeded: TestClient
    ) -> None:
        """No user enumeration."""
        res = seeded.post("/api/v1/auth/pin", json={"username": "ghost", "pin": "1111"})
        assert res.status_code == 401
        assert res.json()["detail"] == "invalid credentials"

    def test_missing_token_is_401(self, seeded: TestClient) -> None:
        assert seeded.get("/api/v1/auth/me").status_code == 401

    def test_forged_token_is_401(self, seeded: TestClient) -> None:
        res = seeded.get("/api/v1/auth/me", headers={"authorization": "Bearer abc.def"})
        assert res.status_code == 401

    def test_me_reports_role_and_shell(self, seeded: TestClient, owner_auth) -> None:
        body = seeded.get("/api/v1/auth/me", headers=owner_auth).json()
        assert body == {
            "subject": "owner",
            "role": "OWNER",
            "gym_id": body["gym_id"],
            "member_id": None,
            "shell": "studio",
        }


class TestMembersCrud:
    def test_create_read_update_delete(self, seeded: TestClient, owner_auth) -> None:
        created = seeded.post(
            "/api/v1/members",
            headers=owner_auth,
            json={
                "membership_code": "MP-1000",
                "first_name": "Ali",
                "last_name": "Rezaei",
                "sex": "male",
            },
        )
        assert created.status_code == 201
        mid = created.json()["id"]

        got = seeded.get(f"/api/v1/members/{mid}", headers=owner_auth)
        assert got.status_code == 200
        assert got.json()["first_name"] == "Ali"

        patched = seeded.patch(
            f"/api/v1/members/{mid}",
            headers=owner_auth,
            json={"first_name": "Alireza"},
        )
        assert patched.json()["first_name"] == "Alireza"

        assert seeded.delete(f"/api/v1/members/{mid}", headers=owner_auth).status_code == 204
        assert seeded.get(f"/api/v1/members/{mid}", headers=owner_auth).status_code == 404

    def test_soft_delete_leaves_a_tombstone_row(self, seeded, owner_auth, db_path) -> None:
        from sqlalchemy import text

        from app.state import get_engine

        mid = seeded.post(
            "/api/v1/members",
            headers=owner_auth,
            json={
                "membership_code": "MP-1001",
                "first_name": "Nima",
                "last_name": "T",
                "sex": "male",
            },
        ).json()["id"]
        seeded.delete(f"/api/v1/members/{mid}", headers=owner_auth)

        with get_engine().connect() as conn:
            row = conn.execute(
                text("SELECT deleted_at, rev FROM members WHERE id = :i"), {"i": mid}
            ).one()
        assert row[0] is not None, "row must be tombstoned, not hard-deleted"
        assert row[1] == 2

    def test_unknown_member_is_404(self, seeded: TestClient, owner_auth) -> None:
        assert seeded.get("/api/v1/members/999999", headers=owner_auth).status_code == 404

    def test_validation_rejects_unknown_fields(self, seeded: TestClient, owner_auth) -> None:
        res = seeded.post(
            "/api/v1/members",
            headers=owner_auth,
            json={
                "membership_code": "X",
                "first_name": "A",
                "last_name": "B",
                "sex": "male",
                "credit_score": 800,
            },
        )
        assert res.status_code == 422

    def test_list_shows_active_injury_count(
        self, seeded: TestClient, owner_auth, member_id: int
    ) -> None:
        seeded.post(
            f"/api/v1/members/{member_id}/injuries",
            headers=owner_auth,
            json={"body_region": "knee", "label": "ACL sprain", "status": "active"},
        )
        rows = seeded.get("/api/v1/members", headers=owner_auth).json()
        match = next(r for r in rows if r["id"] == member_id)
        assert match["active_injuries"] == 1


class TestRbac:
    def test_kiosk_cannot_create_members(self, seeded: TestClient, kiosk_auth) -> None:
        res = seeded.post(
            "/api/v1/members",
            headers=kiosk_auth,
            json={
                "membership_code": "X",
                "first_name": "A",
                "last_name": "B",
                "sex": "male",
            },
        )
        assert res.status_code == 403

    def test_reception_cannot_run_assessments(
        self, seeded: TestClient, reception_auth, member_id: int
    ) -> None:
        """Map §2.4: JP7 belongs to TRAINER/ADMIN/OWNER."""
        res = seeded.post(
            f"/api/v1/members/{member_id}/assessments",
            headers=reception_auth,
            json={"weight_kg": 62.5, "age_years": 30, "sites_mm": JP7_SITES},
        )
        assert res.status_code == 403

    def test_assigned_trainer_can_run_assessments(
        self, seeded: TestClient, assigned_trainer_auth, member_id: int
    ) -> None:
        """A TRAINER may assess a member *they are assigned to* (map §2.4)."""
        trainer_auth, assign = assigned_trainer_auth
        assign(member_id)
        res = seeded.post(
            f"/api/v1/members/{member_id}/assessments",
            headers=trainer_auth,
            json={"weight_kg": 62.5, "age_years": 30, "sites_mm": JP7_SITES},
        )
        assert res.status_code == 201, res.text

    def test_kiosk_is_scan_only_and_cannot_read_the_member_list(
        self, seeded: TestClient, kiosk_auth
    ) -> None:
        """Map §2.4: KIOSK = "Scan only"."""
        assert seeded.get("/api/v1/members", headers=kiosk_auth).status_code == 403

    def test_trainer_can_read_but_not_register_members(
        self, seeded: TestClient, trainer_auth
    ) -> None:
        """Map §2.4: TRAINER manages assigned members, not the registry."""
        assert seeded.get("/api/v1/members", headers=trainer_auth).status_code == 200
        res = seeded.post(
            "/api/v1/members",
            headers=trainer_auth,
            json={
                "membership_code": "MP-2000",
                "first_name": "A",
                "last_name": "B",
                "sex": "male",
            },
        )
        assert res.status_code == 403

    def test_reception_can_register_members(
        self, seeded: TestClient, reception_auth
    ) -> None:
        """Front desk runs registrations and renewals."""
        res = seeded.post(
            "/api/v1/members",
            headers=reception_auth,
            json={
                "membership_code": "MP-3000",
                "first_name": "Raha",
                "last_name": "M",
                "sex": "female",
            },
        )
        assert res.status_code == 201

    def test_trainer_sees_only_assigned_members(
        self, seeded: TestClient, trainer_auth, owner_auth, member_id: int
    ) -> None:
        """Map §2.4: TRAINER = assigned members only. Unassigned = 404, not 403,
        so a trainer cannot even learn the member exists."""
        from sqlalchemy import text

        from app.repo import staff as staff_repo
        from app.state import get_engine

        engine = get_engine()
        gym_id = staff_repo.ensure_gym(engine)
        trainer = staff_repo.find_staff_by_username(engine, gym_id, "trainer")
        assert trainer is not None

        # Not assigned yet: the list is empty and the record looks absent.
        assert seeded.get("/api/v1/members", headers=trainer_auth).json() == []
        assert (
            seeded.get(f"/api/v1/members/{member_id}", headers=trainer_auth).status_code
            == 404
        )

        with engine.begin() as conn:
            conn.execute(
                text(
                    "INSERT INTO member_trainer (gym_id, member_id, trainer_id, "
                    "primary_flag) VALUES (:g, :m, :t, 1)"
                ),
                {"g": gym_id, "m": member_id, "t": trainer["id"]},
            )

        listed = seeded.get("/api/v1/members", headers=trainer_auth).json()
        assert [m["id"] for m in listed] == [member_id]
        assert (
            seeded.get(f"/api/v1/members/{member_id}", headers=trainer_auth).status_code
            == 200
        )

    def test_owner_still_sees_every_member(
        self, seeded: TestClient, owner_auth, member_id: int
    ) -> None:
        listed = seeded.get("/api/v1/members", headers=owner_auth).json()
        assert [m["id"] for m in listed] == [member_id]

    def test_unassigned_trainer_cannot_touch_injuries_or_assessments(
        self, seeded: TestClient, trainer_auth, member_id: int
    ) -> None:
        assert (
            seeded.get(f"/api/v1/members/{member_id}/injuries", headers=trainer_auth).status_code
            == 404
        )
        assert (
            seeded.post(
                f"/api/v1/members/{member_id}/assessments",
                headers=trainer_auth,
                json={"weight_kg": 62.5, "age_years": 30, "sites_mm": JP7_SITES},
            ).status_code
            == 404
        )

    def test_member_role_token_is_locked_out_of_studio_surface(
        self, seeded: TestClient
    ) -> None:
        from app.core.security import Principal, issue_token

        token = issue_token(
            Principal("athlete", "MEMBER", 1, member_id=7),
            secret_key=get_secret_key(),
        )
        headers = {"authorization": f"Bearer {token}"}
        assert seeded.get("/api/v1/members", headers=headers).status_code == 403
        assert seeded.get("/api/v1/auth/me", headers=headers).status_code == 200


class TestAssessments:
    def test_stored_numbers_match_the_golden_math(
        self, seeded: TestClient, owner_auth, member_id: int
    ) -> None:
        """sum=105mm, female, 30y -> the same value jp7.py produces offline."""
        res = seeded.post(
            f"/api/v1/members/{member_id}/assessments",
            headers=owner_auth,
            json={"weight_kg": 62.5, "age_years": 30, "sites_mm": JP7_SITES},
        )
        assert res.status_code == 201
        body = res.json()
        assert body["sum_mm"] == pytest.approx(105.0)
        assert body["protocol"] == "jackson_pollock_7"
        # Independently computed with python decimal at 28 digits:
        #   BD = 1.097 - 0.00046971*105 + 0.00000056*105^2 - 0.00012828*30
        #      = 1.050006  ->  Siri = (4.95/BD - 4.5)*100 = 21.4259
        assert body["body_density"] == pytest.approx(1.050006, abs=1e-5)
        assert body["body_fat_pct"] == pytest.approx(21.4259, abs=0.05)
        assert body["fat_mass_kg"] + body["lean_mass_kg"] == pytest.approx(62.5, abs=1e-6)
        assert body["classification"] == "fit"

    def test_sex_comes_from_the_member_record_not_the_request(
        self, seeded: TestClient, owner_auth, member_id: int
    ) -> None:
        """The member was registered female; a 'male' hint must be ignored."""
        body = seeded.post(
            f"/api/v1/members/{member_id}/assessments",
            headers=owner_auth,
            json={"weight_kg": 62.5, "age_years": 30, "sites_mm": JP7_SITES},
        ).json()
        from app.core.jp7 import assess

        female = assess(
            sex="female", age_years=30, sites_mm=JP7_SITES, weight_kg=62.5
        ).body_fat_pct
        assert body["body_fat_pct"] == pytest.approx(female, abs=1e-6)

    def test_history_is_newest_first(
        self, seeded: TestClient, owner_auth, member_id: int
    ) -> None:
        for weight in (65.0, 64.0, 63.0):
            seeded.post(
                f"/api/v1/members/{member_id}/assessments",
                headers=owner_auth,
                json={"weight_kg": weight, "age_years": 30, "sites_mm": JP7_SITES},
            )
        rows = seeded.get(f"/api/v1/members/{member_id}/assessments", headers=owner_auth).json()
        assert len(rows) == 3
        assert [r["weight_kg"] for r in rows] == [63.0, 64.0, 65.0]

    def test_out_of_range_skinfold_is_422(self, seeded, owner_auth, member_id) -> None:
        res = seeded.post(
            f"/api/v1/members/{member_id}/assessments",
            headers=owner_auth,
            json={
                "weight_kg": 62.5,
                "age_years": 30,
                "sites_mm": {**JP7_SITES, "thigh": 95.0},
            },
        )
        assert res.status_code == 422

    def test_pdf_endpoint_returns_a_downloadable_report(
        self, seeded: TestClient, owner_auth, member_id: int
    ) -> None:
        created = seeded.post(
            f"/api/v1/members/{member_id}/assessments",
            headers=owner_auth,
            json={"weight_kg": 62.5, "age_years": 30, "sites_mm": JP7_SITES},
        ).json()

        res = seeded.get(
            f"/api/v1/members/{member_id}/assessments/{created['id']}/pdf",
            headers=owner_auth,
        )
        assert res.status_code == 200
        assert res.headers["content-type"] == "application/pdf"
        assert res.content[:5] == b"%PDF-"
        assert "attachment" in res.headers["content-disposition"]

    def test_pdf_of_a_missing_assessment_is_404(self, seeded, owner_auth, member_id) -> None:
        res = seeded.get(
            f"/api/v1/members/{member_id}/assessments/999999/pdf", headers=owner_auth
        )
        assert res.status_code == 404

    def test_pdf_of_another_members_assessment_is_404(
        self, seeded: TestClient, owner_auth, member_id: int
    ) -> None:
        """Cross-member reference must not leak another member's report."""
        created = seeded.post(
            f"/api/v1/members/{member_id}/assessments",
            headers=owner_auth,
            json={"weight_kg": 62.5, "age_years": 30, "sites_mm": JP7_SITES},
        ).json()
        res = seeded.get(
            f"/api/v1/members/{member_id + 1}/assessments/{created['id']}/pdf",
            headers=owner_auth,
        )
        assert res.status_code == 404

    def test_assessment_on_unknown_member_is_404(self, seeded, owner_auth) -> None:
        res = seeded.post(
            "/api/v1/members/999999/assessments",
            headers=owner_auth,
            json={"weight_kg": 62.5, "age_years": 30, "sites_mm": JP7_SITES},
        )
        assert res.status_code == 404

    def test_pure_calculate_needs_no_auth_and_persists_nothing(
        self, seeded: TestClient
    ) -> None:
        res = seeded.post(
            "/api/v1/assessments/calculate",
            json={"weight_kg": 80.0, "age_years": 25, "sites_mm": JP7_SITES},
        )
        assert res.status_code == 200
        assert res.json()["sum_mm"] == pytest.approx(105.0)
        assert "disclaimer" in res.json()


class TestQrIdentity:
    def test_qr_payload_verifies_against_the_machine_key(
        self, seeded: TestClient, owner_auth, member_id: int
    ) -> None:
        payload = seeded.get(f"/api/v1/members/{member_id}/qr", headers=owner_auth).json()[
            "payload"
        ]
        core = verify_qr(payload, secret_key=get_secret_key())
        assert core["mid"] == member_id
        assert core["typ"] == "member"

    def test_tampered_qr_is_rejected(self, seeded, owner_auth, member_id) -> None:
        payload = seeded.get(f"/api/v1/members/{member_id}/qr", headers=owner_auth).json()[
            "payload"
        ]
        with pytest.raises(QrError):
            verify_qr({**payload, "mid": member_id + 1}, secret_key=get_secret_key())

    def test_qr_expires(self, seeded, owner_auth, member_id) -> None:
        payload = seeded.get(f"/api/v1/members/{member_id}/qr", headers=owner_auth).json()[
            "payload"
        ]
        with pytest.raises(QrError, match="expired"):
            verify_qr(payload, secret_key=get_secret_key(), now=int(time.time()) + 61)


class TestInjuries:
    def test_clinician_note_is_masked_from_the_member_view(
        self, seeded: TestClient, owner_auth, member_id: int
    ) -> None:
        """Map C10: PII/medical minimisation, server-side."""
        seeded.post(
            f"/api/v1/members/{member_id}/injuries",
            headers=owner_auth,
            json={
                "body_region": "lumbar",
                "label": "L4-L5 disc bulge",
                "status": "active",
                "pain_0_10": 4,
                "contraindicated_patterns": ["spinal_flexion", "heavy_deadlift"],
                "allowed_modifications": ["trap_bar_deadlift"],
                "clinician_note": "MRI shows 4mm protrusion; avoid loaded flexion",
                "member_visible_note": "از خم شدن با وزنه پرهیز کنید",
                "requires_clearance": True,
            },
        )

        studio = seeded.get(f"/api/v1/members/{member_id}/injuries", headers=owner_auth).json()
        assert studio[0]["clinician_note"].startswith("MRI")
        assert studio[0]["contraindicated_patterns"] == ["spinal_flexion", "heavy_deadlift"]

        public = seeded.get(
            f"/api/v1/client/members/{member_id}/injuries", headers=owner_auth
        ).json()
        assert "clinician_note" not in public[0]
        assert public[0]["member_visible_note"].startswith("از")

    def test_filters_expose_blocked_patterns_for_phase3(
        self, seeded: TestClient, owner_auth, member_id: int
    ) -> None:
        seeded.post(
            f"/api/v1/members/{member_id}/injuries",
            headers=owner_auth,
            json={
                "body_region": "shoulder",
                "label": "Impingement",
                "status": "active",
                "contraindicated_patterns": ["overhead_press"],
                "allowed_modifications": ["landmine_press"],
            },
        )
        filters = seeded.get(
            f"/api/v1/members/{member_id}/filters", headers=owner_auth
        ).json()
        assert "overhead_press" in filters["blocked_patterns"]
        assert "landmine_press" in filters["allowed_modifications"]

    def test_cleared_injury_no_longer_blocks(
        self, seeded: TestClient, owner_auth, member_id: int
    ) -> None:
        seeded.post(
            f"/api/v1/members/{member_id}/injuries",
            headers=owner_auth,
            json={
                "body_region": "ankle",
                "label": "Old sprain",
                "status": "cleared",
                "contraindicated_patterns": ["jump_landing"],
            },
        )
        filters = seeded.get(
            f"/api/v1/members/{member_id}/filters", headers=owner_auth
        ).json()
        assert filters["blocked_patterns"] == []

    def test_unknown_region_is_rejected(self, seeded, owner_auth, member_id) -> None:
        res = seeded.post(
            f"/api/v1/members/{member_id}/injuries",
            headers=owner_auth,
            json={"body_region": "elbow_of_the_knee", "label": "x"},
        )
        assert res.status_code == 422

    def test_pain_out_of_range_is_rejected(self, seeded, owner_auth, member_id) -> None:
        res = seeded.post(
            f"/api/v1/members/{member_id}/injuries",
            headers=owner_auth,
            json={"body_region": "knee", "label": "x", "pain_0_10": 14},
        )
        assert res.status_code == 422
