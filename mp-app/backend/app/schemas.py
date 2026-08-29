"""Pydantic schemas for the Phase 1 surface.

Field masking (map §9) is enforced by *which* schema a route returns: a MEMBER
never receives ``MemberOut``, only ``SelfMemberOut`` without clinician notes.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

Sex = Literal["male", "female"]
InjuryStatus = Literal["active", "recovering", "cleared", "chronic"]
BodyRegion = Literal[
    "neck", "cervical", "thoracic", "lumbar", "SI", "shoulder", "scapula",
    "elbow", "wrist", "hand", "hip", "groin", "knee", "ankle", "foot",
    "chest", "abdomen", "cardiovascular", "respiratory", "neurological", "other",
]
Side = Literal["left", "right", "bilateral"]


class MemberCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    membership_code: str = Field(min_length=1, max_length=40)
    first_name: str = Field(min_length=1, max_length=80)
    last_name: str = Field(min_length=1, max_length=80)
    sex: Sex
    birth_date: str | None = None
    phone: str | None = Field(default=None, max_length=32)
    membership_exp: str | None = None
    guardian_consent: bool = False


class MemberUpdate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    first_name: str | None = Field(default=None, min_length=1, max_length=80)
    last_name: str | None = Field(default=None, min_length=1, max_length=80)
    sex: Sex | None = None
    birth_date: str | None = None
    phone: str | None = Field(default=None, max_length=32)
    membership_exp: str | None = None
    guardian_consent: bool | None = None


class MemberOut(BaseModel):
    """Studio view — full record, no clinician notes (those live on injuries)."""

    id: int
    membership_code: str
    first_name: str
    last_name: str
    sex: Sex
    birth_date: str | None
    phone: str | None
    membership_exp: str | None
    guardian_consent: bool
    created_at: str
    active_injuries: int = 0


class SelfMemberOut(BaseModel):
    """Client view — deliberately narrower than MemberOut."""

    id: int
    first_name: str
    last_name: str
    membership_exp: str | None


class PinLogin(BaseModel):
    model_config = ConfigDict(extra="forbid")

    username: str = Field(min_length=1, max_length=64)
    pin: str = Field(min_length=1, max_length=32)


class TokenResponse(BaseModel):
    token: str
    role: str
    gym_id: int
    expires_in: int


class MemberPinLogin(BaseModel):
    model_config = ConfigDict(extra="forbid")

    membership_code: str = Field(min_length=1, max_length=64)
    pin: str = Field(min_length=1, max_length=32)


class SetMemberPin(BaseModel):
    model_config = ConfigDict(extra="forbid")

    pin: str = Field(min_length=4, max_length=32)


class Sites(BaseModel):
    model_config = ConfigDict(extra="forbid")

    chest: float = Field(gt=0, le=80)
    midaxillary: float = Field(gt=0, le=80)
    triceps: float = Field(gt=0, le=80)
    subscapular: float = Field(gt=0, le=80)
    abdominal: float = Field(gt=0, le=80)
    suprailiac: float = Field(gt=0, le=80)
    thigh: float = Field(gt=0, le=80)


class AssessmentCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    weight_kg: float = Field(gt=0, le=400)
    height_cm: float | None = Field(default=None, gt=0, le=280)
    age_years: int = Field(ge=10, le=100)
    sites_mm: Sites
    equation: Literal["siri", "brozek"] = "siri"


class AssessmentOut(BaseModel):
    id: int
    member_id: int
    protocol: str
    equation: str
    age_years: int
    weight_kg: float
    sum_mm: float
    body_density: float
    body_fat_pct: float
    fat_mass_kg: float | None
    lean_mass_kg: float | None
    classification: str | None
    created_at: str


class InjuryCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    body_region: BodyRegion
    side: Side | None = None
    label: str = Field(min_length=1, max_length=120)
    status: InjuryStatus = "active"
    pain_0_10: int | None = Field(default=None, ge=0, le=10)
    onset: str | None = None
    cleared: str | None = None
    contraindicated_patterns: list[str] = Field(default_factory=list)
    allowed_modifications: list[str] = Field(default_factory=list)
    clinician_note: str | None = None
    member_visible_note: str | None = None
    requires_clearance: bool = False


class InjuryOut(BaseModel):
    """Studio view — includes the clinician note."""

    id: int
    member_id: int
    body_region: str
    side: str | None
    label: str
    status: str
    pain_0_10: int | None
    contraindicated_patterns: list[str]
    allowed_modifications: list[str]
    clinician_note: str | None
    member_visible_note: str | None
    requires_clearance: bool


class InjuryPublicOut(BaseModel):
    """Client view — clinician note is stripped (map C10 / §9)."""

    id: int
    body_region: str
    label: str
    status: str
    member_visible_note: str | None
