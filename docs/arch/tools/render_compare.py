#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""صفحهٔ مقایسه: طرحوارهٔ ۵ (موجود) در برابر ۵+ (بهبودیافته) و ۷ (رقیب)
پلانِ طبقهٔ تیپ را از حل‌گرِ محدودیت (floorplan_csp.py → layouts.json) می‌گیرد.
خروجی: docs/arch/compare-5-vs-7.png
"""
import math, os, json
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display

HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT = os.path.join(HERE, "docs", "arch", "compare-5-vs-7.png")
LAY = json.load(open(os.path.join(HERE, "docs", "arch", "layouts.json"), encoding="utf-8"))
FDIR = "/home/user/fonts"

W, D, OCC, FSR = 40.57, 13.37, 0.80, 1.80
BLD_D = W * D * OCC / W                 # ۱۰.۷۰ = عمق کلِ مجاز
SHAL, BALC_D, CORE_W, WELL_W = 8.30, 2.40, 3.00, 2.20
Y0, Y1 = D - BLD_D, D                   # ۲.۶۷ .. ۱۳.۳۷
GND_H, FL_H, NFL = 4.20, 3.00, 4
TOP = GND_H + NFL * FL_H
GFA_FLOOR = W * D * FSR / NFL           # ۱۹۰.۵ m² تراکمِ هر طبقه
SHOP_X0 = W - 19.5

P = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")
_c = {}


def fa(t):
    return get_display(arabic_reshaper.reshape(str(t).translate(P)))


def F(sz, bold=False):
    if (sz, bold) not in _c:
        _c[(sz, bold)] = ImageFont.truetype(
            os.path.join(FDIR, "Vazirmatn-Bold.ttf" if bold else "Vazirmatn-Regular.ttf"), sz)
    return _c[(sz, bold)]


CW, CH = 1910, 1560
COLW, COLP = 620, 630          # سه ستون در عرضِ بوم
img = Image.new("RGB", (CW, CH), (243, 241, 234))
dr = ImageDraw.Draw(img)


def txt(xy, t, size=18, fill=(30, 30, 30), bold=False, anchor="mm", bg=None, pad=(6, 4), max_w=None):
    x, y = xy
    f = F(size, bold)
    t = fa(t)
    if max_w:
        while dr.textbbox((0, 0), t, font=f)[2] > max_w and size > 9:
            size -= 1
            f = F(size, bold)
    b = dr.textbbox((x, y), t, font=f, anchor=anchor)
    if bg:
        dr.rectangle([b[0] - pad[0], b[1] - pad[1], b[2] + pad[0], b[3] + pad[1]], fill=bg)
    dr.text((x, y), t, font=f, fill=fill, anchor=anchor)


# ============================================================ گزینه‌ها
L5 = LAY["۵  (موجود)"]["rooms"]
LS = LAY["۵+ (بهبودیافته)"]["rooms"]
L7 = LAY["۷  (رقیب)"]["rooms"]
U5W = LAY["۵  (موجود)"]["box"]["w"]            # ۷.۴۰
USW = LAY["۵+ (بهبودیافته)"]["box"]["w"]       # ۹.۰۴


def liv_span(rooms):
    r = [x for x in rooms if x["k"] == "living"][0]
    return r["x"], r["x"] + r["w"]


OPTS = [
    dict(name="۵ — وضعِ موجود", sub="دو بلوک + نورگیر ۲ متر، بدون ایوان (عمق ۱۰.۷۰)",
         uw=U5W, well=2.00, deep=BLD_D, balc=0.0, rooms=L5),
    dict(name="۵+ — بهبودیافته", sub="دو بلوک + نورگیر ۲.۲ متر + ایوان ۲.۴ متری",
         uw=USW, well=WELL_W, deep=SHAL, balc=BALC_D, rooms=LS),
    dict(name="۷ — رقیب", sub="تک‌بلوکِ کم‌عمق + ایوان ۲.۴ متری (بدون نورگیر)",
         uw=USW, well=0.0, deep=SHAL, balc=BALC_D, rooms=L7),
]
for o in OPTS:
    o["wdt"] = 2 * o["uw"] + CORE_W + o["well"]       # نورگیر (فضای خالی) هم در ردپا هست
for o in OPTS:
    o["balc_area"] = sum((r["x"] + r["w"] - r["x"]) for r in o["rooms"] if r["k"] == "living") * o["balc"]
    o["encl"] = o["uw"] * o["deep"]
    o["sale_unit"] = o["encl"] + o["balc_area"]
    o["terrace"] = (W - o["wdt"]) * BLD_D
    o["facade"] = 2 * (o["wdt"] + o["deep"]) + (2 * o["deep"] + o["well"] if o["well"] else 0)

# ============================================================ سربرگ
dr.rectangle([0, 0, CW, 100], fill=(26, 40, 58))
txt((CW // 2, 34), "طرحوارهٔ ۵ در برابر دو رقیب — پلانِ طبقهٔ تیپ با حل‌گرِ محدودیت + حجم سه‌بعدی",
    size=32, bold=True, fill=(255, 255, 255))
txt((CW // 2, 74), "سطح اشغال ۸۰٪ · عمقِ کلِ مجاز ۱۰.۷۰ m · بودجهٔ تراکم هر طبقه ۱۹۰.۵ m² · "
                   "هسته ۳ m · محدودیت‌ها از مبحثِ چهارم مقررات ملی",
    size=17, fill=(196, 212, 234))

# ============================================================ ردیف ۱: پلان
PL_Y, PL_H = 112, 350
for i, o in enumerate(OPTS):
    px = 16 + i * COLP
    pw = COLW
    dr.rectangle([px, PL_Y, px + pw, PL_Y + PL_H], fill=(253, 252, 248), outline=(150, 150, 145), width=2)
    dr.rectangle([px, PL_Y, px + pw, PL_Y + 46], fill=(232, 236, 242), outline=(150, 150, 145), width=2)
    txt((px + 16, PL_Y + 23), o["name"], size=20, bold=True, fill=(24, 42, 64), anchor="lm")
    txt((px + pw - 16, PL_Y + 23), o["sub"], size=14, fill=(95, 105, 122), anchor="rm", max_w=520)

    sc = (pw - 110) / max(o["wdt"] + 2 * o["balc"] + 3, 24)
    ox = px + 55 + (pw - 110 - o["wdt"] * sc) / 2
    oy = PL_Y + PL_H - 78                  # لبهٔ جنوبیِ محدودهٔ ساخته‌شده

    def P2(xm, ym):
        # ym از لبهٔ جنوبیِ حجمِ بسته اندازه گرفته می‌شود (ایوان در ym<0)
        return (ox + xm * sc, oy - ym * sc)

    # ردپای پودیوم و تراس
    dr.rectangle([P2(0, BLD_D)[0], P2(0, BLD_D)[1], P2(W, 0)[0], P2(W, 0)[1]], fill=(255, 255, 255),
                 outline=(205, 205, 205), width=1)
    dr.rectangle([P2(o["wdt"], BLD_D)[0], P2(o["wdt"], BLD_D)[1], P2(W, 0)[0], P2(W, 0)[1]],
                 fill=(222, 240, 222))
    txt(((P2(o["wdt"], BLD_D)[0] + P2(W, 0)[0]) / 2, (P2(o["wdt"], BLD_D)[1] + P2(W, 0)[1]) / 2),
        f"تراس پودیوم {o['terrace']:.0f} m²", size=12, fill=(35, 95, 45))

    # ایوان‌ها
    if o["balc"]:
        for k, x0u in enumerate((0, o["uw"] + CORE_W + (o["well"] or 0))):
            bx0, bx1 = liv_span(o["rooms"])
            if k == 1:                       # واحدِ دوم قرینه است
                bx0, bx1 = o["uw"] - bx1, o["uw"] - bx0
            a = P2(x0u + bx0, 0); b = P2(x0u + bx1, -o["balc"])
            dr.rectangle([a[0], a[1], b[0], b[1]], fill=(250, 240, 214), outline=(190, 150, 60), width=1)
            txt(((a[0] + b[0]) / 2, (a[1] + b[1]) / 2), "ایوان", size=11, fill=(120, 85, 20))
    # نورگیر
    if o["well"]:
        wx0 = o["uw"] + CORE_W
        a = P2(wx0, o["deep"]); b = P2(wx0 + o["well"], 0)
        dr.rectangle([a[0], a[1], b[0], b[1]], fill=(186, 214, 186), outline=(70, 140, 80), width=1)
        txt(((a[0] + b[0]) / 2, (a[1] + b[1]) / 2), "نورگیر", size=11, fill=(30, 90, 40), bg=(255, 255, 255))

    COLOR = {'living': (250, 235, 205), 'kitchen': (232, 240, 226), 'bed1': (226, 232, 246),
             'bed2': (226, 232, 246), 'bath': (236, 236, 240), 'wc': (236, 236, 240),
             'hall': (246, 246, 240)}
    for k, x0u in enumerate((0, o["uw"] + CORE_W + (o["well"] or 0))):
        for r in o["rooms"]:
            rx0 = (x0u + r["x"]) if k == 0 else (x0u + o["uw"] - r["x"] - r["w"])
            a = P2(rx0, r["y"] + r["d"]); b = P2(rx0 + r["w"], r["y"])
            dr.rectangle([a[0], a[1], b[0], b[1]], fill=COLOR.get(r["k"], (245, 245, 245)),
                         outline=(120, 120, 120), width=1)
            cx, cy = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
            if r["w"] * sc > 52 and r["d"] * sc > 22:
                txt((cx, cy - 6), r["fa"], size=11, fill=(45, 45, 45))
                txt((cx, cy + 8), f"{r['a']:.1f}", size=10, fill=(95, 95, 95))
            elif r["w"] * sc > 26:
                txt((cx, cy), r["fa"][:4], size=9, fill=(60, 60, 60))
        # هسته
        cx0 = o["uw"] if k == 0 else o["uw"] + CORE_W + (o["well"] or 0) - CORE_W
        if k == 0:
            a = P2(o["uw"], o["deep"]); b = P2(o["uw"] + CORE_W, 0)
            dr.rectangle([a[0], a[1], b[0], b[1]], fill=(214, 214, 220), outline=(110, 110, 110), width=1)
            txt(((a[0] + b[0]) / 2, (a[1] + b[1]) / 2), "هسته", size=11, fill=(60, 60, 70))
    # ابعاد
    a = P2(0, -o["balc"] - 0.55); b = P2(o["wdt"], -o["balc"] - 0.55)
    dr.line([a, b], fill=(180, 60, 60), width=1)
    txt(((a[0] + b[0]) / 2, a[1] - 12), f"عرضِ کل {o['wdt']:.2f} m", size=12, fill=(170, 50, 50), bg=(253, 252, 248))
    a = P2(-0.9, 0); b = P2(-0.9, o["deep"])
    dr.line([a, b], fill=(180, 60, 60), width=1)
    txt((a[0] - 8, (a[1] + b[1]) / 2), f"{o['deep']:.2f}", size=12, fill=(170, 50, 50), bg=(253, 252, 248))
    if o["balc"]:
        a = P2(-0.9, -o["balc"]); b = P2(-0.9, 0)
        dr.line([a, b], fill=(180, 60, 60), width=1)
        txt((a[0] - 8, (a[1] + b[1]) / 2), f"{o['balc']:.1f}", size=11, fill=(170, 50, 50), bg=(253, 252, 248))
    txt((px + pw / 2, PL_Y + PL_H - 22), "شمال ↑", size=12, fill=(110, 110, 110))

# ============================================================ ردیف ۲: حجم سه‌بعدی
C_ST, C_GRN, C_SITE = (206, 206, 206), (198, 228, 198), (226, 224, 214)
C_POD = (243, 206, 150); C_POD_S = (232, 189, 128); C_POD_T = (252, 236, 214)
C_PK = (206, 218, 234); C_PK_S = (188, 203, 224); C_PK_T = (232, 238, 246)
C_R = (226, 234, 244); C_R_S = (208, 218, 232); C_R_T = (248, 250, 252)
C_TER = (196, 230, 196)
COS30, SIN30 = math.cos(math.radians(30)), math.sin(math.radians(30))
AX_Y, AX_H = 476, 572


def shade(c, f):
    return tuple(max(0, min(255, int(v * f))) for v in c)


def draw_box(iso, x0, y0, z0, x1, y1, z1, t, e, s, edge=(105, 105, 108), lw=1, floors=None, stripes=None):
    dr.polygon([iso(x0, y0, z0), iso(x1, y0, z0), iso(x1, y0, z1), iso(x0, y0, z1)], fill=s, outline=edge, width=lw)
    if stripes:                      # ستون‌های پیلوت روی نمای جنوبی
        x = x0 + stripes
        while x < x1:
            dr.line([iso(x, y0, z0 + 0.35), iso(x, y0, z1 - 0.35)], fill=shade(s, 0.86), width=2)
            x += stripes
    dr.polygon([iso(x1, y0, z0), iso(x1, y1, z0), iso(x1, y1, z1), iso(x1, y0, z1)], fill=e, outline=edge, width=lw)
    dr.polygon([iso(x0, y0, z1), iso(x1, y0, z1), iso(x1, y1, z1), iso(x0, y1, z1)], fill=t, outline=edge, width=lw)
    if floors:
        for z in floors:
            dr.line([iso(x0, y0, z), iso(x1, y0, z)], fill=edge, width=1)
            dr.line([iso(x1, y0, z), iso(x1, y1, z)], fill=edge, width=1)


for i, o in enumerate(OPTS):
    px = 16 + i * COLP
    pw = COLW
    dr.rectangle([px, AX_Y, px + pw, AX_Y + AX_H], fill=(253, 252, 248), outline=(150, 150, 145), width=2)
    S = 10.0
    iso = lambda x, y, z: (px + 55 + (x + y) * COS30 * S, AX_Y + 292 + (x - y) * SIN30 * S - z * S)
    ys, ye = Y0 + (BLD_D - o["deep"]), D          # لبهٔ جنوبیِ حجمِ بسته
    blocks = []
    # گروه ۰: صفحاتِ زمین و محیط — همیشه اول (هر حجمِ بالاتر از z=0 از صفحهٔ زمین جلوتر است)
    for (a, b, c, d, z, col) in [(0, D, W, D + 3.2, 0, C_ST), (0, -4.6, W, 0, 0, C_GRN),
                                 (0, 0, W, D, 0, C_SITE), (W, 0, W + 4.0, D, 0, C_ST)]:
        blocks.append(dict(grp=0, x0=a, y0=b, z0=-0.45, x1=c, y1=d, z1=z, t=col, e=shade(col, .9),
                           s=shade(col, .82), edge=(150, 150, 150), key=(a - b)))
    blocks.append(dict(grp=0, x0=0, y0=0, z0=0, x1=W, y1=Y0, z1=0.06, t=(206, 234, 206),
                       e=(200, 230, 200), s=(194, 226, 194), edge=(140, 180, 140), key=0))
    # گروه ۱: پودیوم (z=0)
    blocks.append(dict(grp=1, x0=0, y0=Y0, z0=0, x1=SHOP_X0, y1=D, z1=GND_H, t=C_PK_T, e=C_PK, s=C_PK_S,
                       key=(0 - Y0), stripes=2.5))
    blocks.append(dict(grp=1, x0=SHOP_X0, y0=Y0, z0=0, x1=W, y1=D, z1=GND_H, t=C_POD_T, e=C_POD, s=C_POD_S,
                       key=(SHOP_X0 - Y0)))
    # گروه ۲: حجم‌های روی پودیوم
    blocks.append(dict(grp=2, x0=o["wdt"], y0=Y0, z0=GND_H, x1=W, y1=D, z1=GND_H + 0.25, t=C_TER,
                       e=shade(C_TER, .92), s=shade(C_TER, .86), key=(o["wdt"] - Y0)))
    fl = [GND_H + k * FL_H for k in range(1, NFL)]
    if o["well"]:
        blocks.append(dict(grp=2, x0=0, y0=ys, z0=GND_H, x1=o["uw"] + CORE_W, y1=ye, z1=TOP, t=C_R_T,
                           e=C_R, s=C_R_S, floors=fl, key=(0 - ys)))
        blocks.append(dict(grp=2, x0=o["uw"] + CORE_W, y0=ys, z0=GND_H, x1=o["uw"] + CORE_W + o["well"],
                           y1=ye, z1=GND_H + 0.25, t=C_TER, e=shade(C_TER, .92), s=shade(C_TER, .86),
                           key=(o["uw"] + CORE_W - ys)))
        blocks.append(dict(grp=2, x0=o["uw"] + CORE_W + o["well"], y0=ys, z0=GND_H, x1=o["wdt"], y1=ye,
                           z1=TOP, t=C_R_T, e=C_R, s=C_R_S, floors=fl,
                           key=(o["uw"] + CORE_W + o["well"] - ys)))
    else:
        blocks.append(dict(grp=2, x0=0, y0=ys, z0=GND_H, x1=o["wdt"], y1=ye, z1=TOP, t=C_R_T, e=C_R,
                           s=C_R_S, floors=fl, key=(0 - ys)))
    if o["balc"]:
        bx0, bx1 = liv_span(o["rooms"])
        spans = [(bx0, bx1)]
        if o["well"]:
            spans.append((o["uw"] + CORE_W + o["well"] + o["uw"] - bx1,
                          o["uw"] + CORE_W + o["well"] + o["uw"] - bx0))
        else:
            spans.append((o["uw"] + CORE_W + o["uw"] - bx1, o["uw"] + CORE_W + o["uw"] - bx0))
        for k in range(NFL):
            z = GND_H + k * FL_H
            for (s0, s1) in spans:
                blocks.append(dict(grp=2, x0=s0, y0=Y0, z0=z, x1=s1, y1=ys, z1=z + 1.05, t=(250, 240, 214),
                                   e=(236, 214, 160), s=(226, 200, 140), key=(s0 - Y0 + z + 0.5)))
    for b in sorted(blocks, key=lambda b: (b["grp"], b["key"])):
        draw_box(iso, b["x0"], b["y0"], b["z0"], b["x1"], b["y1"], b["z1"], b["t"], b["e"], b["s"],
                 edge=b.get("edge", (105, 105, 108)), lw=1, floors=b.get("floors"), stripes=b.get("stripes"))
    txt((px + 16, AX_Y + 16), "حجمِ سه‌بعدی (۴ طبقه روی پودیوم)", size=15, fill=(70, 80, 95), anchor="lm")
    txt((px + pw - 16, AX_Y + 16), "پیلوت: ارتفاع مفید ۲.۴۰ m", size=12, fill=(130, 130, 130), anchor="rm")

# ============================================================ ردیف ۳: اعداد
NY = 1060
rows = [
    ("مساحتِ فروشیِ هر واحد (بسته + ایوان)", lambda o: f"{o['sale_unit']:.1f} m²",
     lambda o: f"{o['encl']:.1f} + {o['balc_area']:.1f}"),
    ("مجموعِ زیربنای فروشیِ مسکونی (۸ واحد)", lambda o: f"{8*o['sale_unit']:.0f} m²", None),
    ("عمقِ بسته / عمقِ کل", lambda o: f"{o['deep']:.2f} / {o['deep']+o['balc']:.2f} m", None),
    ("نمای خارجیِ هر طبقه (طولِ دیوار)", lambda o: f"{o['facade']:.0f} m", None),
    ("تراسِ پودیوم", lambda o: f"{o['terrace']:.0f} m²", None),
    ("نورگیر", lambda o: (f"{o['well']:.1f} × {o['deep']:.1f} m" if o["well"] else "ندارد"), None),
]
dr.rectangle([16, NY, CW - 16, NY + 40 + 34 * len(rows) + 34], fill=(250, 250, 246),
             outline=(150, 150, 145), width=2)
txt((34, NY + 24), "مقایسهٔ عددیِ سه گزینه", size=20, bold=True, fill=(24, 42, 64), anchor="lm")
for j, (label, fn, sub) in enumerate(rows):
    y = NY + 58 + j * 34
    dr.line([(26, y - 14), (CW - 26, y - 14)], fill=(225, 225, 220), width=1)
    txt((40, y), label, size=15, fill=(55, 62, 75), anchor="lm", max_w=440)
    for i, o in enumerate(OPTS):
        x = 520 + i * 460
        best = (j == 0 or j == 1)
        val = fn(o)
        txt((x, y), val, size=17, bold=True, fill=(20, 90, 45) if best and i > 0 else (70, 70, 70), anchor="lm")
        if sub:
            txt((x + 120, y), sub(o), size=13, fill=(120, 120, 120), anchor="lm")

FY = NY + 40 + 34 * len(rows) + 44
txt((34, FY + 16), "امتیازِ حل‌گرِ محدودیت (هرچه بالاتر بهتر): "
                   "گزینهٔ ۵ = ۳.۸ امتیاز | گزینهٔ ۵+ = ۴۵.۴ | گزینهٔ ۷ = ۴۵.۴",
    size=16, fill=(40, 50, 65), anchor="lm", max_w=CW - 60)
txt((34, FY + 44), "یافته‌های حقوقیِ به‌کاررفته: بالکنِ سه‌طرف‌باز با عمق ≤ ۳ m نیمی از مساحتش در تراکم حساب می‌شود؛ "
                   "در اصفهان هر واحد <۱۰۰ m² دست‌کم ۳ m² بالکن الزامی است؛",
    size=15, fill=(40, 50, 65), anchor="lm", max_w=CW - 60)
txt((34, FY + 70), "نورگیر برای فضاهای اصلی حداقل ۱۲ m² با عرض ۳ m و برای فضاهای فرعی ۶ m² با عرض ۲ m است؛ "
                   "فاصلهٔ پنجره‌های دو واحدِ روبه‌رو در نورگیر نباید کمتر از ۴ m باشد؛ عمقِ نورگیری حداکثر ۷ m.",
    size=15, fill=(40, 50, 65), anchor="lm", max_w=CW - 60)
txt((34, FY + 96), "⇒ نورگیرِ ۲ متریِ طرحوارهٔ ۵ نمی‌تواند نورِ اتاق‌های اصلی را تأمین کند (فقط خدمات/آشپزخانه) "
                   "و در عمقِ ۱۰.۷ m هم تهویهٔ مؤثر ندارد.",
    size=15, fill=(160, 45, 40), anchor="lm", max_w=CW - 60)

img.save(OUT)
print("saved:", OUT, img.size)
for o in OPTS:
    print(f"{o['name']:16s} واحد={o['sale_unit']:.1f} (بسته {o['encl']:.1f} + ایوان {o['balc_area']:.1f}) | "
          f"عرض={o['wdt']:.2f} | نما={o['facade']:.0f} | تراس={o['terrace']:.0f} | "
          f"فروشی کل={8*o['sale_unit']:.0f} m²")
