"""Client-app read API (map §5). A MEMBER token is force-scoped to its own
member_id and every row is field-masked (map §2.4, §9). Staff tokens are 403.
"""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.deps import PrincipalDep, get_principal
from app.core.field_mask import (
    mask_assessment_row,
    mask_many,
    mask_member_row,
    mask_nutrition_row,
)
from app.core.security import sign_qr
from app.repo import assessments as assessments_repo
from app.repo import injuries as injuries_repo
from app.repo import members as members_repo
from app.repo import nutrition as nutrition_repo
from app.repo import payments as payments_repo
from app.repo import programs as programs_repo
from app.repo import workouts as workouts_repo
from app.schemas import WorkoutLogCreate
from app.state import get_engine, get_secret_key

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


@router.get("/me/injuries", summary="My recorded injuries and limitations")
def my_injuries(principal: MemberPrincipal) -> list[dict]:
    """The athlete sees their own restrictions — but never the clinician note."""
    mid = _require_member(principal)
    rows = injuries_repo.list_injuries(get_engine(), principal.gym_id, mid)
    return mask_many(principal.role, rows, masker=mask_assessment_row)


@router.get("/me/payments", summary="My payment history (staff attribution hidden)")
def my_payments(principal: MemberPrincipal) -> list[dict]:
    mid = _require_member(principal)
    rows = payments_repo.list_for_member(get_engine(), principal.gym_id, mid)
    return mask_many(principal.role, rows)


@router.get("/me/checkin-qr", summary="Signed short-lived QR to show at the kiosk")
def my_checkin_qr(principal: MemberPrincipal) -> dict:
    """The athlete presents this; the kiosk scans and verifies it (map §8)."""
    mid = _require_member(principal)
    payload = sign_qr(
        gym_id=principal.gym_id, member_id=mid, secret_key=get_secret_key(), ttl_seconds=60
    )
    return {"payload": payload, "expires_in": 60}


@router.get("/me/workouts", summary="My logged training sessions, newest first")
def my_workouts(principal: MemberPrincipal) -> list[dict]:
    mid = _require_member(principal)
    rows = workouts_repo.list_for_member(get_engine(), principal.gym_id, mid)
    out = []
    for row in rows:
        raw = row.pop("payload")
        row["exercises"] = workouts_repo.decode_session(str(raw))
        out.append(row)
    return out


@router.post("/me/workouts", status_code=201, summary="Log one of my sessions")
def log_workout(principal: MemberPrincipal, body: WorkoutLogCreate) -> dict:
    """Write-only to the athlete's own log; nothing here is staff-authored."""
    mid = _require_member(principal)
    exercises = [e.model_dump(exclude_none=True) for e in body.exercises]
    payload = workouts_repo.encode_session(exercises)
    log_id = workouts_repo.add_log(
        get_engine(),
        principal.gym_id,
        mid,
        session_date=body.session_date,
        payload=payload,
        program_id=body.program_id,
        athlete_note=body.athlete_note,
    )
    return {
        "id": log_id,
        "session_date": body.session_date,
        "exercises": exercises,
        "athlete_note": body.athlete_note,
    }
