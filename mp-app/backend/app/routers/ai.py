"""AI runtime detection (map §5, §12.4). Local-only; never required (C1/C2)."""

from __future__ import annotations

import os
from typing import Annotated

from fastapi import APIRouter, Depends

from app.auth.deps import PrincipalDep, require_member_read
from app.core.ai_brain import detect_ollama

router = APIRouter(prefix="/ai", tags=["ai"])

# KIOSK is scan-only and has no use for AI runtime info.
StaffPrincipal = Annotated[PrincipalDep, Depends(require_member_read)]


@router.get("/runtime", summary="Is a local LLM (Ollama) available?")
def runtime(principal: StaffPrincipal) -> dict:
    """Detect Ollama on the configured base URL (env MP_AI_BASE_URL)."""
    base = os.environ.get("MP_AI_BASE_URL", "http://127.0.0.1:11434")
    hint = os.environ.get("MP_AI_MODEL")
    rt = detect_ollama(base_url=base, model_hint=hint)
    return {
        "available": rt.available,
        "base_url": rt.base_url,
        "model": rt.model,
        "models": list(rt.models),
        "error": rt.error,
        "note": "Rules remain authoritative even when a local LLM is present (C7).",
    }
