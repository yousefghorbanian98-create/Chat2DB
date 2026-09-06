"""Nutrition endpoint — deterministic from the member's latest LBM (map §9)."""

from __future__ import annotations

import json
from typing import Annotated, Literal

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field

from app.auth.deps import PrincipalDep, require_assessor
from app.auth.scope import ensure_member_visible
from app.core.nutrition import NutritionError, plan_nutrition
from app.repo import assessments as assessments_repo
from app.repo import members as members_repo
from app.repo import nutrition as nutrition_repo
from app.state import get_engine

router = APIRouter(prefix="/nutrition", tags=["nutrition"])

AssessorPrincipal = Annotated[PrincipalDep, Depends(require_assessor)]


class NutritionRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    activity: Literal["sedentary", "light", "moderate", "active", "athlete"] = "moderate"
    goal: Literal["cut", "maintain", "bulk"] = "maintain"
    protein_g_per_kg: float = Field(default=1.8, gt=0, le=4)


@router.post(
    "/members/{member_id}/plan",
    status_code=status.HTTP_201_CREATED,
    summary="Compute + store a nutrition plan from the latest assessment LBM",
)
def create_plan(member_id: int, body: NutritionRequest, principal: AssessorPrincipal) -> dict:
    engine = get_engine()
    ensure_member_visible(principal, member_id)
    try:
        members_repo.get_member(engine, principal.gym_id, member_id)
    except members_repo.MemberNotFound as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    history = assessments_repo.history(engine, principal.gym_id, member_id, limit=1)
    if not history or history[0]["lean_mass_kg"] is None:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="no assessment with lean mass — run a JP7 assessment first",
        )

    lbm = float(history[0]["lean_mass_kg"])
    try:
        plan = plan_nutrition(
            lean_mass_kg=lbm,
            activity=body.activity,
            goal=body.goal,
            protein_g_per_kg=body.protein_g_per_kg,
        )
    except NutritionError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    payload = json.dumps({"schema": "mp.nutrition/v1", "lean_mass_kg": lbm,
                          "goal": body.goal, "activity": body.activity},
                         separators=(",", ":"))
    nutrition_repo.save_plan(engine, principal.gym_id, member_id, plan, payload)
    return {
        "member_id": member_id,
        "lean_mass_kg": lbm,
        **{
            "bmr_kcal": plan.bmr_kcal,
            "tdee_kcal": plan.tdee_kcal,
            "target_kcal": plan.target_kcal,
            "protein_g": plan.protein_g,
            "carbs_g": plan.carbs_g,
            "fat_g": plan.fat_g,
        },
    }


@router.get("/members/{member_id}/plan", summary="Latest stored nutrition plan")
def get_plan(member_id: int, principal: AssessorPrincipal) -> dict:
    ensure_member_visible(principal, member_id)
    row = nutrition_repo.latest(get_engine(), principal.gym_id, member_id)
    if row is None:
        raise HTTPException(status_code=404, detail="no nutrition plan yet")
    return row
