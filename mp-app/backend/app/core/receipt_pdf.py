"""Cash/card receipt PDF (map §3 #11, DoD #6). Money is integer rials.

Persian-first (map C10) with an English fallback, exactly like the assessment
report: shaping lives in ``app/core/persian`` so this module never touches a
font file or the bidi algorithm directly. Numbers stay Latin (rule C6).
"""

from __future__ import annotations

import io
from typing import Any

from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import A5, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from .persian import PERSIAN_FONT, fa, register_persian_font

EMERALD = colors.HexColor("#00B86A")
INK = colors.HexColor("#0B0F14")

_LATIN = "Helvetica"
_LATIN_BOLD = "Helvetica-Bold"

_METHOD_FA = {"cash": "نقد", "card": "کارت", "transfer": "کارت‌به‌کارت", "pos": "POS"}


def _rial(value: int, persian: bool = False) -> str:
    """Group thousands and append the Rial unit (map §16)."""
    return f"{value:,} Rial" if not persian else f"{fa('ریال')} {value:,}"


def _labels(persian: bool) -> dict[str, str]:
    """The receipt's label column, shaped when Persian."""
    s = fa if persian else (lambda x: x)
    if not persian:
        return {
            "receipt": "Receipt no", "member": "Member", "package": "Package",
            "method": "Method", "date": "Date", "amount": "Amount", "status": "Status",
            "paid": "PAID", "voided": "VOIDED",
        }
    return {
        "receipt": s("شماره رسید"), "member": s("عضو"), "package": s("بسته"),
        "method": s("روش"), "date": s("تاریخ"), "amount": s("مبلغ"), "status": s("وضعیت"),
        "paid": s("پرداخت شد"), "voided": s("باطل شد"),
    }


def build_receipt_pdf(
    *,
    gym_name: str,
    payment: dict[str, Any],
    member: dict[str, Any],
    package_name: str | None,
    compress: bool = True,
    persian: bool | None = None,
) -> bytes:
    """Render one payment to a compact A5 (landscape) receipt.

    ``compress=False`` leaves the text layer readable for tests. ``persian``
    defaults to "Persian when a font is registered", else English.
    """
    use_fa = (persian and register_persian_font()) if persian is not None else register_persian_font()
    lab = _labels(use_fa)
    font = PERSIAN_FONT if use_fa else _LATIN
    bold = PERSIAN_FONT if use_fa else _LATIN_BOLD
    align = TA_RIGHT if use_fa else 0

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A5), title="MP Receipt",
                            leftMargin=12 * mm, rightMargin=12 * mm,
                            topMargin=12 * mm, bottomMargin=12 * mm,
                            pageCompression=1 if compress else 0)

    title = ParagraphStyle("t", parent=getSampleStyleSheet()["Title"], textColor=EMERALD,
                           spaceAfter=2, fontName=bold, alignment=align)
    sub = ParagraphStyle("s", parent=getSampleStyleSheet()["Normal"], textColor=colors.grey,
                         fontSize=9, fontName=font, alignment=align)

    voided = bool(payment.get("voided"))
    method = _METHOD_FA.get(str(payment["method"]), str(payment["method"]).upper())
    method = fa(method) if use_fa else str(payment["method"]).upper()
    rows = [
        [lab["receipt"], str(payment["receipt_no"])],
        [lab["member"], fa(f"{member['first_name']} {member['last_name']}") if use_fa
         else f"{member['first_name']} {member['last_name']}"],
        [lab["package"], fa(package_name) if use_fa and package_name else (package_name or "—")],
        [lab["method"], method],
        [lab["date"], str(payment["created_at"])[:10]],
        [lab["amount"], _rial(int(payment["amount_rial"]), use_fa)],
        [lab["status"], lab["voided"] if voided else lab["paid"]],
    ]

    brand = fa(f"{gym_name} — رسید") if use_fa else f"{gym_name} — Receipt"
    tagline = fa("سیستم‌عامل محلی باشگاه") if use_fa else "local-first gym OS"
    thanks = (
        fa("سپاس. این رسید را برای پیگیری عضویت نگه دارید.")
        if use_fa else "Thank you. Keep this receipt for membership disputes."
    )

    story = [
        Paragraph(brand, title),
        Paragraph(tagline, sub),
        Spacer(1, 4 * mm),
        Table(rows, colWidths=[35 * mm, 80 * mm]),
        Spacer(1, 4 * mm),
        Paragraph(thanks, sub),
    ]

    table = story[3]
    assert isinstance(table, Table)
    table.setStyle(TableStyle([
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D8DEE6")),
        ("FONTNAME", (0, 0), (-1, -1), font),
        ("FONTNAME", (0, 0), (0, -1), bold),
        ("ALIGN", (0, 0), (-1, -1), "RIGHT" if use_fa else "LEFT"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("TEXTCOLOR", (0, 0), (-1, -1), INK),
        ("LEFTPADDING", (0, 0), (-1, -1), 6),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
        ("TEXTCOLOR", (1, 5), (1, 5), EMERALD),
    ]))

    doc.build(story)
    return buffer.getvalue()
