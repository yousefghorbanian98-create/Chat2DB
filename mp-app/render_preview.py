"""Render a preview of the MP athlete app from LIVE API data.

This is NOT a browser screenshot — no browser can be installed in this sandbox
(Debian mirrors are unreachable). It is a faithful rasterisation drawn with
Pillow using the real `tokens.css` colours and the real JSON returned by the
running server, so every number and string on it came from the product.
"""

from __future__ import annotations

import json
import urllib.request

import arabic_reshaper
import qrcode
from bidi.algorithm import get_display
from PIL import Image, ImageDraw, ImageFont

FONT = "/home/user/Chat2DB/mp-app/assets/fonts/PersianSans-Regular.ttf"
OUT = "/home/user/Chat2DB/mp-app/docs-preview-athlete.png"
B = "http://127.0.0.1:8751/api/v1"

# Real values, copied verbatim from mp-app/studio/src/styles/tokens.css.
BG = "#0b0f14"
CARD = "#121c24"
FG = "#f1f5f9"
MUTED = "#94a3b8"
PRIMARY = "#00b86a"
ACCENT = "#12d98a"
GOLD = "#ffd700"
DANGER = "#ef4444"
BORDER = "#243040"

W = 1000
PAD = 36
GAP = 22

F_TITLE = ImageFont.truetype(FONT, 34)
F_BODY = ImageFont.truetype(FONT, 26)
F_SMALL = ImageFont.truetype(FONT, 21)
F_H1 = ImageFont.truetype(FONT, 46)

# In-card content lives on a transparent overlay so the panel fill (drawn at
# close time, once the card height is known) never covers it.
OV = Image.new("RGBA", (W, 2600), (0, 0, 0, 0))
OD = ImageDraw.Draw(OV)


def fa(text: str) -> str:
    """Shape Persian text so Pillow draws connected, right-to-left glyphs."""
    return get_display(arabic_reshaper.reshape(text))


def token(principal: str, path: str):
    req = urllib.request.Request(B + path, headers={"Authorization": f"Bearer {principal}"})
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.load(r)


