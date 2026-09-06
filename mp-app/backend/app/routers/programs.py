"""Program generation + lifecycle (map §3 #7, §7, C8). Rules-only in Phase 3."""

from __future__ import annotations

import json
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, ConfigDict, Field

from app.auth.deps import PrincipalDep, require_assessor
from app.auth.scope import ensure_member_visible
from app.core import program_builder as pb
from app.repo import equipment as equipment_repo
from app.repo import exercises as exercises_repo
from app.repo import injuries as injuries_repo
from app.repo import members as members_repo
from app.repo import programs as programs_repo
from app.state import get_engine

router = APIRouter(tags=["programs"])

AssessorPrincipal = Annotated[PrincipalDep, Depends(require_assessor)]


class GenerateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    template: str = Field(default="fb", pattern="^(ppl|ul|fb|corrective)$")


def _library(engine, gym_id: int) -> list[pb.ExerciseRow]:
    """Library + hard-block patterns, shaped for the pure builder."""
    rows = []
    for ex in exercises_repo.list_exercises(engine, gym_id):
        contra = exercises_repo.contraindications_for(engine, gym_id, ex["key"])
        rows.append(
            pb.ExerciseRow(
                key=ex["key"],
                name_en=ex["name_en"],
                name_fa=ex.get("name_fa"),
                equipment=ex.get("equipment"),
                pattern=ex.get("pattern"),
                hard_block_patterns={
                    c["pattern"] for c in contra if c["severity"] == "hard_block"
                },
            )
        )
    return rows


def _build_for_member(engine, gym_id: int, member_id: int, template: str) -> tuple[pb.BuiltProgram, dict]:
    patterns = injuries_repo.list_patterns(engine, gym_id, member_id)
    blocked = set(patterns["blocked_patterns"])

    # Equipment availability is expressed with the same tokens the library
    # uses (barbell/dumbbell/trap_bar/cable/...), stored in the inventory
    # `category` column. Bodyweight is always present.
    equipment = {
        (e["category"] or "").strip().lower()
        for e in equipment_repo.list_equipment(engine, gym_id)
        if e["available"] and e["category"]
    }
    equipment.add("bodyweight")
    library = _library(engine, gym_id)
    has_injury = bool(blocked)

    built = pb.build_program(
        pb.BuildInput(
            template_code=template,
            library=library,
            blocked_patterns=blocked,
            equipment_available=equipment,
            add_corrective_block=has_injury,
        )
    )
    meta = {
        "blocked_patterns": sorted(blocked),
        "equipment_available": sorted(equipment),
        "dropped": [
            {"day": d.name, **drop} for d in built.days for drop in d.dropped
        ],
        "corrective_block_added": built.corrective_block_added,
    }
    return built, meta


@router.post(
    "/members/{member_id}/programs/generate",
    status_code=status.HTTP_201_CREATED,
    summary="Generate a rule-based program (draft)",
)
def generate(member_id: int, body: GenerateRequest, principal: AssessorPrincipal) -> dict:
    engine = get_engine()
    ensure_member_visible(principal, member_id)
    try:
        members_repo.get_member(engine, principal.gym_id, member_id)
    except members_repo.MemberNotFound as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc

    built, meta = _build_for_member(engine, principal.gym_id, member_id, body.template)
    payload = json.dumps({"schema": pb.PROGRAM_SCHEMA, "ops": pb.to_ops(built), "meta": meta},
                         separators=(",", ":"))
    program_id = programs_repo.create_program(
        engine,
        principal.gym_id,
        member_id=member_id,
        title=f"{pb.TEMPLATES[body.template]['name']} (rules)",
        payload=payload,
        source="rules",
    )
    return {
        "id": program_id,
        "status": "draft",
        "template": built.template,
        "days": [
            {"name": d.name, "exercises": [e.key for e in d.exercises], "dropped": d.dropped}
            for d in built.days
        ],
        "meta": meta,
    }


@router.get("/members/{member_id}/programs", summary="Program history for a member")
def list_programs(member_id: int, principal: AssessorPrincipal) -> list[dict]:
    ensure_member_visible(principal, member_id)
    return programs_repo.list_for_member(get_engine(), principal.gym_id, member_id)


@router.post("/programs/{program_id}/dry-run", summary="Dry-run: validate without applying (C8)")
def dry_run(program_id: int, principal: AssessorPrincipal) -> dict:
    """Re-validate the stored ops against the member's CURRENT filters."""
    engine = get_engine()
    program = programs_repo.get_program(engine, principal.gym_id, program_id)
    ensure_member_visible(principal, program["member_id"])

    stored = json.loads(program["payload"])
    patterns = injuries_repo.list_patterns(engine, principal.gym_id, program["member_id"])
    blocked = set(patterns["blocked_patterns"])
    library = {ex.key: ex for ex in _library(engine, principal.gym_id)}

    violations = [
        op["exercise"]
        for op in stored.get("ops", [])
        if op["op"] == "addExercise"
        and library.get(op["exercise"]) is not None
        and (library[op["exercise"]].hard_block_patterns & blocked)
    ]
    return {
        "program_id": program_id,
        "status": program["status"],
        "safe_to_apply": len(violations) == 0,
        "newly_blocked": violations,
    }


@router.post("/programs/{program_id}/apply", summary="Approve + apply (C8: after dry-run)")
def apply(program_id: int, principal: AssessorPrincipal) -> dict:
    engine = get_engine()
    program = programs_repo.get_program(engine, principal.gym_id, program_id)
    ensure_member_visible(principal, program["member_id"])

    # Enforce dry-run-before-apply: refuse if the current filters block any op.
    stored = json.loads(program["payload"])
    blocked = set(injuries_repo.list_patterns(engine, principal.gym_id, program["member_id"])["blocked_patterns"])
    library = {ex.key: ex for ex in _library(engine, principal.gym_id)}
    violations = [
        op["exercise"]
        for op in stored.get("ops", [])
        if op["op"] == "addExercise"
        and library.get(op["exercise"]) is not None
        and (library[op["exercise"]].hard_block_patterns & blocked)
    ]
    if violations:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"reason": "injury filter now blocks exercises", "blocked": violations},
        )

    try:
        updated = programs_repo.set_status(
            engine, principal.gym_id, program_id, "trainer_approved", by=None
        )
    except programs_repo.InvalidTransition as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    return {"id": program_id, "status": updated["status"], "applied_at": updated["applied_at"]}


@router.post("/programs/{program_id}/archive", summary="Archive (the undo of apply)")
def archive(program_id: int, principal: AssessorPrincipal) -> dict:
    try:
        updated = programs_repo.set_status(get_engine(), principal.gym_id, program_id, "archived")
    except programs_repo.ProgramNotFound as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except programs_repo.InvalidTransition as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    return {"id": program_id, "status": updated["status"]}
