"""Optional n8n bridge: config gating, signed events, redacted reports."""

from __future__ import annotations

import hashlib
import hmac
import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

import pytest

from app.automation import events


def test_sign_event_is_a_stable_hmac_sha256() -> None:
    payload = events.build_event("payment.created", 1, {"amount_rial": 100})
    sig = events.sign_event(payload, "secret")
    canonical = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()
    assert sig == hmac.new(b"secret", canonical, hashlib.sha256).hexdigest()
    assert len(sig) == 64


def test_emit_is_a_noop_when_disabled() -> None:
    events.set_config(enabled=False, url="http://127.0.0.1:1/x", secret="secretsecret")
    assert events.emit("payment.created", 1, {}) is False


def test_emit_delivers_a_signed_redacted_payload() -> None:
    received: dict = {}
    ready = threading.Event()

    class Handler(BaseHTTPRequestHandler):
        def do_POST(self):  # noqa: N802
            length = int(self.headers.get("Content-Length", 0))
            received["body"] = json.loads(self.rfile.read(length))
            received["sig"] = self.headers.get("X-MP-Signature")
            self.send_response(200)
            self.end_headers()

        def log_message(self, *a):  # silence
            pass

    server = HTTPServer(("127.0.0.1", 0), Handler)
    port = server.server_address[1]
    threading.Thread(target=server.serve_forever, daemon=True).start()
    ready.set()

    events.set_config(enabled=True, url=f"http://127.0.0.1:{port}/hook", secret="secretsecret")
    try:
        assert events.emit("membership.expiring", 1, {"days_left": 3}) is True
        import time

        for _ in range(50):
            if "body" in received:
                break
            time.sleep(0.02)
        assert received["body"]["event"] == "membership.expiring"
        assert received["body"]["privacy"] == {"phi": False, "redacted": True}
        assert received["sig"] == events.sign_event(received["body"], "secretsecret")
    finally:
        server.shutdown()
        events.set_config(enabled=False)


def test_config_view_never_leaks_the_secret(seeded, owner_auth) -> None:
    res = seeded.post(
        "/api/v1/automation/config",
        headers=owner_auth,
        json={"enabled": True, "url": "http://127.0.0.1:5678/h", "secret": "supersecretvalue"},
    )
    assert res.status_code == 200, res.text
    body = res.json()
    assert body["enabled"] is True
    assert body["secret_configured"] is True
    assert "supersecretvalue" not in json.dumps(body)
    # Reset so other tests see the bridge off.
    seeded.post("/api/v1/automation/config", headers=owner_auth, json={"enabled": False})


def test_config_is_owner_only(seeded, trainer_auth) -> None:
    assert seeded.get("/api/v1/automation/config", headers=trainer_auth).status_code == 403


def test_reports_are_staff_only_and_redacted(seeded, owner_auth, member_auth, member_id) -> None:
    exp = seeded.get("/api/v1/reports/expiring", headers=owner_auth)
    assert exp.status_code == 200
    assert seeded.get("/api/v1/reports/expiring", headers=member_auth(member_id)).status_code == 403

    inactive = seeded.get("/api/v1/reports/inactive-members", headers=owner_auth)
    assert inactive.status_code == 200
    # A fresh member has no attendance yet, so they show as inactive — redacted.
    rows = inactive.json()
    assert any(r["id"] == member_id for r in rows)
    assert all("clinician_note" not in r and "national_id" not in r for r in rows)


@pytest.mark.api
class TestWebhookSchemeAllowlist:
    """urlopen honours file:/ftp:; the bridge must only ever speak http(s)."""

    @pytest.mark.parametrize(
        "url",
        [
            "file:///etc/passwd",
            "ftp://example.com/x",
            "gopher://example.com",
            "http://",          # no host
            "not-a-url",
            "",
        ],
    )
    def test_rejects_non_http_urls(self, url: str) -> None:
        assert events.is_allowed_webhook(url) is False

    @pytest.mark.parametrize(
        "url",
        ["http://127.0.0.1:5678/webhook/mp", "https://n8n.gym.lan/webhook/mp"],
    )
    def test_accepts_http_and_https(self, url: str) -> None:
        assert events.is_allowed_webhook(url) is True

    def test_post_refuses_to_open_a_file_url(self) -> None:
        with pytest.raises(ValueError, match="non-http"):
            events._post("file:///etc/passwd", b"{}", "sig")
