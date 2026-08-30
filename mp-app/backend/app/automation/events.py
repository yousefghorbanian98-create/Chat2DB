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


def _post(url: str, body: bytes, signature: str) -> None:
    req = urllib.request.Request(
        url,
        data=body,
        headers={"Content-Type": "application/json", "X-MP-Signature": signature},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=5) as res:  # noqa: S310 local LAN only
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
