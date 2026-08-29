"""Packages + payments data access (map §3 #11). Money is integer rials."""

from __future__ import annotations

from typing import Any

from sqlalchemy import text
from sqlalchemy.engine import Engine

_PKG_COLS = "id, name, duration_days, price_rial, active, created_at"
_PAY_COLS = (
    "id, member_id, package_id, amount_rial, method, receipt_no, voided, "
    "staff_id, created_at"
)


class PaymentNotFound(LookupError):
    """No live payment with that id."""


def list_packages(engine: Engine, gym_id: int) -> list[dict[str, Any]]:
    with engine.connect() as conn:
        rows = conn.execute(
            text(
                f"SELECT {_PKG_COLS} FROM packages "
                "WHERE gym_id = :g AND active = 1 AND deleted_at IS NULL "
                "ORDER BY price_rial"
            ),
            {"g": gym_id},
        ).mappings().all()
    return [dict(r) for r in rows]


def create_package(
    engine: Engine, gym_id: int, *, name: str, duration_days: int, price_rial: int
) -> int:
    with engine.begin() as conn:
        cur = conn.execute(
            text(
                "INSERT INTO packages (gym_id, name, duration_days, price_rial) "
                "VALUES (:g, :n, :d, :p)"
            ),
            {"g": gym_id, "n": name, "d": duration_days, "p": price_rial},
        )
        return int(cur.lastrowid or 0)


def next_receipt_no(engine: Engine, gym_id: int) -> str:
    """Monotonic, gym-scoped receipt number (zero-padded)."""
    with engine.connect() as conn:
        count = int(
            conn.execute(
                text("SELECT count(*) FROM payments WHERE gym_id = :g"), {"g": gym_id}
            ).scalar()
            or 0
        )
    return f"R-{gym_id}-{count + 1:06d}"


def create_payment(
    engine: Engine,
    gym_id: int,
    *,
    member_id: int,
    amount_rial: int,
    method: str = "cash",
    package_id: int | None = None,
    staff_id: int | None = None,
) -> dict[str, Any]:
    with engine.begin() as conn:
        receipt_no = None
        cur = conn.execute(
            text(
                "INSERT INTO payments (gym_id, member_id, package_id, amount_rial, "
                "method, staff_id, receipt_no) "
                "VALUES (:g, :m, :p, :a, :method, :staff, :r)"
            ),
            {
                "g": gym_id,
                "m": member_id,
                "p": package_id,
                "a": amount_rial,
                "method": method,
                "staff": staff_id,
                "r": next_receipt_no(engine, gym_id),
            },
        )
        payment_id = int(cur.lastrowid or 0)
        row = conn.execute(
            text(f"SELECT {_PAY_COLS} FROM payments WHERE id = :i"), {"i": payment_id}
        ).mappings().one()
    return dict(row)


def get_payment(engine: Engine, gym_id: int, payment_id: int) -> dict[str, Any]:
    with engine.connect() as conn:
        row = conn.execute(
            text(
                f"SELECT {_PAY_COLS} FROM payments "
                "WHERE id = :i AND gym_id = :g AND deleted_at IS NULL"
            ),
            {"i": payment_id, "g": gym_id},
        ).mappings().first()
    if row is None:
        raise PaymentNotFound(f"payment {payment_id} not found")
    return dict(row)


def void_payment(engine: Engine, gym_id: int, payment_id: int) -> None:
    """Void (never hard-delete) — audit trail per map §15."""
    with engine.begin() as conn:
        cur = conn.execute(
            text(
                "UPDATE payments SET voided = 1, rev = rev + 1 "
                "WHERE id = :i AND gym_id = :g AND deleted_at IS NULL"
            ),
            {"i": payment_id, "g": gym_id},
        )
        if cur.rowcount == 0:
            raise PaymentNotFound(f"payment {payment_id} not found")


def revenue_in_month(engine: Engine, gym_id: int, month_prefix: str) -> int:
    """Sum of non-voided payments whose created_at starts with YYYY-MM."""
    with engine.connect() as conn:
        return int(
            conn.execute(
                text(
                    "SELECT coalesce(sum(amount_rial), 0) FROM payments "
                    "WHERE gym_id = :g AND voided = 0 AND created_at LIKE :p "
                    "AND deleted_at IS NULL"
                ),
                {"g": gym_id, "p": f"{month_prefix}%"},
            ).scalar()
            or 0
        )

def has_payment(engine: Engine, gym_id: int, member_id: int) -> bool:
    """True when this member already has a (non-voided-or-not) payment row."""
    with engine.connect() as conn:
        row = conn.execute(
            text(
                "SELECT 1 FROM payments WHERE gym_id = :g AND member_id = :m "
                "AND deleted_at IS NULL LIMIT 1"
            ),
            {"g": gym_id, "m": member_id},
        ).first()
    return row is not None
