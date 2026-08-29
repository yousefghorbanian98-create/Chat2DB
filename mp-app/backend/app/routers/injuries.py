"""Injury & limitation dossier (map §7). Hard filters live here."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.deps import PrincipalDep, require_clinician
from app.auth.scope import ensure_member_visible
from app.core.security import Principal
from app.repo import injuries as injuries_repo
from app.repo import members as members_repo
from app.schemas import InjuryCreate, InjuryOut, InjuryPublicOut
from app.state import get_engine

router = APIRouter(tags=["injuries"])

ClinicianPrincipal = Annotated[PrincipalDep, Depends(require_clinician)]


def _require_member(principal: Principal, member_id: int) -> None:
    """Existence check + per-role scope (trainer sees only assigned)."""
    ensure_member_visible(principal, member_id)
    gym_id = principal.gym_id
    try:
        members_repo.get_member(get_engine(), gym_id, member_id)
    except members_repo.MemberNotFound as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get(
    "/members/{member_id}/injuries",
    response_model=list[InjuryOut],
    summary="Full dossier (Studio — includes clinician note)",
)
def list_injuries(member_id: int, principal: ClinicianPrincipal) -> list[InjuryOut]:
    _require_member(principal, member_id)
    rows = injuries_repo.list_injuries(get_engine(), principal.gym_id, member_id)
    return [InjuryOut(**row) for row in rows]


@router.get(
    "/client/members/{member_id}/injuries",
    response_model=list[InjuryPublicOut],
    summary="Member-visible notes only (field-masked)",
)
def list_public_injuries(
    member_id: int, principal: ClinicianPrincipal
) -> list[InjuryPublicOut]:
    """Same rows, narrower schema — the clinician note never crosses this line."""
    _require_member(principal, member_id)
    rows = injuries_repo.list_injuries(get_engine(), principal.gym_id, member_id)
    return [
        InjuryPublicOut(
            id=row["id"],
            body_region=row["body_region"],
            label=row["label"],
            status=row["status"],
            member_visible_note=row["member_visible_note"],
        )
        for row in rows
    ]


@router.post(
    "/members/{member_id}/injuries",
    response_model=InjuryOut,
    status_code=status.HTTP_201_CREATED,
    summary="Record an injury + contraindications",
)
def create_injury(
    member_id: int, body: InjuryCreate, principal: ClinicianPrincipal
) -> InjuryOut:
    engine = get_engine()
    _require_member(principal, member_id)
    injury_id = injuries_repo.create_injury(
        engine, principal.gym_id, member_id, body.model_dump()
    )
    rows = injuries_repo.list_injuries(engine, principal.gym_id, member_id)
    match = next((r for r in rows if r["id"] == injury_id), None)
    if match is None:  # pragma: no cover - insert just succeeded
        raise HTTPException(status_code=500, detail="injury row vanished after insert")
    return InjuryOut(**match)


@router.delete(
    "/members/{member_id}/injuries/{injury_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Tombstone an injury record",
)
def delete_injury(
    member_id: int, injury_id: int, principal: ClinicianPrincipal
) -> None:
    _require_member(principal, member_id)
    try:
        injuries_repo.soft_delete_injury(get_engine(), principal.gym_id, injury_id)
    except injuries_repo.InjuryNotFound as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get(
    "/members/{member_id}/filters",
    summary="Blocked patterns + allowed modifications for the program builder",
)
def member_filters(member_id: int, principal: ClinicianPrincipal) -> dict[str, list[str]]:
    """The exact input Phase 3's contraindication graph consumes."""
    _require_member(principal, member_id)
    return injuries_repo.list_patterns(get_engine(), principal.gym_id, member_id)
