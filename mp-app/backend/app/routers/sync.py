"""Delta sync endpoint (map §14 Phase 6). Staff-only; scoped by gym."""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.auth.deps import PrincipalDep, require_member_read
from app.core.sync import delta_since
from app.state import get_engine

router = APIRouter(prefix="/sync", tags=["sync"])

StaffPrincipal = Annotated[PrincipalDep, Depends(require_member_read)]


@router.get("/delta", summary="Rows changed since a cursor (full snapshot if none)")
def delta(principal: StaffPrincipal, since: Annotated[str | None, Query()] = None) -> dict:
    d = delta_since(get_engine(), principal.gym_id, since)
    return {"cursor": d.cursor, "total": d.total, "changes": d.changes}
