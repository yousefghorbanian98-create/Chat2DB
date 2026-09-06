"""Equipment inventory (map §3 #5)."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field

from app.auth.deps import PrincipalDep, require_roles, require_staff
from app.repo import equipment as equipment_repo
from app.state import get_engine

router = APIRouter(prefix="/equipment", tags=["equipment"])

ManagePrincipal = Annotated[PrincipalDep, Depends(require_roles("OWNER", "ADMIN"))]
StaffPrincipal = Annotated[PrincipalDep, Depends(require_staff)]


class EquipmentCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, max_length=120)
    category: str | None = None
    count: int = Field(default=1, ge=1)


class AvailabilityUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    available: bool


@router.get("", summary="All equipment")
def list_all(principal: StaffPrincipal) -> list[dict]:
    return equipment_repo.list_equipment(get_engine(), principal.gym_id)


@router.post("", status_code=status.HTTP_201_CREATED, summary="Add equipment")
def create(body: EquipmentCreate, principal: ManagePrincipal) -> dict:
    pid = equipment_repo.create_equipment(
        get_engine(),
        principal.gym_id,
        name=body.name,
        category=body.category,
        count=body.count,
    )
    return {"id": pid, **body.model_dump()}


@router.patch("/{equipment_id}", summary="Toggle availability")
def set_availability(
    equipment_id: int, body: AvailabilityUpdate, principal: ManagePrincipal
) -> dict:
    try:
        equipment_repo.set_availability(
            get_engine(), principal.gym_id, equipment_id, body.available
        )
    except equipment_repo.EquipmentNotFound as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"id": equipment_id, "available": body.available}
