"""Assessment PDF report (map §14 Phase 1: "PDF assessment report").

Rendered in **Persian** (map C10: Persian-first UI) when a Persian TTF is
available, and in English otherwise — never as mojibake. See
``app/core/persian.py`` for the font/shaping contract and provenance.

All numbers come from the stored assessment (server-computed, rule C6); this
module only formats them.
"""

from __future__ import annotations

import io
from typing import Any

from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

from .persian import PERSIAN_FONT, fa, register_persian_font

EMERALD = colors.HexColor("#00B86A")
GOLD = colors.HexColor("#B8860B")  # printable gold on white paper
INK = colors.HexColor("#0B0F14")

#: Latin face used for the English fallback and for numbers.
_LATIN = "Helvetica"
_LATIN_BOLD = "Helvetica-Bold"

_SITE_FA: dict[str, str] = {
    "chest": "سینه",
    "midaxillary": "زیر بغل",
    "triceps": "پشت بازو",
    "subscapular": "زیر کتف",
    "abdominal": "شکم",
    "suprailiac": "لگن",
    "thigh": "ران",
}

_CLASS_FA: dict[str, str] = {
    "essential": "ضروری",
    "athletic": "ورزشکاری",
    "fit": "آماده",
    "average": "متوسط",
    "overfat": "بیش‌چربی",
    "obese": "چاق",
}

_SEX_FA = {"male": "مرد", "female": "زن"}


class _L10n:
    """Bilingual label set chosen once per document.

    Keeping the strings on one object avoids threading a ``persian`` flag
    through every helper (and keeps each function inside the 3-param limit).
    """

    def __init__(self, persian: bool) -> None:
        self.persian = persian
        self.font = PERSIAN_FONT if persian else _LATIN
        self.bold = PERSIAN_FONT if persian else _LATIN_BOLD
        s = fa if persian else (lambda x: x)  # shape only when Persian
        self.title = s("ماسل پارادایز — ارزیابی جکسون-پولاک ۷") if persian else (
            "Muscle Paradise — Jackson–Pollock 7 Assessment"
        )
        self.result = s("نتایج") if persian else "Result"
        self.sites = s("چین‌های پوستی اندازه‌گیری‌شده (میلی‌متر)") if persian else (
            "Measured skinfolds (mm)"
        )
        self.history = s("روند (جدیدترین ابتدا)") if persian else "History (newest first)"
        self.site_col = s("ناحیه") if persian else "Site"
        self.date_col = s("تاریخ") if persian else "Date"
        self.bf_col = s("چربی ٪ (Siri)") if persian else "BF% (Siri)"
        self.weight_col = s("وزن kg") if persian else "Weight kg"
        self.age = s("سن") if persian else "age"
        self.weight = s("وزن") if persian else "weight"

    def t(self, fa_text: str, en_text: str) -> str:
        """Pick the label for the active language, shaping it if Persian."""
        return fa(fa_text) if self.persian else en_text

    def rows(self) -> list[tuple[str, str]]:
        """The result table's label column, already shaped."""
        pairs = [
            ("چربی بدن (Siri، اصلی)", "Body fat (Siri, primary)"),
            ("چربی بدن (Brozek)", "Body fat (Brozek)"),
            ("چگالی بدن", "Body density"),
            ("جرم چربی", "Fat mass"),
            ("جرم بدون چربی", "Lean mass"),
            ("رده‌بندی", "Classification"),
            ("مجموع ۷ چین", "Sum of 7 skinfolds"),
        ]
        return [(self.t(f, e)) for f, e in pairs]


def _styles(l10n: _L10n) -> dict[str, ParagraphStyle]:
    base = getSampleStyleSheet()
    align = TA_RIGHT if l10n.persian else 0
    return {
        "title": ParagraphStyle(
            "mpTitle", parent=base["Title"], textColor=EMERALD, spaceAfter=2,
            fontName=l10n.font, alignment=align,
        ),
        "sub": ParagraphStyle(
            "mpSub", parent=base["Normal"], textColor=colors.grey, fontSize=9,
            fontName=l10n.font, alignment=align,
        ),
        "h2": ParagraphStyle(
            "mpH2", parent=base["Heading2"], textColor=INK, spaceBefore=8,
            fontName=l10n.bold, alignment=align,
        ),
        "body": ParagraphStyle(
            "mpBody", parent=base["Normal"], fontName=l10n.font, alignment=align,
        ),
    }


