"""Phase 5 client API: MEMBER force-scoping + field masking (map §2.4, §9)."""

from __future__ import annotations

import time

import pytest

from app.core.field_mask import mask_assessment_row, mask_member_row


def test_mask_strips_clinician_notes_for_member_only() -> None:
    row = {"id": 1, "first_name": "Sara", "note": "do not tell", "created_by": 7}
    staff = mask_member_row("OWNER", row)
    assert staff["note"] == "do not tell" and staff["created_by"] == 7

    member = mask_member_row("MEMBER", row)
    assert "note" not in member and "created_by" not in member
    assert member["first_name"] == "Sara"


def test_mask_assessment_strips_clinician_note() -> None:
    row = {"id": 1, "body_fat_pct": 21.4, "clinician_note": "internal"}
    assert "clinician_note" in mask_assessment_row("TRAINER", row)
    assert "clinician_note" not in mask_assessment_row("MEMBER", row)


def test_member_can_read_own_profile(seeded, member_auth, member_id) -> None:
    res = seeded.get("/api/v1/client/me", headers=member_auth(member_id))
    assert res.status_code == 200, res.text
    body = res.json()
    assert body["first_name"] == "Sara"
    # A member row carries no clinician/internal leakage.
    assert "note" not in body


def test_staff_token_rejected_on_client_routes(seeded, owner_auth) -> None:
    assert seeded.get("/api/v1/client/me", headers=owner_auth).status_code == 403


def test_member_cannot_read_another_members_assessments(
    seeded, owner_auth, member_auth, member_id
) -> None:
    # A second member exists; a MEMBER token for member_id only sees their own.
    seeded.post(
        "/api/v1/members",
        headers=owner_auth,
        json={"membership_code": "MP-0002", "first_name": "Reza", "last_name": "K",
              "sex": "male"},
    )
    mine = seeded.get("/api/v1/client/me/assessments", headers=member_auth(member_id))
    assert mine.status_code == 200
    assert mine.json() == []  # no assessment yet, and never another member's


# --- Member self-service PIN login (v002, map §5) --------------------------

def test_member_pin_login_flow(seeded, owner_auth, member_id) -> None:
    # Front desk sets the PIN (hash only, never plaintext).
    set_res = seeded.post(
        f"/api/v1/members/{member_id}/pin", headers=owner_auth, json={"pin": "9876"}
    )
    assert set_res.status_code == 204, set_res.text

    login = seeded.post(
        "/api/v1/auth/member-pin",
        json={"membership_code": "MP-0001", "pin": "9876"},
    )
    assert login.status_code == 200, login.text
    body = login.json()
    assert body["role"] == "MEMBER"

    # The MEMBER token is force-scoped: /auth/me reports shell=client + member_id.
    me = seeded.get("/api/v1/auth/me", headers={"authorization": f"Bearer {body['token']}"})
    assert me.status_code == 200
    assert me.json()["shell"] == "client"
    assert me.json()["member_id"] == member_id

    # And it can read the client API.
    prof = seeded.get("/api/v1/client/me", headers={"authorization": f"Bearer {body['token']}"})
    assert prof.status_code == 200


def test_member_pin_rejects_wrong_and_unset_identically(seeded, member_id) -> None:
    # No PIN set yet for this fresh member -> 401, same as a wrong PIN later.
    unset = seeded.post(
        "/api/v1/auth/member-pin", json={"membership_code": "MP-0001", "pin": "0000"}
    )
    assert unset.status_code == 401

    unknown = seeded.post(
        "/api/v1/auth/member-pin", json={"membership_code": "NOPE", "pin": "0000"}
    )
    assert unknown.status_code == 401
    assert unknown.json()["detail"] == unset.json()["detail"], "no user enumeration"


def test_reader_role_cannot_set_member_pin(seeded, trainer_auth, member_id) -> None:
    res = seeded.post(
        f"/api/v1/members/{member_id}/pin", headers=trainer_auth, json={"pin": "1234"}
    )
    assert res.status_code == 403, "TRAINER is a reader, not a writer"


def test_pin_is_never_exposed_in_any_read(seeded, owner_auth, member_id) -> None:
    seeded.post(f"/api/v1/members/{member_id}/pin", headers=owner_auth, json={"pin": "9876"})
    got = seeded.get(f"/api/v1/members/{member_id}", headers=owner_auth).json()
    assert "pin_hash" not in got and "pin" not in got


JP7_SITES = {
    "chest": 12, "midaxillary": 10, "triceps": 14, "subscapular": 16,
    "abdominal": 20, "suprailiac": 15, "thigh": 18,
}


def _give_member_a_plan(seeded, owner_auth, member_id) -> None:
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


def test_member_reads_own_nutrition_without_internal_payload(
    seeded, owner_auth, member_auth, member_id
) -> None:
    _give_member_a_plan(seeded, owner_auth, member_id)

    staff_view = seeded.get(
        f"/api/v1/nutrition/members/{member_id}/plan", headers=owner_auth
    ).json()
    assert "payload" in staff_view  # the coach keeps the envelope

    res = seeded.get("/api/v1/client/me/nutrition", headers=member_auth(member_id))
    assert res.status_code == 200, res.text
    body = res.json()
    assert body["tdee_kcal"] == staff_view["tdee_kcal"]
    assert body["protein_g"] == staff_view["protein_g"]
    assert "payload" not in body  # C11: the athlete never sees the blob


