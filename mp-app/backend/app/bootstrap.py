"""First-run bootstrap: create the gym and its OWNER account.

Usage:
    MP_OWNER_USER=owner MP_OWNER_PIN=1234 python -m app.bootstrap

The PIN is read from the environment (never a CLI flag, so it stays out of
shell history and process listings).
"""

from __future__ import annotations

import os
import sys

from app.config import Settings
from app.db import make_engine
from app.migrations import migrate
from app.repo import staff as staff_repo


def main() -> int:
    """Seed the local gym + owner. Returns a process exit code."""
    username = os.environ.get("MP_OWNER_USER", "owner")
    pin = os.environ.get("MP_OWNER_PIN", "")
    if not pin:
        print("MP_OWNER_PIN must be set (non-empty)", file=sys.stderr)
        return 2

    settings = Settings.from_env()
    engine = make_engine(settings.db_path)
    migrate(engine)

    gym_id = staff_repo.ensure_gym(engine, settings.gym_name)
    existing = staff_repo.find_staff_by_username(engine, gym_id, username)
    if existing is not None:
        print(f"gym={gym_id} owner '{username}' already exists — nothing to do")
        return 0

    staff_id = staff_repo.create_staff(
        engine, gym_id=gym_id, username=username, role="OWNER", pin=pin,
        full_name=os.environ.get("MP_OWNER_NAME"),
    )
    print(f"gym={gym_id} owner='{username}' staff_id={staff_id} db={settings.db_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
