#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""خروجی DXF نسخه ۲ — پیلوت + طبقه تیپ + سایت (لایه‌بندی معماری)"""
import json, math, os, ezdxf
from ezdxf import units

BASE = __file__.rsplit("/",1)[0]
PLAN = json.load(open(BASE+"/plan_data.json", encoding="utf-8"))
B=PLAN["building"]; PI=PLAN["pilotis"]; T=PLAN["typical"]

doc = ezdxf.new("R2018", setup=True)
doc.units = units.M
msp = doc.modelspace()
for name, color, lt in [("SITE",8,None),("WALL-EXT",7,None),("WALL-INT",8,None),
                        ("DOOR",3,None),("WINDOW",4,None),("ROOM-LABEL",1,None),
                        ("DIM",1,None),("PARKING",5,None),("STAIR",6,None),
                        ("SHOP",30,None),("BALCONY",30,"DASHED"),("SETBACK",90,"DASHED")]:
    if lt: doc.layers.add(name, color=color, linetype=lt)
    else: doc.layers.add(name, color=color)

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

def wall_dxf(w, layer, ox=0, oy=0):
    t=w["t"]
    if abs(w["x1"]-w["x0"])<1e-9:
        msp.add_lwpolyline([(ox+w["x0"]-t/2, oy+min(w["y0"],w["y1"])),(ox+w["x0"]+t/2, oy+min(w["y0"],w["y1"])),
                            (ox+w["x0"]+t/2, oy+max(w["y0"],w["y1"])),(ox+w["x0"]-t/2, oy+max(w["y0"],w["y1"]))], close=True, dxfattribs={"layer":layer})
    else:
        msp.add_lwpolyline([(ox+min(w["x0"],w["x1"]), oy+w["y0"]-t/2),(ox+max(w["x0"],w["x1"]), oy+w["y0"]-t/2),
                            (ox+max(w["x0"],w["x1"]), oy+w["y0"]+t/2),(ox+min(w["x0"],w["x1"]), oy+w["y0"]+t/2)], close=True, dxfattribs={"layer":layer})

def room_dxf(r, layer, ox=0):
    msp.add_lwpolyline([(ox+r["x0"],r["y0"]),(ox+r["x1"],r["y0"]),(ox+r["x1"],r["y1"]),(ox+r["x0"],r["y1"])], close=True, dxfattribs={"layer":layer})
    msp.add_text(f'{r["fa"]} ({(r["x1"]-r["x0"])*(r["y1"]-r["y0"]):.1f} m2)',
                 dxfattribs={"layer":"ROOM-LABEL","height":0.2}).set_placement((ox+(r["x0"]+r["x1"])/2-1.2,(r["y0"]+r["y1"])/2))

# ===== پیلوت در مبدأ =====
for r in PI["rooms"]:
    room_dxf(r, "SHOP" if r.get("shop") else "PARKING" if r.get("parking") else "ROOM-LABEL")
for w in build_walls(PI["rooms"], [dict(x0=0,y0=0,x1=B["plateL"],y1=0,t=B["wallExt"]),dict(x0=0,y0=B["plateW"],x1=B["plateL"],y1=B["plateW"],t=B["wallExt"]),
                                   dict(x0=0,y0=0,x1=0,y1=B["plateW"],t=B["wallExt"]),dict(x0=B["plateL"],y0=0,x1=B["plateL"],y1=B["plateW"],t=B["wallExt"])]):
    wall_dxf(w, "WALL-EXT" if w.get("ext") or w["t"]>0.2 else "WALL-INT")
for d in PI["doors"]: msp.add_line((d["x1"],d["y1"]),(d["x2"],d["y2"]), dxfattribs={"layer":"DOOR"})
for r in PI["rooms"]:
    if r.get("stair"):
        for i in range(11):
            y=r["y0"]+0.2+i*(r["y1"]-r["y0"]-0.4)/10
            msp.add_line((r["x0"]+0.05,y),(r["x1"]-0.05,y), dxfattribs={"layer":"STAIR"})
dim=msp.add_linear_dim(base=(0,-1.8), p1=(0,0), p2=(B["plateL"],0), dxfattribs={"layer":"DIM"}); dim.render()
dim=msp.add_linear_dim(base=(-1.8,0), p1=(0,0), p2=(0,B["plateW"]), angle=90, dxfattribs={"layer":"DIM"}); dim.render()