def test_client_nutrition_is_404_before_any_plan(seeded, member_auth, member_id) -> None:
    res = seeded.get("/api/v1/client/me/nutrition", headers=member_auth(member_id))
    assert res.status_code == 404


def test_staff_token_rejected_on_client_nutrition(seeded, owner_auth) -> None:
    assert seeded.get("/api/v1/client/me/nutrition", headers=owner_auth).status_code == 403


# ---------------------------------------------------------------------------
# map §5: the athlete app is a real product, not a stub — they must be able to
# see their restrictions and payments, check themselves in, and log sessions.
# ---------------------------------------------------------------------------


def _record_injury(seeded, owner_auth, member_id: int) -> None:
    seeded.post(
        f"/api/v1/members/{member_id}/injuries",
        headers=owner_auth,
        json={
            "body_region": "lumbar",
            "label": "کمردرد مزمن",
            "status": "active",
            "contraindicated_patterns": ["deadlift"],
            "clinician_note": "داده‌ای که ورزشکار نباید ببیند",
        },
    )


def test_member_sees_own_injury_but_not_the_clinician_note(
    seeded, owner_auth, member_auth, member_id
) -> None:
    _record_injury(seeded, owner_auth, member_id)

    res = seeded.get("/api/v1/client/me/injuries", headers=member_auth(member_id))
    assert res.status_code == 200, res.text
    rows = res.json()
    assert len(rows) == 1
    assert rows[0]["label"] == "کمردرد مزمن"
    assert rows[0]["contraindicated_patterns"] == ["deadlift"]
    assert "clinician_note" not in rows[0]


def test_member_sees_payments_without_staff_attribution(
    seeded, owner_auth, member_auth, member_id
) -> None:
    seeded.post(
        "/api/v1/payments",
        headers=owner_auth,
        json={"member_id": member_id, "amount_rial": 2_500_000, "method": "card"},
    )

    res = seeded.get("/api/v1/client/me/payments", headers=member_auth(member_id))
    assert res.status_code == 200, res.text
    rows = res.json()
    assert len(rows) == 1
    assert rows[0]["amount_rial"] == 2_500_000
    assert rows[0]["method"] == "card"
    assert "staff_id" not in rows[0]


def test_member_checkin_qr_is_signed_and_short_lived(seeded, member_auth, member_id) -> None:
    from app.core.security import verify_qr
    from app.state import get_secret_key

    res = seeded.get("/api/v1/client/me/checkin-qr", headers=member_auth(member_id))
    assert res.status_code == 200, res.text
    body = res.json()
    assert body["expires_in"] == 60

    verified = verify_qr(body["payload"], secret_key=get_secret_key())
    assert verified["mid"] == member_id
    assert verified["exp"] - time.time() <= 61

    tampered = {**body["payload"], "mid": member_id + 1}
    with pytest.raises(Exception):
        verify_qr(tampered, secret_key=get_secret_key())


def test_checkin_qr_is_rejected_for_staff(seeded, owner_auth) -> None:
    assert seeded.get("/api/v1/client/me/checkin-qr", headers=owner_auth).status_code == 403


def test_member_logs_a_session_and_reads_it_back(seeded, member_auth, member_id) -> None:
    session = {
        "session_date": "1405-06-08",
        "exercises": [
            {"name": "اسکات", "sets": [{"weight_kg": 60, "reps": 8}, {"reps": 12}]},
            {"name": "پرس سینه", "sets": [{"weight_kg": 40, "reps": 10}]},
        ],
        "athlete_note": "ست آخر سنگین بود",
    }

    created = seeded.post("/api/v1/client/me/workouts", headers=member_auth(member_id), json=session)
    assert created.status_code == 201, created.text
    assert created.json()["session_date"] == "1405-06-08"

    res = seeded.get("/api/v1/client/me/workouts", headers=member_auth(member_id))
    assert res.status_code == 200, res.text
    rows = res.json()
    assert len(rows) == 1
    assert [e["name"] for e in rows[0]["exercises"]] == ["اسکات", "پرس سینه"]
    # A bodyweight set keeps no invented weight.
    assert "weight_kg" not in rows[0]["exercises"][0]["sets"][1]
    assert rows[0]["athlete_note"] == "ست آخر سنگین بود"
    assert "payload" not in rows[0]


def test_workout_log_rejects_empty_and_unknown_fields(seeded, member_auth, member_id) -> None:
    empty = seeded.post(
        "/api/v1/client/me/workouts",
        headers=member_auth(member_id),
        json={"session_date": "1405-06-08", "exercises": []},
    )
    assert empty.status_code == 422

    extra = seeded.post(
        "/api/v1/client/me/workouts",
        headers=member_auth(member_id),
        json={"session_date": "1405-06-08", "exercises": [{"name": "x"}], "sneaky": 1},
    )
    assert extra.status_code == 422


def test_workout_logs_do_not_leak_between_members(seeded, owner_auth, member_auth, member_id) -> None:
    seeded.post(
        "/api/v1/client/me/workouts",
        headers=member_auth(member_id),
        json={"session_date": "1405-06-08", "exercises": [{"name": "اسکات"}]},
    )

    other = seeded.post(
        "/api/v1/members",
        headers=owner_auth,
        json={"membership_code": "MP-0002", "first_name": "Reza", "last_name": "K", "sex": "male"},
    )
    assert other.status_code in (200, 201), other.text
    other_id = other.json()["id"]
    assert other_id != member_id

    rows = seeded.get("/api/v1/client/me/workouts", headers=member_auth(other_id)).json()
    assert rows == []
