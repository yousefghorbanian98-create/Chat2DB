#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ورق‌های A3 برایِ هر دو طرحِ بازسازی‌شده (۳۰۰ DPI، هر طبقه یک ورق)."""
import os, sys, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from PIL import Image, ImageDraw, ImageFont
import plan_schemes as PS
from render_a3 import A3Sheet, LW, MM, A3W, A3H, OUT as A3ROOT

OUT1 = os.path.join(A3ROOT, "..", "A3-طرح-اول")
OUT2 = os.path.join(A3ROOT, "..", "A3-طرح-دوم")
os.makedirs(OUT1, exist_ok=True)
os.makedirs(OUT2, exist_ok=True)

BG = (252, 251, 247)


def new_sheet(title, sub, lvl, no, sd=125):
    mx0, my0, mx1, my1 = -3.2, PS.Y0 - 3.4, PS.LAND_W + 3.2, PS.LAND_D + 3.6
    return A3Sheet(title, sub, lvl, no, mx0, my0, mx1, my1, sd)


def land(sh):
    sh.rect(0, 0, PS.LAND_W, PS.LAND_D, fill=(250, 249, 245),
            outline=(120, 120, 120), w=2)
    sh.rect(0, 0, PS.LAND_W, PS.Y0, fill=(226, 240, 226), outline=(120, 170, 120), w=1)


def building_outline(sh):
    sh.rect(0, PS.Y0, PS.BLD_W, PS.Y1, fill=(255, 255, 255), outline=(90, 90, 90), w=2)
    for (x0, y0, x1, y1) in [(0, PS.Y0, PS.BLD_W, PS.Y0), (0, PS.Y1, PS.BLD_W, PS.Y1),
                             (0, PS.Y0, 0, PS.Y1), (PS.BLD_W, PS.Y0, PS.BLD_W, PS.Y1)]:
        sh.wall(x0, y0, x1, y1, 0.30)


def draw_floor(sh, kind):
    """kind: 'pilotis' | 'residential' | 'roof'"""
    building_outline(sh)
    cs = PS.cores(); cr = PS.corridor()
    for c in cs:
        sh.rect(c['x0'], c['y0'], c['x1'], c['y1'], fill=(244, 244, 250),
                outline=(90, 90, 90), w=1)
    sh.rect(cr['x0'], cr['y0'], cr['x1'], cr['y1'], fill=(248, 246, 240),
            outline=(170, 160, 140), w=1)
    if kind == 'residential':
        for u in PS.unit_boxes():
            sh.rect(u['x0'], u['y0'], u['x1'], u['y1'], fill=(255, 252, 244),
                    outline=(140, 140, 140), w=1)
            sh.rect(u['x0'], u['by0'], u['x1'], u['by1'], fill=(250, 244, 224),
                    outline=(170, 130, 40), w=1)
            cx = (u['x0'] + u['x1']) / 2
            sh.t_free(sh.M(cx, (u['y0'] + u['y1']) / 2 + 0.9), f"واحد {u['i']+1}",
                      size=13, fill=(40, 40, 40), bold=True, max_w=(u['w'] - 0.5) * sh.sc)
            sh.t_free(sh.M(cx, (u['y0'] + u['y1']) / 2 - 0.9), f"{u['area']:.1f} m²",
                      size=11, fill=(90, 90, 90), max_w=(u['w'] - 0.5) * sh.sc)
            sh.t_free(sh.M(cx, (u['by0'] + u['by1']) / 2), "ایوان", size=10,
                      fill=(130, 95, 25), max_w=(u['w'] - 0.5) * sh.sc)
            sh.window(u['x0'] + 0.8, u['by0'], u['x0'] + 2.8, u['by0'], 0.30)
    m = sh.M((cs[0]['x0'] + cs[0]['x1']) / 2, (cs[0]['y0'] + cs[0]['y1']) / 2)
    sh.t_free(m, "هسته\nپله و آسانسور", size=10, fill=(70, 70, 95))
    m = sh.M((cr['x0'] + cr['x1']) / 2, (cr['y0'] + cr['y1']) / 2)
    sh.t_free(m, f"راهرو {PS.CORR:.2f} m", size=10, fill=(120, 110, 85))


