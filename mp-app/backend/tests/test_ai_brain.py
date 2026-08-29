"""Brain race/judge + Ollama detection (map §5, rule C7), with a fake LLM."""

from __future__ import annotations

from app.core.ai_brain import (
    AiRuntime,
    Candidate,
    detect_ollama,
    judge_score,
    race,
)


def rules_candidate() -> Candidate:
    return Candidate(
        source="rules",
        calorie_error=0.05,
        respects_limitations=True,
        equipment_available=True,
        muscle_balance=0.9,
        progressive_overload=True,
        novelty_vs_last=0.3,
    )


def test_judge_weights_match_the_map() -> None:
    # Perfect candidate: 3 (cal) + 3 + 3 + 2 + 2 + 1 = 14
    perfect = Candidate("ollama", 0.0, True, True, 1.0, True, 1.0)
    assert judge_score(perfect) == 14
    # Terrible candidate: 0 across the board
    awful = Candidate("ollama", 1.0, False, False, 0.0, False, 0.0)
    assert judge_score(awful) == 0


def test_rules_win_when_llm_absent() -> None:
    result = race(rules_candidate(), None)
    assert result.winner == "rules"
    assert result.llm_score is None


def test_rules_win_ties() -> None:
    result = race(rules_candidate(), rules_candidate())
    assert result.winner == "rules"


def test_llm_wins_only_when_strictly_better_and_safe() -> None:
    better = Candidate(
        source="ollama",
        calorie_error=0.0,
        respects_limitations=True,
        equipment_available=True,
        muscle_balance=1.0,
        progressive_overload=True,
        novelty_vs_last=1.0,
    )
    result = race(rules_candidate(), better)
    assert result.winner == "ollama"
    assert result.llm_score == 14


def test_unsafe_llm_is_rejected_even_if_high_scoring() -> None:
    dangerous = Candidate(
        source="ollama",
        calorie_error=0.0,
        respects_limitations=False,  # ignores an injury
        equipment_available=True,
        muscle_balance=1.0,
        progressive_overload=True,
        novelty_vs_last=1.0,
    )
    result = race(rules_candidate(), dangerous)
    assert result.winner == "rules"


def test_detect_ollama_parses_models() -> None:
    def fake_get(url: str) -> tuple[int, dict]:
        assert url.endswith("/api/tags")
        return 200, {"models": [{"name": "llama3.1:8b"}, {"name": "qwen2.5:3b"}]}

    rt = detect_ollama(http_get=fake_get)
    assert rt.available is True
    assert rt.models == ("llama3.1:8b", "qwen2.5:3b")
    assert rt.model == "llama3.1:8b"


def test_detect_ollama_prefers_the_hint_when_present() -> None:
    def fake_get(url: str) -> tuple[int, dict]:
        return 200, {"models": [{"name": "a"}, {"name": "llama3.1:8b"}]}

    rt = detect_ollama(model_hint="llama3.1:8b", http_get=fake_get)
    assert rt.model == "llama3.1:8b"


def test_detect_ollama_handles_unreachable_server() -> None:
    def fake_get(url: str) -> tuple[int, dict]:
        raise ConnectionError("refused")

    rt = detect_ollama(http_get=fake_get)
    assert rt.available is False
    assert rt.error is not None


def test_detect_ollama_handles_non_200() -> None:
    rt = detect_ollama(http_get=lambda url: (500, {}))
    assert rt.available is False
