"""Deterministic rule-based program builder (map §3 #7, §5, §7).

No LLM is involved here (rule C7: the rule planner is always in the race and is
what Phase 3 ships). The pipeline mirrors map §7:

    exercise candidate
      -> hard_block by region/pattern? DROP
      -> replaceable? SWAP from library/allowed mods
      -> equipment missing? DROP
      -> assemble mp.program/v1 ops
      -> publish only when trainer_approved (handled by the router)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

PROGRAM_SCHEMA = "mp.program/v1"

# Movement-pattern slots per template day. Order matters (compound first).
PPL = {
    "name": "Push/Pull/Legs",
    "code": "ppl",
    "days": [
        {"day": "Push", "slots": [("push", 3), ("overhead", 2), ("core", 2)]},
        {"day": "Pull", "slots": [("pull", 3), ("hinge", 2), ("core", 2)]},
        {"day": "Legs", "slots": [("squat", 3), ("hinge", 2), ("single_leg", 2)]},
    ],
}
UL = {
    "name": "Upper/Lower",
    "code": "ul",
    "days": [
        {"day": "Upper", "slots": [("push", 2), ("pull", 2), ("overhead", 2), ("core", 2)]},
        {"day": "Lower", "slots": [("squat", 3), ("hinge", 2), ("single_leg", 2)]},
    ],
}
FB = {
    "name": "Full Body",
    "code": "fb",
    "days": [
        {"day": "A", "slots": [("squat", 2), ("push", 2), ("pull", 2), ("core", 1)]},
        {"day": "B", "slots": [("hinge", 2), ("overhead", 2), ("pull", 2), ("core", 1)]},
    ],
}
CORRECTIVE = {
    "name": "Corrective",
    "code": "corrective",
    "days": [{"day": "Mobility", "slots": [("core", 3)]}],
}

TEMPLATES = {t["code"]: t for t in (PPL, UL, FB, CORRECTIVE)}

# Default loading parameters per pattern (sets, reps, rest_s, rir).
LOADING: dict[str, tuple[int, int, int, int]] = {
    "squat": (3, 8, 150, 2),
    "hinge": (3, 6, 180, 2),
    "push": (3, 10, 120, 2),
    "pull": (3, 10, 120, 2),
    "overhead": (3, 8, 120, 2),
    "single_leg": (3, 10, 90, 2),
    "core": (3, 12, 60, 1),
    "cardio": (1, 20, 60, 0),
    "knee_iso": (3, 12, 90, 2),
    "ankle": (3, 15, 60, 1),
}


@dataclass
class ExerciseRow:
    """A library row, decoupled from the DB for pure testing."""

    key: str
    name_en: str
    name_fa: str | None
    equipment: str | None
    pattern: str | None
    hard_block_patterns: set[str] = field(default_factory=set)


@dataclass
class BuildInput:
    template_code: str
    library: list[ExerciseRow]
    blocked_patterns: set[str]
    equipment_available: set[str]
    add_corrective_block: bool = False


@dataclass
class BuiltExercise:
    key: str
    name_en: str
    pattern: str
    sets: int
    reps: int
    rest_s: int
    rir: int
    swapped_from: str | None = None


@dataclass
class BuiltDay:
    name: str
    exercises: list[BuiltExercise] = field(default_factory=list)
    dropped: list[dict[str, str]] = field(default_factory=list)


@dataclass
class BuiltProgram:
    template: str
    schema: str = PROGRAM_SCHEMA
    days: list[BuiltDay] = field(default_factory=list)
    corrective_block_added: bool = False


def _is_blocked(exercise: ExerciseRow, blocked: set[str]) -> bool:
    """Hard-block when the exercise's contraindicated pattern is blocked."""
    return bool(exercise.hard_block_patterns & blocked)


def _has_equipment(exercise: ExerciseRow, available: set[str]) -> bool:
    if exercise.equipment in (None, "bodyweight"):
        return True
    return exercise.equipment in available


def _pick(
    library: list[ExerciseRow],
    pattern: str,
    blocked: set[str],
    available: set[str],
    exclude: set[str],
) -> ExerciseRow | None:
    """Best available exercise for a pattern slot, respecting all filters."""
    for ex in library:
        if ex.key in exclude:
            continue
        if ex.pattern != pattern:
            continue
        if _is_blocked(ex, blocked):
            continue
        if not _has_equipment(ex, available):
            continue
        return ex
    return None


