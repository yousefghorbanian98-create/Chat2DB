"""Optional n8n bridge: owner toggles + the reports automations poll (map §12.8).

The core gym never needs any of this; it only *enables* side-channel
notifications when the owner wires an n8n instance.
"""

from __future__ import annotations

from typing import Annotated

from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel, ConfigDict, Field

from app.auth.deps import require_roles, require_staff
from app.automation import events
from app.repo import reports
from app.state import get_engine

router = APIRouter(tags=["automation"])


class AutomationConfigIn(BaseModel):
    model_config = ConfigDict(extra="forbid")

    enabled: bool | None = None
    url: str | None = Field(default=None, max_length=256)
    secret: str | None = Field(default=None, min_length=8, max_length=128)
    forbid_phi: bool | None = None


def _config_view() -> dict:
    cfg = events.get_config()
    return {
        "enabled": cfg.enabled,
        "url": cfg.url,
        "secret_configured": bool(cfg.secret),
        "allowed_channels": list(cfg.allowed_channels),
        "forbid_phi": cfg.forbid_phi,
    }


@router.get("/automation/config", summary="Current bridge configuration (owner)")
def get_config(owner=Depends(require_roles("OWNER"))) -> dict:  # noqa: F821
    return _config_view()


@router.post("/automation/config", summary="Enable/disable the n8n bridge (owner)")
def update_config(body: AutomationConfigIn, owner=Depends(require_roles("OWNER"))) -> dict:
    events.set_config(**body.model_dump(exclude_none=True))
    return _config_view()


@router.get("/reports/expiring", summary="Members expiring within N days")
def expiring(
    days: int = Query(default=7, ge=0, le=365), staff=Depends(require_staff)
) -> list[dict]:
    return reports.list_expiring(get_engine(), staff.gym_id, days)


@router.get("/reports/inactive-members", summary="Members not seen in N days")
def inactive(
    days: int = Query(default=7, ge=1, le=365), staff=Depends(require_staff)
) -> list[dict]:
    return reports.list_inactive(get_engine(), staff.gym_id, days)
