"""Members CRUD + signed QR identity (map §9 Studio surface)."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.auth.deps import PrincipalDep, require_member_read, require_member_write
from app.auth.scope import ensure_member_visible, scope_trainer_id
from app.core.security import hash_secret, sign_qr
from app.repo import members as members_repo
from app.schemas import MemberCreate, MemberOut, MemberUpdate, SetMemberPin
from app.state import get_engine, get_secret_key

router = APIRouter(prefix="/members", tags=["members"])

ReaderPrincipal = Annotated[PrincipalDep, Depends(require_member_read)]
WriterPrincipal = Annotated[PrincipalDep, Depends(require_member_write)]


@router.get("", response_model=list[MemberOut], summary="List visible members")
def list_members(principal: ReaderPrincipal) -> list[MemberOut]:
    """OWNER/ADMIN/RECEPTION see everyone; TRAINER only assigned members."""
    rows = members_repo.list_members(
        get_engine(), principal.gym_id, trainer_id=scope_trainer_id(principal)
    )
    return [MemberOut(**row) for row in rows]


@router.post(
    "",
    response_model=MemberOut,
    status_code=status.HTTP_201_CREATED,
    summary="Register a member",
)
def create_member(body: MemberCreate, principal: WriterPrincipal) -> MemberOut:
    member_id = members_repo.create_member(
        get_engine(), principal.gym_id, body.model_dump()
    )
    return MemberOut(**members_repo.get_member(get_engine(), principal.gym_id, member_id))


@router.get("/{member_id}", response_model=MemberOut, summary="One member")
def get_member(member_id: int, principal: ReaderPrincipal) -> MemberOut:
    ensure_member_visible(principal, member_id)
    try:
        return MemberOut(**members_repo.get_member(get_engine(), principal.gym_id, member_id))
    except members_repo.MemberNotFound as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.patch("/{member_id}", response_model=MemberOut, summary="Update a member")
def update_member(
    member_id: int, body: MemberUpdate, principal: WriterPrincipal
) -> MemberOut:
    patch = body.model_dump(exclude_unset=True)
    try:
        return MemberOut(
            **members_repo.update_member(get_engine(), principal.gym_id, member_id, patch)
        )
    except members_repo.MemberNotFound as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.post("/{member_id}/pin", status_code=204, summary="Set member PIN (front desk)")
def set_member_pin(
    member_id: int, body: SetMemberPin, principal: WriterPrincipal
) -> None:
    """Store a PBKDF2 hash of the member's PIN so they can use the client app.

    Only the hash is written; the plaintext never touches disk (C11).
    """
    ensure_member_visible(principal, member_id)
    members_repo.update_member(
        get_engine(), principal.gym_id, member_id, {"pin_hash": hash_secret(body.pin)}
    )


@router.delete(
    "/{member_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Soft-delete (tombstone) a member",
)
def delete_member(member_id: int, principal: WriterPrincipal) -> None:
    try:
        members_repo.soft_delete_member(get_engine(), principal.gym_id, member_id)
    except members_repo.MemberNotFound as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc


@router.get("/{member_id}/qr", summary="Signed short-lived check-in QR payload")
def member_qr(member_id: int, principal: ReaderPrincipal) -> dict[str, object]:
    """QR payload per map §8: ``{v, typ, gym, mid, exp, sig}`` HMAC-signed."""
    ensure_member_visible(principal, member_id)
    try:
        members_repo.get_member(get_engine(), principal.gym_id, member_id)
    except members_repo.MemberNotFound as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    payload = sign_qr(
        gym_id=principal.gym_id,
        member_id=member_id,
        secret_key=get_secret_key(),
        ttl_seconds=60,
    )
    return {"payload": payload, "expires_in": 60}
