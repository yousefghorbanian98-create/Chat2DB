"""Assessment PDF report (map §14 Phase 1: "PDF assessment report").

Built with reportlab. The report is rendered in **English** for now — reportlab
ships only Latin base fonts, and embedding Vazirmatn (OFL) for a proper Persian
PDF is a deliberate later step, not a silent mojibake workaround. All numbers
come from the stored assessment (server-computed, rule C6).
"""

from __future__ import annotations

import io
from typing import Any

from reportlab.lib import colors
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

EMERALD = colors.HexColor("#00B86A")
GOLD = colors.HexColor("#B8860B")  # printable gold on white paper
INK = colors.HexColor("#0B0F14")

_TITLE = ParagraphStyle(
    "mpTitle", parent=getSampleStyleSheet()["Title"], textColor=EMERALD, spaceAfter=2
)
_SUB = ParagraphStyle("mpSub", parent=getSampleStyleSheet()["Normal"], textColor=colors.grey, fontSize=9)
_H2 = ParagraphStyle("mpH2", parent=getSampleStyleSheet()["Heading2"], textColor=INK, spaceBefore=8)


def build_assessment_pdf(
    *,
    gym_name: str,
    member: dict[str, Any],
    assessment: dict[str, Any],
    brozek_pct: float,
    history: list[dict[str, Any]],
    compress: bool = True,
) -> bytes:
    """Render one assessment to PDF bytes.

    Args:
        gym_name: branding line.
        member: member row (first_name/last_name/sex/...).
        assessment: stored assessment row (siri is the primary equation).
        brozek_pct: the Brozek %BF computed for the same inputs (map: store both).
        history: newest-first rows for the trend table.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        title="Muscle Paradise — JP7 Assessment",
        leftMargin=18 * mm,
        rightMargin=18 * mm,
        topMargin=16 * mm,
        bottomMargin=16 * mm,
        pageCompression=1 if compress else 0,
    )

    story: list[Any] = [
        Paragraph("Muscle Paradise — Jackson–Pollock 7 Assessment", _TITLE),
        Paragraph(f"{gym_name} · local-first gym OS", _SUB),
        Spacer(1, 6 * mm),
        Paragraph(
            f"<b>{member['first_name']} {member['last_name']}</b> &nbsp;·&nbsp; "
            f"{member['sex']} &nbsp;·&nbsp; age {assessment['age_years']} &nbsp;·&nbsp; "
            f"weight {assessment['weight_kg']:.1f} kg",
            getSampleStyleSheet()["Normal"],
        ),
        Spacer(1, 4 * mm),
        Paragraph("Result", _H2),
    ]

    result_rows = [
        ["Body fat (Siri, primary)", f"{assessment['body_fat_pct']:.2f} %"],
        ["Body fat (Brozek)", f"{brozek_pct:.2f} %"],
        ["Body density", f"{assessment['body_density']:.4f} g/cc"],
        ["Fat mass", f"{assessment['fat_mass_kg']:.2f} kg" if assessment["fat_mass_kg"] is not None else "—"],
        ["Lean mass", f"{assessment['lean_mass_kg']:.2f} kg" if assessment["lean_mass_kg"] is not None else "—"],
        ["Classification", (assessment["classification"] or "—").title()],
        ["Sum of 7 skinfolds", f"{assessment['sum_mm']:.1f} mm"],
    ]
    story.append(
        Table(result_rows, colWidths=[70 * mm, 60 * mm]),
    )

    story.append(Paragraph("Measured skinfolds (mm)", _H2))
    site_rows = [["Site", "mm"]]
    sites = _parse_sites(assessment.get("sites_mm"))
    for name, value in sites:
        site_rows.append([name.title(), f"{value:.1f}"])
    story.append(Table(site_rows, colWidths=[60 * mm, 30 * mm]))

    if history:
        story.append(Paragraph("History (newest first)", _H2))
        hist_rows = [["Date", "BF% (Siri)", "Weight kg"]]
        for row in history[:12]:
            hist_rows.append([
                row["created_at"][:10],
                f"{row['body_fat_pct']:.2f}",
                f"{row['weight_kg']:.1f}",
            ])
        story.append(Table(hist_rows, colWidths=[45 * mm, 40 * mm, 40 * mm]))

    story.append(Spacer(1, 6 * mm))
    story.append(
        Paragraph(
            "Population equation estimate (Jackson &amp; Pollock 1978; Siri 1961; "
            "Brozek 1963). Not a medical diagnosis. Generated offline by Muscle "
            "Paradise.",
            _SUB,
        )
    )

    _style_tables(story)
    doc.build(story)
    return buffer.getvalue()


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


def _style_tables(story: list[Any]) -> None:
    base = TableStyle(
        [
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D8DEE6")),
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F1F5F9")),
            ("TEXTCOLOR", (0, 0), (-1, 0), INK),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("FONTSIZE", (0, 0), (-1, -1), 9),
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
