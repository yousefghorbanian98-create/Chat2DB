#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""برگهٔ اجراییِ نهایی — پیشنهادِ برگزیده: تک‌بلوکِ کم‌عمق + ایوان ۲.۴ متری + شفتِ ۳×۳ در هسته
خروجی: docs/arch/final-design.png
"""
import math, os, json
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display

HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT = os.path.join(HERE, "docs", "arch", "final-design.png")
FDIR = "/home/user/fonts"
L = json.load(open(os.path.join(HERE, "docs", "arch", "final-layout.json"), encoding="utf-8"))

# ---------------------------------------------------------------- ابعاد
W, D = 40.57, 13.37
Y0, Y1 = 2.67, 13.37           # جای ساختمان در زمین (فضای بازِ جنوبی ۲.۶۷ m)
POD_D = 10.70                  # عمقِ پودیوم (لبهٔ جنوبیِ زمینِ نت تا شمال)
UW, UD = L["unit"]["w"], L["unit"]["d"]          # ۹.۵۳ × ۸.۳۰
BALC = 2.40
CORE_W = L["building"]["core_w"]                 # ۳.۰۰
SH_W, SH_D = 3.00, 3.00        # شفت
BLD_W = 2 * UW + CORE_W                          # ۲۲.۰۷
SHOP_X0, SHOP_DEEP, SVC_DEEP = 21.07, 7.00, 2.00
GND_H, FL_H, NFL = 4.20, 3.00, 4
TOP = GND_H + NFL * FL_H
OCC_AREA = W * D * 0.80

P = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")
_c = {}


def fa(t):
    return get_display(arabic_reshaper.reshape(str(t).translate(P)))


def F(sz, bold=False):
    if (sz, bold) not in _c:
        _c[(sz, bold)] = ImageFont.truetype(
            os.path.join(FDIR, "Vazirmatn-Bold.ttf" if bold else "Vazirmatn-Regular.ttf"), sz)
    return _c[(sz, bold)]


CW, CH = 1900, 2700
img = Image.new("RGB", (CW, CH), (243, 241, 234))
dr = ImageDraw.Draw(img)


def txt(xy, t, size=17, fill=(30, 30, 30), bold=False, anchor="mm", bg=None, pad=(5, 3), max_w=None):
    x, y = xy
    f = F(size, bold)
    t = fa(t)
    if max_w:
        while dr.textbbox((0, 0), t, font=f)[2] > max_w and size > 8:
            size -= 1
            f = F(size, bold)
    b = dr.textbbox((x, y), t, font=f, anchor=anchor)
    if bg:
        dr.rectangle([b[0] - pad[0], b[1] - pad[1], b[2] + pad[0], b[3] + pad[1]], fill=bg)
    dr.text((x, y), t, font=f, fill=fill, anchor=anchor)


def panel(x, y, w, h, title, sub=None):
    dr.rectangle([x, y, x + w, y + h], fill=(253, 252, 248), outline=(150, 150, 145), width=2)
    dr.rectangle([x, y, x + w, y + 44], fill=(228, 233, 240), outline=(150, 150, 145), width=2)
    txt((x + 14, y + 22), title, size=19, bold=True, fill=(24, 42, 64), anchor="lm")
    if sub:
        txt((x + w - 14, y + 22), sub, size=14, fill=(95, 105, 122), anchor="rm", max_w=w - 300)
    return y + 44


# ================================================================ سربرگ
dr.rectangle([0, 0, CW, 100], fill=(26, 40, 58))
txt((CW // 2, 33), "طرحِ نهایی — تک‌بلوکِ کم‌عمق + ایوانِ سراسریِ جنوبی + شفتِ ۳×۳ در هسته",
    size=32, bold=True, fill=(255, 255, 255))
u = L["unit"]; b = L["building"]
txt((CW // 2, 74),
    f"زمین خالص ۵۴۲.۳۸ m² · سطح اشغال ۸۰٪ · زیربنای کل ۹۷۶ m² · هر واحد {u['sale']} m² "
    f"({u['encl']} بسته + {u['balcony']} ایوان) · ۸ واحد · عرضِ ساختمان {b['width']} m",
    size=18, fill=(198, 214, 236))

# ================================================================ A: سایت‌پلان
ax, ay, aw, ah = 20, 110, 930, 450
ay2 = panel(ax, ay, aw, ah, "الف — سایت‌پلان", "عقب‌نشینی‌ها، جایِ حجم، تراس و دسترسی‌ها")
sc = (aw - 90) / (W + 8)
ox = ax + 45 + (aw - 90 - W * sc) / 2
oy = ay2 + 10 + (D + 4) * sc


def S2(xm, ym):
    return (ox + xm * sc, oy - ym * sc)


def RS(x0, y0, x1, y1, fill=None, outline=None, width=1):
    a, b2 = S2(x0, y1), S2(x1, y0)
    dr.rectangle([a[0], a[1], b2[0], b2[1]], fill=fill, outline=outline, width=width)


RS(-4, -4, W + 4, D + 4, fill=(250, 250, 248))
# معبرها و حریم
RS(0, D, W, D + 4, fill=(206, 206, 206))
RS(W, 0, W + 4, D, fill=(206, 206, 206))
RS(0, -4, W, 0, fill=(198, 228, 198))
RS(0, 0, W, D, fill=(255, 255, 255), outline=(200, 60, 60), width=2)
RS(0, Y0, BLD_W, Y1, fill=(232, 240, 226), outline=(90, 120, 90), width=2)
RS(0, Y0, BLD_W, Y0 + BALC, fill=(250, 240, 214), outline=(190, 150, 60), width=1)
RS(BLD_W, Y0, W, Y1, fill=(222, 240, 222), outline=(90, 120, 90), width=1)
txt(((S2(BLD_W, Y0)[0] + S2(W, Y1)[0]) / 2, (S2(BLD_W, Y0)[1] + S2(W, Y1)[1]) / 2),
    f"تراسِ پودیوم\n{b['terrace']} m²", size=15, fill=(35, 95, 45))
# شفت
RS(UW, Y1 - SH_D, UW + SH_W, Y1, fill=(150, 190, 150), outline=(60, 120, 60), width=1)
txt(((S2(UW, Y1 - SH_D)[0] + S2(UW + SH_W, Y1)[0]) / 2,
     (S2(UW, Y1 - SH_D)[1] + S2(UW + SH_W, Y1)[1]) / 2), "شفت ۳×۳", size=11, fill=(255, 255, 255))
# دکلِ برق
tx, ty = S2(8, -2.2)
dr.line([(tx - 9, ty), (tx, ty - 70)], fill=(95, 95, 95), width=2)
dr.line([(tx + 9, ty), (tx, ty - 70)], fill=(95, 95, 95), width=2)
dr.line([(tx - 13, ty - 50), (tx + 13, ty - 50)], fill=(95, 95, 95), width=2)
# ابعاد و برچسب‌ها
def dimh(x0, x1, y, label):
    a, b2 = S2(x0, y), S2(x1, y)
    dr.line([a, b2], fill=(180, 60, 60), width=1)
    txt(((a[0] + b2[0]) / 2, a[1] - 11), label, size=12, fill=(170, 50, 50), bg=(250, 250, 248))


def dimv(y0, y1, x, label):
    a, b2 = S2(x, y0), S2(x, y1)
    dr.line([a, b2], fill=(180, 60, 60), width=1)
    txt((a[0] - 9, (a[1] + b2[1]) / 2), label, size=12, fill=(170, 50, 50), bg=(250, 250, 248))


dimh(0, BLD_W, D + 2.2, f"عرضِ حجم {BLD_W:.2f} m")
dimh(0, W, -5.6, f"عرضِ زمین {W:.2f} m")
dimv(Y0, Y1, W + 2.4, f"{POD_D:.2f}")
dimv(0, Y0, W + 2.4, "۲.۶۷")
dimv(-4, 0, W + 2.4, "۷.۰۸")
txt((S2(BLD_W / 2, Y0 + BALC / 2)[0], S2(BLD_W / 2, Y0 + BALC / 2)[1]), "ایوان ۲.۴۰", size=12,
    fill=(120, 85, 20))
txt((S2(30, D + 2)[0], S2(30, D + 2)[1]), "گذر ۸ متری (شمال)", size=13, fill=(70, 70, 70))
txt((S2(W + 2, D / 2)[0], S2(W + 2, D / 2)[1]), "معبر ۲۶–۲۹ متری", size=12, fill=(70, 70, 70))
txt((S2(22, -2.2)[0], S2(22, -2.2)[1]), "فضای سبزِ حریمِ دکلِ فشارقوی (۷.۰۸ m)", size=12,
    fill=(40, 95, 45))
# ورودی‌ها
dr.line([S2(UW + 1.5, Y1), S2(UW + 1.5, Y1 + 1.2)], fill=(60, 90, 160), width=3)
txt((S2(UW + 1.5, Y1 + 2.0)[0], S2(UW + 1.5, Y1 + 2.0)[1]), "ورودی پیاده", size=11, fill=(60, 90, 160))
dr.line([S2(1.0, Y1), S2(1.0, Y1 + 1.2)], fill=(200, 120, 40), width=3)
txt((S2(1.0, Y1 + 2.0)[0], S2(1.0, Y1 + 2.0)[1]), "ورودی خودرو", size=11, fill=(200, 120, 40))

# ================================================================ B: پلانِ پیلوت
bx, by, bw, bh = 970, 110, 930, 450
by2 = panel(bx, by, bw, bh, "ب — پلانِ پیلوت / همکف", "۳ مغازه + پارکینگ + هسته (ارتفاعِ مفید ۲.۴۰)")
sc2 = (bw - 90) / (W + 4)
ox2 = bx + 45
oy2 = by2 + 20 + POD_D * sc2


def G2(xm, ym):
    return (ox2 + xm * sc2, oy2 - ym * sc2)


def RG(x0, y0, x1, y1, fill=None, outline=None, width=1):
    a, b2 = G2(x0, y1), G2(x1, y0)
    dr.rectangle([a[0], a[1], b2[0], b2[1]], fill=fill, outline=outline, width=width)


RG(0, 0, W, POD_D, fill=(255, 255, 255), outline=(120, 120, 120), width=2)
# پارکینگِ پیلوت: دو جایگاه در دو سویِ هسته (هسته مسیر را قطع می‌کند)
sp_w, sp_d, sp_gap = 2.50, 5.00, 0.15
RG(0, 0, SHOP_X0, POD_D, fill=(235, 240, 247))
n = 0
for bay_x0 in (0.5, 13.0):
    for i in range(3):
        x0 = bay_x0 + i * (sp_w + sp_gap)
        RG(x0, 0.4, x0 + sp_w, 0.4 + sp_d, fill=(255, 255, 255), outline=(110, 140, 190), width=1)
        n += 1
        txt((G2(x0 + sp_w / 2, 0.4 + sp_d / 2)[0], G2(x0 + sp_w / 2, 0.4 + sp_d / 2)[1]), str(n),
            size=11, fill=(90, 120, 170))
txt((G2(4.7, 7.6)[0], G2(4.7, 7.6)[1]), "مسیرِ تردد و مانور", size=12, fill=(70, 100, 150))
txt((G2(16.8, 7.6)[0], G2(16.8, 7.6)[1]), "مسیرِ تردد و مانور", size=12, fill=(70, 100, 150))
txt((G2(10.5, 3.0)[0], G2(10.5, 3.0)[1]), "هسته مسیر را قطع می‌کند", size=11, fill=(150, 60, 30))
# پیشنهادِ زیرزمین (خط‌چین)
for xm in (0.3, SHOP_X0 - 0.3):
    for ym in [0.4 + k * 0.8 for k in range(13)]:
        dr.line([G2(xm, ym), G2(xm, ym + 0.45)], fill=(90, 120, 90), width=2)
for ym in (0.4, POD_D - 0.4):
    for xm in [0.3 + k * 1.2 for k in range(18)]:
        dr.line([G2(xm, ym), G2(xm + 0.7, ym)], fill=(90, 120, 90), width=2)
txt((G2(SHOP_X0 / 2, POD_D - 0.9)[0], G2(SHOP_X0 / 2, POD_D - 0.9)[1]),
    "پیشنهاد: زیرزمینِ پارکینگ ۲۳۶ m² (۹ فضای دیگر)", size=12, fill=(40, 100, 50))
# هسته
RG(UW, 5.6, UW + CORE_W, POD_D, fill=(214, 214, 220), outline=(110, 110, 110), width=1)
txt((G2(UW + CORE_W / 2, 8.1)[0], G2(UW + CORE_W / 2, 8.1)[1]), "لابی + پله + آسانسور", size=11,
    fill=(60, 60, 70))
# مغازه‌ها
for i in range(3):
    x0 = SHOP_X0 + i * 6.5
    RG(x0, POD_D - SHOP_DEEP, x0 + 6.5, POD_D, fill=(252, 236, 214), outline=(170, 120, 50), width=1)
    txt((G2(x0 + 3.25, POD_D - SHOP_DEEP / 2)[0], G2(x0 + 3.25, POD_D - SHOP_DEEP / 2)[1]),
        f"مغازه {i+1}\n{6.5*SHOP_DEEP:.0f} m²", size=12, fill=(120, 80, 20))
RG(SHOP_X0, 0, W, POD_D - SHOP_DEEP, fill=(243, 243, 236), outline=(170, 170, 170), width=1)
txt((G2((SHOP_X0 + W) / 2, SVC_DEEP / 2)[0], G2((SHOP_X0 + W) / 2, SVC_DEEP / 2)[1]),
    "انبار و سرویسِ مغازه‌ها (۳۹ m²)", size=12, fill=(90, 90, 90))
dr.line([G2(0, POD_D), G2(SHOP_X0, POD_D)], fill=(200, 120, 40), width=3)
txt((G2(SHOP_X0 / 2, POD_D + 0.9)[0], G2(SHOP_X0 / 2, POD_D + 0.9)[1]), "ورودی خودرو از گذر ۸ متری",
    size=12, fill=(200, 120, 40))
txt((G2(W / 2, POD_D + 0.9)[0], G2(W / 2, POD_D + 0.9)[1]), "برِ تجاری ۱۹.۵ m رو به گذرِ شمالی", size=12,
    fill=(120, 80, 20))
# پودیوم تراس (خط‌چین بالای مغازه‌ها)
dr.line([G2(SHOP_X0, 0.2), G2(W, 0.2)], fill=(90, 120, 90), width=2)

# ================================================================ C: پلانِ طبقهٔ تیپ
cx, cy, cw, ch = 20, 570, 1280, 520
cy2 = panel(cx, cy, cw, ch, "ج — پلانِ طبقهٔ تیپ (طبقات ۱ تا ۴)",
            "۲ واحد + هسته + شفتِ نور/تهویه + ایوانِ ۲.۴ متری")
sc3 = min((cw - 240) / BLD_W, (ch - 44 - 110) / (UD + BALC))
ox3 = cx + 120
oy3 = cy2 + 40 + UD * sc3


def T2(xm, ym):
    return (ox3 + xm * sc3, oy3 - ym * sc3)


def RT(x0, y0, x1, y1, fill=None, outline=None, width=1):
    a, b2 = T2(x0, y1), T2(x1, y0)
    dr.rectangle([a[0], a[1], b2[0], b2[1]], fill=fill, outline=outline, width=width)


COLOR = {'living': (250, 235, 205), 'kitchen': (232, 240, 226), 'bed1': (226, 232, 246),
         'bed2': (226, 232, 246), 'bath': (234, 234, 240), 'wc': (234, 234, 240),
         'hall': (246, 246, 238)}
rooms = L["rooms"]
for k in (0, 1):                      # ۰ = واحد A (غرب) | ۱ = واحد B (قرینه)
    base = 0 if k == 0 else UW + CORE_W
    # ایوان
    liv = [r for r in rooms if r['k'] == 'living'][0]
    bx0 = liv['x'] if k == 0 else UW - liv['x'] - liv['w']
    RT(base + bx0, -BALC, base + bx0 + liv['w'], 0, fill=(250, 240, 214), outline=(190, 150, 60),
       width=1)
    a = T2(base + bx0, 0); b2 = T2(base + bx0 + liv['w'], -BALC)
    txt(((a[0] + b2[0]) / 2, (a[1] + b2[1]) / 2), f"ایوان {u['balcony']} m²", size=13, fill=(120, 85, 20))
    for r in rooms:
        rx = (base + r['x']) if k == 0 else (base + UW - r['x'] - r['w'])
        a = T2(rx, r['y'] + r['d']); b2 = T2(rx + r['w'], r['y'])
        RT(rx, r['y'], rx + r['w'], r['y'] + r['d'], fill=COLOR.get(r['k'], (245, 245, 245)),
           outline=(120, 120, 120), width=1)
        px_, py_ = (a[0] + b2[0]) / 2, (a[1] + b2[1]) / 2
        if r['w'] * sc3 > 90 and r['d'] * sc3 > 34:
            txt((px_, py_ - 9), r['fa'], size=15, fill=(45, 45, 45))
            txt((px_, py_ + 11), f"{r['w']:.2f} × {r['d']:.2f} = {r['a']:.1f} m²", size=12, fill=(90, 90, 90))
        elif r['w'] * sc3 > 50:
            txt((px_, py_ - 5), r['fa'], size=12, fill=(50, 50, 50))
            txt((px_, py_ + 10), f"{r['a']:.1f}", size=11, fill=(95, 95, 95))
# هسته
RT(UW, 0, UW + CORE_W, UD, fill=(222, 222, 228), outline=(110, 110, 110), width=1)
RT(UW, UD - SH_D, UW + SH_W, UD, fill=(150, 190, 150), outline=(60, 120, 60), width=1)
txt((T2(UW + SH_W / 2, UD - SH_D / 2)[0], T2(UW + SH_W / 2, UD - SH_D / 2)[1]), "شفت ۳×۳\nنور و تهویه",
    size=11, fill=(255, 255, 255))
# اجزای هسته
RT(UW + 0.15, 0.15, UW + 1.75, 1.75, fill=(255, 255, 255), outline=(120, 120, 120), width=1)
txt((T2(UW + 0.95, 0.95)[0], T2(UW + 0.95, 0.95)[1]), "آسانسور", size=10, fill=(60, 60, 70))
RT(UW + 1.8, 0.3, UW + 2.85, 5.3, fill=(255, 255, 255), outline=(120, 120, 120), width=1)
txt((T2(UW + 2.3, 2.8)[0], T2(UW + 2.3, 2.8)[1]), "پله", size=11, fill=(60, 60, 70))
txt((T2(UW + 1.5, 6.2)[0], T2(UW + 1.5, 6.2)[1]), "پاگرد", size=10, fill=(60, 60, 70))
# ابعاد
def dimh3(x0, x1, y, label):
    a, b2 = T2(x0, y), T2(x1, y)
    dr.line([a, b2], fill=(180, 60, 60), width=1)
    txt(((a[0] + b2[0]) / 2, a[1] - 12), label, size=12, fill=(170, 50, 50), bg=(253, 252, 248))


def dimv3(y0, y1, x, label):
    a, b2 = T2(x, y0), T2(x, y1)
    dr.line([a, b2], fill=(180, 60, 60), width=1)
    txt((a[0] - 10, (a[1] + b2[1]) / 2), label, size=12, fill=(170, 50, 50), bg=(253, 252, 248))


dimh3(0, UW, -BALC - 0.8, f"{UW:.2f}")
dimh3(UW, UW + CORE_W, -BALC - 0.8, f"{CORE_W:.2f}")
dimh3(UW + CORE_W, BLD_W, -BALC - 0.8, f"{UW:.2f}")
dimh3(0, BLD_W, -BALC - 2.0, f"عرضِ کل {BLD_W:.2f} m")
dimv3(0, UD, BLD_W + 0.9, f"{UD:.2f}")
dimv3(-BALC, 0, BLD_W + 0.9, "۲.۴۰")
txt((cx + cw - 120, cy2 + 30), "واحد A (غرب)", size=13, fill=(70, 70, 70))
txt((cx + cw - 120, cy2 + 50), "واحد B (قرینه)", size=13, fill=(70, 70, 70))
txt((cx + cw / 2, cy + ch - 18),
    f"هر واحد: {u['encl']} m² بسته + {u['balcony']} m² ایوان = {u['sale']} m² فروشی  ·  "
    f"تراکمِ هر طبقه {L['fsr']['check']} m²", size=15, fill=(40, 50, 65))

# ================================================================ D: مقطع
dx, dy, dw, dh = 1320, 570, 580, 520
dy2 = panel(dx, dy, dw, dh, "د — مقطعِ شمالی-جنوبی", "ارتفاع‌ها و ترازها")
sc4 = (dh - 130) / 20.0
ox4 = dx + 90
oy4 = dy + dh - 70


def M2(xm, zm):
    return (ox4 + xm * sc4, oy4 - zm * sc4)


def RM(x0, z0, x1, z1, fill=None, outline=None, width=1):
    a, b2 = M2(x0, z1), M2(x1, z0)
    dr.rectangle([a[0], a[1], b2[0], b2[1]], fill=fill, outline=outline, width=width)


# زمین
dr.line([M2(-3, 0), M2(19, 0)], fill=(120, 90, 60), width=2)
for i in range(14):
    xx = M2(-3 + i * 1.5, 0)
    dr.line([(xx[0], xx[1]), (xx[0] - 6, xx[1] + 10)], fill=(160, 140, 110), width=1)
# پودیوم
RM(0, 0, POD_D, GND_H, fill=(248, 244, 234), outline=(120, 120, 120), width=1)
txt((M2(7.5, 2.1)[0], M2(7.5, 2.1)[1]), "پیلوت — پارکینگ\nارتفاع مفید ۲.۴۰", size=12, fill=(80, 80, 90))
txt((M2(15, 2.1)[0], M2(15, 2.1)[1]), "مغازه\n۴.۲۰", size=12, fill=(120, 80, 20))
# طبقات
for f in range(NFL):
    z0 = GND_H + f * FL_H
    RM(2.67, z0, 2.67 + UD, z0 + FL_H, fill=(250, 250, 252), outline=(120, 120, 120), width=1)
    txt((M2(7.6, z0 + 1.5)[0], M2(7.6, z0 + 1.5)[1]), f"طبقه {f+1}", size=12, fill=(70, 70, 80))
    # ایوان
    RM(0.27, z0, 2.67, z0 + FL_H, fill=(250, 240, 214), outline=(190, 150, 60), width=1)
# جان‌پناه
RM(2.67, TOP, 2.67 + UD, TOP + 1.0, fill=(225, 225, 228), outline=(120, 120, 120), width=1)
# سقفِ پودیوم / تراس
dr.line([M2(2.67 + UD, GND_H), M2(POD_D, GND_H)], fill=(90, 120, 90), width=3)
txt((M2(15.5, GND_H + 0.7)[0], M2(15.5, GND_H + 0.7)[1]), "تراسِ پودیوم", size=11, fill=(35, 95, 45))
# شفت (خط‌چین عمودی)
for z in [GND_H + k * 0.6 for k in range(int((TOP + 1 - GND_H) / 0.6))]:
    dr.line([M2(2.67 + UD - 0.2, z), M2(2.67 + UD - 0.2, z + 0.3)], fill=(70, 130, 70), width=2)
txt((M2(2.67 + UD + 1.2, TOP - 1.5)[0], M2(2.67 + UD + 1.2, TOP - 1.5)[1]), "شفت ۳×۳\nتا بام", size=10,
    fill=(40, 110, 50))
# ترازها
for z, lab in [(0, "۰.۰۰"), (GND_H, "۴.۲۰"), (TOP, "۱۶.۲۰"), (TOP + 1.0, "۱۷.۲۰")]:
    a = M2(-2.4, z)
    dr.line([a, M2(19.5, z)], fill=(180, 60, 60), width=1)
    txt((a[0] - 26, a[1]), lab, size=11, fill=(170, 50, 50), bg=(253, 252, 248))
txt((M2(8, -1.4)[0], M2(8, -1.4)[1]), "فضای بازِ جنوبی ۲.۶۷ m + حریمِ دکل ۷.۰۸ m", size=11,
    fill=(40, 95, 45))
txt((M2(8, TOP + 2.2)[0], M2(8, TOP + 2.2)[1]), f"ارتفاعِ کل ≈ {TOP+1.0:.2f} m (۵ طبقه)", size=12,
    fill=(60, 60, 70))

# ================================================================ E: حجم سه‌بعدی
ex, ey, ew, eh = 20, 1100, 1860, 740
ey2 = panel(ex, ey, ew, eh, "ه — حجمِ سه‌بعدی", "پیلوت + ۴ طبقه + ایوانِ سراسری + شفتِ میانی")
C_ST, C_GRN, C_SITE = (206, 206, 206), (198, 228, 198), (226, 224, 214)
C_POD, C_POD_S, C_POD_T = (243, 206, 150), (232, 189, 128), (252, 236, 214)
C_PK, C_PK_S, C_PK_T = (206, 218, 234), (188, 203, 224), (232, 238, 246)
C_R, C_R_S, C_R_T = (226, 234, 244), (208, 218, 232), (248, 250, 252)
C_TER, C_SH = (196, 230, 196), (150, 190, 150)
C30, S30 = math.cos(math.radians(30)), math.sin(math.radians(30))
S = 14.0
iso = lambda x, y, z: (ex + 80 + (x + y) * C30 * S, ey2 + 330 + (x - y) * S30 * S - z * S)


def shade(c, f):
    return tuple(max(0, min(255, int(v * f))) for v in c)


def box3(x0, y0, z0, x1, y1, z1, t, e, s, edge=(105, 105, 108), floors=None, stripes=None):
    dr.polygon([iso(x0, y0, z0), iso(x1, y0, z0), iso(x1, y0, z1), iso(x0, y0, z1)], fill=s,
               outline=edge, width=1)
    if stripes:
        x = x0 + stripes
        while x < x1:
            dr.line([iso(x, y0, z0 + 0.35), iso(x, y0, z1 - 0.35)], fill=shade(s, .86), width=2)
            x += stripes
    dr.polygon([iso(x1, y0, z0), iso(x1, y1, z0), iso(x1, y1, z1), iso(x1, y0, z1)], fill=e,
               outline=edge, width=1)
    dr.polygon([iso(x0, y0, z1), iso(x1, y0, z1), iso(x1, y1, z1), iso(x0, y1, z1)], fill=t,
               outline=edge, width=1)
    if floors:
        for z in floors:
            dr.line([iso(x0, y0, z), iso(x1, y0, z)], fill=edge, width=1)
            dr.line([iso(x1, y0, z), iso(x1, y1, z)], fill=edge, width=1)


blks = []
for (a, bb, c, d, z, col) in [(0, D, W, D + 3.4, 0, C_ST), (0, -4.6, W, 0, 0, C_GRN),
                              (0, 0, W, D, 0, C_SITE), (W, 0, W + 4.2, D, 0, C_ST)]:
    blks.append((0, a - bb, a, bb, -0.45, c, d, z, col, shade(col, .9), shade(col, .82), (150, 150, 150)))
blks.append((0, 0, 0, 0, 0, W, Y0, 0.06, (206, 234, 206), (200, 230, 200), (194, 226, 194), (140, 180, 140)))
blks.append((1, -Y0, 0, Y0, 0, SHOP_X0, D, GND_H, C_PK_T, C_PK, C_PK_S, (105, 105, 108)))
blks.append((1, SHOP_X0 - Y0, SHOP_X0, Y0, 0, W, D, GND_H, C_POD_T, C_POD, C_POD_S, (105, 105, 108)))
blks.append((2, BLD_W - Y0, BLD_W, Y0, GND_H, W, D, GND_H + 0.25, C_TER, shade(C_TER, .92),
             shade(C_TER, .86), (105, 105, 108)))
YS = Y0 + BALC
fl = [GND_H + k * FL_H for k in range(1, NFL)]
# دو بالِ مسکونی + شفت بین‌شان (شفت در هسته)
blks.append((2, -YS, 0, YS, GND_H, UW, Y1, TOP, C_R_T, C_R, C_R_S, (105, 105, 108)))
blks.append((2, UW - YS, UW, YS, GND_H, UW + SH_W, Y1 - SH_D, TOP, C_R_T, C_R, C_R_S, (105, 105, 108)))
blks.append((2, UW + SH_W - YS, UW + SH_W, YS, GND_H, UW + CORE_W, Y1, TOP, C_R_T, C_R, C_R_S,
             (105, 105, 108)))
blks.append((2, UW + CORE_W - YS, UW + CORE_W, YS, GND_H, BLD_W, Y1, TOP, C_R_T, C_R, C_R_S,
             (105, 105, 108)))
blks.append((2, UW - (Y1 - SH_D), UW, Y1 - SH_D, GND_H, UW + SH_W, Y1, GND_H + 0.3, C_SH,
             shade(C_SH, .9), shade(C_SH, .82), (60, 120, 60)))
# ایوان‌ها
liv = [r for r in rooms if r['k'] == 'living'][0]
for f in range(NFL):
    z = GND_H + f * FL_H
    blks.append((3, liv['x'] - Y0 + z, liv['x'], Y0, z, liv['x'] + liv['w'], YS, z + 1.05,
                 (250, 240, 214), (236, 214, 160), (226, 200, 140), (105, 105, 108)))
    xb = UW + CORE_W + UW - liv['x'] - liv['w']
    blks.append((3, xb - Y0 + z, xb, Y0, z, xb + liv['w'], YS, z + 1.05,
                 (250, 240, 214), (236, 214, 160), (226, 200, 140), (105, 105, 108)))
for (g, k, x0, y0, z0, x1, y1, z1, t, e, s, edge) in sorted(blks, key=lambda b: (b[0], b[1])):
    box3(x0, y0, z0, x1, y1, z1, t, e, s, edge=edge,
         floors=fl if (g == 2 and z1 > TOP - 0.1) else None,
         stripes=2.5 if (g == 1 and x0 == 0) else None)
txt((ex + 16, ey + 20), "پیلوت: ارتفاعِ مفیدِ پارکینگ ۲.۴۰ m (معاف از تراکم)", size=13, fill=(70, 80, 95),
    anchor="lm")

# ================================================================ F: جداول
fx, fy, fw, fh = 20, 1850, 1860, 830
fy2 = panel(fx, fy, fw, fh, "و — جداول، کنترلِ ضوابط و پرسش‌های باقی‌مانده")
col = [fx + 30, fx + 500, fx + 980, fx + 1450]

# ۱: مساحتِ واحد
txt((col[0], fy2 + 26), "۱) مساحتِ یک واحد (طبقهٔ تیپ)", size=18, bold=True, fill=(24, 42, 64), anchor="lm")
rows1 = [(r['fa'], f"{r['a']:.1f}") for r in sorted(rooms, key=lambda r: -r['a'])]
rows1 += [("جمعِ فضای بسته", f"{u['encl']:.1f}"), ("ایوان (۵۰٪ در تراکم)", f"{u['balcony']:.1f}")]
yy = fy2 + 56
for i, (a, b3) in enumerate(rows1):
    last = i >= len(rows1) - 2
    txt((col[0] + 8, yy), a, size=15, fill=(45, 45, 45), anchor="lm",
        bold=last)
    txt((col[0] + 250, yy), b3, size=15, fill=(45, 45, 45), anchor="lm", bold=last)
    yy += 26
txt((col[0] + 8, yy + 8), "مساحتِ فروشیِ واحد (سند):", size=17, bold=True, fill=(20, 90, 45), anchor="lm")
txt((col[0] + 250, yy + 8), f"{u['sale']} m²", size=17, bold=True, fill=(20, 90, 45), anchor="lm")

# ۲: زیربنا
txt((col[1], fy2 + 26), "۲) جدولِ زیربنا (فرمِ شهرداری)", size=18, bold=True, fill=(24, 42, 64), anchor="lm")
gnd = 175.5 + 17.1
rows2 = [("همکف — ۳ مغازه (۳ × ۵۲ m²)", "۱۵۶.۰"), ("همکف — انبار/سرویسِ تجاری", "۱۹.۵"),
         ("همکف — لابی و هسته", "۱۷.۱"), ("پیلوت — پارکینگ (معاف از تراکم)", "—"),
         ("طبقات ۱ تا ۴ — هر طبقه ۲ واحد", f"{4*L['fsr']['check']:.0f}"),
         ("جمعِ زیربنای مشمولِ تراکم", f"{4*L['fsr']['check']+gnd:.0f}"),
         ("تراکمِ مجاز (۱۸۰٪ × ۵۴۲.۳۸)", "۹۷۶")]
yy = fy2 + 56
for i, (a, b3) in enumerate(rows2):
    last = i >= len(rows2) - 2
    txt((col[1] + 8, yy), a, size=15, fill=(45, 45, 45), anchor="lm", bold=last)
    txt((col[1] + 330, yy), b3, size=15, fill=(45, 45, 45), anchor="lm", bold=last)
    yy += 26

# ۳: کنترلِ ضوابط
txt((col[2], fy2 + 26), "۳) کنترلِ تطبیق با مقررات", size=18, bold=True, fill=(24, 42, 64), anchor="lm")
checks = [
    ("سطح اشغال", f"{BLD_W*POD_D:.0f} m² از {OCC_AREA:.0f} m² مجاز (۸۰٪)", True),
    ("تراکم", f"{4*L['fsr']['check']+gnd:.0f} از ۹۷۶ m²", True),
    ("بالکنِ هر واحد", f"{u['balcony']} m² ≥ ۳ m² (الزامِ اصفهان)", True),
    ("عرضِ نشیمن", "۶.۸۱ m ≥ ۳.۰۰ m", True),
    ("عرضِ خواب / آشپزخانه", "۵.۳۴ / ۲.۷۲ m ≥ ۲.۵۰ m", True),
    ("عمقِ نورگیری", "۴.۱۵ m ≤ ۷.۰۰ m", True),
    ("شفت (غیراقامتی)", "۹ m² با عرض ۳ m ≥ ۶ m² / ۲ m", True),
    ("تهویهٔ متقاطع", "پنجره در شمال و جنوب (دیوارِ روبه‌رو)", True),
]
yy = fy2 + 56
for a, b3, ok in checks:
    txt((col[2] + 8, yy), ("✓ " if ok else "✗ ") + a, size=15, fill=(20, 90, 45) if ok else (160, 45, 40),
        anchor="lm")
    txt((col[2] + 200, yy), b3, size=13, fill=(75, 75, 75), anchor="lm", max_w=230)
    yy += 27

# ۴: پارکینگ و هشدارها
txt((col[3], fy2 + 26), "۴) پارکینگ و هشدارها", size=18, bold=True, fill=(24, 42, 64), anchor="lm")
warn = [
    ("پارکینگ در پیلوت", "۶ فضا (۲ جایگاه در دو سویِ هسته)"),
    ("نیازِ برآوردی", "۸ مسکونی + ۲ تا ۴ تجاری = ۱۰ تا ۱۲"),
    ("راه‌حلِ پیشنهادی", "زیرزمینِ ۲۳۶ m² ⇒ +۹ فضا (جمع ۱۵)"),
    ("جایگزین", "پرداختِ جریمه برای ۴ تا ۶ فضای کسری"),
    ("تراکم", "اگر ۲۴۰٪ باشد: زیربنا ۱۳۰۲ m² (+۳۳٪)"),
    ("ارتفاع", "محدودیتِ احتمالیِ حریمِ خطِ برق"),
    ("اعتبارِ استعلام", "صدور ۱۴۰۲/۰۳/۲۸ — اعتبار ۳ ماهه"),
]
yy = fy2 + 56
for a, b3 in warn:
    txt((col[3] + 8, yy), a, size=14, fill=(150, 60, 30), anchor="lm", max_w=200)
    txt((col[3] + 215, yy), b3, size=13, fill=(60, 60, 70), anchor="lm", max_w=190)
    yy += 30

# ۵) قبل و بعد
yy = fy2 + 250
txt((col[0], yy), "۵) این طرح در برابر طرحوارهٔ اولیهٔ ۵", size=18, bold=True, fill=(24, 42, 64), anchor="lm")
cmp_rows = [("مساحتِ فروشیِ هر واحد", "۷۹.۲ m²", f"{u['sale']} m²", "+۱۶.۳"),
            ("جمعِ زیربنای فروشی (۸ واحد)", "۶۳۳ m²", f"{L['total_sale_res']} m²", "+۱۳۱"),
            ("نمای خارجیِ هر طبقه", "۸۴ m", f"{b['facade_per_floor']} m", "−۱۴"),
            ("بالکن (الزامی در اصفهان)", "ندارد", f"{u['balcony']} m²", "✓"),
            ("عمقِ نورگیریِ هر فضا", "تا ۱۰.۷ m", "≤ ۴.۲ m", "✓"),
            ("نورگیرِ کارا", "۲ متر (بی‌اثر)", "شفت ۳×۳", "✓")]
yy += 30
for a, b1, b2_, d_ in cmp_rows:
    txt((col[0] + 8, yy), a, size=14, fill=(55, 62, 75), anchor="lm", max_w=280)
    txt((col[0] + 300, yy), b1, size=14, fill=(150, 60, 30), anchor="lm")
    txt((col[0] + 400, yy), b2_, size=14, fill=(20, 90, 45), anchor="lm", bold=True)
    txt((col[0] + 520, yy), d_, size=14, fill=(20, 90, 45), anchor="lm")
    yy += 24

# پانوشت
fn = fy + fh - 150
dr.rectangle([fx + 16, fn - 16, fx + fw - 16, fn + 118], fill=(238, 242, 247), outline=(160, 175, 195),
             width=1)
txt((fx + 36, fn + 8), "جمع‌بندی: نسبت به طرحوارهٔ اولیهٔ ۵، این طرح ۱۳۱ m² مساحتِ فروشیِ بیشتر "
                       "(۷۶۴ در برابر ۶۳۳ m²) و نمای کمتر (۷۰ در برابر ۸۴ m در هر طبقه) دارد،",
    size=16, fill=(40, 50, 65), anchor="lm", max_w=fw - 80)
txt((fx + 36, fn + 36), "و هر ۸ واحد از نورِ دوطرفه و تهویهٔ متقاطعِ واقعی برخوردارند. ایوانِ ۲.۴ متری "
                        "تنها نیمی از مساحتش در تراکم حساب می‌شود — یعنی ۱۶.۳ m² فضای خصوصی با ۸.۲ m² تراکم.",
    size=16, fill=(40, 50, 65), anchor="lm", max_w=fw - 80)
txt((fx + 36, fn + 64), "شفتِ ۳×۳ متر در هسته، نور و تهویهٔ طبیعیِ پاگرد را تأمین می‌کند "
                        "(حدِّ مؤثرِ پژوهش برای ۴ طبقه) بدون آنکه نمای سراسریِ یک نورگیر را بپردازید.",
    size=16, fill=(40, 50, 65), anchor="lm", max_w=fw - 80)
txt((fx + 36, fn + 92), "پیش از اجرا: پاسخِ ۷ پرسشِ انتهای research-notes.md را از شهرداری بگیرید — "
                        "به‌ویژه تراکمِ مجاز و معافیتِ پارکینگِ پیلوت.",
    size=16, fill=(160, 45, 40), anchor="lm", max_w=fw - 80)

img.save(OUT)
print("saved:", OUT, img.size)
