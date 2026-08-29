"""Client-app read API (map §5). A MEMBER token is force-scoped to its own
member_id and every row is field-masked (map §2.4, §9). Staff tokens are 403.
"""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.deps import PrincipalDep, get_principal
from app.core.field_mask import mask_assessment_row, mask_member_row, mask_nutrition_row
from app.repo import assessments as assessments_repo
from app.repo import members as members_repo
from app.repo import nutrition as nutrition_repo
from app.repo import programs as programs_repo
from app.state import get_engine

router = APIRouter(prefix="/client", tags=["client"])

MemberPrincipal = Annotated[PrincipalDep, Depends(get_principal)]


def _require_member(principal: MemberPrincipal) -> int:
    """Force-scope: only a MEMBER token with a member_id may use /client."""
    if principal.role != "MEMBER":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="client endpoints are for member tokens only",
        )
    if principal.member_id is None:
        raise HTTPException(status_code=403, detail="member token has no member_id")
    return principal.member_id


@router.get("/me", summary="My profile (clinician notes stripped)")
def me(principal: MemberPrincipal) -> dict:
    mid = _require_member(principal)
    try:
        row = members_repo.get_member(get_engine(), principal.gym_id, mid)
    except members_repo.MemberNotFound as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return mask_member_row(principal.role, row)


@router.get("/me/assessments", summary="My assessment history (masked)")
def my_assessments(principal: MemberPrincipal) -> list[dict]:
    mid = _require_member(principal)
    rows = assessments_repo.history(get_engine(), principal.gym_id, mid)
    return [mask_assessment_row(principal.role, dict(r)) for r in rows]


@router.get("/me/programs", summary="My programs")
def my_programs(principal: MemberPrincipal) -> list[dict]:
    mid = _require_member(principal)
    return programs_repo.list_for_member(get_engine(), principal.gym_id, mid)


@router.get("/me/nutrition", summary="My latest nutrition plan (payload stripped)")
def my_nutrition(principal: MemberPrincipal) -> dict:
    mid = _require_member(principal)
    row = nutrition_repo.latest(get_engine(), principal.gym_id, mid)
    if row is None:
        raise HTTPException(status_code=404, detail="no nutrition plan yet")
    return mask_nutrition_row(principal.role, row)
