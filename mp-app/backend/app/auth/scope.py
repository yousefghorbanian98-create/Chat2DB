"""Per-role member scoping (map §2.4: TRAINER sees only assigned members).

Centralised so no router can forget it. Unassigned access returns *not found*,
not *forbidden* — a trainer must not learn that an unassigned member exists.
"""

from __future__ import annotations

from fastapi import HTTPException, status

from app.core.security import Principal
from app.repo import staff as staff_repo
from app.state import get_engine

#: Roles that see every member in the gym.
FULL_SCOPE_ROLES = frozenset({"OWNER", "ADMIN", "RECEPTION"})


def staff_id_for(principal: Principal) -> int | None:
    """Resolve the staff row behind a principal (None for MEMBER tokens)."""
    if principal.role == "MEMBER":
        return None
    row = staff_repo.find_staff_by_username(get_engine(), principal.gym_id, principal.subject)
    return int(row["id"]) if row else None


def scope_trainer_id(principal: Principal) -> int | None:
    """Trainer id used to filter member lists, or None for full-scope roles."""
    if principal.role in FULL_SCOPE_ROLES:
        return None
    if principal.role == "TRAINER":
        return staff_id_for(principal)
    return None  # KIOSK/MEMBER never reach member routes (RBAC blocks them)


def ensure_member_visible(principal: Principal, member_id: int) -> None:
    """Raise 404 when this principal may not see ``member_id``.

    404 (not 403) on purpose: existence of unassigned members is not the
    trainer's business.
    """
    trainer_id = scope_trainer_id(principal)
    if trainer_id is None:
        return
    if not staff_repo.staff_can_see_member(
        get_engine(), staff_id=trainer_id, member_id=member_id
    ):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"member {member_id} not found",
        )
