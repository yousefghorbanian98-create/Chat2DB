#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""شیت طراحی: سایت‌پلان + مقطع + پلان پیلوت + دو گزینهٔ پلان طبقهٔ تیپ
زمین: خالص ۴۰.۵۷ × ۱۳.۳۷ متر (۵۴۲.۳۸ m²) — اصفهان، منطقه ۴
خروجی: docs/arch/design-proposal.png
"""
import os
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display

HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT = os.path.join(HERE, "docs", "arch", "design-proposal.png")
FDIR = "/home/user/fonts"

# ------------------------------------------------------------------ ابعاد (متر)
W, D = 40.57, 13.37            # زمین خالص
GROSS_W, GROSS_D = 47.64, 28.45
SB_N, SB_S, SB_E, SB_W = 8.00, 7.08, 7.08, 0.00
BLD_D = 8.00                   # عمق ساختمان (سطح اشغال ۶۰٪)
OPEN_D = D - BLD_D             # فضای باز جنوبی
FLOORS, FLOOR_H, GND_H, BASE_H = 4, 3.00, 4.20, 3.00
SHOP_W, SHOP_D = 6.50, 6.00
SERVICE_D = BLD_D - SHOP_D
CORE_W, LOBBY_W = 5.50, 3.50
RES_LEN = 25.10                # طولِ حجم مسکونی (تراکم ۱۸۰٪ → ۲۰۱ m² در طبقه)
TER_LEN = W - RES_LEN

# ------------------------------------------------------------------ متن فارسی
P = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")


def fa(t):
    return get_display(arabic_reshaper.reshape(str(t).translate(P)))


_cache = {}


def F(sz, bold=False):
    key = (sz, bold)
    if key not in _cache:
        _cache[key] = ImageFont.truetype(
            os.path.join(FDIR, "Vazirmatn-Bold.ttf" if bold else "Vazirmatn-Regular.ttf"), sz)
    return _cache[key]


# ------------------------------------------------------------------ بوم
CW, CH = 1720, 1520
img = Image.new("RGB", (CW, CH), (243, 241, 234))
dr = ImageDraw.Draw(img)


def txt(xy, t, size=20, fill=(30, 30, 30), bold=False, anchor="mm", bg=None,
        stroke=None, sw=3, pad=(6, 4), max_w=None):
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
        dr.text((x, y), t, font=f, fill=stroke, anchor=anchor, stroke_width=sw,
                stroke_fill=stroke)
    dr.text((x, y), t, font=f, fill=fill, anchor=anchor)


def rect(xy, fill=None, outline=None, width=2):
    dr.rectangle(xy, fill=fill, outline=outline, width=width)


def dim(x1, y1, x2, y2, label, off=0, size=16, vertical=False):
    """خط اندازه با برچسب"""
    if vertical:
        x = x1 + off
        dr.line([(x, y1), (x, y2)], fill=(90, 90, 90), width=1)
        for yy in (y1, y2):
            dr.line([(x - 5, yy), (x + 5, yy)], fill=(90, 90, 90), width=2)
        txt((x, (y1 + y2) / 2), label, size=size, fill=(60, 60, 60), bg=(243, 241, 234))
    else:
        y = y1 + off
        dr.line([(x1, y), (x2, y)], fill=(90, 90, 90), width=1)
        for xx in (x1, x2):
            dr.line([(xx, y - 5), (xx, y + 5)], fill=(90, 90, 90), width=2)
        txt(((x1 + x2) / 2, y), label, size=size, fill=(60, 60, 60), bg=(243, 241, 234))


def panel(x0, y0, x1, y1, title, sub=None):
    rect([x0, y0, x1, y1], fill=(253, 252, 248), outline=(150, 150, 145), width=2)
    dr.rectangle([x0, y0, x1, y0 + 44], fill=(226, 231, 238), outline=(150, 150, 145), width=2)
    txt((x0 + 16, y0 + 22), title, size=22, bold=True, fill=(25, 40, 60), anchor="lm")
    if sub:
        tw = dr.textbbox((0, 0), fa(title), font=F(22, True))[2]
        txt((x0 + 30 + tw, y0 + 23), sub, size=17, fill=(90, 100, 115), anchor="lm")
    return x0 + 20, y0 + 60, x1 - 20, y1 - 20


# ================================================================== سربرگ
dr.rectangle([0, 0, CW, 92], fill=(28, 42, 62))
txt((CW // 2, 34), "طرح پیشنهادی — مجتمع مسکونی-تجاری ۴ طبقه روی پیلوت", size=32, bold=True,
    fill=(255, 255, 255))
txt((CW // 2, 70), "مشتاق دوم، خیابان باغ مشهد، کوی منصور — اصفهان منطقه ۴ | زمین خالص ۵۴۲.۳۸ m² "
                   "(۴۰.۵۷ × ۱۳.۳۷ متر)", size=19, fill=(198, 214, 234))

# ================================================================== ۱) سایت‌پلان
x0, y0, x1, y1 = panel(30, 110, 820, 640, "۱) سایت‌پلان و پاکتِ ساخت",
                        "قرمز: عقب‌نشینی‌های طرح مصوب | سبز: فضای باز جنوبی")
s = min((x1 - x0) / GROSS_W, (y1 - y0 - 40) / GROSS_D)
ox = x0 + ((x1 - x0) - GROSS_W * s) / 2
oy = y0 + ((y1 - y0 - 40) - GROSS_D * s) / 2 + 10


def S(xm, ym):
    """متر از گوشهٔ SW زمین ناخالص → پیکسل"""
    return (ox + xm * s, oy + (GROSS_D - ym) * s)


# زمین ناخالص
g = [S(0, 0), S(GROSS_W, 0), S(GROSS_W, GROSS_D), S(0, GROSS_D)]
dr.polygon(g, fill=(255, 255, 255), outline=(120, 120, 120), width=2)
# نوارهای عقب‌نشینی
zones = [((0, D + SB_S, GROSS_W, GROSS_D), "جنوب: حریم دکل فشار قوی (فضای سبز) — عقب‌نشینی ۷.۰۸ m"),
         ((W, SB_S, GROSS_W, D + SB_S), "شرق: گذر متغیر ۲۶–۲۹ m — عقب‌نشینی ۷.۰۸ m"),
         ((0, D, W, GROSS_D - (GROSS_D - D - SB_S) + 0), "")]
for (a, b, c, d), lab in zones[:2]:
    p = [S(a, b), S(c, b), S(c, d), S(a, d)]
    dr.polygon(p, fill=(240, 205, 200))
# عقب‌نشینی شمالی (بالای زمین خالص)
dr.polygon([S(0, D), S(GROSS_W, D), S(GROSS_W, GROSS_D - SB_S), S(0, GROSS_D - SB_S)],
           fill=(240, 205, 200))
# زمین خالص
dr.polygon([S(0, 0), S(W, 0), S(W, D), S(0, D)], fill=(255, 255, 255), outline=(200, 60, 60), width=3)
# فضای باز جنوبی
dr.polygon([S(0, 0), S(W, 0), S(W, OPEN_D), S(0, OPEN_D)], fill=(214, 240, 214))
# ساختمان (ردیف شمالی، عمق ۸ متر)
dr.polygon([S(0, OPEN_D), S(W, OPEN_D), S(W, D), S(0, D)], fill=(255, 232, 196),
           outline=(150, 95, 20), width=3)
# حجم مسکونی (۲۵.۱ متر از غرب)
dr.polygon([S(0, OPEN_D), S(RES_LEN, OPEN_D), S(RES_LEN, D), S(0, D)], fill=(255, 214, 150),
           outline=(150, 95, 20), width=2)
txt((S(W / 2, D - 4)[0], S(W / 2, D - 4)[1] + 14), "زیربنای همکف (۳ مغازه + پارکینگ)", size=15,
    fill=(110, 70, 10))
txt((S(RES_LEN / 2, OPEN_D + 4)[0], S(RES_LEN / 2, OPEN_D + 4)[1] - 2), "حجم ۴ طبقه مسکونی", size=15,
    fill=(110, 70, 10))
txt((S(RES_LEN + TER_LEN / 2, OPEN_D + 4)[0], S(RES_LEN + TER_LEN / 2, OPEN_D + 4)[1] - 2),
    "تراس‌ها", size=15, fill=(70, 110, 70))
# معابر
txt((S(GROSS_W / 2, GROSS_D + 1.4)[0], S(GROSS_W / 2, GROSS_D + 1.4)[1]), "گذر ۸ متری (طرح مصوب) — جبههٔ شمالی",
    size=17, fill=(60, 60, 60), bg=(253, 252, 248))
dr.line([S(0, GROSS_D), S(GROSS_W, GROSS_D)], fill=(90, 90, 90), width=3)
# اندازه‌ها
dim(*S(0, 0), *S(W, 0), f"{W:.2f} m", off=+26, size=15)
dim(*S(0, 0), *S(0, D), f"{D:.2f} m", off=-26, size=15, vertical=True)
dim(*S(0, D), *S(0, GROSS_D), f"{SB_N:.2f}", off=-54, size=14, vertical=True)
# قطب‌نما
nx, ny = x1 - 58, y0 + 66
dr.polygon([(nx, ny - 26), (nx - 13, ny + 16), (nx, ny + 6), (nx + 13, ny + 16)], fill=(30, 30, 30))
txt((nx, ny + 34), "شمال", size=16, fill=(30, 30, 30))
# مقیاس
sb = 10 * s
sx, sy = x0 + 24, y1 - 30
dr.line([(sx, sy), (sx + sb, sy)], fill=(40, 40, 40), width=3)
for xx in (sx, sx + sb):
    dr.line([(xx, sy - 6), (xx, sy + 6)], fill=(40, 40, 40), width=2)
txt((sx + sb / 2, sy - 16), "۱۰ متر", size=15, bg=(253, 252, 248))

# ================================================================== ۲) مقطع عرضی
x0, y0, x1, y1 = panel(850, 110, 1690, 640, "۲) مقطع عرضی (جنوب ← شمال)",
                        "از فضای سبزِ حریم دکل برق تا کوچهٔ ۸ متری")
TOT = SB_S + D + SB_N                      # عرض کلِ زمین ناخالص = ۲۸.۴۵ m
HAB = BASE_H + GND_H + FLOORS * FLOOR_H    # ارتفاع کل سازه
sc = min((x1 - x0 - 150) / TOT, (y1 - y0 - 80) / (BASE_H + GND_H + FLOORS * FLOOR_H + 6))
cx = x0 + 96
cy = y1 - 52                               # تراز سطح زمین


def C(xm, ym):
    """xm از لبهٔ جنوبیِ زمین ناخالص | ym ارتفاع از سطح زمین"""
    return (cx + xm * sc, cy - ym * sc)


XB0, XB1 = SB_S + OPEN_D, SB_S + D         # جای ساختمان در عمق زمین

# خاک
dr.rectangle([(cx - 60, cy), (cx + TOT * sc + 40, cy + 26)], fill=(168, 140, 104))
dr.line([(cx - 60, cy), (cx + TOT * sc + 40, cy)], fill=(110, 85, 60), width=3)

# پهنهٔ جنوبی (عقب‌نشینی حریم دکل)
dr.rectangle([C(0, 6.0)[0], C(0, 6.0)[1], C(SB_S, 0)[0], C(SB_S, 0)[1]], fill=(214, 236, 214))
txt((C(SB_S / 2, 9.4)), "عقب‌نشینی حریم دکل", size=13, fill=(40, 95, 45))
txt((C(SB_S / 2, 7.6)), "۷.۰۸ m — فضای سبز", size=13, fill=(40, 95, 45))
# دکل برق (نماد)
tx, ty = C(SB_S * 0.42, 0)
th = 15.5 * sc
dr.line([(tx - 11, ty), (tx, ty - th)], fill=(80, 80, 80), width=2)
dr.line([(tx + 11, ty), (tx, ty - th)], fill=(80, 80, 80), width=2)
for i in range(1, 8):
    f = i / 8
    dr.line([(tx - 11 * (1 - f) - 2, ty - th * f), (tx + 11 * (1 - f) + 2, ty - th * f)],
            fill=(110, 110, 110), width=1)
dr.line([(tx - 16, ty - th * 0.78), (tx + 16, ty - th * 0.78)], fill=(80, 80, 80), width=2)
txt((tx, ty - th - 16), "دکل فشار قوی", size=12, fill=(70, 70, 70), bg=(253, 252, 248))

# حیاط/نورگیر جنوبی
dr.rectangle([C(SB_S, 0)[0], C(SB_S, 0)[1], C(XB0, 0)[0], C(XB0, 0)[1] + 4], fill=(232, 244, 226))
txt((C((SB_S + XB0) / 2, 3.2)), "حیاط/نورگیر ۵.۳۵ m", size=12, fill=(55, 95, 55))
txt((C((SB_S + XB0) / 2, 1.9)), "(۲۱۷ m² فضای باز)", size=11, fill=(70, 110, 70))

# زیرزمین
dr.rectangle([C(XB0, 0)[0], C(XB0, 0)[1], C(XB1, 0)[0], C(XB1, -BASE_H)[1]],
             fill=(220, 228, 240), outline=(110, 130, 150), width=2)
txt((C((XB0 + XB1) / 2, -BASE_H / 2)), f"زیرزمین — پارکینگ ۱۲ خودرو + انباری ({BASE_H:.1f} m)",
    size=13, fill=(45, 70, 100), max_w=(XB1 - XB0) * sc + 190)

# همکف
dr.rectangle([C(XB0, 0)[0], C(XB0, GND_H)[1], C(XB1, 0)[0], C(XB1, GND_H)[1]],
             fill=(255, 232, 196), outline=(150, 95, 20), width=2)
txt((C((XB0 + XB1) / 2, GND_H / 2)), f"همکف/پیلوت — ۳ مغازه + پارکینگ ({GND_H:.1f} m)", size=13,
    fill=(110, 70, 10), max_w=(XB1 - XB0) * sc + 190)

# طبقات مسکونی
for i in range(FLOORS):
    yb = GND_H + i * FLOOR_H
    dr.rectangle([C(XB0, yb)[0], C(XB0, yb + FLOOR_H)[1], C(XB1, yb)[0], C(XB1, yb)[1]],
                 fill=(230, 242, 230), outline=(60, 120, 70), width=2)
    txt((C((XB0 + XB1) / 2, yb + FLOOR_H / 2)), f"طبقه {i+1} — واحد مسکونی ~۲۰۱ m²", size=13,
        fill=(35, 85, 45), max_w=(XB1 - XB0) * sc - 6)

# جان‌پناه
top = GND_H + FLOORS * FLOOR_H
dr.rectangle([C(XB0, top)[0], C(XB0, top + 0.8)[1], C(XB1, top)[0], C(XB1, top)[1]],
             fill=(185, 185, 185))
txt((C((XB0 + XB1) / 2, top + 2.6)), f"بام: تراس مشترک + پنل خورشیدی | ارتفاع از زمین {top:.1f} m",
    size=13, fill=(60, 60, 60), max_w=(XB1 - XB0) * sc + 260)

# گذر ۸ متری
dr.rectangle([C(SB_S + D, 0)[0], C(SB_S + D, 0)[1], C(TOT, 0)[0], C(TOT, 0)[1] + 4],
             fill=(228, 228, 228))
txt((C(SB_S + D + SB_N / 2, 3.4)), "گذر ۸ متری", size=13, fill=(70, 70, 70))
txt((C(SB_S + D + SB_N / 2, 1.9)), "(طرح مصوب)", size=11, fill=(95, 95, 95))

# اندازه‌ها
dim(C(XB0, top)[0], C(XB0, top)[1], C(XB1, top)[0], C(XB1, top)[1], f"{BLD_D:.1f} m", off=-22,
    size=13)
dim(C(TOT, 0)[0], C(TOT, top)[1], C(TOT, 0)[0], C(TOT, 0)[1], f"{HAB:.1f} m", off=+56,
    size=13, vertical=True)

# ================================================================== ۳) پلان پیلوت
x0, y0, x1, y1 = panel(30, 670, 1690, 1000, "۳) پلان همکف / پیلوت",
                        "۳ مغازه رو به شمال و نبش شمال‌شرقی + هسته + پارکینگ + رمپ زیرزمین")
ps = min((x1 - x0 - 90) / W, (y1 - y0 - 60) / BLD_D)
px0 = x0 + 45
py0 = y0 + ((y1 - y0) - BLD_D * ps) / 2


def Q(xm, ym):
    """متر از گوشه SW ساختمان"""
    return (px0 + xm * ps, py0 + (BLD_D - ym) * ps)


def box(a, b, c, d, fill, outline, lw=2, label=None, size=15, lab_col=(40, 40, 40)):
    dr.rectangle([Q(a, b)[0], Q(a, d)[1], Q(c, b)[0], Q(c, b)[1]], fill=fill, outline=outline,
                 width=lw)
    if label:
        txt(((Q(a, b)[0] + Q(c, b)[0]) / 2, (Q(a, b)[1] + Q(a, d)[1]) / 2), label, size=size,
            fill=lab_col)


box(0, 0, W, BLD_D, (255, 250, 240), (150, 95, 20), 3)
# مغازه‌ها (از شرق/راست)
xs = W
for i in range(3):
    xs -= SHOP_W
    box(xs, SERVICE_D, xs + SHOP_W, BLD_D, (255, 226, 178), (170, 110, 30), 2,
        f"مغازه {3-i}\n{SHOP_W*SHOP_D:.0f} m²", size=15, lab_col=(110, 65, 10))
box(W - 3 * SHOP_W, 0, W, SERVICE_D, (255, 240, 214), (170, 110, 30), 1,
    "سرویس/انباری مغازه‌ها", size=13, lab_col=(110, 90, 40))
# هسته، لابی، پارکینگ
core_x = W - 3 * SHOP_W - CORE_W
box(core_x, SERVICE_D, core_x + CORE_W, BLD_D, (214, 214, 214), (90, 90, 90), 2,
    "هسته\nپله+آسانسور", size=14)
lb_x = core_x - LOBBY_W
box(lb_x, SERVICE_D, core_x, BLD_D, (232, 240, 248), (90, 130, 170), 2, "لابی", size=14)
box(0, 0, lb_x, BLD_D, (226, 234, 244), (110, 130, 150), 2, None)
txt(((Q(0, 0)[0] + Q(lb_x, 0)[0]) / 2, (Q(lb_x, 0)[1] + Q(lb_x, BLD_D)[1]) / 2 - 14),
    "پارکینگ پیلوت (۴ خودرو) + رمپ زیرزمین", size=15, fill=(50, 70, 95))
txt(((Q(0, 0)[0] + Q(lb_x, 0)[0]) / 2, (Q(lb_x, 0)[1] + Q(lb_x, BLD_D)[1]) / 2 + 14),
    f"≈ {(lb_x*BLD_D):.0f} m²", size=14, fill=(70, 90, 115))
# جبهه شمال
dr.line([Q(0, BLD_D), Q(W, BLD_D)], fill=(150, 95, 20), width=5)
txt(((Q(0, BLD_D)[0] + Q(W, BLD_D)[0]) / 2, Q(0, BLD_D)[1] - 22),
    "جبههٔ شمالی — گذر ۸ متری (ویترین مغازه‌ها)", size=16, fill=(110, 70, 10), bg=(253, 252, 248))
dim(Q(0, 0)[0], Q(0, 0)[1], Q(W, 0)[0], Q(W, 0)[1], f"{W:.2f} m", off=+34, size=15)

# ================================================================== ۴) طبقه تیپ A
x0, y0, x1, y1 = panel(30, 1030, 850, 1310, "۴) طبقهٔ تیپ — گزینهٔ A (خواستهٔ شما)",
                        "هر طبقه یک واحد بزرگ ~۲۰۱ m² + تراس ~۱۲۴ m²")
s2 = min((x1 - x0 - 40) / W, (y1 - y0 - 50) / BLD_D)
ax = x0 + 20 + ((x1 - x0 - 40) - W * s2) / 2
ay = y0 + ((y1 - y0 - 50) - BLD_D * s2) / 2 + 10


def A(xm, ym):
    return (ax + xm * s2, ay + (BLD_D - ym) * s2)


dr.rectangle([A(0, 0)[0], A(0, BLD_D)[1], A(W, 0)[0], A(W, 0)[1]], fill=(255, 255, 255),
             outline=(180, 180, 180), width=2)
# تراس
dr.rectangle([A(RES_LEN, 0)[0], A(RES_LEN, BLD_D)[1], A(W, 0)[0], A(W, 0)[1]],
             fill=(226, 242, 226), outline=(80, 150, 90), width=2)
txt(((A(RES_LEN, 0)[0] + A(W, 0)[0]) / 2, (A(RES_LEN, 0)[1] + A(RES_LEN, BLD_D)[1]) / 2),
    f"تراس اختصاصی\n≈{TER_LEN*BLD_D:.0f} m²", size=15, fill=(40, 100, 50))
# واحد
dr.rectangle([A(0, 0)[0], A(0, BLD_D)[1], A(RES_LEN, 0)[0], A(RES_LEN, 0)[1]],
             fill=(248, 250, 252), outline=(60, 120, 70), width=3)
# داخلی
L = RES_LEN
boxA = [(0.2, 0.2, 7.0, 3.2, "نشیمن + ناهارخوری", (226, 238, 250)),
        (7.2, 0.2, 12.0, 3.2, "آشپزخانه", (240, 240, 232)),
        (0.2, 3.4, 5.0, 7.8, "خواب ۱ ( master )", (236, 244, 236)),
        (5.2, 3.4, 8.6, 7.8, "خواب ۲", (236, 244, 236)),
        (8.8, 3.4, 12.2, 7.8, "خواب ۳", (236, 244, 236)),
        (12.4, 0.2, 15.0, 7.8, " حمام/سرویس", (232, 236, 240)),
        (15.2, 0.2, 18.6, 7.8, "هال/ورودی", (240, 240, 236)),
        (18.8, 0.2, 20.0, 7.8, "هسته", (214, 214, 214)),
        (20.2, 0.2, 24.9, 7.8, "نشیمن دوم / کار", (232, 240, 248))]
for a, b, c, d, lab, col in boxA:
    dr.rectangle([A(a, b)[0], A(a, d)[1], A(c, b)[0], A(c, b)[1]], fill=col, outline=(150, 150, 150))
    txt(((A(a, b)[0] + A(c, b)[0]) / 2, (A(a, b)[1] + A(c, d)[1]) / 2), lab, size=11, fill=(45, 45, 45),
        max_w=(c - a) * s2 - 6)
txt(((A(0, 0)[0] + A(RES_LEN, 0)[0]) / 2, A(0, BLD_D)[1] - 16),
    f"واحد مسکونی ≈ {RES_LEN*BLD_D:.0f} m² ناخالص (≈ ۱۷۰ m² مفید)", size=14, fill=(30, 80, 40),
    bg=(253, 252, 248))

# ================================================================== ۵) طبقه تیپ B
x0, y0, x1, y1 = panel(870, 1030, 1690, 1310, "۵) طبقهٔ تیپ — گزینهٔ B (پیشنهادِ بهره‌وری)",
                        "هر طبقه دو واحد ~۱۰۰ m² → جمعاً ۸ واحد")
bx = x0 + 20 + ((x1 - x0 - 40) - W * s2) / 2
by = ay


def B_(xm, ym):
    return (bx + xm * s2, by + (BLD_D - ym) * s2)


dr.rectangle([B_(0, 0)[0], B_(0, BLD_D)[1], B_(W, 0)[0], B_(W, 0)[1]], fill=(255, 255, 255),
             outline=(180, 180, 180), width=2)
dr.rectangle([B_(RES_LEN, 0)[0], B_(RES_LEN, BLD_D)[1], B_(W, 0)[0], B_(W, 0)[1]],
             fill=(226, 242, 226), outline=(80, 150, 90), width=2)
txt(((B_(RES_LEN, 0)[0] + B_(W, 0)[0]) / 2, (B_(RES_LEN, 0)[1] + B_(RES_LEN, BLD_D)[1]) / 2),
    f"تراس مشترک\n≈{TER_LEN*BLD_D:.0f} m²", size=15, fill=(40, 100, 50))
dr.rectangle([B_(0, 0)[0], B_(0, BLD_D)[1], B_(RES_LEN, 0)[0], B_(RES_LEN, 0)[1]],
             fill=(248, 250, 252), outline=(60, 120, 70), width=3)
# corridor
dr.rectangle([B_(0, BLD_D)[0], B_(0, BLD_D)[1], B_(RES_LEN, BLD_D - 1.6)[0],
              B_(RES_LEN, BLD_D - 1.6)[1]], fill=(235, 235, 235), outline=(160, 160, 160))
txt(((B_(0, BLD_D - .8)[0] + B_(RES_LEN, BLD_D - .8)[0]) / 2, B_(RES_LEN, BLD_D - .8)[1]),
    "راهرو ۱.۶ m", size=11, fill=(70, 70, 70))
half = RES_LEN / 2
units = [(0.2, 0.2, half - 0.2, BLD_D - 1.8, "واحد A — ۲ خوابه ≈ ۱۰۰ m²", (236, 244, 236)),
         (half + 0.2, 0.2, RES_LEN - 0.2, BLD_D - 1.8, "واحد B — ۲ خوابه ≈ ۱۰۰ m²", (240, 240, 232))]
for a, b, c, d, lab, col in units:
    dr.rectangle([B_(a, b)[0], B_(a, d)[1], B_(c, b)[0], B_(c, b)[1]], fill=col,
                 outline=(150, 150, 150))
    txt(((B_(a, b)[0] + B_(c, b)[0]) / 2, (B_(a, b)[1] + B_(c, d)[1]) / 2), lab, size=12,
        fill=(45, 45, 45), max_w=(c - a) * s2 - 8)
txt(((B_(0, 0)[0] + B_(RES_LEN, 0)[0]) / 2, B_(0, BLD_D)[1] - 16),
    "۸ واحدِ نقدشونده‌تر در همان زیربنا — ریسک فروش کمتر", size=14, fill=(30, 80, 40),
    bg=(253, 252, 248))

# ================================================================== پانوشت
dr.rectangle([30, 1340, 1690, 1500], fill=(233, 238, 244), outline=(150, 150, 145), width=2)
notes = [
    "مفروضاتِ ضوابط (حتماً با شهرداری منطقهٔ ۴ تأیید شود): سطح اشغال ۶۰٪ = ۳۲۵ m² | "
    "تراکم ۱۸۰٪ = ۹۷۶ m² زیربنا | پیلوت و زیرزمینِ پارکینگ معاف از تراکم",
    "برنامه: همکف = ۳ مغازه (هر کدام ۳۹ m²) + هسته ۳۳ m² + لابی ۲۱ m² + پارکینگ | "
    "۴ طبقه مسکونی (هر طبقه ۲۰۱ m²) | زیرزمین = ۱۲ پارکینگ + انباری",
    "جهت‌گیری: نشیمن و خواب‌ها رو به جنوب (دیدِ باز و دائمی به فضای سبزِ حریم دکل)؛ "
    "سرویس‌ها، راهرو و هسته در جبههٔ شمالی | مغازه‌ها در نبش شمال‌شرقی برای بیشترین دید",
    "هشدارها: ۱) تعداد طبقات تابعِ عرض معبر است (۸ m شمالی در برابر ۲۶–۲۹ m شرقی) — استعلام کنید؛ "
    "۲) ارتفاع و فاصله تا دکل فشار قوی را از اداره برق بپرسید؛ ۳) امکانِ حفر زیرزمین",
]
for i, n in enumerate(notes):
    txt((50, 1372 + i * 34), f"{i+1}. {n}", size=16, fill=(40, 50, 65), anchor="lm",
        max_w=1640)

img.save(OUT)
print("saved:", OUT, img.size)
