#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""تولیدِ اسکریپتِ یک‌کلیکِ بلندر با داده‌هایِ توکار.
خروجی: docs/arch/blender/{build_scene.py, aerial_z19.jpg, راهنما-بلندر.md}
"""
import os, json, math, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import plan_model as PM
import export_model as EM

HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT = os.path.join(HERE, "docs", "arch", "blender")
os.makedirs(OUT, exist_ok=True)

# ---------------------------------------------------------------- داده‌ها
EM.build()
BOXES = [(b[0],) + tuple(round(float(v), 3) for v in b[1:7]) + (b[7],) for b in EM.BOXES]

ov = json.load(open(os.path.join(HERE, "docs", "arch", "geo", "overpass.json")))
LAT0, LON0 = 32.6305401, 51.7238816
MLAT = 110734.0
MLON = 111320.0 * math.cos(math.radians(32.63))
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
print(f"داده: {len(BOXES)} جعبه · {len(streets)} رهگذر")

AER = dict(w=1280, h=1792, mx=0.2515, my=0.2498, px=604.75, py=839.35, cx=20.285, cy=6.685)

MATS = {
    "facade":    "نمای اصلی — تراورتن/سیمان سفید",
    "core":      "هسته",
    "concrete":  "بتنِ اکسپوز",
    "slab":      "سقف",
    "balcony":   "کفِ ایوان",
    "railing":   "نرده (شیشه/فلز)",
    "shopfront": "ویترینِ مغازه",
    "roof":      "بام",
    "parapet":   "جان‌پناه",
    "terrace":   "تراس",
    "site":      "زمین",
    "sign":      "تابلو",
}
MP = {  # (رنگ RGB خطی, زبری, فلزی)
    "facade":    ((0.78, 0.735, 0.665), 0.62, 0.0),
    "core":      ((0.70, 0.67, 0.63), 0.70, 0.0),
    "concrete":  ((0.58, 0.57, 0.55), 0.78, 0.0),
    "slab":      ((0.62, 0.61, 0.59), 0.80, 0.0),
    "balcony":   ((0.60, 0.55, 0.48), 0.70, 0.0),
    "railing":   ((0.18, 0.22, 0.26), 0.18, 0.75),
    "shopfront": ((0.10, 0.13, 0.17), 0.06, 0.10),
    "roof":      ((0.50, 0.49, 0.47), 0.85, 0.0),
    "parapet":   ((0.68, 0.66, 0.63), 0.70, 0.0),
    "terrace":   ((0.26, 0.38, 0.18), 0.90, 0.0),
    "site":      ((0.52, 0.48, 0.43), 0.95, 0.0),
    "sign":      ((0.85, 0.83, 0.80), 0.55, 0.0),
}

TEMPLATE = r'''# -*- coding: utf-8 -*-
"""
ساختِ خودکارِ صحنهٔ سه‌بعدی در بلندر — زمین ۵۴۲٫۳۸ m²، اصفهان
==================================================================
این فایل همه‌چیز را خودکار می‌سازد: حجمِ ساختمان، زمین با بافتِ ماهواره‌ایِ واقعی،
شبکهٔ معابر، ساختمان‌های همسایه، خورشیدِ واقعیِ اصفهان، درخت و ماشین و تیرِ چراغ،
سه دوربین، و تنظیماتِ رندرِ بهینه برای کارت‌های ضعیف (مانند GTX 1650).

دو روشِ اجرا
------------
۱) محیطِ گرافیکی: بلندر را باز کنید → زبانهٔ Scripting → Open → این فایل → Run Script
   (صحنه ساخته می‌شود و می‌توانید همان‌جا آن را تماشا و ویرایش کنید)

۲) خطِ فرمان (رندرِ مستقیم، بدون باز کردنِ بلندر):
   بلندر را در این دستور جایگزین کنید:
     blender --background --python build_scene.py -- --render
   گزینه‌ها:
     --samples 160        تعداد نمونه (هرچه بیشتر، تمیزتر و کندتر)
     --res 1600x1000      ابعادِ خروجی
     --device auto|cpu|cuda|optix
     --hour 9.0           ساعتِ خورشید (محلیِ ایران)
     --month 9 --day 17   تاریخِ خورشید
     --out ../renders     پوشهٔ خروجی
     --save               ذخیرهٔ فایلِ .blend برای ویرایشِ بعدی

