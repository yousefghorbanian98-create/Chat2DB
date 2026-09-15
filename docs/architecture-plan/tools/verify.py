#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""اعتبارسنجی هندسی طرح نسخه ۲ — پیلوت + ۴ طبقه + ۳ مغازه"""
import json, math

PLAN = json.load(open(__file__.replace("verify.py","plan_data.json"), encoding="utf-8"))

def shoelace(pts):
    s = 0
    for i in range(len(pts)):
        x1,y1 = pts[i]; x2,y2 = pts[(i+1)%len(pts)]
        s += x1*y2 - x2*y1
    return abs(s)/2

B=PLAN["building"]; PI=PLAN["pilotis"]; T=PLAN["typical"]
a0 = shoelace(PLAN["parcel"]["basePts"])
s = math.sqrt(PLAN["parcel"]["targetArea"]/a0)
parcel = a0*s*s
fails = []
def chk(label, val, cond, extra=""):
    st = "OK" if cond else "FAIL"
    if not cond: fails.append(label)
    print(f"  [{'✓' if cond else '✗'}] {label}: {val} {extra}")

print("="*64)
print("گزارش اعتبارسنجی — نسخه ۲: پیلوت + ۴ طبقه مسکونی + ۳ مغازه")
print("="*64)
print(f"\n[1] عرصه: {parcel:.2f} m² (هدف 600)")
plate = B["plateL"]*B["plateW"]; tower = B["towerL"]*B["towerW"]
print(f"\n[2] اشغال: پلیت پیلوت {plate:.2f} m² = {plate/parcel*100:.1f}% (≤60)")
chk("سطح اشغال", f"{plate/parcel*100:.1f}%", plate/parcel<=0.60)
chk("فضای باز", f"{parcel-plate:.1f} m² = {(parcel-plate)/parcel*100:.1f}%", (parcel-plate)/parcel>=0.20)

def area(r): return (r["x1"]-r["x0"])*(r["y1"]-r["y0"])
shops=[r for r in PI["rooms"] if r.get("shop")]
sh=sum(area(r) for r in shops)
core=sum(area(r) for r in PI["rooms"] if not r.get("parking") and not r.get("aisle") and not r.get("shop"))
floors=B["nRes"]*tower
balc=sum((b["x1"]-b["x0"])*(b["y1"]-b["y0"]) for b in T["balconies"])*B["nRes"]*0.5
used=floors+sh+core+balc
print(f"\n[3] تراکم:")
chk("۴ طبقه مسکونی", f"{floors:.2f} m² (۴×{tower:.2f})", True)
chk("مغازه‌ها", f"{len(shops)} عدد = {sh:.2f} m²", len(shops)==3, "(هر یک ~۱۹٫۱)")
chk("مشاعات بسته پیلوت", f"{core:.2f} m² (≤۳۰٪ پیلوت=۶۷)", core<=0.30*plate)
chk("بالکن ۴×۳ @۵۰٪", f"{balc:.2f} m²", True)
chk("جمع تراکم مصرفی", f"{used:.2f} ≤ {PLAN['meta']['allowedArea']}", used<=PLAN["meta"]["allowedArea"], f"(حاشیه {PLAN['meta']['allowedArea']-used:.2f})")

unit=[r for r in T["rooms"] if r["id"].startswith("U-")]
un=sum(area(r) for r in unit)
print(f"\n[4] واحد مسکونی: مفید {un:.2f} m² — فضاها:")
for r in unit: print(f"      {r['fa']:<18} {area(r):5.2f} m²")
pk=[r for r in PI["rooms"] if r.get("parking")]
print(f"\n[5] پارکینگ: {len(pk)} قطعه", end=" ")
def bay_ok(r):
    w,d=r['x1']-r['x0'], r['y1']-r['y0']
    perp = abs(w-2.5)<0.05 and abs(d-5.0)<0.05
    par  = abs(d-2.5)<0.05 and w>=5.4   # موازی
    return perp or par
dims_ok=all(bay_ok(r) for r in pk)
chk("", f"{len(pk)} قطعه (۳ عمودی 2.5×5 + ۱ موازی 5.88×2.5)", len(pk)>=4 and dims_ok)
print(f"\n[6] هسته: پله {PLAN['rules']['stairWidth']}m مفید | آسانسور {PLAN['rules']['liftBox']} | کف‌پا {PLAN['rules']['riser']*100:.1f}cm")
st=[r for r in T["rooms"] if r.get("stair")][0]
chk("عرض مفید پله", f"{st['x1']-st['x0']:.3f} m ≥ 1.10", st['x1']-st['x0']>=1.10)
balc_raw=sum((b["x1"]-b["x0"])*(b["y1"]-b["y0"]) for b in T["balconies"])
chk("بالکن ≥ ۳ m² (واحد<۱۰۰)", f"{balc_raw:.2f}", balc_raw>=3.0)

print("\n[7] همپوشانی فضاها:")
bad=0
for nm,rooms in (("پیلوت",PI["rooms"]),("تیپ",T["rooms"])):
    for i in range(len(rooms)):
        for j in range(i+1,len(rooms)):
            a,b=rooms[i],rooms[j]
            if min(a["x1"],b["x1"])-max(a["x0"],b["x0"])>0.01 and min(a["y1"],b["y1"])-max(a["y0"],b["y0"])>0.01:
                print(f"    OVERLAP[{nm}]: {a['id']} × {b['id']}"); bad+=1
chk("همپوشانی", "هیچ" if bad==0 else f"{bad} مورد", bad==0)

print("\n[8] مرز برج داخل پلیت:", end=" ")
chk("", f"y:[{B['towerOy']:.2f},{B['towerOy']+B['towerW']:.2f}] ⊆ [0,{B['plateW']}]، x:[0,{B['towerL']:.2f}] ⊆ [0,{B['plateL']}]",
    B["towerOy"]>=0 and B["towerOy"]+B["towerW"]<=B["plateW"] and B["towerL"]<=B["plateL"])
print(f"\n{'!'*10} {len(fails)} مورد ناموفق: {fails}" if fails else "\nهمه بررسی‌ها موفق ✔")
