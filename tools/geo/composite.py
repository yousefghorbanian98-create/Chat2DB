#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ترکیب واقعیت: پلی‌گون ملک + جانمایی ساختمان + شبکه OSM
روی تصویر هوایی واقعی Esri (z19) — ژئورفرنس کامل
"""
import json, math, os
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display

ROOT = "/home/user/Chat2DB"
G = os.path.join(ROOT, "docs", "architecture-plan", "geo")
P = os.path.join(ROOT, "docs", "architecture-plan")

meta = json.load(open(G + "/meta.json"))
z19 = meta["zooms"]["19"]
im = Image.open(G + "/" + z19["file"]).convert("RGB")
W19, N19 = z19["west"], z19["north"]
LAT0, LON0 = meta["lat"], meta["lon"]

# متر بر پیکسل در z19 (وب‌مرکاتور در این عرض)
phi = math.radians(LAT0)
mpp = 156543.03392 * math.cos(phi) / 2**19          # ≈0.2515 m/px
DLAT = mpp / 111320.0                                # درجه/پیکسل
DLON = mpp / (111320.0 * math.cos(phi))

def geo2px(lat, lon):
    x = (lon - W19) / DLON
    y = (N19 - lat) / DLAT
    return x, y

def local2geo(xm, ym):  # متر از گوشه SW ملک
    sw_lat, sw_lon = 32.6303810, 51.7236610
    return sw_lat + ym * 9.0119e-6, sw_lon + xm * 1.05885e-5

# پلی‌گون ملک (متر از SW — بازسازی کاداستر مقیاس به ۶۰۰ m²)
PARCEL = [(0,0),(27.93,0),(32.44,9.01),(32.44,19.37),(4.50,19.37),(0,15.77)]
B = dict(ox=5.4, oy=4.2, plateL=18.6, plateW=12.0, towerL=9.7, towerW=11.5, towerOy=0.25)

cx, cy = geo2px(LAT0, LON0)
HALF = 240   # ±60 متر
box = (int(cx-HALF), int(cy-HALF), int(cx+HALF), int(cy+HALF))
crop = im.crop(box)
SC = 2.5
OW = int((box[2]-box[0])*SC); OH = int((box[3]-box[1])*SC)
canvas = crop.resize((OW, OH), Image.LANCZOS)
dr = ImageDraw.Draw(canvas, "RGBA")

def to_canvas(lat, lon):
    x, y = geo2px(lat, lon)
    return (x - box[0]) * SC, (y - box[1]) * SC

def L(xm, ym):
    return to_canvas(*local2geo(xm, ym))

# ---------- شبکه معابر OSM ----------
osm = json.load(open(G + "/overpass.json"))
for e in osm["elements"]:
    if "highway" not in e.get("tags", {}): continue
    hw = e["tags"]["highway"]
    wpx = {"secondary": 13, "secondary_link": 9, "residential": 6, "track": 4}.get(hw, 5)
    col = (250, 245, 225, 90) if hw.startswith("secondary") else (245, 240, 220, 60)
    pts = [to_canvas(g["lat"], g["lon"]) for g in e.get("geometry", [])]
    if len(pts) > 1:
        dr.line(pts, fill=col, width=int(wpx*SC*0.5))

# ---------- پلی‌گون ملک (قرمز) ----------
pp = [L(x, y) for x, y in PARCEL]
dr.polygon(pp, outline=(220, 30, 30, 255), width=6)
for p in pp:
    dr.ellipse([p[0]-7, p[1]-7, p[0]+7, p[1]+7], fill=(255, 210, 40, 255), outline=(120,0,0,255), width=2)

# ---------- حریم (خط‌چین سبز) ----------
def dashed(p1, p2, dash=16, gap=10, fill=(30,140,70,220), w=4):
    import math as m
    dx, dy = p2[0]-p1[0], p2[1]-p1[1]
    d = m.hypot(dx, dy); n = int(d // (dash+gap)) + 1
    for i in range(n):
        t0 = i*(dash+gap)/d; t1 = min((i*(dash+gap)+dash)/d, 1)
        if t0 >= 1: break
        dr.line([(p1[0]+dx*t0, p1[1]+dy*t0), (p1[0]+dx*t1, p1[1]+dy*t1)], fill=fill, width=w)
sb = dict(S=4.2, N=3.17, W=5.4, E=6.0)
corners = [L(B["ox"]-sb["W"], B["oy"]-sb["S"]), L(B["ox"]+B["plateL"]+sb["E"], B["oy"]-sb["S"]),
           L(B["ox"]+B["plateL"]+sb["E"], B["oy"]+B["plateW"]+sb["N"]), L(B["ox"]-sb["W"], B["oy"]+B["plateW"]+sb["N"])]
for i in range(4):
    dashed(corners[i], corners[(i+1)%4])

# ---------- پلیت پیلوت + برج (آبی) ----------
pl = [L(B["ox"],B["oy"]), L(B["ox"]+B["plateL"],B["oy"]), L(B["ox"]+B["plateL"],B["oy"]+B["plateW"]), L(B["ox"],B["oy"]+B["plateW"])]
dr.polygon(pl, fill=(40, 90, 200, 70), outline=(20, 60, 220, 255), width=6)
tw = [L(B["ox"],B["oy"]+B["towerOy"]), L(B["ox"]+B["towerL"],B["oy"]+B["towerOy"]),
      L(B["ox"]+B["towerL"],B["oy"]+B["towerOy"]+B["towerW"]), L(B["ox"],B["oy"]+B["towerOy"]+B["towerW"])]
dr.polygon(tw, fill=(250, 150, 20, 110), outline=(200, 90, 0, 255), width=6)

# ---------- متن ----------
def fnt(sz, bold=False):
    p = "/usr/share/fonts/truetype/dejavu/DejaVuSans%s.ttf" % ("-Bold" if bold else "")
    return ImageFont.truetype(p, sz)
def fa(t): return get_display(arabic_reshaper.reshape(t))

def label(x, y, txt, color=(255,255,255,255), sz=30, bg=(0,0,0,170), bold=True, anchor="mm"):
    f = fnt(sz, bold); t = fa(txt)
    bb = dr.textbbox((0,0), t, font=f)
    w, h = bb[2]-bb[0], bb[3]-bb[1]
    if anchor=="mm": x0, y0 = x-w/2-10, y-h/2-6
    else: x0, y0 = x+8, y-h/2-6
    dr.rounded_rectangle([x0, y0, x0+w+20, y0+h+12], radius=8, fill=bg)
    dr.text((x0+10, y0+4), t, font=f, fill=color)

lab_pilot_y = max(p[1] for p in pl) + 56

# ---------- ملک اولیه ~۱۳۰۰ m² و خط فشار قوی (اندازه‌گیری از تصویر واقعی) ----------
ORIG = [(-5.5,0),(39.0,0),(39.0,29.2),(-5.5,29.2)]
po = [L(x,y) for x,y in ORIG]
dr.polygon(po, outline=(160,90,20,255), width=5)
# خط انتقال: از دکل غربی (-7.9,24.2) به دکل شمالشرقی (37.1,28.9)
TW1, TW2 = (-7.9,24.2), (37.1,28.9)
import math as _m
ax_,ay_ = L(*TW1); bx_,by_ = L(*TW2)
dr.line([ (ax_,ay_),(bx_,by_) ], fill=(200,30,90,255), width=7)
# حریم دو طرف خط (۶ متر)
dxl, dyl = TW2[0]-TW1[0], TW2[1]-TW1[1]
dl = _m.hypot(dxl,dyl); nx_, ny_ = -dyl/dl, dxl/dl
for sgn in (1,-1):
    p1 = L(TW1[0]+nx_*6*sgn, TW1[1]+ny_*6*sgn)
    p2 = L(TW2[0]+nx_*6*sgn, TW2[1]+ny_*6*sgn)
    dashed(p1, p2, dash=12, gap=8, fill=(200,30,90,170), w=3)
# هاشور ناحیه غیرقابل استفاده (شمال حریم جنوبی تا شمال ملک)
zone = [(ORIG[0][0], TW1[1]-6),(ORIG[1][0], TW2[1]-6),(ORIG[1][0],ORIG[1][1]),(ORIG[0][0],ORIG[0][1])]
pz = [L(x,y) for x,y in zone]
dr.polygon(pz, fill=(200,30,90,42))
# علامت دکل‌ها
for twx, twy, lab in [(TW1[0],TW1[1],"دکل همسایه"),(TW2[0],TW2[1],"دکل فشار قوی")]:
    q = L(twx,twy)
    dr.line([(q[0]-14,q[1]-14),(q[0]+14,q[1]+14)], fill=(200,30,90,255), width=5)
    dr.line([(q[0]-14,q[1]+14),(q[0]+14,q[1]-14)], fill=(200,30,90,255), width=5)
_q=L(15,23.6); label(_q[0], _q[1], "≈ ۷۰۰ m² ازدست‌رفته: خط + حریم ۶ متری", (255,210,225), 23, bg=(120,10,50,215))
label((po[0][0]+po[2][0])/2 - 10, min(p[1] for p in po) - 26, "ملک اولیه ≈ ۱۳۰۰ m² (۴۴٫۵×۲۹٫۲)", (255,230,200), 26, bg=(90,45,0,200))
_q2=L(-6.5,6.4); label(_q2[0], _q2[1], "قابل‌ساخت ≈ ۶۰۰ m²", (210,255,215), 24, bg=(10,80,40,215), anchor="ml")
_qp=L(-6.5,15.6); label(_qp[0], _qp[1], "پیلوت: ۳ مغازه + ۴ پارکینگ", (225,240,255), 21, bg=(25,70,160,215), anchor="ml")
_qt=L(-6.5,11.2); label(_qt[0], _qt[1], "برج ۴ طبقه مسکونی", (255,240,220), 21, bg=(140,70,0,215), anchor="ml")
label((pp[0][0]+pp[1][0])/2, max(p[1] for p in pp) + 26, "۲۷٫۹۳", (255,225,225), 23)
label(max(p[0] for p in pp) + 42, (pp[2][1]+pp[3][1])/2, "۱۰٫۳۶", (255,225,225), 21, bg=(0,0,0,150))
label((pp[0][0]+pp[1][0])/2 + 60, (pp[1][1]+pp[2][1])/2 + 22, "۱۰٫۰۷", (255,225,225), 21, bg=(0,0,0,150))
label((pp[3][0]+pp[4][0])/2, min(p[1] for p in pp) - 18, "۲۷٫۹۳", (255,225,225), 23)
label((pp[4][0]+pp[5][0])/2 - 55, (pp[4][1]+pp[5][1])/2 - 12, "۵٫۷۷", (255,225,225), 20, bg=(0,0,0,150))
label(pp[5][0] - 40, (pp[5][1]+pp[0][1])/2, "۱۵٫۷۷", (255,225,225), 20, bg=(0,0,0,150))

# نوار مقیاس (۲۰ متر)
seg = 10 / mpp * SC  # ۱۰ متر به پیکسل
sb_x, sb_y = OW-2*seg-70, OH-56
for i in range(4):
    dr.rectangle([sb_x+i*seg/2, sb_y, sb_x+(i+1)*seg/2, sb_y+13], fill=((15,15,15,235) if i%2==0 else (255,255,255,235)))
dr.rectangle([sb_x, sb_y, sb_x+2*seg, sb_y+13], outline=(0,0,0,255), width=2)
dr.text((sb_x-4, sb_y-32), "0", font=fnt(22), fill=(255,255,255,255))
dr.text((sb_x+seg-14, sb_y-32), "10", font=fnt(22), fill=(255,255,255,255))
dr.text((sb_x+2*seg-10, sb_y-32), "20m", font=fnt(22), fill=(255,255,255,255))
# فلش شمال
nx, ny = 58, 128
dr.polygon([(nx,ny-52),(nx+16,ny+26),(nx,ny+12),(nx-16,ny+26)], fill=(255,60,60,235))
dr.text((nx-8, ny+34), "N", font=fnt(30, True), fill=(255,255,255,255))

# عنوان و اعتبار
t1 = fa("جانمایی واقعی — با خط فشار قوی و حریم آن")
t2 = "Esri World Imagery + OpenStreetMap | 32.6305401, 51.7238816"
f1, f2 = fnt(33, True), fnt(24)
w1 = dr.textbbox((0,0), t1, font=f1)[2]; w2 = dr.textbbox((0,0), t2, font=f2)[2]
bw = max(w1, w2) + 36
dr.rounded_rectangle([OW-bw-12, 10, OW-12, 96], radius=10, fill=(10, 20, 40, 205))
dr.text((OW-bw+6, 18), t1, font=f1, fill=(255,255,255,255))
dr.text((OW-bw+6, 60), t2, font=f2, fill=(190,215,250,255))

out = P + "/renders/geo-composite.png"
canvas.save(out)
print("saved", out, canvas.size)

# ---------- نسخه زمینه گسترده z18 ----------
z18 = meta["zooms"]["18"]
im18 = Image.open(G + "/" + z18["file"]).convert("RGB")
W18, N18 = z18["west"], z18["north"]
def geo2px18(lat, lon):
    dl18 = 156543.03392*math.cos(phi)/2**18 / 111320.0
    dn18 = 156543.03392*math.cos(phi)/2**18 / (111320.0*math.cos(phi))
    return (lon-W18)/dn18, (N18-lat)/dl18
cx18, cy18 = geo2px18(LAT0, LON0)
H18 = 400
box18 = (int(cx18-H18), int(cy18-H18), int(cx18+H18), int(cy18+H18))
crop18 = im18.crop(box18)
OW18 = 1300
SC18 = OW18/(box18[2]-box18[0])
canvas18 = crop18.resize((OW18, int((box18[3]-box18[1])*SC18)), Image.LANCZOS)
d2 = ImageDraw.Draw(canvas18, "RGBA")
def L18(xm, ym):
    la, lo = local2geo(xm, ym)
    x, y = geo2px18(la, lo)
    return (x-box18[0])*SC18, (y-box18[1])*SC18
p18 = [L18(x,y) for x,y in PARCEL]
d2.polygon(p18, outline=(220,30,30,255), width=5)
pl18 = [L18(B["ox"],B["oy"]), L18(B["ox"]+B["plateL"],B["oy"]), L18(B["ox"]+B["plateL"],B["oy"]+B["plateW"]), L18(B["ox"],B["oy"]+B["plateW"])]
d2.polygon(pl18, fill=(40,90,200,90), outline=(20,60,220,255), width=4)
d2.rounded_rectangle([10,10,OW18-10,86], radius=10, fill=(10,20,40,190))
d2.text((OW18-24-980, 20), fa("زمینه محله — کوی مصباح/دولت‌آباد اصفهان (Esri + OSM)"), font=fnt(32, True), fill=(255,255,255,255))
out18 = P + "/renders/geo-context.png"
canvas18.save(out18)
print("saved", out18, canvas18.size)
