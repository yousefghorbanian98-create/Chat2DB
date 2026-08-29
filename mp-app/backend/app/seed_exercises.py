"""CLI: seed the exercise library for the local gym.

Usage:
    python -m app.seed_exercises            # seed into MP_DB_PATH
"""

from __future__ import annotations

from app.config import Settings
from app.db import make_engine
from app.migrations import migrate
from app.repo import exercises as exercises_repo
from app.repo import staff as staff_repo


def main() -> int:
    settings = Settings.from_env()
    engine = make_engine(settings.db_path)
    migrate(engine)
    gym_id = staff_repo.ensure_gym(engine, settings.gym_name)
    inserted = exercises_repo.seed_exercises(engine, gym_id)
    total = len(exercises_repo.list_exercises(engine, gym_id))
    print(f"gym={gym_id} inserted={inserted} total_exercises={total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