def draw_pilotis(sh, with_shops=False):
    building_outline(sh)
    if with_shops:
        for s in PS.shops(4):
            sh.rect(s['x0'], s['y0'], s['x1'], s['y1'], fill=(253, 243, 224),
                    outline=(165, 115, 45), w=1)
            cx = (s['x0'] + s['x1']) / 2
            sh.t_free(sh.M(cx, (s['y0'] + s['y1']) / 2 + 0.8), f"مغازه {s['i']+1}",
                      size=13, fill=(120, 80, 20), bold=True, max_w=(s['w'] - 0.6) * sh.sc)
            sh.t_free(sh.M(cx, (s['y0'] + s['y1']) / 2 - 0.9), f"{s['area']:.1f} m²",
                      size=11, fill=(120, 80, 20), max_w=(s['w'] - 0.6) * sh.sc)
            sh.window(s['x0'] + 1.2, s['y1'], s['x0'] + 3.6, s['y1'], 0.30)
        sh.rect(0, PS.Y0, PS.BLD_W, PS.Y1 - 6.0, fill=(255, 255, 255),
                outline=(150, 150, 150), w=1)
        sh.t_free(sh.M(PS.BLD_W / 2, PS.Y0 + 1.4), "انبار، تأسیسات و پارکینگِ سرپوشیده",
                  size=12, fill=(90, 90, 90))
    rows = PS.parking_rows()
    for r in rows:
        sh.rect(r['x0'], r['y0'], r['x1'], r['y1'], fill=(255, 255, 255),
                outline=(105, 135, 185), w=1)
        sh.t_free(sh.M((r['x0'] + r['x1']) / 2, (r['y0'] + r['y1']) / 2), str(r['n']),
                  size=11, fill=(90, 120, 170))
    cs = PS.cores()
    for c in cs:
        sh.rect(c['x0'], c['y0'], c['x1'], c['y1'], fill=(244, 244, 250),
                outline=(90, 90, 90), w=1)
    m = sh.M((cs[0]['x0'] + cs[0]['x1']) / 2, (cs[0]['y0'] + cs[0]['y1']) / 2)
    sh.t_free(m, "هسته", size=10, fill=(70, 70, 95))
    sh.rect(PS.BLD_W - 4.0, PS.Y0, PS.BLD_W, PS.Y0 + 5.6, fill=(246, 246, 240),
            outline=(150, 150, 150), w=1)
    sh.t_free(sh.M(PS.BLD_W - 2.0, PS.Y0 + 2.8), "رمپ", size=10, fill=(120, 120, 120))


def draw_roof(sh):
    building_outline(sh)
    sh.rect(0, PS.Y0, PS.BLD_W, PS.Y1, fill=(238, 238, 234), outline=(90, 90, 90), w=2)
    sh.t_free(sh.M(PS.BLD_W / 2, (PS.Y0 + PS.Y1) / 2 + 1.2), "بام", size=15,
              fill=(60, 60, 70), bold=True)
    sh.t_free(sh.M(PS.BLD_W / 2, (PS.Y0 + PS.Y1) / 2 - 1.0),
              "شیب ۱٪ به سمتِ آبروهایِ جنوبی", size=11, fill=(90, 90, 100))
    cs = PS.cores()
    sh.rect(cs[0]['x0'], cs[0]['y0'], cs[0]['x1'], cs[0]['y1'], fill=(246, 246, 250),
            outline=(90, 90, 90), w=2)
    sh.t_free(sh.M((cs[0]['x0'] + cs[0]['x1']) / 2, (cs[0]['y0'] + cs[0]['y1']) / 2),
              "اتاقکِ پله و آسانسور", size=10, fill=(70, 70, 90))
    for (x0, y0, x1, y1) in [(0, PS.Y0, PS.BLD_W, PS.Y0), (0, PS.Y1, PS.BLD_W, PS.Y1),
                             (0, PS.Y0, 0, PS.Y1), (PS.BLD_W, PS.Y0, PS.BLD_W, PS.Y1)]:
        sh.wall(x0, y0, x1, y1, 0.25, fill=(100, 100, 100))
    sh.t_free(sh.M(PS.BLD_W / 2, PS.Y1 + 1.0), "جان‌پناه ۱.۰۰ m", size=10,
              fill=(100, 100, 100))


