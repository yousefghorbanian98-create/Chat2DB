#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""رندر PNG نسخه ۲ — سایت، پیلوت، طبقه تیپ، ایزومتریک"""
import json, math, os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mp

BASE = __file__.rsplit("/",1)[0]
PLAN = json.load(open(BASE+"/plan_data.json", encoding="utf-8"))
font_manager = plt.matplotlib.font_manager
try: font_manager.fontManager.addfont("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf")
except Exception: pass
plt.rcParams["font.family"] = ["DejaVu Sans"]
# matplotlib ≥3.11 شکل‌دهی فارسی را داخلی انجام می‌دهد — متن خام پاس می‌شود.
def fa(t): return t

B=PLAN["building"]; PI=PLAN["pilotis"]; T=PLAN["typical"]
os.makedirs(BASE+"/../renders", exist_ok=True)

def shoelace(pts):
    s=0
    for i in range(len(pts)):
        x1,y1=pts[i]; x2,y2=pts[(i+1)%len(pts)]
        s+=x1*y2-x2*y1
    return abs(s)/2
a0=shoelace(PLAN["parcel"]["basePts"]); sc=math.sqrt(PLAN["parcel"]["targetArea"]/a0)
PARCEL=[[x*sc,y*sc] for x,y in PLAN["parcel"]["basePts"]]

def build_walls(rooms, outer):
    walls=[dict(**o, ext=True) for o in outer]
    for i in range(len(rooms)):
        for j in range(i+1,len(rooms)):
            a,b=rooms[i],rooms[j]
            ov=max(a["y0"],b["y0"]), min(a["y1"],b["y1"])
            if ov[1]-ov[0]>0.3:
                for r,l in ((a["x1"],b["x0"]),(b["x1"],a["x0"])):
                    if abs(r-l)<=0.46: walls.append(dict(x0=(r+l)/2,y0=ov[0],x1=(r+l)/2,y1=ov[1],t=max(abs(r-l),0.1)))
            ov=(max(a["x0"],b["x0"]), min(a["x1"],b["x1"]))
            if ov[1]-ov[0]>0.3:
                for r,l in ((a["y1"],b["y0"]),(b["y1"],a["y0"])):
                    if abs(r-l)<=0.46: walls.append(dict(x0=ov[0],y0=(r+l)/2,x1=ov[1],y1=(r+l)/2,t=max(abs(r-l),0.1)))
    return walls