نکته: این اسکریپت برای بلندر ۴٫x نوشته شده و در ۵٫x هم باید کار کند.
"""
import bpy, math, os, sys, random
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
SAT_IMAGE = os.path.join(HERE, "aerial_z19.jpg")

# ============================================================ داده‌هایِ پروژه (خودکار تولید شده)
BOXES = __BOXES__
STREETS = __STREETS__
AERIAL = __AERIAL__
MAT_DEF = __MATDEF__

# ============================================================ پارامترها
LAT, LON = 32.6307, 51.7238
MONTH, DAY, HOUR = 9, 17, 9.0
RES_X, RES_Y = 1600, 1000
SAMPLES = 160
DEVICE = "auto"
EXPOSURE = 0.0

# دوربین‌ها: (نام, مکان, هدف, فاصلهٔ کانونی mm)
CAMERAS = [
    ("نما-خیابان-جنوبی", (44.0, -27.0, 1.70), (9.0, 7.5, 13.0), 26),
    ("نما-سه-رخ",        (-9.0, -19.0, 1.70), (11.0, 7.0, 9.0), 28),
    ("نما-هوایی",        (78.0, -62.0, 44.0), (20.0, 16.0, 14.0), 28),
]


# ============================================================ ابزارها
def clear_scene():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    sc.unit_settings.system = 'METRIC'
    sc.unit_settings.length_unit = 'METERS'
    return sc


def make_materials():
    """ساختِ مصالحِ استاندارد با گرهٔ Principled BSDF"""
    out = {}
    for key, (col, rough, metal) in MAT_DEF.items():
        m = bpy.data.materials.new(key)
        m.use_nodes = True
        bsdf = m.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs['Base Color'].default_value = (col[0], col[1], col[2], 1.0)
            bsdf.inputs['Roughness'].default_value = rough
            bsdf.inputs['Metallic'].default_value = metal
        out[key] = m
    return out


def add_box(name, x0, y0, z0, x1, y1, z1, material, collection=None):
    verts = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
             (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
    faces = [(0, 1, 2, 3), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5),
             (2, 3, 7, 6), (3, 0, 4, 7)]
    mesh = bpy.data.meshes.new(name)
    mesh.from_pydata(verts, [], faces)
    mesh.update()
    obj = bpy.data.objects.new(name, mesh)
    if material is not None:
        obj.data.materials.append(material)
    (collection or bpy.context.scene.collection).objects.link(obj)
    return obj


def sat_ground():
    """زمین با بافتِ ماهواره‌ایِ ژئورفرنس"""
    w = AERIAL['w'] * AERIAL['mx']
    h = AERIAL['h'] * AERIAL['my']
    verts = [(-w / 2, -h / 2, 0.0), (w / 2, -h / 2, 0.0), (w / 2, h / 2, 0.0), (-w / 2, h / 2, 0.0)]
    mesh = bpy.data.meshes.new("SAT_GROUND")
    mesh.from_pydata(verts, [], [(0, 1, 2, 3)])
    mesh.uv_layers.new(name="UVMap")
    uv = mesh.uv_layers['UVMap'].data
    for i, (u, v) in enumerate([(0, 0), (1, 0), (1, 1), (0, 1)]):
        uv[i].uv = (u, v)
    mesh.update()
    obj = bpy.data.objects.new("SAT_GROUND", mesh)
    obj.location = (AERIAL['cx'], AERIAL['cy'], -0.06)
    m = bpy.data.materials.new("SATELLITE")
    m.use_nodes = True
    nt = m.node_tree
    bsdf = nt.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs['Roughness'].default_value = 0.95
        bsdf.inputs['Metallic'].default_value = 0.0
        if os.path.exists(SAT_IMAGE):
            try:
                img = bpy.data.images.load(SAT_IMAGE)
                tex = nt.nodes.new("ShaderNodeTexImage")
                tex.image = img
                nt.links.new(tex.outputs['Color'], bsdf.inputs['Base Color'])
            except Exception as e:
                print("هشدار: بارگذاری تصویر ناموفق:", e)
        else:
            print("هشدار: aerial_z19.jpg پیدا نشد — زمین با رنگ ساده ساخته می‌شود")
    obj.data.materials.append(m)
    bpy.context.scene.collection.objects.link(obj)
    return obj


def sun_vector(month, day, hour, lat=LAT):
    """بردارِ خورشید برای تاریخ/ساعتِ محلیِ ایران"""
    N = (month - 1) * 30.4 + day
    decl = math.radians(23.45 * math.sin(math.radians(360.0 / 365.0 * (284 + N))))
    H = math.radians(15.0 * (hour - 12.0))
    phi = math.radians(lat)
    alt = math.asin(max(-1.0, min(1.0,
          math.sin(phi) * math.sin(decl) + math.cos(phi) * math.cos(decl) * math.cos(H))))
    ca = (math.sin(decl) - math.sin(alt) * math.sin(phi)) / (math.cos(alt) * math.cos(phi) + 1e-9)
    az = math.acos(max(-1.0, min(1.0, ca)))
    if H > 0:
        az = 2 * math.pi - az
    L = Vector((math.cos(alt) * math.sin(az), math.cos(alt) * math.cos(az), math.sin(alt)))
    return L, math.degrees(alt), math.degrees(az)


def setup_sky_and_sun(L):
    """آسمانِ نیشیتا + چراغِ خورشید"""
    world = bpy.data.worlds.new("SkyWorld")
    bpy.context.scene.world = world
    world.use_nodes = True
    nt = world.node_tree
    nt.nodes.clear()
    out = nt.nodes.new("ShaderNodeOutputWorld")
    bg = nt.nodes.new("ShaderNodeBackground")
    try:
        sky = nt.nodes.new("ShaderNodeTexSky")
        sky.sky_type = 'NISHITA'
        sky.sun_elevation = math.asin(max(-1.0, min(1.0, L.z)))
        sky.sun_rotation = math.atan2(L.y, L.x)
        sky.air_density = 1.0
        sky.dust_density = 0.55
        sky.ozone_density = 0.35
        nt.links.new(sky.outputs['Color'], bg.inputs['Color'])
    except Exception as e:
        print("هشدار: ساختِ آسمانِ نیشیتا ناموفق — پس‌زمینهٔ ساده:", e)
        bg.inputs['Color'].default_value = (0.30, 0.46, 0.80, 1.0)
    bg.inputs['Strength'].default_value = 1.0
    nt.links.new(bg.outputs['Background'], out.inputs['Surface'])

    d = bpy.data.lights.new("SUN", type='SUN')
    d.energy = 4.0
    try:
        d.angle = math.radians(0.545)
    except Exception:
        pass
    o = bpy.data.objects.new("SUN", d)
    bpy.context.scene.collection.objects.link(o)
    o.rotation_euler = Vector((-L.x, -L.y, -L.z)).to_track_quat('-Z', 'Y').to_euler()
    return o


def add_neighbors(collection):
    """ساختمان‌های همسایه — استنتاج از بافتِ واقعیِ معابر (تقریبی)"""
    rng = random.Random(7)
    mats = []
    for col, rough in [((0.74, 0.70, 0.64), 0.8), ((0.62, 0.58, 0.55), 0.85),
                       ((0.83, 0.79, 0.73), 0.8), ((0.55, 0.50, 0.46), 0.85)]:
        m = bpy.data.materials.new("NEIGHBOR_%d" % len(mats))
        m.use_nodes = True
        bsdf = m.node_tree.nodes.get("Principled BSDF")
        if bsdf:
            bsdf.inputs['Base Color'].default_value = (col[0], col[1], col[2], 1.0)
            bsdf.inputs['Roughness'].default_value = rough
        mats.append(m)
    n = 0
    for pts, w, hw in STREETS:
        if hw == "secondary":
            continue
        off = w / 2 + 2.5
        for side in (1, -1):
            for i in range(len(pts) - 1):
                (x0, y0), (x1, y1) = pts[i], pts[i + 1]
                dx, dy = x1 - x0, y1 - y0
                L = math.hypot(dx, dy)
                if L < 4:
                    continue
                nx, ny = -dy / L * off * side, dx / L * off * side
                t = 0.0
                while t < L - 3:
                    ln = min(rng.uniform(9, 20), L - t)
                    if ln < 6:
                        break
                    ax, ay = x0 + dx / L * t + nx, y0 + dy / L * t + ny
                    bx, by = x0 + dx / L * (t + ln) + nx, y0 + dy / L * (t + ln) + ny
                    dep = rng.uniform(8, 14)
                    px_, py_ = nx / off, ny / off
                    ex, ey = bx + px_ * dep, by + py_ * dep
                    fx, fy = ax + px_ * dep, ay + py_ * dep
                    hgt = rng.choice([4.5, 6.0, 7.5, 9.0, 10.5, 12.0])
                    ccx, ccy = (ax + bx + ex + fx) / 4, (ay + by + ey + fy) / 4
                    if not (-3 < ccx < 43.6 and -3 < ccy < 15.4):
                        add_box("NB_%d" % n,
                                min(ax, bx, ex, fx), min(ay, by, ey, fy), 0.0,
                                max(ax, bx, ex, fx), max(ay, by, ey, fy), hgt,
                                mats[n % len(mats)], collection)
                        n += 1
                    t += ln + rng.uniform(1.0, 3.0)
    return n


def add_roads_and_walks(collection):
    """روسازیِ معابر و پیاده‌روها"""
    m_asp = bpy.data.materials.new("ASPHALT")
    m_asp.use_nodes = True
    b1 = m_asp.node_tree.nodes.get("Principled BSDF")
    if b1:
        b1.inputs['Base Color'].default_value = (0.055, 0.055, 0.06, 1.0)
        b1.inputs['Roughness'].default_value = 0.72
    m_walk = bpy.data.materials.new("SIDEWALK")
    m_walk.use_nodes = True
    b2 = m_walk.node_tree.nodes.get("Principled BSDF")
    if b2:
        b2.inputs['Base Color'].default_value = (0.42, 0.41, 0.39, 1.0)
        b2.inputs['Roughness'].default_value = 0.85
    for pts, w, hw in STREETS:
        for i in range(len(pts) - 1):
            (x0, y0), (x1, y1) = pts[i], pts[i + 1]
            dx, dy = x1 - x0, y1 - y0
            L = math.hypot(dx, dy)
            if L < 1e-6:
                continue
            nx, ny = -dy / L * w / 2, dx / L * w / 2
            add_box("ROAD", x0 + nx, y0 + ny, 0.01, x1 - nx, y1 - ny, 0.03, m_asp, collection)
            for s in (1, -1):
                ox, oy = -dy / L * s * (w / 2 + 1.0), dx / L * s * (w / 2 + 1.0)
                add_box("WALK", x0 + ox, y0 + oy, 0.03, x1 + ox, y1 + oy, 0.18, m_walk, collection)


def add_entourage(collection):
    """درخت، خودرو، تیرِ چراغ‌برق و دکلِ برق"""
    m_trunk = bpy.data.materials.new("TRUNK")
    m_trunk.use_nodes = True
    t1 = m_trunk.node_tree.nodes.get("Principled BSDF")
    if t1:
        t1.inputs['Base Color'].default_value = (0.16, 0.12, 0.08, 1.0)
        t1.inputs['Roughness'].default_value = 0.9
    m_leaf = bpy.data.materials.new("LEAF")
    m_leaf.use_nodes = True
    t2 = m_leaf.node_tree.nodes.get("Principled BSDF")
    if t2:
        t2.inputs['Base Color'].default_value = (0.13, 0.26, 0.10, 1.0)
        t2.inputs['Roughness'].default_value = 0.95
    for (x, y) in [(2, 16.4), (8, 16.4), (14, 16.4), (20, 16.4), (26, 16.4), (32, 16.4),
                   (38, 16.4), (12, -1.2), (20, -1.2), (28, -1.2), (36, -1.2)]:
        add_box("TRUNK", x - 0.18, y - 0.18, 0.0, x + 0.18, y + 0.18, 3.0, m_trunk, collection)
        bpy.ops.mesh.primitive_ico_sphere_add(subdivisions=1, radius=1.9,
                                              location=(x, y, 4.6))
        o = bpy.context.active_object
        o.name = "FOLIAGE"
        o.scale = (1.0, 1.0, 1.25)
        o.data.materials.append(m_leaf)
        bpy.context.scene.collection.objects.unlink(o)
        collection.objects.link(o)
    car_cols = [(0.72, 0.73, 0.76), (0.14, 0.16, 0.22), (0.55, 0.18, 0.15), (0.28, 0.30, 0.36)]
    for i, (x, y) in enumerate([(3.0, 17.4), (6.0, 17.4), (9.0, 17.4), (15.0, 17.4),
                                (18.0, 17.4), (24.0, 17.4), (30.0, 17.4), (33.0, 17.4)]):
        c = car_cols[i % 4]
        m = bpy.data.materials.new("CAR_%d" % i)
        m.use_nodes = True
        bb = m.node_tree.nodes.get("Principled BSDF")
        if bb:
            bb.inputs['Base Color'].default_value = (c[0], c[1], c[2], 1.0)
            bb.inputs['Roughness'].default_value = 0.22
            bb.inputs['Metallic'].default_value = 0.85
        add_box("CAR_BODY", x, y, 0.18, x + 4.3, y + 1.75, 0.85, m, collection)
        add_box("CAR_CABIN", x + 0.7, y, 0.85, x + 3.4, y + 1.75, 1.45, m, collection)
    m_metal = bpy.data.materials.new("METAL")
    m_metal.use_nodes = True
    m3 = m_metal.node_tree.nodes.get("Principled BSDF")
    if m3:
        m3.inputs['Base Color'].default_value = (0.40, 0.41, 0.43, 1.0)
        m3.inputs['Roughness'].default_value = 0.45
        m3.inputs['Metallic'].default_value = 0.9
    for (x, y) in [(4, 16.0), (16, 16.0), (28, 16.0), (40, 16.0)]:
        add_box("LAMP", x - 0.12, y - 0.12, 0.0, x + 0.12, y + 0.12, 8.5, m_metal, collection)
        add_box("LAMP_ARM", x - 0.9, y - 0.14, 8.3, x + 0.9, y + 0.14, 8.6, m_metal, collection)
    for tx in (10.0, 34.0):
        ty = -3.6
        add_box("TOWER_BASE", tx - 0.45, ty - 0.45, 0.0, tx + 0.45, ty + 0.45, 2.0, m_metal, collection)
        add_box("TOWER_MAST", tx - 0.16, ty - 0.16, 2.0, tx + 0.16, ty + 0.16, 17.0, m_metal, collection)
        add_box("TOWER_ARM1", tx - 3.2, ty - 0.12, 15.4, tx + 3.2, ty + 0.12, 15.7, m_metal, collection)
        add_box("TOWER_ARM2", tx - 2.4, ty - 0.12, 13.2, tx + 2.4, ty + 0.12, 13.5, m_metal, collection)
    add_box("WIRE_A", 9.0, -3.7, 15.55, 35.0, -3.5, 15.61, m_metal, collection)
    add_box("WIRE_B", 9.0, -3.7, 13.35, 35.0, -3.5, 13.41, m_metal, collection)


def add_cameras():
    cams = []
    for name, loc, tgt, lens in CAMERAS:
        c = bpy.data.cameras.new(name)
        c.lens = lens
        c.clip_start = 0.1
        c.clip_end = 900.0
        o = bpy.data.objects.new(name, c)
        bpy.context.scene.collection.objects.link(o)
        o.location = loc
        d = Vector((tgt[0] - loc[0], tgt[1] - loc[1], tgt[2] - loc[2]))
        o.rotation_euler = d.to_track_quat('-Z', 'Y').to_euler()
        cams.append(o)
    return cams


def configure(device=DEVICE, samples=SAMPLES, resx=RES_X, resy=RES_Y, exposure=EXPOSURE):
    sc = bpy.context.scene
    sc.render.engine = 'CYCLES'
    sc.cycles.samples = samples
    sc.cycles.max_bounces = 8
    sc.cycles.diffuse_bounces = 3
    sc.cycles.glossy_bounces = 3
    sc.cycles.transmission_bounces = 6
    sc.cycles.use_adaptive_sampling = True
    sc.cycles.adaptive_threshold = 0.012
    sc.cycles.use_denoising = True
    try:
        sc.cycles.denoiser = 'OPENIMAGEDENOISE'      # روی CPU اجرا می‌شود — برای هر کارتی
    except Exception:
        pass
    sc.render.resolution_x, sc.render.resolution_y = resx, resy
    sc.render.resolution_percentage = 100
    for vt in ('AgX', 'Filmic'):
        try:
            sc.view_settings.view_transform = vt
            break
        except Exception:
            continue
    sc.view_settings.exposure = exposure
    sc.view_settings.look = 'Medium High Contrast' if 'Medium High Contrast' in \
        [x.identifier for x in type(sc.view_settings).bl_rna.properties['look'].enum_items] \
        else sc.view_settings.look
    used = 'CPU'
    if device in ('auto', 'cuda', 'optix'):
        try:
            prefs = bpy.context.preferences.addons['cycles'].preferences
            prefs.compute_device_type = 'OPTIX' if device == 'optix' else 'CUDA'
            prefs.get_devices()
            gpus = [d for d in prefs.devices if d.type in ('CUDA', 'OPTIX')]
            if gpus:
                for d in prefs.devices:
                    d.use = (d in gpus)
                sc.cycles.device = 'GPU'
                used = 'GPU (%s)' % prefs.compute_device_type
            else:
                sc.cycles.device = 'CPU'
        except Exception as e:
            print("هشدار: فعال‌سازیِ GPU ناموفق — رندر روی CPU:", e)
            sc.cycles.device = 'CPU'
    else:
        sc.cycles.device = 'CPU'
    return used


def build(args):
    sc = clear_scene()
    mats = make_materials()
    print("  زمین با بافتِ ماهواره‌ای …")
    sat_ground()
    coll_n = bpy.data.collections.new("ساختمان")
    bpy.context.scene.collection.children.link(coll_n)
    print("  حجمِ ساختمان …")
    for (name, x0, y0, z0, x1, y1, z1, mk) in BOXES:
        add_box(name, x0, y0, z0, x1, y1, z1, mats.get(mk), coll_n)
    coll_c = bpy.data.collections.new("زمینه")
    bpy.context.scene.collection.children.link(coll_c)
    print("  معابر و همسایه‌ها …")
    add_roads_and_walks(coll_c)
    nb = add_neighbors(coll_c)
    print("  درخت، خودرو و دکل …")
    add_entourage(coll_c)
    L, alt, az = sun_vector(args['month'], args['day'], args['hour'])
    print("  خورشید %s/%s ساعت %s → ارتفاع %.1f° آزیموت %.1f°" %
          (args['month'], args['day'], args['hour'], alt, az))
    setup_sky_and_sun(L)
    cams = add_cameras()
    used = configure(args['device'], args['samples'], args['resx'], args['resy'], args['exposure'])
    print("  دستگاهِ رندر:", used)
    sc.camera = cams[0]
    print("  صحنه آماده: %d شیء · %d بنای همسایه" % (len(bpy.data.objects), nb))
    return sc, cams, used


def main():
    argv = sys.argv
    if '--' in argv:
        argv = argv[argv.index('--') + 1:]
    else:
        argv = []
    a = {'samples': SAMPLES, 'resx': RES_X, 'resy': RES_Y, 'device': DEVICE,
         'hour': HOUR, 'month': MONTH, 'day': DAY, 'exposure': EXPOSURE,
         'out': os.path.join(HERE, 'renders'), 'render': False, 'save': False}
    i = 0
    while i < len(argv):
        k = argv[i]
        if k == '--samples' and i + 1 < len(argv): a['samples'] = int(argv[i + 1]); i += 2
        elif k == '--res' and i + 1 < len(argv):
            a['resx'], a['resy'] = [int(x) for x in argv[i + 1].split('x')]; i += 2
        elif k == '--device' and i + 1 < len(argv): a['device'] = argv[i + 1]; i += 2
        elif k == '--hour' and i + 1 < len(argv): a['hour'] = float(argv[i + 1]); i += 2
        elif k == '--month' and i + 1 < len(argv): a['month'] = int(argv[i + 1]); i += 2
        elif k == '--day' and i + 1 < len(argv): a['day'] = int(argv[i + 1]); i += 2
        elif k == '--exposure' and i + 1 < len(argv): a['exposure'] = float(argv[i + 1]); i += 2
        elif k == '--out' and i + 1 < len(argv): a['out'] = argv[i + 1]; i += 2
        elif k == '--render': a['render'] = True; i += 1
        elif k == '--save': a['save'] = True; i += 1
        else: i += 1

    print("=== ساختِ صحنه ===")
    sc, cams, used = build(a)
    os.makedirs(a['out'], exist_ok=True)
    blend = os.path.join(HERE, 'scene.blend')
    try:
        bpy.ops.wm.save_as_mainfile(filepath=blend)
        print("فایلِ بلندر ذخیره شد:", blend)
    except Exception as e:
        print("ذخیرهٔ .blend ناموفق:", e)
    if a['render']:
        print("=== رندر ===")
        for i, cam in enumerate(cams):
            sc.camera = cam
            p = os.path.join(a['out'], "%02d_%s.png" % (i + 1, cam.name))
            sc.render.filepath = p
            bpy.ops.render.render(write_still=True)
            print("  ذخیره:", p)
    print("پایان. اکنون می‌توانید scene.blend را در بلندر باز کنید.")


if __name__ == "__main__":
    main()
'''

script = (TEMPLATE
          .replace("__BOXES__", "[\n" + ",\n".join(
              '    ("%s", %g, %g, %g, %g, %g, %g, "%s")' % b for b in BOXES) + ",\n]")
          .replace("__STREETS__", "[\n" + ",\n".join(
              '    (%r, %g, "%s")' % (pts, w, hw) for (pts, w, hw) in streets) + ",\n]")
          .replace("__AERIAL__", repr(AER))
          .replace("__MATDEF__", "{\n" + ",\n".join(
              '    "%s": (%r, %g, %g)' % (k, v[0], v[1], v[2]) for k, v in MP.items()) + ",\n}"))
open(os.path.join(OUT, "build_scene.py"), "w", encoding="utf-8").write(script)

import shutil
shutil.copy(os.path.join(HERE, "docs", "arch", "geo", "aerial_z19.jpg"),
            os.path.join(OUT, "aerial_z19.jpg"))

guide = """# راهنمایِ ساختِ رندرِ حرفه‌ای با کارتِ GTX 1650

