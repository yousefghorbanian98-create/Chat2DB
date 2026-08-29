"""Phase 2 Ops: attendance QR check-in, payments + receipt, equipment, KPIs."""

from __future__ import annotations

import time
from datetime import date, timedelta

from fastapi.testclient import TestClient

from app.core.security import sign_qr
from app.state import get_secret_key


def _qr(seeded: TestClient, member_id: int, **overrides) -> dict:
    payload = sign_qr(gym_id=1, member_id=member_id, secret_key=get_secret_key(), ttl_seconds=60)
    return {**payload, **overrides}


class TestAttendance:
    def test_signed_qr_checks_in(self, seeded, reception_auth, member_id) -> None:
        res = seeded.post(
            "/api/v1/attendance/check-in",
            headers=reception_auth,
            json={"payload": _qr(seeded, member_id)},
        )
        assert res.status_code == 201, res.text
        assert res.json()["method"] == "qr"
        assert res.json()["member_id"] == member_id

    def test_tampered_qr_is_rejected(self, seeded, reception_auth, member_id) -> None:
        res = seeded.post(
            "/api/v1/attendance/check-in",
            headers=reception_auth,
            json={"payload": _qr(seeded, member_id, mid=member_id + 1)},
        )
        assert res.status_code == 401

    def test_expired_qr_is_rejected(self, seeded, reception_auth, member_id) -> None:
        payload = sign_qr(
            gym_id=1, member_id=member_id, secret_key=get_secret_key(), ttl_seconds=1
        )
        time.sleep(1.2)
        res = seeded.post(
            "/api/v1/attendance/check-in",
            headers=reception_auth,
            json={"payload": payload},
        )
        assert res.status_code == 401

    def test_double_check_in_is_a_conflict(self, seeded, reception_auth, member_id) -> None:
        seeded.post(
            "/api/v1/attendance/check-in",
            headers=reception_auth,
            json={"payload": _qr(seeded, member_id)},
        )
        res = seeded.post(
            "/api/v1/attendance/check-in",
            headers=reception_auth,
            json={"payload": _qr(seeded, member_id)},
        )
        assert res.status_code == 409

    def test_expired_membership_is_denied_at_the_door(
        self, seeded: TestClient, owner_auth, reception_auth
    ) -> None:
        """DoD #5: an expired membership cannot check in."""
        mid = seeded.post(
            "/api/v1/members",
            headers=owner_auth,
            json={
                "membership_code": "MP-EXP",
                "first_name": "Late",
                "last_name": "Payer",
                "sex": "male",
                "membership_exp": (date.today() - timedelta(days=1)).isoformat(),
            },
        ).json()["id"]
        res = seeded.post(
            "/api/v1/attendance/check-in",
            headers=reception_auth,
            json={"payload": _qr(seeded, mid)},
        )
        assert res.status_code == 402

    def test_check_out_closes_the_visit_and_today_counts(
        self, seeded, reception_auth, member_id
    ) -> None:
        seeded.post(
            "/api/v1/attendance/check-in",
            headers=reception_auth,
            json={"payload": _qr(seeded, member_id)},
        )
        out = seeded.post(f"/api/v1/attendance/check-out/{member_id}", headers=reception_auth)
        assert out.status_code == 200
        assert out.json()["checked_out"] is not None

        count = seeded.get("/api/v1/attendance/today", headers=reception_auth)
        assert count.json()["check_ins"] >= 1

    def test_check_out_without_open_visit_is_404(self, seeded, reception_auth, member_id) -> None:
        res = seeded.post(f"/api/v1/attendance/check-out/{member_id}", headers=reception_auth)
        assert res.status_code == 404


