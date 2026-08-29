"""HTTP surface tests for the Phase 0 skeleton."""

from __future__ import annotations

import pytest


@pytest.mark.api
def test_health_at_root(client) -> None:
    body = client.get("/health").json()
    assert body["status"] == "ok"
    assert body["service"] == "muscle-paradise-core"
    assert body["db"]["ok"] is True
    assert body["db"]["schema_version"] == "0001_core"
    assert body["db"]["table_count"] >= 25  # 24 business + schema_migrations


@pytest.mark.api
def test_health_also_under_api_prefix(client) -> None:
    """Studio and the Flutter client both call /api/v1/health."""
    assert client.get("/api/v1/health").status_code == 200


@pytest.mark.api
def test_health_reports_degraded_when_db_is_broken(client, monkeypatch) -> None:
    """A dead DB must surface a recovery signal, not a 500."""
    from app.state import get_state

    engine = get_state().engine
    monkeypatch.setattr(engine, "connect", lambda: (_ for _ in ()).throw(RuntimeError("db gone")))

    body = client.get("/health").json()
    assert body["status"] == "degraded"
    assert body["db"]["ok"] is False
    assert "db gone" in body["db"]["error"]


@pytest.mark.api
def test_request_id_is_returned_and_reused(client) -> None:
    first = client.get("/health")
    assert first.headers["x-request-id"]
    second = client.get("/health", headers={"x-request-id": "abc123"})
    assert second.headers["x-request-id"] == "abc123"


@pytest.mark.api
def test_response_time_header_present(client) -> None:
    header = client.get("/health").headers["x-response-ms"]
    assert float(header) >= 0.0


@pytest.mark.api
def test_cors_allows_local_shell_only(client) -> None:
    ok = client.get("/health", headers={"origin": "http://127.0.0.1:5173"})
    assert ok.headers.get("access-control-allow-origin") == "http://127.0.0.1:5173"

    blocked = client.get("/health", headers={"origin": "https://evil.example"})
    assert "access-control-allow-origin" not in blocked.headers


@pytest.mark.api
def test_openapi_document_describes_health(client) -> None:
    spec = client.get("/openapi.json").json()
    assert "/health" in spec["paths"]
    assert spec["info"]["title"] == "Muscle Paradise Core"


@pytest.mark.api
def test_unknown_route_is_404_not_500(client) -> None:
    assert client.get("/api/v1/nope").status_code == 404