def build_program(inp: BuildInput) -> BuiltProgram:
    """Assemble a program; never emits a hard-blocked or unequipped exercise."""
    template = TEMPLATES.get(inp.template_code)
    if template is None:
        raise ValueError(f"unknown template {inp.template_code!r}")

    program = BuiltProgram(template=template["code"])
    used: set[str] = set()

    for day in template["days"]:
        built_day = BuiltDay(name=day["day"])
        for pattern, count in day["slots"]:
            for _ in range(count):
                primary = _pick(inp.library, pattern, inp.blocked_patterns,
                                inp.equipment_available, used)
                if primary is not None:
                    sets, reps, rest, rir = LOADING.get(pattern, (3, 10, 90, 2))
                    used.add(primary.key)
                    built_day.exercises.append(
                        BuiltExercise(
                            key=primary.key, name_en=primary.name_en, pattern=pattern,
                            sets=sets, reps=reps, rest_s=rest, rir=rir,
                        )
                    )
                    continue

                # Primary unavailable: it was blocked or unequipped. Try a swap
                # from the same pattern that is allowed (the SWAP branch).
                swap = _find_swap(inp, pattern, used)
                if swap is not None:
                    sets, reps, rest, rir = LOADING.get(pattern, (3, 10, 90, 2))
                    used.add(swap.key)
                    built_day.exercises.append(
                        BuiltExercise(
                            key=swap.key, name_en=swap.name_en, pattern=pattern,
                            sets=sets, reps=reps, rest_s=rest, rir=rir,
                            swapped_from=pattern,
                        )
                    )
                else:
                    built_day.dropped.append({"pattern": pattern, "reason": "blocked_or_unequipped"})
        program.days.append(built_day)

    if inp.add_corrective_block:
        program.corrective_block_added = True
        program.days.append(
            BuiltDay(
                name="Corrective",
                exercises=[
                    BuiltExercise(key="core:dead_bug", name_en="Dead Bug", pattern="core",
                                  sets=2, reps=10, rest_s=45, rir=1),
                    BuiltExercise(key="core:bird_dog", name_en="Bird Dog", pattern="core",
                                  sets=2, reps=10, rest_s=45, rir=1),
                ],
            )
        )

    return program


def _find_swap(inp: BuildInput, pattern: str, used: set[str]) -> ExerciseRow | None:
    """A same-pattern exercise that is safe + equipped when the primary is not.

    The primary _pick already returns the first safe exercise, so reaching here
    means every exercise of that pattern is blocked/unequipped; a swap only
    exists if some exercise of a *related safe* pattern can stand in. We look at
    exercises whose hard_block_patterns are disjoint from blocked AND equipped,
    preferring ones tagged as modifications (name contains 'Trap'/'Landmine').
    """
    for ex in inp.library:
        if ex.key in used or ex.pattern == pattern:
            continue
        if _is_blocked(ex, inp.blocked_patterns) or not _has_equipment(ex, inp.equipment_available):
            continue
        if "trap" in (ex.name_en or "").lower() or "landmine" in (ex.name_en or "").lower():
            return ex
    return None


def to_ops(program: BuiltProgram) -> list[dict[str, Any]]:
    """Serialise to the mp.program/v1 whitelist op list (map §8)."""
    ops: list[dict[str, Any]] = []
    for day in program.days:
        for ex in day.exercises:
            ops.append({"op": "addExercise", "day": day.name, "exercise": ex.key,
                        "name": ex.name_en, "swapped_from": ex.swapped_from})
            ops.append({"op": "setSets", "exercise": ex.key, "value": ex.sets})
            ops.append({"op": "setReps", "exercise": ex.key, "value": ex.reps})
            ops.append({"op": "setRest", "exercise": ex.key, "value": ex.rest_s})
            ops.append({"op": "setRIR", "exercise": ex.key, "value": ex.rir})
    if program.corrective_block_added:
        ops.append({"op": "addCorrectiveBlock"})
    return ops