class TestPayments:
    def test_reception_records_cash_payment_and_gets_receipt(
        self, seeded, owner_auth, reception_auth, member_id
    ) -> None:
        pkg = seeded.post(
            "/api/v1/packages",
            headers=owner_auth,
            json={"name": "ماهانه", "duration_days": 30, "price_rial": 50_000_000},
        ).json()

        pay = seeded.post(
            "/api/v1/payments",
            headers=reception_auth,
            json={"member_id": member_id, "amount_rial": 50_000_000, "package_id": pkg["id"]},
        )
        assert pay.status_code == 201, pay.text
        receipt_no = pay.json()["receipt_no"]
        assert receipt_no.startswith("R-1-")

        pdf = seeded.get(f"/api/v1/payments/{pay.json()['id']}/receipt", headers=reception_auth)
        assert pdf.status_code == 200
        assert pdf.headers["content-type"] == "application/pdf"
        assert pdf.content[:5] == b"%PDF-"

    def test_rial_formatter_groups_thousands(self) -> None:
        from app.core.receipt_pdf import _rial

        assert _rial(1_234_567) == "1,234,567 Rial"
        assert _rial(0) == "0 Rial"

    def test_receipt_uncompressed_contains_grouped_rial(
        self, seeded, reception_auth, member_id
    ) -> None:
        """Direct (uncompressed) render so the text layer is assertable."""
        from app.core.receipt_pdf import build_receipt_pdf

        pdf = build_receipt_pdf(
            gym_name="Muscle Paradise",
            payment={
                "receipt_no": "R-1-000001",
                "member_id": member_id,
                "package_id": None,
                "amount_rial": 1_234_567,
                "method": "cash",
                "created_at": "2026-08-29T10:00:00Z",
                "voided": 0,
            },
            member={"first_name": "Sara", "last_name": "Azad"},
            package_name=None,
            compress=False,
        )
        assert b"1,234,567 Rial" in pdf

    def test_reception_cannot_void_a_payment(
        self, seeded, reception_auth, owner_auth, member_id
    ) -> None:
        pay = seeded.post(
            "/api/v1/payments",
            headers=reception_auth,
            json={"member_id": member_id, "amount_rial": 100},
        ).json()
        assert (
            seeded.post(f"/api/v1/payments/{pay['id']}/void", headers=reception_auth).status_code
            == 403
        )
        assert (
            seeded.post(f"/api/v1/payments/{pay['id']}/void", headers=owner_auth).status_code
            == 200
        )

    def test_trainer_cannot_create_packages(self, seeded, trainer_auth) -> None:
        res = seeded.post(
            "/api/v1/packages",
            headers=trainer_auth,
            json={"name": "X", "duration_days": 30, "price_rial": 1},
        )
        assert res.status_code == 403


class TestEquipment:
    def test_admin_creates_and_toggles_equipment(self, seeded, owner_auth, trainer_auth) -> None:
        eq = seeded.post(
            "/api/v1/equipment",
            headers=owner_auth,
            json={"name": "Smith Machine", "category": "strength", "count": 2},
        )
        assert eq.status_code == 201

        listed = seeded.get("/api/v1/equipment", headers=trainer_auth)
        assert any(e["name"] == "Smith Machine" for e in listed.json())

        patch = seeded.patch(
            f"/api/v1/equipment/{eq.json()['id']}",
            headers=owner_auth,
            json={"available": False},
        )
        assert patch.json()["available"] is False

    def test_reception_cannot_add_equipment(self, seeded, reception_auth) -> None:
        res = seeded.post(
            "/api/v1/equipment",
            headers=reception_auth,
            json={"name": "Bench", "category": "strength"},
        )
        assert res.status_code == 403


class TestDashboard:
    def test_dashboard_aggregates_revenue_and_checkins(
        self, seeded, owner_auth, reception_auth, member_id
    ) -> None:
        seeded.post(
            "/api/v1/payments",
            headers=reception_auth,
            json={"member_id": member_id, "amount_rial": 777},
        )
        seeded.post(
            "/api/v1/attendance/check-in",
            headers=reception_auth,
            json={"payload": _qr(seeded, member_id)},
        )
        dash = seeded.get("/api/v1/reports/dashboard", headers=owner_auth).json()
        assert dash["revenue_rial_this_month"] >= 777
        assert dash["check_ins_today"] >= 1
        assert dash["members_total"] >= 1

    def test_trainer_has_no_full_finance_dashboard(self, seeded, trainer_auth) -> None:
        assert seeded.get("/api/v1/reports/dashboard", headers=trainer_auth).status_code == 403

    def test_reception_has_no_full_finance_dashboard(self, seeded, reception_auth) -> None:
        """Map §2.4: RECEPTION enters cash but does not read the full finance."""
        assert seeded.get("/api/v1/reports/dashboard", headers=reception_auth).status_code == 403
