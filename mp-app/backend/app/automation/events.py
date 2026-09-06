"""Signed, best-effort webhook events for the optional n8n bridge.

Nothing here may ever raise into a request path: a dead n8n instance is an
ops inconvenience, never a correctness bug for the gym (map §12.8). Payloads
are PHI-redacted by construction.
"""

from __future__ import annotations

import hashlib
import hmac
import json
import threading
import time
import urllib.parse
import urllib.request
from dataclasses import dataclass
from typing import Any


@dataclass
class AutomationConfig:
    """Runtime toggle for the bridge; defaults to OFF (core-first)."""

    enabled: bool = False
    url: str = ""
    secret: str = ""
    allowed_channels: tuple[str, ...] = ("telegram", "whatsapp", "sms", "email")
    forbid_phi: bool = True


#: Single process-wide instance; replaced atomically by the owner endpoint.
_CONFIG = AutomationConfig()
_LOCK = threading.Lock()


def get_config() -> AutomationConfig:
    with _LOCK:
        return _CONFIG


def set_config(**kwargs: Any) -> AutomationConfig:
    """Replace the runtime config (owner-only at the router layer)."""
    global _CONFIG
    with _LOCK:
        current = {
            "enabled": _CONFIG.enabled,
            "url": _CONFIG.url,
            "secret": _CONFIG.secret,
            "allowed_channels": _CONFIG.allowed_channels,
            "forbid_phi": _CONFIG.forbid_phi,
        }
        current.update(kwargs)
        _CONFIG = AutomationConfig(**current)
        return _CONFIG


def sign_event(payload: dict[str, Any], secret: str) -> str:
    """HMAC-SHA256 over the canonical JSON, hex-encoded."""
    canonical = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()
    return hmac.new(secret.encode(), canonical, hashlib.sha256).hexdigest()


def build_event(event: str, gym_id: int, data: dict[str, Any]) -> dict[str, Any]:
    """The envelope from the bridge doc §3 (PHI-redacted by callers)."""
    return {
        "v": 1,
        "event": event,
        "gym_id": gym_id,
        "at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "data": data,
        "privacy": {"phi": False, "redacted": True},
    }


#: The bridge posts to an owner-supplied URL. urlopen honours ``file:``,
#: ``ftp:`` and any custom scheme, so an operator (or anyone who reaches the
#: config endpoint) could otherwise turn the webhook into a local-file read.
_ALLOWED_SCHEMES = frozenset({"http", "https"})


def is_allowed_webhook(url: str) -> bool:
    """True when ``url`` is an http(s) URL with a host — the only shape we POST to."""
    try:
        parsed = urllib.parse.urlparse(url)
    except ValueError:
        return False
    return parsed.scheme in _ALLOWED_SCHEMES and bool(parsed.hostname)


def _post(url: str, body: bytes, signature: str) -> None:
    if not is_allowed_webhook(url):
        raise ValueError(f"refusing non-http(s) automation URL: {url!r}")
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json", "X-MP-Signature": signature},
        method="POST",
    )
    # Scheme is validated immediately above, so urlopen cannot reach file:/ftp:.
    with urllib.request.urlopen(req, timeout=5) as res:  # noqa: S310
        res.read()


def emit(event: str, gym_id: int, data: dict[str, Any]) -> bool:
    """Fire-and-forget delivery in a daemon thread. Returns whether it was sent.

    Returns False (and never raises) when the bridge is disabled or misconfigured.
    """
    cfg = get_config()
    if not cfg.enabled or not cfg.url or not cfg.secret:
        return False
    payload = build_event(event, gym_id, data)
    signature = sign_event(payload, cfg.secret)
    body = json.dumps(payload, ensure_ascii=False).encode()

    def _run() -> None:
        try:
            _post(cfg.url, body, signature)
        except Exception:  # best-effort: a dead n8n must not surface anywhere
            pass

    threading.Thread(target=_run, daemon=True).start()
    return True


__all__ = [
    "AutomationConfig",
    "build_event",
    "emit",
    "get_config",
    "set_config",
    "sign_event",
]