def build_assessment_pdf(
    *,
    gym_name: str,
    member: dict[str, Any],
    assessment: dict[str, Any],
    brozek_pct: float,
    history: list[dict[str, Any]],
    compress: bool = True,
    persian: bool | None = None,
) -> bytes:
    """Render one assessment to PDF bytes.

    Args:
        gym_name: branding line.
        member: member row (first_name/last_name/sex/...).
        assessment: stored assessment row (siri is the primary equation).
        brozek_pct: the Brozek %BF computed for the same inputs (map: store both).
        history: newest-first rows for the trend table.
        persian: force the language. Defaults to "use Persian if a font is
            registered", so the report degrades to English instead of breaking.
    """
    use_fa = register_persian_font() if persian is None else (persian and register_persian_font())
    l10n = _L10n(use_fa)
    st = _styles(l10n)

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4, title="Muscle Paradise — JP7 Assessment",
        leftMargin=18 * mm, rightMargin=18 * mm, topMargin=16 * mm, bottomMargin=16 * mm,
        pageCompression=1 if compress else 0,
    )

    story: list[Any] = [
        Paragraph(l10n.title, st["title"]),
        Paragraph(fa(f"{gym_name} — سیستم‌عامل محلی باشگاه") if use_fa
                  else f"{gym_name} · local-first gym OS", st["sub"]),
        Spacer(1, 6 * mm),
        Paragraph(_member_line(member, assessment, l10n), st["body"]),
        Spacer(1, 4 * mm),
        Paragraph(l10n.result, st["h2"]),
    ]

    story.append(Table(_result_rows(assessment, brozek_pct, l10n), colWidths=[70 * mm, 60 * mm]))
    story.append(Paragraph(l10n.sites, st["h2"]))
    story.append(Table(_site_rows(assessment, l10n), colWidths=[60 * mm, 30 * mm]))

    if history:
        story.append(Paragraph(l10n.history, st["h2"]))
        story.append(Table(_history_rows(history, l10n), colWidths=[45 * mm, 40 * mm, 40 * mm]))

    story.append(Spacer(1, 6 * mm))
    story.append(Paragraph(_disclaimer(use_fa), st["sub"]))

    _style_tables(story, l10n)
    doc.build(story)
    return buffer.getvalue()


def _member_line(member: dict[str, Any], assessment: dict[str, Any], l10n: _L10n) -> str:
    """The identity line under the title."""
    sex = _SEX_FA.get(str(member["sex"]), str(member["sex"])) if l10n.persian else str(member["sex"])
    name = f"{member['first_name']} {member['last_name']}"
    return (
        f"{fa(name)} &nbsp;·&nbsp; {fa(sex)} &nbsp;·&nbsp; {l10n.age} "
        f"{assessment['age_years']} &nbsp;·&nbsp; {l10n.weight} {assessment['weight_kg']:.1f} kg"
    )


def _result_rows(
    assessment: dict[str, Any], brozek_pct: float, l10n: _L10n
) -> list[list[str]]:
    """The seven headline numbers. Values stay Latin numerals (they read fine)."""
    fm = assessment["fat_mass_kg"]
    lm = assessment["lean_mass_kg"]
    cls_raw = assessment["classification"] or ""
    cls = _CLASS_FA.get(cls_raw, cls_raw.title()) if l10n.persian else cls_raw.title()
    values = [
        f"{assessment['body_fat_pct']:.2f} %",
        f"{brozek_pct:.2f} %",
        f"{assessment['body_density']:.4f} g/cc",
        f"{fm:.2f} kg" if fm is not None else "—",
        f"{lm:.2f} kg" if lm is not None else "—",
        fa(cls) if l10n.persian else cls,
        f"{assessment['sum_mm']:.1f} mm",
    ]
    return [[label, value] for label, value in zip(l10n.rows(), values, strict=True)]


def _site_rows(assessment: dict[str, Any], l10n: _L10n) -> list[list[str]]:
    rows = [[l10n.site_col, "mm"]]
    for name, value in _parse_sites(assessment.get("sites_mm")):
        label = _SITE_FA.get(name, name.title())
        rows.append([fa(label) if l10n.persian else label, f"{value:.1f}"])
    return rows


def _history_rows(history: list[dict[str, Any]], l10n: _L10n) -> list[list[str]]:
    rows = [[l10n.date_col, l10n.bf_col, l10n.weight_col]]
    for row in history[:12]:
        rows.append([
            row["created_at"][:10],
            f"{row['body_fat_pct']:.2f}",
            f"{row['weight_kg']:.1f}",
        ])
    return rows


def _disclaimer(persian: bool) -> str:
    if persian:
        return fa(
            "برآورد بر پایهٔ معادلات جمعیت: جکسون و پولاک ۱۹۷۸، سیری ۱۹۶۱، بروزک ۱۹۶۳. "
            "تشخیص پزشکی نیست. به‌صورت آفلاین توسط ماسل پارادایز تولید شده است."
        )
    return (
        "Population equation estimate (Jackson &amp; Pollock 1978; Siri 1961; "
        "Brozek 1963). Not a medical diagnosis. Generated offline by Muscle Paradise."
    )


def _parse_sites(raw: Any) -> list[tuple[str, float]]:
    """Decode the stored sites JSON (kept as a JSON string in 0001_core)."""
    import json

    if not raw:
        return []
    if isinstance(raw, str):
        try:
            raw = json.loads(raw)
        except json.JSONDecodeError:
            return []
    if not isinstance(raw, dict):
        return []
    return [(k, float(v)) for k, v in raw.items()]


def _style_tables(story: list[Any], l10n: _L10n) -> None:
    base = TableStyle(
        [
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D8DEE6")),
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F1F5F9")),
            ("TEXTCOLOR", (0, 0), (-1, 0), INK),
            ("FONTNAME", (0, 0), (-1, -1), l10n.font),
            ("FONTNAME", (0, 0), (-1, 0), l10n.bold),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
            ("ALIGN", (0, 0), (-1, -1), "RIGHT" if l10n.persian else "LEFT"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F8FAFC")]),
            ("LEFTPADDING", (0, 0), (-1, -1), 6),
            ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ]
    )
    for element in story:
        if isinstance(element, Table):
            element.setStyle(base)
