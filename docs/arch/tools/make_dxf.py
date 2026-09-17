#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""خروجیِ DXFِ پلان‌ها از مدلِ یکپارچه (plan_model) — برای مهندسِ طراح
لایه‌ها: WALL · DOOR · WINDOW · ROOM · CORE · PARK · SHOP · DIM · AXIS · TEXT
یکا: متر. خروجی: docs/arch/final-plan.dxf
"""
import os, json
import ezdxf
from ezdxf.enums import TextEntityAlignment
import plan_model as PM

HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT = os.path.join(HERE, "docs", "arch", "final-plan.dxf")

dwg = ezdxf.new("R2010", setup=True)
msp = dwg.modelspace()
for n, c in [("WALL", 7), ("DOOR", 1), ("WINDOW", 4), ("ROOM", 8), ("CORE", 3), ("PARK", 5),
             ("SHOP", 40), ("STORAGE", 50), ("DIM", 2), ("AXIS", 140), ("TEXT", 6), ("FURN", 9)]:
    dwg.layers.add(n, color=c)


def rect(x0, y0, x1, y1, layer="WALL"):
    msp.add_lwpolyline([(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)],
                       dxfattribs={"layer": layer})


def wall(x0, y0, x1, y1, t=PM.T_INT, layer="WALL"):
    if abs(x1 - x0) > abs(y1 - y0):
        rect(x0, y0 - t / 2, x1, y1 + t / 2, layer)
    else:
        rect(x0 - t / 2, y0, x1 + t / 2, y1, layer)


def text(x, y, s, h=0.20, layer="TEXT"):
    msp.add_text(s, height=h, dxfattribs={"layer": layer}).set_placement(
        (x, y), align=TextEntityAlignment.MIDDLE_CENTER)


def dimh(x0, x1, y, layer="DIM"):
    msp.add_linear_dim(base=(0, y - 0.8), p1=(x0, y), p2=(x1, y),
                       dimstyle="EZDXF", dxfattribs={"layer": layer}).render()


def dimv(y0, y1, x, layer="DIM"):
    msp.add_linear_dim(base=(x - 0.8, 0), p1=(x, y0), p2=(x, y1), angle=90,
                       dimstyle="EZDXF", dxfattribs={"layer": layer}).render()


def axis(x, y, name):
    msp.add_line((x, y), (x, y + 1.2), dxfattribs={"layer": "AXIS"})
    msp.add_circle((x, y + 1.6), 0.28, dxfattribs={"layer": "AXIS"})
    text(x, y + 1.6, name, 0.22, "AXIS")


# ---------------------------------------------------------------- واحد
def draw_unit(offx, mirror):
    UWX = PM.UW
    X = lambda x: offx + (UWX - x if mirror else x)
    rooms = PM.mirrored_rooms(offx) if mirror else PM.unit_rooms(offx)
    for r in rooms:
        rect(r["x0"], r["y0"], r["x1"], r["y1"], "ROOM")
        text((r["x0"] + r["x1"]) / 2, (r["y0"] + r["y1"]) / 2 - 0.25, r["name"], 0.22, "TEXT")
        text((r["x0"] + r["x1"]) / 2, (r["y0"] + r["y1"]) / 2 - 0.60,
             f"{r['area']:.2f} m2", 0.18, "TEXT")
    y0 = PM.ENC_Y0
    lw = [("V", 6.56, 0.00, 3.83), ("H", 0.00, 3.83, UWX), ("V", 1.39, 3.83, 5.57),
          ("V", 3.99, 3.83, 5.57), ("H", 0.00, 5.57, UWX), ("V", 5.14, 5.57, 8.30)]
    for kind, a, b1, b2 in lw:
        if kind == "V":
            xx = X(a)
            wall(xx, y0 + b1, xx, y0 + b2, PM.T_INT)
        else:
            wall(min(X(b1), X(b2)), y0 + a, max(X(b1), X(b2)), y0 + a, PM.T_INT)
    # پنجره‌ها
    for side, wx0, wy0, wx1, wy1 in PM.WINDOWS:
        if side in ("W", "E"):
            xx = X(wx0)
            for o in (-PM.T_EXT / 2, 0, PM.T_EXT / 2):
                msp.add_line((xx + o if side == "W" else xx + o, y0 + wy0),
                             (xx + o, y0 + wy1), dxfattribs={"layer": "WINDOW"})
        else:
            xa, xb = X(wx0), X(wx1)
            for o in (-PM.T_EXT / 2, 0, PM.T_EXT / 2):
                msp.add_line((min(xa, xb), y0 + wy0 + o), (max(xa, xb), y0 + wy0 + o),
                             dxfattribs={"layer": "WINDOW"})
    # درِ ایوان
    xa, xb = X(0.90), X(3.60)
    for o in (-PM.T_EXT / 2, 0, PM.T_EXT / 2):
        msp.add_line((min(xa, xb), y0 + o), (max(xa, xb), y0 + o), dxfattribs={"layer": "WINDOW"})
    # درها
    s = 1 if not mirror else -1
    dr = [(9.186, 4.30, 9.186, 5.40, (-0.9, 0)), (4.60, 3.83, 5.80, 3.83, (0, -0.9)),
          (7.20, 3.83, 8.10, 3.83, (0, -0.9)), (3.99, 4.25, 3.99, 5.05, (-0.9, 0)),
          (1.39, 4.25, 1.39, 5.05, (-0.9, 0)), (4.30, 5.57, 5.20, 5.57, (0, 0.9)),
          (6.30, 5.57, 7.20, 5.57, (0, 0.9))]
    for dx0, dy0, dx1, dy1, sw in dr:
        hx, hy = X(dx0), y0 + dy0
        r = abs(dx1 - dx0) if abs(dx1 - dx0) > 0.01 else abs(dy1 - dy0)
        if abs(dx1 - dx0) > 0.01:                      # افقی
            msp.add_line((min(X(dx0), X(dx1)), hy), (min(X(dx0), X(dx1)),
                          hy + (r if sw[1] > 0 else -r)), dxfattribs={"layer": "DOOR"})
            msp.add_arc((hx, hy), r,
                        90 if sw[1] > 0 else 270, 0 if sw[1] > 0 else 360,
                        dxfattribs={"layer": "DOOR"})
        else:
            msp.add_line((hx, hy), (hx + (r * s if sw[0] > 0 else -r * s), hy),
                         dxfattribs={"layer": "DOOR"})
            msp.add_arc((hx, hy), r, 0 if sw[0] > 0 else 180, 90, dxfattribs={"layer": "DOOR"})


def draw_core():
    z = {c["kind"]: c for c in PM.core_zones()}
    st, lf, shf, lb = z["stair"], z["lift"], z["shaft"], z["lobby"]
    for c in (st, lf, lb):
        rect(c["x0"], c["y0"], c["x1"], c["y1"], "CORE")
    rect(shf["x0"], shf["y0"], shf["x1"], shf["y1"], "CORE")
    text((st["x0"] + st["x1"]) / 2, (st["y0"] + st["y1"]) / 2, "STAIR 16R", 0.20, "TEXT")
    text((lf["x0"] + lf["x1"]) / 2, (lf["y0"] + lf["y1"]) / 2, "LIFT", 0.20, "TEXT")
    text((lb["x0"] + lb["x1"]) / 2, (lb["y0"] + lb["y1"]) / 2, "LOBBY", 0.18, "TEXT")
    text((shf["x0"] + shf["x1"]) / 2, (shf["y0"] + shf["y1"]) / 2,
         f"SHAFT {PM.SH_W:.2f}x{PM.SH_D:.2f}", 0.20, "TEXT")
    for (tx0, ty0, tx1, ty1) in PM.stair_treads(st):
        rect(tx0, ty0, tx1, ty1, "CORE")
    wall(shf["x0"], shf["y0"], shf["x1"], shf["y0"], PM.T_CORE)
    wall(st["x0"] + 2.50, st["y0"], st["x0"] + 2.50, st["y1"], PM.T_INT)


# ================================================================ طبقهٔ تیپ (تراز Y=0 در فایل)
YO = -PM.ENC_Y0                       # انتقال: mبدأ در گوشهٔ جنوبیِ فضای بسته


def sh(dx, dy=0.0):
    return dy


def typical(offset_y):
    def T(y):
        return y + offset_y
    for offx, mir in ((0.0, False), (PM.UNIT_B_X, True)):
        rooms = PM.mirrored_rooms(offx) if mir else PM.unit_rooms(offx)
        for r in rooms:
            rect(r["x0"], T(r["y0"] - PM.ENC_Y0), r["x1"], T(r["y1"] - PM.ENC_Y0), "ROOM")
            text((r["x0"] + r["x1"]) / 2, T((r["y0"] + r["y1"]) / 2 - PM.ENC_Y0 - 0.25),
                 r["name"], 0.22, "TEXT")
            text((r["x0"] + r["x1"]) / 2, T((r["y0"] + r["y1"]) / 2 - PM.ENC_Y0 - 0.60),
                 f"{r['area']:.2f} m2", 0.18, "TEXT")
        y0 = T(0.0)
        UWX = PM.UW
        Xl = lambda x: offx + (UWX - x if mir else x)
        lw = [("V", 6.56, 0.00, 3.83), ("H", 0.00, 3.83, UWX), ("V", 1.39, 3.83, 5.57),
              ("V", 3.99, 3.83, 5.57), ("H", 0.00, 5.57, UWX), ("V", 5.14, 5.57, 8.30)]
        for kind, a, b1, b2 in lw:
            if kind == "V":
                xx = Xl(a); wall(xx, y0 + b1, xx, y0 + b2, PM.T_INT)
            else:
                wall(min(Xl(b1), Xl(b2)), y0 + a, max(Xl(b1), Xl(b2)), y0 + a, PM.T_INT)
        for side, wx0, wy0, wx1, wy1 in PM.WINDOWS:
            if side in ("W", "E"):
                xx = Xl(wx0)
                for o in (-PM.T_EXT / 2, 0, PM.T_EXT / 2):
                    msp.add_line((xx + o, y0 + wy0), (xx + o, y0 + wy1),
                                 dxfattribs={"layer": "WINDOW"})
            else:
                xa, xb = Xl(wx0), Xl(wx1)
                for o in (-PM.T_EXT / 2, 0, PM.T_EXT / 2):
                    msp.add_line((min(xa, xb), y0 + wy0 + o), (max(xa, xb), y0 + wy0 + o),
                                 dxfattribs={"layer": "WINDOW"})
        xa, xb = Xl(0.90), Xl(3.60)
        for o in (-PM.T_EXT / 2, 0, PM.T_EXT / 2):
            msp.add_line((min(xa, xb), y0 + o), (max(xa, xb), y0 + o),
                         dxfattribs={"layer": "WINDOW"})
        s = 1 if not mir else -1
        dr = [(9.186, 4.30, 9.186, 5.40, (-0.9, 0)), (4.60, 3.83, 5.80, 3.83, (0, -0.9)),
              (7.20, 3.83, 8.10, 3.83, (0, -0.9)), (3.99, 4.25, 3.99, 5.05, (-0.9, 0)),
              (1.39, 4.25, 1.39, 5.05, (-0.9, 0)), (4.30, 5.57, 5.20, 5.57, (0, 0.9)),
              (6.30, 5.57, 7.20, 5.57, (0, 0.9))]
        for dx0, dy0, dx1, dy1, sw in dr:
            hx, hy = Xl(dx0), y0 + dy0
            r = abs(dx1 - dx0) if abs(dx1 - dx0) > 0.01 else abs(dy1 - dy0)
            if abs(dx1 - dx0) > 0.01:
                msp.add_line((min(Xl(dx0), Xl(dx1)), hy),
                             (min(Xl(dx0), Xl(dx1)), hy + (r if sw[1] > 0 else -r)),
                             dxfattribs={"layer": "DOOR"})
                msp.add_arc((hx, hy), r, 90 if sw[1] > 0 else 270, 0 if sw[1] > 0 else 360,
                            dxfattribs={"layer": "DOOR"})
            else:
                msp.add_line((hx, hy), (hx + (r * s if sw[0] > 0 else -r * s), hy),
                             dxfattribs={"layer": "DOOR"})
                msp.add_arc((hx, hy), r, 0 if sw[0] > 0 else 180, 90, dxfattribs={"layer": "DOOR"})
    # دیوارهای پیرامونی و هسته
    y0 = T(0.0)
    wall(0, y0, PM.BLD_W, y0, PM.T_EXT)
    wall(0, y0 + PM.UD, PM.BLD_W, y0 + PM.UD, PM.T_EXT)
    wall(0, y0, 0, y0 + PM.UD, PM.T_EXT)
    wall(PM.BLD_W, y0, PM.BLD_W, y0 + PM.UD, PM.T_EXT)
    wall(PM.CORE_X0, y0, PM.CORE_X0, y0 + PM.UD, PM.T_CORE)
    wall(PM.CORE_X1, y0, PM.CORE_X1, y0 + PM.UD, PM.T_CORE)
    # هسته
    z = {c["kind"]: c for c in PM.core_zones()}
    for c in (z["stair"], z["lift"], z["lobby"], z["shaft"]):
        rect(c["x0"], T(c["y0"] - PM.ENC_Y0), c["x1"], T(c["y1"] - PM.ENC_Y0), "CORE")
    for (tx0, ty0, tx1, ty1) in PM.stair_treads(z["stair"]):
        rect(tx0, T(ty0 - PM.ENC_Y0), tx1, T(ty1 - PM.ENC_Y0), "CORE")
    text((z["stair"]["x0"] + z["stair"]["x1"]) / 2, T(2.6), "STAIR 16R", 0.20, "TEXT")
    text((z["lift"]["x0"] + z["lift"]["x1"]) / 2, T(0.85), "LIFT", 0.20, "TEXT")
    text((z["shaft"]["x0"] + z["shaft"]["x1"]) / 2, T(6.3),
         f"SHAFT {PM.SH_W:.2f}x{PM.SH_D:.2f}", 0.20, "TEXT")
    # ایوان
    liv = [r for r in PM.ROOMS if r[1] == "living"][0]
    rect(0.0, T(-PM.BALC_D), (liv[4] - liv[2]), T(0.0), "WALL")
    rect(PM.BLD_W - (liv[4] - liv[2]), T(-PM.BALC_D), PM.BLD_W, T(0.0), "WALL")
    text((liv[4] - liv[2]) / 2, T(-PM.BALC_D / 2), "BALCONY", 0.22, "TEXT")
    # ابعاد و محورها
    dimh(0, PM.UW, T(-PM.BALC_D - 0.6))
    dimh(PM.UW, PM.CORE_X1, T(-PM.BALC_D - 0.6))
    dimh(PM.CORE_X1, PM.BLD_W, T(-PM.BALC_D - 0.6))
    dimh(0, PM.BLD_W, T(-PM.BALC_D - 1.4))
    dimv(T(-PM.BALC_D), T(PM.UD), PM.BLD_W + 0.9)
    for i, x in enumerate([0, PM.UW, PM.CORE_X1, PM.BLD_W]):
        axis(x, T(PM.UD + 0.6), ["A", "B", "C", "D"][i])
    text(PM.BLD_W / 2, T(PM.UD + 2.2),
         f"TYPICAL FLOOR x{PM.NFL} - 2 UNITS OF {PM.summary()['unit_sale']} m2", 0.32, "TEXT")


# ================================================================ همکف
def ground(off):
    def T(y):
        return y + off
    rect(0, T(PM.Y0), PM.LAND_W, T(PM.Y1), "WALL")
    n = 0
    for bay in (0.5, PM.CORE_X1 + 0.4):
        for i in range(3):
            if bay + i * 2.65 + PM.PARK_W > PM.SHOP_X0 - 0.2:
                break
            n += 1
            x0 = bay + i * 2.65
            rect(x0, T(PM.Y0 + 0.5), x0 + PM.PARK_W, T(PM.Y0 + 0.5 + PM.PARK_L), "PARK")
            text(x0 + PM.PARK_W / 2, T(PM.Y0 + 3.0), str(n), 0.3, "TEXT")
    for i in range(PM.NSHOP):
        x0 = PM.SHOP_X0 + i * PM.SHOP_W
        rect(x0, T(PM.Y1 - PM.SHOP_DEEP), x0 + PM.SHOP_W, T(PM.Y1), "SHOP")
        text(x0 + PM.SHOP_W / 2, T(PM.Y1 - PM.SHOP_DEEP / 2),
             f"SHOP {i+1} {PM.summary()['shop_area']} m2", 0.24, "TEXT")
    rect(PM.SHOP_X0, T(PM.Y0), PM.LAND_W, T(PM.Y1 - PM.SHOP_DEEP), "SHOP")
    rect(PM.CORE_X0, T(PM.Y1 - 5.10), PM.CORE_X1, T(PM.Y1), "CORE")
    text((PM.CORE_X0 + PM.CORE_X1) / 2, T(PM.Y1 - 2.5), "LOBBY/STAIR/LIFT", 0.24, "TEXT")
    dimh(0, PM.BLD_W, T(PM.Y0 - 0.7))
    dimh(PM.SHOP_X0, PM.LAND_W, T(PM.Y0 - 0.7))
    text(PM.LAND_W / 2, T(PM.Y0 - 2.6), "GROUND FLOOR - 3 SHOPS + PARKING + CORE", 0.32, "TEXT")


def mezz(off):
    def T(y):
        return y + off
    rect(0, T(PM.Y0), PM.LAND_W, T(PM.Y1), "WALL")
    for i in range(PM.ANB_N):
        x0 = 0.4 + i * 2.60
        if x0 + PM.ANB_W > PM.SHOP_X0 - 0.3:
            break
        rect(x0, T(PM.Y0 + 0.3), x0 + PM.ANB_W, T(PM.Y0 + 0.3 + PM.ANB_D), "STORAGE")
        text(x0 + PM.ANB_W / 2, T(PM.Y0 + 1.4), f"S{i+1}", 0.20, "TEXT")
    for i in range(PM.NSHOP):
        x0 = PM.SHOP_X0 + i * PM.SHOP_W
        rect(x0, T(PM.Y1 - PM.MEZ_DEEP), x0 + PM.SHOP_W, T(PM.Y1), "SHOP")
        text(x0 + PM.SHOP_W / 2, T(PM.Y1 - PM.MEZ_DEEP / 2),
             f"MEZZ {i+1} {PM.SHOP_W*PM.MEZ_DEEP:.1f} m2", 0.22, "TEXT")
    rect(PM.CORE_X0, T(PM.Y1 - 5.10), PM.CORE_X1, T(PM.Y1), "CORE")
    text(PM.LAND_W / 2, T(PM.Y0 - 2.6), "LEVEL +2.60 - STORAGE (FAR EXEMPT) + MEZZANINE (20%)",
         0.32, "TEXT")


def roof(off):
    def T(y):
        return y + off
    rect(0, T(PM.Y0), PM.LAND_W, T(PM.Y1), "WALL")
    rect(0, T(PM.ENC_Y0 - PM.ENC_Y0), PM.BLD_W, T(PM.UD), "WALL")
    rect(PM.BLD_W, T(PM.Y0 - PM.ENC_Y0), PM.LAND_W, T(PM.Y1 - PM.ENC_Y0), "WALL")
    z = {c["kind"]: c for c in PM.core_zones()}
    shf = z["shaft"]
    rect(shf["x0"], T(shf["y0"] - PM.ENC_Y0), shf["x1"], T(shf["y1"] - PM.ENC_Y0), "CORE")
    rect(z["stair"]["x0"], T(z["stair"]["y0"] - PM.ENC_Y0), z["lift"]["x1"],
         T(z["stair"]["y1"] - PM.ENC_Y0), "CORE")
    text(PM.BLD_W / 2, T(PM.UD / 2), "ROOF", 0.32, "TEXT")
    text((PM.BLD_W + PM.LAND_W) / 2, T((PM.Y0 + PM.Y1) / 2 - PM.ENC_Y0), "TERRACE", 0.32, "TEXT")
    text(PM.LAND_W / 2, T(-2.6), f"ROOF LEVEL +{PM.TOP:.2f}", 0.32, "TEXT")


# ---------------------------------------------------------------- چیدمانِ سطح‌ها در فایل
typical(0.0)
ground(-30.0)
mezz(-60.0)
roof(-90.0)
text(0, 12.0, "Chat2DB - ARCH PACKAGE - units: metres", 0.5, "TEXT")

dwg.saveas(OUT)
s = PM.summary()
print("ذخیره:", OUT)
print("موجودیت‌ها:", len(msp))
print(json.dumps(s, ensure_ascii=False))
