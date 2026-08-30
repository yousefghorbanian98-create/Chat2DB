"""Packages, payments, receipts (map §3 #11). Finance-gated per §2.4."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from pydantic import BaseModel, ConfigDict, Field

from app.auth.deps import PrincipalDep, require_finance, require_roles
from app.core.receipt_pdf import build_receipt_pdf
from app.repo import members as members_repo
from app.repo import payments as payments_repo
from app.automation import events
from app.state import get_engine, get_gym_name

router = APIRouter(tags=["payments"])

# RECEPTION enters cash payments + prints receipts; OWNER/ADMIN full finance.
CashierPrincipal = Annotated[
    PrincipalDep, Depends(require_roles("OWNER", "ADMIN", "RECEPTION"))
]
FinancePrincipal = Annotated[PrincipalDep, Depends(require_finance)]


class PackageCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=1, max_length=80)
    duration_days: int = Field(ge=1, le=3650)
    price_rial: int = Field(ge=0)


class PaymentCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    member_id: int
    amount_rial: int = Field(ge=0)
    method: str = Field(default="cash", pattern="^(cash|card|transfer|pos)$")
    package_id: int | None = None


@router.get("/packages", summary="Active membership packages")
def list_packages(principal: CashierPrincipal) -> list[dict]:
    return payments_repo.list_packages(get_engine(), principal.gym_id)


@router.post(
    "/packages",
    status_code=status.HTTP_201_CREATED,
    summary="Define a package (finance only)",
)
def create_package(body: PackageCreate, principal: FinancePrincipal) -> dict:
    pid = payments_repo.create_package(
        get_engine(),
        principal.gym_id,
        name=body.name,
        duration_days=body.duration_days,
        price_rial=body.price_rial,
    )
    return {"id": pid, **body.model_dump()}


@router.post(
    "/payments",
    status_code=status.HTTP_201_CREATED,
    summary="Record a payment (cash entry at the desk)",
)
def create_payment(body: PaymentCreate, principal: CashierPrincipal) -> dict:
    engine = get_engine()
    try:
        members_repo.get_member(engine, principal.gym_id, body.member_id)
    except members_repo.MemberNotFound as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    row = payments_repo.create_payment(
        engine,
        principal.gym_id,
        member_id=body.member_id,
        amount_rial=body.amount_rial,
        method=body.method,
        package_id=body.package_id,
    )
    # Optional n8n bridge (best-effort, redacted): receipt delivery downstream.
    events.emit(
        "payment.created",
        principal.gym_id,
        {
            "member_id": row["member_id"],
            "amount_rial": row["amount_rial"],
            "method": row["method"],
            "receipt_no": row["receipt_no"],
        },
    )
    return row


@router.get("/payments/{payment_id}/receipt", summary="Receipt PDF")
def receipt(payment_id: int, principal: CashierPrincipal) -> Response:
    engine = get_engine()
    try:
        payment = payments_repo.get_payment(engine, principal.gym_id, payment_id)
    except payments_repo.PaymentNotFound as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    member = members_repo.get_member(engine, principal.gym_id, payment["member_id"])
    packages = {p["id"]: p["name"] for p in payments_repo.list_packages(engine, principal.gym_id)}
    pdf = build_receipt_pdf(
        gym_name=get_gym_name(),
        payment=payment,
        member=member,
        package_name=packages.get(payment["package_id"]),
    )
    return Response(
        content=pdf,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{payment["receipt_no"]}.pdf"'},
    )


@router.post("/payments/{payment_id}/void", summary="Void (finance only, audited)")
def void(payment_id: int, principal: FinancePrincipal) -> dict:
    try:
        payments_repo.void_payment(get_engine(), principal.gym_id, payment_id)
    except payments_repo.PaymentNotFound as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    return {"voided": True}