## چرا بلندر
کارتِ شما (GTX 1650، ۴ گیگابایت، معماریِ Turing، **بدون هستهٔ RTX**):

| برنامه | وضعیت رویِ کارتِ شما |
|---|---|
| **D5 Render** | ✗ فقط کارت‌های NVIDIA RTX را پشتیبانی می‌کند |
| **Twinmotion** | ✗ حداقل ۶ گیگابایت حافظهٔ گرافیکی می‌خواهد (شما ۴ دارید) |
| **Enscape / Lumion** | ✗ همان محدودیت |
| **Blender** | ✓ **CUDA روی همین کارت کار می‌کند** و در بدترین حالت روی CPU رندر می‌گیرد |

پس بلندر تنها گزینهٔ جدیِ شماست — و خوشبختانه کم‌رقیب‌ترین هم هست.

## نصب
1. بلندر را از `blender.org` دانلود و نصب کنید (نسخهٔ ۴٫۲ LTS پیشنهاد می‌شود؛ رایگان و متن‌باز)
2. این پوشه را یک‌جا کپی کنید (فایلِ `build_scene.py` باید کنارِ `aerial_z19.jpg` بماند)

## اجرا — دو روش

**روشِ ۱ (پیشنهادی، ساده‌ترین):** بلندر را باز کنید → زبانهٔ **Scripting** → **Open** → فایلِ
`build_scene.py` → **Run Script**. صحنه کامل ساخته می‌شود و همان‌جا می‌بینیدش و می‌توانید
تغییرش دهید. فایلِ `scene.blend` هم کنارش ذخیره می‌شود.

