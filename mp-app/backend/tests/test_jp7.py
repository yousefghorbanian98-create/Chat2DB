"""Golden known-answer tests for the JP7 pipeline (map §6: >=10 fixtures).

HOW THE EXPECTED VALUES WERE DERIVED
------------------------------------
1. **External anchor** — a published worked example (male, age 35, sum of 7
   skinfolds = 107 mm) states body density **1.06166**. We assert our density
   matches it to 1e-5. (That source then computes 495/BD as 466.34; the correct
   quotient is 466.2492, i.e. 16.25% BF — so we anchor on *density*, not on
   their rounded percentage. See test_external_anchor_matches_published_density.)
2. **Independent arithmetic** — the remaining fixtures were computed with
   Python ``decimal`` at 28-digit precision directly from the published
   coefficients (Jackson & Pollock 1978; Siri 1961; Brozek 1963) *before* this
   module existed, then pasted in as literals. They therefore catch coefficient
   typos, sign errors, sex-mixups and rounding drift in ``app/core/jp7.py``.
3. Tolerance: map requires |error| <= 0.05 percentage points of BF.
"""

from __future__ import annotations

import pytest

from app.core.jp7 import (
    MAX_SITE_MM,
    MIN_SITE_MM,
    SITES,
    Jp7Error,
    MissingSiteError,
    OutOfRangeError,
    assess,
    body_density,
    body_fat_percent,
    classify,
)


def _sites(total_mm: float) -> dict[str, float]:
    """Spread ``total_mm`` evenly across the 7 sites (1 decimal each)."""
    per = round(total_mm / len(SITES), 4)
    out = {site: per for site in SITES}
    # Put the rounding remainder on the last site so the sum is exact.
    out[SITES[-1]] = round(total_mm - per * (len(SITES) - 1), 4)
    return out


# (sex, age, sum_mm, expected_density, expected_siri_pct, expected_brozek_pct)
GOLDEN: list[tuple[str, int, float, float, float, float]] = [
    ("male", 25, 60, 1.080674, 8.0474, 8.6842),
    ("male", 25, 100, 1.066794, 14.0069, 14.1862),
    ("male", 35, 80, 1.070632, 12.3439, 12.6508),
    ("male", 45, 120, 1.054750, 19.3057, 19.0782),
    ("male", 55, 150, 1.043272, 24.4687, 23.8448),
    ("male", 18, 30, 1.094257, 2.3619, 3.4351),
    ("female", 25, 60, 1.067626, 13.6453, 13.8524),
    ("female", 25, 100, 1.052422, 20.3436, 20.0365),
    ("female", 35, 80, 1.058517, 17.6352, 17.5359),
    ("female", 45, 120, 1.042926, 24.6261, 23.9902),
    ("female", 55, 150, 1.032088, 29.6102, 28.5917),
    ("female", 18, 30, 1.081104, 7.8654, 8.5162),
]


@pytest.mark.golden
@pytest.mark.parametrize(("sex", "age", "sum_mm", "bd", "siri", "brozek"), GOLDEN)
def test_golden_fixtures(
    sex: str, age: int, sum_mm: float, bd: float, siri: float, brozek: float
) -> None:
    """12 known-answer fixtures, asserted to map §6 tolerance."""
    sites = _sites(sum_mm)
    assert abs(sum(sites.values()) - sum_mm) < 1e-9, "fixture sites must sum exactly"

    got_bd = body_density(sex, sites, age)  # type: ignore[arg-type]
    assert got_bd == pytest.approx(bd, abs=1e-5)
    assert body_fat_percent(got_bd, "siri") == pytest.approx(siri, abs=0.05)
    assert body_fat_percent(got_bd, "brozek") == pytest.approx(brozek, abs=0.05)


@pytest.mark.golden
def test_external_anchor_matches_published_density() -> None:
    """Published example (male, 35, sum=107) -> BD 1.06166."""
    sites = _sites(107.0)
    assert body_density("male", sites, 35) == pytest.approx(1.06166, abs=1e-5)