def draw_floor(ax, rooms, outer, doors, title, windows=False, cars=False):
    for r in rooms:
        c = "#fdeede" if r.get("shop") else "#e7ebef" if r.get("parking") else "#f6ead2" if (r.get("stair") or r.get("lift")) else "#fafaf7" if r.get("aisle") else "#f3f1ea"
        ax.add_patch(mp.Rectangle((r["x0"],r["y0"]), r["x1"]-r["x0"], r["y1"]-r["y0"], facecolor=c, edgecolor="#c9c3b6", lw=.6, zorder=1))
    for w in build_walls(rooms, outer):
        col="#3a414b" if w.get("ext") or w["t"]>0.2 else "#8a929c"
        if abs(w["x1"]-w["x0"])<1e-9:
            ax.add_patch(mp.Rectangle((w["x0"]-w["t"]/2, min(w["y0"],w["y1"])), w["t"], abs(w["y1"]-w["y0"]), facecolor=col, zorder=3))
        else:
            ax.add_patch(mp.Rectangle((min(w["x0"],w["x1"]), w["y0"]-w["t"]/2), abs(w["x1"]-w["x0"]), w["t"], facecolor=col, zorder=3))
    for d in doors:
        if d["t"]=="open":
            ax.plot([d["x1"],d["x2"]],[d["y1"],d["y2"]], color="#b06a2c", lw=2, ls=(0,(6,3)), zorder=5)
        else:
            ax.plot([d["x1"],d["x2"]],[d["y1"],d["y2"]], color="#fff", lw=6, zorder=4)
            ax.plot([d["x1"],d["x2"]],[d["y1"],d["y2"]], color="#7a3c14", lw=1, ls="--", zorder=5)
    if windows:
        for r in T["rooms"]:
            for win in r.get("win",[]):
                if win.get("door"): continue
                if win["s"]=="S": ax.plot([win["a"],win["b"]],[0.25,0.25], color="#3f83b0", lw=5, zorder=5)
                if win["s"]=="N": ax.plot([win["a"],win["b"]],[B["towerOy"]+B["towerW"],B["towerOy"]+B["towerW"]], color="#3f83b0", lw=5, zorder=5)
                if win["s"]=="W": ax.plot([0,0],[win["a"]+B["towerOy"],win["b"]+B["towerOy"]], color="#3f83b0", lw=5, zorder=5)
                if win["s"]=="E": ax.plot([B["towerL"],B["towerL"]],[win["a"]+B["towerOy"],win["b"]+B["towerOy"]], color="#3f83b0", lw=5, zorder=5)
        for b in T["balconies"]:
            ax.add_patch(mp.Rectangle((b["x0"],b["y0"]+B["towerOy"]), b["x1"]-b["x0"], b["y1"]-b["y0"], facecolor="#eef3f7", edgecolor="#9fb2c2", ls="--", zorder=2))
    if cars:
        for r in rooms:
            if r.get("parking"):
                cx,cy=(r["x0"]+r["x1"])/2,(r["y0"]+r["y1"])/2
                horiz=(r["y1"]-r["y0"])<(r["x1"]-r["x0"])
                car=mp.FancyBboxPatch((cx-(0.95 if horiz else 0.5), cy-(0.5 if horiz else 0.95)), 1.9 if horiz else 1.0, 1.0 if horiz else 1.9,
                                      boxstyle="round,pad=0.02,rounding_size=0.18", fc="none", ec="#5c7ea6", lw=1.1, zorder=2)
                ax.add_patch(car)
                ax.text(cx,cy,r["id"].replace("P",""),ha="center",va="center",fontsize=7,zorder=6)
    for r in rooms:
        if r.get("parking") or r.get("stair") or r.get("lift"): continue
        w=r["x1"]-r["x0"]; h=r["y1"]-r["y0"]
        ax.text((r["x0"]+r["x1"])/2,(r["y0"]+r["y1"])/2+(0.22 if not r.get("aisle") else 0), fa(r["fa"]), ha="center", fontsize=8 if w>2 else 6.5, weight="bold", zorder=6)
        if not r.get("aisle") and w>1.6:
            ax.text((r["x0"]+r["x1"])/2,(r["y0"]+r["y1"])/2-0.38, f"{w:.2f}×{h:.2f} — {w*h:.1f} m²", ha="center", fontsize=6.5, color="#5b6b7d", zorder=6)
    for r in rooms:
        if r.get("stair"):
            for i in range(11):
                y=r["y0"]+0.2+i*(r["y1"]-r["y0"]-0.4)/10
                ax.plot([r["x0"]+0.05,r["x1"]-0.05],[y,y], color="#666", lw=.7, zorder=2)
            ax.annotate("", xy=((r["x0"]+r["x1"])/2,r["y0"]+0.5), xytext=((r["x0"]+r["x1"])/2,r["y1"]-0.5), arrowprops=dict(arrowstyle="-|>", color="#c0392b"), zorder=6)
        if r.get("lift"):
            cx,cy=(r["x0"]+r["x1"])/2,(r["y0"]+r["y1"])/2
            ax.plot([cx-0.5,cx+0.5],[cy-0.4,cy+0.4], color="#20567c", lw=1.5, zorder=4)
            ax.plot([cx-0.5,cx+0.5],[cy+0.4,cy-0.4], color="#20567c", lw=1.5, zorder=4)

def plan_png(rooms, outer, doors, fname, title, xlim, ylim, windows=False, cars=False, label=None):
    fig,ax=plt.subplots(figsize=(13.5,9), dpi=150)
    draw_floor(ax, rooms, outer, doors, title, windows, cars)
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.set_aspect("equal")
    ax.set_title(fa(title), fontsize=13, weight="bold", pad=12)
    if label:
        ax.text(0.99,0.01,label, transform=ax.transAxes, ha="right", fontsize=9, color="#7d8b99")
    ax.axis("off")
    fig.tight_layout(); fig.savefig(BASE+"/../renders/"+fname, bbox_inches="tight"); plt.close(fig)

# پیلوت
outerP=[dict(x0=0,y0=0,x1=B["plateL"],y1=0,t=B["wallExt"]),dict(x0=0,y0=B["plateW"],x1=B["plateL"],y1=B["plateW"],t=B["wallExt"]),
        dict(x0=0,y0=0,x1=0,y1=B["plateW"],t=B["wallExt"]),dict(x0=B["plateL"],y0=0,x1=B["plateL"],y1=B["plateW"],t=B["wallExt"])]
