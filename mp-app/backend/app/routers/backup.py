"""Owner-only encrypted backup + verified restore (map §14 Phase 6)."""

from __future__ import annotations

import base64
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field

from app.auth.deps import PrincipalDep, require_roles
from app.core.backup import BackupError, create_backup, restore_backup, verify_row_counts
from app.state import get_engine

router = APIRouter(prefix="/admin/backup", tags=["admin"])

OwnerPrincipal = Annotated[PrincipalDep, Depends(require_roles("OWNER"))]


class BackupRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")
    password: str = Field(min_length=8, max_length=200)


class RestoreRequest(BackupRequest):
    blob_b64: str


@router.post("", summary="Create a password-encrypted backup (OWNER)")
def make_backup(body: BackupRequest, principal: OwnerPrincipal) -> dict:
    blob = create_backup(get_engine(), body.password)
    return {"blob_b64": base64.b64encode(blob).decode("ascii"), "bytes": len(blob)}


@router.post("/restore", status_code=status.HTTP_200_OK,
             summary="Restore from an encrypted backup, verifying row counts (OWNER)")
def restore(body: RestoreRequest, principal: OwnerPrincipal) -> dict:
    engine = get_engine()
    try:
        blob = base64.b64decode(body.blob_b64, validate=True)
        counts = restore_backup(engine, blob, body.password)
        verify_row_counts(engine, counts)
    except (BackupError, ValueError) as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc
    return {"restored": counts, "rows": sum(counts.values())}
