"""Auth: PIN login, token issue, /me (map §9)."""

from __future__ import annotations

from fastapi import APIRouter, HTTPException, status

from app.auth.deps import PrincipalDep
from app.core.security import (
    Principal,
    issue_token,
    verify_secret,
)
from app.repo import staff as staff_repo
from app.schemas import PinLogin, TokenResponse
from app.state import get_engine, get_secret_key

router = APIRouter(prefix="/auth", tags=["auth"])

TOKEN_TTL_SECONDS = 8 * 3600


@router.post("/pin", response_model=TokenResponse, summary="Staff PIN login")
def login_with_pin(body: PinLogin) -> TokenResponse:
    """Exchange a staff username + PIN for a machine-local session token.

    Raises:
        HTTPException 401: unknown user, inactive user, or wrong PIN. The
        message is deliberately identical for all three (no user enumeration).
    """
    engine = get_engine()
    gym_id = staff_repo.ensure_gym(engine)
    row = staff_repo.find_staff_by_username(engine, gym_id, body.username)

    if row is None or not verify_secret(body.pin, row.get("pin_hash") or ""):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid credentials"
        )

    principal = Principal(
        subject=str(row["username"]), role=str(row["role"]), gym_id=gym_id
    )
    return TokenResponse(
        token=issue_token(principal, secret_key=get_secret_key(), ttl_seconds=TOKEN_TTL_SECONDS),
        role=principal.role,
        gym_id=principal.gym_id,
        expires_in=TOKEN_TTL_SECONDS,
    )


@router.get("/me", summary="Current principal")
def me(principal: PrincipalDep) -> dict[str, object]:
    """Echo the verified identity — the shell renders role-appropriate UI."""
    return {
        "subject": principal.subject,
        "role": principal.role,
        "gym_id": principal.gym_id,
        "member_id": principal.member_id,
        "shell": "client" if principal.role == "MEMBER" else "studio",
    }
