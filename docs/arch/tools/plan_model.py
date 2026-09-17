#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""مدلِ هندسیِ یکپارچهٔ ساختمان — منبعِ واحد برای پلان‌ها، DXF و رندرِ سه‌بعدی.

همهٔ اندازه‌ها به متر. مبدأ: گوشهٔ جنوب‌غربیِ زمینِ خالص (۴۰٫۵۷ × ۱۳٫۳۷).
محورِ Y به سمتِ شمال (گذرِ ۸ متری) افزایش می‌یابد.
"""
import json, os, math

HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# ---------------------------------------------------------------- زمین و کلیات
LAND_W, LAND_D, NET_AREA = 40.57, 13.37, 542.38
Y0, Y1 = 2.67, 13.37          # محدودهٔ ساخت (فضای بازِ جنوبی ۲٫۶۷)
PODIUM_D = 10.70
SETBACK_N, SETBACK_E, SETBACK_S = 8.00, 7.08, 7.08

# ---------------------------------------------------------------- ساختمان
UW, UD = 9.186, 8.30          # واحد: عرض × عمقِ بسته
CORE_W = 4.20                 # هسته (پلهٔ رفت‌وبرگشتی + آسانسور + شفت)
SH_W, SH_D = 4.20, 3.00       # شفتِ نور و تهویه (در انتهای شمالیِ هسته)
BALC_D = 2.40                 # عمقِ ایوان
BLD_W = 2 * UW + CORE_W       # ۲۲٫۵۷۲
BALC_Y0, BALC_Y1 = Y0, Y0 + BALC_D       # ایوان
ENC_Y0, ENC_Y1 = Y0 + BALC_D, Y1         # فضای بسته (۸٫۳۰)
NFL, FL_H, POD_H = 5, 2.90, 5.40
TOP = POD_H + NFL * FL_H                 # ۱۹٫۹۰
PARAPET = 1.00

# ---------------------------------------------------------------- ضخامتِ دیوارها
T_EXT, T_CORE, T_INT = 0.30, 0.25, 0.15

# ---------------------------------------------------------------- چیدمانِ واحد (خروجیِ حل‌گر)
ROOMS = [
    # نام، کلید، x0, y0, x1, y1 (مختصاتِ محلیِ واحد، y=۰ لبهٔ داخلیِ ایوان)
    ("نشیمن",       "living",  0.00, 0.00, 6.56, 3.83),
    ("آشپزخانه",    "kitchen", 6.56, 0.00, 9.186, 3.83),
    ("سرویس",       "wc",      0.00, 3.83, 1.39, 5.57),
    ("حمام",        "bath",    1.39, 3.83, 3.99, 5.57),
    ("هال / ورودی", "hall",    3.99, 3.83, 9.186, 5.57),
    ("خواب ۱",      "bed1",    0.00, 5.57, 5.14, 8.30),
    ("خواب ۲",      "bed2",    5.14, 5.57, 9.186, 8.30),
]
ROOM_COLOR = {"living": (250, 236, 208), "kitchen": (233, 242, 226), "bath": (232, 236, 244),
              "wc": (232, 236, 244), "hall": (248, 248, 240), "bed1": (228, 234, 248),
              "bed2": (228, 234, 248)}

# پنجره‌ها و درِ ورودیِ واحد (مختصاتِ محلی)
WINDOWS = [                      # (x0, y0, x1, y1, جهت)
    ("S", 0.90, 0.00, 3.60, 0.00),        # نشیمن رو به ایوان
    ("W", 0.00, 1.20, 0.00, 2.80),        # نشیمن، نماي غرب
    ("E", 9.186, 1.00, 9.186, 2.60),      # آشپزخانه
    ("W", 0.00, 4.30, 0.00, 5.10),        # سرویس
    ("N", 1.00, 8.30, 2.90, 8.30),        # خواب ۱
    ("N", 6.10, 8.30, 8.10, 8.30),        # خواب ۲
]
UNIT_DOOR = ("E", 4.30, 5.20)             # درِ ورودیِ واحد روی دیوارِ شرقی (هسته)

# ---------------------------------------------------------------- همکف
SHOP_X0 = 22.60
SHOP_DEEP = 7.50
NSHOP = 3
SHOP_W = (LAND_W - SHOP_X0) / NSHOP       # ≈ ۵٫۹۹
SVC_DEEP = PODIUM_D - SHOP_DEEP           # نوارِ انبار/سرویسِ مغازه‌ها
PARK_N = 6                                # فضای پارک در پیلوت
PARK_W, PARK_L = 2.50, 5.00
ANB_N, ANB_W, ANB_D = 8, 2.40, 2.20       # انباری‌ها در تراز ۲٫۶۰+
MEZ_DEEP = 4.50                           # عمقِ نیم‌طبقه

# ---------------------------------------------------------------- ترازها
LEVELS = [
    ("همکف / پیلوت",   "±0.00",  0.00),
    ("نیم‌طبقه و انباری", "+2.60",  2.60),
    ("طبقهٔ تیپ ۱ تا ۵", "+5.40",  5.40),
    ("بام",            "+19.90", TOP),
]


# ================================================================ ابزار
def unit_rooms(offset_x):
    """اتاق‌هایِ یک واحد با انتقال به مختصاتِ جهانی"""
    out = []
    for name, key, x0, y0, x1, y1 in ROOMS:
        out.append(dict(name=name, key=key,
                        x0=offset_x + x0, y0=ENC_Y0 + y0, x1=offset_x + x1, y1=ENC_Y0 + y1,
                        area=round((x1 - x0) * (y1 - y0), 2)))
    return out


def mirrored_rooms(offset_x):
    """همان واحد، قرینه (برای واحدِ شرقی)"""
    out = []
    for name, key, x0, y0, x1, y1 in ROOMS:
        mx0 = offset_x + UW - x1
        mx1 = offset_x + UW - x0
        out.append(dict(name=name, key=key, x0=mx0, y0=ENC_Y0 + y0, x1=mx1, y1=ENC_Y0 + y1,
                        area=round((x1 - x0) * (y1 - y0), 2)))
    return out


UNIT_A_X = 0.0
CORE_X0 = UW                              # ۹٫۱۸۶
CORE_X1 = UW + CORE_W                     # ۱۳٫۳۸۶
UNIT_B_X = CORE_X1                        # ۱۳٫۳۸۶


def core_zones():
    """اجزای هسته در مختصاتِ جهانی"""
    shaft_y0 = ENC_Y1 - SH_D
    stair = dict(x0=CORE_X0 + 0.10, y0=ENC_Y0 + 0.04,
                 x1=CORE_X0 + 2.60, y1=ENC_Y0 + 5.30, kind="stair")
    lift = dict(x0=CORE_X0 + 2.70, y0=ENC_Y0 + 0.10,
                x1=CORE_X0 + 4.10, y1=ENC_Y0 + 1.60, kind="lift")
    shaft = dict(x0=CORE_X0, y0=shaft_y0, x1=CORE_X1, y1=ENC_Y1, kind="shaft")
    lobby = dict(x0=CORE_X0 + 2.70, y0=ENC_Y0 + 1.60,
                 x1=CORE_X0 + 4.10, y1=shaft_y0, kind="lobby")
    return [stair, lift, shaft, lobby]


def stair_treads(box, risers=16, h=FL_H):
    """کف‌پله‌های پلهٔ رفت‌وبرگشتی (دو پاگرد میانی)"""
    n_per = risers // 2                       # ۸ پله در هر شاخه
    treads = []
    # شاخهٔ رفت (جنوب به شمال) در نیمهٔ غربی
    run = (box["y1"] - box["y0"] - 1.20) / 2   # طولِ هر شاخه
    w_flight = 1.20
    x0 = box["x0"]
    for i in range(n_per - 1):
        y = box["y0"] + i * run / (n_per - 1)
        treads.append((x0, y, x0 + w_flight, y + run / (n_per - 1)))
    # پاگرد
    treads.append((x0, box["y0"] + run, x0 + 2.50, box["y0"] + run + 1.20))
    # شاخهٔ برگشت در نیمهٔ شرقی
    x1 = box["x0"] + 1.30
    for i in range(n_per - 1):
        y = box["y0"] + run + 1.20 + i * run / (n_per - 1)
        treads.append((x1, y, x1 + w_flight, y + run / (n_per - 1)))
    return treads


# ================================================================ خروجیِ داده برای رندرر
def building_boxes():
    """جعبه‌هایِ سه‌بعدیِ ساختمان برای رندرر (x0,y0,z0,x1,y1,z1, مصالح)"""
    B = []
    # پودیوم — پارکینگ (غرب) و مغازه‌ها (شرق)
    B.append((0.0, Y0, 0.0, SHOP_X0, Y1, POD_H, "concrete"))
    B.append((SHOP_X0, Y0, 0.0, LAND_W, Y1, POD_H, "shopfront"))
    # سقفِ پودیوم / تراس
    B.append((BLD_W, Y0, POD_H - 0.30, LAND_W, Y1, POD_H, "terrace"))
    # حجمِ مسکونی در ۵ طبقه، بدونِ شفت
    z = POD_H
    for f in range(NFL):
        z0 = POD_H + f * FL_H
        z1 = z0 + FL_H
        # بالِ غربی و شرقی
        B.append((0.0, ENC_Y0, z0, UW, ENC_Y1, z1, "facade"))
        B.append((UNIT_B_X, ENC_Y0, z0, BLD_W, ENC_Y1, z1, "facade"))
        # هسته (دو سویِ شفت)
        B.append((CORE_X0, ENC_Y0, z0, CORE_X1, ENC_Y1 - SH_D, z1, "core"))
        # ایوان‌ها
        liv = [r for r in ROOMS if r[1] == "living"][0]
        B.append((0.0 + liv[2], BALC_Y0, z0, 0.0 + liv[4], ENC_Y0, z1 - 0.85, "balcony"))
        bx0 = BLD_W - liv[4]
        bx1 = BLD_W - liv[2]
        B.append((bx0, BALC_Y0, z0, bx1, ENC_Y0, z1 - 0.85, "balcony"))
        # نردهٔ ایوان
        B.append((0.0 + liv[2], BALC_Y0, z1 - 0.85, 0.0 + liv[4], BALC_Y0 + 0.12, z1, "railing"))
        B.append((bx0, BALC_Y0, z1 - 0.85, bx1, BALC_Y0 + 0.12, z1, "railing"))
    # جان‌پناهِ بام
    B.append((0.0, ENC_Y1 - 0.25, TOP, BLD_W, ENC_Y1, TOP + PARAPET, "parapet"))
    B.append((0.0, ENC_Y0, TOP - 0.30, BLD_W, ENC_Y1, TOP, "roof"))
    return B


def shaft_boxes():
    return [(CORE_X0, ENC_Y1 - SH_D, POD_H, CORE_X1, ENC_Y1, TOP + 0.30)]


def summary():
    enc = UW * UD
    liv = [r for r in ROOMS if r[1] == "living"][0]
    balc = (liv[4] - liv[2]) * BALC_D
    core_net = CORE_W * UD - SH_W * SH_D
    per_floor = 2 * enc + core_net + 2 * 0.5 * balc
    gnd = NSHOP * SHOP_W * SHOP_DEEP + (LAND_W - SHOP_X0) * SVC_DEEP + 19.0
    mez_cnt = NSHOP * min(SHOP_W * MEZ_DEEP * 0.20, 20.0)
    tot = NFL * per_floor + gnd + mez_cnt
    return dict(unit_encl=round(enc, 1), balcony=round(balc, 1), unit_sale=round(enc + balc, 1),
                core_net=round(core_net, 1), per_floor=round(per_floor, 1),
                nfl=NFL, units=NFL * 2, sale_res=round(NFL * 2 * (enc + balc), 1),
                ground=round(gnd, 1), mezz_counted=round(mez_cnt, 1),
                total=round(tot, 1), far_pct=round(tot / NET_AREA * 100, 1),
                mazad_180=round(tot - 976, 1), mazad_120=round(tot - 650.9, 1),
                height=round(TOP + PARAPET, 2), bld_w=round(BLD_W, 2),
                mez_phys=round(NSHOP * SHOP_W * MEZ_DEEP, 1),
                shop_area=round(SHOP_W * SHOP_DEEP, 1), anb=ANB_N * 5)


if __name__ == "__main__":
    s = summary()
    print(json.dumps(s, ensure_ascii=False, indent=1))
