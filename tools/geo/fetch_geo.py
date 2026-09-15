#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
دریافت داده‌های جغرافیایی واقعی محل زمین (مختصات کارفرما)
- تایل‌های هوایی Esri World Imagery (زوم ۱۶ تا ۱۹) + متادیتا ژئورفرنس
- داده OSM (خیابان‌ها + بناها) از Overpass
خروجی: docs/architecture-plan/geo/
"""
import json, math, os, io, time, urllib.request

LAT, LON = 32.6305401, 51.7238816
OUT = os.path.join(os.path.dirname(__file__), "..", "..", "architecture-plan", "geo")
os.makedirs(OUT, exist_ok=True)
UA = {"User-Agent": "arena-arch-plan/1.0 (site analysis; contact: repo owner)"}

def deg2num(lat, lon, z):
    xr = (lon + 180) / 360 * 2 ** z
    lr = math.radians(lat)
    yr = (1 - math.log(math.tan(lr) + 1 / math.cos(lr)) / math.pi) / 2 * 2 ** z
    return xr, yr

def get(url, binary=True, retries=4):
    last = None
    for i in range(retries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=40) as r:
                d = r.read()
            return d if binary else json.loads(d)
        except Exception as e:
            last = e
            time.sleep(2 + 3 * i)
    raise RuntimeError(f"GET failed {url[:90]}...: {last}")

meta = {"lat": LAT, "lon": LON, "zooms": {}}
for z in (16, 17, 18, 19):
    xf, yf = deg2num(LAT, LON, z)
    xc, yc = int(xf), int(yf)
    rx = 3 if z < 19 else 2
    ry = 3 if z < 19 else 3
    x0, x1 = xc - rx, xc + rx
    y0, y1 = yc - ry, yc + ry
    from PIL import Image
    W = (x1 - x0 + 1) * 256
    H = (y1 - y0 + 1) * 256
    canvas = Image.new("RGB", (W, H))
    n = 0
    for tx in range(x0, x1 + 1):
        for ty in range(y0, y1 + 1):
            url = f"https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{ty}/{tx}"
            data = get(url)
            tile = Image.open(io.BytesIO(data)).convert("RGB")
            canvas.paste(tile, ((tx - x0) * 256, (ty - y0) * 256))
            n += 1
    # مرز جغرافیایی کامل کانواس (مستطیل روی وب‌مرکاتور)
    def num2deg(xt, yt, zz):
        lon2 = xt / 2 ** zz * 360 - 180
        lat2 = math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * yt / 2 ** zz))))
        return lat2, lon2
    latN, lonW = num2deg(x0, y0, z)
    latS, lonE = num2deg(x1 + 1, y1 + 1, z)
    p = os.path.join(OUT, f"aerial_z{z}.jpg")
    canvas.save(p, quality=88)
    meta["zooms"][z] = {
        "file": f"aerial_z{z}.jpg", "w": W, "h": H,
        "north": latN, "south": latS, "west": lonW, "east": lonE,
        "tiles": n, "center_px": [ (xf - x0) * 256, (yf - y0) * 256 ],
    }
    print(f"z{z}: {n} tiles -> {p} ({W}x{H})  bounds SW({latS:.6f},{lonW:.6f}) NE({latN:.6f},{lonE:.6f})")

# ---- Overpass (خیابان + بنا، شعاع ۲۵۰ متر) ----
Q = ('[out:json][timeout:60];('
     'way["highway"](around:250,%.7f,%.7f);'
     'way["building"](around:250,%.7f,%.7f);'
     ');out geom tags;' % (LAT, LON, LAT, LON))
servers = [
    "https://overpass-api.de/api/interpreter",
    "https://overpass.kumi.systems/api/interpreter",
    "https://overpass.private.coffee/api/interpreter",
    "https://overpass.osm.jp/api/interpreter",
]
oj = None
for s in servers:
    try:
        oj = get(s + "?data=" + urllib.parse.quote(Q), binary=False)
        print("Overpass OK:", s, "| elements:", len(oj.get("elements", [])))
        break
    except Exception as e:
        print("Overpass fail:", s, e)
        time.sleep(3)
if oj:
    json.dump(oj, open(os.path.join(OUT, "overpass.json"), "w", encoding="utf-8"), ensure_ascii=False)
else:
    raise SystemExit("ALL OVERPASS SERVERS FAILED")

json.dump(meta, open(os.path.join(OUT, "meta.json"), "w"), indent=1)
print("ALL DONE")
