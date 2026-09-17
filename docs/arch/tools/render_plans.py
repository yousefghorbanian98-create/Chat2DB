#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ترسیمِ پلان‌های مهندسیِ هر طبقه — خروجی: docs/arch/plan-*.png
مقیاس، کادرِ ترسیم، ابعاد، محورها، در و پنجره، پله، مبلمان و تأسیساتِ بهداشتی.
"""
import os, math, json
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display
import plan_model as PM

HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUTDIR = os.path.join(HERE, "docs", "arch")
FDIR = "/home/user/fonts"
SW, SH = 1680, 1180

P = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")
_c = {}


def fa(t):
    return get_display(arabic_reshaper.reshape(str(t).translate(P)))


def F(sz, bold=False):
    k = (sz, bold)
    if k not in _c:
        _c[k] = ImageFont.truetype(os.path.join(FDIR, "Vazirmatn-Bold.ttf" if bold else
                                                "Vazirmatn-Regular.ttf"), sz)
    return _c[k]


class Sheet:
    def __init__(self, title, subtitle, level, sheet_no, model_x0, model_y0, model_x1, model_y1):
        self.img = Image.new("RGB", (SW, SH), (252, 251, 247))
        self.d = ImageDraw.Draw(self.img)
        self.title, self.sub, self.lvl, self.no = title, subtitle, level, sheet_no
        mg = 150
        sx = (SW - 2 * mg) / (model_x1 - model_x0)
        sy = (SH - 2 * mg - 60) / (model_y1 - model_y0)
        self.sc = min(sx, sy)
        self.ox = mg + ((SW - 2 * mg) - (model_x1 - model_x0) * self.sc) / 2
        self.oy = SH - mg - 40 + (model_y1 - model_y0 - (model_y1 - 0)) * 0
        self.oy = SH - mg - 40
        self.my0 = model_y0

    def M(self, x, y):
        return (self.ox + (x) * self.sc, self.oy - (y - self.my0) * self.sc)

    def t(self, xy, s, size=14, fill=(40, 40, 40), bold=False, anchor="mm", bg=None, rot=0):
        if rot:
            tmp = Image.new("RGBA", (400, 120), (0, 0, 0, 0))
            td = ImageDraw.Draw(tmp)
            f = F(size, bold)
            td.text((200, 60), fa(s), font=f, fill=fill + (255,), anchor="mm")
            tmp = tmp.rotate(rot, expand=True, resample=Image.BICUBIC)
            bx, by = int(xy[0]), int(xy[1])
            self.img.paste(tmp, (bx - tmp.width // 2, by - tmp.height // 2), tmp)
            return
        f = F(size, bold)
        s2 = fa(s)
        if bg:
            b = self.d.textbbox(xy, s2, font=f, anchor=anchor)
            self.d.rectangle([b[0] - 4, b[1] - 2, b[2] + 4, b[3] + 2], fill=bg)
        self.d.text(xy, s2, font=f, fill=fill, anchor=anchor)

    def rect(self, x0, y0, x1, y1, fill=None, outline=None, w=1):
        a, b = self.M(x0, y1), self.M(x1, y0)
        self.d.rectangle([a[0], a[1], b[0], b[1]], fill=fill, outline=outline, width=w)

    def line(self, pts, fill=(40, 40, 40), w=1):
        self.d.line([self.M(*p) for p in pts], fill=fill, width=w)

    # ------------------------------------------------------------ دیوار
    def wall(self, x0, y0, x1, y1, t=PM.T_INT, fill=(58, 58, 58)):
        if abs(x1 - x0) > abs(y1 - y0):
            self.rect(x0, y0 - t / 2, x1, y1 + t / 2, fill=fill)
        else:
            self.rect(x0 - t / 2, y0, x1 + t / 2, y1, fill=fill)

    # ------------------------------------------------------------ در
    def door(self, x0, y0, x1, y1, swing, leaf=True):
        """swing: بردارِ جهتِ بازشو به سمتِ داخلِ اتاق"""
        horiz = abs(x1 - x0) > abs(y1 - y0)
        r = abs(x1 - x0) if horiz else abs(y1 - y0)
        if horiz:
            self.rect(x0, y0 - 0.20, x1, y1 + 0.20, fill=(252, 251, 247))
            if leaf:
                if swing[1] > 0:
                    self.line([(x0, y0), (x0, y0 + r)], w=2)
                    self.qarc(x0, y0, r, 90, 0)
                else:
                    self.line([(x0, y0), (x0, y0 - r)], w=2)
                    self.qarc(x0, y0, r, 270, 360)
        else:
            self.rect(x0 - 0.20, y0, x1 + 0.20, y1, fill=(252, 251, 247))
            if leaf:
                if swing[0] > 0:
                    self.line([(x0, y0), (x0 + r, y0)], w=2)
                    self.qarc(x0, y0, r, 0, 90)
                else:
                    self.line([(x0, y0), (x0 - r, y0)], w=2)
                    self.qarc(x0, y0, r, 180, 90)

    def qarc(self, cx, cy, r, a0, a1):
        """کمان به‌صورتِ پلی‌لاین — بدونِ ابهام در جهتِ زاویه"""
        pts = []
        for i in range(19):
            a = math.radians(a0 + (a1 - a0) * i / 18)
            pts.append(self.M(cx + r * math.cos(a), cy + r * math.sin(a)))
        self.d.line(pts, fill=(40, 40, 40), width=1)

    def opening(self, x0, y0, x1, y1):
        if abs(x1 - x0) > abs(y1 - y0):
            self.rect(x0, y0 - 0.20, x1, y1 + 0.20, fill=(252, 251, 247))
        else:
            self.rect(x0 - 0.20, y0, x1 + 0.20, y1, fill=(252, 251, 247))

    # ------------------------------------------------------------ پنجره
    def window(self, x0, y0, x1, y1, t=PM.T_EXT):
        if abs(x1 - x0) > abs(y1 - y0):
            for o in (-t / 2, 0, t / 2):
                self.line([(x0, y0 + o), (x1, y1 + o)], fill=(210, 235, 245), w=2)
            self.rect(x0, y0 - t / 2, x1, y1 + t / 2, outline=(120, 150, 165), w=1)
        else:
            for o in (-t / 2, 0, t / 2):
                self.line([(x0 + o, y0), (x1 + o, y1)], fill=(210, 235, 245), w=2)
            self.rect(x0 - t / 2, y0, x1 + t / 2, y1, outline=(120, 150, 165), w=1)

    # ------------------------------------------------------------ ابعاد
    def dimh(self, x0, x1, y, label=None, off=0.0):
        yy = y - off
        self.line([(x0, yy), (x1, yy)], fill=(190, 70, 70), w=1)
        for xx in (x0, x1):
            self.line([(xx, yy - 0.18), (xx, yy + 0.18)], fill=(190, 70, 70), w=1)
        m = self.M((x0 + x1) / 2, yy)
        self.t((m[0], m[1] - 11), label or f"{abs(x1-x0):.2f}", size=12, fill=(170, 55, 55),
               bg=(252, 251, 247))

    def dimv(self, y0, y1, x, label=None, off=0.0):
        xx = x - off
        self.line([(xx, y0), (xx, y1)], fill=(190, 70, 70), w=1)
        for yy in (y0, y1):
            self.line([(xx - 0.18, yy), (xx + 0.18, yy)], fill=(190, 70, 70), w=1)
        m = self.M(xx, (y0 + y1) / 2)
        self.t((m[0] - 12, m[1]), label or f"{abs(y1-y0):.2f}", size=12, fill=(170, 55, 55),
               bg=(252, 251, 247), rot=90)

    def axis(self, x, y, name):
        """محور با دایره و نام"""
        cx, cy = self.M(x, y)
        self.d.line([(cx, cy), (cx, cy - 46)], fill=(90, 120, 170), width=1)
        self.d.ellipse([cx - 13, cy - 59, cx + 13, cy - 33], fill=(252, 251, 247),
                       outline=(90, 120, 170), width=1)
        self.t((cx, cy - 46), name, size=11, fill=(60, 90, 140), bold=True)

    # ------------------------------------------------------------ کادر
    def frame(self, notes=(), scale_text=""):
        self.d.rectangle([14, 14, SW - 14, SH - 14], outline=(70, 70, 70), width=2)
        self.d.rectangle([24, 24, SW - 24, SH - 24], outline=(70, 70, 70), width=1)
        # کادرِ ترسیم
        bx, by, bw, bh = SW - 560, SH - 150, 536, 122
        self.d.rectangle([bx, by, bx + bw, by + bh], fill=(252, 251, 247), outline=(70, 70, 70), width=2)
        self.d.line([(bx, by + 38), (bx + bw, by + 38)], fill=(70, 70, 70), width=1)
        self.d.line([(bx, by + 78), (bx + bw, by + 78)], fill=(70, 70, 70), width=1)
        self.d.line([(bx + 300, by + 38), (bx + 300, by + bh)], fill=(70, 70, 70), width=1)
        self.t((bx + 12, by + 19), "پروژه: مجتمعِ مسکونی-تجاری — زمینِ ۵۴۲٫۳۸ m²، اصفهان",
               size=13, fill=(30, 30, 30), anchor="lm", bold=True)
        self.t((bx + 12, by + 58), f"عنوانِ نقشه: {self.title}", size=13, fill=(30, 30, 30), anchor="lm")
        self.t((bx + 312, by + 58), f"تراز: {self.lvl}", size=13, fill=(30, 30, 30), anchor="lm")
        self.t((bx + 12, by + 100), f"مقیاس {scale_text}", size=13, fill=(30, 30, 30), anchor="lm")
        self.t((bx + 312, by + 100), f"شمارهٔ برگه: {self.no}", size=13, fill=(30, 30, 30), anchor="lm")
        # قطب‌نما
        nx, ny = 90, SH - 110
        self.d.ellipse([nx - 26, ny - 26, nx + 26, ny + 26], outline=(70, 70, 70), width=1)
        self.d.polygon([(nx, ny - 22), (nx - 8, ny + 14), (nx, ny + 6), (nx + 8, ny + 14)],
                       fill=(60, 60, 60))
        self.t((nx, ny - 36), "شمال", size=12, fill=(50, 50, 50))
        # مقیاسِ خطی
        sx, sy = 190, SH - 90
        for i in range(4):
            self.d.rectangle([sx + i * 40, sy, sx + i * 40 + 40, sy + 9],
                             fill=(60, 60, 60) if i % 2 == 0 else (252, 251, 247), outline=(60, 60, 60))
        self.t((sx, sy - 12), "۰", size=11, anchor="lm")
        self.t((sx + 160, sy - 12), "۱۰ متر", size=11, anchor="lm")
        # یادداشت‌ها
        ny2 = SH - 150
        for i, n in enumerate(notes):
            self.t((36, ny2 - (len(notes) - i) * 22), n, size=12, fill=(70, 70, 70), anchor="lm")

    def save(self, path):
        self.img.save(path)
        print("ذخیره:", os.path.basename(path))


# ================================================================ واحد
def draw_unit_shell(sh, offx, mirror=False):
    """اتاق‌ها و دیوارهایِ داخلیِ یک واحد"""
    UWX = PM.UW
    def X(x):
        return offx + (UWX - x if mirror else x)
    def XP(a, b):
        return (X(a), X(b)) if not mirror else (X(a), X(b))

    rooms = PM.mirrored_rooms(offx) if mirror else PM.unit_rooms(offx)
    for r in rooms:
        sh.rect(r["x0"], r["y0"], r["x1"], r["y1"], fill=PM.ROOM_COLOR[r["key"]], outline=(150, 150, 150))
    y0, y1 = PM.ENC_Y0, PM.ENC_Y1

    # دیوارهای داخلی
    lw = [("V", 6.56, 0.00, 3.83), ("H", 0.00, 3.83, UWX), ("V", 1.39, 3.83, 5.57),
          ("V", 3.99, 3.83, 5.57), ("H", 0.00, 5.57, UWX), ("V", 5.14, 5.57, 8.30)]
    for kind, a, b1, b2 in lw:
        if kind == "V":
            xa, xb = XP(a, a)
            sh.wall(min(X(a), X(a)), y0 + b1, min(X(a), X(a)), y0 + b2, PM.T_INT)
        else:
            sh.wall(min(X(b1), X(b2)), y0 + a, max(X(b1), X(b2)), y0 + a, PM.T_INT)

    return


def draw_unit_openings(sh, offx, mirror=False):
    """پنجره‌ها و درهایِ یک واحد — باید پس از همهٔ دیوارها ترسیم شود"""
    UWX = PM.UW
    def X(x):
        return offx + (UWX - x if mirror else x)
    def XP(a, b):
        return (X(a), X(b))
    y0, y1 = PM.ENC_Y0, PM.ENC_Y1
    # پنجره‌ها
    for side, wx0, wy0, wx1, wy1 in PM.WINDOWS:
        if side in ("W", "E"):
            xx = X(wx0)
            sh.window(xx, y0 + wy0, xx, y0 + wy1, PM.T_EXT)
        else:
            sh.window(min(X(wx0), X(wx1)), y0 + wy0, max(X(wx0), X(wx1)), y0 + wy0, PM.T_EXT)
    # درِ ایوان (کشویی)
    sh.window(min(X(0.90), X(3.60)), y0, max(X(0.90), X(3.60)), y0, PM.T_EXT)

    # درها
    s = 1 if not mirror else -1
    dr = [  # (x0,y0,x1,y1,swing)
        (9.186, 4.30, 9.186, 5.40, (-0.9, 0)),      # ورودیِ واحد
        (4.60, 3.83, 5.80, 3.83, (0, -0.9)),        # نشیمن-هال (بازشو)
        (7.20, 3.83, 8.10, 3.83, (0, -0.9)),        # آشپزخانه
        (3.99, 4.25, 3.99, 5.05, (-0.9, 0)),        # حمام
        (1.39, 4.25, 1.39, 5.05, (-0.9, 0)),        # سرویس
        (4.30, 5.57, 5.20, 5.57, (0, 0.9)),         # خواب ۱
        (6.30, 5.57, 7.20, 5.57, (0, 0.9)),         # خواب ۲
    ]
    for dx0, dy0, dx1, dy1, sw in dr:
        a, b = XP(dx0, dx1)
        sh.door(min(a, b), y0 + dy0, max(a, b), y0 + dy1, (sw[0] * s, sw[1]),
                leaf=(dx0 != 4.60))

    return


def draw_unit_fixtures(sh, offx, mirror=False):
    """مبلمان، تجهیزات و برچسبِ اتاق‌ها"""
    UWX = PM.UW
    def X(x):
        return offx + (UWX - x if mirror else x)
    def XP(a, b):
        return (X(a), X(b))
    y0 = PM.ENC_Y0
    rooms = PM.mirrored_rooms(offx) if mirror else PM.unit_rooms(offx)
    # مبلمان و تجهیزات
    def fx(rx0, ry0, rx1, ry1, fill, out=(120, 120, 120), label=None, size=10):
        a, b = XP(rx0, rx1)
        sh.rect(min(a, b), y0 + ry0, max(a, b), y0 + ry1, fill=fill, outline=out)
        if label:
            m = sh.M((min(a, b) + max(a, b)) / 2, y0 + (ry0 + ry1) / 2)
            sh.t(m, label, size=size, fill=(90, 90, 90))
    # آشپزخانه: کانترِ L
    fx(6.66, 0.30, 9.09, 0.90, (238, 238, 232), label="کانتر")
    fx(8.49, 0.90, 9.09, 3.53, (238, 238, 232))
    fx(7.20, 1.60, 7.80, 2.20, (222, 222, 216), label="یخچال")
    # حمام
    fx(1.49, 4.20, 2.49, 5.20, (230, 240, 246), label="دوش")
    fx(3.19, 3.95, 3.79, 4.55, (230, 240, 246), label="روشویی")
    # سرویس
    fx(0.25, 4.20, 1.15, 4.95, (230, 240, 246), label="توالت")
    # خواب ۱
    fx(0.40, 5.90, 2.40, 7.60, (236, 240, 246), label="تخت ۱.۶۰")
    fx(0.30, 7.75, 1.00, 8.15, (236, 240, 246))
    fx(4.24, 5.75, 4.94, 8.15, (240, 240, 236), label="کمد")
    # خواب ۲
    fx(5.44, 5.90, 7.24, 7.50, (236, 240, 246), label="تخت ۱.۴۰")
    fx(8.56, 5.75, 9.06, 8.15, (240, 240, 236), label="کمد")
    # نشیمن
    fx(0.50, 1.20, 2.30, 2.00, (242, 238, 230), label="مبل")
    fx(0.60, 0.30, 2.60, 0.80, (242, 238, 230), label="میز تلویزیون")
    fx(3.20, 1.60, 4.60, 2.60, (242, 238, 230), label="ناهارخوری")
    # هال
    fx(4.20, 4.10, 4.90, 5.30, (240, 240, 236), label="کمد دیواری")

    # برچسبِ اتاق‌ها
    for r in rooms:
        cx = (r["x0"] + r["x1"]) / 2
        cy = (r["y0"] + r["y1"]) / 2
        m = sh.M(cx, cy)
        sh.t((m[0], m[1] + 20), f"{r['area']:.1f} m²", size=12, fill=(80, 80, 80))
        sh.t((m[0], m[1] + 4), r["name"], size=14, fill=(40, 40, 40), bold=True)
    return


def draw_core(sh):
    """هسته: پلهٔ رفت‌وبرگشتی، آسانسور، لابی و شفت"""
    z = {c["kind"]: c for c in PM.core_zones()}
    st, lf, shf, lb = z["stair"], z["lift"], z["shaft"], z["lobby"]
    sh.rect(st["x0"], st["y0"], st["x1"], st["y1"], fill=(250, 250, 250), outline=(90, 90, 90))
    sh.rect(lf["x0"], lf["y0"], lf["x1"], lf["y1"], fill=(246, 246, 250), outline=(90, 90, 90))
    sh.rect(lb["x0"], lb["y0"], lb["x1"], lb["y1"], fill=(252, 251, 247), outline=(150, 150, 150))
    sh.rect(shf["x0"], shf["y0"], shf["x1"], shf["y1"], fill=(214, 236, 214), outline=(70, 130, 70))
    # کف‌پله‌ها
    for (tx0, ty0, tx1, ty1) in PM.stair_treads(st):
        sh.rect(tx0, ty0, tx1, ty1, fill=(255, 255, 255), outline=(160, 160, 160))
    mx = (st["x0"] + st["x1"]) / 2
    my = (st["y0"] + st["y1"]) / 2
    p0, p1 = sh.M(mx, st["y0"] + 0.6), sh.M(mx, st["y1"] - 0.6)
    sh.d.line([p0, p1], fill=(200, 60, 60), width=2)
    sh.d.polygon([p1, (p1[0] - 7, p1[1] - 12), (p1[0] + 7, p1[1] - 12)], fill=(200, 60, 60))
    m = sh.M(mx, my)
    sh.t((m[0], m[1]), "پله ۱۶ پله", size=12, fill=(80, 80, 80), bg=(252, 251, 247))
    m = sh.M((lf["x0"] + lf["x1"]) / 2, (lf["y0"] + lf["y1"]) / 2)
    sh.t(m, "آسانسور", size=12, fill=(80, 80, 80))
    sh.d.line([sh.M(lf["x0"], lf["y0"]), sh.M(lf["x1"], lf["y1"])], fill=(150, 150, 150))
    sh.d.line([sh.M(lf["x1"], lf["y0"]), sh.M(lf["x0"], lf["y1"])], fill=(150, 150, 150))
    m = sh.M((lb["x0"] + lb["x1"]) / 2, (lb["y0"] + lb["y1"]) / 2)
    sh.t(m, "پاگرد", size=12, fill=(90, 90, 90), rot=90)
    m = sh.M((shf["x0"] + shf["x1"]) / 2, (shf["y0"] + shf["y1"]) / 2)
    sh.t((m[0], m[1] - 10), "شفتِ نور و تهویه", size=13, fill=(40, 100, 50), bg=(252, 251, 247))
    sh.t((m[0], m[1] + 10), f"{PM.SH_W:.2f} × {PM.SH_D:.2f} = {PM.SH_W*PM.SH_D:.1f} m²", size=12,
         fill=(40, 100, 50), bg=(252, 251, 247))
    # دیوارِ شفت
    sh.wall(shf["x0"], shf["y0"], shf["x1"], shf["y0"], PM.T_CORE)
    sh.wall(st["x0"] + 2.50, st["y0"], st["x0"] + 2.50, st["y1"], PM.T_INT)


# ================================================================ برگه‌ها
def sheet_typical():
    s = PM.summary()
    sh = Sheet("پلانِ طبقهٔ تیپ — طبقات ۱ تا ۵", "۲ واحد + هسته + شفت + ایوان", "+۵٫۴۰", "A-۱۰۳",
               -1.6, PM.BALC_Y0 - 1.4, PM.BLD_W + 1.8, PM.ENC_Y1 + 1.8)
    # ایوان‌ها
    liv = [r for r in PM.ROOMS if r[1] == "living"][0]
    for offx, mir in ((0.0, False), (PM.UNIT_B_X, True)):
        x0 = (offx + PM.UW - liv[4]) if mir else (offx + liv[2])
        sh.rect(x0, PM.BALC_Y0, x0 + (liv[4] - liv[2]), PM.ENC_Y0, fill=(252, 246, 224),
                outline=(190, 150, 60))
        m = sh.M(x0 + (liv[4] - liv[2]) / 2, (PM.BALC_Y0 + PM.ENC_Y0) / 2)
        sh.t((m[0], m[1] - 9), "ایوان", size=14, fill=(120, 85, 20), bold=True)
        sh.t((m[0], m[1] + 9), f"{s['balcony']} m² (۵۰٪ در تراکم)", size=11, fill=(120, 85, 20))
        # نرده
        sh.line([(x0, PM.BALC_Y0), (x0 + (liv[4] - liv[2]), PM.BALC_Y0)], fill=(150, 110, 40), w=3)
    # ۱) اتاق‌ها و دیوارهای داخلی
    draw_unit_shell(sh, 0.0, False)
    draw_unit_shell(sh, PM.UNIT_B_X, True)
    # ۲) دیوارهای پیرامونی و هسته
    sh.wall(0, PM.ENC_Y0, PM.BLD_W, PM.ENC_Y0, PM.T_EXT)
    sh.wall(0, PM.ENC_Y1, PM.BLD_W, PM.ENC_Y1, PM.T_EXT)
    sh.wall(0, PM.ENC_Y0, 0, PM.ENC_Y1, PM.T_EXT)
    sh.wall(PM.BLD_W, PM.ENC_Y0, PM.BLD_W, PM.ENC_Y1, PM.T_EXT)
    sh.wall(PM.CORE_X0, PM.ENC_Y0, PM.CORE_X0, PM.ENC_Y1, PM.T_CORE)
    sh.wall(PM.CORE_X1, PM.ENC_Y0, PM.CORE_X1, PM.ENC_Y1, PM.T_CORE)
    draw_core(sh)
    # ۳) بازشوها (پس از همهٔ دیوارها)
    draw_unit_openings(sh, 0.0, False)
    draw_unit_openings(sh, PM.UNIT_B_X, True)
    # ۴) مبلمان و برچسب‌ها
    draw_unit_fixtures(sh, 0.0, False)
    draw_unit_fixtures(sh, PM.UNIT_B_X, True)
    # ابعاد
    for i, x in enumerate([0, PM.UW, PM.CORE_X1, PM.BLD_W]):
        sh.axis(x, PM.ENC_Y1 + 1.0, ["A", "B", "C", "D"][i])
    sh.dimh(0, PM.UW, PM.BALC_Y0 - 0.55, f"{PM.UW:.2f}")
    sh.dimh(PM.UW, PM.CORE_X1, PM.BALC_Y0 - 0.55, f"{PM.CORE_W:.2f}")
    sh.dimh(PM.CORE_X1, PM.BLD_W, PM.BALC_Y0 - 0.55, f"{PM.UW:.2f}")
    sh.dimh(0, PM.BLD_W, PM.BALC_Y0 - 1.25, f"{PM.BLD_W:.2f}")
    sh.dimv(PM.BALC_Y0, PM.ENC_Y0, PM.BLD_W + 0.75, "۲.۴۰")
    sh.dimv(PM.ENC_Y0, PM.ENC_Y1, PM.BLD_W + 0.75, "۸.۳۰")
    sh.dimv(PM.BALC_Y0, PM.ENC_Y1, PM.BLD_W + 1.45, "۱۰.۷۰")
    sh.frame(notes=[
        f"زیربنایِ هر طبقه: {s['per_floor']} m² (۲ واحدِ {s['unit_encl']} + هستهٔ {s['core_net']} + نیمی از ایوان‌ها)",
        f"مساحتِ فروشیِ هر واحد: {s['unit_sale']} m² ({s['unit_encl']} بسته + {s['balcony']} ایوان)",
        "دیوارِ پیرامونی ۳۰cm · دیوارِ هسته و همسایگی ۲۵cm · تیغه‌ها ۱۵cm",
        "سرویس از داخلِ حمام باز می‌شود (جایگزین: ادغامِ حمام و سرویس = ۶.۹ m²)",
        "ارتفاعِ طبقه ۲.۹۰ m · پلهٔ رفت‌وبرگشتی ۱۶ پله (ارتفاعِ پله ۱۸.۱cm، کف‌پله ۲۹cm)",
    ], scale_text="۱:۱۰۰")
    sh.save(os.path.join(OUTDIR, "plan-typical.png"))
    return s


def sheet_ground():
    s = PM.summary()
    sh = Sheet("پلانِ همکف / پیلوت", "۳ مغازه + پارکینگ + هستهٔ عمودی", "±0.00", "A-۱۰۱",
               -2.0, PM.Y0 - 1.8, PM.LAND_W + 2.0, PM.Y1 + 2.2)
    sh.rect(0, PM.Y0, PM.LAND_W, PM.Y1, fill=(255, 255, 255), outline=(120, 120, 120), w=2)
    # فضای بازِ جنوبی و حریم
    sh.rect(0, 0, PM.LAND_W, PM.Y0, fill=(228, 242, 228), outline=(120, 170, 120))
    m = sh.M(PM.LAND_W / 2, PM.Y0 / 2)
    sh.t(m, "فضای بازِ جنوبی ۲.۶۷ m + حریمِ دکلِ فشارقوی ۷.۰۸ m", size=12, fill=(40, 100, 50))
    # پارکینگ
    sh.rect(0, PM.Y0, PM.SHOP_X0, PM.Y1, fill=(238, 243, 250))
    n = 0
    for bay in (0.5, PM.CORE_X1 + 0.4):
        for i in range(3):
            if bay + i * 2.65 + 2.5 > PM.SHOP_X0 - 0.2:
                break
            n += 1
            x0 = bay + i * 2.65
            sh.rect(x0, PM.Y0 + 0.5, x0 + PM.PARK_W, PM.Y0 + 0.5 + PM.PARK_L,
                    fill=(255, 255, 255), outline=(110, 140, 190))
            m = sh.M(x0 + 1.25, PM.Y0 + 3.0)
            sh.t(m, str(n), size=12, fill=(90, 120, 170))
    m = sh.M(4.5, PM.Y1 - 2.0)
    sh.t(m, "مسیرِ تردد و مانور", size=12, fill=(70, 100, 150))
    m = sh.M(18.0, PM.Y1 - 2.0)
    sh.t(m, "مسیرِ تردد و مانور", size=12, fill=(70, 100, 150))
    # هسته در همکف
    sh.rect(PM.CORE_X0, PM.Y1 - 5.10, PM.CORE_X1, PM.Y1, fill=(246, 246, 250), outline=(90, 90, 90))
    m = sh.M((PM.CORE_X0 + PM.CORE_X1) / 2, PM.Y1 - 2.5)
    sh.t(m, "لابی · پله · آسانسور", size=12, fill=(80, 80, 90))
    # مغازه‌ها
    for i in range(PM.NSHOP):
        x0 = PM.SHOP_X0 + i * PM.SHOP_W
        sh.rect(x0, PM.Y1 - PM.SHOP_DEEP, x0 + PM.SHOP_W, PM.Y1, fill=(253, 243, 224),
                outline=(170, 120, 50))
        m = sh.M(x0 + PM.SHOP_W / 2, PM.Y1 - PM.SHOP_DEEP / 2)
        sh.t((m[0], m[1] - 12), f"مغازه {i+1}", size=14, fill=(120, 80, 20), bold=True)
        sh.t((m[0], m[1] + 6), f"{s['shop_area']} m²", size=12, fill=(120, 80, 20))
        sh.t((m[0], m[1] + 24), f"نیم‌طبقه {PM.SHOP_W*PM.MEZ_DEEP:.1f} m² (خط‌چین)", size=11,
             fill=(150, 110, 50))
        # درِ مغازه
        sh.window(x0 + 1.6, PM.Y1, x0 + 1.6 + 2.8, PM.Y1, 0.3)
    sh.rect(PM.SHOP_X0, PM.Y0, PM.LAND_W, PM.Y1 - PM.SHOP_DEEP, fill=(246, 246, 240),
            outline=(170, 170, 170))
    m = sh.M((PM.SHOP_X0 + PM.LAND_W) / 2, PM.Y0 + 1.2)
    sh.t(m, "انبار و سرویسِ مغازه‌ها", size=12, fill=(90, 90, 90))
    # خط‌چینِ نیم‌طبقه
    for i in range(PM.NSHOP):
        x0 = PM.SHOP_X0 + i * PM.SHOP_W
        for yy in [PM.Y1 - PM.SHOP_DEEP + k * 0.6 for k in range(int(PM.MEZ_DEEP / 0.6))]:
            sh.d.line([sh.M(x0 + 0.15, yy), sh.M(x0 + 0.15, yy + 0.35)], fill=(170, 120, 50), width=2)
            sh.d.line([sh.M(x0 + PM.SHOP_W - 0.15, yy), sh.M(x0 + PM.SHOP_W - 0.15, yy + 0.35)],
                      fill=(170, 120, 50), width=2)
        for xx in [x0 + 0.15 + k * 0.9 for k in range(int((PM.SHOP_W - 0.3) / 0.9))]:
            sh.d.line([sh.M(xx, PM.Y1 - 0.15), sh.M(xx + 0.5, PM.Y1 - 0.15)], fill=(170, 120, 50), width=2)
            sh.d.line([sh.M(xx, PM.Y1 - PM.MEZ_DEEP), sh.M(xx + 0.5, PM.Y1 - PM.MEZ_DEEP)],
                      fill=(170, 120, 50), width=2)
    # ورودی‌ها
    sh.d.polygon([sh.M(1.2, PM.Y1 + 1.4), sh.M(1.2, PM.Y1), sh.M(4.2, PM.Y1)], outline=(200, 120, 40),
                 width=2)
    m = sh.M(2.7, PM.Y1 + 1.9)
    sh.t(m, "ورودیِ خودرو", size=12, fill=(200, 120, 40))
    sh.d.polygon([sh.M(PM.CORE_X0 + 1.5, PM.Y1 + 1.4), sh.M(PM.CORE_X0 + 1.5, PM.Y1),
                  sh.M(PM.CORE_X0 + 4.0, PM.Y1)], outline=(60, 90, 160), width=2)
    m = sh.M(PM.CORE_X0 + 2.8, PM.Y1 + 1.9)
    sh.t(m, "ورودیِ پیاده", size=12, fill=(60, 90, 160))
    # ابعاد
    sh.dimh(0, PM.BLD_W, PM.Y0 - 0.6, f"{PM.BLD_W:.2f}")
    sh.dimh(PM.SHOP_X0, PM.LAND_W, PM.Y0 - 0.6, f"{PM.LAND_W-PM.SHOP_X0:.2f}")
    sh.dimh(0, PM.LAND_W, PM.Y0 - 1.3, f"{PM.LAND_W:.2f}")
    sh.dimv(PM.Y0, PM.Y1, PM.LAND_W + 0.7, "۱۰.۷۰")
    sh.dimv(0, PM.Y0, PM.LAND_W + 0.7, "۲.۶۷")
    sh.frame(notes=[
        f"زیربنایِ همکف: {s['ground']} m² (۳ مغازه + انبار/سرویس + هسته)",
        f"{n} فضای پارکینگ با ابعاد ۲.۵۰ × ۵.۰۰ · ارتفاعِ مفیدِ پیلوت ۲.۴۰ m (معاف از تراکم)",
        "ارتفاعِ مغازه ۵.۴۰ m با نیم‌طبقه (تراز ۲.۶۰) — تنها ۲۰٪ نیم‌طبقه در تراکم",
        "نیازِ واقعیِ پارکینگ ۱۲ تا ۱۴ فضا ⇒ کسری با زیرزمین یا جریمهٔ تبصرهٔ ۵ مادهٔ ۱۰۰ جبران شود",
    ], scale_text="۱:۱۰۰")
    sh.save(os.path.join(OUTDIR, "plan-ground.png"))


def sheet_mezz():
    s = PM.summary()
    sh = Sheet("پلانِ نیم‌طبقه و انباری", "تراز ۲.۶۰+ — معاف از تراکم", "+۲.۶۰", "A-۱۰۲",
               -2.0, PM.Y0 - 1.8, PM.LAND_W + 2.0, PM.Y1 + 2.2)
    sh.rect(0, PM.Y0, PM.LAND_W, PM.Y1, fill=(255, 255, 255), outline=(120, 120, 120), w=2)
    sh.rect(0, PM.Y0, PM.SHOP_X0, PM.Y1, fill=(250, 247, 238))
    for i in range(PM.ANB_N):
        x0 = 0.4 + i * 2.60
        if x0 + PM.ANB_W > PM.SHOP_X0 - 0.3:
            break
        sh.rect(x0, PM.Y0 + 0.3, x0 + PM.ANB_W, PM.Y0 + 0.3 + PM.ANB_D, fill=(255, 255, 255),
                outline=(150, 130, 90))
        m = sh.M(x0 + PM.ANB_W / 2, PM.Y0 + 1.4)
        sh.t(m, f"انباری {i+1}", size=10, fill=(120, 100, 60))
    m = sh.M(10.0, PM.Y0 + 4.6)
    sh.t(m, "راهروی انباری‌ها (۱.۲۰ m)", size=12, fill=(120, 100, 60))
    m = sh.M(10.0, PM.Y1 - 2.2)
    sh.t(m, "فضای باز — نورگیرِ پارکینگ", size=12, fill=(110, 130, 110))
    for i in range(PM.NSHOP):
        x0 = PM.SHOP_X0 + i * PM.SHOP_W
        sh.rect(x0, PM.Y1 - PM.MEZ_DEEP, x0 + PM.SHOP_W, PM.Y1, fill=(253, 243, 224),
                outline=(170, 120, 50))
        m = sh.M(x0 + PM.SHOP_W / 2, PM.Y1 - PM.MEZ_DEEP / 2)
        sh.t((m[0], m[1] - 10), f"نیم‌طبقه {i+1}", size=13, fill=(120, 80, 20), bold=True)
        sh.t((m[0], m[1] + 8), f"{PM.SHOP_W*PM.MEZ_DEEP:.1f} m²", size=12, fill=(120, 80, 20))
        sh.t((m[0], m[1] + 24), "ارتفاعِ مفید ۲.۵۰", size=10, fill=(150, 110, 50))
    sh.rect(PM.SHOP_X0, PM.Y0, PM.LAND_W, PM.Y1 - PM.MEZ_DEEP, fill=(246, 246, 240),
            outline=(170, 170, 170))
    m = sh.M((PM.SHOP_X0 + PM.LAND_W) / 2, PM.Y0 + 1.5)
    sh.t(m, "بخشِ زیرِ نیم‌طبقه: دسترسی از داخلِ مغازه", size=12, fill=(90, 90, 90))
    sh.rect(PM.CORE_X0, PM.Y1 - 5.10, PM.CORE_X1, PM.Y1, fill=(246, 246, 250), outline=(90, 90, 90))
    m = sh.M((PM.CORE_X0 + PM.CORE_X1) / 2, PM.Y1 - 2.5)
    sh.t(m, "هسته (پله و آسانسور)", size=12, fill=(80, 80, 90))
    sh.dimh(0, PM.SHOP_X0, PM.Y0 - 0.6, f"{PM.SHOP_X0:.2f}")
    sh.dimh(PM.SHOP_X0, PM.LAND_W, PM.Y0 - 0.6, f"{PM.LAND_W-PM.SHOP_X0:.2f}")
    sh.frame(notes=[
        f"۸ انباریِ ۵ m² = {s['anb']} m² — کاملاً معاف از تراکم (ارتفاعِ مفید ۲.۲۰ m)",
        f"۳ نیم‌طبقه = {s['mez_phys']} m² واقعی که تنها {s['mezz_counted']} m² در تراکم می‌آید",
        "ضابطه: نیم‌طبقه تا ۵۵٪ مساحتِ مغازه مجاز و تنها ۲۰٪ آن (حداکثر ۲۰ m²) جزو تراکم است",
        "پارکینگِ زیرِ این سطح ارتفاعِ مفیدِ ۲.۴۰ m دارد و معاف است",
    ], scale_text="۱:۱۰۰")
    sh.save(os.path.join(OUTDIR, "plan-mezzanine.png"))


def sheet_roof():
    s = PM.summary()
    sh = Sheet("پلانِ بام", "عایق‌کاری، شیب‌بندی و جان‌پناه", f"+{PM.TOP:.2f}", "A-۱۰۴",
               -2.0, PM.Y0 - 1.8, PM.LAND_W + 2.0, PM.Y1 + 2.2)
    sh.rect(0, PM.Y0, PM.LAND_W, PM.Y1, fill=(252, 251, 247), outline=(120, 120, 120), w=2)
    sh.rect(0, PM.ENC_Y0, PM.BLD_W, PM.ENC_Y1, fill=(238, 238, 234), outline=(90, 90, 90), w=2)
    m = sh.M(PM.BLD_W / 2, (PM.ENC_Y0 + PM.ENC_Y1) / 2)
    sh.t((m[0], m[1] - 10), "بامِ مسکونی", size=15, fill=(60, 60, 70), bold=True)
    sh.t((m[0], m[1] + 12), "شیب ۱٪ به سمتِ آبروهایِ جنوبی", size=12, fill=(90, 90, 100))
    # تراس
    sh.rect(PM.BLD_W, PM.Y0, PM.LAND_W, PM.Y1, fill=(224, 240, 224), outline=(90, 130, 90), w=2)
    m = sh.M((PM.BLD_W + PM.LAND_W) / 2, (PM.Y0 + PM.Y1) / 2)
    sh.t((m[0], m[1] - 10), "تراسِ پودیوم", size=15, fill=(35, 95, 45), bold=True)
    sh.t((m[0], m[1] + 12), f"{round((PM.LAND_W-PM.BLD_W)*PM.PODIUM_D)} m²", size=12, fill=(35, 95, 45))
    # شفت
    z = {c["kind"]: c for c in PM.core_zones()}
    shf = z["shaft"]
    sh.rect(shf["x0"], shf["y0"], shf["x1"], shf["y1"], fill=(160, 200, 160), outline=(60, 120, 60), w=2)
    m = sh.M((shf["x0"] + shf["x1"]) / 2, (shf["y0"] + shf["y1"]) / 2)
    sh.t((m[0], m[1] - 10), "دهانهٔ شفت", size=13, fill=(30, 90, 40), bold=True)
    sh.t((m[0], m[1] + 10), f"{PM.SH_W:.2f} × {PM.SH_D:.2f}", size=12, fill=(30, 90, 40))
    # اتاقکِ پله و آسانسور
    st, lf = z["stair"], z["lift"]
    sh.rect(st["x0"], st["y0"], lf["x1"], st["y1"], fill=(246, 246, 250), outline=(90, 90, 90), w=2)
    m = sh.M((st["x0"] + lf["x1"]) / 2, (st["y0"] + st["y1"]) / 2)
    sh.t(m, "اتاقکِ پله و آسانسور", size=13, fill=(70, 70, 90))
    # جان‌پناه
    for (x0, y0, x1, y1) in [(0, PM.ENC_Y0, PM.BLD_W, PM.ENC_Y0), (0, PM.ENC_Y1, PM.BLD_W, PM.ENC_Y1),
                             (0, PM.ENC_Y0, 0, PM.ENC_Y1), (PM.BLD_W, PM.ENC_Y0, PM.BLD_W, PM.ENC_Y1)]:
        sh.wall(x0, y0, x1, y1, 0.25, fill=(90, 90, 90))
    m = sh.M(PM.BLD_W / 2, PM.ENC_Y1 + 0.7)
    sh.t(m, "جان‌پناه ۱.۰۰ m", size=12, fill=(90, 90, 90))
    sh.dimh(0, PM.BLD_W, PM.Y0 - 0.6, f"{PM.BLD_W:.2f}")
    sh.dimv(PM.Y0, PM.Y1, PM.LAND_W + 0.7, "۱۰.۷۰")
    sh.frame(notes=[
        f"ارتفاعِ تمام‌شده: {s['height']} m (پودیوم ۵.۴۰ + ۵ طبقه × ۲.۹۰ + جان‌پناه ۱.۰۰)",
        "موتورخانه و منبعِ آب روی بام با ارتفاعِ مفید کمتر از ۲.۲۰ ⇒ معاف از تراکم",
        "دهانهٔ شفت باید تا بام ادامه یابد و با کلاهکِ باران‌گیر پوشش شود",
    ], scale_text="۱:۱۰۰")
    sh.save(os.path.join(OUTDIR, "plan-roof.png"))


if __name__ == "__main__":
    s = sheet_typical()
    sheet_ground()
    sheet_mezz()
    sheet_roof()
    print(json.dumps(s, ensure_ascii=False))
