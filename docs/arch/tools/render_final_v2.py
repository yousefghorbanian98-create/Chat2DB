#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""نسخهٔ کاملِ پیشنهادِ نهایی:
   ۵ طبقهٔ مسکونی (۱۰ واحد) + نیم‌طبقه در ۳ مغازه + سطحِ انباریِ معاف از تراکم + ایوانِ سراسری + شفتِ ۳×۳
خروجی: docs/arch/final-design-v2.png
"""
import math, os, json
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display

HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT = os.path.join(HERE, "docs", "arch", "final-design-v2.png")
FDIR = "/home/user/fonts"
L = json.load(open(os.path.join(HERE, "docs", "arch", "final-layout.json"), encoding="utf-8"))
V = json.load(open('/tmp/v2.json', encoding='utf-8'))

# ---------------------------------------------------------------- ابعاد
W, D, NET = 40.57, 13.37, 542.38
Y0, Y1 = 2.67, 13.37
POD_D = 10.70
UW, UD = L["unit"]["w"], L["unit"]["d"]
BALC, CORE_W = 2.40, L["building"]["core_w"]
BLD_W = 2 * UW + CORE_W
SH_W, SH_D = 3.00, 3.00
YS = Y0 + BALC
NFL, FL_H, POD_H = V['nfl'], V['fl_h'], V['pod']
PARK_H, ANB_H = V['park_h'], V['anb_h']
SHOP_X0, SHOP_DEEP, SHOP_W, NSHOP = 21.07, 7.00, 6.50, 3
ANB_N, ANB_A = 8, 5.0
TOP = POD_H + NFL * FL_H

P = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")
_c = {}


def fa(t):
    return get_display(arabic_reshaper.reshape(str(t).translate(P)))


def F(sz, bold=False):
    if (sz, bold) not in _c:
        _c[(sz, bold)] = ImageFont.truetype(
            os.path.join(FDIR, "Vazirmatn-Bold.ttf" if bold else "Vazirmatn-Regular.ttf"), sz)
    return _c[(sz, bold)]


CW, CH = 1920, 2500
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
    txt((x + 14, y + 22), title, size=18, bold=True, fill=(24, 42, 64), anchor="lm")
    if sub:
        txt((x + w - 14, y + 22), sub, size=13, fill=(95, 105, 122), anchor="rm", max_w=w - 260)
    return y + 44


# ================================================================ سربرگ
dr.rectangle([0, 0, CW, 110], fill=(26, 40, 58))
txt((CW // 2, 30), "نسخهٔ کامل — ۵ طبقه (۱۰ واحد) + نیم‌طبقهٔ تجاری + انباریِ معاف از تراکم",
    size=31, bold=True, fill=(255, 255, 255))
txt((CW // 2, 62),
    f"هر واحد {L['unit']['sale']} m² ({L['unit']['encl']} بسته + {L['unit']['balcony']} ایوان) · "
    f"فروشیِ مسکونی {V['sale_res']:.0f} m² · تراکمِ محاسبه‌ای {V['far']}٪ · ارتفاع ≈ {TOP:.1f} m",
    size=18, fill=(198, 214, 236))
txt((CW // 2, 90),
    f"مازاد بر ۱۸۰٪: {V['mazad_180']} m² باید خریداری شود (اصفهان تراکمِ مازاد می‌فروشد — ضریبِ طبقهٔ پنجم ۱.۲)",
    size=16, fill=(255, 210, 150))

# ================================================================ A: سایت‌پلان
ax, ay, aw, ah = 20, 120, 620, 400
ay2 = panel(ax, ay, aw, ah, "الف — سایت‌پلان")
sc = min((aw - 70) / (W + 8), (ah - 60) / (D + 8))
ox = ax + 35 + (aw - 70 - W * sc) / 2
oy = ay2 + 8 + (D + 4) * sc


def S2(x, y):
    return (ox + x * sc, oy - y * sc)


def RS(x0, y0, x1, y1, fill=None, outline=None, width=1):
    a, b2 = S2(x0, y1), S2(x1, y0)
    dr.rectangle([a[0], a[1], b2[0], b2[1]], fill=fill, outline=outline, width=width)


RS(-4, -4, W + 4, D + 4, fill=(250, 250, 248))
RS(0, D, W, D + 4, fill=(206, 206, 206))
RS(W, 0, W + 4, D, fill=(206, 206, 206))
RS(0, -4, W, 0, fill=(198, 228, 198))
RS(0, 0, W, D, fill=(255, 255, 255), outline=(200, 60, 60), width=2)
RS(0, Y0, BLD_W, Y1, fill=(232, 240, 226), outline=(90, 120, 90), width=2)
RS(0, Y0, BLD_W, YS, fill=(250, 240, 214), outline=(190, 150, 60), width=1)
RS(BLD_W, Y0, W, Y1, fill=(222, 240, 222), outline=(90, 120, 90), width=1)
RS(UW, Y1 - SH_D, UW + SH_W, Y1, fill=(150, 190, 150), outline=(60, 120, 60), width=1)
txt(((S2(BLD_W, Y0)[0] + S2(W, Y1)[0]) / 2, (S2(BLD_W, Y0)[1] + S2(W, Y1)[1]) / 2),
    f"تراسِ پودیوم\n{L['building']['terrace']} m²", size=13, fill=(35, 95, 45))
tx, ty = S2(8, -2.2)
dr.line([(tx - 8, ty), (tx, ty - 60)], fill=(95, 95, 95), width=2)
dr.line([(tx + 8, ty), (tx, ty - 60)], fill=(95, 95, 95), width=2)
dr.line([(tx - 12, ty - 42), (tx + 12, ty - 42)], fill=(95, 95, 95), width=2)


def dh(x0, x1, y, lb):
    a, b2 = S2(x0, y), S2(x1, y)
    dr.line([a, b2], fill=(180, 60, 60), width=1)
    txt(((a[0] + b2[0]) / 2, a[1] - 10), lb, size=11, fill=(170, 50, 50), bg=(250, 250, 248))


dh(0, BLD_W, D + 2.2, f"{BLD_W:.2f}")
dh(0, W, -5.4, f"{W:.2f}")
txt((S2(BLD_W / 2, Y0 + BALC / 2)[0], S2(BLD_W / 2, Y0 + BALC / 2)[1]), "ایوان ۲.۴۰", size=11, fill=(120, 85, 20))
txt((S2(30, D + 2)[0], S2(30, D + 2)[1]), "گذر ۸ متری", size=12, fill=(70, 70, 70))
txt((S2(W + 2, D / 2)[0], S2(W + 2, D / 2)[1]), "معبر ۲۶–۲۹ متری", size=11, fill=(70, 70, 70))
txt((S2(22, -2.2)[0], S2(22, -2.2)[1]), "حریمِ دکلِ فشارقوی", size=10, fill=(40, 95, 45))
dr.line([S2(UW + 1.5, Y1), S2(UW + 1.5, Y1 + 1.4)], fill=(60, 90, 160), width=3)
dr.line([S2(1.0, Y1), S2(1.0, Y1 + 1.4)], fill=(200, 120, 40), width=3)

# ================================================================ B: همکف
bx, by, bw, bh = 660, 120, 620, 400
by2 = panel(bx, by, bw, bh, "ب — همکف / پیلوت", "ارتفاع ۵.۴۰: ۳ مغازهٔ دوقلو + پارکینگِ ۲.۴۰")
s2 = (bw - 70) / (W + 2)
ox2 = bx + 35
oy2 = by2 + 14 + POD_D * s2


def G2(x, y):
    return (ox2 + x * s2, oy2 - y * s2)


def RG(x0, y0, x1, y1, fill=None, outline=None, width=1):
    a, b2 = G2(x0, y1), G2(x1, y0)
    dr.rectangle([a[0], a[1], b2[0], b2[1]], fill=fill, outline=outline, width=width)


RG(0, 0, W, POD_D, fill=(255, 255, 255), outline=(120, 120, 120), width=2)
RG(0, 0, SHOP_X0, POD_D, fill=(235, 240, 247))
n = 0
for bay in (0.5, 13.0):
    for i in range(3):
        x0 = bay + i * 2.65
        RG(x0, 0.4, x0 + 2.5, 0.4 + 5.0, fill=(255, 255, 255), outline=(110, 140, 190), width=1)
        n += 1
        txt((G2(x0 + 1.25, 2.9)[0], G2(x0 + 1.25, 2.9)[1]), str(n), size=11, fill=(90, 120, 170))
txt((G2(4.7, 8.2)[0], G2(4.7, 8.2)[1]), "مسیرِ تردد", size=12, fill=(70, 100, 150))
txt((G2(16.8, 8.2)[0], G2(16.8, 8.2)[1]), "مسیرِ تردد", size=12, fill=(70, 100, 150))
RG(UW, 5.6, UW + CORE_W, POD_D, fill=(214, 214, 220), outline=(110, 110, 110), width=1)
txt((G2(UW + 1.5, 8.4)[0], G2(UW + 1.5, 8.4)[1]), "لابی\nپله\nآسانسور", size=10, fill=(60, 60, 70))
for i in range(NSHOP):
    x0 = SHOP_X0 + i * SHOP_W
    RG(x0, POD_D - SHOP_DEEP, x0 + SHOP_W, POD_D, fill=(252, 236, 214), outline=(170, 120, 50), width=1)
    txt((G2(x0 + SHOP_W / 2, POD_D - SHOP_DEEP / 2)[0], G2(x0 + SHOP_W / 2, POD_D - SHOP_DEEP / 2)[1]),
        f"مغازه {i+1}\n{SHOP_W*SHOP_DEEP:.0f} m²\n+ نیم‌طبقه {V['mez_phys']:.0f}", size=11, fill=(120, 80, 20))
RG(SHOP_X0, 0, W, POD_D - SHOP_DEEP, fill=(243, 243, 236), outline=(170, 170, 170), width=1)
txt((G2((SHOP_X0 + W) / 2, 1.0)[0], G2((SHOP_X0 + W) / 2, 1.0)[1]), "انبار و سرویسِ مغازه‌ها", size=11,
    fill=(90, 90, 90))
txt((G2(SHOP_X0 / 2, POD_D + 1.2)[0], G2(SHOP_X0 / 2, POD_D + 1.2)[1]), "پارکینگ ۶ فضا — ارتفاعِ مفید ۲.۴۰ (معاف)",
    size=12, fill=(70, 100, 150))
txt((G2(W / 2, POD_D + 1.2)[0], G2(W / 2, POD_D + 1.2)[1]), "برِ تجاری ۱۹.۵ m — ارتفاع ۵.۴۰", size=12,
    fill=(120, 80, 20))

# ================================================================ C: سطحِ انباری و نیم‌طبقه
cxx, cyy, cww, chh = 1300, 120, 600, 400
cy2 = panel(cxx, cyy, cww, chh, "ج — سطحِ انباری و نیم‌طبقه", "تراز ۲.۶۰+ — معاف از تراکم")
s3 = (cww - 70) / (W + 2)
ox3 = cxx + 35
oy3 = cy2 + 14 + POD_D * s3


def A2(x, y):
    return (ox3 + x * s3, oy3 - y * s3)


def RA(x0, y0, x1, y1, fill=None, outline=None, width=1):
    a, b2 = A2(x0, y1), A2(x1, y0)
    dr.rectangle([a[0], a[1], b2[0], b2[1]], fill=fill, outline=outline, width=width)


RA(0, 0, W, POD_D, fill=(255, 255, 255), outline=(120, 120, 120), width=2)
RA(0, 0, SHOP_X0, POD_D, fill=(246, 243, 232))
# ردیفِ انباری
for i in range(ANB_N):
    x0 = 0.4 + i * 2.60
    RA(x0, 0.4, x0 + 2.4, 0.4 + 2.2, fill=(255, 255, 255), outline=(150, 130, 90), width=1)
    txt((A2(x0 + 1.2, 1.5)[0], A2(x0 + 1.2, 1.5)[1]), f"ا{i+1}", size=11, fill=(120, 100, 60))
txt((A2(10.4, 4.6)[0], A2(10.4, 4.6)[1]), "راهروی انباری‌ها ۱.۲۰ m", size=11, fill=(120, 100, 60))
txt((A2(10.4, 7.6)[0], A2(10.4, 7.6)[1]), "فضای باز (نورگیرِ پارکینگ)", size=11, fill=(110, 130, 110))
# نیم‌طبقهٔ مغازه‌ها
for i in range(NSHOP):
    x0 = SHOP_X0 + i * SHOP_W
    RA(x0, POD_D - SHOP_DEEP, x0 + SHOP_W, POD_D - SHOP_DEEP + 4.5, fill=(252, 236, 214),
       outline=(170, 120, 50), width=1)
    txt((A2(x0 + SHOP_W / 2, POD_D - SHOP_DEEP + 2.2)[0],
         A2(x0 + SHOP_W / 2, POD_D - SHOP_DEEP + 2.2)[1]),
        f"نیم‌طبقه {i+1}\n{V['mez_phys']:.0f} m²", size=11, fill=(120, 80, 20))
RA(SHOP_X0, 0, W, POD_D - SHOP_DEEP, fill=(243, 243, 236), outline=(170, 170, 170), width=1)
txt((A2((SHOP_X0 + W) / 2, 1.6)[0], A2((SHOP_X0 + W) / 2, 1.6)[1]), "سرویسِ مغازه‌ها", size=11,
    fill=(90, 90, 90))
txt((A2(W / 2, POD_D + 1.2)[0], A2(W / 2, POD_D + 1.2)[1]),
    "نیم‌طبقه: تنها ۲۰٪ (حداکثر ۲۰ m²) در تراکم · انباری: کاملاً معاف", size=12, fill=(40, 100, 50))

# ================================================================ D: طبقهٔ تیپ
dx, dy, dw, dh_ = 20, 540, 1220, 480
dy2 = panel(dx, dy, dw, dh_, "د — پلانِ طبقهٔ تیپ (طبقات ۱ تا ۵)",
            "۲ واحد + هسته + شفتِ ۳×۳ + ایوانِ ۲.۴۰ — تکرار در ۵ طبقه")
s4 = min((dw - 240) / BLD_W, (dh_ - 44 - 110) / (UD + BALC))
ox4 = dx + 120
oy4 = dy2 + 40 + UD * s4


def T2(x, y):
    return (ox4 + x * s4, oy4 - y * s4)


def RT(x0, y0, x1, y1, fill=None, outline=None, width=1):
    a, b2 = T2(x0, y1), T2(x1, y0)
    dr.rectangle([a[0], a[1], b2[0], b2[1]], fill=fill, outline=outline, width=width)


COLOR = {'living': (250, 235, 205), 'kitchen': (232, 240, 226), 'bed1': (226, 232, 246),
         'bed2': (226, 232, 246), 'bath': (234, 234, 240), 'wc': (234, 234, 240),
         'hall': (246, 246, 238)}
rooms = L["rooms"]
liv = [r for r in rooms if r['k'] == 'living'][0]
for k in (0, 1):
    base = 0 if k == 0 else UW + CORE_W
    bx0 = liv['x'] if k == 0 else UW - liv['x'] - liv['w']
    RT(base + bx0, -BALC, base + bx0 + liv['w'], 0, fill=(250, 240, 214), outline=(190, 150, 60), width=1)
    txt(((T2(base + bx0, 0)[0] + T2(base + bx0 + liv['w'], -BALC)[0]) / 2,
         (T2(base + bx0, 0)[1] + T2(base + bx0 + liv['w'], -BALC)[1]) / 2),
        f"ایوان {L['unit']['balcony']} m²", size=13, fill=(120, 85, 20))
    for r in rooms:
        rx = (base + r['x']) if k == 0 else (base + UW - r['x'] - r['w'])
        RT(rx, r['y'], rx + r['w'], r['y'] + r['d'], fill=COLOR.get(r['k'], (245, 245, 245)),
           outline=(120, 120, 120), width=1)
        px_, py_ = (T2(rx, r['y'] + r['d'])[0] + T2(rx + r['w'], r['y'])[0]) / 2, \
                   (T2(rx, r['y'] + r['d'])[1] + T2(rx + r['w'], r['y'])[1]) / 2
        if r['w'] * s4 > 90 and r['d'] * s4 > 34:
            txt((px_, py_ - 9), r['fa'], size=15, fill=(45, 45, 45))
            txt((px_, py_ + 11), f"{r['w']:.2f} × {r['d']:.2f} = {r['a']:.1f} m²", size=12, fill=(90, 90, 90))
        elif r['w'] * s4 > 50:
            txt((px_, py_ - 5), r['fa'], size=12, fill=(50, 50, 50))
            txt((px_, py_ + 10), f"{r['a']:.1f}", size=11, fill=(95, 95, 95))
RT(UW, 0, UW + CORE_W, UD, fill=(222, 222, 228), outline=(110, 110, 110), width=1)
RT(UW, UD - SH_D, UW + SH_W, UD, fill=(150, 190, 150), outline=(60, 120, 60), width=1)
txt((T2(UW + SH_W / 2, UD - SH_D / 2)[0], T2(UW + SH_W / 2, UD - SH_D / 2)[1]), "شفت ۳×۳", size=12,
    fill=(255, 255, 255))
RT(UW + 0.15, 0.15, UW + 1.75, 1.75, fill=(255, 255, 255), outline=(120, 120, 120), width=1)
txt((T2(UW + 0.95, 0.95)[0], T2(UW + 0.95, 0.95)[1]), "آسانسور", size=10, fill=(60, 60, 70))
RT(UW + 1.8, 0.3, UW + 2.85, 5.3, fill=(255, 255, 255), outline=(120, 120, 120), width=1)
txt((T2(UW + 2.3, 2.8)[0], T2(UW + 2.3, 2.8)[1]), "پله", size=11, fill=(60, 60, 70))


def dh4(x0, x1, y, lb):
    a, b2 = T2(x0, y), T2(x1, y)
    dr.line([a, b2], fill=(180, 60, 60), width=1)
    txt(((a[0] + b2[0]) / 2, a[1] - 12), lb, size=11, fill=(170, 50, 50), bg=(253, 252, 248))


dh4(0, UW, -BALC - 0.8, f"{UW:.2f}")
dh4(UW, UW + CORE_W, -BALC - 0.8, f"{CORE_W:.2f}")
dh4(UW + CORE_W, BLD_W, -BALC - 0.8, f"{UW:.2f}")
dh4(0, BLD_W, -BALC - 2.1, f"عرضِ کل {BLD_W:.2f} m")
txt((dx + dw / 2, dy + dh_ - 18),
    f"هر واحد {L['unit']['encl']} m² بسته + {L['unit']['balcony']} m² ایوان = {L['unit']['sale']} m² فروشی · "
    f"تراکمِ هر طبقه {L['fsr']['check']} m² · تکرار در ۵ طبقه = ۱۰ واحد", size=15, fill=(40, 50, 65))

# ================================================================ E: مقطع
ex, ey, ew, eh = 1260, 540, 640, 480
ey2 = panel(ex, ey, ew, eh, "ه — مقطعِ شمالی-جنوبی", "ترازها و ارتفاع‌ها")
s5 = min((ew - 150) / 21.0, (eh - 120) / 23.0)
ox5 = ex + 100
oy5 = ey + eh - 46


def M2(x, z):
    return (ox5 + x * s5, oy5 - z * s5)


def RM(x0, z0, x1, z1, fill=None, outline=None, width=1):
    a, b2 = M2(x0, z1), M2(x1, z0)
    dr.rectangle([a[0], a[1], b2[0], b2[1]], fill=fill, outline=outline, width=width)


dr.line([M2(-3, 0), M2(19, 0)], fill=(120, 90, 60), width=2)
# پودیومِ غربی: پارکینگ + انباری
RM(2.67, 0, 13.37, PARK_H + 0.20, fill=(235, 240, 247), outline=(120, 120, 120), width=1)
txt((M2(8.0, 1.3)[0], M2(8.0, 1.3)[1]), "پارکینگ — ارتفاعِ مفید ۲.۴۰ (معاف از تراکم)", size=11, fill=(70, 100, 150))
RM(2.67, PARK_H + 0.20, 13.37, PARK_H + 0.20 + ANB_H + 0.20, fill=(246, 243, 232), outline=(120, 120, 120), width=1)
txt((M2(8.0, PARK_H + 1.4)[0], M2(8.0, PARK_H + 1.4)[1]), "انباری — ارتفاع ۲.۲۰ (معاف)", size=11, fill=(120, 100, 60))
RM(2.67, 4.80, 13.37, POD_H, fill=(228, 228, 232), outline=(180, 180, 180), width=1)
txt((M2(8.0, 5.1)[0], M2(8.0, 5.1)[1]), "فضای تأسیسات ۰.۶۰", size=9, fill=(110, 110, 110))
# طبقات
for f in range(NFL):
    z0 = POD_H + f * FL_H
    RM(2.67, z0, 13.37, z0 + FL_H, fill=(250, 250, 252), outline=(120, 120, 120), width=1)
    txt((M2(8.0, z0 + 1.5)[0], M2(8.0, z0 + 1.5)[1]), f"طبقه {f+1}", size=11, fill=(70, 70, 80))
    RM(0.27, z0, 2.67, z0 + FL_H, fill=(250, 240, 214), outline=(190, 150, 60), width=1)
RM(2.67, TOP, 13.37, TOP + 1.0, fill=(225, 225, 228), outline=(120, 120, 120), width=1)
dr.line([M2(13.37, POD_H), M2(19, POD_H)], fill=(90, 120, 90), width=3)
txt((M2(16.5, POD_H + 0.8)[0], M2(16.5, POD_H + 0.8)[1]), "تراس", size=11, fill=(35, 95, 45))
for z in [POD_H + k * 0.6 for k in range(int((TOP + 1 - POD_H) / 0.6))]:
    dr.line([M2(12.9, z), M2(12.9, z + 0.3)], fill=(70, 130, 70), width=2)
for z, lab in [(0, "۰.۰۰"), (PARK_H + 0.2, "۲.۶۰"), (POD_H, "۵.۴۰"), (TOP, "۱۹.۹۰"), (TOP + 1, "۲۰.۹۰")]:
    a = M2(-2.4, z)
    dr.line([a, M2(19.5, z)], fill=(180, 60, 60), width=1)
    txt((a[0] - 22, a[1]), lab, size=10, fill=(170, 50, 50), bg=(253, 252, 248))
txt((M2(8, -1.5)[0], M2(8, -1.5)[1]), "فضای باز ۲.۶۷ + حریم ۷.۰۸", size=10, fill=(40, 95, 45))
# مقطعِ کوتاهِ شرقی (مغازه و نیم‌طبقه)
my = ey + eh - 100
for z0, z1, lab, col in [(0, 2.70, "مغازه ۲.۵۰", (252, 236, 214)),
                         (2.70, POD_H, "نیم‌طبقه ۲.۵۰", (250, 232, 205))]:
    a, b2 = M2(14.0, z1), M2(18.5, z0)
    a = (a[0], a[1] + (int((TOP + 1 - POD_H) / 0.6) * 0 + 0))
    dr.rectangle([M2(14.0, z1)[0], M2(14.0, z1)[1], M2(18.5, z0)[0], M2(18.5, z0)[1]], fill=col,
                 outline=(170, 120, 50), width=1)
    txt(((M2(14.0, z1)[0] + M2(18.5, z0)[0]) / 2, (M2(14.0, z1)[1] + M2(18.5, z0)[1]) / 2), lab, size=10,
        fill=(120, 80, 20))
txt((M2(16.2, POD_H + 1.6)[0], M2(16.2, POD_H + 1.6)[1]), "مقطعِ مغازه (شرق)", size=10, fill=(120, 80, 20))

# ================================================================ F: حجم سه‌بعدی
fx_, fy_, fw_, fh_ = 20, 1040, 1880, 700
fy2 = panel(fx_, fy_, fw_, fh_, "و — حجمِ سه‌بعدی", "پودیومِ ۵.۴۰ + ۵ طبقهٔ مسکونی + ایوانِ سراسری")
C_ST, C_GRN, C_SITE = (206, 206, 206), (198, 228, 198), (226, 224, 214)
C_POD, C_POD_S, C_POD_T = (243, 206, 150), (232, 189, 128), (252, 236, 214)
C_PK, C_PK_S, C_PK_T = (206, 218, 234), (188, 203, 224), (232, 238, 246)
C_R, C_R_S, C_R_T = (226, 234, 244), (208, 218, 232), (248, 250, 252)
C_TER, C_SH = (196, 230, 196), (150, 190, 150)
C30, S30 = math.cos(math.radians(30)), math.sin(math.radians(30))
S = 12.0
iso = lambda x, y, z: (fx_ + 120 + (x + y) * C30 * S, fy2 + 300 + (x - y) * S30 * S - z * S)


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
blks.append((1, -Y0, 0, Y0, 0, SHOP_X0, D, POD_H, C_PK_T, C_PK, C_PK_S, (105, 105, 108)))
blks.append((1, SHOP_X0 - Y0, SHOP_X0, Y0, 0, W, D, POD_H, C_POD_T, C_POD, C_POD_S, (105, 105, 108)))
blks.append((2, BLD_W - Y0, BLD_W, Y0, POD_H, W, D, POD_H + 0.25, C_TER, shade(C_TER, .92),
             shade(C_TER, .86), (105, 105, 108)))
fl = [POD_H + k * FL_H for k in range(1, NFL)]
blks.append((2, -YS, 0, YS, POD_H, UW, Y1, TOP, C_R_T, C_R, C_R_S, (105, 105, 108)))
blks.append((2, UW - YS, UW, YS, POD_H, UW + SH_W, Y1 - SH_D, TOP, C_R_T, C_R, C_R_S, (105, 105, 108)))
blks.append((2, UW + SH_W - YS, UW + SH_W, YS, POD_H, UW + CORE_W, Y1, TOP, C_R_T, C_R, C_R_S, (105, 105, 108)))
blks.append((2, UW + CORE_W - YS, UW + CORE_W, YS, POD_H, BLD_W, Y1, TOP, C_R_T, C_R, C_R_S, (105, 105, 108)))
blks.append((2, UW - (Y1 - SH_D), UW, Y1 - SH_D, POD_H, UW + SH_W, Y1, POD_H + 0.3, C_SH,
             shade(C_SH, .9), shade(C_SH, .82), (60, 120, 60)))
for f in range(NFL):
    z = POD_H + f * FL_H
    blks.append((3, liv['x'] - Y0 + z, liv['x'], Y0, z, liv['x'] + liv['w'], YS, z + 1.05,
                 (250, 240, 214), (236, 214, 160), (226, 200, 140), (105, 105, 108)))
    xb = UW + CORE_W + UW - liv['x'] - liv['w']
    blks.append((3, xb - Y0 + z, xb, Y0, z, xb + liv['w'], YS, z + 1.05,
                 (250, 240, 214), (236, 214, 160), (226, 200, 140), (105, 105, 108)))
for (g, k, x0, y0, z0, x1, y1, z1, t, e, s, edge) in sorted(blks, key=lambda b: (b[0], b[1])):
    box3(x0, y0, z0, x1, y1, z1, t, e, s, edge=edge,
         floors=fl if (g == 2 and z1 > TOP - 0.1) else None,
         stripes=2.5 if (g == 1 and x0 == 0) else None)
txt((fx_ + 16, fy_ + 20), "نیم‌طبقهٔ مغازه‌ها و سطحِ انباری داخلِ پودیوم (معاف یا با ۲۰٪ تراکم)",
    size=13, fill=(70, 80, 95), anchor="lm")

# ================================================================ G: جداول
gx, gy, gw, gh = 20, 1760, 1880, 720
gy2 = panel(gx, gy, gw, gh, "ز — جداول، کنترلِ ضوابط و هشدارها")
col = [gx + 30, gx + 480, gx + 950, gx + 1430]

txt((col[0], gy2 + 26), "۱) ترازِ مساحت‌ها (فرمِ شهرداری)", size=18, bold=True, fill=(24, 42, 64), anchor="lm")
rows = [("همکف — ۳ مغازه (۳ × ۴۵.۵)", "۱۳۶.۵"),
        ("همکف — انبار/سرویسِ تجاری", "۳۹.۰"),
        ("همکف — لابی و هسته", "۱۵.۳"),
        ("نیم‌طبقه (۷۵ m² واقعی، ۲۰٪ محاسبه‌ای)", "۱۵.۰"),
        (f"طبقات ۱ تا {NFL} — هر طبقه ۲ واحد", f"{V['res']:.0f}"),
        ("جمعِ زیربنای مشمولِ تراکم", f"{V['tot']:.0f}"),
        ("تراکمِ محاسبه‌ای", f"{V['far']}٪")]
yy = gy2 + 56
for i, (a, b3) in enumerate(rows):
    last = i >= len(rows) - 2
    txt((col[0] + 8, yy), a, size=14, fill=(45, 45, 45), anchor="lm", bold=last, max_w=330)
    txt((col[0] + 350, yy), b3, size=14, fill=(45, 45, 45), anchor="lm", bold=last)
    yy += 25
txt((col[0] + 8, yy + 6), "مازادِ قابلِ خرید:", size=15, bold=True, fill=(20, 90, 45), anchor="lm")
txt((col[0] + 350, yy + 6), f"{V['mazad_180']} m² (بر ۱۸۰٪) · {V['mazad_120']} m² (بر پایهٔ ۱۲۰٪)",
    size=14, fill=(20, 90, 45), anchor="lm", max_w=330)

txt((col[1], gy2 + 26), "۲) سودِ سه‌گانهٔ این نسخه", size=18, bold=True, fill=(24, 42, 64), anchor="lm")
gain = [("طبقهٔ پنجم (۲ واحدِ دیگر)", f"+{2*L['unit']['sale']:.0f} m² فروشی", "+۱۴ میلیارد*"),
        ("نیم‌طبقهٔ ۳ مغازه", "+۷۵ m² تجاری", "+۷.۵ میلیارد*"),
        ("انباریِ ۸ واحد", "+۴۰ m² فروشی", "+۱ میلیارد*"),
        ("ایوان (۵۰٪ در تراکم)", f"+{L['unit']['balcony']} m² در واحد", "رایگان"),
        ("شفتِ ۳×۳ به‌جای نورگیر", "تهویهٔ هسته", "بدون هزینه")]
yy = gy2 + 56
for a, b3, c in gain:
    txt((col[1] + 8, yy), a, size=14, fill=(55, 62, 75), anchor="lm", max_w=200)
    txt((col[1] + 215, yy), b3, size=13, fill=(20, 90, 45), anchor="lm", bold=True, max_w=180)
    txt((col[1] + 400, yy), c, size=12, fill=(120, 80, 20), anchor="lm", max_w=110)
    yy += 27
txt((col[1] + 8, yy + 4), "* برآورد با نرخِ ۷۵ میلیون تومان هر متر مسکونی و ۱۰۰ میلیون تجاری",
    size=11, fill=(110, 110, 110), anchor="lm", max_w=430)

txt((col[2], gy2 + 26), "۳) کنترلِ تطبیق", size=18, bold=True, fill=(24, 42, 64), anchor="lm")
checks = [("سطح اشغال", f"{BLD_W*POD_D:.0f} m² از {W*D*0.8:.0f} مجاز", True),
          ("عرضِ نشیمن / خواب", "۶.۸۱ / ۵.۲۵ m ≥ ۳.۰۰ / ۲.۵۰", True),
          ("عمقِ نورگیری", "۴.۱۵ m ≤ ۷.۰۰", True),
          ("بالکنِ هر واحد", f"{L['unit']['balcony']} m² ≥ ۳ m²", True),
          ("نیم‌طبقه", "۵۵٪ مجاز — این طرح ۵۵٪", True),
          ("ارتفاعِ انباری/پارکینگ", "۲.۲۰ / ۲.۴۰ ⇒ معاف از تراکم", True),
          ("ارتفاعِ کل", f"{TOP:.1f} m — وابسته به حدِّ پهنه", None),
          ("پارکینگ", "۶ موجود / ۱۲ تا ۱۴ نیاز", False)]
yy = gy2 + 56
for a, b3, ok in checks:
    mk = "✓ " if ok else ("؟ " if ok is None else "! ")
    cl = (20, 90, 45) if ok else ((200, 130, 20) if ok is None else (160, 45, 40))
    txt((col[2] + 8, yy), mk + a, size=14, fill=cl, anchor="lm")
    txt((col[2] + 190, yy), b3, size=12, fill=(75, 75, 75), anchor="lm", max_w=240)
    yy += 27

txt((col[3], gy2 + 26), "۴) تصمیم‌های پیشِ رو", size=18, bold=True, fill=(24, 42, 64), anchor="lm")
warn = [("خرید در برابر جریمه", "خرید: پایان‌کارِ تمیز | جریمه: ۰.۵ تا ۳× ارزشِ معاملاتی"),
        ("تراکمِ پایه", "اگر ۱۲۰٪ باشد، ۵۰۷ m² باید خریداری شود"),
        ("ارتفاع", "۲۰.۹ m — حدِّ پهنه و حریمِ برق را بپرسید"),
        ("پارکینگ", "کسریِ ۶ تا ۸ فضا ⇒ زیرزمین یا جریمهٔ تبصرهٔ ۵"),
        ("اسکلت", "از ابتدا برای ۵ طبقه ببندید"),
        ("نیم‌طبقه", "ارتفاعِ همکف را به ۵.۴۰ رسانده است"),
        ("تأییدِ شهرسازی", "مازاد منوط به تأییدِ معاونتِ شهرسازی است")]
yy = gy2 + 56
for a, b3 in warn:
    txt((col[3] + 8, yy), a, size=14, fill=(150, 60, 30), anchor="lm", max_w=190)
    txt((col[3] + 205, yy), b3, size=12, fill=(60, 60, 70), anchor="lm", max_w=230)
    yy += 30

fn = gy + gh - 140
dr.rectangle([gx + 16, fn - 16, gx + gw - 16, fn + 110], fill=(238, 242, 247), outline=(160, 175, 195), width=1)
txt((gx + 36, fn + 6), "جمع‌بندی: نسبت به نسخهٔ قبل، دو طبقهٔ کامل (+۱۹۱ m² فروشی)، ۷۵ m² نیم‌طبقهٔ تجاری و ۴۰ m² انباری اضافه شده،",
    size=15, fill=(40, 50, 65), anchor="lm", max_w=gw - 80)
txt((gx + 36, fn + 32), "در حالی که فقط ۱۸۲ m² تراکمِ مازاد لازم دارد — چون نیم‌طبقه تنها ۲۰٪ و انباری و پارکینگ صفر در تراکم حساب می‌شوند.",
    size=15, fill=(40, 50, 65), anchor="lm", max_w=gw - 80)
txt((gx + 36, fn + 58), "این مازاد را می‌توانید از شهرداری اصفهان بخرید (اصفهان تراکم می‌فروشد؛ ضریبِ طبقهٔ پنجم ۱.۲) و پایان‌کارِ تمیز بگیرید.",
    size=15, fill=(20, 90, 45), anchor="lm", max_w=gw - 80)
txt((gx + 36, fn + 84), "پیش از هر اقدام: تراکمِ پایهٔ پهنه، حدِّ ارتفاع، و بهای هر متر تراکمِ مازاد را از شهرداری استعلام کنید.",
    size=15, fill=(160, 45, 40), anchor="lm", max_w=gw - 80)

img.save(OUT)
print("saved:", OUT, img.size)
