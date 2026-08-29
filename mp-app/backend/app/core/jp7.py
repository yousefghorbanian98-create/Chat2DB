"""Jackson–Pollock 7-site body composition — **deterministic, no AI**.

Map rule C6: the LLM never invents measurements. Every number here comes from
the published generalized equations (Jackson & Pollock, 1978) plus the
Siri (1961) / Brozek (1963) density→%BF conversions.

Sites (mm): chest, midaxillary, triceps, subscapular, abdominal, suprailiac,
thigh.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal, Mapping

Sex = Literal["male", "female"]
Equation = Literal["siri", "brozek"]

SITES: tuple[str, ...] = (
    "chest",
    "midaxillary",
    "triceps",
    "subscapular",
    "abdominal",
    "suprailiac",
    "thigh",
)

#: Plausible caliper range in mm. Outside this the measurement is a typo.
MIN_SITE_MM = 1.0
MAX_SITE_MM = 80.0
MIN_AGE = 10
MAX_AGE = 100

PROTOCOL = "jackson_pollock_7"


class Jp7Error(ValueError):
    """Base class for JP7 input problems."""


class MissingSiteError(Jp7Error):
    """A required caliper site is absent or not a number."""


class OutOfRangeError(Jp7Error):
    """A site or age is outside the physically plausible range."""


@dataclass(frozen=True)
class Jp7Result:
    """Full assessment output, safe to persist as ``mp.assessment/v1``."""

    sex: Sex
    age_years: int
    sites_mm: dict[str, float]
    sum_mm: float
    body_density: float
    body_fat_pct: float
    fat_mass_kg: float | None
    lean_mass_kg: float | None
    equation: Equation
    protocol: str = PROTOCOL
    classification: str | None = None


def body_density(sex: Sex, sites: Mapping[str, float], age_years: int) -> float:
    """Body density (g/cc) from the seven skinfolds.

    Raises:
        MissingSiteError: a site is missing/None/non-numeric.
        OutOfRangeError: a site is outside 1–80 mm or age outside 10–100.
    """
    if sex not in ("male", "female"):
        raise Jp7Error(f"sex must be 'male' or 'female', got {sex!r}")
    if not isinstance(age_years, int):
        raise Jp7Error(f"age_years must be an int, got {age_years!r}")
    if not MIN_AGE <= age_years <= MAX_AGE:
        raise OutOfRangeError(
            f"age_years {age_years} outside {MIN_AGE}-{MAX_AGE}"
        )

    total = 0.0
    for site in SITES:
        if site not in sites:
            raise MissingSiteError(f"missing caliper site: {site}")
        raw = sites[site]
        if raw is None or isinstance(raw, bool) or not isinstance(raw, (int, float)):
            raise MissingSiteError(f"site {site} must be a number, got {raw!r}")
        value = float(raw)
        if not MIN_SITE_MM <= value <= MAX_SITE_MM:
            raise OutOfRangeError(
                f"site {site}={value}mm outside {MIN_SITE_MM}-{MAX_SITE_MM}mm"
            )
        total += value

    if sex == "male":
        return (
            1.112
            - 0.00043499 * total
            + 0.00000055 * total**2
            - 0.00028826 * age_years
        )
    return (
        1.097
        - 0.00046971 * total
        + 0.00000056 * total**2
        - 0.00012828 * age_years
    )


def body_fat_percent(density: float, equation: Equation = "siri") -> float:
    """%BF from body density.

    Raises:
        OutOfRangeError: density is not physically meaningful (<= 0).
    """
    if density <= 0:
        raise OutOfRangeError(f"body density must be > 0, got {density}")
    if equation == "siri":
        return (4.95 / density - 4.50) * 100
    if equation == "brozek":
        return (4.57 / density - 4.142) * 100
    raise Jp7Error(f"unknown equation {equation!r} (use 'siri' or 'brozek')")


#: Guide bands from map §6 (men athletic ~6–13%, obese ≥32%; women athletic
#: ~14–20%, obese ≥40%). Below the athletic floor is essential-fat territory.
_BANDS: dict[str, tuple[tuple[float, str], ...]] = {
    "male": (
        (6.0, "essential"),
        (14.0, "athletic"),
        (18.0, "fit"),
        (25.0, "average"),
        (32.0, "overfat"),
    ),
    "female": (
        (14.0, "essential"),
        (21.0, "athletic"),
        (25.0, "fit"),
        (32.0, "average"),
        (40.0, "overfat"),
    ),
}


def classify(sex: Sex, body_fat_pct: float) -> str:
    """Guide classification (map §6). UI must show the source disclaimer."""
    bands = _BANDS[sex]
    for threshold, label in bands:
        if body_fat_pct < threshold:
            return label
    return "obese"


def assess(
    *,
    sex: Sex,
    age_years: int,
    sites_mm: Mapping[str, float],
    weight_kg: float | None = None,
    equation: Equation = "siri",
) -> Jp7Result:
    """Run the whole JP7 pipeline and derive FM/LBM when weight is known.

    Raises:
        Jp7Error (or subclass) for any invalid input.
    """
    if weight_kg is not None and weight_kg <= 0:
        raise OutOfRangeError(f"weight_kg must be > 0, got {weight_kg}")

    cleaned = {site: float(sites_mm[site]) for site in SITES if site in sites_mm}
    density = body_density(sex, sites_mm, age_years)
    pct = body_fat_percent(density, equation)

    fat_mass = round(weight_kg * pct / 100, 4) if weight_kg else None
    lean_mass = round(weight_kg - fat_mass, 4) if weight_kg else None

    return Jp7Result(
        sex=sex,
        age_years=age_years,
        sites_mm={site: round(cleaned[site], 2) for site in SITES},
        sum_mm=round(sum(cleaned.values()), 2),
        body_density=round(density, 6),
        body_fat_pct=round(pct, 4),
        fat_mass_kg=fat_mass,
        lean_mass_kg=lean_mass,
        equation=equation,
        classification=classify(sex, pct),
    )