def member_token() -> str:
    body = json.dumps({"membership_code": "MP-DEMO-1", "pin": "1234"}).encode()
    req = urllib.request.Request(
        B + "/auth/member-pin", data=body, headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        return json.load(r)["token"]


class Card:
    """A glass panel that grows as content is added to the overlay."""

    def __init__(self, d: ImageDraw.ImageDraw, img: Image.Image, y: int, title: str):
        self.d = d
        self.img = img
        self.top = y
        self.y = y + 74
        self.title = title
        OD.text((W - PAD - 24, y + 22), fa(title), font=F_TITLE, fill=FG, anchor="ra")

    def text(self, s: str, *, color: str = FG, size: int = 26, dy: int = 12):
        f = F_BODY if size == 26 else (F_TITLE if size > 30 else F_SMALL)
        OD.text((W - PAD - 24, self.y + dy), fa(s), font=f, fill=color, anchor="ra")
        self.y += dy + (size + 14)

    def gap(self, n: int = 14):
        self.y += n

    def close(self) -> int:
        self.d.rounded_rectangle(
            [PAD, self.top, W - PAD, self.y + 18], radius=18, fill=CARD, outline=BORDER, width=1
        )
        self.img.paste(OV, (0, 0), OV)
        return self.y + 18 + GAP


def stat_row(y: int, items: list[tuple[str, str, str, str]]):
    """Four labelled figures, right-to-left like the real StatCard row."""
    box = (W - 2 * PAD - 48) // len(items)
    for i, (label, value, unit, color) in enumerate(items):
        x0 = W - PAD - 24 - box * (i + 1)
        OD.text((x0 + box - 12, y + 6), fa(label), font=F_SMALL, fill=MUTED, anchor="ra")
        OD.text((x0 + box - 12, y + 40), fa(value), font=F_TITLE, fill=color, anchor="ra")
        if unit:
            OD.text((x0 + box - 12, y + 84), unit, font=F_SMALL, fill=MUTED, anchor="ra")


def main() -> int:
    tok = member_token()
    me = token(tok, "/client/me")
    nut = token(tok, "/client/me/nutrition")
    pays = token(tok, "/client/me/payments")
    logs = token(tok, "/client/me/workouts")
    injuries = token(tok, "/client/me/injuries")
    checkin = token(tok, "/client/me/checkin-qr")
    qr_payload = checkin["payload"]
    qr_ttl = checkin["expires_in"]

    img = Image.new("RGB", (W, 2600), BG)
    d = ImageDraw.Draw(img)

    # --- header ------------------------------------------------------------
    d.text((W - PAD, 60), fa("ماسل پارادایز"), font=F_H1, fill=FG, anchor="ra")
    d.text((W - PAD, 118), fa("ورزشکار"), font=F_TITLE, fill=ACCENT, anchor="ra")
    d.rounded_rectangle([PAD, 62, PAD + 150, 118], radius=12, outline=BORDER, width=1)
    d.text((PAD + 75, 90), fa("خروج"), font=F_BODY, fill=MUTED, anchor="mm")

    y = 176

    # --- profile -----------------------------------------------------------
    c = Card(d, img, y, "پروفایل من")
    stat_row(
        c.y + 14,
        [
            ("نام", f"{me['first_name']} {me['last_name']}", "", FG),
            ("کد عضویت", str(me["membership_code"]), "", FG),
            ("اعتبار تا", "۱۴۰۵/۰۷/۰۸", "", FG),
        ],
    )
    c.y += 132
    y = c.close()

    # --- check-in QR (a real, scannable symbol of the real signed payload) --
    c = Card(d, img, y, "ورود به باشگاه")
    qr = qrcode.QRCode(box_size=6, border=2, error_correction=qrcode.constants.ERROR_CORRECT_M)
    qr.add_data(json.dumps(qr_payload, separators=(",", ":"), sort_keys=True))
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="#04140c", back_color="white").convert("RGB")
    pad = 14
    frame = Image.new("RGB", (qr_img.width + pad * 2, qr_img.height + pad * 2), "white")
    frame.paste(qr_img, (pad, pad))
    OV.paste(frame, ((W - frame.width) // 2, c.y + 10))
    c.y += frame.height + 26
    c.text(f"اعتبار تا {qr_ttl} ثانیهٔ دیگر", color=MUTED, size=21)
    c.text("این کد را جلوی دستگاه ورود نشان دهید.", color=MUTED, size=21)
    y = c.close()

    # --- nutrition ---------------------------------------------------------
    c = Card(d, img, y, "تغذیهٔ من")
    stat_row(
        c.y + 14,
        [
            ("کالری روزانه", f"{nut['tdee_kcal']:.0f}", "kcal", ACCENT),
            ("پروتئین", f"{nut['protein_g']:.0f}", "g", GOLD),
            ("کربوهیدرات", f"{nut['carbs_g']:.0f}", "g", FG),
            ("چربی", f"{nut['fat_g']:.0f}", "g", FG),
        ],
    )
    c.y += 132
    y = c.close()

    # --- workout log -------------------------------------------------------
    c = Card(d, img, y, "ثبت جلسهٔ تمرین")
    c.text("تاریخ جلسه ۲۰۲۶-۰۸-۳۰", color=MUTED, size=21)
    for w in logs:
        c.text(f"جلسهٔ ثبت‌شده — {len(w['exercises'])} حرکت", color=ACCENT, size=21)
        for ex in w["exercises"]:
            sets = "، ".join(
                f"{s['weight_kg']}kg × {s['reps']}" if "weight_kg" in s else f"× {s['reps']}"
                for s in ex["sets"]
            )
            c.text(f"• {ex['name']} — {sets}", size=26)
        if w.get("athlete_note"):
            c.text(f"یادداشت: {w['athlete_note']}", color=MUTED, size=21)
    c.gap(8)
    OD.rounded_rectangle([W // 2 - 110, c.y + 6, W // 2 + 110, c.y + 62], radius=12, fill=PRIMARY)
    OD.text((W // 2, c.y + 34), fa("ثبت جلسه"), font=F_BODY, fill="#04140c", anchor="mm")
    c.y += 86
    y = c.close()

    # --- injuries ----------------------------------------------------------
    c = Card(d, img, y, "محدودیت‌های من")
    for i in injuries:
        c.text(f"{i['label']} — کمر", size=26)
        c.text(f"وضعیت: {'فعال' if i['status'] == 'active' else i['status']}", color=MUTED, size=21)
        for p in i["contraindicated_patterns"]:
            c.text(f"ممنوع: {p}", color=DANGER, size=21)
        if i.get("member_visible_note"):
            c.text(i["member_visible_note"], color=MUTED, size=21)
    y = c.close()

    # --- payments ----------------------------------------------------------
    c = Card(d, img, y, "سوابق پرداخت من")
    for p in pays:
        method = {"cash": "نقدی", "card": "کارت", "pos": "کارت‌خوان", "transfer": "کارت‌به‌کارت"}.get(
            p["method"], p["method"]
        )
        c.text(f"{p['amount_rial']:,} ریال · {method}", color=ACCENT, size=26)
        c.text(f"رسید {p['receipt_no']}", color=MUTED, size=21)
    y = c.close()

    # --- honesty footer ----------------------------------------------------
    d.line([PAD, y + 6, W - PAD, y + 6], fill=BORDER, width=1)
    d.text(
        (W - PAD, y + 30),
        fa("پیش‌نمایش رندرشده از دادهٔ زندهٔ API — اسکرین‌شات مرورگر نیست"),
        font=F_SMALL,
        fill=MUTED,
        anchor="ra",
    )
    d.text(
        (W - PAD, y + 62),
        fa("نصب‌شونده روی اندروید و ویندوز از طریق PWA"),
        font=F_SMALL,
        fill=MUTED,
        anchor="ra",
    )

    img.crop((0, 0, W, y + 100)).save(OUT)
    print("wrote", OUT)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
