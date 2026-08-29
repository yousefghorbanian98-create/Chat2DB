"""Deterministic nutrition math (map §3 #9, §5: no LLM invents macros).

Katch–McArdle BMR from lean body mass, TDEE from an activity factor, then a
goal-adjusted calorie target and macro split. All deterministic and golden-tested.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

Goal = Literal["cut", "maintain", "bulk"]
Activity = Literal["sedentary", "light", "moderate", "active", "athlete"]

ACTIVITY_FACTORS: dict[Activity, float] = {
    "sedentary": 1.2,
    "light": 1.375,
    "moderate": 1.55,
    "active": 1.725,
    "athlete": 1.9,
}

GOAL_ADJUST: dict[Goal, float] = {
    "cut": 0.85,   # -15%
    "maintain": 1.0,
    "bulk": 1.10,  # +10%
}


class NutritionError(ValueError):
    """Invalid nutrition input."""


@dataclass(frozen=True)
class NutritionPlan:
    bmr_kcal: float
    tdee_kcal: float
    target_kcal: float
    protein_g: float
    carbs_g: float
    fat_g: float
    goal: Goal
    activity: Activity


def bmr_katch_mcardle(lean_mass_kg: float) -> float:
    """BMR = 370 + 21.6 * LBM (Katch–McArdle).

    Raises:
        NutritionError: non-positive or implausible LBM.
    """
    if lean_mass_kg is None or lean_mass_kg <= 0:
        raise NutritionError("lean_mass_kg must be > 0")
    if lean_mass_kg > 150:
        raise NutritionError("lean_mass_kg implausible (>150)")
    return 370 + 21.6 * lean_mass_kg


def plan_nutrition(
    *,
    lean_mass_kg: float,
    activity: Activity = "moderate",
    goal: Goal = "maintain",
    protein_g_per_kg: float = 1.8,
) -> NutritionPlan:
    """Full deterministic plan from LBM.

    Macro split: protein fixed at ``protein_g_per_kg`` of *total* body-relevant
    mass approximated by LBM; fat 25% of target calories; carbs the remainder.
    """
    if activity not in ACTIVITY_FACTORS:
        raise NutritionError(f"unknown activity {activity!r}")
    if goal not in GOAL_ADJUST:
        raise NutritionError(f"unknown goal {goal!r}")
    if protein_g_per_kg <= 0 or protein_g_per_kg > 4:
        raise NutritionError("protein_g_per_kg must be in (0, 4]")

    bmr = bmr_katch_mcardle(lean_mass_kg)
    tdee = bmr * ACTIVITY_FACTORS[activity]
    target = tdee * GOAL_ADJUST[goal]

    protein = lean_mass_kg * protein_g_per_kg
    fat = (target * 0.25) / 9
    carbs = max(0.0, (target - protein * 4 - fat * 9) / 4)

    return NutritionPlan(
        bmr_kcal=round(bmr, 1),
        tdee_kcal=round(tdee, 1),
        target_kcal=round(target, 1),
        protein_g=round(protein, 1),
        carbs_g=round(carbs, 1),
        fat_g=round(fat, 1),
        goal=goal,
        activity=activity,
    )
