"""Phase 6 API: encrypted backup/restore + delta sync, RBAC-gated."""

from __future__ import annotations


def test_backup_roundtrip_via_api(seeded, owner_auth, member_id) -> None:
    res = seeded.post(
        "/api/v1/admin/backup", headers=owner_auth, json={"password": "s3cret-pass"}
    )
    assert res.status_code == 200, res.text
    blob = res.json()["blob_b64"]

    restored = seeded.post(
        "/api/v1/admin/backup/restore",
        headers=owner_auth,
        json={"password": "s3cret-pass", "blob_b64": blob},
    )
    assert restored.status_code == 200, restored.text
    assert restored.json()["restored"]["members"] >= 1


def test_backup_wrong_password_422(seeded, owner_auth) -> None:
    blob = seeded.post(
        "/api/v1/admin/backup", headers=owner_auth, json={"password": "right-pass"}
    ).json()["blob_b64"]
    res = seeded.post(
        "/api/v1/admin/backup/restore",
        headers=owner_auth,
        json={"password": "wrong-pass", "blob_b64": blob},
    )
    assert res.status_code == 422


def test_backup_is_owner_only(seeded, trainer_auth, reception_auth) -> None:
    for auth in (trainer_auth, reception_auth):
        assert seeded.post(
            "/api/v1/admin/backup", headers=auth, json={"password": "whatever1"}
        ).status_code == 403


def test_backup_short_password_rejected(seeded, owner_auth) -> None:
    assert seeded.post(
        "/api/v1/admin/backup", headers=owner_auth, json={"password": "short"}
    ).status_code == 422


def test_sync_delta_returns_cursor_and_changes(seeded, owner_auth, member_id) -> None:
    res = seeded.get("/api/v1/sync/delta", headers=owner_auth)
    assert res.status_code == 200, res.text
    body = res.json()
    assert "cursor" in body and body["total"] >= 1
    assert "members" in body["changes"]

    # A second call with the cursor returns nothing new.
    again = seeded.get(
        "/api/v1/sync/delta", headers=owner_auth, params={"since": body["cursor"]}
    )
    assert again.status_code == 200
    assert again.json()["total"] == 0


def test_sync_is_staff_gated(seeded, kiosk_auth) -> None:
    assert seeded.get("/api/v1/sync/delta", headers=kiosk_auth).status_code == 403
