"""Local-only security primitives: PIN hashing, session tokens, signed QR.

Map §15 constraints this module must satisfy:
* PIN/passwords hashed (PBKDF2-HMAC-SHA256 from the stdlib — no new dependency,
  and MP must install on an air-gapped gym PC);
* session secrets stay on this machine (never a cloud KMS);
* QR payloads are HMAC-signed with the gym secret so a photographed code cannot
  be forged or replayed after expiry;
* constant-time comparison everywhere a secret is checked.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import json
import os
import secrets
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any

PBKDF2_ALGO = "sha256"
PBKDF2_ITERATIONS = 200_000
QR_VERSION = 1


class SecurityError(ValueError):
    """Base class for auth/token/QR failures."""


class InvalidCredentialsError(SecurityError):
    """Wrong PIN or password."""


class TokenError(SecurityError):
    """Session token missing, malformed, expired or forged."""


class QrError(SecurityError):
    """QR payload malformed, expired or signature-invalid."""


# --------------------------------------------------------------------------- #
# PIN / password hashing
# --------------------------------------------------------------------------- #


def hash_secret(secret: str, *, iterations: int = PBKDF2_ITERATIONS) -> str:
    """Hash a PIN/password as ``algo$iterations$salt$digest`` (all hex).

    Raises:
        SecurityError: empty secret (an empty PIN is a policy bug, not a hash).
    """
    if not secret:
        raise SecurityError("secret must not be empty")
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac(PBKDF2_ALGO, secret.encode(), salt, iterations)
    return f"{PBKDF2_ALGO}${iterations}${salt.hex()}${digest.hex()}"


def verify_secret(secret: str, stored: str) -> bool:
    """Constant-time check of ``secret`` against a ``hash_secret`` string."""
    if not stored:
        return False
    parts = stored.split("$")
    if len(parts) != 4:
        return False
    algo, raw_iter, salt_hex, digest_hex = parts
    if algo != PBKDF2_ALGO:
        return False
    try:
        iterations = int(raw_iter)
        salt = bytes.fromhex(salt_hex)
        expected = bytes.fromhex(digest_hex)
    except ValueError:
        return False
    actual = hashlib.pbkdf2_hmac(algo, secret.encode(), salt, iterations)
    return hmac.compare_digest(actual, expected)


# --------------------------------------------------------------------------- #
# Session tokens (compact, local, no external dependency)
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class Principal:
    """Who a request belongs to."""

    subject: str
    role: str
    gym_id: int
    member_id: int | None = None


def _b64e(raw: bytes) -> str:
    return base64.urlsafe_b64encode(raw).decode().rstrip("=")


def _b64d(text: str) -> bytes:
    return base64.urlsafe_b64decode(text + "=" * (-len(text) % 4))


def issue_token(
    principal: Principal, *, secret_key: str, ttl_seconds: int = 8 * 3600
) -> str:
    """Sign a session token: ``base64(payload).base64(hmac_sha256)``.

    Args:
        principal: the identity to embed.
        secret_key: machine-local key (never leaves this PC).
        ttl_seconds: default 8h = one gym shift.
    """
    if ttl_seconds <= 0:
        raise SecurityError("ttl_seconds must be positive")
    now = int(time.time())
    payload = {
        "sub": principal.subject,
        "role": principal.role,
        "gym": principal.gym_id,
        "mid": principal.member_id,
        "iat": now,
        "exp": now + ttl_seconds,
        "jti": secrets.token_hex(8),
    }
    body = _b64e(json.dumps(payload, separators=(",", ":"), sort_keys=True).encode())
    signature = _b64e(hmac.new(secret_key.encode(), body.encode(), hashlib.sha256).digest())
    return f"{body}.{signature}"


def verify_token(token: str, *, secret_key: str, now: int | None = None) -> Principal:
    """Verify signature + expiry and return the embedded principal.

    Raises:
        TokenError: malformed, forged, or expired.
    """
    if not token or "." not in token:
        raise TokenError("token missing or malformed")
    body, _, signature = token.partition(".")
    expected = _b64e(hmac.new(secret_key.encode(), body.encode(), hashlib.sha256).digest())
    if not hmac.compare_digest(expected, signature):
        raise TokenError("bad signature")

    try:
        payload: dict[str, Any] = json.loads(_b64d(body))
    except (ValueError, json.JSONDecodeError) as exc:
        raise TokenError("unreadable payload") from exc

    current = int(time.time()) if now is None else now
    exp = payload.get("exp")
    if not isinstance(exp, int) or current >= exp:
        raise TokenError("token expired")

    subject = payload.get("sub")
    role = payload.get("role")
    gym = payload.get("gym")
    if not isinstance(subject, str) or not isinstance(role, str) or not isinstance(gym, int):
        raise TokenError("incomplete claims")

    member_id = payload.get("mid")
    return Principal(
        subject=subject,
        role=role,
        gym_id=gym,
        member_id=member_id if isinstance(member_id, int) else None,
    )


# --------------------------------------------------------------------------- #
# Signed QR identity (map §8: {v, typ, gym, mid, exp, sig})
# --------------------------------------------------------------------------- #


def sign_qr(
    *,
    gym_id: int,
    member_id: int,
    secret_key: str,
    typ: str = "member",
    ttl_seconds: int = 60,
) -> dict[str, Any]:
    """Build a signed, short-lived QR payload for check-in."""
    exp = int(time.time()) + ttl_seconds
    core = {"v": QR_VERSION, "typ": typ, "gym": gym_id, "mid": member_id, "exp": exp}
    canonical = json.dumps(core, separators=(",", ":"), sort_keys=True).encode()
    sig = hmac.new(secret_key.encode(), canonical, hashlib.sha256).hexdigest()
    return {**core, "sig": sig}


def verify_qr(payload: dict[str, Any], *, secret_key: str, now: int | None = None) -> dict[str, Any]:
    """Validate a scanned QR payload.

    Raises:
        QrError: bad shape, bad signature, or expired.
    """
    core = {k: payload.get(k) for k in ("v", "typ", "gym", "mid", "exp")}
    if any(core[k] is None for k in ("typ", "gym", "mid", "exp")):
        raise QrError("payload missing fields")
    if core["v"] != QR_VERSION:
        raise QrError(f"unsupported QR version {core['v']!r}")

    canonical = json.dumps(core, separators=(",", ":"), sort_keys=True).encode()
    expected = hmac.new(secret_key.encode(), canonical, hashlib.sha256).hexdigest()
    provided = payload.get("sig")
    if not isinstance(provided, str) or not hmac.compare_digest(expected, provided):
        raise QrError("bad signature")

    current = int(time.time()) if now is None else now
    if current >= int(core["exp"]):
        raise QrError("qr expired")
    return core


# --------------------------------------------------------------------------- #
# Machine-local key management
# --------------------------------------------------------------------------- #


def load_or_create_secret_key(path: Path) -> str:
    """Read the machine-local key, creating it (mode 0600) on first run."""
    if path.exists():
        stored = path.read_text(encoding="utf-8").strip()
        if stored:
            return stored
    path.parent.mkdir(parents=True, exist_ok=True)
    key = secrets.token_urlsafe(48)
    path.write_text(key, encoding="utf-8")
    try:
        os.chmod(path, 0o600)
    except OSError:  # pragma: no cover - Windows/odd filesystems
        pass
    return key
