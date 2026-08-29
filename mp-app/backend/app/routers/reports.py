"""Dashboard KPIs (map §3 #12). Full numbers are finance-gated (§2.4)."""

from __future__ import annotations

from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends

from app.auth.deps import PrincipalDep, require_finance
from app.repo import attendance as attendance_repo
from app.repo import members as members_repo
from app.repo import payments as payments_repo
from app.state import get_engine

router = APIRouter(prefix="/reports", tags=["reports"])

FinancePrincipal = Annotated[PrincipalDep, Depends(require_finance)]


@router.get("/dashboard", summary="Gym KPIs (finance roles)")
def dashboard(principal: FinancePrincipal) -> dict:
    engine = get_engine()
    today = date.today()
    members = members_repo.list_members(engine, principal.gym_id, limit=100000)
    active = [m for m in members if (m["membership_exp"] or "9999") >= today.isoformat()]

    return {
        "date": today.isoformat(),
        "members_total": len(members),
        "members_active": len(active),
        "members_with_active_injury": sum(1 for m in members if m["active_injuries"] > 0),
        "check_ins_today": attendance_repo.count_today(engine, principal.gym_id, today.isoformat()),
        "revenue_rial_this_month": payments_repo.revenue_in_month(
            engine, principal.gym_id, today.isoformat()[:7]
        ),
    }