**روشِ ۲ (رندرِ مستقیم از خطِ فرمان):**
```
blender --background --python build_scene.py -- --render --samples 160 --res 1600x1000
```

گزینه‌ها: `--samples` (تعداد نمونه) · `--res` (ابعاد) · `--device auto|cpu|cuda|optix`
· `--hour` (ساعتِ خورشید) · `--out` (پوشهٔ خروجی) · `--save`

## تنظیماتِ پیشنهادی برای کارتِ شما
شروع کنید با این و اگر روان بود بالاتر ببرید:
```
--samples 128 --res 1280x800
```
و بعد:
```
--samples 256 --res 1920x1200
```
**کلیدِ ماجرا «کم‌نمونه + حذفِ نویز» است:** نمونهٔ کم تصویر را دانه‌دانه می‌کند،
و حذف‌کنندهٔ نویزِ OpenImageDenoise (که روی CPU کار می‌کند و به کارتِ گرافیک ربطی ندارد)
آن را تمیز می‌کند. با ۱۲۸ نمونه + حذفِ نویز، تصویری می‌گیرید که قبلاً به ۱۰۰۰ نمونه نیاز داشت.

اگر در حینِ رندر پیغامِ کمبودِ حافظهٔ گرافیکی آمد، یکی از این‌ها را امتحان کنید:
`--device cpu` · یا `--res 1280x800` · یا مصالح را ساده کنید.

