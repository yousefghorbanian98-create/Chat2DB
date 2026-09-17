#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""خروجیِ مدل سه‌بعدی برای برنامه‌های رندر (OBJ + MTL)
یکا: متر · محورِ Z رو به بالا · مبدأ: گوشهٔ جنوب‌غربیِ زمین
قابلِ وارد کردن در: D5 Render · Twinmotion · Blender · SketchUp · 3ds Max · Lumion · Revit
خروجی: docs/arch/model/{model.obj, model.mtl, راهنمای-ورود.md}
"""
import os, math
import plan_model as PM

HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT = os.path.join(HERE, "docs", "arch", "model")
os.makedirs(OUT, exist_ok=True)

# گروه‌ها بر حسبِ مصالح — در برنامهٔ مقصد به‌همین نام‌ها دیده می‌شوند
GROUP = {}
verts, faces = [], []


def add_box(name, x0, y0, z0, x1, y1, z1, mat):
    base = len(verts)
    p = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
         (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
    verts.extend(p)
    quads = [(1, 2, 6, 5), (2, 3, 7, 6), (3, 4, 8, 7), (4, 1, 5, 8), (5, 6, 7, 8), (4, 3, 2, 1)]
    for q in quads:
        a, b, c, d = [base + i - 1 for i in q]
        faces.append((name, mat, (a, b, c), (a, c, d)))


def build():
    z = {c["kind"]: c for c in PM.core_zones()}
    shf = z["shaft"]
    # سایت
    add_box("SITE_PLOT", 0, 0, -0.02, PM.LAND_W, PM.LAND_D, 0.0, "site")
    # پودیوم
    add_box("PODIUM_PARKING", 0, PM.Y0, 0, PM.SHOP_X0, PM.Y1, PM.POD_H, "concrete")
    add_box("PODIUM_SHOPS", PM.SHOP_X0, PM.Y0, 0, PM.LAND_W, PM.Y1, PM.POD_H, "shopfront")
    add_box("PODIUM_TERRACE", PM.BLD_W, PM.Y0, PM.POD_H - 0.30, PM.LAND_W, PM.Y1, PM.POD_H, "terrace")
    # حجمِ مسکونی
    liv = [r for r in PM.ROOMS if r[1] == "living"][0]
    for f in range(PM.NFL):
        z0 = PM.POD_H + f * PM.FL_H
        z1 = z0 + PM.FL_H
        add_box(f"FLOOR_{f+1}_WEST_WING", 0, PM.ENC_Y0, z0, PM.UW, PM.ENC_Y1, z1, "facade")
        add_box(f"FLOOR_{f+1}_EAST_WING", PM.UNIT_B_X, PM.ENC_Y0, z0, PM.BLD_W, PM.ENC_Y1, z1,
                "facade")
        add_box(f"FLOOR_{f+1}_CORE", PM.CORE_X0, PM.ENC_Y0, z0, PM.CORE_X1,
                PM.ENC_Y1 - PM.SH_D, z1, "core")
        add_box(f"FLOOR_{f+1}_SLAB_W", 0, PM.BALC_Y0, z0 - 0.30, PM.UW, PM.ENC_Y1, z0, "slab")
        add_box(f"FLOOR_{f+1}_SLAB_E", PM.UNIT_B_X, PM.BALC_Y0, z0 - 0.30, PM.BLD_W, PM.ENC_Y1,
                z0, "slab")
        # ایوان
        add_box(f"FLOOR_{f+1}_BALCONY_W", liv[2], PM.BALC_Y0, z0 - 0.30, liv[4], PM.ENC_Y0, z0,
                "balcony")
        bx0, bx1 = PM.BLD_W - liv[4], PM.BLD_W - liv[2]
        add_box(f"FLOOR_{f+1}_BALCONY_E", bx0, PM.BALC_Y0, z0 - 0.30, bx1, PM.ENC_Y0, z0,
                "balcony")
        add_box(f"FLOOR_{f+1}_RAIL_W", liv[2], PM.BALC_Y0, z0, liv[4], PM.BALC_Y0 + 0.12, z1,
                "railing")
        add_box(f"FLOOR_{f+1}_RAIL_E", bx0, PM.BALC_Y0, z0, bx1, PM.BALC_Y0 + 0.12, z1, "railing")
    # دیواره‌های شفت
    add_box("SHAFT_WALL_W", shf["x0"] - 0.15, shf["y0"], PM.POD_H, shf["x0"], shf["y1"], PM.TOP,
            "core")
    add_box("SHAFT_WALL_E", shf["x1"], shf["y0"], PM.POD_H, shf["x1"] + 0.15, shf["y1"], PM.TOP,
            "core")
    add_box("SHAFT_WALL_S", shf["x0"], shf["y0"] - 0.15, PM.POD_H, shf["x1"], shf["y0"], PM.TOP,
            "core")
    # بام
    add_box("ROOF_SLAB", 0, PM.ENC_Y0, PM.TOP - 0.30, PM.BLD_W, PM.ENC_Y1, PM.TOP, "roof")
    add_box("ROOF_PARAPET", 0, PM.ENC_Y1 - 0.25, PM.TOP, PM.BLD_W, PM.ENC_Y1, PM.TOP + PM.PARAPET,
            "parapet")
    add_box("TERRACE_RAIL", PM.BLD_W, PM.Y0, PM.POD_H, PM.LAND_W, PM.Y0 + 0.15,
            PM.POD_H + 1.10, "railing")
    add_box("ENTRANCE_CANOPY", PM.CORE_X0, PM.Y1, 0, PM.CORE_X0 + 2.6, PM.Y1 + 2.5, 3.20,
            "concrete")
    for i in range(PM.NSHOP):
        x0 = PM.SHOP_X0 + i * PM.SHOP_W
        add_box(f"SHOP_{i+1}_SIGN", x0, PM.Y1 - 0.10, 3.40, x0 + PM.SHOP_W, PM.Y1 + 1.60, 3.55,
                "sign")


MTL = {
    "facade":    (0.78, 0.74, 0.67),
    "core":      (0.70, 0.68, 0.64),
    "concrete":  (0.58, 0.57, 0.55),
    "slab":      (0.62, 0.61, 0.59),
    "balcony":   (0.66, 0.62, 0.57),
    "railing":   (0.22, 0.26, 0.30),
    "shopfront": (0.16, 0.18, 0.21),
    "glass":     (0.12, 0.15, 0.20),
    "roof":      (0.50, 0.49, 0.47),
    "parapet":   (0.68, 0.66, 0.63),
    "terrace":   (0.30, 0.42, 0.22),
    "site":      (0.52, 0.48, 0.43),
    "sign":      (0.85, 0.83, 0.80),
}

if __name__ == "__main__":
    build()
    obj = os.path.join(OUT, "model.obj")
    with open(obj, "w", encoding="utf-8") as f:
        f.write("# مدل سه‌بعدی — زمین ۵۴۲٫۳۸ m² اصفهان\n")
        f.write("# یکا: متر · محور Z رو به بالا · مبدأ: گوشه جنوب‌غربی زمین\n")
        f.write("mtllib model.mtl\n")
        for v in verts:
            f.write("v %.4f %.4f %.4f\n" % v)
        cur = None
        for name, mat, t1, t2 in faces:
            if name != cur:
                f.write(f"g {name}\nusemtl {mat}\n")
                cur = name
            f.write("f %d %d %d\n" % tuple(i + 1 for i in t1))
            f.write("f %d %d %d\n" % tuple(i + 1 for i in t2))
    with open(os.path.join(OUT, "model.mtl"), "w", encoding="utf-8") as f:
        for k, c in MTL.items():
            f.write(f"newmtl {k}\nKd {c[0]:.3f} {c[1]:.3f} {c[2]:.3f}\nKa 0.05 0.05 0.05\n"
                    f"Ks 0.08 0.08 0.08\nNs 40\n\n")
    n_g = len({n for n, *_ in faces})
    print(f"مدل: {len(verts)} رأس · {len(faces)*2} وجه · {n_g} گروه")
    print("ذخیره:", obj)
