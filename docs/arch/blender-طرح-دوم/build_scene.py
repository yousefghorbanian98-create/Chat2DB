# -*- coding: utf-8 -*-
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
BOXES = [
    ("SITE_PLOT", 0, 0, -0.05, 40.57, 13.37, 0, "site"),
    ("BASE_SLAB", 0, 2.67, -0.3, 40.555, 13.37, 0, "concrete"),
    ("BASE_CORE", 0, 8.27, 0, 4.2, 13.37, 2.6, "core"),
    ("PARK_LINE", 0.6, 3.27, 0.02, 3.1, 8.27, 0.05, "parking"),
    ("PARK_LINE", 3.25, 3.27, 0.02, 5.75, 8.27, 0.05, "parking"),
    ("PARK_LINE", 5.9, 3.27, 0.02, 8.4, 8.27, 0.05, "parking"),
    ("PARK_LINE", 8.55, 3.27, 0.02, 11.05, 8.27, 0.05, "parking"),
    ("PARK_LINE", 11.2, 3.27, 0.02, 13.7, 8.27, 0.05, "parking"),
    ("PARK_LINE", 13.85, 3.27, 0.02, 16.35, 8.27, 0.05, "parking"),
    ("PARK_LINE", 16.5, 3.27, 0.02, 19, 8.27, 0.05, "parking"),
    ("PARK_LINE", 19.15, 3.27, 0.02, 21.65, 8.27, 0.05, "parking"),
    ("PARK_LINE", 21.8, 3.27, 0.02, 24.3, 8.27, 0.05, "parking"),
    ("PARK_LINE", 24.45, 3.27, 0.02, 26.95, 8.27, 0.05, "parking"),
    ("PARK_LINE", 27.1, 3.27, 0.02, 29.6, 8.27, 0.05, "parking"),
    ("PARK_LINE", 29.75, 3.27, 0.02, 32.25, 8.27, 0.05, "parking"),
    ("PARK_LINE", 32.4, 3.27, 0.02, 34.9, 8.27, 0.05, "parking"),
    ("PILOTIS_COL", 1.8, 9.97, 0, 2.2, 10.37, 2.6, "concrete"),
    ("PILOTIS_COL", 9.111, 9.97, 0, 9.511, 10.37, 2.6, "concrete"),
    ("PILOTIS_COL", 16.422, 9.97, 0, 16.822, 10.37, 2.6, "concrete"),
    ("PILOTIS_COL", 23.733, 9.97, 0, 24.133, 10.37, 2.6, "concrete"),
    ("PILOTIS_COL", 31.044, 9.97, 0, 31.444, 10.37, 2.6, "concrete"),
    ("PILOTIS_COL", 38.355, 9.97, 0, 38.755, 10.37, 2.6, "concrete"),
    ("F1_SLAB", 0, 2.67, 2.3, 40.555, 13.37, 2.6, "slab"),
    ("F1_WALL_W", 0, 2.67, 2.6, 0.3, 13.37, 5.5, "facade"),
    ("F1_WALL_E", 40.255, 2.67, 2.6, 40.555, 13.37, 5.5, "facade"),
    ("F1_WALL_S", 0, 4.87, 2.6, 40.555, 5.12, 5.5, "facade"),
    ("F1_WALL_N", 0, 13.07, 2.6, 40.555, 13.37, 5.5, "facade"),
    ("F1_CORE", 0, 8.27, 2.6, 4.2, 13.37, 5.5, "core"),
    ("F1_PARTY", 4.1, 4.87, 2.6, 4.3, 12.07, 5.5, "concrete"),
    ("F1_BALC", 4.2, 2.67, 2.6, 13.289, 4.87, 2.72, "balcony"),
    ("F1_RAIL", 4.2, 2.67, 2.6, 13.289, 2.79, 3.7, "railing"),
    ("F1_RAIL_S", 4.2, 2.67, 2.6, 4.32, 4.87, 3.7, "railing"),
    ("F1_RAIL_E", 13.169, 2.67, 2.6, 13.289, 4.87, 3.7, "railing"),
    ("F1_PARTY", 13.189, 4.87, 2.6, 13.389, 12.07, 5.5, "concrete"),
    ("F1_BALC", 13.289, 2.67, 2.6, 22.377, 4.87, 2.72, "balcony"),
    ("F1_RAIL", 13.289, 2.67, 2.6, 22.377, 2.79, 3.7, "railing"),
    ("F1_RAIL_S", 13.289, 2.67, 2.6, 13.409, 4.87, 3.7, "railing"),
    ("F1_RAIL_E", 22.257, 2.67, 2.6, 22.377, 4.87, 3.7, "railing"),
    ("F1_PARTY", 22.277, 4.87, 2.6, 22.477, 12.07, 5.5, "concrete"),
    ("F1_BALC", 22.377, 2.67, 2.6, 31.466, 4.87, 2.72, "balcony"),
    ("F1_RAIL", 22.377, 2.67, 2.6, 31.466, 2.79, 3.7, "railing"),
    ("F1_RAIL_S", 22.377, 2.67, 2.6, 22.497, 4.87, 3.7, "railing"),
    ("F1_RAIL_E", 31.346, 2.67, 2.6, 31.466, 4.87, 3.7, "railing"),
    ("F1_PARTY", 31.366, 4.87, 2.6, 31.566, 12.07, 5.5, "concrete"),
    ("F1_BALC", 31.466, 2.67, 2.6, 40.555, 4.87, 2.72, "balcony"),
    ("F1_RAIL", 31.466, 2.67, 2.6, 40.555, 2.79, 3.7, "railing"),
    ("F1_RAIL_S", 31.466, 2.67, 2.6, 31.586, 4.87, 3.7, "railing"),
    ("F1_RAIL_E", 40.435, 2.67, 2.6, 40.555, 4.87, 3.7, "railing"),
    ("F2_SLAB", 0, 2.67, 5.2, 40.555, 13.37, 5.5, "slab"),
    ("F2_WALL_W", 0, 2.67, 5.5, 0.3, 13.37, 8.4, "facade"),
    ("F2_WALL_E", 40.255, 2.67, 5.5, 40.555, 13.37, 8.4, "facade"),
    ("F2_WALL_S", 0, 4.87, 5.5, 40.555, 5.12, 8.4, "facade"),
    ("F2_WALL_N", 0, 13.07, 5.5, 40.555, 13.37, 8.4, "facade"),
    ("F2_CORE", 0, 8.27, 5.5, 4.2, 13.37, 8.4, "core"),
    ("F2_PARTY", 4.1, 4.87, 5.5, 4.3, 12.07, 8.4, "concrete"),
    ("F2_BALC", 4.2, 2.67, 5.5, 13.289, 4.87, 5.62, "balcony"),
    ("F2_RAIL", 4.2, 2.67, 5.5, 13.289, 2.79, 6.6, "railing"),
    ("F2_RAIL_S", 4.2, 2.67, 5.5, 4.32, 4.87, 6.6, "railing"),
    ("F2_RAIL_E", 13.169, 2.67, 5.5, 13.289, 4.87, 6.6, "railing"),
    ("F2_PARTY", 13.189, 4.87, 5.5, 13.389, 12.07, 8.4, "concrete"),
    ("F2_BALC", 13.289, 2.67, 5.5, 22.377, 4.87, 5.62, "balcony"),
    ("F2_RAIL", 13.289, 2.67, 5.5, 22.377, 2.79, 6.6, "railing"),
    ("F2_RAIL_S", 13.289, 2.67, 5.5, 13.409, 4.87, 6.6, "railing"),
    ("F2_RAIL_E", 22.257, 2.67, 5.5, 22.377, 4.87, 6.6, "railing"),
    ("F2_PARTY", 22.277, 4.87, 5.5, 22.477, 12.07, 8.4, "concrete"),
    ("F2_BALC", 22.377, 2.67, 5.5, 31.466, 4.87, 5.62, "balcony"),
    ("F2_RAIL", 22.377, 2.67, 5.5, 31.466, 2.79, 6.6, "railing"),
    ("F2_RAIL_S", 22.377, 2.67, 5.5, 22.497, 4.87, 6.6, "railing"),
    ("F2_RAIL_E", 31.346, 2.67, 5.5, 31.466, 4.87, 6.6, "railing"),
    ("F2_PARTY", 31.366, 4.87, 5.5, 31.566, 12.07, 8.4, "concrete"),
    ("F2_BALC", 31.466, 2.67, 5.5, 40.555, 4.87, 5.62, "balcony"),
    ("F2_RAIL", 31.466, 2.67, 5.5, 40.555, 2.79, 6.6, "railing"),
    ("F2_RAIL_S", 31.466, 2.67, 5.5, 31.586, 4.87, 6.6, "railing"),
    ("F2_RAIL_E", 40.435, 2.67, 5.5, 40.555, 4.87, 6.6, "railing"),
    ("F3_SLAB", 0, 2.67, 8.1, 40.555, 13.37, 8.4, "slab"),
    ("F3_WALL_W", 0, 2.67, 8.4, 0.3, 13.37, 11.3, "facade"),
    ("F3_WALL_E", 40.255, 2.67, 8.4, 40.555, 13.37, 11.3, "facade"),
    ("F3_WALL_S", 0, 4.87, 8.4, 40.555, 5.12, 11.3, "facade"),
    ("F3_WALL_N", 0, 13.07, 8.4, 40.555, 13.37, 11.3, "facade"),
    ("F3_CORE", 0, 8.27, 8.4, 4.2, 13.37, 11.3, "core"),
    ("F3_PARTY", 4.1, 4.87, 8.4, 4.3, 12.07, 11.3, "concrete"),
    ("F3_BALC", 4.2, 2.67, 8.4, 13.289, 4.87, 8.52, "balcony"),
    ("F3_RAIL", 4.2, 2.67, 8.4, 13.289, 2.79, 9.5, "railing"),
    ("F3_RAIL_S", 4.2, 2.67, 8.4, 4.32, 4.87, 9.5, "railing"),
    ("F3_RAIL_E", 13.169, 2.67, 8.4, 13.289, 4.87, 9.5, "railing"),
    ("F3_PARTY", 13.189, 4.87, 8.4, 13.389, 12.07, 11.3, "concrete"),
    ("F3_BALC", 13.289, 2.67, 8.4, 22.377, 4.87, 8.52, "balcony"),
    ("F3_RAIL", 13.289, 2.67, 8.4, 22.377, 2.79, 9.5, "railing"),
    ("F3_RAIL_S", 13.289, 2.67, 8.4, 13.409, 4.87, 9.5, "railing"),
    ("F3_RAIL_E", 22.257, 2.67, 8.4, 22.377, 4.87, 9.5, "railing"),
    ("F3_PARTY", 22.277, 4.87, 8.4, 22.477, 12.07, 11.3, "concrete"),
    ("F3_BALC", 22.377, 2.67, 8.4, 31.466, 4.87, 8.52, "balcony"),
    ("F3_RAIL", 22.377, 2.67, 8.4, 31.466, 2.79, 9.5, "railing"),
    ("F3_RAIL_S", 22.377, 2.67, 8.4, 22.497, 4.87, 9.5, "railing"),
    ("F3_RAIL_E", 31.346, 2.67, 8.4, 31.466, 4.87, 9.5, "railing"),
    ("F3_PARTY", 31.366, 4.87, 8.4, 31.566, 12.07, 11.3, "concrete"),
    ("F3_BALC", 31.466, 2.67, 8.4, 40.555, 4.87, 8.52, "balcony"),
    ("F3_RAIL", 31.466, 2.67, 8.4, 40.555, 2.79, 9.5, "railing"),
    ("F3_RAIL_S", 31.466, 2.67, 8.4, 31.586, 4.87, 9.5, "railing"),
    ("F3_RAIL_E", 40.435, 2.67, 8.4, 40.555, 4.87, 9.5, "railing"),
    ("ROOF_SLAB", 0, 2.67, 11, 40.555, 13.37, 11.3, "roof"),
    ("ROOF_PARAPET_W", 0, 2.67, 11.3, 0.25, 13.37, 12.3, "parapet"),
    ("ROOF_PARAPET_E", 40.305, 2.67, 11.3, 40.555, 13.37, 12.3, "parapet"),
    ("ROOF_PARAPET_S", 0, 2.67, 11.3, 40.555, 2.92, 12.3, "parapet"),
    ("ROOF_PARAPET_N", 0, 13.12, 11.3, 40.555, 13.37, 12.3, "parapet"),
    ("ROOF_CORE", 0, 8.27, 11.3, 4.2, 13.37, 14.1, "core"),
]
STREETS = [
    ([(-88.0, 112.13), (-99.0, 135.03), (-120.0, 159.84), (-132.27, 174.45), (-143.11, 188.94), (-146.08, 192.92), (-152.31, 199.0), (-194.37, 245.44), (-196.71, 246.83), (-206.69, 254.45), (-230.62, 265.63), (-260.75, 275.96), (-291.42, 283.24), (-294.57, 284.0), (-317.58, 289.47), (-352.43, 296.68), (-401.35, 306.81)], 22, "secondary"),
    ([(-109.13, 123.31), (-107.98, 121.51), (-98.81, 107.13), (-94.32, 80.81), (-93.05, 60.59), (-90.19, 14.47), (-91.43, -14.86), (-94.62, -31.11), (-97.21, -44.37), (-105.25, -72.58), (-109.65, -88.03), (-116.66, -113.74), (-120.22, -126.79), (-125.61, -147.66), (-128.22, -157.82), (-130.55, -167.72), (-133.79, -179.45), (-137.08, -188.72), (-143.6, -207.1), (-162.46, -248.11), (-165.84, -254.12), (-176.55, -273.18), (-186.73, -291.27), (-211.88, -335.04), (-240.56, -387.48)], 22, "secondary"),
    ([(-109.13, 123.31), (-153.41, 131.01)], 8.5, "residential"),
    ([(-94.62, -31.11), (-139.33, -28.5)], 8.5, "residential"),
    ([(-116.66, -113.74), (-148.8, -110.83)], 8.5, "residential"),
    ([(-105.25, -72.58), (-155.87, -69.1)], 8.5, "residential"),
    ([(-232.14, -391.12), (-182.47, -303.68), (-179.18, -297.89), (-168.92, -277.61), (-159.16, -258.32), (-130.49, -202.79), (-126.42, -191.62), (-124.04, -182.59), (-120.43, -168.95), (-117.57, -158.01), (-115.53, -149.63), (-114.25, -144.37), (-111.04, -131.23), (-110.4, -128.65), (-106.72, -113.56), (-105.61, -109.52), (-100.4, -90.87), (-91.04, -60.15), (-82.93, -30.64), (-80.2, -14.82), (-79.88, 13.14), (-81.92, 59.22), (-82.47, 81.35), (-86.26, 107.03), (-88.0, 112.13)], 22, "secondary"),
    ([(-80.2, -14.82), (-47.85, -13.68), (-21.01, -8.75), (-7.77, -7.49), (0.16, -7.77), (14.16, -12.95), (29.14, -13.73), (39.96, -11.98), (77.68, -13.73), (97.29, -15.86), (131.49, -26.75), (192.89, -46.39)], 8.5, "residential"),
    ([(-47.85, -13.68), (-48.13, -24.36), (-57.01, -90.15), (-58.64, -106.4)], 8.5, "residential"),
    ([(-58.64, -106.4), (-100.4, -90.87)], 8.5, "residential"),
    ([(-21.01, -8.75), (-29.53, -79.62), (-29.09, -82.87), (-27.34, -85.15), (-24.13, -85.66), (32.57, -90.46)], 8.5, "residential"),
    ([(-61.28, -49.97), (-65.56, -66.75), (-91.04, -60.15)], 8.5, "residential"),
    ([(-86.26, 107.03), (-78.06, 107.55), (-61.13, 105.21), (-43.67, 98.37), (-30.32, 92.19), (-18.38, 92.07), (93.86, 98.74)], 8.5, "residential"),
    ([(-90.19, 14.47), (-134.66, 18.83)], 8.5, "residential"),
    ([(-93.05, 60.59), (-123.18, 60.91)], 8.5, "residential"),
    ([(97.29, -15.86), (93.75, -37.85), (90.45, -51.87)], 8.5, "residential"),
    ([(-438.31, 301.71), (-354.79, 287.96), (-288.19, 273.0), (-234.58, 256.5), (-216.69, 247.99), (-200.39, 237.44), (-184.58, 221.74), (-175.28, 211.01), (-170.7, 205.14), (-153.76, 182.63), (-141.64, 166.82), (-137.03, 160.39), (-130.47, 151.62), (-109.13, 123.31)], 22, "secondary"),
    ([(80.87, -149.06), (26.7, -135.98), (-60.95, -119.9)], 8.5, "residential"),
    ([(-60.95, -119.9), (-105.61, -109.52)], 8.5, "residential"),
    ([(-64.5, -141.06), (-60.95, -119.9)], 8.5, "residential"),
    ([(39.96, -11.98), (32.57, -90.46), (26.7, -135.98)], 8.5, "residential"),
    ([(-58.64, -106.4), (-60.95, -119.9)], 8.5, "residential"),
    ([(-99.0, 135.03), (-95.45, 147.85), (-89.8, 162.73), (-84.97, 175.1), (-77.47, 195.62), (-72.19, 209.13), (-65.78, 226.91)], 8.5, "residential"),
]
AERIAL = {'w': 1280, 'h': 1792, 'mx': 0.2515, 'my': 0.2498, 'px': 604.75, 'py': 839.35, 'cx': 20.285, 'cy': 6.685}
MAT_DEF = {
    "facade": ((0.78, 0.735, 0.665), 0.62, 0),
    "concrete": ((0.58, 0.57, 0.55), 0.78, 0),
    "slab": ((0.62, 0.61, 0.59), 0.8, 0),
    "balcony": ((0.6, 0.55, 0.48), 0.7, 0),
    "railing": ((0.18, 0.22, 0.26), 0.18, 0.75),
    "shopfront": ((0.1, 0.13, 0.17), 0.06, 0.1),
    "roof": ((0.5, 0.49, 0.47), 0.85, 0),
    "parapet": ((0.68, 0.66, 0.63), 0.7, 0),
    "core": ((0.7, 0.67, 0.63), 0.7, 0),
    "site": ((0.52, 0.48, 0.43), 0.95, 0),
    "sign": ((0.85, 0.83, 0.8), 0.55, 0),
    "parking": ((0.42, 0.46, 0.55), 0.85, 0),
}

# ============================================================ پارامترها
LAT, LON = 32.6307, 51.7238
MONTH, DAY, HOUR = 9, 17, 9.0
RES_X, RES_Y = 1600, 1000
SAMPLES = 160
DEVICE = "auto"
EXPOSURE = 0.0

# دوربین‌ها: (نام, مکان, هدف, فاصلهٔ کانونی mm)
CAMERAS = [
    ("نما-خیابان", (46.0, -26.0, 1.7), (18.0, 8.0, 6.0), 26),
    ("نما-سه-رخ", (-12.0, -18.0, 1.7), (18.0, 7.0, 5.0), 28),
    ("نما-هوایی", (72.0, -58.0, 38.0), (20.0, 14.0, 8.0), 28),
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
