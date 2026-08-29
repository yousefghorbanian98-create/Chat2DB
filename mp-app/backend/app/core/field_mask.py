"""Field masking for the client app (map §2.4, §9).

A MEMBER must never see clinician notes, other members' data, or internal fields.
Masking is a single choke point so no router can leak by forgetting to strip.
"""

from __future__ import annotations

from typing import Any

#: Columns a MEMBER must never see on their own member row.
MEMBER_HIDDEN = frozenset({
    "note", "clinical_note", "trainer_note", "internal_note",
    "created_by", "updated_by", "deleted_at",
})


def mask_member_row(role: str, row: dict[str, Any]) -> dict[str, Any]:
    """Return a role-appropriate copy of a member row.

    MEMBER: strips clinician/internal notes. Staff roles: unchanged.
    """
    if role != "MEMBER":
        return dict(row)
    return {k: v for k, v in row.items() if k not in MEMBER_HIDDEN}


def mask_assessment_row(role: str, row: dict[str, Any]) -> dict[str, Any]:
    """Strip clinician-only commentary from an assessment for MEMBER."""
    if role != "MEMBER":
        return dict(row)
    return {k: v for k, v in row.items() if k not in {"note", "clinician_note"}}


def mask_many(role: str, rows, masker=mask_member_row) -> list[dict[str, Any]]:
    return [masker(role, dict(r)) for r in rows]