plan_png(PI["rooms"], outerP, PI["doors"], "plan-pilotis.png",
         "پلان پیلوت (همکف) — ۳ مغازه + پارکینگ ۴ خودرو + مشاعات — اشغال ۲۲۳٫۲۰ m²",
         (-2.2,20.8), (-2.6,14.4), cars=True, label="ویترین مغازه‌ها رو به شرق (معبر ۲۴ متری) — ورود خودرو از جنوب، ورود پیاده از شمال")
# تیپ
oyt=B["towerOy"]
outerT=[dict(x0=0,y0=oyt,x1=B["towerL"],y1=oyt,t=B["wallExt"]),dict(x0=0,y0=oyt+B["towerW"],x1=B["towerL"],y1=oyt+B["towerW"],t=B["wallExt"]),
        dict(x0=0,y0=oyt,x1=0,y1=oyt+B["towerW"],t=B["wallExt"]),dict(x0=B["towerL"],y0=oyt,x1=B["towerL"],y1=oyt+B["towerW"],t=B["wallExt"])]
doorsT=[dict(d) for d in T["doors"]]
for d in doorsT: d["y1"]+=oyt; d["y2"]+=oyt
roomsT=[dict(r) for r in T["rooms"]]
for r in roomsT: r["y0"]+=oyt; r["y1"]+=oyt
plan_png(roomsT, outerT, doorsT, "plan-typical.png",
         "پلان تیپ طبقات ۱ تا ۴ — واحد ۲ خوابه ۷۰٫۵ m² + پله/آسانسور — ۱۱۱٫۵۵ m²",
         (-2.2,12.2), (-2.2,14.2), windows=True, label="۴ طبقه یکسان — بالکن ۳ m² رو به جنوب")

# ---- سایت ----
fig,ax=plt.subplots(figsize=(13.5,10), dpi=150)
ax.add_patch(mp.Polygon(PARCEL, closed=True, facecolor="#f4efe4", edgecolor="#7a5c3a", lw=2.4))
ax.add_patch(mp.Polygon(PARCEL, closed=True, facecolor="none", edgecolor="#b49a78", hatch="///", lw=0))
ax.add_patch(mp.Rectangle((B["ox"],B["oy"]), B["plateL"], B["plateW"], facecolor="#efe9db", edgecolor="#273444", lw=2, ls=(0,(9,4)), zorder=3))
ax.add_patch(mp.Rectangle((B["ox"],B["oy"]+B["towerOy"]), B["towerL"], B["towerW"], facecolor="#e9e3d5", edgecolor="#273444", lw=2.5, zorder=4))
ax.text(B["ox"]+B["plateL"]/2, B["oy"]+B["plateW"]+0.35, "پیلوت ۱۸٫۶۰×۱۲٫۰۰ = ۲۲۳٫۲۰ m² (۳۷٫۲٪)", fontsize=10, weight="bold", ha="center", zorder=6)
ax.text(B["ox"]+B["towerL"]/2, B["oy"]+B["towerOy"]+B["towerW"]/2+0.3, "برج ۴ طبقه", fontsize=10, weight="bold", ha="center", zorder=6)
ax.text(B["ox"]+B["towerL"]/2, B["oy"]+B["towerOy"]+B["towerW"]/2-0.4, "۹٫۷۰×۱۱٫۵۰", fontsize=8, ha="center", zorder=6)
ax.text(B["ox"]+B["plateL"]-2.7, B["oy"]+2, "۳ مغازه", fontsize=9, ha="center", zorder=6, style="italic")
ax.text(B["ox"]+B["plateL"]-2.7, B["oy"]+6, "۳ مغازه", fontsize=9, ha="center", zorder=6, style="italic")
ax.text(B["ox"]+B["plateL"]-2.7, B["oy"]+10, "۳ مغازه", fontsize=9, ha="center", zorder=6, style="italic")
xmax=max(p[0] for p in PARCEL); ymax=max(p[1] for p in PARCEL)
ax.add_patch(mp.Rectangle((xmax,0), 7, ymax, facecolor="#dde3e9", zorder=0))
ax.add_patch(mp.Rectangle((-6,ymax), xmax+6, 6, facecolor="#dde3e9", zorder=0))
ax.add_patch(mp.Rectangle((-6,-6), xmax+6, 6, facecolor="#dde3e9", zorder=0))
ax.text(xmax+3.5, ymax/2, "معبر اصلی ۲۴ متری", rotation=90, ha="center", va="center", fontsize=10)
ax.text(xmax/2, ymax+3, "کوی ۸ متری شمالی — ورودی پیاده ساکنین", ha="center", fontsize=10)
ax.text(xmax/2, -3, "کوی ۸ متری جنوبی — ورود خودرو به پیلوت", ha="center", fontsize=10)
ax.annotate("", xy=(B["ox"]+3.4, B["oy"]+0.2), xytext=(B["ox"]+3.4, B["oy"]-1.6), arrowprops=dict(arrowstyle="-|>", color="#1d7a46", lw=1.6), zorder=6)
ax.annotate("", xy=(B["ox"]+11.1, B["oy"]+B["plateW"]+0.2), xytext=(B["ox"]+11.1, B["oy"]+B["plateW"]+1.8), arrowprops=dict(arrowstyle="-|>", color="#20567c", lw=1.6), zorder=6)
for i in range(len(PARCEL)):
    p,q=PARCEL[i],PARCEL[(i+1)%len(PARCEL)]
    mx,my=(p[0]+q[0])/2,(p[1]+q[1])/2
    dx,dy=q[0]-p[0],q[1]-p[1]; L=math.hypot(dx,dy)
    ax.text(mx+dy/L*1.1, my-dx/L*1.1, f"{L:.2f}", fontsize=10, color="#8c2f21", ha="center", weight="bold")
