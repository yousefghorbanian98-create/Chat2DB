"""Cutting-Edge-style brain: rule vs optional LLM, decided by a judge (map §5).

Rule C7: the rule planner is ALWAYS in the race; if the LLM is absent, fails, or
scores <= the rules, the rules win. The judge is a deterministic weighted score so
the "race" is reproducible and unit-testable with a fake LLM client.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Literal

PlannerSource = Literal["rules", "ollama", "gateway"]


@dataclass(frozen=True)
class Candidate:
    """A program candidate as scored by the judge (higher is better)."""

    source: PlannerSource
    calorie_error: float          # |planned - target| / target, 0..1+
    respects_limitations: bool
    equipment_available: bool
    muscle_balance: float         # 0..1 (push/pull, antag. coverage)
    progressive_overload: bool
    novelty_vs_last: float        # 0..1


def judge_score(c: Candidate) -> int:
    """Weighted judge from map §5 (higher is better)."""
    score = 0
    score += int(round((1.0 - min(1.0, c.calorie_error)) * 3))
    score += 3 if c.respects_limitations else 0
    score += 3 if c.equipment_available else 0
    score += int(round(c.muscle_balance * 2))
    score += 2 if c.progressive_overload else 0
    score += int(round(c.novelty_vs_last * 1))
    return score


@dataclass(frozen=True)
class RaceResult:
    winner: PlannerSource
    rule_score: int
    llm_score: int | None
    reason: str


def race(
    rule_candidate: Candidate,
    llm_candidate: Candidate | None,
) -> RaceResult:
    """Pick the higher-scoring candidate; rules win ties and absent/unsafe LLM."""
    rule = judge_score(rule_candidate)

    if llm_candidate is None:
        return RaceResult("rules", rule, None, "no LLM available — rules win (C7)")

    # An LLM plan that violates hard limitations is never eligible.
    if not llm_candidate.respects_limitations:
        return RaceResult("rules", rule, judge_score(llm_candidate),
                          "LLM violated limitations — rules win (C5)")

    llm = judge_score(llm_candidate)
    if llm > rule:
        return RaceResult(llm_candidate.source, rule, llm, "LLM out-scored rules")
    return RaceResult("rules", rule, llm, "rules >= LLM — rules win (C7)")


# --------------------------------------------------------------------------- #
# Ollama detection
# --------------------------------------------------------------------------- #


@dataclass(frozen=True)
class AiRuntime:
    available: bool
    base_url: str
    model: str | None
    models: tuple[str, ...]
    error: str | None = None


def detect_ollama(
    base_url: str = "http://127.0.0.1:11434",
    model_hint: str | None = None,
    *,
    http_get: Callable[[str], tuple[int, dict]] | None = None,
    timeout: float = 1.5,
) -> AiRuntime:
    """Probe Ollama's ``/api/tags``. Injectable ``http_get`` keeps this testable.

    Returns an ``AiRuntime`` describing availability; never raises.
    """
    getter = http_get or _default_get
    try:
        status, body = getter(f"{base_url.rstrip('/')}/api/tags")
    except Exception as exc:  # pragma: no cover - network failure path
        return AiRuntime(False, base_url, model_hint, (), f"{type(exc).__name__}: {exc}")

    if status != 200:
        return AiRuntime(False, base_url, model_hint, (), f"HTTP {status}")

    models = tuple(m.get("name", "") for m in body.get("models", []))
    chosen = model_hint if model_hint in models else (models[0] if models else None)
    return AiRuntime(True, base_url, chosen, models)


def _default_get(url: str) -> tuple[int, dict]:
    import httpx

    resp = httpx.get(url, timeout=1.5)
    try:
        return resp.status_code, resp.json()
    except ValueError:
        return resp.status_code, {}
