#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""تولیدِ اسکریپتِ یک‌کلیکِ بلندر برایِ هر دو طرح — داده‌ها توکار می‌شوند."""
import os, sys, json, math, shutil
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plan_schemes as PS

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # docs/arch
SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "make_blender_script.py")
_t = open(SRC, encoding="utf-8").read()
TEMPLATE = _t[_t.index("TEMPLATE = r'''") + 15: _t.index("'''\n\nscript =")]

ov = json.load(open(os.path.join(HERE, "geo", "overpass.json")))
LAT0, LON0 = 32.6305401, 51.7238816
MLAT, MLON = 110734.0, 111320.0 * math.cos(math.radians(32.63))
PLC_X, PLC_Y = 20.285, 6.685
HW_W = {"secondary": 22.0, "secondary_link": 12.0, "residential": 8.5, "track": 5.0}
streets = []
for e in ov["elements"]:
    g = e.get("geometry")
    if not g or len(g) < 2:
        continue
    hw = e.get("tags", {}).get("highway")
    if not hw:
        continue
    pts = [(round((p["lon"] - LON0) * MLON + PLC_X, 2),
            round((p["lat"] - LAT0) * MLAT + PLC_Y, 2)) for p in g]
    if any(-120 < x < 160 and -120 < y < 160 for x, y in pts):
        streets.append((pts, HW_W.get(hw, 7.0), hw))

AER = dict(w=1280, h=1792, mx=0.2515, my=0.2498, px=604.75, py=839.35, cx=20.285, cy=6.685)

MP = {
    "facade":    ((0.78, 0.735, 0.665), 0.62, 0.0),
    "concrete":  ((0.58, 0.57, 0.55), 0.78, 0.0),
    "slab":      ((0.62, 0.61, 0.59), 0.80, 0.0),
    "balcony":   ((0.60, 0.55, 0.48), 0.70, 0.0),
    "railing":   ((0.18, 0.22, 0.26), 0.18, 0.75),
    "shopfront": ((0.10, 0.13, 0.17), 0.06, 0.10),
    "roof":      ((0.50, 0.49, 0.47), 0.85, 0.0),
    "parapet":   ((0.68, 0.66, 0.63), 0.70, 0.0),
    "core":      ((0.70, 0.67, 0.63), 0.70, 0.0),
    "site":      ((0.52, 0.48, 0.43), 0.95, 0.0),
    "sign":      ((0.85, 0.83, 0.80), 0.55, 0.0),
    "parking":   ((0.42, 0.46, 0.55), 0.85, 0.0),
}


def boxes(kind):
    """ساختِ جعبه‌هایِ سه‌بعدیِ طرح — Z رو به بالا، مبدأ گوشهٔ جنوب‌غربیِ زمین"""
    B, out = [], None
    W, Y0, Y1 = PS.BLD_W, PS.Y0, PS.Y1

    def bx(name, x0, y0, z0, x1, y1, z1, m):
        B.append((name, round(x0, 3), round(y0, 3), round(z0, 3),
                  round(x1, 3), round(y1, 3), round(z1, 3), m))

    lv = PS.levels(kind)
    z_res = [l[1] for l in lv if l[0].startswith("طبقه")]
    z_top = lv[-1][1]
    z_base = 0.0
    pil_h = PS.PIL_H if kind == 'pilotis' else PS.SHOP_H

    bx("SITE_PLOT", 0, 0, -0.05, PS.LAND_W, PS.LAND_D, 0.0, "site")
    # پیلوت یا همکفِ مغازه
    bx("BASE_SLAB", 0, Y0, -0.30, W, Y1, 0.0, "concrete")
    for c in PS.cores():
        bx("BASE_CORE", c['x0'], c['y0'], 0.0, c['x1'], c['y1'], pil_h, "core")
    if kind == 'pilotis':
        for r in PS.parking_rows():
            bx("PARK_LINE", r['x0'], r['y0'], 0.02, r['x1'], r['y1'], 0.05, "parking")
        for i in range(0, 6):                      # ستون‌هایِ پیلوت
            x = 2.0 + i * (W - 4.0) / 5.0
            bx("PILOTIS_COL", x - 0.20, Y1 - 3.2 - 0.20, 0.0,
               x + 0.20, Y1 - 3.2 + 0.20, pil_h, "concrete")
    else:
        for s in PS.shops(4):
            bx("SHOP", s['x0'], s['y0'], 0.05, s['x1'], s['y1'], pil_h, "shopfront")

    # طبقاتِ مسکونی
    for fi, z in enumerate(z_res, start=1):
        n = f"F{fi}"
        bx(f"{n}_SLAB", 0, Y0, z - 0.30, W, Y1, z, "slab")
        bx(f"{n}_WALL_W", 0, Y0, z, 0.30, Y1, z + PS.FL_H, "facade")
        bx(f"{n}_WALL_E", W - 0.30, Y0, z, W, Y1, z + PS.FL_H, "facade")
        bx(f"{n}_WALL_S", 0, Y0 + PS.BALC, z, W, Y0 + PS.BALC + 0.25, z + PS.FL_H, "facade")
        bx(f"{n}_WALL_N", 0, Y1 - 0.30, z, W, Y1, z + PS.FL_H, "facade")
        for c in PS.cores():
            bx(f"{n}_CORE", c['x0'], c['y0'], z, c['x1'], c['y1'], z + PS.FL_H, "core")
        for u in PS.unit_boxes():
            bx(f"{n}_PARTY", u['x0'] - 0.10, u['y0'], z, u['x0'] + 0.10, u['y1'],
               z + PS.FL_H, "concrete")
            bx(f"{n}_BALC", u['x0'], u['by0'], z, u['x1'], u['by1'], z + 0.12, "balcony")
            bx(f"{n}_RAIL", u['x0'], u['by0'], z, u['x1'], u['by0'] + 0.12,
               z + 1.10, "railing")
            bx(f"{n}_RAIL_S", u['x0'], u['by0'], z, u['x0'] + 0.12, u['by1'],
               z + 1.10, "railing")
            bx(f"{n}_RAIL_E", u['x1'] - 0.12, u['by0'], z, u['x1'], u['by1'],
               z + 1.10, "railing")

    # بام
    bx("ROOF_SLAB", 0, Y0, z_top - 0.30, W, Y1, z_top, "roof")
    bx("ROOF_PARAPET_W", 0, Y0, z_top, 0.25, Y1, z_top + PS.PARAPET, "parapet")
    bx("ROOF_PARAPET_E", W - 0.25, Y0, z_top, W, Y1, z_top + PS.PARAPET, "parapet")
    bx("ROOF_PARAPET_S", 0, Y0, z_top, W, Y0 + 0.25, z_top + PS.PARAPET, "parapet")
    bx("ROOF_PARAPET_N", 0, Y1 - 0.25, z_top, W, Y1, z_top + PS.PARAPET, "parapet")
    for c in PS.cores():
        bx("ROOF_CORE", c['x0'], c['y0'], z_top, c['x1'], c['y1'], z_top + 2.80, "core")
    return B


