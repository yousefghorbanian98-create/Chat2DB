"""FastAPI dependencies for auth and role checks.

Map §9: a MEMBER token is force-scoped to its own member_id, and field masking
strips clinician notes and other members' rows. That enforcement lives here so
no router can forget it.
"""

from __future__ import annotations

from typing import Annotated

from fastapi import Depends, Header, HTTPException, status

from app.core.security import Principal, TokenError, verify_token
from app.state import get_secret_key

STUDIO_ROLES = frozenset({"OWNER", "ADMIN", "TRAINER", "RECEPTION", "KIOSK"})
MEMBER_ROLE = "MEMBER"


def get_principal(authorization: Annotated[str | None, Header()] = None) -> Principal:
    """Decode ``Authorization: Bearer <token>`` into a Principal.

    Raises:
        HTTPException 401: missing, malformed, forged or expired token.
    """
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="missing bearer token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = authorization.split(" ", 1)[1].strip()
    try:
        return verify_token(token, secret_key=get_secret_key())
    except TokenError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(exc),
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc


PrincipalDep = Annotated[Principal, Depends(get_principal)]


def require_roles(*roles: str):
    """Build a dependency that 403s anyone outside ``roles``."""
    allowed = frozenset(roles)

    def checker(principal: PrincipalDep) -> Principal:
        if principal.role not in allowed:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"role {principal.role} cannot access this resource",
            )
        return principal

    return checker


#: Who may read the member list. KIOSK is scan-only (map §2.4) and MEMBER is
#: confined to the /client surface, so neither appears here.
MEMBER_READ_ROLES = frozenset({"OWNER", "ADMIN", "TRAINER", "RECEPTION"})
#: Who may register/edit/tombstone members. RECEPTION runs the front desk;
#: KIOSK and MEMBER cannot write members at all.
MEMBER_WRITE_ROLES = frozenset({"OWNER", "ADMIN", "RECEPTION"})

#: Staff-only dependency — settings, sync, backup, anything generic.
require_staff = require_roles(*STUDIO_ROLES)
require_member_read = require_roles(*MEMBER_READ_ROLES)
require_member_write = require_roles(*MEMBER_WRITE_ROLES)
#: Who may run a JP7 assessment (map §2.4: TRAINER does JP7).
require_assessor = require_roles("OWNER", "ADMIN", "TRAINER")
#: Who may write injury/limitation dossiers.
require_clinician = require_roles("OWNER", "ADMIN", "TRAINER")
#: Full-finance roles (map: TRAINER sees no full finance).
require_finance = require_roles("OWNER", "ADMIN")


def assert_same_gym(principal: Principal, gym_id: int) -> None:
    """Cross-gym access is always a bug — fail closed."""
    if principal.gym_id != gym_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="cross-gym access denied"
        )
