"""Nutrition math: Katch–McArdle + TDEE + macros (deterministic, map §9)."""

from __future__ import annotations

import pytest

from app.core.nutrition import (
    NutritionError,
    bmr_katch_mcardle,
    plan_nutrition,
)


def test_bmr_katch_mcardle_known_answer() -> None:
    # BMR = 370 + 21.6 * LBM. LBM 50 -> 370 + 1080 = 1450.
    assert bmr_katch_mcardle(50) == pytest.approx(1450.0)
    assert bmr_katch_mcardle(49.1088) == pytest.approx(370 + 21.6 * 49.1088)


@pytest.mark.parametrize("bad", [0, -5, None, 200])
def test_bmr_rejects_bad_lbm(bad) -> None:
    with pytest.raises(NutritionError):
        bmr_katch_mcardle(bad)


def test_activity_factors_order_monotonically() -> None:
    lbm = 60
    values = [
        plan_nutrition(lean_mass_kg=lbm, activity=a).tdee_kcal
        for a in ("sedentary", "light", "moderate", "active", "athlete")
    ]
    assert values == sorted(values)
    assert values[0] < values[-1]


def test_goal_adjustment_cut_lt_maintain_lt_bulk() -> None:
    lbm = 60
    cut = plan_nutrition(lean_mass_kg=lbm, goal="cut").target_kcal
    maintain = plan_nutrition(lean_mass_kg=lbm, goal="maintain").target_kcal
    bulk = plan_nutrition(lean_mass_kg=lbm, goal="bulk").target_kcal
    assert cut < maintain < bulk


def test_macro_calories_reconstruct_the_target() -> None:
    plan = plan_nutrition(lean_mass_kg=60, activity="moderate", goal="maintain")
    kcal = plan.protein_g * 4 + plan.carbs_g * 4 + plan.fat_g * 9
    # rounding per macro is <=0.05 each; allow small tolerance
    assert kcal == pytest.approx(plan.target_kcal, abs=3.0)


def test_protein_scales_with_lbm_and_per_kg() -> None:
    a = plan_nutrition(lean_mass_kg=50, protein_g_per_kg=2.0)
    assert a.protein_g == pytest.approx(100.0)
    b = plan_nutrition(lean_mass_kg=50, protein_g_per_kg=1.6)
    assert b.protein_g == pytest.approx(80.0)


def test_unknown_goal_or_activity_raises() -> None:
    with pytest.raises(NutritionError):
        plan_nutrition(lean_mass_kg=60, goal="shred")  # type: ignore[arg-type]
    with pytest.raises(NutritionError):
        plan_nutrition(lean_mass_kg=60, activity="couch")  # type: ignore[arg-type]