def emit(kind, outdir, cams):
    os.makedirs(outdir, exist_ok=True)
    B = boxes(kind)
    s = PS.summary('shops' if kind == 'shops' else 'pilotis', nshop=(4 if kind == 'shops' else 0))
    doc = TEMPLATE
    doc = doc.replace('"""ساختِ خودکارِ صحنهٔ سه‌بعدی در بلندر — زمین ۵۴۲٫۳۸ m²، اصفهان',
                      f'"""ساختِ خودکارِ صحنهٔ سه‌بعدی در بلندر — زمین ۵۴۲٫۳۸ m²، اصفهان\n'
                      f'طرح {"اول (مغازه + ۳ طبقه)" if kind=="shops" else "دوم (تماماً مسکونی)"}\n'
                      f'{s["units"]} واحد · ارتفاع {s["height"]:.2f} m · تراکم {s["far"]:.1f}٪')
    doc = (doc
           .replace("__BOXES__", "[\n" + ",\n".join(
               '    ("%s", %g, %g, %g, %g, %g, %g, "%s")' % b for b in B) + ",\n]")
           .replace("__STREETS__", "[\n" + ",\n".join(
               '    (%r, %g, "%s")' % st for st in streets) + ",\n]")
           .replace("__AERIAL__", repr(AER))
           .replace("__MATDEF__", "{\n" + ",\n".join(
               '    "%s": (%r, %g, %g)' % (k, v[0], v[1], v[2]) for k, v in MP.items()) + ",\n}")
           .replace("CAMERAS = [", "CAMERAS = [   # «%s»\n" % kind + "    " * 0, 1))
    # جایگزینیِ دوربین‌ها
    i0 = doc.index("CAMERAS = [")
    i1 = doc.index("]", doc.index("\n", i0)) + 1
    doc = doc[:i0] + "CAMERAS = [\n" + ",\n".join(
        '    ("%s", %r, %r, %g)' % c for c in cams) + ",\n]" + doc[i1:]
    open(os.path.join(outdir, "build_scene.py"), "w", encoding="utf-8").write(doc)
    shutil.copy(os.path.join(HERE, "geo", "aerial_z19.jpg"),
                os.path.join(outdir, "aerial_z19.jpg"))
    zs = [b[5] for b in B]
    print(f"  {os.path.basename(outdir)}: {len(B)} جعبه · بلندی {max(zs):.2f} m")
    return B


if __name__ == "__main__":
    print("تولیدِ اسکریپتِ بلندر:")
    emit('pilotis', os.path.join(HERE, "blender-طرح-دوم"),
         [("نما-خیابان", (46.0, -26.0, 1.70), (18.0, 8.0, 6.0), 26),
          ("نما-سه-رخ", (-12.0, -18.0, 1.70), (18.0, 7.0, 5.0), 28),
          ("نما-هوایی", (72.0, -58.0, 38.0), (20.0, 14.0, 8.0), 28)])
    emit('shops', os.path.join(HERE, "blender-طرح-اول"),
         [("نما-خیابان", (46.0, -26.0, 1.70), (18.0, 8.0, 7.0), 26),
          ("نما-سه-رخ", (-12.0, -18.0, 1.70), (18.0, 7.0, 6.0), 28),
          ("نما-هوایی", (72.0, -58.0, 40.0), (20.0, 14.0, 9.0), 28)])
