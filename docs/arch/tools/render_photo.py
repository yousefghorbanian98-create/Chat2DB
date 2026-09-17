#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""رندررِ واقع‌گرایانه (CPU، numpy) — زمینِ شما پس از ساخت، در جایِ واقعی.

ویژگی‌ها: پرسپکتیوِ درست · نقشهٔ سایهٔ خورشید با PCF · نورِ آسمانِ نیم‌کره‌ای ·
بافتِ ماهواره‌ایِ زمینِ واقعی (ژئورفرنس) · شبکهٔ معابر از OSM · ساختمان‌هایِ همسایه ·
مه و دورنمایِ هوایی · نقشه‌یِ تُنِ فیلمی · ویگنت و دانهٔ فیلم.

خروجی: docs/arch/photo-*.png
"""
import os, sys, json, math
import numpy as np
from PIL import Image, ImageFilter
import plan_model as PM

HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUTDIR = os.path.join(HERE, "docs", "arch")
GEO = os.path.join(HERE, "docs", "arch", "geo")

# ---------------------------------------------------------------- مختصاتِ جهان: مبدأ گوشهٔ جنوب‌غربیِ زمین
LAT0, LON0 = 32.6305401, 51.7238816
M_PER_DEG_LAT = 110734.0
M_PER_DEG_LON = 111320.0 * math.cos(math.radians(32.63))
PLC_X, PLC_Y = 20.285, 6.685          # مرکزِ زمین در مختصاتِ جهان

AERIAL = Image.open(os.path.join(GEO, "aerial_z19.jpg")).convert("RGB")
AER = np.asarray(AERIAL).astype(np.float32) / 255.0
AER_H, AER_W = AER.shape[:2]
AER_PX, AER_PY = 604.75, 839.35       # پیکسلِ مرکز
AER_MX = (51.72569274902344 - 51.722259521484375) * M_PER_DEG_LON / AER_W
AER_MY = (32.632436063121546 - 32.628388175159984) * M_PER_DEG_LAT / AER_H


def ll2xy(lat, lon):
    x = (lon - LON0) * M_PER_DEG_LON + PLC_X
    y = (lat - LAT0) * M_PER_DEG_LAT + PLC_Y
    return x, y


def world2aerial_uv(x, y):
    u = (AER_PX + (x - PLC_X) / AER_MX) / AER_W
    v = (AER_PY - (y - PLC_Y) / AER_MY) / AER_H
    return u, v


# ================================================================ مصالح
MAT = {
    "terrain":   dict(alb=(0.52, 0.48, 0.43), spec=0.02, rough=0.95, tex="aerial"),
    "asphalt":   dict(alb=(0.145, 0.145, 0.150), spec=0.06, rough=0.55),
    "sidewalk":  dict(alb=(0.60, 0.58, 0.55), spec=0.03, rough=0.85),
    "curb":      dict(alb=(0.44, 0.43, 0.41), spec=0.03, rough=0.8),
    "facade":    dict(alb=(0.80, 0.755, 0.685), spec=0.03, rough=0.85),
    "facade2":   dict(alb=(0.70, 0.655, 0.60), spec=0.03, rough=0.85),
    "core":      dict(alb=(0.72, 0.69, 0.645), spec=0.03, rough=0.85),
    "balcony":   dict(alb=(0.66, 0.62, 0.575), spec=0.05, rough=0.7),
    "railing":   dict(alb=(0.20, 0.24, 0.28), spec=0.45, rough=0.20),
    "glass":     dict(alb=(0.10, 0.13, 0.17), spec=0.85, rough=0.06),
    "shopfront": dict(alb=(0.13, 0.15, 0.18), spec=0.75, rough=0.10),
    "concrete":  dict(alb=(0.58, 0.565, 0.545), spec=0.03, rough=0.85),
    "terrace":   dict(alb=(0.30, 0.42, 0.22), spec=0.02, rough=0.95),
    "roof":      dict(alb=(0.50, 0.485, 0.465), spec=0.04, rough=0.8),
    "parapet":   dict(alb=(0.68, 0.65, 0.615), spec=0.03, rough=0.85),
    "nbr1":      dict(alb=(0.74, 0.70, 0.64), spec=0.03, rough=0.88),
    "nbr2":      dict(alb=(0.62, 0.58, 0.55), spec=0.03, rough=0.88),
    "nbr3":      dict(alb=(0.83, 0.79, 0.73), spec=0.03, rough=0.88),
    "nbr4":      dict(alb=(0.55, 0.50, 0.46), spec=0.03, rough=0.88),
    "trunk":     dict(alb=(0.20, 0.15, 0.11), spec=0.02, rough=0.9),
    "leaf":      dict(alb=(0.16, 0.29, 0.13), spec=0.02, rough=0.95),
    "metal":     dict(alb=(0.42, 0.43, 0.45), spec=0.30, rough=0.4),
    "car1":      dict(alb=(0.72, 0.73, 0.76), spec=0.55, rough=0.18),
    "car2":      dict(alb=(0.16, 0.18, 0.24), spec=0.55, rough=0.18),
    "car3":      dict(alb=(0.62, 0.20, 0.16), spec=0.55, rough=0.18),
    "car4":      dict(alb=(0.30, 0.32, 0.38), spec=0.55, rough=0.18),
    "sign":      dict(alb=(0.85, 0.83, 0.80), spec=0.05, rough=0.6),
}
MAT_KEYS = list(MAT.keys())
MAT_IDX = {k: i for i, k in enumerate(MAT_KEYS)}


# ================================================================ صحنه
class Scene:
    def __init__(self):
        self.V = []          # رأس‌ها (x,y,z)
        self.T = []          # مثلث‌ها (i0,i1,i2)
        self.M = []          # شناسهٔ مصالحِ هر مثلث

    def vert(self, x, y, z):
        self.V.append((float(x), float(y), float(z)))
        return len(self.V) - 1

    def tri(self, a, b, c, mat):
        self.T.append((a, b, c))
        self.M.append(MAT_IDX[mat] if isinstance(mat, str) else mat)

    def quad(self, p0, p1, p2, p3, mat):
        a = self.vert(*p0); b = self.vert(*p1); c = self.vert(*p2); d = self.vert(*p3)
        self.tri(a, b, c, mat); self.tri(a, c, d, mat)

    def grid(self, x0, y0, x1, y1, z, mat, n=34):
        """چهارگوشِ شبکه‌بندی‌شده — برای جلوگیری از مثلث‌های غول‌پیکر"""
        for i in range(n):
            for j in range(n):
                ax = x0 + (x1 - x0) * i / n
                bx = x0 + (x1 - x0) * (i + 1) / n
                ay = y0 + (y1 - y0) * j / n
                by = y0 + (y1 - y0) * (j + 1) / n
                self.quad((ax, ay, z), (bx, ay, z), (bx, by, z), (ax, by, z), mat)

    def box(self, x0, y0, z0, x1, y1, z1, mat, skip_bottom=True):
        p = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0),
             (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
        q = [(0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7), (4, 5, 6, 7)]
        if not skip_bottom:
            q.append((0, 3, 2, 1))
        for (a, b, c, d) in q:
            self.quad(p[a], p[b], p[c], p[d], mat)

    def arrays(self):
        return (np.asarray(self.V, dtype=np.float64),
                np.asarray(self.T, dtype=np.int32),
                np.asarray(self.M, dtype=np.int32))


# ================================================================ خورشید (اصفهان)
def sun_vector(month_day_hour=(9, 17, 9.0), lat=32.6307):
    """بردارِ خورشید برای تاریخ و ساعتِ محلیِ ایران (UTC+3:30، بدونِ DST)"""
    m, d, hour = month_day_hour
    N = (m - 1) * 30.4 + d                      # شمارهٔ روزِ سال (تقریب)
    decl = 23.45 * math.sin(math.radians(360.0 / 365.0 * (284 + N)))
    H = 15.0 * (hour - 12.0)
    phi = math.radians(lat)
    de = math.radians(decl)
    h = math.radians(H)
    sa = math.sin(phi) * math.sin(de) + math.cos(phi) * math.cos(de) * math.cos(h)
    alt = math.asin(max(-1, min(1, sa)))
    ca = (math.sin(de) - math.sin(alt) * math.sin(phi)) / (math.cos(alt) * math.cos(phi) + 1e-9)
    az = math.acos(max(-1, min(1, ca)))
    if H > 0:
        az = 2 * math.pi - az
    return np.array([math.cos(alt) * math.sin(az), math.cos(alt) * math.cos(az),
                     math.sin(alt)], dtype=np.float64), math.degrees(alt), math.degrees(az)


# ================================================================ رستر
def rasterize(V, T, M, cam_pos, cam_basis, fovx, W, H, near=0.1):
    """برگرداندنِ G-buffer: عمق، شناسه، نقطهٔ جهان، نرمال"""
    fwd, right, up = cam_basis
    d = V - cam_pos[None, :]
    zc = d @ fwd
    xc = d @ right
    yc = d @ up
    with np.errstate(divide="ignore", invalid="ignore"):
        sx = (xc / zc) / math.tan(fovx / 2.0)
        sy = (yc / zc) / (math.tan(fovx / 2.0) * H / W)
    px = (sx * 0.5 + 0.5) * W
    py = (0.5 - sy * 0.5) * H
    depth = zc.copy()

    zb = np.full((H, W), 1e18, dtype=np.float64)
    idb = np.full((H, W), -1, dtype=np.int32)
    wbuf = np.zeros((H, W, 3), dtype=np.float64)          # نقطهٔ جهان (برای محاسبات بعدی)
    tri_id = np.full((H, W), -1, dtype=np.int32)
    bary = np.zeros((H, W, 2), dtype=np.float64)

    P = np.stack([px, py], axis=1)
    for ti in range(T.shape[0]):
        i0, i1, i2 = T[ti]
        if zc[i0] < near or zc[i1] < near or zc[i2] < near:
            continue
        x0, y0 = px[i0], py[i0]
        x1, y1 = px[i1], py[i1]
        x2, y2 = px[i2], py[i2]
        minx = max(0, int(math.floor(min(x0, x1, x2))))
        maxx = min(W - 1, int(math.ceil(max(x0, x1, x2))))
        miny = max(0, int(math.floor(min(y0, y1, y2))))
        maxy = min(H - 1, int(math.ceil(max(y0, y1, y2))))
        if minx > maxx or miny > maxy:
            continue
        yy, xx = np.mgrid[miny:maxy + 1, minx:maxx + 1]
        cxp = xx + 0.5
        cyp = yy + 0.5
        d00 = (x1 - x0) * (y2 - y0) - (x2 - x0) * (y1 - y0)
        if abs(d00) < 1e-12:
            continue
        l0 = ((x1 - cxp) * (y2 - cyp) - (x2 - cxp) * (y1 - cyp)) / d00
        l1 = ((x2 - cxp) * (y0 - cyp) - (x0 - cxp) * (y2 - cyp)) / d00
        l2 = 1.0 - l0 - l1
        m = (l0 >= -1e-9) & (l1 >= -1e-9) & (l2 >= -1e-9)
        if not m.any():
            continue
        # درون‌یابیِ پرسپکتیو-صحیح
        w0 = l0 / max(zc[i0], near)
        w1 = l1 / max(zc[i1], near)
        w2 = l2 / max(zc[i2], near)
        iw = 1.0 / (w0 + w1 + w2 + 1e-18)
        zz = 1.0 / (w0 + w1 + w2 + 1e-18)         # عمقِ درون‌یابی‌شده
        sel = m & (zz < zb[yy, xx])
        if not sel.any():
            continue
        yy2, xx2 = yy[sel], xx[sel]
        zb[yy2, xx2] = zz[sel]
        idb[yy2, xx2] = M[ti]
        tri_id[yy2, xx2] = ti
        b0 = (w0 * iw)[sel]
        b1 = (w1 * iw)[sel]
        wbuf[yy2, xx2] = (V[i0][None, :] * b0[:, None] + V[i1][None, :] * b1[:, None] +
                          V[i2][None, :] * (1 - b0 - b1)[:, None])
        bary[yy2, xx2, 0] = b0
        bary[yy2, xx2, 1] = b1
    return zb, idb, tri_id, wbuf, bary


def normals(V, T, tri_id, H, W):
    v0 = V[T[:, 0]]; v1 = V[T[:, 1]]; v2 = V[T[:, 2]]
    n = np.cross(v1 - v0, v2 - v0)
    ln = np.linalg.norm(n, axis=1, keepdims=True) + 1e-12
    n = n / ln
    out = np.zeros((H, W, 3), dtype=np.float64)
    m = tri_id >= 0
    out[m] = n[tri_id[m]]
    return out


def shadow_map(V, T, L, extent=110.0, res=1600):
    """نقشهٔ عمق از دیدِ خورشید (اورتوگرافیک در امتدادِ L)"""
    L = L / np.linalg.norm(L)
    upv = np.array([0.0, 0.0, 1.0])
    if abs(np.dot(L, upv)) > 0.98:
        upv = np.array([0.0, 1.0, 0.0])
    fwd = -L
    right = np.cross(fwd, upv); right /= np.linalg.norm(right)
    up = np.cross(right, fwd)
    c = V[T].reshape(-1, 3)
    u = c @ right
    v = c @ up
    o = 0.5 * extent
    px = (u + o) / extent * res
    py = (v + o) / extent * res
    zb = np.full((res, res), 1e18, dtype=np.float32)
    for ti in range(T.shape[0]):
        i0, i1, i2 = T[ti]
        x0, y0 = px[i0], py[i0]; x1, y1 = px[i1], py[i1]; x2, y2 = px[i2], py[i2]
        minx = max(0, int(math.floor(min(x0, x1, x2)))); maxx = min(res - 1, int(math.ceil(max(x0, x1, x2))))
        miny = max(0, int(math.floor(min(y0, y1, y2)))); maxy = min(res - 1, int(math.ceil(max(y0, y1, y2))))
        if minx > maxx or miny > maxy:
            continue
        yy, xx = np.mgrid[miny:maxy + 1, minx:maxx + 1]
        cxp = xx + 0.5; cyp = yy + 0.5
        d00 = (x1 - x0) * (y2 - y0) - (x2 - x0) * (y1 - y0)
        if abs(d00) < 1e-12:
            continue
        l0 = ((x1 - cxp) * (y2 - cyp) - (x2 - cxp) * (y1 - cyp)) / d00
        l1 = ((x2 - cxp) * (y0 - cyp) - (x0 - cxp) * (y2 - cyp)) / d00
        l2 = 1 - l0 - l1
        m = (l0 >= -1e-9) & (l1 >= -1e-9) & (l2 >= -1e-9)
        if not m.any():
            continue
        z = l0 * (c[i0] @ (-fwd)) + l1 * (c[i1] @ (-fwd)) + l2 * (c[i2] @ (-fwd))
        sel = m & (z > zb[yy, xx])
        zb[yy[sel], xx[sel]] = z[sel]
    return zb, right, up, -fwd, o, extent, res


# ================================================================ ساختِ صحنه
def build_scene(corridors=()):
    sc = Scene()
    z = PM.core_zones()
    shf = [c for c in z if c["kind"] == "shaft"][0]

    # ---- زمین (بافتِ ماهواره‌ای)
    R = 150.0
    cx, cy = PLC_X, PLC_Y
    sc.grid(cx - R, cy - R, cx + R, cy + R, -0.05, "terrain", n=40)
    # ---- پیاده‌رو و جدولِ کنارِ گذرِ ۸ متری و گذرِ جنوبی
    sc.box(-4.0, PM.Y1, 0.0, PM.LAND_W + 4.0, PM.Y1 + 2.2, 0.16, "sidewalk")
    sc.box(-4.0, PM.Y1 + 2.2, 0.0, PM.LAND_W + 4.0, PM.Y1 + 2.5, 0.30, "curb")
    sc.box(-8.0, -9.4, 0.0, PM.LAND_W + 8.0, -7.9, 0.16, "sidewalk")
    sc.box(-8.0, -9.7, 0.0, PM.LAND_W + 8.0, -9.4, 0.30, "curb")
    # ---- گذرِ ۸ متری
    sc.box(-6.0, PM.Y1 + 2.5, 0.0, PM.LAND_W + 6.0, PM.Y1 + 2.5 + 8.0, 0.02, "asphalt")
    # ---- فضای بازِ جنوبیِ زمین
    sc.box(0.0, 0.0, 0.0, PM.LAND_W, PM.Y0, 0.10, "terrace")

    # ---- ساختمانِ شما
    for (x0, y0, zz0, x1, y1, zz1, m) in PM.building_boxes():
        sc.box(x0, y0, zz0, x1, y1, zz1, m)
    # دیواره‌هایِ شفت
    sc.box(shf["x0"] - 0.15, shf["y0"], PM.POD_H, shf["x0"], shf["y1"], PM.TOP, "core")
    sc.box(shf["x1"], shf["y0"], PM.POD_H, shf["x1"] + 0.15, shf["y1"], PM.TOP, "core")
    sc.box(shf["x0"], shf["y0"] - 0.15, PM.POD_H, shf["x1"], shf["y0"], PM.TOP, "core")
    # نردهٔ تراس
    sc.box(PM.BLD_W, PM.Y0, PM.POD_H, PM.LAND_W, PM.Y0 + 0.15, PM.POD_H + 1.1, "railing")
    # ورودیِ پیاده
    sc.box(PM.CORE_X0, PM.Y1, 0.0, PM.CORE_X0 + 2.6, PM.Y1 + 2.5, 3.2, "concrete")
    # سایبانِ مغازه‌ها
    for i in range(PM.NSHOP):
        x0 = PM.SHOP_X0 + i * PM.SHOP_W
        sc.box(x0, PM.Y1 - 0.1, 3.4, x0 + PM.SHOP_W, PM.Y1 + 1.6, 3.55, "sign")

    # ---- شبکهٔ معابر از OSM
    ov = json.load(open(os.path.join(GEO, "overpass.json")))
    ways = []
    for e in ov["elements"]:
        if "geometry" not in e or len(e["geometry"]) < 2:
            continue
        t = e.get("tags", {})
        hw = t.get("highway")
        if not hw:
            continue
        w = {"secondary": 22.0, "secondary_link": 12.0, "residential": 8.5, "track": 5.0}.get(hw, 7.0)
        pts = [ll2xy(p["lat"], p["lon"]) for p in e["geometry"]]
        ways.append((pts, w, hw))
    for (pts, w, hw) in ways:
        for i in range(len(pts) - 1):
            (x0, y0), (x1, y1) = pts[i], pts[i + 1]
            dx, dy = x1 - x0, y1 - y0
            L = math.hypot(dx, dy)
            if L < 1e-6:
                continue
            nx, ny = -dy / L * w / 2, dx / L * w / 2
            sc.quad((x0 + nx, y0 + ny, 0.012), (x1 + nx, y1 + ny, 0.012),
                    (x1 - nx, y1 - ny, 0.012), (x0 - nx, y0 - ny, 0.012), "asphalt")

    # ---- ساختمان‌های همسایه (از بافتِ معابر) — با حفظِ کریدورِ دید
    rng = np.random.RandomState(7)

    def seg_dist(px_, py_, a, b):
        ax, ay = a; bx, by = b
        dx, dy = bx - ax, by - ay
        L2 = dx * dx + dy * dy
        t = 0.0 if L2 == 0 else max(0.0, min(1.0, ((px_ - ax) * dx + (py_ - ay) * dy) / L2))
        return math.hypot(px_ - (ax + dx * t), py_ - (ay + dy * t))

    nb = 0
    for (pts, w, hw) in ways:
        if hw == "secondary":
            continue
        off = w / 2 + 2.5
        for side in (1, -1):
            seg_start = 0.0
            total = 0.0
            for i in range(len(pts) - 1):
                (x0, y0), (x1, y1) = pts[i], pts[i + 1]
                dx, dy = x1 - x0, y1 - y0
                L = math.hypot(dx, dy)
                if L < 4:
                    continue
                nx, ny = -dy / L * off * side, dx / L * off * side
                # بُرش‌های ۸ تا ۲۰ متری با درز
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
                    in_plot = (-3 < ccx < PM.LAND_W + 3) and (-3 < ccy < PM.Y1 + 2)
                    blocked = any(seg_dist(ccx, ccy, c[0][:2], c[1][:2]) < c[2] for c in corridors)
                    if not in_plot and not blocked:
                        mat = rng.choice(["nbr1", "nbr2", "nbr3", "nbr4"])
                        sc.box(min(ax, bx, ex, fx), min(ay, by, ey, fy), 0.0,
                               max(ax, bx, ex, fx), max(ay, by, ey, fy), hgt, mat)
                        nb += 1
                    t += ln + rng.uniform(1.0, 3.0)

    # ---- درختانِ کنارِ خیابان
    for (x, y) in [(2, PM.Y1 + 3.4), (8, PM.Y1 + 3.4), (14, PM.Y1 + 3.4), (20, PM.Y1 + 3.4),
                   (26, PM.Y1 + 3.4), (32, PM.Y1 + 3.4), (38, PM.Y1 + 3.4),
                   (12, -1.2), (20, -1.2), (28, -1.2), (36, -1.2)]:
        sc.box(x - 0.18, y - 0.18, 0.0, x + 0.18, y + 0.18, 3.0, "trunk")
        sc.box(x - 1.9, y - 1.9, 3.0, x + 1.9, y + 1.9, 6.6, "leaf")

    # ---- تیرِ چراغ‌برق
    for (x, y) in [(4, PM.Y1 + 3.0), (16, PM.Y1 + 3.0), (28, PM.Y1 + 3.0), (40, PM.Y1 + 3.0)]:
        sc.box(x - 0.12, y - 0.12, 0.0, x + 0.12, y + 0.12, 8.5, "metal")
        sc.box(x - 0.9, y - 0.14, 8.3, x + 0.9, y + 0.14, 8.6, "metal")

    # ---- دکلِ فشارقوی در نوارِ جنوبی
    for tx in (10.0, 34.0):
        ty = -3.6
        sc.box(tx - 0.45, ty - 0.45, 0.0, tx + 0.45, ty + 0.45, 2.0, "metal")
        sc.box(tx - 0.16, ty - 0.16, 2.0, tx + 0.16, ty + 0.16, 17.0, "metal")
        sc.box(tx - 3.2, ty - 0.12, 15.4, tx + 3.2, ty + 0.12, 15.7, "metal")
        sc.box(tx - 2.4, ty - 0.12, 13.2, tx + 2.4, ty + 0.12, 13.5, "metal")
    # سیم‌ها
    for yy in (15.55, 13.35):
        sc.box(9.0, -3.7, yy, 35.0, -3.5, yy + 0.06, "metal")

    # ---- خودروهای پارک‌شده
    cars = ["car1", "car2", "car3", "car4"]
    for i, (x, y) in enumerate([(3.0, PM.Y1 + 4.2), (6.0, PM.Y1 + 4.2), (9.0, PM.Y1 + 4.2),
                                (15.0, PM.Y1 + 4.2), (18.0, PM.Y1 + 4.2), (24.0, PM.Y1 + 4.2),
                                (30.0, PM.Y1 + 4.2), (33.0, PM.Y1 + 4.2)]):
        c = cars[i % 4]
        sc.box(x, y, 0.0, x + 4.3, y + 1.75, 0.75, c)
        sc.box(x + 0.7, y, 0.75, x + 3.4, y + 1.75, 1.45, c)
    return sc, nb


# ================================================================ رندر
def render(sc, cam_pos, cam_target, fovx_deg, W, H, ss, L, out_path, view_name=""):
    V, T, M = sc.arrays()
    fwd = np.asarray(cam_target, dtype=np.float64) - np.asarray(cam_pos, dtype=np.float64)
    fwd = fwd / np.linalg.norm(fwd)
    up0 = np.array([0.0, 0.0, 1.0])
    right = np.cross(fwd, up0); right = right / np.linalg.norm(right)
    up = np.cross(right, fwd)
    fovx = math.radians(fovx_deg)
    RW, RH = W * ss, H * ss
    print(f"  [{view_name}] رستر در {RW}×{RH} …", flush=True)
    zb, idb, tri_id, wbuf, bary = rasterize(V, T, M, np.asarray(cam_pos, float),
                                            (fwd, right, up), fovx, RW, RH)
    N = normals(V, T, tri_id, RH, RW)
    hit = tri_id >= 0
    print(f"  [{view_name}] نقشهٔ سایه …", flush=True)
    sm, sright, sup, sfwd, so, sext, sres = shadow_map(V, T, L)

    # نورِ آسمان و خورشید
    Ln = L / np.linalg.norm(L)
    alt = math.degrees(math.asin(Ln[2]))
    t_sun = max(0.0, min(1.0, (alt + 6) / 40.0))
    sun_col = np.array([1.00, 0.94, 0.86]) * (0.55 + 0.45 * t_sun) * 1.32
    sky_top = np.array([0.24, 0.40, 0.76])
    sky_hor = np.array([0.78, 0.83, 0.90])
    gnd_col = np.array([0.34, 0.30, 0.26])

    P = wbuf
    dist = np.linalg.norm(P - np.asarray(cam_pos, float)[None, None, :], axis=2)

    # --- سایه
    sh_u = P @ sright
    sh_v = P @ sup
    shx = ((sh_u + so) / sext * sres).astype(np.int32)
    shy = ((sh_v + so) / sext * sres).astype(np.int32)
    shx = np.clip(shx, 0, sres - 1); shy = np.clip(shy, 0, sres - 1)
    d_sun = P @ sfwd
    vis = np.zeros((RH, RW), dtype=np.float64)
    for oy in (-1, 0, 1):
        for ox in (-1, 0, 1):
            zs = sm[np.clip(shy + oy, 0, sres - 1), np.clip(shx + ox, 0, sres - 1)]
            vis += (d_sun > zs - 0.34).astype(np.float64)
    vis /= 9.0
    ndl = np.clip((N * Ln[None, None, :]).sum(2), 0, 1) * vis

    # --- رنگِ پایه
    alb = np.zeros((RH, RW, 3), dtype=np.float64)
    spec = np.zeros((RH, RW), dtype=np.float64)
    rough = np.ones((RH, RW), dtype=np.float64)
    for k, name in enumerate(MAT_KEYS):
        m = (idb == k)
        if not m.any():
            continue
        mm = MAT[name]
        if mm.get("tex") == "aerial":
            u, v = world2aerial_uv(P[..., 0], P[..., 1])
            uu = np.clip((u * AER_W).astype(np.int32), 0, AER_W - 1)
            vv = np.clip((v * AER_H).astype(np.int32), 0, AER_H - 1)
            tex = AER[vv, uu]
            alb[m] = (tex[m] ** 2.2) * 1.18
        else:
            alb[m] = np.array(mm["alb"])
        spec[m] = mm["spec"]
        rough[m] = mm["rough"]

    # --- نورپردازی
    sky_w = 0.5 + 0.5 * N[..., 2]
    amb = (sky_hor * 0.55 + sky_top * 0.45)[None, None, :] * sky_w[..., None] * 0.40
    amb = amb + gnd_col[None, None, :] * (1 - sky_w)[..., None] * 0.14 + 0.05
    diffuse = alb * (sun_col[None, None, :] * ndl[..., None] * 1.00 + amb)
    # درخششِ آسمان در پنجره‌ها و شیشه
    refl = np.clip((N[..., 2] * 0.5 + 0.5), 0, 1)
    diffuse += alb * spec[..., None] * (sky_hor * 0.5 + sky_top * 0.5)[None, None, :] * \
        (0.35 + 0.65 * refl[..., None]) * 0.55
    # تابشِ آفتابیِ مستقیم (specular)
    Vdir = np.asarray(cam_pos, float)[None, None, :] - P
    Vdir /= (np.linalg.norm(Vdir, axis=2, keepdims=True) + 1e-9)
    Hv = Vdir + Ln[None, None, :]
    Hv /= (np.linalg.norm(Hv, axis=2, keepdims=True) + 1e-9)
    nh = np.clip((N * Hv).sum(2), 0, 1)
    shin = np.exp((1 - rough) * 8) * 24 + 4
    specular = (nh ** shin[..., None] if False else np.power(nh, 8)[..., None]) * \
        spec[..., None] * vis[..., None] * sun_col[None, None, :] * 0.55
    col = diffuse + specular

    # --- آسمان
    yy, xx = np.mgrid[0:RH, 0:RW]
    ndcx = (xx + 0.5) / RW * 2 - 1
    ndcy = 1 - (yy + 0.5) / RH * 2
    tanx = math.tan(fovx / 2)
    dirs = (fwd[None, None, :] + right[None, None, :] * (ndcx * tanx)[..., None] +
            up[None, None, :] * (ndcy * tanx * RH / RW)[..., None])
    dirs /= np.linalg.norm(dirs, axis=2, keepdims=True)
    hz = np.clip(dirs[..., 2], 0, 1)
    sky = (sky_hor[None, None, :] * (1 - hz ** 0.42)[..., None] +
           sky_top[None, None, :] * (hz ** 0.42)[..., None])
    sunamt = np.clip((dirs * Ln[None, None, :]).sum(2), 0, 1)
    sky += np.array([1.0, 0.92, 0.80])[None, None, :] * (sunamt ** 220)[..., None] * 2.2
    sky += np.array([1.0, 0.90, 0.74])[None, None, :] * (sunamt ** 8)[..., None] * 0.20
    haze = np.array([0.86, 0.87, 0.87])[None, None, :] * (1 - np.clip(hz * 3.2, 0, 1))[..., None] * 0.35
    sky = sky * (1 - 0) + haze
    col = np.where(hit[..., None], col, sky)

    # --- مه / دورنمای هوایی
    fogc = np.array([0.74, 0.76, 0.79])
    fog = 1 - np.exp(-(dist / 320.0) ** 1.7)
    col = col * (1 - fog[..., None]) + fogc[None, None, :] * fog[..., None]

    # --- کاهشِ نورِ آسمان در پیش‌زمینه (عمقِ میدانِ هوایی)
    col = np.clip(col, 0, None)

    # --- پس‌پردازش
    imgf = col.astype(np.float32)
    # تون‌مپِ فیلمی (ACES تقریبی)
    a, b, c, d, e = 2.51, 0.03, 2.43, 0.59, 0.14
    imgf = np.clip((imgf * (a * imgf + b)) / (imgf * (c * imgf + d) + e), 0, 1)
    imgf = imgf ** (1 / 2.2)
    imgf = np.clip((imgf - 0.50) * 1.14 + 0.47, 0, 1)          # کنتراست و نقطهٔ میانی
    sat = imgf.mean(2, keepdims=True)
    imgf = np.clip(sat + (imgf - sat) * 1.18, 0, 1)            # اشباعِ رنگ
    # ویگنت
    vy, vx = np.mgrid[0:RH, 0:RW]
    rr = np.sqrt(((vx - RW / 2) / (RW / 2)) ** 2 + ((vy - RH / 2) / (RH / 2)) ** 2)
    imgf *= (1 - 0.30 * np.clip(rr - 0.55, 0, 1) ** 1.6)[..., None]
    # گرمایِ نوری و کنتراست
    imgf[..., 0] *= 1.02
    imgf[..., 2] *= 0.985
    imgf = np.clip(imgf, 0, 1)

    im = Image.fromarray((imgf * 255).astype(np.uint8)).resize((W, H), Image.LANCZOS)
    # دانهٔ فیلمِ ملایم
    nz = np.random.RandomState(3).normal(0, 0.006, (H, W, 1)).astype(np.float32)
    arr = np.asarray(im).astype(np.float32) / 255.0 + nz
    im = Image.fromarray(np.clip(arr, 0, 1).__mul__(255).astype(np.uint8))
    im.save(out_path)
    return out_path


if __name__ == "__main__":
    L, alt, az = sun_vector((9, 17, 9.0))
    print(f"خورشیدِ ۱۷ شهریور، ساعت ۹ صبحِ اصفهان: ارتفاع {alt:.1f}° · آزیموت {az:.1f}°")
    W, H = 1500, 940
    VIEWS = [
        ("photo-street.png", (44.0, -27.0, 1.70), (9.0, 7.5, 13.0), 66, 2,
         "ایستاده در پیاده‌رویِ روبه‌رو در خیابانِ جنوبی"),
        ("photo-close.png", (-9.0, -19.0, 1.70), (11.0, 7.0, 9.0), 66, 2,
         "نمای سه‌رخ از جنوب‌غربی"),
        ("photo-aerial.png", (78.0, -62.0, 44.0), (20.0, 16.0, 14.0), 65, 2,
         "نمای هوایی (پهپاد) از جنوب‌شرق"),
    ]
    corridors = [(v[1], v[2], 26.0) for v in VIEWS if v[0] != "photo-aerial.png"]
    sc, nb = build_scene(corridors)
    V, T, M = sc.arrays()
    print(f"صحنه: {len(V)} رأس · {len(T)} مثلث · {nb} بنای همسایه")
    for name, pos, tgt, fov, ss, vn in VIEWS:
        render(sc, pos, tgt, fov, W, H, ss, L, os.path.join(OUTDIR, name), vn)
        print("  ذخیره:", name, flush=True)
