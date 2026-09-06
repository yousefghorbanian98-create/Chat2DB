"""Attendance: signed-QR check-in/out (map §3 #10, DoD #5)."""

from __future__ import annotations

from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict

from app.auth.deps import PrincipalDep, require_roles
from app.core.security import QrError, verify_qr
from app.repo import attendance as attendance_repo
from app.repo import members as members_repo
from app.state import get_engine, get_secret_key

router = APIRouter(prefix="/attendance", tags=["attendance"])

# Check-in is run by RECEPTION and KIOSK (scan), plus OWNER/ADMIN.
CheckinPrincipal = Annotated[
    PrincipalDep, Depends(require_roles("OWNER", "ADMIN", "RECEPTION", "KIOSK"))
]


class QrCheckin(BaseModel):
    model_config = ConfigDict(extra="forbid")

    payload: dict
    method: str = "qr"


class ManualCheckin(BaseModel):
    model_config = ConfigDict(extra="forbid")

    member_id: int
    method: str = "manual"


def _deny_expired_membership(member: dict) -> None:
    """DoD #5: an expired membership must be denied at the door."""
    exp = member.get("membership_exp")
    if exp and exp < date.today().isoformat():
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="membership expired — renew at the front desk",
        )


@router.post(
    "/check-in",
    status_code=status.HTTP_201_CREATED,
    summary="Check in via signed QR or manual entry",
)
def check_in(body: QrCheckin | ManualCheckin, principal: CheckinPrincipal) -> dict:
    engine = get_engine()

    if isinstance(body, QrCheckin):
        try:
            core = verify_qr(body.payload, secret_key=get_secret_key())
        except QrError as exc:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(exc)) from exc
        member_id = int(core["mid"])
        method = "qr"
        qr_sig = str(body.payload.get("sig") or "")
    else:
        member_id = body.member_id
        method = body.method
        qr_sig = None

    if principal.gym_id != getattr(principal, "gym_id"):  # unreachable; keeps symmetry
        raise HTTPException(status_code=403, detail="cross-gym")

    try:
        member = members_repo.get_member(engine, principal.gym_id, member_id)
    except members_repo.MemberNotFound as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    _deny_expired_membership(member)

    if attendance_repo.open_visit(engine, principal.gym_id, member_id) is not None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="member is already checked in"
        )

    attendance_id = attendance_repo.check_in(
        engine, principal.gym_id, member_id, method=method, qr_sig=qr_sig
    )
    return {"id": attendance_id, "member_id": member_id, "method": method}


@router.post(
    "/check-out/{member_id}",
    summary="Close the member's open visit",
)
def check_out(member_id: int, principal: CheckinPrincipal) -> dict:
    engine = get_engine()
    visit = attendance_repo.open_visit(engine, principal.gym_id, member_id)
    if visit is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="no open visit")
    return attendance_repo.check_out(engine, principal.gym_id, visit["id"])


@router.get("/today", summary="Today's check-in count (ops KPI)")
def today_count(principal: CheckinPrincipal) -> dict:
    engine = get_engine()
    prefix = date.today().isoformat()
    return {"date": prefix, "check_ins": attendance_repo.count_today(engine, principal.gym_id, prefix)}
