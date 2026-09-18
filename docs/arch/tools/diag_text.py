#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""تشخیصِ عددیِ مشکل‌هایِ متن در برگه‌های A3:
اندازهٔ واقعی به میلی‌متر، بیرون‌زدگی از کادر، هم‌پوشانی، متنِ چرخیده
"""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault("A3_DIAG", "1")
import render_a3 as R
from PIL import ImageFont

REC = []
DPI = R.DPI
MM = R.MM


def fa(s):
    return R.fa(s) if hasattr(R, "fa") else s


_orig_t = R.A3Sheet.t


LAST = {}
_origF = R.F


def F(sz, bold=False):
    LAST["sz"], LAST["bold"] = sz, bold
    return _origF(sz, bold)


R.F = F


def t(self, xy, s, size=14, fill=(35, 35, 35), bold=False, anchor="mm", bg=None,
      rot=0, max_w=None, **kw):
    box = _orig_t(self, xy, s, size=size, fill=fill, bold=bold, anchor=anchor,
                  bg=bg, rot=rot, max_w=max_w, **kw)
    em = LAST.get("sz", size * self.tscale)
    REC.append(dict(sheet=getattr(self, "no", "?"), text=str(s), size=size, rot=rot,
                    bold=bold, anchor=anchor, bg=bg, box=box, em=em,
                    mm=em * 0.72 / MM, skipped=box is None))
    return box


R.A3Sheet.t = t
_orig_save = R.A3Sheet.save


def save(self, path):
    return path


R.A3Sheet.save = save

STRIP_X0 = R.A3W - 8 * MM - R.STRIP_W
STRIP_X1 = R.A3W - 8 * MM
FRAME = (R.MARGIN, R.MARGIN, R.MARGIN + R.DRAW_W, R.MARGIN + R.DRAW_H)

print("=" * 94)
print("گزارشِ تشخیصیِ متن‌هایِ برگه‌های A3")
print("=" * 94)

for fn in (R.sheet_ground, R.sheet_mezz, R.sheet_typical, R.sheet_roof):
    REC.clear()
    fn()
    nm = fn.__name__
    print(f"\n──── {nm}: {len(REC)} متن ────")
    # ۱) اندازهٔ واقعیِ حروف به میلی‌متر
    hs = [(r["mm"], r) for r in REC if not r["skipped"]]
    hs.sort(key=lambda z: z[0])
    print(f"  کوچک‌ترین بلندای حرف: {hs[0][0]:.2f} mm  («{hs[0][1]['text'][:30]}» size={hs[0][1]['size']})")
    print(f"  بزرگ‌ترین بلندای حرف: {hs[-1][0]:.2f} mm  («{hs[-1][1]['text'][:30]}» size={hs[-1][1]['size']})")
    small = [x for x in hs if x[0] < 2.5]
    print(f"  متن‌های زیرِ حدِّ خوانایی (۲.۵ mm): {len(small)} از {len(hs)}")
    # ۲) بیرون‌زدگی از نوارِ ترسیم
    out_strip = [r for r in REC if not r["skipped"]
                 if r["box"][0] >= STRIP_X0 - 400 and
                 (r["box"][0] < STRIP_X0 + 4 or r["box"][2] > STRIP_X1 - 4 or
                  r["box"][1] < 8 * MM or r["box"][3] > R.A3H - 8 * MM)]
    if out_strip:
        print(f"  ⚠ بیرون‌زدگی از نوارِ ترسیم: {len(out_strip)}")
        for r in out_strip[:6]:
            print(f"      «{r['text'][:40]}»  x {r['box'][0]:.0f}..{r['box'][2]:.0f} "
                  f"(کادر {STRIP_X0:.0f}..{STRIP_X1:.0f})")
    # ۳) بیرون‌زدگی از ورق
    off = [r for r in REC if not r["skipped"] and r["box"][0] < 2 or r["box"][1] < 2 or
           r["box"][2] > R.A3W - 2 or r["box"][3] > R.A3H - 2]
    if off:
        print(f"  ⚠ بیرون‌زدگی از ورق: {len(off)}")
        for r in off[:6]:
            print(f"      «{r['text'][:40]}»  جعبه {r['box'][0]:.0f},{r['box'][1]:.0f}"
                  f"..{r['box'][2]:.0f},{r['box'][3]:.0f}")
    # ۴) بیرون‌زدگی از کادرِ ترسیم (متن‌هایِ رویِ نقشه)
    outd = [r for r in REC if not r["skipped"] and r["box"][2] < STRIP_X0 and
            (r["box"][0] < FRAME[0] - 30 or r["box"][2] > FRAME[2] + 30 or
             r["box"][1] < FRAME[1] - 30 or r["box"][3] > FRAME[3] + 30)]
    if outd:
        print(f"  ⚠ بیرون‌زدگی از کادرِ ترسیم: {len(outd)}")
        for r in outd[:6]:
            print(f"      «{r['text'][:40]}»  جعبه {r['box'][0]:.0f},{r['box'][1]:.0f}"
                  f"..{r['box'][2]:.0f},{r['box'][3]:.0f}  (کادر "
                  f"{FRAME[0]:.0f},{FRAME[1]:.0f}..{FRAME[2]:.0f},{FRAME[3]:.0f})")
    # ۵) متنِ چرخیده
    rot = [r for r in REC if r["rot"] and not r["skipped"]]
    if rot:
        print(f"  متنِ چرخیده: {len(rot)}  (با زمینه: {sum(1 for r in rot if r['bg'])} تا)")
    sk = sum(1 for r in REC if r["skipped"])
    if sk:
        print(f"  متن‌های حذف‌شده چون جا نمی‌شدند: {sk}")
    # ۶) هم‌پوشانیِ متن‌ها
    ov = []
    live = [r for r in REC if not r["skipped"]]
    for i in range(len(live)):
        for j in range(i + 1, len(live)):
            a, b = live[i]["box"], live[j]["box"]
            ix = min(a[2], b[2]) - max(a[0], b[0])
            iy = min(a[3], b[3]) - max(a[1], b[1])
            if ix > 6 and iy > 6:
                ov.append((ix * iy, live[i]["text"], live[j]["text"]))
    ov.sort(reverse=True)
    if ov:
        print(f"  ⚠ هم‌پوشانیِ متن‌ها: {len(ov)} جفت")
        for area, a, b in ov[:6]:
            print(f"      «{a[:26]}» ✕ «{b[:26]}»  ({math.sqrt(area):.0f} px)")

print("\n" + "=" * 94)
print(f"قطع: {R.A3W}×{R.A3H} px = ۴۲۰×۲۹۷ mm در ۳۰۰ DPI | یک میلی‌متر = {MM:.2f} px")
print(f"کادرِ ترسیم: {FRAME[0]:.0f},{FRAME[1]:.0f} .. {FRAME[2]:.0f},{FRAME[3]:.0f}")
print(f"نوارِ ترسیم: {STRIP_X0:.0f} .. {STRIP_X1:.0f}  (پهنا {R.STRIP_W/MM:.0f} mm)")
