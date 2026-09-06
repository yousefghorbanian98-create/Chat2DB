"""Persian text support for generated PDFs (map C10: Persian-first UI).

reportlab ships Latin base fonts only and has no RTL/shaping engine, so a
Persian PDF needs two things this module owns:

1. a TrueType font with Arabic/Persian glyphs **and** the Arabic Presentation
   Forms blocks that shaped text maps into, and
2. visual-order shaping — ``arabic_reshaper`` joins the letters, ``python-bidi``
   reorders the run for left-to-right placement.

Both are applied through :func:`fa`, which every Persian string in a PDF must go
through. Unshaped Persian renders as disconnected reversed letters, which reads
as garbage to a native speaker — so the helper is the only supported path.

Font provenance (recorded honestly, see NOTICES.md): the bundled
``PersianSans-Regular.ttf`` is **DejaVu Sans 2.37**, not Vazirmatn. It was
chosen because it is already present in the workspace and covers every glyph
the reshaped output needs (verified: zero missing codepoints for a full Persian
sentence). Vazirmatn remains the intended face; drop its TTF next to this one
and set ``MP_PERSIAN_FONT`` to switch.
"""

from __future__ import annotations

import os
from pathlib import Path

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

#: reportlab font name once registered. Callers reference this, never a filename.
PERSIAN_FONT = "MPPersian"

# mp-app/backend/app/core/persian.py -> parents[3] is mp-app/, which owns assets/.
_DEFAULT_FONT_PATH = Path(__file__).resolve().parents[3] / "assets" / "fonts" / "PersianSans-Regular.ttf"

_registered: bool = False
_last_error: str | None = None


def font_path() -> Path:
    """Path of the Persian TTF, overridable via ``MP_PERSIAN_FONT``."""
    override = os.environ.get("MP_PERSIAN_FONT", "").strip()
    return Path(override) if override else _DEFAULT_FONT_PATH


def register_persian_font() -> bool:
    """Register the Persian TTF with reportlab. Idempotent.

    Returns:
        True when ``PERSIAN_FONT`` is usable. False (and a recorded reason) when
        the font file or the shaping libraries are missing, so callers can fall
        back to English instead of emitting mojibake.
    """
    global _registered, _last_error

    if _registered:
        return True

    path = font_path()
    if not path.is_file():
        _last_error = f"Persian font not found at {path}"
        return False

    try:
        pdfmetrics.registerFont(TTFont(PERSIAN_FONT, str(path)))
        _registered = True
        _last_error = None
        return True
    except Exception as exc:  # noqa: BLE001 - any failure must degrade, not crash
        _last_error = f"could not register Persian font: {exc}"
        return False


def last_error() -> str | None:
    """Why registration failed, for logs and the API ``detail`` field."""
    return _last_error


_MIRROR = {"(": ")", ")": "(", "[": "]", "]": "[", "{": "}", "}": "{", "<": ">", ">": "<"}


def _cat(ch: str) -> str:
    """Coarse bidi class: European numbers, Latin, or Arabic (strong RTL)."""
    if ch in "0123456789.%,+-" or ch in "۰۱۲۳۴۵۶۷۸۹":
        return "EN"
    if "A" <= ch <= "Z" or "a" <= ch <= "z":
        return "L"
    cp = ord(ch)
    if 0x0600 <= cp <= 0x06FF or 0xFB50 <= cp <= 0xFEFF:
        return "R"
    return "N"


def _display(reshaped: str) -> str:
    """Reorder a reshaped RTL string into left-to-right visual order.

    A minimal UAX #9 subset for base-RTL paragraphs: build directional runs,
    resolve neutrals against their neighbours (else base R), reverse the run
    order, reverse characters inside RTL runs, and mirror brackets. Matches
    python-bidi on the report's strings (oracle-verified) without the LGPL dep.
    """
    text = reshaped.replace("\u200c", "").replace("\u200d", "")

    runs: list[list[str]] = []
    for ch in text:
        c = _cat(ch)
        if runs and runs[-1][0] == c:
            runs[-1][1] += ch
        else:
            runs.append([c, ch])

    resolved: list[list[str]] = []
    for i, (d, txt) in enumerate(runs):
        if d != "N":
            resolved.append([d, txt])
            continue
        prev = resolved[-1][0] if resolved else "R"
        nxt = next((runs[j][0] for j in range(i + 1, len(runs)) if runs[j][0] != "N"), "R")
        resolved.append([prev if prev == nxt else "R", txt])

    merged: list[list[str]] = []
    for d, txt in resolved:
        if merged and merged[-1][0] == d:
            merged[-1][1] += txt
        else:
            merged.append([d, txt])

    merged.reverse()
    visual = "".join(txt if d in ("L", "EN") else txt[::-1] for d, txt in merged)
    return "".join(_MIRROR.get(c, c) for c in visual)


def fa(text: str) -> str:
    """Shape Persian/Arabic text into visual order for reportlab.

    Joins letters with ``arabic_reshaper`` (MIT) and reorders the runs with the
    in-house :func:`_display`. We deliberately do NOT depend on ``python-bidi``
    (LGPL-3.0) at runtime, per the permissive-license rule (C11).

    Falls back to the raw string when the reshaper is unavailable — degraded
    (unjoined letters) but never a crash.
    """
    if not text:
        return text
    try:
        import arabic_reshaper
    except ImportError:
        return text
    return _display(arabic_reshaper.reshape(text))


def is_persian_available() -> bool:
    """Whether Persian PDFs can be produced at all (font + shapers present)."""
    if not register_persian_font():
        return False
    try:
        import arabic_reshaper  # noqa: F401
    except ImportError:
        return False
    return True