ax.text(1.5,ymax-1.5, "عرصه: ۶۰۰٫۰۰ m²  |  اشغال ۳۷٫۲٪  |  تراکم مصرفی ۵۳۵٫۵ از ۵۴۲٫۳۸", fontsize=11, weight="bold",
        bbox=dict(facecolor="white", edgecolor="#273444"))
ax.set_xlim(-7,xmax+9); ax.set_ylim(-7,ymax+7); ax.set_aspect("equal"); ax.axis("off")
ax.set_title("پلان سایت — مجتمع مسکونی-تجاری: پیلوت + ۴ طبقه + ۳ مغازه", fontsize=13, weight="bold")
fig.tight_layout(); fig.savefig(BASE+"/../renders/site.png", bbox_inches="tight"); plt.close(fig)

# ---- ایزومتریک ----
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
def box_faces(x,y,z,w,d,h):
    x2,y2,z2=x+w,y+d,z+h
    return [[(x,y,z),(x2,y,z),(x2,y2,z),(x,y2,z)],[(x,y,z2),(x2,y,z2),(x2,y2,z2),(x,y2,z2)],
            [(x,y,z),(x2,y,z),(x2,y,z2),(x,y,z2)],[(x,y2,z),(x2,y2,z),(x2,y2,z2),(x,y2,z2)],
            [(x,y,z),(x,y2,z),(x,y2,z2),(x,y,z2)],[(x2,y,z),(x2,y2,z),(x2,y2,z2),(x2,y,z2)]]
fig=plt.figure(figsize=(15,10.5), dpi=140)
ax=fig.add_subplot(111, projection="3d")
ax.add_collection3d(Poly3DCollection([[(p[0],-p[1],-0.08) for p in PARCEL]], facecolor="#b8c9a3", edgecolor="#7a5c3a", lw=1.5))
OX,OZ=B["ox"],-B["oy"]; PL,PW=B["plateL"],B["plateW"]; TL,TW=B["towerL"],B["towerW"]; FH=B["floorH"]
# کف و ستون‌های پیلوت
ax.add_collection3d(Poly3DCollection(box_faces(OX-0.25,OZ-0.25,0.0,PL+0.5,PW+0.5,0.12), facecolor="#c9c2b6", edgecolor="#b9b2a6", lw=.1))
for cx in (0.45,4.8,12.85,15.4,18.15):
    for cy in (0.45,6.0,11.55):
        ax.add_collection3d(Poly3DCollection(box_faces(OX+cx-0.2,OZ-cy-0.2,0.12,0.4,0.4,2.88), facecolor="#bfb8ac", edgecolor="#a8a196", lw=.1))
