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
        persian=False,
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
        persian=False,
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


# --- Persian PDF (map C10: Persian-first UI) -------------------------------
# The bundled font is DejaVu Sans 2.37 (see app/core/persian.py provenance).
# Raw PDF bytes store Persian as glyph IDs (TrueType subset), so reading the
# text layer back requires a PDF reader; we use PyMuPDF when importable and
# otherwise skip the content assertions while still pinning font embedding.

FA_MEMBER = {"first_name": "نسیم", "last_name": "رحیمی", "sex": "female"}


def _extract_text(pdf: bytes) -> str:
    """Decode the PDF text layer via PyMuPDF (glyph IDs -> unicode)."""
    import pymupdf

    doc = pymupdf.open(stream=pdf, filetype="pdf")
    return "".join(page.get_text() for page in doc)


def test_fa_shaper_produces_visual_order_and_joined_forms() -> None:
    from app.core.persian import fa

    shaped = fa("سلام")
    # Reshaped to visual order, so it is no longer the logical string.
    assert shaped != "سلام"
    assert len(shaped) >= 3


def test_persian_report_embeds_the_persian_font() -> None:
    pdf = build_assessment_pdf(
        gym_name="ماسل پارادایز", member=FA_MEMBER, assessment=ASSESSMENT,
        brozek_pct=21.1, history=[], compress=False, persian=True,
    )
    assert pdf[:5] == b"%PDF-"
    assert b"FontFile2" in pdf, "the TTF must be embedded"
    assert b"DejaVuSans" in pdf, "embedded subset must be the bundled face"
    # Embedding a ~50 KB subset makes the Persian report far larger than the
    # Helvetica English one — a cheap, dependency-free signal it is NOT Latin.
    english = build_assessment_pdf(
        gym_name="G", member=MEMBER, assessment=ASSESSMENT,
        brozek_pct=21.1, history=[], compress=False, persian=False,
    )
    assert len(pdf) > len(english), "Persian must carry the embedded font"


def test_persian_report_content_survives_shaping_rule_c6() -> None:
    pymupdf = __import__("pymupdf") if _has_pymupdf() else None
    if pymupdf is None:
        import pytest
        pytest.skip("pymupdf not installed; raw bytes store glyph IDs")

    pdf = build_assessment_pdf(
        gym_name="ماسل پارادایز", member=FA_MEMBER, assessment=ASSESSMENT,
        brozek_pct=21.1, history=[], compress=False, persian=True,
    )
    from app.core.persian import fa

    text = _extract_text(pdf)
    # PyMuPDF re-applies bidi on extraction, so the embedded visual string and
    # the extracted one carry the SAME glyphs in a different order. Compare as
    # multisets rather than as substrings.
    shaped = fa("نتایج")
    lines = [ln for ln in text.splitlines() if sorted(ln) == sorted(shaped)]
    assert lines, "Persian 'نتایج' heading must round-trip through shaping+embedding"
    # Server-computed values are written as Latin numerals and must survive.
    assert "21.43" in text, "primary Siri BF must appear in the Persian PDF"
    assert "1.0500" in text


def _has_pymupdf() -> bool:
    try:
        import pymupdf  # noqa: F401
        return True
    except ImportError:
        return False


def test_english_fallback_is_still_available() -> None:
    pdf = build_assessment_pdf(
        gym_name="Muscle Paradise", member=MEMBER, assessment=ASSESSMENT,
        brozek_pct=21.1, history=[], compress=False, persian=False,
    )
    text = pdf.decode("latin-1")
    assert "Result" in text
    assert "Sara" in text


def test_default_language_prefers_persian_when_font_present() -> None:
    from app.core.persian import is_persian_available

    if not is_persian_available():
        import pytest
        pytest.skip("Persian font/shapers not available in this environment")

    pdf = build_assessment_pdf(
        gym_name="ماسل پارادایز", member=FA_MEMBER, assessment=ASSESSMENT,
        brozek_pct=21.1, history=[], compress=False,
    )
    assert b"FontFile2" in pdf, "default with a font present must embed it"


def test_receipt_persian_and_english_both_render() -> None:
    from app.core.persian import is_persian_available
    from app.core.receipt_pdf import build_receipt_pdf

    pay = {"receipt_no": "R-1-000001", "method": "cash",
           "created_at": "2026-08-30T10:00:00Z", "amount_rial": 1_500_000, "voided": 0}
    member = {"first_name": "نسیم", "last_name": "رحیمی"}

    en = build_receipt_pdf(gym_name="G", payment=pay, member={"first_name": "S", "last_name": "A"},
                           package_name=None, compress=False, persian=False)
    assert b"Receipt no" in en and b"1,500,000 Rial" in en

    if not is_persian_available():
        import pytest
        pytest.skip("Persian font/shapers not available")
    fa_pdf = build_receipt_pdf(gym_name="ماسل پارادایز", payment=pay, member=member,
                               package_name="ماهانه", compress=False, persian=True)
    assert fa_pdf[:5] == b"%PDF-"
    assert b"FontFile2" in fa_pdf, "Persian receipt must embed the font"
    assert len(fa_pdf) > len(en), "Persian carries the embedded subset"
