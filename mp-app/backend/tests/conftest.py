"""Shared fixtures: every test gets a throwaway database."""

from __future__ import annotations

import sys
from collections.abc import Iterator
from pathlib import Path

import pytest

# Allow ``pytest`` to run from mp-app/backend without installation.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient  # noqa: E402

from app.config import Settings  # noqa: E402
from app.db import make_engine  # noqa: E402
from app.main import create_app  # noqa: E402
from app.migrations import migrate  # noqa: E402


@pytest.fixture
def db_path(tmp_path: Path) -> Path:
    """A fresh SQLite file per test."""
    return tmp_path / "mp-test.db"


@pytest.fixture
def engine(db_path: Path):
    """Migrated engine on a temp database."""
    eng = make_engine(db_path)
    migrate(eng)
    yield eng
    eng.dispose()


@pytest.fixture
def raw_engine(db_path: Path):
    """Engine with NO migrations applied."""
    eng = make_engine(db_path)
    yield eng
    eng.dispose()


@pytest.fixture
def client(db_path: Path) -> Iterator[TestClient]:
    """HTTP client against a fully migrated app."""
    app = create_app(Settings(db_path=db_path))
    with TestClient(app) as test_client:
        yield test_client
