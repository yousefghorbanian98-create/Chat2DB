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
    """HTTP client against a fully migrated app (fixed test secret)."""
    app = create_app(Settings(db_path=db_path, secret_key="test-machine-local-secret"))
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def seeded(client: TestClient, db_path: Path) -> TestClient:
    """Client with one gym + staff accounts for every role."""
    from app.repo import staff as staff_repo
    from app.state import get_engine

    engine = get_engine()
    gym_id = staff_repo.ensure_gym(engine, "Muscle Paradise")
    for username, role, pin in (
        ("owner", "OWNER", "1111"),
        ("trainer", "TRAINER", "2222"),
        ("reception", "RECEPTION", "3333"),
        ("kiosk", "KIOSK", "4444"),
    ):
        staff_repo.create_staff(engine, gym_id=gym_id, username=username, role=role, pin=pin)
    return client


def _login(client: TestClient, username: str, pin: str) -> str:
    res = client.post("/api/v1/auth/pin", json={"username": username, "pin": pin})
    assert res.status_code == 200, res.text
    return str(res.json()["token"])


@pytest.fixture
def owner_auth(seeded: TestClient) -> dict[str, str]:
    return {"authorization": f"Bearer {_login(seeded, 'owner', '1111')}"}


@pytest.fixture
def trainer_auth(seeded: TestClient) -> dict[str, str]:
    return {"authorization": f"Bearer {_login(seeded, 'trainer', '2222')}"}


@pytest.fixture
def reception_auth(seeded: TestClient) -> dict[str, str]:
    return {"authorization": f"Bearer {_login(seeded, 'reception', '3333')}"}


@pytest.fixture
def kiosk_auth(seeded: TestClient) -> dict[str, str]:
    return {"authorization": f"Bearer {_login(seeded, 'kiosk', '4444')}"}


@pytest.fixture
def assigned_trainer_auth(seeded: TestClient, trainer_auth: dict[str, str]):
    """Trainer token + a helper that assigns a member to that trainer.

    Map §2.4 scopes a TRAINER to assigned members, so tests that exercise
    trainer-side features must state the assignment explicitly.
    """
    from sqlalchemy import text

    from app.repo import staff as staff_repo
    from app.state import get_engine

    def assign(member_id: int) -> None:
        engine = get_engine()
        gym_id = staff_repo.ensure_gym(engine)
        trainer = staff_repo.find_staff_by_username(engine, gym_id, "trainer")
        assert trainer is not None
        with engine.begin() as conn:
            conn.execute(
                text(
                    "INSERT INTO member_trainer (gym_id, member_id, trainer_id, "
                    "primary_flag) VALUES (:g, :m, :t, 1)"
                ),
                {"g": gym_id, "m": member_id, "t": trainer["id"]},
            )

    return trainer_auth, assign


@pytest.fixture
def member_id(seeded: TestClient, owner_auth: dict[str, str]) -> int:
    """One registered female member, used across Phase 1 tests."""
    res = seeded.post(
        "/api/v1/members",
        headers=owner_auth,
        json={
            "membership_code": "MP-0001",
            "first_name": "Sara",
            "last_name": "Azad",
            "sex": "female",
            "birth_date": "1996-04-11",
            "phone": "09120000000",
        },
    )
    assert res.status_code == 201, res.text
    return int(res.json()["id"])
