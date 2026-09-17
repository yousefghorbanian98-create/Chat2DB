#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
پیاده‌سازی عقب‌نشینی‌های «دستور نقشه» روی زمین واقعی و نمایش مساحت باقیمانده
روی تصویر هوایی واقعی (Esri World Imagery, z19 — ژئورفرنس‌شده).

ورودی‌ها (از متن استخراج‌شدهٔ دستور نقشه + بازسازی کاداسترِ جلسهٔ قبل):
  AREA_DEED  = 1293.95 m²   مساحت عرصه طبق سند
  AREA_NET   = 642.28  m²   مساحت زمین پس از رعایت برِ اصلاحی
  SETBACK_N  = 8.0 m        عقب‌نشینی شمالی (گذر ۸ متری مطابق طرح مصوب)
  عقب‌نشینی شرق (گذر با عرض متغیر ۲۶–۲۹ متر) و جنوب (حریم دکل برق) مجهول است
  → با فرضِ عمقِ برابر برای شرق و جنوب، عددی حل می‌شود.

خروجی: docs/arch/remaining-area-aerial.png
"""
import json, math, os
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display

# ------------------------------------------------------------------ ورودی‌ها
LAT0, LON0 = 32.630676, 51.723828          # پین اعلامی کارفرما
AREA_DEED, AREA_NET = 1293.95, 642.28
SETBACK_N = 8.0

# بازسازی کاداستر (متر از گوشهٔ SW) — از جلسهٔ قبل، مساحتِ مبنا ۵۹۹.۹۷ m²
BASE = [(0, 0), (27.93, 0), (32.44, 9.01), (32.44, 19.37), (4.50, 19.37), (0, 15.77)]

GEO = "/tmp/oldgeo"
HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT = os.path.join(HERE, "docs", "arch", "remaining-area-aerial.png")
FONTS = "/home/user/fonts"

# ------------------------------------------------------------------ هندسه
def area(p):
    s = 0.0
    for i in range(len(p)):
        x1, y1 = p[i]
        x2, y2 = p[(i + 1) % len(p)]
        s += x1 * y2 - x2 * y1
    return abs(s) / 2.0


def centroid(p):
    a = cx = cy = 0.0
    for i in range(len(p)):
        x1, y1 = p[i]
        x2, y2 = p[(i + 1) % len(p)]
        f = x1 * y2 - x2 * y1
        a += f
        cx += (x1 + x2) * f
        cy += (y1 + y2) * f
    a *= 0.5
    return cx / (6 * a), cy / (6 * a), abs(a)


def clip(poly, inside, interp):
    """Sutherland–Hodgman با یک نیم‌صفحه"""
    out = []
    n = len(poly)
    for i in range(n):
        a, b = poly[i], poly[(i + 1) % n]
        ia, ib = inside(a), inside(b)
        if ia:
            out.append(a)
            if not ib:
                out.append(interp(a, b))
        elif ib:
            out.append(interp(a, b))
    return out


def apply_setbacks(poly, n=0.0, e=0.0, s=0.0, w=0.0):
    xs = [p[0] for p in poly]
    ys = [p[1] for p in poly]
    xmin, xmax, ymin, ymax = min(xs), max(xs), min(ys), max(ys)
    p = poly
    if n > 0:
        y = ymax - n
        p = clip(p, lambda q: q[1] <= y,
                 lambda a, b: (a[0] + (b[0] - a[0]) * (y - a[1]) / (b[1] - a[1]), y))
    if s > 0:
        y = ymin + s
        p = clip(p, lambda q: q[1] >= y,
                 lambda a, b: (a[0] + (b[0] - a[0]) * (y - a[1]) / (b[1] - a[1]), y))
    if e > 0:
        x = xmax - e
        p = clip(p, lambda q: q[0] <= x,
                 lambda a, b: (x, a[1] + (b[1] - a[1]) * (x - a[0]) / (b[0] - a[0])))
    if w > 0:
        x = xmin + w
        p = clip(p, lambda q: q[0] >= x,
                 lambda a, b: (x, a[1] + (b[1] - a[1]) * (x - a[0]) / (b[0] - a[0])))
    return p


# مقیاسِ کاداستر به مساحتِ سند
k = math.sqrt(AREA_DEED / area(BASE))
GROSS = [(x * k, y * k) for x, y in BASE]

# حلِ عددیِ عمق عقب‌نشینیِ شرق/جنوب طوری که مساحت خالص = AREA_NET
lo, hi = 0.0, 30.0
for _ in range(80):
    mid = (lo + hi) / 2
    a = area(apply_setbacks(GROSS, n=SETBACK_N, e=mid, s=mid))
    if a > AREA_NET:
        lo = mid
    else:
        hi = mid
X_ES = (lo + hi) / 2
NET = apply_setbacks(GROSS, n=SETBACK_N, e=X_ES, s=X_ES)
A_GROSS = area(GROSS)
A_NET = area(NET)
LOST = A_GROSS - A_NET

cx, cy, _ = centroid(GROSS)
LAT_M = 1.0 / 110574.0
LON_M = 1.0 / (111320.0 * math.cos(math.radians(LAT0)))
ANCHOR_LAT = LAT0 - cy * LAT_M          # طوری که مرکز زمین روی پین باشد
ANCHOR_LON = LON0 - cx * LON_M


def local2geo(x, y):
    return ANCHOR_LAT + y * LAT_M, ANCHOR_LON + x * LON_M


# ------------------------------------------------------------------ تصویر هوایی
meta = json.load(open(os.path.join(GEO, "meta.json")))
z = meta["zooms"]["19"]
im = Image.open(os.path.join(GEO, z["file"])).convert("RGB")
IW, IH = im.size
W, N, S, E = z["west"], z["north"], z["south"], z["east"]


def geo2px(lat, lon):
    return ((lon - W) / (E - W) * IW, (N - lat) / (N - S) * IH)


MPPX = (E - W) * 111320 * math.cos(math.radians(LAT0)) / IW     # متر بر پیکسل
MARGIN = 32.0                                                   # متر حاشیه
gl = [local2geo(x, y) for x, y in GROSS]
pxx = [geo2px(a, b)[0] for a, b in gl]
pxy = [geo2px(a, b)[1] for a, b in gl]
mp = MARGIN / MPPX
box = (max(0, int(min(pxx) - mp)), max(0, int(min(pxy) - mp)),
       min(IW, int(max(pxx) + mp)), min(IH, int(max(pxy) + mp)))
crop = im.crop(box)
SC = min(3.0, 2400 / max(crop.size))
canvas = crop.resize((int(crop.width * SC), int(crop.height * SC)), Image.LANCZOS).convert("RGBA")
OW, OH = canvas.size
dr = ImageDraw.Draw(canvas)


def to_canvas(lat, lon):
    x, y = geo2px(lat, lon)
    return ((x - box[0]) * SC, (y - box[1]) * SC)


def P(x, y):
    return to_canvas(*local2geo(x, y))


# ------------------------------------------------------------------ متن فارسی
PERSIAN_DIGITS = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")


def fa(t):
    t = str(t).translate(PERSIAN_DIGITS)
    return get_display(arabic_reshaper.reshape(t))


def F(size, bold=False):
    return ImageFont.truetype(
        os.path.join(FONTS, "Vazirmatn-Bold.ttf" if bold else "Vazirmatn-Regular.ttf"), size)


def text(xy, t, size=30, fill=(255, 255, 255, 255), bold=False, anchor="mm",
         stroke=(0, 0, 0, 220), sw=4, box_fill=None, pad=(10, 6), max_w=None,
         bounds=None):
    """max_w: اگر عرضِ متن از این مقدار بیشتر شد، اندازهٔ فونت خودکار کوچک می‌شود."""
    x, y = xy
    f = F(size, bold)
    t = fa(t)
    if max_w:
        while True:
            b = dr.textbbox((0, 0), t, font=f, stroke_width=sw)
            if b[2] - b[0] <= max_w or size <= 12:
                break
            size -= 2
            f = F(size, bold)
    b = dr.textbbox((x, y), t, font=f, anchor=anchor, stroke_width=sw)
    if bounds:
        bw, bh = b[2] - b[0], b[3] - b[1]
        x = min(max(x, bw / 2 + 8), bounds[0] - bw / 2 - 8)
        y = min(max(y, bh / 2 + 8), bounds[1] - bh / 2 - 8)
        b = dr.textbbox((x, y), t, font=f, anchor=anchor, stroke_width=sw)
    if box_fill is not None:
        dr.rectangle([b[0] - pad[0], b[1] - pad[1], b[2] + pad[0], b[3] + pad[1]], fill=box_fill)
    dr.text((x, y), t, font=f, fill=fill, anchor=anchor, stroke_width=sw, stroke_fill=stroke)


def dashed(p1, p2, dash=14, gap=9, fill=(255, 240, 60, 255), w=4):
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    d = math.hypot(dx, dy)
    if d < 1:
        return
    n = int(d // (dash + gap)) + 1
    for i in range(n):
        t0 = i * (dash + gap) / d
        t1 = min((i * (dash + gap) + dash) / d, 1.0)
        dr.line([(p1[0] + dx * t0, p1[1] + dy * t0), (p1[0] + dx * t1, p1[1] + dy * t1)],
                fill=fill, width=w)


def hatch(poly, color=(225, 60, 60, 255), spacing=16, w=3, alpha_mask=150, sub=None):
    """sub: ماسکِ ناحیه‌ای که باید از هاشور حذف شود (مثلاً مساحت خالص)."""
    from PIL import ImageChops
    m = Image.new("L", (OW, OH), 0)
    ImageDraw.Draw(m).polygon([tuple(map(int, p)) for p in poly], fill=alpha_mask)
    if sub is not None:
        m2 = Image.new("L", (OW, OH), 0)
        ImageDraw.Draw(m2).polygon([tuple(map(int, p)) for p in sub], fill=alpha_mask)
        m = ImageChops.subtract(m, m2)
    h = Image.new("L", (OW, OH), 0)
    hd = ImageDraw.Draw(h)
    x0 = int(min(p[0] for p in poly)) - OH
    x1 = int(max(p[0] for p in poly)) + OH
    for x in range(x0, x1, spacing):
        hd.line([(x, 0), (x + OH, OH)], fill=255, width=w)
    mask = ImageChops.multiply(m, h)
    canvas.paste(Image.new("RGBA", (OW, OH), color), (0, 0), mask)


def fillring(outer, inner, color, alpha=70):
    """رنگِ نیمه‌شفاف فقط در ناحیهٔ بین دو چندضلعی (نوار عقب‌نشینی)"""
    from PIL import ImageChops
    m1 = Image.new("L", (OW, OH), 0)
    ImageDraw.Draw(m1).polygon([tuple(map(int, p)) for p in outer], fill=alpha)
    m2 = Image.new("L", (OW, OH), 0)
    ImageDraw.Draw(m2).polygon([tuple(map(int, p)) for p in inner], fill=alpha)
    canvas.paste(Image.new("RGBA", (OW, OH), color), (0, 0), ImageChops.subtract(m1, m2))


def fillpoly(poly, color, alpha=95):
    m = Image.new("L", (OW, OH), 0)
    ImageDraw.Draw(m).polygon([tuple(map(int, p)) for p in poly], fill=alpha)
    canvas.paste(Image.new("RGBA", (OW, OH), color), (0, 0), m)


# ------------------------------------------------------------------ ترسیم
GP = [P(x, y) for x, y in GROSS]
NP = [P(x, y) for x, y in NET]

# شبکه معابر OSM
try:
    osm = json.load(open(os.path.join(GEO, "overpass.json")))
    for e in osm.get("elements", []):
        tags = e.get("tags", {})
        if "highway" not in tags:
            continue
        hw = tags["highway"]
        pts = [to_canvas(g["lat"], g["lon"]) for g in e.get("geometry", [])]
        if len(pts) < 2:
            continue
        wdt = {"secondary": 11, "secondary_link": 8, "residential": 5, "track": 3}.get(hw, 4)
        dr.line(pts, fill=(255, 250, 225, 70), width=int(wdt * SC * 0.55))
        nm = tags.get("name")
        if nm and (hw.startswith("secondary") or nm in ("مجید منصوری", "بهار", "مهران")):
            for i in range(len(pts) - 1):
                if 0 < pts[i][0] < OW and 0 < pts[i][1] < OH:
                    text(pts[i], nm, size=22, fill=(255, 245, 200, 235), box_fill=(20, 20, 20, 150))
                    break
except Exception:
    pass

# نوارِ عقب‌نشینی (عرصهٔ سند منهای خالص): زمینهٔ قرمز + هاشور
fillring(GP, NP, (215, 35, 35), alpha=80)
hatch(GP, color=(235, 45, 45, 255), spacing=22, w=6, alpha_mask=215, sub=NP)
# مرز عرصهٔ سند: کادر زرد
dr.polygon([tuple(map(int, p)) for p in GP], outline=(255, 214, 40, 255), width=8)

# مساحتِ باقیمانده (قابل ساخت): سبز
fillpoly(NP, (30, 185, 85), alpha=175)
dr.polygon([tuple(map(int, p)) for p in NP], outline=(40, 255, 120, 255), width=6)
for p1, p2 in zip(NP, NP[1:] + [NP[0]]):
    dashed(p1, p2, fill=(220, 255, 220, 200), w=3)

# ابعادِ عقب‌نشینی روی هر ضلع
xs = [p[0] for p in GROSS]; ys = [p[1] for p in GROSS]
ymax, xmax, ymin = max(ys), max(xs), min(ys)
mid_n = P((min(xs) + max(xs)) / 2, ymax)
mid_n_in = P((min(xs) + max(xs)) / 2, ymax - SETBACK_N)
dr.line([mid_n, mid_n_in], fill=(255, 90, 90, 255), width=5)
text(((mid_n[0] + mid_n_in[0]) / 2 + 66, (mid_n[1] + mid_n_in[1]) / 2),
     f"عقب‌نشینی شمالی {SETBACK_N:g} متر (گذر ۸ متری)", size=26, fill=(255, 220, 220, 255),
     box_fill=(120, 20, 20, 210), max_w=OW * 0.5, bounds=(OW, OH))

mid_e = P(xmax, (min(ys) + max(ys)) / 2)
mid_e_in = P(xmax - X_ES, (min(ys) + max(ys)) / 2)
dr.line([mid_e, mid_e_in], fill=(255, 90, 90, 255), width=5)
text((mid_e[0] + 118, mid_e[1]), f"عقب‌نشینی شرقی {X_ES:.1f} متر\n(گذر متغیر ۲۶–۲۹ متر)", size=26,
     fill=(255, 220, 220, 255), box_fill=(120, 20, 20, 210), max_w=OW * 0.32, bounds=(OW, OH))

mid_s = P((min(xs) + max(xs)) / 2, ymin)
mid_s_in = P((min(xs) + max(xs)) / 2, ymin + X_ES)
dr.line([mid_s, mid_s_in], fill=(255, 90, 90, 255), width=5)
text((mid_s[0] - 130, mid_s[1] + 40), f"عقب‌نشینی جنوبی {X_ES:.1f} متر\n(حریم دکل فشار قوی)", size=26,
     fill=(255, 220, 220, 255), box_fill=(120, 20, 20, 210), max_w=OW * 0.32, bounds=(OW, OH))

# پین کارفرما
pin = to_canvas(LAT0, LON0)
r = 13
dr.ellipse([pin[0] - r, pin[1] - r, pin[0] + r, pin[1] + r],
           fill=(40, 130, 255, 255), outline=(255, 255, 255, 255), width=4)
text((pin[0] + 110, pin[1] - 30), "پین شما: ۳۲٫۶۳۰۶۷۶ , ۵۱٫۷۲۳۸۲۸", size=24,
     fill=(255, 255, 255, 255), box_fill=(15, 60, 140, 220), max_w=OW * 0.34, bounds=(OW, OH))

# برچسبِ مساحت خالص در مرکز
cnet = centroid(NET)[:2]
cp = P(*cnet)
text(cp, f"{A_NET:,.2f} m²", size=58, bold=True, fill=(255, 255, 255, 255),
     box_fill=(10, 90, 40, 225), stroke=(0, 40, 10, 255), sw=5)
text((cp[0], cp[1] + 52), "مساحت باقیمانده (قابل ساخت)", size=28, fill=(225, 255, 225, 255),
     box_fill=(10, 90, 40, 210))
text((cp[0], cp[1] + 90), f"{A_NET / A_GROSS * 100:.1f}٪ از عرصهٔ سند", size=24,
     fill=(210, 255, 215, 255), box_fill=(10, 80, 35, 200))
nx_ = [p[0] for p in NET]; ny_ = [p[1] for p in NET]
text((cp[0], cp[1] + 132),
     f"ابعاد خالص ≈ {max(nx_) - min(nx_):.1f} × {max(ny_) - min(ny_):.1f} متر", size=23,
     fill=(200, 250, 210, 255), box_fill=(10, 80, 35, 200), max_w=OW * 0.5)

# ------------------------------------------------------------------ حاشیه‌ها
HDR = 96
FTR = 132
final = Image.new("RGBA", (OW, OH + HDR + FTR), (12, 16, 24, 255))
final.paste(canvas, (0, HDR))
d2 = ImageDraw.Draw(final)
dr = d2


def T(*a, **kw):
    text(*a, **kw)


T((OW / 2, 38), "پیاده‌سازی اصلاحیِ دستور نقشه روی زمین واقعی — تصویر هوایی واقعی",
  size=36, bold=True, fill=(255, 255, 255, 255), box_fill=None, stroke=(0, 0, 0, 255), sw=5,
  max_w=OW - 60)
T((OW / 2, 76), "مشتاق دوم، خیابان باغ مشهد، کوی منصور — شهرداری اصفهان، منطقهٔ ۴",
  size=25, fill=(215, 225, 245, 255), box_fill=None, max_w=OW - 60)

# راهنما
lx, ly = 26, OH + HDR + 22
d2.rectangle([lx - 8, ly - 8, lx + 690, ly + 106], fill=(22, 28, 40, 235), outline=(80, 95, 125, 255), width=2)
d2.rectangle([lx, ly + 6, lx + 30, ly + 32], fill=(40, 190, 90, 190), outline=(60, 255, 130, 255), width=2)
T((lx + 44, ly + 19), f"مساحت باقیمانده پس از عقب‌نشینی: {A_NET:,.2f} مترمربع", size=25,
  fill=(235, 255, 240, 255), anchor="lm", box_fill=None, stroke=(0, 0, 0, 200), sw=3,
  max_w=OW * 0.45)
d2.rectangle([lx, ly + 48, lx + 30, ly + 74], fill=(230, 55, 55, 200), outline=(255, 214, 40, 255), width=2)
T((lx + 44, ly + 61), f"عرصهٔ طبق سند: {A_GROSS:,.2f} مترمربع — بخشِ حذف‌شده: {LOST:,.2f} مترمربع",
  size=25, fill=(255, 235, 235, 255), anchor="lm", box_fill=None, stroke=(0, 0, 0, 200), sw=3,
  max_w=OW * 0.5)
T((OW - 26, ly + 15), "منبع متراژ: دستور نقشهٔ ۱۴۰۲/۰۳/۲۸", size=23, fill=(255, 235, 180, 255),
  anchor="rm", box_fill=None, stroke=(0, 0, 0, 200), sw=3, max_w=OW * 0.40)
T((OW - 26, ly + 48), "مرز زمین بازسازی‌شده و تقریبی است", size=23, fill=(255, 200, 190, 255),
  anchor="rm", box_fill=None, stroke=(0, 0, 0, 200), sw=3, max_w=OW * 0.40)
T((OW - 26, ly + 81), "برای جانمایی دقیق: مختصات گوشه‌ها را بفرستید", size=23,
  fill=(255, 200, 190, 255), anchor="rm", box_fill=None, stroke=(0, 0, 0, 200), sw=3,
  max_w=OW * 0.40)

# مقیاس + جهت شمال
sb_m = 25.0
sb_px = sb_m / MPPX * SC
sx, sy = OW - 40 - sb_px, OH + HDR - 34
d2.line([(sx, sy), (sx + sb_px, sy)], fill=(255, 255, 255, 255), width=6)
for xx in (sx, sx + sb_px):
    d2.line([(xx, sy - 9), (xx, sy + 9)], fill=(255, 255, 255, 255), width=5)
T((sx + sb_px / 2, sy - 24), f"{sb_m:g} متر", size=22, fill=(255, 255, 255, 255),
  box_fill=None, stroke=(0, 0, 0, 220), sw=3)
nx, ny = 66, OH + HDR - 60
d2.polygon([(nx, ny - 34), (nx - 16, ny + 22), (nx, ny + 8), (nx + 16, ny + 22)],
           fill=(255, 255, 255, 255))
T((nx, ny + 44), "شمال", size=22, fill=(255, 255, 255, 255), box_fill=None,
  stroke=(0, 0, 0, 220), sw=3)

final.convert("RGB").save(OUT, quality=94)
print("saved:", OUT, final.size)
print(f"gross={A_GROSS:.2f} net={A_NET:.2f} lost={LOST:.2f} setback_N={SETBACK_N} setback_E/S={X_ES:.2f}")
print("net polygon (m from SW):", [(round(x, 2), round(y, 2)) for x, y in NET])
print("SW anchor:", round(ANCHOR_LAT, 7), round(ANCHOR_LON, 7))