def dims(sh):
    sh.dimh(0, PS.CORE_W, PS.Y0 - 1.0, f"{PS.CORE_W:.2f}")
    sh.dimh(PS.CORE_W, PS.BLD_W, PS.Y0 - 1.0, f"{PS.BLD_W-PS.CORE_W:.2f}")
    sh.dimh(0, PS.BLD_W, PS.Y0 - 2.2, f"{PS.BLD_W:.2f}")
    sh.dimh(0, PS.LAND_W, PS.Y0 - 3.0, f"{PS.LAND_W:.2f}")
    sh.dimv(0, PS.Y0, PS.LAND_W + 1.0, f"{PS.Y0:.2f}")
    sh.dimv(PS.Y0, PS.Y1, PS.LAND_W + 1.0, f"{PS.DEEP:.2f}")
    for i, x in enumerate([0, PS.BLD_W / 2, PS.BLD_W]):
        sh.axis(x, PS.LAND_D + 1.6, ["A", "B", "C"][i])


def sheet_pilotis(out, no, title, sub, lvl, with_shops):
    sh = new_sheet(title, sub, lvl, no)
    land(sh)
    draw_pilotis(sh, with_shops)
    dims(sh)
    sh.level_mark(-1.8, PS.Y1, lvl)
    sh.frame()
    s = PS.summary('shops' if with_shops else 'pilotis', nshop=(4 if with_shops else 0))
    sched = [("پارکینگ", f"{s['park_have']} فضا", "۲.۵۰×۵.۰۰"),
             ("هسته", f"{s['core']:.1f}", f"{PS.CORE_W:.2f}×{PS.CORE_D:.2f}"),
             ("راهرو", f"{s['corr']:.1f}", f"{PS.CORR:.2f} m عرض")]
    if with_shops:
        sched.insert(0, ("مغازه (۴ واحد)", f"{s['com']:.1f}", "۶.۰۰ m عمق"))
    sh.strip([("عنوان نقشه", title), ("تراز", lvl), ("مقیاس", f"۱:{sh.sd}"),
              ("شماره برگه", no), ("تاریخ", "۱۴۰۵/۰۶/۲۷"),
              ("زیربنای این سطح", f"{s['foot']:.1f} m²")], sched,
             [notes_block(s, with_shops)])
    return sh.save(os.path.join(out, f"A3-{no}.png"))


def sheet_typical(out, no, title, lvl, with_shops):
    sh = new_sheet(title, "طبقات ۱ تا ۳ — ۴ واحد در هر طبقه", lvl, no)
    land(sh)
    draw_floor(sh, 'residential')
    dims(sh)
    sh.level_mark(-1.8, PS.Y1, lvl)
    sh.frame()
    s = PS.summary('shops' if with_shops else 'pilotis', nshop=(4 if with_shops else 0))
    sched = [(f"واحد {u['i']+1}", f"{u['area']:.1f}", f"{u['w']:.2f}×{PS.ENC_D:.2f}")
             for u in PS.unit_boxes()]
    sched += [(f"ایوان {u['i']+1}", f"{u['barea']:.1f}", f"{u['w']:.2f}×{PS.BALC:.2f}")
              for u in PS.unit_boxes()[:2]]
    sched += [("هسته", f"{s['core']:.1f}", f"{PS.CORE_W:.2f}×{PS.CORE_D:.2f}"),
              ("راهرو", f"{s['corr']:.1f}", f"{PS.CORR:.2f} m")]
    sh.strip([("عنوان نقشه", title), ("تراز", lvl), ("مقیاس", f"۱:{sh.sd}"),
              ("شماره برگه", no), ("تاریخ", "۱۴۰۵/۰۶/۲۷"),
              ("زیربنای طبقه", f"{s['cnt_per_floor']:.1f} m²")], sched,
             [f"هر طبقه {PS.UPF} واحد · هر واحد {s['unit_area']:.1f} m² بسته + ایوان",
              f"تراکمِ کل {s['far']:.1f}٪ · مازاد بر ۱۸۰٪: {s['exc180']:.0f} m²",
              f"مجموعِ واحدها {s['units']} واحد · ارتفاع {s['height']:.2f} m"])
    return sh.save(os.path.join(out, f"A3-{no}.png"))


