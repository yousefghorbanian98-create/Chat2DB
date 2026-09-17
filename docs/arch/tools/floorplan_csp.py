#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""حل‌گرِ محدودیت (CSP) برای چیدمانِ واحدِ مسکونی — الهام‌گرفته از دو منبعِ اوپن‌سورس:
  1) مولدِ مبتنی بر CSP در فهرستِ منابع (resource 5 در ai-tools-review.md)
  2) DStruct2Design (arXiv 2407.15723): محدودیت‌های عددی/متریک به‌جای تولیدِ تصویری
  3) ResPlan (arXiv 2508.14006): بازنماییِ گرافِ مجاورتِ اتاق‌ها برای ارزیابی
محدودیت‌ها از مبحثِ چهارم مقررات ملی ساختمان ایران گرفته شده‌اند.
"""
from itertools import permutations

# ---------------------------------------------------------------- برنامهٔ فیزیکی
# target: مترمربع هدف | min_a: حداقل مساحت | min_w: حداقل بعد (عرضِ مفید)
# max_ar: حداکثر نسبتِ طول به عرض | fac: نیاز به نما ('S','N','any',None)
PROGRAM = [
    dict(k='living',  fa='نشیمن',     target=25.0, min_a=20.0, min_w=3.00, max_ar=2.0, fac='S',
         adj={'entry': 2, 'kitchen': 2, 'balcony': 4},
         notadj={'wc': 3, 'bath': 2}),
    dict(k='kitchen', fa='آشپزخانه',  target=10.0, min_a=7.0,  min_w=2.50, max_ar=2.2, fac='any',
         adj={'living': 2, 'entry': 2}, notadj={'wc': 2, 'bath': 2}),
    dict(k='bed1',    fa='خواب ۱',    target=14.0, min_a=11.0, min_w=2.60, max_ar=1.9, fac='any',
         adj={'hall': 2, 'bath': 2}, notadj={'kitchen': 1, 'wc': 1}),
    dict(k='bed2',    fa='خواب ۲',    target=11.0, min_a=9.0,  min_w=2.50, max_ar=1.9, fac='any',
         adj={'hall': 2, 'bath': 1}, notadj={'kitchen': 1, 'wc': 1}),
    dict(k='bath',    fa='حمام',      target=4.5,  min_a=3.5,  min_w=1.60, max_ar=2.2, fac=None,
         adj={'hall': 3, 'bed1': 2}, notadj={'living': 3, 'kitchen': 3}),
    dict(k='wc',      fa='سرویس',     target=2.4,  min_a=1.8,  min_w=1.10, max_ar=2.5, fac=None,
         adj={'hall': 3}, notadj={'living': 3, 'kitchen': 3, 'bed1': 1, 'bed2': 1}),
    dict(k='hall',    fa='هال/ورودی', target=9.0,  min_a=6.0,  min_w=1.60, max_ar=3.2, fac=None,
         adj={'living': 2, 'kitchen': 1, 'bed1': 2, 'bed2': 2, 'bath': 3, 'wc': 3, 'core': 3},
         notadj={}),
]

SIDES = ('S', 'N', 'W', 'E')
from itertools import combinations
# محل‌های برش: تقسیمِ ۷ اتاق به ۲ یا ۳ نوارِ پیاپی
CUTS = [tuple(c) for c in combinations(range(1, 7), 1)] + \
       [tuple(sorted(c)) for c in combinations(range(1, 7), 2)]   # جهتِ کندنِ نوار از مستطیلِ باقیمانده


def touches(cell, box, eps=0.02):
    """نماهایی که سلول با آن‌ها تماس دارد"""
    _, x, y, w, d = cell
    bx, by, bw, bd = box
    out = set()
    if abs(y - by) < eps: out.add('S')
    if abs((y + d) - (by + bd)) < eps: out.add('N')
    if abs(x - bx) < eps: out.add('W')
    if abs((x + w) - (bx + bw)) < eps: out.add('E')
    return out


def shared(a, b, need=0.90):
    """طول دیوار مشترکِ دو اتاق (برای امکان در)"""
    _, ax, ay, aw, ad = a
    _, bx, by, bw, bd = b
    oy = min(ay + ad, by + bd) - max(ay, by)
    ox = min(ax + aw, bx + bw) - max(ax, bx)
    if abs(ox) < 1e-6 and oy > need: return oy
    if abs(oy) < 1e-6 and ox > need: return ox
    return 0.0


def box_of(wd):
    """ورودیِ (عرض، عمق) را به مستطیلِ (x,y,w,d) تبدیل می‌کند"""
    w, d = wd
    return (0.0, 0.0, float(w), float(d))


MULTS = (0.70, 0.85, 1.00, 1.20, 1.45)


def peel(rect, rm, side, mult=1.0, rest_t=0.0):
    """نوار را با «توزیعِ متناسب» می‌کَند: مساحتِ اتاق = سهمِ هدف × مساحتِ باقیمانده.
    rest_t = مجموعِ اهدافِ اتاق‌هایی که بعد از این یکی کنده می‌شوند.
    ⇒ اتاقِ آخر دیگر «ماندهٔ فضا» نمی‌شود و تخطیِ مساحت از بین می‌رود."""
    x, y, w, d = rect
    tgt_here = rm['target'] * mult
    A = (w * d) * tgt_here / (tgt_here + rest_t) if (tgt_here + rest_t) > 0 else w * d
    if side in ('S', 'N'):
        t = min(max(A / w, 0.9), d * 0.72)
        if side == 'S':
            return (rm, x, y, w, t), (x, y + t, w, d - t)
        return (rm, x, y + d - t, w, t), (x, y, w, d - t)
    t = min(max(A / d, 0.9), w * 0.72)
    if side == 'W':
        return (rm, x, y, t, d), (x + t, y, w - t, d)
    return (rm, x + w - t, y, t, d), (x, y, w - t, d)


def geo_penalty(cell, box, facades, total_t):
    """جریمه‌های هندسیِ یک اتاق (مستقل از بقیه) — مقیاس‌ناپذیر"""
    rm, x, y, w, d = cell
    a = w * d
    p = 0.0
    share = rm['target'] / total_t
    p += 26.0 * abs(a / (box[2] * box[3]) - share) / share          # انحراف از سهمِ هدف
    if min(w, d) < rm['min_w']:
        p += 70.0 * (rm['min_w'] - min(w, d) + 0.10)                # حداقل بعد (مبحث ۴)
    if a < rm['min_a']:
        p += 22.0 * (rm['min_a'] - a) / rm['min_a']                 # حداقل مساحت
    ar = max(w / d, d / w)
    if ar > rm['max_ar']:
        p += 26.0 * (ar - rm['max_ar'])                             # کشیدگیِ بیش‌ازحد
    t = touches(cell, box)
    need = rm['fac']
    if need == 'S':
        if 'S' in t and 'S' in facades: p -= 9.0                    # نشیمن رو به جنوب و ایوان
        elif not (t & facades): p += 42.0                           # فضای اصلی بی‌نور
    elif need == 'any':
        if not (t & facades): p += 26.0
    if rm['k'] in ('bath', 'wc') and (t & facades): p += 7.0        # نما را هدر ندهد
    if t & facades:                                                 # عمقِ نورگیری ≤ ۷ متر
        depth = d if (('S' in t and 'S' in facades) or ('N' in t and 'N' in facades)) else w
        if depth > 7.0: p += 16.0 * (depth - 7.0)
    return p


def full_score(cells, box, facades, core_side=None, balcony=True):
    """امتیازِ نهایی: هندسه + گرافِ مجاورت (به سبکِ ResPlan)"""
    total_t = sum(r['target'] for r in PROGRAM)
    s = -sum(geo_penalty(c, box, facades, total_t) for c in cells)
    byk = {c[0]['k']: c for c in cells}
    for c in cells:
        rm = c[0]
        for other, wt in rm['adj'].items():
            if other == 'balcony':
                if balcony and 'S' in touches(c, box) and 'S' in facades: s += 3.0 * wt
                elif balcony: s -= 2.0 * wt
                continue
            if other == 'core':
                if core_side and core_side in touches(c, box): s += 1.2 * wt
                elif core_side: s -= 6.0 * wt          # درِ واحد باید از هال به پاگرد باز شود
                continue
            oc = byk.get(other)
            if oc is None: continue
            s += 2.0 * wt if shared(c, oc) > 0 else -1.6 * wt
        for other, wt in rm['notadj'].items():
            oc = byk.get(other)
            if oc is not None and shared(c, oc) > 0: s -= 3.0 * wt
    return s


def band_layouts(box, facades, core_side, balcony, verbose=False):
    """تولیدِ تمام چیدمان‌های «نوار پهنی»: کلِ جعبه به ۲ یا ۳ نوارِ شمالی-جنوبی
    تقسیم می‌شود و هر نوار بین اتاق‌هایش به نسبتِ هدف تقسیم می‌گردد.
    این مدلِ واقعیِ آپارتمان‌سازی است و اتاق‌های متناسب (مربعی) می‌دهد."""
    x0, y0, W, D = box
    ks = [r['k'] for r in PROGRAM]
    best = []
    for order in permutations(PROGRAM):
        for cuts in CUTS:                      # محلِ برش بین نوارها
            bands, prev = [], 0
            for c in list(cuts) + [len(order)]:
                bands.append(list(order[prev:c])); prev = c
            if any(len(b) == 0 for b in bands): continue
            # عمقِ هر نوار ≡ سهمِ مساحتِ اتاق‌هایش
            areas = [sum(r['target'] for r in b) for b in bands]
            tot = sum(areas)
            cells, y = [], y0
            for bi, b in enumerate(bands):
                dep = D * areas[bi] / tot
                bw = sum(r['target'] for r in b)
                x = x0
                for ri, rm in enumerate(b):
                    w = W * rm['target'] / bw
                    cells.append((rm, x, y, w, dep)); x += w
                y += dep
            sc = full_score(cells, box, facades, core_side, balcony)
            best.append((sc, cells))
    best.sort(key=lambda t: -t[0])
    return best


def solve(wd, facades, core_side=None, balcony=True, topn=1):
    box = box_of(wd)
    out = band_layouts(box, facades, core_side, balcony)
    return out[:topn]


def ascii_plan(cells, box, W=60):
    x0, y0, w0, d0 = box
    sc = W / w0
    H = max(1, int(d0 * sc / 2))
    grid = [[' '] * W for _ in range(H)]
    for rm, x, y, w, d in cells:
        for yy in range(int((y - y0) * sc / 2), max(int((y - y0) * sc / 2) + 1, int((y + d - y0) * sc / 2))):
            for xx in range(int((x - x0) * sc), min(W, int((x + w - x0) * sc))):
                if 0 <= yy < H and 0 <= xx < W:
                    grid[yy][xx] = rm['k'][0].upper()
    return "\n".join("".join(r) for r in grid)


def export(cells, box, path):
    import json
    data = {'box': {'w': box[2], 'd': box[3]},
            'rooms': [{'k': r['k'], 'fa': r['fa'], 'x': round(x, 3), 'y': round(y, 3),
                       'w': round(w, 3), 'd': round(d, 3), 'a': round(w * d, 2),
                       'fac': ''.join(sorted(touches((r, x, y, w, d), box)))}
                      for r, x, y, w, d in cells]}
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    return data


if __name__ == '__main__':
    # بودجهٔ هر طبقه ۱۹۰.۵ m² | هسته+مشاعات ۲.۶ متر عرض | عمقِ کل ۱۰.۷ m
    DEEP, SHAL, CORE_W, BALC_D = 10.70, 8.30, 3.00, 2.40
    u5 = (190.5 - CORE_W * DEEP) / 2 / DEEP                      # عرضِ هر واحد در گزینهٔ ۵
    w7 = (190.5 - CORE_W * SHAL) / (2 * SHAL + 2 * 0.5 * 0.715 * BALC_D)
    cases = [
        ("۵  (موجود)",        (u5,   DEEP), {'S', 'N'}, 'W',  False),
        ("۵+ (بهبودیافته)",   (w7,   SHAL), {'S', 'N'}, 'E',  True),
        ("۷  (رقیب)",         (w7,   SHAL), {'S', 'N'}, 'W',  True),
    ]
    print(f"عرض واحد: گزینهٔ ۵ = {u5:.2f} m | گزینه‌های ۵+/۷ = {w7:.2f} m")
    import os, json
    OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'layouts.json')
    res = {}
    for name, wd, fac, core, balc in cases:
        sc, cells = solve(wd, fac, core, balc)[0]
        box = box_of(wd)
        print(f"\n=== {name} | جعبه {wd[0]:.2f} × {wd[1]:.2f} = {wd[0]*wd[1]:.1f} m² | امتیاز {sc:.1f} ===")
        print(ascii_plan(cells, box))
        for rm, x, y, w, d in sorted(cells, key=lambda c: (round(c[2], 1), round(c[1], 1))):
            t = touches((rm, x, y, w, d), box)
            print(f"  {rm['fa']:10s} {w:5.2f} × {d:5.2f} = {w*d:6.2f} m²  (هدف {rm['target']:5.1f})  نما: {''.join(sorted(t)) or '—'}")
        res[name.strip()] = {'score': round(sc, 1), 'box': {'w': wd[0], 'd': wd[1]},
                             'rooms': [{'k': rm['k'], 'fa': rm['fa'], 'x': round(x, 2), 'y': round(y, 2),
                                        'w': round(w, 2), 'd': round(d, 2), 'a': round(w * d, 2),
                                        'fac': ''.join(sorted(touches((rm, x, y, w, d), box)))}
                                       for rm, x, y, w, d in cells]}
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    print("\nذخیره شد:", OUT)
