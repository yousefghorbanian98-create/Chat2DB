"""Security primitives: PIN hashing, session tokens, signed QR (map §15)."""

from __future__ import annotations

import time
from pathlib import Path

import pytest

from app.core.security import (
    InvalidCredentialsError,
    Principal,
    QrError,
    SecurityError,
    TokenError,
    hash_secret,
    issue_token,
    load_or_create_secret_key,
    sign_qr,
    verify_qr,
    verify_secret,
    verify_token,
)

SECRET = "test-machine-local-secret"


class TestPinHashing:
    def test_roundtrip_accepts_the_right_pin(self) -> None:
        stored = hash_secret("4821")
        assert verify_secret("4821", stored) is True

    def test_wrong_pin_is_rejected(self) -> None:
        stored = hash_secret("4821")
        assert verify_secret("4822", stored) is False

    def test_same_pin_hashes_differently_each_time(self) -> None:
        """Salt must be random — identical PINs must not look identical."""
        assert hash_secret("4821") != hash_secret("4821")

    def test_stored_format_is_self_describing(self) -> None:
        assert hash_secret("4821").startswith("sha256$200000$")

    def test_empty_pin_is_a_policy_error(self) -> None:
        with pytest.raises(SecurityError):
            hash_secret("")

    def test_garbage_stored_value_returns_false_not_raises(self) -> None:
        for bad in ("", "nope", "sha256$x$y$z", "md5$1$00$00"):
            assert verify_secret("4821", bad) is False

    def test_unknown_algo_is_rejected(self) -> None:
        assert verify_secret("4821", "md5$200000$00$00") is False

    def test_invalid_credentials_type_exists_for_callers(self) -> None:
        assert issubclass(InvalidCredentialsError, SecurityError)


class TestTokens:
    def test_roundtrip_preserves_identity(self) -> None:
        principal = Principal(subject="owner", role="OWNER", gym_id=1)
        token = issue_token(principal, secret_key=SECRET)
        got = verify_token(token, secret_key=SECRET)
        assert got.subject == "owner"
        assert got.role == "OWNER"
        assert got.gym_id == 1

    def test_member_claim_survives(self) -> None:
        token = issue_token(
            Principal(subject="m", role="MEMBER", gym_id=1, member_id=42),
            secret_key=SECRET,
        )
        assert verify_token(token, secret_key=SECRET).member_id == 42

    def test_forged_signature_is_rejected(self) -> None:
        token = issue_token(Principal("o", "OWNER", 1), secret_key=SECRET)
        body, _, _sig = token.partition(".")
        with pytest.raises(TokenError, match="signature"):
            verify_token(f"{body}.{'0' * 43}", secret_key=SECRET)

    def test_token_from_another_key_is_rejected(self) -> None:
        token = issue_token(Principal("o", "OWNER", 1), secret_key=SECRET)
        with pytest.raises(TokenError):
            verify_token(token, secret_key="a-different-machine-key")

    def test_tampered_role_claim_is_rejected(self) -> None:
        """Flipping MEMBER -> OWNER must break the signature."""
        token = issue_token(Principal("m", "MEMBER", 1, 7), secret_key=SECRET)
        body, _, sig = token.partition(".")
        forged_body = body.replace("TUVNQkVS", "T1dORVI")  # MEMBER -> OWNER in b64
        if forged_body == body:  # pragma: no cover - defensive
            pytest.skip("payload did not contain the expected b64 fragment")
        with pytest.raises(TokenError):
            verify_token(f"{forged_body}.{sig}", secret_key=SECRET)

    def test_expired_token_is_rejected(self) -> None:
        token = issue_token(Principal("o", "OWNER", 1), secret_key=SECRET, ttl_seconds=30)
        with pytest.raises(TokenError, match="expired"):
            verify_token(token, secret_key=SECRET, now=int(time.time()) + 31)

    def test_malformed_token_is_rejected(self) -> None:
        for bad in ("", "nodot", "a.b", "!!!.!!!"):
            with pytest.raises(TokenError):
                verify_token(bad, secret_key=SECRET)

    def test_non_positive_ttl_is_rejected(self) -> None:
        with pytest.raises(SecurityError):
            issue_token(Principal("o", "OWNER", 1), secret_key=SECRET, ttl_seconds=0)


class TestSignedQr:
    def test_roundtrip(self) -> None:
        payload = sign_qr(gym_id=1, member_id=7, secret_key=SECRET)
        core = verify_qr(payload, secret_key=SECRET)
        assert core["mid"] == 7
        assert core["gym"] == 1
        assert core["typ"] == "member"

    def test_forged_member_id_is_rejected(self) -> None:
        payload = sign_qr(gym_id=1, member_id=7, secret_key=SECRET)
        with pytest.raises(QrError, match="signature"):
            verify_qr({**payload, "mid": 8}, secret_key=SECRET)

    def test_qr_signed_by_another_gym_key_is_rejected(self) -> None:
        payload = sign_qr(gym_id=1, member_id=7, secret_key=SECRET)
        with pytest.raises(QrError):
            verify_qr(payload, secret_key="another-gym-key")

    def test_expired_qr_is_rejected(self) -> None:
        payload = sign_qr(gym_id=1, member_id=7, secret_key=SECRET, ttl_seconds=15)
        with pytest.raises(QrError, match="expired"):
            verify_qr(payload, secret_key=SECRET, now=int(time.time()) + 16)

    def test_incomplete_payload_is_rejected(self) -> None:
        with pytest.raises(QrError, match="missing"):
            verify_qr({"v": 1, "typ": "member"}, secret_key=SECRET)

    def test_future_qr_version_is_rejected(self) -> None:
        payload = sign_qr(gym_id=1, member_id=7, secret_key=SECRET)
        with pytest.raises(QrError, match="version"):
            verify_qr({**payload, "v": 99}, secret_key=SECRET)


class TestKeyManagement:
    def test_creates_then_reuses_the_machine_key(self, tmp_path: Path) -> None:
        path = tmp_path / "secret.key"
        first = load_or_create_secret_key(path)
        assert len(first) >= 32
        assert path.stat().st_mode & 0o777 == 0o600
        assert load_or_create_secret_key(path) == first

    def test_empty_key_file_is_regenerated(self, tmp_path: Path) -> None:
        path = tmp_path / "secret.key"
        path.write_text("   ", encoding="utf-8")
        assert load_or_create_secret_key(path).strip() != ""
