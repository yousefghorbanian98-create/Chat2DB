#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""خروجیِ OBJ و DXF برایِ هر دو طرح."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ezdxf
import make_blender_schemes as M
import plan_schemes as PS

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT1 = os.path.join(HERE, "مدل-سه‌بعدی-طرح-اول")
OUT2 = os.path.join(HERE, "مدل-سه‌بعدی-طرح-دوم")
for d in (OUT1, OUT2):
    os.makedirs(d, exist_ok=True)

MTR = {k: (v[0], v[1], v[2]) for k, v in M.MP.items()}


def write_obj(boxes, path, name):
    verts, faces = [], []
    for (nm, x0, y0, z0, x1, y1, z1, mat) in boxes:
        b = len(verts)
        verts += [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
                  (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
        for q in [(1, 2, 6, 5), (2, 3, 7, 6), (3, 4, 8, 7), (4, 1, 5, 8),
                  (5, 6, 7, 8), (4, 3, 2, 1)]:
            a, c, d, e = [b + i - 1 for i in q]
            faces.append((nm, mat, (a, c, d), (a, d, e)))
    with open(path, "w", encoding="utf-8") as f:
        f.write(f"# {name}\n# یکا: متر · Z رو به بالا · مبدأ: گوشهٔ جنوب‌غربیِ زمین\n")
        f.write("mtllib model.mtl\n")
        for v in verts:
            f.write("v %.4f %.4f %.4f\n" % v)
        cur = None
        for (grp, mat, t1, t2) in faces:
            if grp != cur:
                f.write(f"g {grp}\nusemtl {mat}\n")
                cur = grp
            f.write("f %d %d %d\n" % tuple(i + 1 for i in t1))
            f.write("f %d %d %d\n" % tuple(i + 1 for i in t2))
    with open(path.replace(".obj", ".mtl"), "w", encoding="utf-8") as f:
        for k, (col, rough, metal) in M.MP.items():
            f.write(f"newmtl {k}\nKd {col[0]:.3f} {col[1]:.3f} {col[2]:.3f}\n"
                    f"Ks 0.05 0.05 0.05\nNs {max(2.0, (1.0 - rough) * 200):.0f}\n"
                    f"d 1.0\nillum 2\n\n")
    return len(verts), len(faces)


def write_dxf(kind, path, name):
    doc = ezdxf.new("R2010")
    doc.header["$INSUNITS"] = 6            # متر
    msp = doc.modelspace()
    layers = ["زمین", "دیوار", "هسته", "ایوان", "نرده", "سقف", "بام",
              "پارکینگ", "مغازه", "بعد", "متن"]
    for L in layers:
        if L not in doc.layers:
            doc.layers.add(L)

    def rect(x0, y0, x1, y1, layer):
        msp.add_lwpolyline([(x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0)],
                           dxfattribs={"layer": layer})

    rect(0, 0, PS.LAND_W, PS.LAND_D, "زمین")
    rect(0, PS.Y0, PS.BLD_W, PS.Y1, "دیوار")
    for c in PS.cores():
        rect(c['x0'], c['y0'], c['x1'], c['y1'], "هسته")
    cr = PS.corridor()
    rect(cr['x0'], cr['y0'], cr['x1'], cr['y1'], "سقف")
    if kind == 'pilotis':
        for r in PS.parking_rows():
            rect(r['x0'], r['y0'], r['x1'], r['y1'], "پارکینگ")
    else:
        for s in PS.shops(4):
            rect(s['x0'], s['y0'], s['x1'], s['y1'], "مغازه")
    for u in PS.unit_boxes():
        rect(u['x0'], u['y0'], u['x1'], u['y1'], "دیوار")
        rect(u['x0'], u['by0'], u['x1'], u['by1'], "ایوان")
    # ابعاد
    msp.add_linear_dim(base=(0, PS.Y0 - 2.2),
                       p1=(0, PS.Y0), p2=(PS.BLD_W, PS.Y0),
                       dxfattribs={"layer": "بعد"}).render()
    msp.add_linear_dim(base=(PS.LAND_W + 1.5, 0),
                       p1=(0, 0), p2=(0, PS.LAND_D), angle=90,
                       dxfattribs={"layer": "بعد"}).render()
    doc.saveas(path)
    return len(msp)


for kind, out, nm in (("pilotis", OUT2, "طرح دوم — تماماً مسکونی"),
                      ("shops", OUT1, "طرح اول — مغازه + ۳ طبقه")):
    B = M.boxes(kind)
    v, f = write_obj(B, os.path.join(out, "model.obj"), nm)
    n = write_dxf(kind, os.path.join(out, "final-plan.dxf"), nm)
    s = PS.summary('shops' if kind == 'shops' else 'pilotis', nshop=(4 if kind == 'shops' else 0))
    open(os.path.join(out, "خلاصه.txt"), "w", encoding="utf-8").write(
        f"{nm}\nزمین: {PS.LAND_W:.2f} × {PS.LAND_D:.2f} = {PS.LAND:.2f} m²\n"
        f"زیربنای هر طبقه: {s['cnt_per_floor']:.1f} m² (مشمولِ تراکم)\n"
        f"تراکم: {s['far']:.1f}٪ · مازاد بر ۱۸۰٪: {s['exc180']:.0f} m²\n"
        f"واحدها: {s['units']} واحد · هر واحد {s['unit_area']:.1f} m² بسته + ایوان\n"
        f"ارتفاع: {s['height']:.2f} m · پارکینگِ موجود: {s['park_have']} فضا\n")
    print(f"  {os.path.basename(out)}: {v} رأس / {f} وجه / {n} موجودیتِ DXF")
