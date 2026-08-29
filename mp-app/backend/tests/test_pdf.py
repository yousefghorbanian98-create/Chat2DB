"""PDF assessment report: deterministic bytes, correct content, correct types."""

from __future__ import annotations

from app.core.pdf_report import build_assessment_pdf

MEMBER = {
    "first_name": "Sara",
    "last_name": "Azad",
    "sex": "female",
}

ASSESSMENT = {
    "age_years": 30,
    "weight_kg": 62.5,
    "body_fat_pct": 21.4259,
    "body_density": 1.050006,
    "fat_mass_kg": 13.3912,
    "lean_mass_kg": 49.1088,
    "classification": "fit",
    "sum_mm": 105.0,
    "sites_mm": {
        "chest": 12, "midaxillary": 10, "triceps": 14, "subscapular": 16,
        "abdominal": 20, "suprailiac": 15, "thigh": 18,
    },
}


def test_pdf_is_a_real_pdf_document() -> None:
    pdf = build_assessment_pdf(
        gym_name="Muscle Paradise",
        member=MEMBER,
        assessment=ASSESSMENT,
        brozek_pct=21.1,
        history=[],
    )
    assert isinstance(pdf, bytes)
    assert pdf[:5] == b"%PDF-", "must be a genuine PDF"
    assert len(pdf) > 1000


def test_pdf_contains_the_member_and_key_numbers() -> None:
    # compress=False so the text layer is readable for assertions.
    pdf = build_assessment_pdf(
        gym_name="Muscle Paradise",
        member=MEMBER,
        assessment=ASSESSMENT,
        brozek_pct=21.1,
        history=[],
        compress=False,
    )
    text = pdf.decode("latin-1")
    assert "Sara" in text
    assert "Azad" in text
    assert "21.43" in text, "primary Siri BF should appear"
    assert "Jackson" in text or "Pollock" in text


def test_pdf_handles_missing_fat_mass_and_empty_sites() -> None:
    """A weightless assessment must not crash the report."""
    sparse = dict(ASSESSMENT)
    sparse["fat_mass_kg"] = None
    sparse["lean_mass_kg"] = None
    sparse["sites_mm"] = None
    pdf = build_assessment_pdf(
        gym_name="Muscle Paradise",
        member=MEMBER,
        assessment=sparse,
        brozek_pct=21.1,
        history=[],
    )
    assert pdf[:5] == b"%PDF-"


def test_pdf_includes_history_table_when_present() -> None:
    pdf = build_assessment_pdf(
        gym_name="Muscle Paradise",
        member=MEMBER,
        assessment=ASSESSMENT,
        brozek_pct=21.1,
        history=[
            {"created_at": "2026-08-29T10:00:00Z", "body_fat_pct": 21.42, "weight_kg": 62.5},
            {"created_at": "2026-08-01T10:00:00Z", "body_fat_pct": 22.1, "weight_kg": 63.0},
        ],
        compress=False,
    )
    assert pdf[:5] == b"%PDF-"
    assert b"History" in pdf


def test_compressed_pdf_is_smaller_than_uncompressed() -> None:
    """Sanity: compression actually shrinks the report (perf watchdog)."""
    plain = build_assessment_pdf(
        gym_name="G", member=MEMBER, assessment=ASSESSMENT, brozek_pct=21.1, history=[],
        compress=False,
    )
    zipped = build_assessment_pdf(
        gym_name="G", member=MEMBER, assessment=ASSESSMENT, brozek_pct=21.1, history=[],
        compress=True,
    )
    assert zipped[:5] == b"%PDF-"
    assert len(zipped) < len(plain)
