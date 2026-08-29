"""Exercise library endpoints (map §3 #6)."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends

from app.auth.deps import PrincipalDep, require_member_read
from app.repo import exercises as exercises_repo
from app.state import get_engine

router = APIRouter(prefix="/exercises", tags=["exercises"])

# The library is reference data for planning; KIOSK (scan-only) has no need of it.
StaffPrincipal = Annotated[PrincipalDep, Depends(require_member_read)]


@router.get("", summary="Exercise library (seeded)")
def list_all(principal: StaffPrincipal) -> list[dict]:
    return exercises_repo.list_exercises(get_engine(), principal.gym_id)


@router.get("/{exercise_key}/contraindications", summary="Contraindications for one exercise")
def contraindications(exercise_key: str, principal: StaffPrincipal) -> list[dict]:
    return exercises_repo.contraindications_for(get_engine(), principal.gym_id, exercise_key)
