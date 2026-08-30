"""Packaged single-service mode: the core serves a built Studio shell at `/`.

The installer ships one process on one port, so the API must keep winning over
the static catch-all and a bad `MP_STATIC_DIR` must fail loudly.
"""

from __future__ import annotations

from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from app.config import Settings
from app.main import create_app


def _shell(root: Path) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    (root / "index.html").write_text("<!doctype html><title>MP Studio</title>", encoding="utf-8")
    assets = root / "assets"
    assets.mkdir(exist_ok=True)
    (assets / "app.js").write_text("console.log('mp')", encoding="utf-8")
    return root


@pytest.mark.api
def test_serves_the_built_shell_at_root(tmp_path: Path) -> None:
    app = create_app(
        Settings(
            db_path=tmp_path / "mp.db",
            secret_key="test-machine-local-secret",
            static_dir=str(_shell(tmp_path / "dist")),
        )
    )
    with TestClient(app) as client:
        res = client.get("/")
        assert res.status_code == 200, res.text
        assert "MP Studio" in res.text
        assert client.get("/assets/app.js").status_code == 200


@pytest.mark.api
def test_api_routes_still_win_over_the_static_catchall(tmp_path: Path) -> None:
    app = create_app(
        Settings(
            db_path=tmp_path / "mp.db",
            secret_key="test-machine-local-secret",
            static_dir=str(_shell(tmp_path / "dist")),
        )
    )
    with TestClient(app) as client:
        assert client.get("/health").json()["status"] == "ok"
        assert client.get("/api/v1/health").status_code == 200
        assert client.get("/meta").json()["service"] == "muscle-paradise-core"


def test_missing_index_html_is_a_loud_failure(tmp_path: Path) -> None:
    empty = tmp_path / "dist"
    empty.mkdir()
    with pytest.raises(ValueError, match="no index.html"):
        create_app(
            Settings(
                db_path=tmp_path / "mp.db",
                secret_key="test-machine-local-secret",
                static_dir=str(empty),
            )
        )


@pytest.mark.api
def test_api_only_by_default(tmp_path: Path) -> None:
    """No MP_STATIC_DIR means no shell is served — the dev setup is unchanged."""
    app = create_app(Settings(db_path=tmp_path / "mp.db", secret_key="test-machine-local-secret"))
    with TestClient(app) as client:
        assert client.get("/").status_code == 404
        assert client.get("/health").status_code == 200


def test_static_dir_comes_from_the_environment() -> None:
    settings = Settings.from_env({"MP_STATIC_DIR": "/opt/mp/studio", "MP_DB_PATH": "/tmp/x.db"})
    assert settings.static_dir == "/opt/mp/studio"
    assert Settings.from_env({"MP_DB_PATH": "/tmp/x.db"}).static_dir == ""
