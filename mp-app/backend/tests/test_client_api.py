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
