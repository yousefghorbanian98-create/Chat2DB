#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""پلان‌های مهندسی در قطعِ A3 افقی، ۳۰۰ DPI، آمادهٔ چاپ — هر طبقه روی یک ورق.

ابعادِ فیزیکی: ۴۲۰ × ۲۹۷ میلی‌متر · نوارِ ترسیم در سمتِ راست (رویهٔ رایجِ ایران)
مقیاس: طبقهٔ تیپ ۱:۷۵ · همکف/نیم‌طبقه/بام ۱:۱۵۰
خروجی: docs/arch/A3/*.png و یک PDFِ چندصفحه‌ای
"""
import os, math, json
from PIL import Image, ImageDraw, ImageFont
import arabic_reshaper
from bidi.algorithm import get_display
import plan_model as PM
from render_plans import (draw_unit_shell, draw_unit_openings, draw_unit_fixtures,
                          draw_core, fa)

HERE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
OUT = os.path.join(HERE, "docs", "arch", "A3")
FDIR = "/home/user/fonts"

DPI = 300
MM = DPI / 25.4                       # پیکسل بر میلی‌متر
A3W, A3H = int(420 * MM), int(297 * MM)          # ۴۹۶۱ × ۳۵۰۸
MARGIN = 13 * MM                                  # حاشیهٔ داخلی
STRIP_W = 62 * MM                                 # نوارِ ترسیم (راست)
DRAW_W = A3W - MARGIN - STRIP_W - 8 * MM - MARGIN
DRAW_H = A3H - 2 * MARGIN

_c = {}


def F(sz, bold=False):
    k = (int(sz), bold)
    if k not in _c:
        _c[k] = ImageFont.truetype(os.path.join(FDIR, "Vazirmatn-Bold.ttf" if bold else
                                                "Vazirmatn-Regular.ttf"), int(sz))
    return _c[k]


LW = {1: 4, 2: 7, 3: 11, 4: 15}


class A3Sheet:
    def __init__(self, title, subtitle, level, no, mx0, my0, mx1, my1, scale_denom):
        self.img = Image.new("RGB", (A3W, A3H), (252, 251, 247))
        self.d = ImageDraw.Draw(self.img)
        self.title, self.sub, self.lvl, self.no = title, subtitle, level, no
        # برازشِ خودکار: مقیاس را آن‌قدر درشت کن (به مقیاسِ استاندارد) که از کادر بیرون نزند
        STD = [50, 75, 100, 125, 150, 200, 250]
        sd = scale_denom
        for cand in [x for x in STD if x >= scale_denom]:
            sc = (1000.0 / cand) * MM
            if (mx1 - mx0) * sc <= DRAW_W and (my1 - my0) * sc <= DRAW_H:
                sd = cand
                break
        else:
            sd = 250
        self.sd = sd
        self.sc = (1000.0 / sd) * MM
        ox = MARGIN + (DRAW_W - (mx1 - mx0) * self.sc) / 2
        oy = MARGIN + (DRAW_H - (my1 - my0) * self.sc) / 2
        self.ox, self.oy = ox - mx0 * self.sc, oy + my1 * self.sc
        self.labels = []                          # جعبه‌هایِ اشغال‌شده
        self.tscale = DPI / 72.0     # اندازهٔ قلم بر حسبِ نقطه (pt)؛ ۱pt = ۰.۳۵۳ mm

    # ---------------------------------------------------------- تبدیل
    def M(self, x, y):
        return (self.ox + x * self.sc, self.oy - y * self.sc)

    # ---------------------------------------------------------- چیدمانِ متن
    def _layout(self, xy, s, size, bold, anchor, max_w, min_size):
        """محاسبهٔ چیدمانِ متن بدون ترسیم — برای اندازه‌گیری و یافتنِ جایِ خالی"""
        s2 = fa(str(s))
        size = float(size)
        f = F(size * self.tscale, bold)
        lines = [s2]
        if max_w and max_w > 10 and f.getlength(s2) > max_w:
            while size > min_size:
                lines = _wrap_px(s2, f, max_w)
                if max(f.getlength(l) for l in lines) <= max_w:
                    break
                size -= 0.5
                f = F(size * self.tscale, bold)
        if size < min_size:
            return None
        f = F(size * self.tscale, bold)
        lh = size * self.tscale * 1.18                      # فاصلهٔ سطر
        wmax = max(f.getlength(l) for l in lines)
        htot = lh * len(lines)
        hh = anchor[0] if len(anchor) == 2 else anchor[0]
        vv = anchor[1] if len(anchor) == 2 else "m"
        x0 = xy[0] if hh == "l" else (xy[0] - wmax if hh == "r" else xy[0] - wmax / 2)
        y0 = (xy[1] if vv in "at" else (xy[1] - htot if vv in "sb" else xy[1] - htot / 2))
        return (f, lines, lh, x0, y0, wmax, htot)

    def measure(self, xy, s, size=14, bold=False, anchor="mm", max_w=None,
                min_size=7.0, rot=0):
        """جعبه‌ای که متن اشغال می‌کند — بدون ترسیم"""
        L = self._layout(xy, s, size, bold, anchor, max_w, min_size)
        if L is None:
            return None
        f, lines, lh, x0, y0, wmax, htot = L
        if rot:                                   # پس از چرخش جابه‌جا می‌شود
            return (xy[0] - htot / 2, xy[1] - wmax / 2, xy[0] + htot / 2, xy[1] + wmax / 2)
        return (x0, y0, x0 + wmax, y0 + htot)

    def t_free(self, xy, s, size=14, fill=(35, 35, 35), bold=False, anchor="mm",
               bg=None, rot=0, max_w=None, cands=None, **kw):
        """ترسیم در نخستین جایِ خالی — تا برچسبی رویِ برچسبِ دیگر نیفتد"""
        lh = size * self.tscale * 1.18
        if cands is None:
            cands = [(0, 0), (0, -lh), (0, lh), (0, -2 * lh), (0, 2 * lh),
                     (0, -3 * lh), (0, 3 * lh)]
        for (dx, dy) in cands:
            p = (xy[0] + dx, xy[1] + dy)
            b = self.measure(p, s, size=size, bold=bold, anchor=anchor,
                             max_w=max_w, rot=rot)
            if b is None:
                continue
            if not any(_ovl(b, o) for o in self.labels):
                return self.t(p, s, size=size, fill=fill, bold=bold, anchor=anchor,
                              bg=bg, rot=rot, max_w=max_w, **kw)
        return self.t(xy, s, size=size, fill=fill, bold=bold, anchor=anchor,
                      bg=bg, rot=rot, max_w=max_w, **kw)

    # ---------------------------------------------------------- ترسیمِ پایه
    def t(self, xy, s, size=14, fill=(35, 35, 35), bold=False, anchor="mm", bg=None,
          rot=0, max_w=None, min_size=7.0, pad=5):
        """ترسیمِ متنِ فارسی — اندازه بر حسبِ «نقطه» (pt)؛ هر نقطه ۰.۳۵۳ میلی‌متر.

        max_w   : پهنایِ مجاز به پیکسل؛ اگر متن عریض‌تر بود سطر می‌شکند و در
                  صورتِ نیاز قلم کوچک می‌شود تا هرگز از کادر بیرون نزند.
        min_size: اگر حتی با کوچک کردن هم جا نشد، متن ترسیم نمی‌شود (به‌جایِ
                  بیرون‌زدگی یا ناخوانایی).
        برمی‌گرداند: جعبهٔ ترسیم‌شده (x0, y0, x1, y1) یا None
        """
        L = self._layout(xy, s, size, bold, anchor, max_w, min_size)
        if L is None:
            return None
        f, lines, lh, x0, y0, wmax, htot = L

        # ---- متنِ چرخیده: بوم به اندازهٔ نیاز (دیگر بریده نمی‌شود) + زمینه
        if rot:
            tw = max(f.getlength(l) for l in lines)
            th = lh * len(lines)
            cw, ch = int(tw) + 2 * pad, int(th) + 2 * pad
            tmp = Image.new("RGBA", (cw, ch), tuple(bg) + (255,) if bg else (0, 0, 0, 0))
            td = ImageDraw.Draw(tmp)
            for i, l in enumerate(lines):
                td.text((cw / 2, pad + lh * i + lh / 2), l, font=f,
                        fill=tuple(fill) + (255,), anchor="mm")
            tmp = tmp.rotate(rot, expand=True, resample=Image.BICUBIC)
            x, y = int(xy[0] - tmp.width / 2), int(xy[1] - tmp.height / 2)
            self.img.paste(tmp, (x, y), tmp)
            self.labels.append((x, y, x + tmp.width, y + tmp.height))
            return (x, y, x + tmp.width, y + tmp.height)

        # ---- متنِ افقی
        if bg:
            self.d.rectangle([x0 - pad, y0 - pad * 0.7, x0 + wmax + pad,
                              y0 + htot + pad * 0.7], fill=bg)
        for i, l in enumerate(lines):
            lw = f.getlength(l)
            lx = x0 + {"l": 0.0, "r": wmax - lw}.get(anchor[0], (wmax - lw) / 2)
            self.d.text((lx, y0 + lh * i), l, font=f, fill=fill, anchor="la")
        box = (x0, y0, x0 + wmax, y0 + htot)
        self.labels.append(box)
        return box

    def rect(self, x0, y0, x1, y1, fill=None, outline=None, w=1):
        a, b = self.M(x0, y1), self.M(x1, y0)
        self.d.rectangle([a[0], a[1], b[0], b[1]], fill=fill,
                         outline=outline, width=LW.get(w, 4) if outline else 0)

    def line(self, pts, fill=(40, 40, 40), w=1):
        self.d.line([self.M(*p) for p in pts], fill=fill, width=LW.get(w, 4))

    def wall(self, x0, y0, x1, y1, t=PM.T_INT, fill=(58, 58, 58)):
        if abs(x1 - x0) > abs(y1 - y0):
            self.rect(x0, y0 - t / 2, x1, y1 + t / 2, fill=fill)
        else:
            self.rect(x0 - t / 2, y0, x1 + t / 2, y1, fill=fill)

    def door(self, x0, y0, x1, y1, swing, leaf=True):
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
        pts = []
        for i in range(25):
            a = math.radians(a0 + (a1 - a0) * i / 24)
            pts.append(self.M(cx + r * math.cos(a), cy + r * math.sin(a)))
        self.d.line(pts, fill=(40, 40, 40), width=LW[1])

    def opening(self, x0, y0, x1, y1):
        if abs(x1 - x0) > abs(y1 - y0):
            self.rect(x0, y0 - 0.20, x1, y1 + 0.20, fill=(252, 251, 247))
        else:
            self.rect(x0 - 0.20, y0, x1 + 0.20, y1, fill=(252, 251, 247))

    def window(self, x0, y0, x1, y1, t=PM.T_EXT):
        if abs(x1 - x0) > abs(y1 - y0):
            for o in (-t / 2, 0, t / 2):
                self.line([(x0, y0 + o), (x1, y1 + o)], fill=(190, 225, 240), w=2)
            self.rect(x0, y0 - t / 2, x1, y1 + t / 2, outline=(110, 145, 160), w=1)
        else:
            for o in (-t / 2, 0, t / 2):
                self.line([(x0 + o, y0), (x1 + o, y1)], fill=(190, 225, 240), w=2)
            self.rect(x0 - t / 2, y0, x1 + t / 2, y1, outline=(110, 145, 160), w=1)

    # ---------------------------------------------------------- ابعاد و محور
    def dimh(self, x0, x1, y, label=None, off=0.0):
        yy = y - off
        self.line([(x0, yy), (x1, yy)], fill=(185, 65, 65), w=1)
        for xx in (x0, x1):
            self.line([(xx, yy - 0.20), (xx, yy + 0.20)], fill=(185, 65, 65), w=1)
        m = self.M((x0 + x1) / 2, yy)
        self.t((m[0], m[1] - 0.42 * self.sc), label or f"{abs(x1-x0):.2f}",
               size=12, fill=(165, 50, 50), bg=(252, 251, 247))

    def dimv(self, y0, y1, x, label=None, off=0.0):
        xx = x - off
        self.line([(xx, y0), (xx, y1)], fill=(185, 65, 65), w=1)
        for yy in (y0, y1):
            self.line([(xx - 0.20, yy), (xx + 0.20, yy)], fill=(185, 65, 65), w=1)
        m = self.M(xx, (y0 + y1) / 2)
        self.t((m[0] - 0.42 * self.sc, m[1]), label or f"{abs(y1-y0):.2f}",
               size=12, fill=(165, 50, 50), bg=(252, 251, 247), rot=90)

    def axis(self, x, y, name):
        cx, cy = self.M(x, y)
        self.d.line([(cx, cy), (cx, cy - 1.5 * self.sc)], fill=(85, 115, 165), width=LW[1])
        r = 0.42 * self.sc
        self.d.ellipse([cx - r, cy - 1.5 * self.sc - r, cx + r, cy - 1.5 * self.sc + r],
                       fill=(252, 251, 247), outline=(85, 115, 165), width=LW[1])
        self.t((cx, cy - 1.5 * self.sc), name, size=11, fill=(55, 85, 135), bold=True)

    def level_mark(self, x, y, text):
        """علامتِ تراز"""
        cx, cy = self.M(x, y)
        s = 0.9 * self.sc
        self.d.polygon([(cx - s * 0.6, cy), (cx + s * 0.6, cy), (cx, cy - s * 0.75)],
                       fill=(252, 251, 247), outline=(60, 60, 60), width=LW[1])
        self.d.line([(cx - s * 1.6, cy), (cx + s * 1.6, cy)], fill=(60, 60, 60), width=LW[1])
        self.t((cx + s * 1.9, cy - s * 0.3), text, size=12, fill=(40, 40, 40), anchor="lm")

    # ---------------------------------------------------------- نوارِ ترسیم
    def strip(self, rows, schedule=None, notes=()):
        x0 = A3W - 8 * MM - STRIP_W
        x1 = A3W - 8 * MM
        y0, y1 = 8 * MM, A3H - 8 * MM
        self.d.rectangle([x0, y0, x1, y1], fill=(252, 251, 247), outline=(60, 60, 60), width=LW[2])
        self.d.rectangle([x0 + 5, y0 + 5, x1 - 5, y1 - 5], outline=(60, 60, 60), width=LW[1])
        pad = 16
        il, ir = x0 + 5 + pad, x1 - 5 - pad        # درونِ نوار: چپ / راست
        iw = ir - il                               # پهنایِ قابلِ استفاده
        cy = y0 + 5
        # عنوانِ پروژه
        h_head = 178
        self.d.rectangle([x0 + 5, y0 + 5, x1 - 5, y0 + 5 + h_head], fill=(238, 241, 246))
        self.t(((il + ir) / 2, y0 + 5 + 54), "مجتمع مسکونی-تجاری",
               size=17, fill=(25, 45, 80), bold=True, max_w=iw)
        self.t(((il + ir) / 2, y0 + 5 + 128), "زمین ۵۴۲٫۳۸ m² — اصفهان",
               size=12, fill=(60, 80, 110), max_w=iw)
        cy = y0 + 5 + h_head
        # ردیف‌هایِ اطلاعات (فاصلهٔ کافی که کلید و مقدار هم‌دیگر را نپوشانند)
        for k, v in rows:
            h = 142
            self.d.line([(x0 + 5, cy + h), (x1 - 5, cy + h)], fill=(150, 150, 150), width=LW[1])
            self.t((ir, cy + 16), k, size=10, fill=(95, 95, 95), anchor="ra", max_w=iw - 8)
            self.t((ir, cy + 70), v, size=14, fill=(30, 30, 30), anchor="ra", bold=True,
                   max_w=iw - 8)
            cy += h
        # جدولِ فضاها — ستون‌ها با پهنایِ اندازه‌گیری‌شده
        cy += 16
        if schedule:
            b = self.t((ir, cy), "جدول فضاها", size=13, fill=(25, 45, 80), bold=True,
                       anchor="ra", max_w=iw)
            cy += ((b[3] - b[1]) if b else 30) + 16
            self.d.line([(x0 + 5, cy), (x1 - 5, cy)], fill=(60, 60, 60), width=LW[1])
            cy += 12
            for nm, a, dim in schedule:
                # سطرِ یکم: نام (راست) و مساحت (چپ) — سطرِ دوم: ابعاد
                b1 = self.t((ir, cy), nm, size=11, fill=(45, 45, 45), anchor="ra",
                            max_w=0.60 * iw)
                b2 = self.t((ir - 0.66 * iw, cy), str(a), size=11, fill=(60, 60, 60),
                            anchor="ra", max_w=0.32 * iw)
                h1 = max((b[3] - b[1]) for b in (b1, b2) if b) or 26
                b3 = self.t((ir - 0.05 * iw, cy + h1 + 3), dim, size=10,
                            fill=(120, 120, 120), anchor="ra", max_w=0.93 * iw)
                cy += h1 + 3 + ((b3[3] - b3[1]) if b3 else 22) + 13
        # یادداشت‌ها — شکستنِ سطر بر پایهٔ پهنا
        cy += 18
        for n in notes:
            b = self.t((ir, cy), n, size=10, fill=(85, 85, 85), anchor="ra", max_w=iw)
            if b:
                cy += (b[3] - b[1]) + 14

    def frame(self):
        self.d.rectangle([0, 0, A3W - 1, A3H - 1], outline=(70, 70, 70), width=6)
        self.d.rectangle([8 * MM, 8 * MM, A3W - 8 * MM, A3H - 8 * MM],
                         outline=(70, 70, 70), width=LW[2])
        self.d.rectangle([MARGIN, MARGIN, MARGIN + DRAW_W, MARGIN + DRAW_H],
                         outline=(150, 150, 150), width=LW[1])
        # قطب‌نما
        nx, ny = MARGIN + 1.6 * MM + 46, A3H - MARGIN - 1.6 * MM - 46
        self.d.ellipse([nx - 46, ny - 46, nx + 46, ny + 46], outline=(70, 70, 70), width=LW[1])
        self.d.polygon([(nx, ny - 40), (nx - 15, ny + 26), (nx, ny + 12), (nx + 15, ny + 26)],
                       fill=(60, 60, 60))
        self.t((nx, ny - 60), "شمال", size=10, fill=(50, 50, 50))
        # مقیاسِ خطی (۵ متر)
        m5 = 5.0 * self.sc
        sx, sy = MARGIN + 0.6 * MM + 130, A3H - MARGIN - 1.6 * MM - 26
        for i in range(5):
            self.d.rectangle([sx + i * m5 / 5, sy, sx + (i + 1) * m5 / 5, sy + 20],
                             fill=(60, 60, 60) if i % 2 == 0 else (252, 251, 247),
                             outline=(60, 60, 60), width=LW[1])
        self.t((sx, sy - 16), "۰", size=10, anchor="lm")
        self.t((sx + m5, sy - 16), "۵ متر", size=10, anchor="lm")
        self.t((sx + m5 / 2, sy + 34), f"مقیاس ۱:{self.sd}", size=11, bold=True)

    def save(self, path):
        self.img.save(path, dpi=(DPI, DPI))
        print("  ذخیره:", os.path.basename(path), f"({self.img.size[0]}×{self.img.size[1]})")
        return path


def _ovl(a, b, tol=4.0):
    """آیا دو جعبه بیش از tol پیکسل هم‌پوشانی دارند؟"""
    return (min(a[2], b[2]) - max(a[0], b[0]) > tol and
            min(a[3], b[3]) - max(a[1], b[1]) > tol)


def _wrap_px(s, font, max_w):
    """شکستنِ سطر بر پایهٔ پهنایِ واقعی به پیکسل — نه تعدادِ کاراکتر"""
    words = s.split()
    if not words:
        return [s]
    lines, cur = [], words[0]
    for w in words[1:]:
        trial = cur + " " + w
        if font.getlength(trial) <= max_w:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines


# ================================================================ برگه‌ها
def sheet_typical():
    s = PM.summary()
    liv = [r for r in PM.ROOMS if r[1] == "living"][0]
    sh = A3Sheet("پلان طبقهٔ تیپ", f"طبقات ۱ تا ۵ — ۲ واحد {s['unit_sale']} m²", "+۵٫۴۰", "A-۱۰۳",
                 -2.2, PM.BALC_Y0 - 1.9, PM.BLD_W + 2.4, PM.ENC_Y1 + 2.2, 75)
    # ایوان‌ها
    for offx, mir in ((0.0, False), (PM.UNIT_B_X, True)):
        x0 = (offx + PM.UW - liv[4]) if mir else (offx + liv[2])
        w = liv[4] - liv[2]
        sh.rect(x0, PM.BALC_Y0, x0 + w, PM.ENC_Y0, fill=(252, 246, 224), outline=(170, 130, 40), w=1)
        m = sh.M(x0 + w / 2, (PM.BALC_Y0 + PM.ENC_Y0) / 2)
        sh.t_free((m[0], m[1] - 0.28 * sh.sc), "ایوان", size=13, fill=(120, 85, 20), bold=True)
        sh.t_free((m[0], m[1] + 0.28 * sh.sc), f"{s['balcony']} m² (۵۰٪ در تراکم)", size=10,
             fill=(120, 85, 20))
        sh.line([(x0, PM.BALC_Y0), (x0 + w, PM.BALC_Y0)], fill=(150, 110, 40), w=3)
    # هسته و واحدها
    draw_unit_shell(sh, 0.0, False)
    draw_unit_shell(sh, PM.UNIT_B_X, True)
    for x0, y0, x1, y1, t in [(0, PM.ENC_Y0, PM.BLD_W, PM.ENC_Y0, PM.T_EXT),
                              (0, PM.ENC_Y1, PM.BLD_W, PM.ENC_Y1, PM.T_EXT),
                              (0, PM.ENC_Y0, 0, PM.ENC_Y1, PM.T_EXT),
                              (PM.BLD_W, PM.ENC_Y0, PM.BLD_W, PM.ENC_Y1, PM.T_EXT),
                              (PM.CORE_X0, PM.ENC_Y0, PM.CORE_X0, PM.ENC_Y1, PM.T_CORE),
                              (PM.CORE_X1, PM.ENC_Y0, PM.CORE_X1, PM.ENC_Y1, PM.T_CORE)]:
        sh.wall(x0, y0, x1, y1, t)
    draw_core(sh)
    draw_unit_openings(sh, 0.0, False)
    draw_unit_openings(sh, PM.UNIT_B_X, True)
    draw_unit_fixtures(sh, 0.0, False)
    draw_unit_fixtures(sh, PM.UNIT_B_X, True)
    # ابعاد
    for i, x in enumerate([0, PM.UW, PM.CORE_X1, PM.BLD_W]):
        sh.axis(x, PM.ENC_Y1 + 1.3, ["A", "B", "C", "D"][i])
    sh.dimh(0, PM.UW, PM.BALC_Y0 - 0.75, f"{PM.UW:.2f}")
    sh.dimh(PM.UW, PM.CORE_X1, PM.BALC_Y0 - 0.75, f"{PM.CORE_W:.2f}")
    sh.dimh(PM.CORE_X1, PM.BLD_W, PM.BALC_Y0 - 0.75, f"{PM.UW:.2f}")
    sh.dimh(0, PM.BLD_W, PM.BALC_Y0 - 1.65, f"{PM.BLD_W:.2f}")
    sh.dimv(PM.BALC_Y0, PM.ENC_Y0, PM.BLD_W + 0.95, "۲.۴۰")
    sh.dimv(PM.ENC_Y0, PM.ENC_Y1, PM.BLD_W + 0.95, "۸.۳۰")
    sh.dimv(PM.BALC_Y0, PM.ENC_Y1, PM.BLD_W + 1.95, f"{PM.BALC_D + PM.UD:.2f}")
    sh.level_mark(-1.2, PM.ENC_Y1, "+۵.۴۰")
    sh.frame()
    sched = [(r["name"], f"{r['area']:.2f}", f"{r['x1']-r['x0']:.2f}×{r['y1']-r['y0']:.2f}")
             for r in PM.unit_rooms(0.0)]
    sched += [("ایوان", f"{s['balcony']:.2f}", f"{liv[4]-liv[2]:.2f}×{PM.BALC_D:.2f}"),
              ("پله/آسانسور/پاگرد", f"{s['core_net']:.2f}", "—"),
              ("شفت نور و تهویه", f"{PM.SH_W*PM.SH_D:.1f}", f"{PM.SH_W:.2f}×{PM.SH_D:.2f}")]
    sh.strip([("عنوان نقشه", "پلان طبقهٔ تیپ"), ("تراز", "+۵.۴۰ متر"),
              ("مقیاس", f"۱:{sh.sd}"), ("شماره برگه", sh.no), ("تاریخ", "۱۴۰۵/۰۶/۲۷"),
              ("زیربنا", f"{s['per_floor']} m²")],
             sched,
             ["دیوار پیرامونی ۳۰cm · هسته و همسایگی ۲۵cm · تیغه ۱۵cm",
              "ارتفاع طبقه ۲.۹۰ m · پلهٔ رفت‌وبرگشتی ۱۶ پله (۱۸.۱×۲۹cm)",
              "سرویس از داخل حمام باز می‌شود (جایگزین: ادغام = ۶.۹ m²)",
              f"هر واحد {s['unit_sale']} m² = {s['unit_encl']} بسته + {s['balcony']} ایوان"])
    return sh.save(os.path.join(OUT, "A3-03-طبقه-تیپ.png"))


def sheet_ground():
    s = PM.summary()
    sh = A3Sheet("پلان همکف / پیلوت", "۳ مغازه + پارکینگ + هستهٔ عمودی", "±0.00", "A-۱۰۱",
                 -2.6, PM.Y0 - 2.4, PM.LAND_W + 2.6, PM.Y1 + 3.0, 150)
    sh.rect(0, PM.Y0, PM.LAND_W, PM.Y1, fill=(255, 255, 255), outline=(120, 120, 120), w=2)
    sh.rect(0, 0, PM.LAND_W, PM.Y0, fill=(228, 242, 228), outline=(120, 170, 120), w=1)
    sh.dimh(0, PM.BLD_W, PM.Y0 - 0.85, f"{PM.BLD_W:.2f}")
    sh.dimh(PM.SHOP_X0, PM.LAND_W, PM.Y0 - 0.85, f"{PM.LAND_W-PM.SHOP_X0:.2f}")
    sh.dimh(0, PM.LAND_W, PM.Y0 - 1.9, f"{PM.LAND_W:.2f}")
    sh.dimv(PM.Y0, PM.Y1, PM.LAND_W + 0.9, "۱۰.۷۰")
    sh.dimv(0, PM.Y0, PM.LAND_W + 0.9, "۲.۶۷")
    sh.level_mark(-1.5, PM.Y1, "±0.00")
    m = sh.M(PM.LAND_W / 2, PM.Y0 / 2)
    sh.t_free(m, "فضای باز جنوبی ۲.۶۷ m + حریم دکل فشارقوی ۷.۰۸ m", size=10, fill=(40, 100, 50))
    sh.rect(0, PM.Y0, PM.SHOP_X0, PM.Y1, fill=(238, 243, 250))
    n = 0
    for bay in (0.6, PM.CORE_X1 + 0.5):
        for i in range(3):
            if bay + i * 2.65 + PM.PARK_W > PM.SHOP_X0 - 0.2:
                break
            n += 1
            x0 = bay + i * 2.65
            sh.rect(x0, PM.Y0 + 0.6, x0 + PM.PARK_W, PM.Y0 + 0.6 + PM.PARK_L,
                    fill=(255, 255, 255), outline=(105, 135, 185), w=1)
            m = sh.M(x0 + 1.25, PM.Y0 + 3.2)
            sh.t_free(m, str(n), size=11, fill=(90, 120, 170))
    for tx, ty in ((5.0, PM.Y1 - 1.6), (18.5, PM.Y1 - 1.6)):
        m = sh.M(tx, ty)
        sh.t_free(m, "مسیر تردد و مانور", size=10, fill=(70, 100, 150))
    sh.rect(PM.CORE_X0, PM.Y1 - 5.10, PM.CORE_X1, PM.Y1, fill=(246, 246, 250),
            outline=(90, 90, 90), w=1)
    m = sh.M((PM.CORE_X0 + PM.CORE_X1) / 2, PM.Y1 - 2.5)
    sh.t_free(m, "لابی · پله · آسانسور", size=10, fill=(80, 80, 90))
    for i in range(PM.NSHOP):
        x0 = PM.SHOP_X0 + i * PM.SHOP_W
        sh.rect(x0, PM.Y1 - PM.SHOP_DEEP, x0 + PM.SHOP_W, PM.Y1, fill=(253, 243, 224),
                outline=(165, 115, 45), w=1)
        m = sh.M(x0 + PM.SHOP_W / 2, PM.Y1 - PM.SHOP_DEEP / 2)
        sh.t_free((m[0], m[1] - 0.92 * sh.sc), f"مغازه {i+1}", size=12, fill=(120, 80, 20), bold=True)
        sh.t_free((m[0], m[1]), f"{s['shop_area']} m²", size=10, fill=(120, 80, 20))
        sh.t_free((m[0], m[1] + 0.92 * sh.sc), f"نیم‌طبقه {PM.SHOP_W*PM.MEZ_DEEP:.1f} m² (خط‌چین)",
             size=10, fill=(150, 110, 50))
        sh.window(x0 + 1.6, PM.Y1, x0 + 1.6 + 2.8, PM.Y1, 0.3)
        for k in range(int(PM.MEZ_DEEP / 0.7)):
            yy = PM.Y1 - PM.SHOP_DEEP + k * 0.7
            sh.d.line([sh.M(x0 + 0.2, yy), sh.M(x0 + 0.2, yy + 0.4)], fill=(165, 115, 45), width=LW[1])
            sh.d.line([sh.M(x0 + PM.SHOP_W - 0.2, yy), sh.M(x0 + PM.SHOP_W - 0.2, yy + 0.4)],
                      fill=(165, 115, 45), width=LW[1])
        for k in range(int((PM.SHOP_W - 0.4) / 1.0)):
            xx = x0 + 0.2 + k * 1.0
            sh.d.line([sh.M(xx, PM.Y1 - 0.2), sh.M(xx + 0.6, PM.Y1 - 0.2)], fill=(165, 115, 45), width=LW[1])
            sh.d.line([sh.M(xx, PM.Y1 - PM.MEZ_DEEP), sh.M(xx + 0.6, PM.Y1 - PM.MEZ_DEEP)],
                      fill=(165, 115, 45), width=LW[1])
    sh.rect(PM.SHOP_X0, PM.Y0, PM.LAND_W, PM.Y1 - PM.SHOP_DEEP, fill=(246, 246, 240),
            outline=(170, 170, 170), w=1)
    m = sh.M((PM.SHOP_X0 + PM.LAND_W) / 2, PM.Y0 + 1.4)
    sh.t_free(m, "انبار و سرویس مغازه‌ها", size=10, fill=(90, 90, 90))
    sh.d.polygon([sh.M(1.4, PM.Y1 + 2.4), sh.M(1.4, PM.Y1), sh.M(4.6, PM.Y1)],
                 outline=(200, 120, 40), width=LW[2])
    sh.t_free(sh.M(3.0, PM.Y1 + 3.2), "ورودی خودرو", size=10, fill=(200, 120, 40))
    sh.d.polygon([sh.M(PM.CORE_X0 + 1.6, PM.Y1 + 2.4), sh.M(PM.CORE_X0 + 1.6, PM.Y1),
                  sh.M(PM.CORE_X0 + 4.2, PM.Y1)], outline=(60, 90, 160), width=LW[2])
    sh.t_free(sh.M(PM.CORE_X0 + 3.0, PM.Y1 + 3.2), "ورودی پیاده", size=10, fill=(60, 90, 160))
    sh.frame()
    sh.strip([("عنوان نقشه", "پلان همکف / پیلوت"), ("تراز", "±0.00 متر"),
              ("مقیاس", f"۱:{sh.sd}"), ("شماره برگه", sh.no), ("تاریخ", "۱۴۰۵/۰۶/۲۷"),
              ("زیربنا", f"{s['ground']} m²")],
             [("مغازه ۱", f"{s['shop_area']:.2f}", f"{PM.SHOP_W:.2f}×{PM.SHOP_DEEP:.2f}"),
              ("مغازه ۲", f"{s['shop_area']:.2f}", f"{PM.SHOP_W:.2f}×{PM.SHOP_DEEP:.2f}"),
              ("مغازه ۳", f"{s['shop_area']:.2f}", f"{PM.SHOP_W:.2f}×{PM.SHOP_DEEP:.2f}"),
              ("انبار/سرویس", f"{(PM.LAND_W-PM.SHOP_X0)*PM.SVC_DEEP:.1f}", "—"),
              ("پارکینگ", f"{n} فضا", "۲.۵۰×۵.۰۰"),
              ("لابی و هسته", "۲۱.۴", "۴.۲۰×۵.۱۰")],
             ["ارتفاع مفید پیلوت ۲.۴۰ m ⇒ معاف از تراکم",
              "ارتفاع مغازه ۵.۴۰ m با نیم‌طبقه در تراز ۲.۶۰+",
              f"نیاز واقعی پارکینگ ۱۲ تا ۱۴ فضا؛ اینجا {n} فضا",
              "کسری با زیرزمین یا جریمهٔ تبصره ۵ ماده ۱۰۰ جبران شود"])
    return sh.save(os.path.join(OUT, "A3-01-همکف.png"))


def sheet_mezz():
    s = PM.summary()
    sh = A3Sheet("پلان نیم‌طبقه و انباری", "تراز ۲.۶۰+ — معاف از تراکم", "+۲.۶۰", "A-۱۰۲",
                 -2.6, PM.Y0 - 2.4, PM.LAND_W + 2.6, PM.Y1 + 3.0, 150)
    sh.rect(0, PM.Y0, PM.LAND_W, PM.Y1, fill=(255, 255, 255), outline=(120, 120, 120), w=2)
    sh.rect(0, PM.Y0, PM.SHOP_X0, PM.Y1, fill=(250, 247, 238))
    for i in range(PM.ANB_N):
        x0 = 0.5 + i * 2.60
        if x0 + PM.ANB_W > PM.SHOP_X0 - 0.3:
            break
        sh.rect(x0, PM.Y0 + 0.4, x0 + PM.ANB_W, PM.Y0 + 0.4 + PM.ANB_D, fill=(255, 255, 255),
                outline=(150, 130, 90), w=1)
        m = sh.M(x0 + PM.ANB_W / 2, PM.Y0 + 1.5)
        sh.t_free(m, f"{i+1}", size=10, fill=(120, 100, 60))
    m = sh.M(11.0, PM.Y0 + 4.8)
    sh.t_free(m, "راهرو انباری‌ها (۱.۲۰ m)", size=10, fill=(120, 100, 60))
    m = sh.M(11.0, PM.Y1 - 2.0)
    sh.t_free(m, "فضای باز — نورگیر پارکینگ", size=10, fill=(110, 130, 110))
    for i in range(PM.NSHOP):
        x0 = PM.SHOP_X0 + i * PM.SHOP_W
        sh.rect(x0, PM.Y1 - PM.MEZ_DEEP, x0 + PM.SHOP_W, PM.Y1, fill=(253, 243, 224),
                outline=(165, 115, 45), w=1)
        m = sh.M(x0 + PM.SHOP_W / 2, PM.Y1 - PM.MEZ_DEEP / 2)
        sh.t_free((m[0], m[1] - 0.5 * sh.sc), f"نیم‌طبقه {i+1}", size=12, fill=(120, 80, 20), bold=True)
        sh.t_free((m[0], m[1] + 0.5 * sh.sc), f"{PM.SHOP_W*PM.MEZ_DEEP:.1f} m²", size=10, fill=(120, 80, 20))
    sh.rect(PM.SHOP_X0, PM.Y0, PM.LAND_W, PM.Y1 - PM.MEZ_DEEP, fill=(246, 246, 240),
            outline=(170, 170, 170), w=1)
    sh.rect(PM.CORE_X0, PM.Y1 - 5.10, PM.CORE_X1, PM.Y1, fill=(246, 246, 250),
            outline=(90, 90, 90), w=1)
    m = sh.M((PM.CORE_X0 + PM.CORE_X1) / 2, PM.Y1 - 2.5)
    sh.t_free(m, "هسته (پله و آسانسور)", size=10, fill=(80, 80, 90))
    sh.dimh(0, PM.SHOP_X0, PM.Y0 - 0.85, f"{PM.SHOP_X0:.2f}")
    sh.dimh(PM.SHOP_X0, PM.LAND_W, PM.Y0 - 0.85, f"{PM.LAND_W-PM.SHOP_X0:.2f}")
    sh.dimv(PM.Y0, PM.Y1, PM.LAND_W + 0.9, "۱۰.۷۰")
    sh.level_mark(-1.5, PM.Y1, "+۲.۶۰")
    sh.frame()
    sh.strip([("عنوان نقشه", "نیم‌طبقه و انباری"), ("تراز", "+۲.۶۰ متر"),
              ("مقیاس", f"۱:{sh.sd}"), ("شماره برگه", sh.no), ("تاریخ", "۱۴۰۵/۰۶/۲۷"),
              ("زیربنا", f"{s['anb']} m² انباری")],
             [("انباری (۸ واحد)", f"{s['anb']:.1f}", "۵.۰ m² هرکدام"),
              ("نیم‌طبقه ۱", f"{PM.SHOP_W*PM.MEZ_DEEP:.1f}", f"{PM.SHOP_W:.2f}×{PM.MEZ_DEEP:.2f}"),
              ("نیم‌طبقه ۲", f"{PM.SHOP_W*PM.MEZ_DEEP:.1f}", f"{PM.SHOP_W:.2f}×{PM.MEZ_DEEP:.2f}"),
              ("نیم‌طبقه ۳", f"{PM.SHOP_W*PM.MEZ_DEEP:.1f}", f"{PM.SHOP_W:.2f}×{PM.MEZ_DEEP:.2f}")],
             ["نیم‌طبقه تا ۵۵٪ مساحت مغازه مجاز است",
              f"تنها ۲۰٪ آن ({s['mezz_counted']} m² از {s['mez_phys']} m²) در تراکم",
              "انباری با ارتفاع مفید ۲.۲۰ m کاملاً معاف از تراکم",
              "ارتفاع مفید نیم‌طبقه ۲.۵۰ m"])
    return sh.save(os.path.join(OUT, "A3-02-نیم‌طبقه-و-انباری.png"))


def sheet_roof():
    s = PM.summary()
    sh = A3Sheet("پلان بام", "عایق‌کاری، شیب‌بندی و جان‌پناه", f"+{PM.TOP:.2f}", "A-۱۰۴",
                 -2.6, PM.Y0 - 2.4, PM.LAND_W + 2.6, PM.Y1 + 3.0, 150)
    sh.rect(0, PM.Y0, PM.LAND_W, PM.Y1, fill=(252, 251, 247), outline=(120, 120, 120), w=2)
    sh.rect(0, PM.ENC_Y0, PM.BLD_W, PM.ENC_Y1, fill=(238, 238, 234), outline=(90, 90, 90), w=2)
    m = sh.M(PM.BLD_W / 2, (PM.ENC_Y0 + PM.ENC_Y1) / 2)
    sh.t_free((m[0], m[1] - 0.6 * sh.sc), "بام مسکونی", size=13, fill=(60, 60, 70), bold=True)
    sh.t_free((m[0], m[1] + 0.6 * sh.sc), "شیب ۱٪ به سمت آبروهای جنوبی", size=10, fill=(90, 90, 100))
    sh.rect(PM.BLD_W, PM.Y0, PM.LAND_W, PM.Y1, fill=(224, 240, 224), outline=(90, 130, 90), w=2)
    m = sh.M((PM.BLD_W + PM.LAND_W) / 2, (PM.Y0 + PM.Y1) / 2)
    sh.t_free((m[0], m[1] - 0.6 * sh.sc), "تراس پودیوم", size=13, fill=(35, 95, 45), bold=True)
    sh.t_free((m[0], m[1] + 0.6 * sh.sc), f"{round((PM.LAND_W-PM.BLD_W)*PM.PODIUM_D)} m²",
         size=10, fill=(35, 95, 45))
    z = {c["kind"]: c for c in PM.core_zones()}
    shf, st, lf = z["shaft"], z["stair"], z["lift"]
    sh.rect(shf["x0"], shf["y0"], shf["x1"], shf["y1"], fill=(160, 200, 160),
            outline=(60, 120, 60), w=2)
    m = sh.M((shf["x0"] + shf["x1"]) / 2, (shf["y0"] + shf["y1"]) / 2)
    sh.t_free((m[0], m[1] - 0.4 * sh.sc), "دهانه شفت", size=11, fill=(30, 90, 40), bold=True)
    sh.t_free((m[0], m[1] + 0.5 * sh.sc), f"{PM.SH_W:.2f} × {PM.SH_D:.2f}", size=10, fill=(30, 90, 40))
    sh.rect(st["x0"], st["y0"], lf["x1"], st["y1"], fill=(246, 246, 250), outline=(90, 90, 90), w=2)
    m = sh.M((st["x0"] + lf["x1"]) / 2, (st["y0"] + st["y1"]) / 2)
    sh.t_free(m, "اتاقک پله و آسانسور", size=11, fill=(70, 70, 90))
    for (x0, y0, x1, y1) in [(0, PM.ENC_Y0, PM.BLD_W, PM.ENC_Y0), (0, PM.ENC_Y1, PM.BLD_W, PM.ENC_Y1),
                             (0, PM.ENC_Y0, 0, PM.ENC_Y1), (PM.BLD_W, PM.ENC_Y0, PM.BLD_W, PM.ENC_Y1)]:
        sh.wall(x0, y0, x1, y1, 0.25, fill=(90, 90, 90))
    m = sh.M(PM.BLD_W / 2, PM.ENC_Y1 + 0.8)
    sh.t_free(m, "جان‌پناه ۱.۰۰ m", size=10, fill=(90, 90, 90))
    sh.dimh(0, PM.BLD_W, PM.Y0 - 0.85, f"{PM.BLD_W:.2f}")
    sh.dimh(PM.BLD_W, PM.LAND_W, PM.Y0 - 0.85, f"{PM.LAND_W - PM.BLD_W:.2f}")
    sh.dimv(PM.Y0, PM.Y1, PM.LAND_W + 0.9, "۱۰.۷۰")
    sh.level_mark(-1.5, PM.Y1, f"+{PM.TOP:.2f}")
    sh.frame()
    sh.strip([("عنوان نقشه", "پلان بام"), ("تراز", f"+{PM.TOP:.2f} متر"),
              ("مقیاس", f"۱:{sh.sd}"), ("شماره برگه", sh.no), ("تاریخ", "۱۴۰۵/۰۶/۲۷"),
              ("ارتفاع کل", f"{s['height']} m")],
             [("بام مسکونی", f"{PM.BLD_W*PM.UD:.1f}", f"{PM.BLD_W:.2f}×{PM.UD:.2f}"),
              ("تراس پودیوم", f"{round((PM.LAND_W-PM.BLD_W)*PM.PODIUM_D)}", f"{PM.LAND_W-PM.BLD_W:.2f}×۱۰.۷۰"),
              ("اتاقک پله/آسانسور", f"{(lf['x1']-st['x0'])*(st['y1']-st['y0']):.1f}", "—"),
              ("دهانه شفت", f"{PM.SH_W*PM.SH_D:.1f}", f"{PM.SH_W:.2f}×{PM.SH_D:.2f}")],
             [f"ارتفاع تمام‌شده {s['height']} m (پودیوم ۵.۴۰ + ۵×۲.۹۰ + جان‌پناه ۱.۰۰)",
              "موتورخانه و منبع آب با ارتفاع مفید زیر ۲.۲۰ ⇒ معاف از تراکم",
              "دهانه شفت تا بام ادامه یابد و با کلاهک باران‌گیر پوشش شود"])
    return sh.save(os.path.join(OUT, "A3-04-بام.png"))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    print("ساختِ برگه‌های A3 (۳۰۰ DPI):")
    paths = [sheet_ground(), sheet_mezz(), sheet_typical(), sheet_roof()]
    # PDF
    from reportlab.lib.pagesizes import A3, landscape
    from reportlab.pdfgen import canvas as _c2
    from reportlab.lib.utils import ImageReader
    pdf = os.path.join(OUT, "تمام-طبقات-A3.pdf")
    W, H = landscape(A3)
    cv = _c2.Canvas(pdf, pagesize=landscape(A3))
    cv.setTitle("پلان‌های معماری — هر طبقه روی یک ورق A3")
    for p in paths:
        cv.drawImage(ImageReader(p), 0, 0, width=W, height=H)
        cv.showPage()
    cv.save()
    for p in paths:
        single = p.replace(".png", ".pdf")
        cv = _c2.Canvas(single, pagesize=landscape(A3))
        cv.drawImage(ImageReader(p), 0, 0, width=W, height=H)
        cv.showPage(); cv.save()
    print("PDF چندصفحه‌ای:", os.path.basename(pdf))
    print("ابعاد:", f"{A3W}×{A3H} پیکسل = ۴۲۰×۲۹۷ mm در ۳۰۰ DPI")