@pytest.mark.golden
def test_derived_fat_and_lean_mass() -> None:
    """male 25 / sum 60 / 80 kg -> FM 6.4379, LBM 73.5621 (hand-computed)."""
    result = assess(sex="male", age_years=25, sites_mm=_sites(60), weight_kg=80.0)
    assert result.fat_mass_kg == pytest.approx(6.4379, abs=0.0005)
    assert result.lean_mass_kg == pytest.approx(73.5621, abs=0.0005)
    assert result.lean_mass_kg + result.fat_mass_kg == pytest.approx(80.0, abs=1e-6)


@pytest.mark.golden
def test_body_fat_rises_monotonically_with_skinfold_sum() -> None:
    """Sanity invariant: thicker folds always mean higher BF, same age/sex."""
    male = [
        assess(sex="male", age_years=30, sites_mm=_sites(total)).body_fat_pct
        for total in (30, 50, 70, 90, 110, 130, 150)
    ]
    assert male == sorted(male)
    assert male[0] < male[-1]


@pytest.mark.golden
def test_same_sum_higher_age_means_higher_body_fat() -> None:
    """Age enters the density equation with a negative coefficient."""
    young = assess(sex="female", age_years=20, sites_mm=_sites(90)).body_fat_pct
    older = assess(sex="female", age_years=50, sites_mm=_sites(90)).body_fat_pct
    assert older > young


@pytest.mark.golden
def test_sex_equations_differ_for_identical_input() -> None:
    """Guards against a copy/paste that made both sexes use one equation."""
    sites = _sites(90)
    assert body_density("male", sites, 30) != pytest.approx(
        body_density("female", sites, 30), abs=1e-6
    )


@pytest.mark.golden
def test_classification_bands_follow_map() -> None:
    """Map §6: men athletic ~6–13%, obese >=32%; women athletic ~14–20%, >=40%."""
    assert classify("male", 8.0) == "athletic"
    assert classify("male", 32.0) == "obese"
    assert classify("male", 31.9) == "overfat"
    assert classify("male", 2.0) == "essential"
    assert classify("female", 16.0) == "athletic"
    assert classify("female", 40.0) == "obese"
    assert classify("female", 39.9) == "overfat"


@pytest.mark.golden
def test_missing_site_is_rejected() -> None:
    sites = _sites(70)
    del sites["subscapular"]
    with pytest.raises(MissingSiteError, match="subscapular"):
        body_density("male", sites, 30)


@pytest.mark.golden
@pytest.mark.parametrize("bad", [0.0, 0.4, MAX_SITE_MM + 0.1, 999.0, -5.0])
def test_out_of_range_site_is_rejected(bad: float) -> None:
    sites = _sites(70)
    sites["thigh"] = bad
    with pytest.raises(OutOfRangeError):
        body_density("male", sites, 30)


@pytest.mark.golden
@pytest.mark.parametrize("age", [0, 9, 101, 250])
def test_out_of_range_age_is_rejected(age: int) -> None:
    with pytest.raises(OutOfRangeError):
        body_density("male", _sites(70), age)


@pytest.mark.golden
def test_non_numeric_site_is_rejected_not_coerced() -> None:
    sites = _sites(70)
    sites["chest"] = "12"  # type: ignore[assignment]
    with pytest.raises(MissingSiteError):
        body_density("male", sites, 30)


@pytest.mark.golden
def test_unknown_equation_raises() -> None:
    with pytest.raises(Jp7Error):
        body_fat_percent(1.07, "deurenberg")  # type: ignore[arg-type]


@pytest.mark.golden
def test_bad_weight_is_rejected() -> None:
    with pytest.raises(OutOfRangeError):
        assess(sex="male", age_years=30, sites_mm=_sites(70), weight_kg=0)


@pytest.mark.golden
def test_result_is_json_serialisable_payload() -> None:
    """Persisted as mp.assessment/v1 — must survive JSON round-trip."""
    import json
    from dataclasses import asdict

    result = assess(sex="female", age_years=31, sites_mm=_sites(95), weight_kg=62.5)
    assert json.loads(json.dumps(asdict(result)))["protocol"] == "jackson_pollock_7"
    assert set(result.sites_mm) == set(SITES)
    assert MIN_SITE_MM <= min(result.sites_mm.values())
