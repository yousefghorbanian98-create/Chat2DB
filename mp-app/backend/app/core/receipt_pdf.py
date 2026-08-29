"""Cash/card receipt PDF (map §3 #11, DoD #6). Money is integer rials."""

from __future__ import annotations

import io
from typing import Any

from reportlab.lib import colors
from reportlab.lib.pagesizes import A5, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

EMERALD = colors.HexColor("#00B86A")
INK = colors.HexColor("#0B0F14")


def _rial(value: int) -> str:
    """Group thousands and append the Rial unit (map §16)."""
    return f"{value:,} Rial"


def build_receipt_pdf(
    *,
    gym_name: str,
    payment: dict[str, Any],
    member: dict[str, Any],
    package_name: str | None,
    compress: bool = True,
) -> bytes:
    """Render one payment to a compact A5 (landscape) receipt.

    ``compress=False`` leaves the text layer readable for tests.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A5), title="MP Receipt",
                            leftMargin=12 * mm, rightMargin=12 * mm,
                            topMargin=12 * mm, bottomMargin=12 * mm,
                            pageCompression=1 if compress else 0)

    title = ParagraphStyle("t", parent=getSampleStyleSheet()["Title"], textColor=EMERALD, spaceAfter=2)
    sub = ParagraphStyle("s", parent=getSampleStyleSheet()["Normal"], textColor=colors.grey, fontSize=9)

    voided = bool(payment.get("voided"))
    rows = [
        ["Receipt no", str(payment["receipt_no"])],
        ["Member", f"{member['first_name']} {member['last_name']}"],
        ["Package", package_name or "—"],
        ["Method", str(payment["method"]).upper()],
        ["Date", str(payment["created_at"])[:10]],
        ["Amount", _rial(int(payment["amount_rial"]))],
        ["Status", "VOIDED" if voided else "PAID"],
    ]

    story = [
        Paragraph(f"{gym_name} — Receipt", title),
        Paragraph("local-first gym OS", sub),
        Spacer(1, 4 * mm),
        Table(rows, colWidths=[35 * mm, 80 * mm]),
        Spacer(1, 4 * mm),
        Paragraph("Thank you. Keep this receipt for membership disputes.", sub),
    ]

    table = story[3]
    assert isinstance(table, Table)
    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D8DEE6")),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("TEXTCOLOR", (0, 0), (-1, -1), INK),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("TEXTCOLOR", (1, 5), (1, 5), EMERALD),
    ]))

    doc.build(story)
    return buffer.getvalue()
