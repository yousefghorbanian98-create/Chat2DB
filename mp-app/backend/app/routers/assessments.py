"""JP7 assessments: compute, persist, history (map §6, §9)."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.deps import PrincipalDep, require_assessor
from app.auth.scope import ensure_member_visible
from app.core.security import Principal
from app.core.jp7 import Jp7Error, assess
from app.repo import assessments as assessments_repo
from app.repo import members as members_repo
from app.schemas import AssessmentCreate, AssessmentOut
from app.state import get_engine

router = APIRouter(tags=["assessments"])

AssessorPrincipal = Annotated[PrincipalDep, Depends(require_assessor)]


def _require_member(principal: Principal, member_id: int) -> None:
    """Existence check + per-role scope (trainer sees only assigned)."""
    ensure_member_visible(principal, member_id)
    gym_id = principal.gym_id
    try:
        members_repo.get_member(get_engine(), gym_id, member_id)
    except members_repo.MemberNotFound as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post(
    "/members/{member_id}/assessments",
    response_model=AssessmentOut,
    status_code=status.HTTP_201_CREATED,
    summary="Compute + store a JP7 assessment",
)
def create_assessment(
    member_id: int, body: AssessmentCreate, principal: AssessorPrincipal
) -> AssessmentOut:
    """Deterministic JP7 — rule C6: no LLM is involved in these numbers."""
    engine = get_engine()
    _require_member(principal, member_id)

    try:
        result = assess(
            sex=_member_sex(engine, principal.gym_id, member_id),
            age_years=body.age_years,
            sites_mm=body.sites_mm.model_dump(),
            weight_kg=body.weight_kg,
            equation=body.equation,
        )
    except Jp7Error as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc

    assessment_id = assessments_repo.save_assessment(
        engine,
        gym_id=principal.gym_id,
        member_id=member_id,
        result=result,
        weight_kg=body.weight_kg,
        height_cm=body.height_cm,
        staff_id=None,
    )
    return AssessmentOut(
        **assessments_repo.get_assessment(engine, principal.gym_id, assessment_id)
    )


@router.get(
    "/members/{member_id}/assessments",
    response_model=list[AssessmentOut],
    summary="Assessment history (newest first)",
)
def list_assessments(
    member_id: int, principal: AssessorPrincipal
) -> list[AssessmentOut]:
    _require_member(principal, member_id)
    rows = assessments_repo.history(get_engine(), principal.gym_id, member_id)
    return [AssessmentOut(**row) for row in rows]


@router.post(
    "/assessments/calculate",
    summary="Pure JP7 calculation (no persistence)",
)
def calculate(body: AssessmentCreate) -> dict[str, object]:
    """Stateless math endpoint — used by the assessment form's live preview."""
    try:
        result = assess(
            sex="male",  # caller supplies sex via the member record when persisting
            age_years=body.age_years,
            sites_mm=body.sites_mm.model_dump(),
            weight_kg=body.weight_kg,
            equation=body.equation,
        )
    except Jp7Error as exc:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc

    return {
        "protocol": result.protocol,
        "equation": result.equation,
        "sum_mm": result.sum_mm,
        "body_density": result.body_density,
        "body_fat_pct": result.body_fat_pct,
        "fat_mass_kg": result.fat_mass_kg,
        "lean_mass_kg": result.lean_mass_kg,
        "classification": result.classification,
        "disclaimer": "Population equation estimate; not a medical diagnosis.",
    }


def _member_sex(engine, gym_id: int, member_id: int) -> str:
    """Sex is read from the member record, never trusted from the request."""
    return str(members_repo.get_member(engine, gym_id, member_id)["sex"])
