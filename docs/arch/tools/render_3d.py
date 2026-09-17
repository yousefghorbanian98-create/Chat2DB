#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""شماتیک سه‌بعدی اجرایی (آکسونومتریک) از دو طرحوارهٔ باقیمانده
سطح اشغال ۸۰٪ (عمق ۱۰.۷۰ m) · تراکم ۱۸۰٪ · پیلوت + ۳ مغازه + ۴ طبقه مسکونی
خروجی: docs/arch/schemes-3d.png
"""
import math, os
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display

HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT = os.path.join(HERE, "docs", "arch", "schemes-3d.png")
FDIR = "/home/user/fonts"

# ---------------------------------------------------------------- ابعاد (متر)
W, D = 40.57, 13.37
OCC, FSR = 0.80, 1.80
FP = W * D * OCC                 # ۴۳۳.۹ m²
BLD_D = FP / W                   # ۱۰.۷۰ m
OPEN_D = D - BLD_D               # ۲.۶۷ m
Y0, Y1 = OPEN_D, D               # جای ساختمان در عرض زمین
GND_H, FL_H, NFL, BASE_H = 4.20, 3.00, 4, 3.00
TOP = GND_H + NFL * FL_H         # ۱۶.۲۰ m
AREA_NET = W * D
GFA = AREA_NET * FSR
RES_PER_FLOOR = (GFA - 214) / NFL          # ~۱۹۱ m²
BAR_L = RES_PER_FLOOR / BLD_D              # ~۱۷.۸ m
SHOP_X0 = W - 3 * 6.5                      # ۲۱.۰۷ — سه مغازه در شمال شرق

# رنگ‌ها
C_SITE, C_ST, C_GRN = (226, 224, 214), (206, 206, 206), (198, 228, 198)
C_POD_T, C_POD_E, C_POD_S = (252, 236, 214), (243, 206, 150), (232, 189, 128)
C_PK_T, C_PK_E, C_PK_S = (232, 238, 246), (206, 218, 234), (188, 203, 224)
C_RES_T, C_RES_E, C_RES_S = (248, 250, 252), (226, 234, 244), (208, 218, 232)
C_TER = (196, 230, 196)
C_CORE = (196, 196, 200)

P = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")
_c = {}


def fa(t):
    return get_display(arabic_reshaper.reshape(str(t).translate(P)))


def F(sz, bold=False):
    if (sz, bold) not in _c:
        _c[(sz, bold)] = ImageFont.truetype(
            os.path.join(FDIR, "Vazirmatn-Bold.ttf" if bold else "Vazirmatn-Regular.ttf"), sz)
    return _c[(sz, bold)]


# ---------------------------------------------------------------- بوم
CW, CH = 1900, 1320
img = Image.new("RGB", (CW, CH), (243, 241, 234))
dr = ImageDraw.Draw(img)


def txt(xy, t, size=20, fill=(30, 30, 30), bold=False, anchor="mm", bg=None, pad=(6, 4),
        max_w=None, stroke=None, sw=3):
    x, y = xy
    f = F(size, bold)
    t = fa(t)
    if max_w:
        while dr.textbbox((0, 0), t, font=f, stroke_width=sw)[2] > max_w and size > 9:
            size -= 1
            f = F(size, bold)
    b = dr.textbbox((x, y), t, font=f, anchor=anchor, stroke_width=sw)
    if bg:
        dr.rectangle([b[0] - pad[0], b[1] - pad[1], b[2] + pad[0], b[3] + pad[1]], fill=bg)
    if stroke:
        dr.text((x, y), t, font=f, fill=fill, anchor=anchor, stroke_width=sw, stroke_fill=stroke)
    else:
        dr.text((x, y), t, font=f, fill=fill, anchor=anchor)


# ---------------------------------------------------------------- آکسونومتریک
COS30, SIN30 = math.cos(math.radians(30)), math.sin(math.radians(30))


def make_view(ox, oy, S):
    def iso(x, y, z):
        return (ox + (x + y) * COS30 * S, oy + (x - y) * SIN30 * S - z * S)
    return iso


def shade(c, f):
    return tuple(max(0, min(255, int(v * f))) for v in c)


def draw_box(iso, x0, y0, z0, x1, y1, z1, ctop, ceast, csouth, edge=(105, 105, 108),
             lw=1, floors=None, stripes=None):
    """نمای جنوب (y=y0) و شرق (x=x1) و بام رسم می‌شوند"""
    pts = {
        'top': [iso(x0, y0, z1), iso(x1, y0, z1), iso(x1, y1, z1), iso(x0, y1, z1)],
        'east': [iso(x1, y0, z0), iso(x1, y1, z0), iso(x1, y1, z1), iso(x1, y0, z1)],
        'south': [iso(x0, y0, z0), iso(x1, y0, z0), iso(x1, y0, z1), iso(x0, y0, z1)],
    }
    dr.polygon(pts['south'], fill=csouth, outline=edge, width=lw)
    dr.polygon(pts['east'], fill=ceast, outline=edge, width=lw)
    dr.polygon(pts['top'], fill=ctop, outline=edge, width=lw)
    if floors:
        for z in floors:
            dr.line([iso(x0, y0, z), iso(x1, y0, z)], fill=edge, width=1)
            dr.line([iso(x1, y0, z), iso(x1, y1, z)], fill=edge, width=1)
    if stripes:
        sp = stripes
        x = x0 + sp
        while x < x1:
            dr.line([iso(x, y0, z0), iso(x, y0, z1)], fill=shade(csouth, 0.88), width=2)
            x += sp


def tower(iso, x, y, h=17.0, w=1.6):
    b = iso(x, y, 0)
    t = iso(x, y, h)
    dr.line([(b[0] - 9, b[1]), t], fill=(95, 95, 95), width=2)
    dr.line([(b[0] + 9, b[1]), t], fill=(95, 95, 95), width=2)
    for i in range(1, 8):
        f = i / 8
        yy = b[1] + (t[1] - b[1]) * f
        ww = 9 * (1 - f) + 2
        dr.line([(b[0] - ww + (b[0] - t[0]) * 0 + (t[0] - b[0]) * f * 0, yy),
                 (b[0] + ww, yy)], fill=(120, 120, 120), width=1)
    dr.line([(t[0] - 13, t[1] + h * 0.0 + 22), (t[0] + 13, t[1] + 22)], fill=(95, 95, 95), width=2)


# ---------------------------------------------------------------- پانل‌ها
def panel(idx, title, sub, blocks, labels, nums, inset_blocks, inset_end):
    px0 = 20 + idx * 940
    py0 = 106
    pw, ph = 920, 1010
    dr.rectangle([px0, py0, px0 + pw, py0 + ph], fill=(253, 252, 248), outline=(150, 150, 145), width=2)
    dr.rectangle([px0, py0, px0 + pw, py0 + 54], fill=(228, 233, 240), outline=(150, 150, 145), width=2)
    txt((px0 + 18, py0 + 27), title, size=22, bold=True, fill=(24, 42, 64), anchor="lm")
    txt((px0 + pw - 18, py0 + 27), sub, size=16, fill=(95, 105, 122), anchor="rm", max_w=380)

    S = 16.0
    ox = px0 + 60
    oy = py0 + 470
    iso = make_view(ox, oy, S)

    # زمینه: خیابان شمالی، فضای سبز جنوبی، زمین، خیابان شرقی
    for (a, b, c, d, z, col) in [
        (0, D, W, D + 3.2, 0, C_ST),            # گذر ۸ متری (شمال)
        (0, -5.0, W, 0, 0, C_GRN),              # فضای سبز حریم دکل (جنوب)
        (0, 0, W, D, 0, C_SITE),                # زمین
        (W, 0, W + 4.0, D, 0, C_ST),            # معبر شرقی
    ]:
        draw_box(iso, a, b, -0.45, c, d, z, col, shade(col, 0.9), shade(col, 0.82),
                 edge=(150, 150, 150), lw=1)
    # فضای باز جنوبی (۲.۶۷ متر)
    draw_box(iso, 0, 0, 0, W, OPEN_D, 0.06, (206, 234, 206), (200, 230, 200), (194, 226, 194),
             edge=(140, 180, 140), lw=1)
    tower(iso, 6.0, -2.6, 16.0)

    # بلوک‌های ساختمان (مرتب‌شده از دور به نزدیک)
    # کلیدِ عمق در راستای پرتوِ دید (۱,-۱,۱): دورترین اول رسم می‌شود
    for blk in sorted(blocks, key=lambda b: (b['x0'] - b['y0'] + b['z0'])):
        draw_box(iso, blk['x0'], blk['y0'], blk['z0'], blk['x1'], blk['y1'], blk['z1'],
                 blk.get('t', C_RES_T), blk.get('e', C_RES_E), blk.get('s', C_RES_S),
                 edge=blk.get('edge', (105, 105, 108)), lw=blk.get('lw', 1),
                 floors=blk.get('floors'), stripes=blk.get('stripes'))

    # برچسب‌ها
    for (pt, t, off, col) in labels:
        a = iso(*pt)
        b = (a[0] + off[0], a[1] + off[1])
        dr.line([a, b], fill=(90, 90, 90), width=1)
        dr.ellipse([a[0] - 3, a[1] - 3, a[0] + 3, a[1] + 3], fill=(90, 90, 90))
        txt(b, t, size=15, fill=(35, 35, 35), bg=(253, 252, 248), max_w=230)

    # جهت‌نما (بالا-چپ)
    nx, ny = px0 + 48, py0 + 104
    dr.polygon([(nx, ny - 24), (nx - 12, ny + 14), (nx, ny + 5), (nx + 12, ny + 14)], fill=(40, 40, 40))
    txt((nx, ny + 30), "شمال", size=15, fill=(40, 40, 40))

    # پلان طبقهٔ تیپ (درج در بالا-راست)
    iw = 250
    ix, iy = px0 + pw - iw - 26, py0 + 74
    sc = (iw - 10) / W
    ih = int(D * sc)
    dr.rectangle([ix, iy, ix + iw, iy + ih + 42], fill=(255, 255, 255), outline=(170, 170, 170),
                 width=1)
    txt((ix + iw / 2, iy + 16), "پلان طبقهٔ تیپ", size=15, fill=(70, 70, 70))
    fy = iy + 26

    def P2(xm, ym):
        return (ix + 5 + xm * sc, fy + (D - ym) * sc)

    dr.rectangle([P2(0, D)[0], P2(0, D)[1], P2(W, 0)[0], P2(W, 0)[1]], fill=(255, 255, 255),
                 outline=(200, 60, 60), width=2)
    dr.rectangle([P2(0, OPEN_D)[0], P2(0, OPEN_D)[1], P2(W, 0)[0], P2(W, 0)[1]], fill=(214, 240, 214))
    dr.rectangle([P2(0, D)[0], P2(0, D)[1], P2(W, OPEN_D)[0], P2(W, OPEN_D)[1]], fill=(252, 231, 197))
    for (bx0, bx1) in inset_blocks:
        dr.rectangle([P2(bx0, D)[0], P2(bx0, D)[1], P2(bx1, OPEN_D)[0], P2(bx1, OPEN_D)[1]],
                     fill=(246, 196, 120), outline=(150, 95, 20), width=1)
    dr.rectangle([P2(inset_end, D)[0], P2(inset_end, D)[1], P2(W, OPEN_D)[0], P2(W, OPEN_D)[1]],
                 fill=(196, 230, 196), outline=(70, 140, 80), width=1)
    txt(((P2(inset_end, D)[0] + P2(W, OPEN_D)[0]) / 2,
         (P2(inset_end, D)[1] + P2(W, OPEN_D)[1]) / 2), "تراس", size=11, fill=(35, 95, 45))
    if len(inset_blocks) == 2:
        gx = (inset_blocks[0][1] + inset_blocks[1][0]) / 2
        dr.rectangle([P2(gx - 0.35, D)[0], P2(gx - 0.35, D)[1], P2(gx + 0.35, OPEN_D)[0],
                      P2(gx + 0.35, OPEN_D)[1]], fill=(120, 190, 120))
        txt((P2(gx, D - 1.6)[0], P2(gx, D - 1.6)[1] - 12), "نورگیر", size=10, fill=(30, 90, 40))
    # برِ مغازه‌ها
    dr.line([P2(SHOP_X0, D), P2(W, D)], fill=(150, 95, 20), width=3)
    txt((ix + iw / 2, iy + ih + 32), "شمال ↑  |  مقیاس تقریبی", size=12, fill=(110, 110, 110))

    # اعداد
    ny2 = py0 + ph - 210
    dr.rectangle([px0 + 16, ny2, px0 + pw - 16, py0 + ph - 14], fill=(238, 242, 247),
                 outline=(180, 190, 205), width=1)
    for k, line in enumerate(nums):
        txt((px0 + 32, ny2 + 26 + k * 34), f"▪ {line}", size=17, fill=(36, 46, 60), anchor="lm",
            max_w=pw - 64)


# ============================================================ طرحوارهٔ ۲
blocks2 = [
    # پارکینگ پیلوت (غرب)
    dict(x0=0, y0=Y0, z0=0, x1=SHOP_X0, y1=Y1, z1=3.20, t=C_PK_T, e=C_PK_E, s=C_PK_S, stripes=2.5),
    # ۳ مغازه (شمال شرق)
    dict(x0=SHOP_X0, y0=Y0, z0=0, x1=W, y1=Y1, z1=GND_H, t=C_POD_T, e=C_POD_E, s=C_POD_S),
    # تراس پودیوم روی سقف مغازه‌ها
    dict(x0=BAR_L, y0=Y0, z0=GND_H, x1=W, y1=Y1, z1=GND_H + 0.25, t=C_TER, e=(186, 224, 186),
         s=(176, 216, 176)),
    # برج مسکونی ۴ طبقه
    dict(x0=0, y0=Y0, z0=GND_H, x1=BAR_L, y1=Y1, z1=TOP, t=C_RES_T, e=C_RES_E, s=C_RES_S,
         floors=[GND_H + i * FL_H for i in range(1, NFL)]),
    # هسته
    dict(x0=7.3, y0=10.9, z0=TOP, x1=11.3, y1=Y1, z1=TOP + 1.8, t=C_CORE, e=shade(C_CORE, .88),
         s=shade(C_CORE, .8)),
]
labels2 = [
    ((SHOP_X0 + 9, Y1, GND_H), "۳ مغازهٔ همکف (۱۹.۵ متر برِ شمالی)", (-30, -120), 0),
    ((6, Y1, 1.6), "پارکینگ پیلوت (۸ فضا) + رمپ زیرزمین", (-40, 60), 0),
    ((BAR_L / 2, Y0, TOP), "۴ طبقه مسکونی — ۸ واحد ~۸۱ m² مفید", (-20, -86), 0),
    ((30, Y0, GND_H + 0.25), "تراس پودیوم ۲۴۳ m²", (60, -52), 0),
    ((9.3, 12.1, TOP + 1.8), "هستهٔ پله و آسانسور", (-100, -40), 0),
    ((20, -2.6, 0), "فضای سبز حریم دکل", (10, 46), 0),
    ((20, D + 1.6, 0), "گذر ۸ متری", (10, -30), 0),
    ((W + 2, 6, 0), "معبر ۲۶–۲۹ متری", (58, -18), 0),
    ((20, 1.3, 0.06), "فضای باز ۲.۶۷ m", (10, 30), 0),
]
nums2 = [
    f"سطح اشغال ۸۰٪ = {FP:.0f} m² ⇒ عمق ساختمان {BLD_D:.2f} m + فضای باز {OPEN_D:.2f} m",
    f"زیربنای کل {GFA:.0f} m² | همکف: ۳ مغازه ۱۱۷ m² + هسته/لابی/خدمات + پارکینگ",
    f"۴ طبقه × {RES_PER_FLOOR:.0f} m² = هر طبقه ۲ واحد ۹۵ m² ناخالص (~۸۱ m² مفید) ⇒ ۸ واحد",
    "تراس پودیوم ۲۴۳ m² · پارکینگ نیاز ۱۱ / تأمین ۱۲ (زیرزمین) · نقدشوندگی زیاد",
]

# ============================================================ طرحوارهٔ ۵
B1, GAP = 8.9, 2.0
B2 = B1 * 2 + GAP                      # ۱۹.۸
blocks5 = [
    dict(x0=0, y0=Y0, z0=0, x1=SHOP_X0, y1=Y1, z1=3.20, t=C_PK_T, e=C_PK_E, s=C_PK_S, stripes=2.5),
    dict(x0=SHOP_X0, y0=Y0, z0=0, x1=W, y1=Y1, z1=GND_H, t=C_POD_T, e=C_POD_E, s=C_POD_S),
    dict(x0=B2, y0=Y0, z0=GND_H, x1=W, y1=Y1, z1=GND_H + 0.25, t=C_TER, e=(186, 224, 186),
         s=(176, 216, 176)),
    dict(x0=B1, y0=Y0, z0=GND_H, x1=B1 + GAP, y1=Y1, z1=GND_H + 0.25, t=C_TER, e=(186, 224, 186),
         s=(176, 216, 176)),
    dict(x0=0, y0=Y0, z0=GND_H, x1=B1, y1=Y1, z1=TOP, t=C_RES_T, e=C_RES_E, s=C_RES_S,
         floors=[GND_H + i * FL_H for i in range(1, NFL)]),
    dict(x0=B1 + GAP, y0=Y0, z0=GND_H, x1=B2, y1=Y1, z1=TOP, t=C_RES_T, e=C_RES_E, s=C_RES_S,
         floors=[GND_H + i * FL_H for i in range(1, NFL)]),
    dict(x0=8.4, y0=10.9, z0=TOP, x1=11.4, y1=Y1, z1=TOP + 1.8, t=C_CORE, e=shade(C_CORE, .88),
         s=shade(C_CORE, .8)),
]
labels5 = [
    ((SHOP_X0 + 9, Y1, GND_H), "۳ مغازهٔ همکف (۱۹.۵ متر برِ شمالی)", (-30, -120), 0),
    ((5, Y1, 1.6), "پارکینگ پیلوت + رمپ زیرزمین", (-40, 62), 0),
    ((4.4, Y0, TOP), "بلوک A — ۴ واحد", (-30, -80), 0),
    ((14.8, Y0, TOP), "بلوک B — ۴ واحد", (30, -60), 0),
    ((B1 + GAP / 2, Y0, GND_H + 0.25), "نورگیر ۲ m", (-10, 76), 0),
    ((30, Y0, GND_H + 0.25), "تراس پودیوم ۲۲۲ m²", (56, -46), 0),
    ((9.9, 12.1, TOP + 1.8), "هستهٔ پله و آسانسور", (-104, -40), 0),
    ((20, D + 1.6, 0), "گذر ۸ متری", (10, -30), 0),
    ((W + 2, 6, 0), "معبر ۲۶–۲۹ متری", (58, -18), 0),
]
nums5 = [
    f"سطح اشغال ۸۰٪ = {FP:.0f} m² ⇒ عمق {BLD_D:.2f} m | دو بلوک {B1:.1f} متری + نورگیر ۲ m",
    f"زیربنای کل {GFA:.0f} m² | هر طبقه ۲ × ۹۵ m² ناخالص (~۸۱ m² مفید) ⇒ ۸ واحدِ دو‌نورگیره",
    "هر واحد از شمال و جنوب نور می‌گیرد (تهویهٔ متقاطع — اقلیم اصفهان)",
    "تراس پودیوم ۲۲۲ m² · پارکینگ نیاز ۱۱ / تأمین ۱۲ · نقدشوندگی زیاد",
]

# ============================================================ سربرگ و پانوشت
dr.rectangle([0, 0, CW, 96], fill=(26, 40, 58))
txt((CW // 2, 36), "شماتیک سه‌بعدی اجرایی — دو طرحوارهٔ نقدشونده با سطح اشغال ۸۰٪", size=33,
    bold=True, fill=(255, 255, 255))
txt((CW // 2, 74), "زمین خالص ۵۴۲.۳۸ m² (۴۰.۵۷ × ۱۳.۳۷) | سطح اشغال ۸۰٪ = ۴۳۳.۹ m² | "
                   "تراکم فرضی ۱۸۰٪ = ۹۷۶ m² | عمق ساختمان ۱۰.۷۰ m + فضای باز جنوبی ۲.۶۷ m",
    size=18, fill=(194, 210, 232))

panel(0, "طرحوارهٔ ۲ — دو واحد در هر طبقه", "۸ واحد · یک برج روی پودیوم", blocks2, labels2, nums2,
      [(0, BAR_L)], BAR_L)
panel(1, "طرحوارهٔ ۵ — دو بلوک + نورگیر", "۸ واحدِ دو‌نورگیره", blocks5, labels5, nums5,
      [(0, B1), (B1 + GAP, B2)], B2)

FY = 1140
dr.rectangle([20, FY, CW - 20, FY + 156], fill=(233, 238, 244), outline=(150, 150, 145), width=2)
txt((40, FY + 30), "تفسیرِ من از «تا ۸۰٪ مجوز»: سطح اشغال ۸۰٪ (مساحتِ مجازِ ساخت = ۸۰٪ زمین). "
                   "اگر منظورتان تراکمِ ۸۰٪ یا موردِ دیگری است بگویید تا با یک دستور بازسازی کنم.",
    size=17, fill=(40, 50, 65), anchor="lm", max_w=CW - 80)
txt((40, FY + 62), "نکتهٔ کلیدی: با تراکمِ ثابت، سطح اشغال فقط «شکل» ساختمان را عوض می‌کند نه مقدار زیربنا را. "
                   "در ۸۰٪ اشغال، هر طبقه تنها ۱۹۱ m² از ۴۳۴ m² ردپا ساخته می‌شود ⇒ ۲۴۳ m² تراسِ پودیوم به‌دست می‌آید.",
    size=17, fill=(40, 50, 65), anchor="lm", max_w=CW - 80)
txt((40, FY + 94), "هزینهٔ این انتخاب: فضای باز جنوبی از ۵.۳۵ m به ۲.۶۷ m می‌رسد — یعنی حیاط به نورگیر تبدیل می‌شود "
                   "و دیگر مزیتِ «باغچه» را ندارد؛ در عوض تراسِ پودیوم جایگزینش می‌شود.",
    size=17, fill=(150, 45, 40), anchor="lm", max_w=CW - 80)
txt((40, FY + 126), "هردو گزینه ۸ واحد ~۸۱ متری می‌دهند. تفاوت: طرحوارهٔ ۲ ساده‌تر و ارزان‌تر است؛ "
                   "طرحوارهٔ ۵ نور و تهویهٔ دوطرفه می‌دهد اما نما و دیوارِ بیشتری می‌خواهد.",
    size=17, fill=(40, 50, 65), anchor="lm", max_w=CW - 80)

img.save(OUT)
print("saved:", OUT, img.size)
