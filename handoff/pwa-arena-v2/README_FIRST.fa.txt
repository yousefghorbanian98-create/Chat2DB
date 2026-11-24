Muscle Paradise — Arena Handoff v2.0.0 — 2026-11-24
برنامهٔ کامل اصلاح‌شدهٔ PWA، نه پیاده‌سازی یا گواه آمادگی محصول

مهم‌ترین اصلاح: مرجع این نسخه ۵۰ میکرولوپ ارسالی کاربر است، نه ۲۸ مورد v1 و نه شمارش اثبات‌نشدهٔ ۵۶.
شناسه‌ها gap و حرف دارند؛ PWA-56 آخرین شماره است، نه تعداد. هیچ موردی حذف/ادغام/بازشماره‌گذاری نشده.

هدف: mp-app/studio/ موجود به یک React PWA عضو + کارکنان توسعه یابد.
اپ React دوم نساز؛ staff موجود را adapt کن؛ رفتار عضو را از Flutter تدریجی منتقل کن.
Flutter/Android، اسناد/تست/CI/Flutter Web و Electron حذف/overwrite یا خاموش نشوند.

شروع بدون تاریخچه:
۱. HANDOFF.fa.html را باز کن: آفلاین، راست‌به‌چپ، بدون اسکریپت/شبکه، همراه دو نمودار و متن کامل ۵۰ کارت.
   نسخهٔ قابل‌ویرایش: HANDOFF.fa.md + MICROLOOPS.fa.md.
۲. SOURCE_PLAN.fa.md و COMPARISON_AND_CHANGELOG.fa.md را بخوان؛ مرجع ID/عنوان/AC اصلی و علت اصلاح روشن است.
۳. FINN_LOOP_FINAL.fa.md و DECISION_PACKAGE.fa.md را بخوان؛ ۹ حوزهٔ Finn + پنج گیت مستقل برای هر کارت/فرزند.
۴. templates/RESUME_PROMPT.fa.txt را همراه کل پوشه به Arena بده؛ از PWA-00 شروع کند.
۵. پیش از اجرا repo/شاخه/HEAD/AGENTS/صف جاریِ مجاز را تأیید کن؛ محصول در yousefghorbanian98-create/MP است.
   Chat2DB فقط میزبان بسته است؛ اینجا mp-app ندارد. pin بررسی منبع MP: c46e792657e361cd09799c896c47149b4a5c4d86.
   pin دستور checkout/reset/switch نیست. تغییرات دیگران محفوظ.
۶. Python 3.11+ برای کنترل خود بسته:
   sha256sum -c MANIFEST.sha256
   python3 scripts/sync_plan.py --check
   python3 scripts/make_roadmap.py --check
   python3 scripts/validate_package.py
   این فرمان‌ها محصول، DB، install یا شبکه را اجرا نمی‌کنند؛ PACKAGE_OK_NOT_QA یعنی فقط خود بسته معتبر است.
۷. برای inventory محصول: python3 scripts/preflight.py --repo /absolute/path/to/authorized/MP
   موفقیت inventory = INVENTORY_OK_NOT_QA؛ نه AGENT-READY. روی Chat2DB عمداً BLOCKED/exit 2.
۸. TOOLCHAIN.fa.md نصب ایزوله، منبع/نسخه/مجوز و کاربرد ابزارها را توضیح می‌دهد؛ install-all یا dependency محصول نیست.

هنوز هیچ کارت محصول این ZIP AGENT-READY/DONE نیست؛ همه PROPOSED و PWA-3F پیش‌فرض BLOCKED است.
جهت React معلوم است؛ مدل نقش/مجوز، session/storage، offline، release-baseline و staging از آن نتیجه نمی‌شوند.
D-01…D-11 اصل متن بازیابی‌شده دارند؛ پاسخ‌های قبلی معتبر در مقصد reconcile شوند، نه دوباره حدس زده شوند.
تصمیم کوچک برگشت‌پذیر در scope ثبت شود؛ سؤال واقعی یک‌جا و فقط وابسته BLOCKED، مستقلِ مجاز ادامه.
سه تلاش کل = اولیه + دو retry؛ ۹۰ دقیقه فقط پیشنهادِ نیازمند تصویب؛ هزینه/egress مکمل بدون اذن صفر.
UNKNOWN/NOT_RUN و defer ≠ PASS؛ self-review مستقل نیست؛ قرارداد مصوب، شاهد همان SHA، review و merge انسانی لازم.

این بسته مجوز push/PR/merge/deploy/release/rollback/DB/پرداخت واقعی/مدل ابری/افشای کد یا دادهٔ محصول نیست.
مجوز MP proprietary است؛ عمومی‌بودن مخزن مجوز مستقل بازتوزیع یا egress نیست.
گزارش اجرای واقعیِ فقط بسته و محدودیت‌ها: VERIFICATION.fa.md.
تمامیت تمام فایل‌ها: PACKAGE_MANIFEST.json و MANIFEST.sha256؛ checksum خود ZIP بیرون آن است.