# مغازه‌ها
for r in PI["rooms"]:
    if r.get("shop"):
        ax.add_collection3d(Poly3DCollection(box_faces(OX+r["x0"],OZ-r["y1"],0.12,r["x1"]-r["x0"],r["y1"]-r["y0"],2.7), facecolor=(0.99,0.93,0.87,0.92), edgecolor="#8a7a62", lw=.3))
# هسته
ax.add_collection3d(Poly3DCollection(box_faces(OX+6.85,OZ-11.825,0.12,2.85,11.65,2.88), facecolor=(0.94,0.85,0.72,0.95), edgecolor="#c9a86a", lw=.3))
# ۴ طبقه — لبه دال‌ها + شیشه نما (فقط دو ضلع برای حفظ دید داخلی)
walls=build_walls(roomsT, outerT)
for i in range(4):
    z0=FH*(i+1)
    # لبه دال
    for f in (box_faces(OX-0.25,OZ-B["towerOy"]-0.25,z0-0.2,TL+0.5,0.24,0.2),
              box_faces(OX-0.25,OZ-B["towerOy"]+TW+0.01,z0-0.2,TL+0.5,0.24,0.2),
              box_faces(OX-0.25,OZ-B["towerOy"],z0-0.2,0.24,TW+0.25,0.2),
              box_faces(OX+TL+0.01,OZ-B["towerOy"],z0-0.2,0.24,TW+0.25,0.2)):
        ax.add_collection3d(Poly3DCollection(f, facecolor="#c9c2b6", edgecolor="#a8a196", lw=.2))
    # شیشه جنوبی و غربی (شفاف)
    ax.add_collection3d(Poly3DCollection(box_faces(OX,OZ-B["towerOy"]-0.09,z0,TL,0.09,2.8), facecolor=(0.55,0.72,0.86,0.18), edgecolor="#8fb4cc", lw=.15))
    ax.add_collection3d(Poly3DCollection(box_faces(OX-0.09,OZ-B["towerOy"],z0,0.09,TW,2.8), facecolor=(0.55,0.72,0.86,0.18), edgecolor="#8fb4cc", lw=.15))
# دیوارهای داخلی طبقه اول
for wl in walls:
    t=max(wl["t"],0.1)
    if abs(wl["x1"]-wl["x0"])<1e-9:
        fs=box_faces(OX+wl["x0"]-t/2, OZ-wl["y1"], FH+0.2, t, wl["y1"]-wl["y0"], 2.7)
    else:
        fs=box_faces(OX+min(wl["x0"],wl["x1"]), OZ-wl["y1"], FH+0.2, wl["x1"]-wl["x0"], t, 2.7)
    ax.add_collection3d(Poly3DCollection(fs, facecolor=(0.86,0.84,0.80,0.62), edgecolor="#b5ada0", lw=.12))
# جان‌پناه بام
zt=FH*5
for f in (box_faces(OX-0.25,OZ-B["towerOy"]-0.25,zt,TL+0.5,0.16,0.8), box_faces(OX-0.25,OZ-B["towerOy"]+TW+0.09,zt,TL+0.5,0.16,0.8),
          box_faces(OX-0.25,OZ-B["towerOy"],zt,0.16,TW+0.25,0.8), box_faces(OX+TL+0.09,OZ-B["towerOy"],zt,0.16,TW+0.25,0.8)):
    ax.add_collection3d(Poly3DCollection(f, facecolor=(0.85,0.83,0.79,0.6), edgecolor="#b0a89c", lw=.2))
ax.text(OX+PL+1.2, OZ-4.0, 1.9, "پیلوت: ۳ مغازه + ۴ پارکینگ", fontsize=8.5)
ax.text(OX+TL+1.4, OZ-B["towerOy"]-TW/2, FH*2.5+1, "۴ طبقه مسکونی (هر طبقه ۱ واحد)", fontsize=9)
ax.set_xlim(2,32); ax.set_ylim(-18,4); ax.set_zlim(-1.2,16.5)
ax.set_box_aspect((30,22,17.7))
ax.view_init(elev=24, azim=-119)
ax.set_title("نمای ایزومتریک — پیلوت (مغازه+پارکینگ) + ۴ طبقه مسکونی — ۱۵٫۸ متر", fontsize=12.5, weight="bold", pad=2)
ax.axis("off")
fig.tight_layout(); fig.savefig(BASE+"/../renders/iso3d.png", bbox_inches="tight"); plt.close(fig)
print("renders OK:", sorted(os.listdir(BASE+"/../renders")))