## برای اینکه رندر «حرفه‌ای» شود (به ترتیبِ اهمیت)
۱. **عناصرِ انسانی:** آدم، ماشین، درخت، چراغ · بیشترین تفاوتِ رندرِ آماتور و حرفه‌ای همین است
۲. **مصالح:** زبری و مقیاسِ واقعیِ بافت (گیاهان و دیوارها را با بافت بپوشانید)
۳. **زمانِ خورشید:** ساعت ۱۶ تا ۱۸ (نورِ گرم و سایه‌های بلند) یا ۸ تا ۱۰ صبح
۴. **دوربین:** چشمِ انسان در ۱٫۶۵ تا ۱٫۷۰ متر، لنزِ ۲۴ تا ۳۵ میلی‌متر
۵. **پس‌پردازش:** در زبانهٔ Compositing، کمی کنتراست و تیزی و گردگرفتگی

## سایت‌هایِ رایگان برای مصالح و دارایی
- **polyhaven.com** — بافت، HDRI و مدل با مجوزِ CC0 (کاملاً رایگان، حتی تجاری)
- **ambientCG.com** — بافتِ رایگان
- برای درخت و آدمِ آماده: **BlenderKit** (افزونه، نسخهٔ رایگان دارد)

## شرافتِ روش
این اسکریپت در محیطی نوشته شده که بلندر در آن اجرا نمی‌شود، بنابراین **اجرایش را تست نکرده‌ام**.
اگر خطا داد، متنِ خطا را برایم بفرستید تا همان لحظه درستش کنم. ساختارش ساده و خط‌به‌خط
خوانا است و هر بخشی را می‌توانید جداگانه خاموش کنید.
"""
open(os.path.join(OUT, "راهنما-بلندر.md"), "w", encoding="utf-8").write(guide)
print("تولید شد:", os.listdir(OUT))
print("اندازهٔ اسکریپت:", round(os.path.getsize(os.path.join(OUT, "build_scene.py")) / 1024, 1), "KB")
