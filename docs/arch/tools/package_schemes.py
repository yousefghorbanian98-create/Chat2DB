#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""بسته‌بندیِ نهایی — هر طرح در پوشهٔ خودش، همه‌چیز داخلِ یک زیپ.

ساختارِ زیپ:
    طرح اول/  README.md · A3-پلان‌ها/ · مدل-سه‌بعدی/ · بلندر/(build_scene.py،
              scene.blend، راهنما، aerial) · رندر/
    طرح دوم/  همین ساختار
    + ششِ سندِ بالادستی در ریشه
"""
import os, sys, shutil, zipfile

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))      # docs/arch
ROOT = os.path.dirname(os.path.dirname(HERE))                            # repo
OUT_ZIP = os.path.join(ROOT, "Chat2DB-Arch-Package.zip")
STAGE = os.path.join("/home/user", "_pkg")

SCHEMES = [
    dict(folder="طرح اول", kind="shops",
         a3="A3-طرح-اول", model="مدل-سه‌بعدی-طرح-اول", blender="blender-طرح-اول",
         render_prefix="طرح-اول",
         title="طرح اول — مختلط: چهار مغازه در همکف + سه طبقهٔ مسکونی روی پیلوت",
         rows=[("برنامه", "همکفِ تجاری (۴ مغازه) + ۳ طبقهٔ مسکونی"),
               ("اشغالِ زمین", "433.9 m² (۸۰٪ از زمین 542.38 m²)"),
               ("زیربنایِ هر طبقه", "393.9 m² مشمولِ تراکم + 218.1 m²ِ تجاریِ همکف"),
               ("زیربنایِ کل", "1399.9 m²"),
               ("تراکم", "258.1٪ — مازاد بر ۱۸۰٪ : 424 m²"),
               ("واحدها", "12 واحد · 65.4 m² بسته + ایوان"),
               ("بلندی", "14.20 m (با پاراپت)"),
               ("پارکینگ", "13 فضا — زیرزمین و پشتِ مغازه‌ها"),
               ("مازاد", "جریمهٔ مادهٔ ۱۰۰ یا خریدِ تراکم؛ تخلفِ اصول ثلاثه نیست، تخریب ندارد")]),
    dict(folder="طرح دوم", kind="pilotis",
         a3="A3-طرح-دوم", model="مدل-سه‌بعدی-طرح-دوم", blender="blender-طرح-دوم",
         render_prefix="طرح-دوم",
         title="طرح دوم — تماماً مسکونی: سه طبقه روی پیلوتِ پارکینگ",
         rows=[("برنامه", "پیلوتِ پارکینگ + ۳ طبقهٔ مسکونی"),
               ("اشغالِ زمین", "433.9 m² (۸۰٪ از زمین 542.38 m²)"),
               ("زیربنایِ هر طبقه", "393.9 m² مشمولِ تراکم (واحد + هسته + راهرو + دیوار)"),
               ("زیربنایِ کل", "1181.8 m²"),
               ("تراکم", "217.9٪ — مازاد بر ۱۸۰٪ : 205 m²"),
               ("واحدها", "12 واحد · 65.4 m² بسته + ایوان"),
               ("بلندی", "12.30 m (با پاراپت)"),
               ("پارکینگ", "13 فضا در پیلوت — ارتفاعِ مفید 2.60 m"),
               ("مازاد", "جریمهٔ مادهٔ ۱۰۰ یا خریدِ تراکم؛ تخلفِ اصول ثلاثه نیست، تخریب ندارد")]),
]

ROOT_DOCS = ["سقف-طبقه-بازنگری.md", "مذاکره-طرح-دوم.md", "PROMPT-MASTER.md",
             "regulations-compendium.md"]




def cp(src, dst):
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    shutil.copy2(src, dst)


def build_scheme(s):
    d = os.path.join(STAGE, s["folder"])
    if os.path.isdir(d):
        shutil.rmtree(d)
    # پلان‌های A3
    a3 = os.path.join(HERE, s["a3"])
    for f in sorted(os.listdir(a3)):
        cp(os.path.join(a3, f), os.path.join(d, "A3-پلان‌ها", f))
    # مدل و DXF
    mdl = os.path.join(HERE, s["model"])
    for f in sorted(os.listdir(mdl)):
        cp(os.path.join(mdl, f), os.path.join(d, "مدل-سه‌بعدی", f))
    # بلندر
    bl = os.path.join(HERE, s["blender"])
    for f in ("build_scene.py", "scene.blend", "aerial_z19.jpg", "راهنما-بلندر.md"):
        q = os.path.join(bl, f)
        if os.path.exists(q):
            cp(q, os.path.join(d, "بلندر", f))
    top = os.path.join(HERE, "blender-README.md")
    if os.path.exists(top):
        cp(top, os.path.join(d, "بلندر", "راهنمای-ساخت-سه‌بعدی.md"))
    # رندرهایِ راستی‌آزمایی‌شده
    rd = os.path.join(HERE, "رندرها")
    made = []
    if os.path.isdir(rd):
        for f in sorted(os.listdir(rd)):
            if f.startswith(s["render_prefix"]) and f.endswith(".jpg"):
                cp(os.path.join(rd, f), os.path.join(d, "رندر", f))
                made.append(f)
    # README
    t = ["# " + s["title"], "", "## جدولِ مشخصات", "", "| ویژگی | مقدار |", "|---|---|"]
    t += ["| %s | %s |" % r for r in s["rows"]]
    t += ["", "## فایل‌ها", "",
          "| پوشه/فایل | چیست | چگونه استفاده شود |", "|---|---|---|"]
    t += ["| `A3-پلان‌ها/` | سه برگهٔ چاپیِ A3 (افقی، ۱:۱۵۰) + PDF | PDF را رویِ A3 چاپ کنید؛ PNG 4960×3507 برایِ پرینتِ ۳۰۰dpi است |",
          "| `مدل-سه‌بعدی/model.obj` | حجمِ ساختمان با ۱۲ جنس | هر نرم‌افزارِ سه‌بعدی/موتورِ بازی |",
          "| `مدل-سه‌بعدی/final-plan.dxf` | پلان‌ها در اتوکد/CAD | واحد: متر، لایه‌بندی‌شده |",
          "| `بلندر/build_scene.py` | اسکریپتِ یک‌کلیک | بلندر → Scripting → Open → Run Script |",
          "| `بلندر/scene.blend` | صحنهٔ آماده (نتیجهٔ اجرای اسکریپت) | دو‌بار‌کلیک در بلندر |",
          "| `بلندر/aerial_z19.jpg` | بافتِ ماهواره‌ایِ زمین | کنارِ اسکریپت بماند |",
          "| `بلندر/راهنما-بلندر.md` | راهنمایِ اجرا و تنظیماتِ GTX 1650 | بخوانید |"]
    if made:
        t += ["| `رندر/` | %d رندرِ راستی‌آزمایی‌شده (1280×800، Cycles، JPGِ کیفیت ۸۸) | برایِ ارائه |" % len(made)]
    t += ["", "## سه برگهٔ A3 کدام‌اند",
          "۱) همکف (پیلوت/مغازه‌ها) · ۲) طبقهٔ نمونه · ۳) بام — هر برگه شاملِ کادر، شبکهٔ محور، "
          "زنجیرهٔ اندازه و جدولِ برنامه است و هیچ نوشته‌ای از کادر بیرون نمی‌زند.",
          "", "## دو عددی که قبل ازِ ساخت باید قطعی شود",
          "۱) آیا «۳ طبقه روی پیلوت» یعنی پیلوت جزوِ همان سه طبقه است یا جدا؟ "
          "اگر جدا باشد، یک طبقهٔ کامل مسکونی بیشتر به شما می‌رسد.",
          "۲) آیا ضلعِ شمالی زیرِ حریمِ خطِ برق است و سقفِ ارتفاع چقدر است؟",
          ""]
    open(os.path.join(d, "README.md"), "w", encoding="utf-8").write("\n".join(t))
    return len(made)


if __name__ == "__main__":
    if os.path.isdir(STAGE):
        shutil.rmtree(STAGE)
    os.makedirs(STAGE)
    counts = {s["folder"]: build_scheme(s) for s in SCHEMES}
    for f in ROOT_DOCS:
        p = os.path.join(HERE, f)
        if os.path.exists(p):
            cp(p, os.path.join(STAGE, f))
        else:
            print("  ! سندِ ریشه پیدا نشد:", f)
    if os.path.exists(OUT_ZIP):
        os.remove(OUT_ZIP)
    n = 0
    with zipfile.ZipFile(OUT_ZIP, "w", zipfile.ZIP_DEFLATED, compresslevel=6) as z:
        for base, _, files in os.walk(STAGE):
            for f in sorted(files):
                p = os.path.join(base, f)
                z.write(p, os.path.relpath(p, STAGE))
                n += 1
    print("زیپ نوشته شد:", OUT_ZIP)
    print("  فایل‌ها:", n, "· حجم: %.2f MB" % (os.path.getsize(OUT_ZIP) / 1048576))
    for s in SCHEMES:
        d = os.path.join(STAGE, s["folder"])
        k = sum(len(fs) for _, _, fs in os.walk(d))
        print("  %s: %d فایل · %d رندر" % (s["folder"], k, counts[s["folder"]]))