def sheet_roof(out, no, title, lvl, with_shops):
    sh = new_sheet(title, "عایق‌کاری، شیب‌بندی و جان‌پناه", lvl, no)
    land(sh)
    draw_roof(sh)
    dims(sh)
    sh.level_mark(-1.8, PS.Y1, lvl)
    sh.frame()
    s = PS.summary('shops' if with_shops else 'pilotis', nshop=(4 if with_shops else 0))
    sh.strip([("عنوان نقشه", title), ("تراز", lvl), ("مقیاس", f"۱:{sh.sd}"),
              ("شماره برگه", no), ("تاریخ", "۱۴۰۵/۰۶/۲۷"),
              ("ارتفاع کل", f"{s['height']:.2f} m")],
             [("بام", f"{PS.BLD_W*PS.DEEP:.1f}", f"{PS.BLD_W:.2f}×{PS.DEEP:.2f}"),
              ("اتاقکِ پله/آسانسور", f"{s['core']:.1f}", "—")],
             [f"ارتفاع تمام‌شده {s['height']:.2f} m",
              "موتورخانه و منبع با ارتفاعِ مفید زیر ۲.۲۰ ⇒ معاف از تراکم"])
    return sh.save(os.path.join(out, f"A3-{no}.png"))


def notes_block(s, with_shops):
    if with_shops:
        return (f"مغازه‌ها در نوارِ شمالی · پارکینگ در زیرزمین و فضایِ باز · "
                f"تراکم {s['far']:.1f}٪")
    return (f"پیلوت با ارتفاعِ مفید ۲.۶۰ m ⇒ معاف از تراکم · "
            f"{s['park_have']} فضایِ پارکینگ")


def build(out, prefix, with_shops):
    s = PS.summary('shops' if with_shops else 'pilotis', nshop=(4 if with_shops else 0))
    lv = PS.levels('shops' if with_shops else 'pilotis')
    p = []
    p.append(sheet_pilotis(out, f"{prefix}-۱",
                           "پلان همکف — مغازه" if with_shops else "پلان پیلوت — پارکینگ",
                           "تراز ۰.۰۰" if with_shops else "تراز ۰.۰۰", "±0.00", with_shops))
    p.append(sheet_typical(out, f"{prefix}-۲", "پلان طبقهٔ تیپ", f"{lv[1][1]:+.2f}", with_shops))
    p.append(sheet_roof(out, f"{prefix}-۳", "پلان بام", f"{lv[-1][1]:+.2f}", with_shops))
    from reportlab.lib.pagesizes import A3, landscape
    from reportlab.pdfgen import canvas as _c
    from reportlab.lib.utils import ImageReader
    W, H = landscape(A3)
    pdf = os.path.join(out, f"تمام-برگه‌ها-{prefix}.pdf")
    cv = _c.Canvas(pdf, pagesize=landscape(A3))
    cv.setTitle("پلان‌های A3")
    for f in p:
        cv.drawImage(ImageReader(f), 0, 0, width=W, height=H)
        cv.showPage()
    cv.save()
    for f in p:
        cv = _c.Canvas(f.replace(".png", ".pdf"), pagesize=landscape(A3))
        cv.drawImage(ImageReader(f), 0, 0, width=W, height=H)
        cv.showPage(); cv.save()
    print(f"  {os.path.basename(out)}: {len(p)} ورق + PDF")
    return p


if __name__ == "__main__":
    print("ساختِ ورق‌های A3 برایِ هر دو طرح:")
    build(OUT2, "دوم", False)
    build(OUT1, "اول", True)
