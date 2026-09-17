#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""خروجیِ DXF از پلانِ نهایی (طبقهٔ تیپ + همکف + سطحِ انباری/نیم‌طبقه) برای مهندسِ طراح
دستگاهِ مختصات: X از لبهٔ غربیِ زمینِ خالص، Y از لبهٔ جنوبیِ زمینِ خالص، واحد متر.
خروجی: docs/arch/final-plan.dxf
"""
import json, os
import ezdxf
from ezdxf.enums import TextEntityAlignment

HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT = os.path.join(HERE, "docs", "arch", "final-plan.dxf")
L = json.load(open(os.path.join(HERE, "docs", "arch", "final-layout.json"), encoding="utf-8"))
try:
    V = json.load(open('/tmp/v2.json', encoding='utf-8'))
except Exception:
    V = {'nfl': 5, 'fl_h': 2.90, 'pod': 5.40, 'mez_phys': 25.0}

W, D = 40.57, 13.37
Y0, Y1 = 2.67, 13.37                       # محدودهٔ ساخت (عمق ۱۰.۷۰)
UW, UD = L["unit"]["w"], L["unit"]["d"]    # ۹.۵۳۳ × ۸.۳۰
BALC = 2.40
CORE_W = L["building"]["core_w"]
SH_W, SH_D = 3.00, 3.00
BLD_W = 2 * UW + CORE_W
SHOP_X0, SHOP_DEEP = 21.07, 7.00
YS = Y0 + BALC                             # لبهٔ جنوبیِ فضای بسته

dwg = ezdxf.new("R2010", setup=True)
msp = dwg.modelspace()
dwg.layers.add("PLAN-WALL", color=7)
dwg.layers.add("PLAN-ROOM", color=8)
dwg.layers.add("PLAN-CORE", color=1)
dwg.layers.add("PLAN-BALC", color=30)
dwg.layers.add("PLAN-SHOP", color=40)
dwg.layers.add("PLAN-PARK", color=5)
dwg.layers.add("PLAN-ANB", color=50)
dwg.layers.add("PLAN-MEZ", color=42)
dwg.layers.add("OUTLINE", color=2)
dwg.layers.add("TEXT", color=3)


def rect(x0, y0, x1, y1, layer="PLAN-WALL"):
    msp.add_lwpolyline([(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)],
                       dxfattribs={"layer": layer})


def label(x, y, t, h=0.22, layer="TEXT"):
    msp.add_text(t, height=h, dxfattribs={"layer": layer}).set_placement(
        (x, y), align=TextEntityAlignment.MIDDLE_CENTER)


# ---------------------------------------------------------------- زمین و ردپا
rect(0, 0, W, D, "OUTLINE")                       # زمینِ خالص
rect(0, Y0, BLD_W, Y1, "OUTLINE")                 # ردپای ساختمان (با ایوان)
rect(0, YS, BLD_W, Y1, "PLAN-WALL")               # فضای بسته


def typical_floor(yoff):
    """یک طبقهٔ تیپ را در تراز yoff می‌کشد"""
    rooms = L["rooms"]
    for k in (0, 1):
        base = 0 if k == 0 else UW + CORE_W
        liv = [r for r in rooms if r["k"] == "living"][0]
        bx0 = liv["x"] if k == 0 else UW - liv["x"] - liv["w"]
        rect(base + bx0, yoff - BALC, base + bx0 + liv["w"], yoff, "PLAN-BALC")
        label(base + bx0 + liv["w"] / 2, yoff - BALC / 2, "BALCONY 2.40", 0.18)
        for r in rooms:
            rx = (base + r["x"]) if k == 0 else (base + UW - r["x"] - r["w"])
            rect(rx, yoff + r["y"], rx + r["w"], yoff + r["y"] + r["d"], "PLAN-ROOM")
            label(rx + r["w"] / 2, yoff + r["y"] + r["d"] / 2, f"{r['a']:.1f}", 0.17)
    # هسته
    rect(UW, yoff, UW + CORE_W, yoff + UD, "PLAN-CORE")
    # شفت ۳×۳
    rect(UW, yoff + UD - SH_D, UW + SH_W, yoff + UD, "PLAN-CORE")
    label(UW + SH_W / 2, yoff + UD - SH_D / 2, "SHAFT 3x3", 0.18)
    # آسانسور و پله
    rect(UW + 0.15, yoff + 0.15, UW + 1.75, yoff + 1.75, "PLAN-CORE")
    rect(UW + 1.80, yoff + 0.30, UW + 2.85, yoff + 5.30, "PLAN-CORE")


typical_floor(YS)

# ---------------------------------------------------------------- پیلوت (در ترازِ جداگانه)
PY = -22.0                                        # زیرِ پلان، برایِ خوانایی
rect(0, PY, W, PY + 10.70, "OUTLINE")
for bay in (0.5, 13.0):
    for i in range(3):
        x0 = bay + i * 2.65
        rect(x0, PY + 0.4, x0 + 2.5, PY + 5.4, "PLAN-PARK")
for i in range(3):
    x0 = SHOP_X0 + i * 6.5
    rect(x0, PY + 10.70 - SHOP_DEEP, x0 + 6.5, PY + 10.70, "PLAN-SHOP")
    label(x0 + 3.25, PY + 10.70 - SHOP_DEEP / 2, f"SHOP {i+1} 45.5", 0.20)
rect(SHOP_X0, PY, W, PY + 10.70 - SHOP_DEEP, "PLAN-SHOP")
rect(UW, PY + 5.6, UW + CORE_W, PY + 10.70, "PLAN-CORE")

# ---------------------------------------------------------------- سطحِ انباری و نیم‌طبقه (تراز ۲.۶۰+)
AY = -44.0
rect(0, AY, W, AY + 10.70, "OUTLINE")
for i in range(8):
    x0 = 0.4 + i * 2.60
    rect(x0, AY + 0.4, x0 + 2.4, AY + 2.6, "PLAN-ANB")
    label(x0 + 1.2, AY + 1.5, f"ANBARI {i+1}", 0.18)
for i in range(3):
    x0 = SHOP_X0 + i * 6.5
    rect(x0, AY + 3.2, x0 + 6.5, AY + 7.7, "PLAN-MEZ")
    label(x0 + 3.25, AY + 5.45, f"MEZZANINE {i+1} 25", 0.20)
label(SHOP_X0 / 2, AY - 1.2, "LEVEL +2.60 : 8 STORAGE (FAR-EXEMPT) + 3 MEZZANINE (20% OF AREA IN FAR)",
      0.26)
label(W / 2, PY - 1.2, "GROUND : 3 SHOPS + 6 PARKING + CORE (clear height 2.40 m)", 0.26)
label(BLD_W / 2, YS + 3.0, f"TYPICAL FLOOR x{V.get('nfl',5)} : 2 UNITS OF {L['unit']['sale']} m2", 0.30)

# ---------------------------------------------------------------- ابعادِ کلیدی
def dim(x0, y0, x1, y1, t, off=1.2):
    msp.add_aligned_dim(p1=(x0, y0), p2=(x1, y1), text=t,
                        dimstyle="EZDXF",
                        override={"dimtxsty": "Standard"}).render()
    msp.add_line((x0, y0 - off), (x1, y1 - off), dxfattribs={"layer": "OUTLINE"})


label(BLD_W / 2, Y1 + 1.6, f"BUILDING WIDTH {BLD_W:.2f} m", 0.30)
label(BLD_W / 2, Y0 - 1.2, "BALCONY DEPTH 2.40 m / ENCLOSED DEPTH 8.30 m", 0.26)
label(-3.2, (Y0 + Y1) / 2, f"TOTAL DEPTH 10.70 m", 0.26)
label(BLD_W / 2, PY - 1.2, "PILOTIS: 3 SHOPS + 6 PARKING + CORE (clear height 2.40 m)", 0.26)

dwg.saveas(OUT)
print("saved:", OUT)
print(f"ردپا {BLD_W:.2f} × ۱۰.۷۰ | واحد {L['unit']['encl']}+{L['unit']['balcony']} = {L['unit']['sale']} m²")
