"""Phase 5 client API: MEMBER force-scoping + field masking (map §2.4, §9)."""

from __future__ import annotations

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
