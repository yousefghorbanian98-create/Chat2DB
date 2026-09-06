"""Rule-based program builder: the safety contract (map §5/§7), no AI."""

from __future__ import annotations

import pytest

from app.core.program_builder import (
    BuildInput,
    ExerciseRow,
    build_program,
    to_ops,
    PROGRAM_SCHEMA,
)


def lib() -> list[ExerciseRow]:
    return [
        ExerciseRow("ex001", "Barbell Back Squat", "اسکوات", "barbell", "squat", {"deep_squat"}),
        ExerciseRow("ex002", "Goblet Squat", "اسکوات جامی", "dumbbell", "squat", {"deep_squat"}),
        ExerciseRow("ex003", "Conventional Deadlift", "ددلیفت", "barbell", "hinge", {"heavy_deadlift"}),
        ExerciseRow("ex004", "Trap Bar Deadlift", "ددلیفت ذوزنقه", "trap_bar", "hinge", set()),
        ExerciseRow("ex006", "Bench Press", "پرس سینه", "barbell", "push", set()),
        ExerciseRow("ex007", "Push-Up", "شنا", "bodyweight", "push", set()),
        ExerciseRow("ex008", "Overhead Press", "پرس سرشانه", "barbell", "overhead", {"overhead_press"}),
        ExerciseRow("ex009", "Landmine Press", "پرس لندماین", "landmine", "overhead", set()),
        ExerciseRow("ex010", "Pull-Up", "بارفیکس", "bodyweight", "pull", set()),
        ExerciseRow("ex012", "Cable Row", "قایقی", "cable", "pull", set()),
        ExerciseRow("ex019", "Walking Lunge", "لانگز", "dumbbell", "single_leg", set()),
        ExerciseRow("ex025", "Plank", "پلانک", "bodyweight", "core", set()),
        ExerciseRow("ex026", "Dead Bug", "ددباگ", "bodyweight", "core", set()),
    ]


ALL_EQUIPMENT = {"barbell", "dumbbell", "trap_bar", "landmine", "cable", "bodyweight"}


def test_no_hard_blocked_exercise_is_emitted() -> None:
    """The single most important invariant: injuries hard-filter programs."""
    program = build_program(BuildInput(
        template_code="ppl",
        library=lib(),
        blocked_patterns={"heavy_deadlift", "overhead_press"},
        equipment_available=ALL_EQUIPMENT,
    ))
    emitted = {ex.key for day in program.days for ex in day.exercises}
    assert "ex003" not in emitted, "conventional deadlift is hard-blocked"
    assert "ex008" not in emitted, "overhead press is hard-blocked"


def test_blocked_exercise_is_swapped_when_a_safe_alternative_exists() -> None:
    program = build_program(BuildInput(
        template_code="ul",
        library=lib(),
        blocked_patterns={"overhead_press"},
        equipment_available=ALL_EQUIPMENT,
    ))
    emitted = {ex.key for day in program.days for ex in day.exercises}
    assert "ex008" not in emitted
    assert "ex009" in emitted, "landmine press stands in for overhead press"


def test_unequipped_exercise_is_dropped_not_invented() -> None:
    """No trap bar in the gym -> hinge falls back to what IS available."""
    program = build_program(BuildInput(
        template_code="ul",
        library=lib(),
        blocked_patterns=set(),
        equipment_available={"barbell", "dumbbell", "bodyweight", "cable"},  # no trap_bar
    ))
    emitted = {ex.key for day in program.days for ex in day.exercises}
    # deadlift (barbell) is available, so hinge fills; trap bar never appears.
    assert "ex004" not in emitted
    assert "ex003" in emitted


def test_missing_equipment_drops_slot_when_no_alternative() -> None:
    """Only bodyweight in the gym -> barbell-only patterns are dropped."""
    program = build_program(BuildInput(
        template_code="fb",
        library=lib(),
        blocked_patterns=set(),
        equipment_available={"bodyweight"},
    ))
    emitted = {ex.key for day in program.days for ex in day.exercises}
    assert "ex001" not in emitted and "ex006" not in emitted  # barbell gone
    assert "ex007" in emitted, "push-up (bodyweight) stands in for push"


def test_corrective_block_added_only_for_injured_member() -> None:
    injured = build_program(BuildInput(
        template_code="fb", library=lib(), blocked_patterns={"spinal_flexion"},
        equipment_available=ALL_EQUIPMENT, add_corrective_block=True,
    ))
    assert injured.corrective_block_added is True
    assert any(d.name == "Corrective" for d in injured.days)

    healthy = build_program(BuildInput(
        template_code="fb", library=lib(), blocked_patterns=set(),
        equipment_available=ALL_EQUIPMENT, add_corrective_block=False,
    ))
    assert healthy.corrective_block_added is False


def test_unknown_template_raises() -> None:
    with pytest.raises(ValueError):
        build_program(BuildInput("bro-split", lib(), set(), ALL_EQUIPMENT))


def test_to_ops_uses_only_whitelisted_ops() -> None:
    allowed = {"addExercise", "setSets", "setReps", "setRest", "setRIR",
               "addNote", "swapExercise", "addCorrectiveBlock"}
    program = build_program(BuildInput(
        template_code="ppl", library=lib(), blocked_patterns=set(),
        equipment_available=ALL_EQUIPMENT, add_corrective_block=True,
    ))
    ops = to_ops(program)
    assert program.schema == PROGRAM_SCHEMA
    assert all(op["op"] in allowed for op in ops)
    assert any(op["op"] == "addExercise" for op in ops)
    assert any(op["op"] == "addCorrectiveBlock" for op in ops)


def test_every_exercise_in_ops_has_loading_params() -> None:
    program = build_program(BuildInput(
        template_code="ppl", library=lib(), blocked_patterns=set(),
        equipment_available=ALL_EQUIPMENT,
    ))
    ops = to_ops(program)
    added = [op["exercise"] for op in ops if op["op"] == "addExercise"]
    for key in added:
        assert any(o["op"] == "setSets" and o["exercise"] == key for o in ops)
        assert any(o["op"] == "setReps" and o["exercise"] == key for o in ops)
        assert any(o["op"] == "setRest" and o["exercise"] == key for o in ops)
        assert any(o["op"] == "setRIR" and o["exercise"] == key for o in ops)
