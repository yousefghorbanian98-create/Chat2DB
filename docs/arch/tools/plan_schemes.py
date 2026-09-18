#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""هندسهٔ هر دو طرح پس از سقفِ سه طبقهٔ منطقه — منبعِ واحدِ حقیقت

زمین (پس از عقب‌نشینی)     ۴۰٫۵۷ × ۱۳٫۳۷ = ۵۴۲٫۳۸ m²
سطحِ اشغالِ مجاز (۸۰٪)      ۴۳۳٫۹ m²
سقفِ طبقات                 پیلوت + ۳ طبقه
"""
import math

LAND_W, LAND_D = 40.57, 13.37
LAND = LAND_W * LAND_D
COV = 0.80 * LAND                 # ۴۳۳٫۹
DEEP = 10.70                      # عمقِ بنا
BLD_W = COV / DEEP                # ۴۰٫۵۵ m — عرضِ کاملِ زمین
Y0 = LAND_D - DEEP                # ۲٫۶۷ — فضایِ بازِ جنوبی
Y1 = LAND_D                       # ۱۳٫۳۷

CORR = 1.30                       # راهرویِ شمالی
BALC = 2.20                       # عمقِ ایوانِ جنوبی
CORE_W, CORE_D = 4.20, 5.10       # هسته: پلهٔ رفت‌وبرگشتی + آسانسور
FL_H = 2.90                       # ارتفاعِ طبقه
PIL_H = 2.60                      # ارتفاعِ پیلوت
SHOP_H = 4.50                     # ارتفاعِ مغازه
PARAPET = 1.00
ENC_D = DEEP - CORR - BALC        # عمقِ بستهٔ واحد = ۷٫۲۰

UPF = 4                           # واحد در هر طبقه
NF_RES = 3                        # طبقاتِ مسکونی


def unit_boxes(offy=Y0):
    """جعبهٔ واحدهایِ یک طبقه — هسته در انتهایِ غربی، راهرو در شمال"""
    w = (BLD_W - CORE_W) / UPF
    out = []
    for i in range(UPF):
        x0 = CORE_W + i * w
        out.append(dict(i=i, x0=x0, x1=x0 + w, w=w,
                        y0=offy + BALC, y1=offy + BALC + ENC_D,
                        by0=offy, by1=offy + BALC,
                        area=w * ENC_D, barea=w * BALC))
    return out


def cores(offy=Y0):
    """یک هسته در انتهایِ غربی — برایِ ۱۲ واحد کافی است"""
    return [dict(x0=0.0, x1=CORE_W, y0=offy + DEEP - CORE_D, y1=offy + DEEP)]


def corridor(offy=Y0):
    """راهرویِ شمالی در سراسرِ طول، از کنارِ هسته تا انتهایِ شرقی"""
    return dict(x0=CORE_W, x1=BLD_W, y0=offy + DEEP - CORR, y1=offy + DEEP)


def parking_rows(inset=0.60, depth=5.00, width=2.50):
    """چیدمانِ پارکینگ در پیلوت — ردیف‌هایِ عمودی"""
    rows, y = [], Y0 + inset
    while y + depth <= Y1 - inset:
        x = inset
        n = 0
        while x + width <= BLD_W - inset - 3.5:      # ۳٫۵ m برایِ رمپ/مانور
            rows.append(dict(n=n + 1, x0=x, x1=x + width, y0=y, y1=y + depth))
            x += width + 0.15
            n += 1
        y += depth + 5.5                              # راهرویِ مانور
    return rows


def shops(n=4, depth=6.00):
    """مغازه‌هایِ همکف در نوارِ شمالی"""
    w = (BLD_W - CORE_W) / n
    return [dict(i=i, x0=CORE_W + i * w, x1=CORE_W + (i + 1) * w,
                 y0=Y1 - depth, y1=Y1, area=w * depth, w=w) for i in range(n)]


def levels(kind):
    """kind: 'pilotis' | 'shops' — تراز و ارتفاعِ هر سطح"""
    if kind == 'pilotis':
        base = [(f"پیلوت (پارکینگ)", 0.0, PIL_H)]
        z = PIL_H
    else:
        base = [(f"همکف (مغازه)", 0.0, SHOP_H)]
        z = SHOP_H
    for i in range(NF_RES):
        base.append((f"طبقهٔ {i + 1}", z, z + FL_H))
        z += FL_H
    base.append(("بام", z, z + PARAPET))
    return base


def summary(kind, upf=UPF, nshop=0):
    """محاسبهٔ زیربنا و تراکم با احتسابِ هسته و راهرو (تصحیحِ اشتباهِ پیشین)"""
    u = unit_boxes()
    cs = cores()
    cr = corridor()
    enc = sum(x['area'] for x in u)
    balc = sum(x['barea'] for x in u)
    core_a = sum((c['x1'] - c['x0']) * (c['y1'] - c['y0']) for c in cs)
    corr_a = (cr['x1'] - cr['x0']) * (cr['y1'] - cr['y0'])
    foot = BLD_W * DEEP
    walls = max(0.0, foot - enc - balc - core_a - corr_a)
    # زیربنای مشمول: همه به‌جز نیمی از ایوان
    cnt = enc + 0.5 * balc + core_a + corr_a + walls
    com = sum(s['area'] for s in shops(nshop)) if nshop else 0.0
    nf = NF_RES
    gfa = nf * cnt + com
    if kind == 'pilotis':
        h = PIL_H + nf * FL_H + PARAPET
    else:
        h = SHOP_H + nf * FL_H + PARAPET
    return dict(foot=foot, enc=enc, balc=balc, core=core_a, corr=corr_a, walls=walls,
                cnt_per_floor=cnt, gfa=gfa, far=gfa / LAND * 100,
                exc180=max(0.0, gfa - 1.80 * LAND),
                exc120=max(0.0, gfa - 1.20 * LAND),
                units=upf * nf, unit_area=enc / upf, height=h,
                park_have=len(parking_rows()), com=com)


if __name__ == "__main__":
    for k in ('pilotis', 'shops'):
        s = summary(k, nshop=(4 if k == 'shops' else 0))
        print(f"── {k} ──")
        for key in ('foot', 'enc', 'balc', 'core', 'corr', 'walls', 'cnt_per_floor',
                    'gfa', 'far', 'exc180', 'exc120', 'units', 'unit_area', 'height',
                    'park_have', 'com'):
            print(f"   {key:15s} {s[key]:8.2f}")
        print()
