"""CLI: seed a small, coherent Persian demo dataset for the local gym.

Usage:
    python -m app.seed_demo            # seed into MP_DB_PATH

Idempotent: every row is looked up by a stable code before insertion, so the
command can run any number of times without duplicating the demo. Numbers are
derived by the deterministic JP7 core (rule C4) — never invented here.
"""

from __future__ import annotations

from sqlalchemy.engine import Engine

from app.core.jp7 import assess
from app.repo import assessments as assessments_repo
from app.repo import attendance as attendance_repo
from app.repo import members as members_repo
from app.repo import payments as payments_repo
from app.repo import staff as staff_repo

DEMO_CODE = "MP-DEMO-1"
DEMO_PIN = "1234"

#: 7 caliper sites summing to 60 mm (matches the backend golden fixture).
_SITES = {"chest": 10, "midaxillary": 10, "triceps": 10, "subscapular": 10,
          "abdominal": 10, "suprailiac": 5, "thigh": 5}


def _ensure_member(engine: Engine, gym_id: int, staff_id: int | None) -> int:
    """Create the demo athlete once; return the (existing or new) id."""
    existing = members_repo.find_member_by_code(engine, gym_id, DEMO_CODE)
    if existing is not None:
        return int(existing["id"])

    member_id = members_repo.create_member(
        engine,
        gym_id,
        {
            "membership_code": DEMO_CODE,
            "first_name": "نسیم",
            "last_name": "رحیمی",
            "sex": "female",
            "birth_date": "2001-03-21",
            "phone": "09120000001",
            "membership_exp": None,
            "guardian_consent": False,
        },
    )
    # A member PIN so the client shell demo can log in immediately.
    from app.core.security import hash_secret

    members_repo.update_member(
        engine, gym_id, member_id, {"pin_hash": hash_secret(DEMO_PIN)}
    )
    return member_id


def seed_demo(engine: Engine, gym_id: int) -> dict[str, int]:
    """Populate the demo member with an assessment, a payment and a check-in.

    Returns a count dict for the CLI to print (and for tests to assert).
    """
    owner = staff_repo.find_staff_by_username(engine, gym_id, "owner")
    staff_id = int(owner["id"]) if owner else None

    member_id = _ensure_member(engine, gym_id, staff_id)
    counts = {"member": member_id, "assessment": 0, "payment": 0, "checkin": 0}

    if not assessments_repo.history(engine, gym_id, member_id):
        result = assess(sex="female", age_years=25, sites_mm=_SITES, weight_kg=58.0)
        counts["assessment"] = assessments_repo.save_assessment(
            engine, gym_id=gym_id, member_id=member_id, result=result,
            weight_kg=58.0, height_cm=165.0, staff_id=staff_id,
        )

    if not payments_repo.list_packages(engine, gym_id):
        pkg = payments_repo.create_package(
            engine, gym_id, name="ماهانه", duration_days=30, price_rial=1_500_000
        )
    else:
        pkg = payments_repo.list_packages(engine, gym_id)[0]["id"]

    if not payments_repo.has_payment(engine, gym_id, member_id):
        payment = payments_repo.create_payment(
            engine, gym_id, member_id=member_id, amount_rial=1_500_000,
            method="cash", package_id=pkg, staff_id=staff_id,
        )
        counts["payment"] = int(payment["id"])

    if attendance_repo.open_visit(engine, gym_id, member_id) is None:
        counts["checkin"] = attendance_repo.check_in(
            engine, gym_id, member_id, method="manual", staff_id=staff_id
        )
    return counts


def main() -> int:
    from app.config import Settings
    from app.db import make_engine
    from app.migrations import migrate

    settings = Settings.from_env()
    engine = make_engine(settings.db_path)
    migrate(engine)
    gym_id = staff_repo.ensure_gym(engine, settings.gym_name)
    counts = seed_demo(engine, gym_id)
    print(f"gym={gym_id} member={counts['member']} pin={DEMO_PIN} counts={counts}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