# ===== طبقه تیپ (جابجایی X=+25) =====
OXT=25.0; oyt=B["towerOy"]
roomsT=[{**r, "y0":r["y0"]+oyt, "y1":r["y1"]+oyt} for r in T["rooms"]]
for r in roomsT: room_dxf(r, "ROOM-LABEL", ox=OXT)
outerT=[dict(x0=0,y0=oyt,x1=B["towerL"],y1=oyt,t=B["wallExt"]),dict(x0=0,y0=oyt+B["towerW"],x1=B["towerL"],y1=oyt+B["towerW"],t=B["wallExt"]),
        dict(x0=0,y0=oyt,x1=0,y1=oyt+B["towerW"],t=B["wallExt"]),dict(x0=B["towerL"],y0=oyt,x1=B["towerL"],y1=oyt+B["towerW"],t=B["wallExt"])]
for w in build_walls(roomsT, outerT):
    wall_dxf(w, "WALL-EXT" if w.get("ext") or w["t"]>0.2 else "WALL-INT", ox=OXT)
for d in T["doors"]: msp.add_line((OXT+d["x1"],d["y1"]+oyt),(OXT+d["x2"],d["y2"]+oyt), dxfattribs={"layer":"DOOR"})
for r in roomsT:
    for win in r.get("win",[]):
        if win.get("door"): continue
        if win["s"]=="S": msp.add_line((OXT+win["a"],oyt),(OXT+win["b"],oyt), dxfattribs={"layer":"WINDOW"})
        if win["s"]=="N": msp.add_line((OXT+win["a"],oyt+B["towerW"]),(OXT+win["b"],oyt+B["towerW"]), dxfattribs={"layer":"WINDOW"})
        if win["s"]=="W": msp.add_line((OXT,oyt+win["a"]),(OXT,oyt+win["b"]), dxfattribs={"layer":"WINDOW"})
        if win["s"]=="E": msp.add_line((OXT+B["towerL"],oyt+win["a"]),(OXT+B["towerL"],oyt+win["b"]), dxfattribs={"layer":"WINDOW"})
for b in T["balconies"]:
    msp.add_lwpolyline([(OXT+b["x0"],b["y0"]+oyt),(OXT+b["x1"],b["y0"]+oyt),(OXT+b["x1"],b["y1"]+oyt),(OXT+b["x0"],b["y1"]+oyt)], close=True, dxfattribs={"layer":"BALCONY"})
for r in roomsT:
    if r.get("stair"):
        for i in range(11):
            y=r["y0"]+0.2+i*(r["y1"]-r["y0"]-0.4)/10
            msp.add_line((OXT+r["x0"]+0.05,y),(OXT+r["x1"]-0.05,y), dxfattribs={"layer":"STAIR"})

# ===== سایت (X=-40) =====
def shoelace(pts):
    s=0
    for i in range(len(pts)):
        x1,y1=pts[i]; x2,y2=pts[(i+1)%len(pts)]
        s+=x1*y2-x2*y1
    return abs(s)/2
a0=shoelace(PLAN["parcel"]["basePts"]); sc=math.sqrt(PLAN["parcel"]["targetArea"]/a0)
OXS=-40.0
pts=[(OXS+x*sc,y*sc) for x,y in PLAN["parcel"]["basePts"]]
msp.add_lwpolyline(pts, close=True, dxfattribs={"layer":"SITE"})
bx=[(OXS+B["ox"]+x,B["oy"]+y) for x,y in [(0,0),(B["plateL"],0),(B["plateL"],B["plateW"]),(0,B["plateW"])]]
msp.add_lwpolyline(bx, close=True, dxfattribs={"layer":"WALL-EXT"})
bt=[(OXS+B["ox"]+x,B["oy"]+B["towerOy"]+y) for x,y in [(0,0),(B["towerL"],0),(B["towerL"],B["towerW"]),(0,B["towerW"])]]
msp.add_lwpolyline(bt, close=True, dxfattribs={"layer":"WALL-EXT"})
# حریم ۶ متری شرقی (نمونه)
msp.add_lwpolyline([(OXS+B["ox"]+B["plateL"]+6.0, B["oy"]),(OXS+B["ox"]+B["plateL"]+6.0, B["oy"]+B["plateW"])], dxfattribs={"layer":"SETBACK"})
os.makedirs(BASE+"/../exports", exist_ok=True)
doc.saveas(BASE+"/../exports/plan.dxf")
print("DXF v2 saved:", os.path.getsize(BASE+"/../exports/plan.dxf"), "bytes")
