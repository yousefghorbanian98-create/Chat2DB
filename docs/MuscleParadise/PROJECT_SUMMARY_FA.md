توضیح پروژهٔ «Muscle Paradise» برای کسی که اصلاً در جریان نیست

سلام. این متن به زبان ساده می‌گوید این برنامه چه بود، قرار بود چه کار کنیم و چه خروجی‌ای حاصل شده است.

۱) چه داشتیم؟

روی سرویس GitHub یک مخزن به نام

Chat2DB

وجود داشت و داخل آن، در پوشهٔ

docs/MuscleParadise

یک سند به نام «نقشهٔ مهندسی کامل» قرار داشت. این نقشه، مشخصاتِ یک سیستم مدیریت باشگاه بدن‌سازی (سیستم‌عامل باشگاه) به نام «Muscle Paradise» بود: از جدول‌های پایگاه داده و API ها و امنیت تا رابط کاربری، همه‌چیز را تعیین کرده بود. چند قانون الزام‌آور هم وجود داشت: برنامه باید «local-first» باشد (بدون ابرِ اجباری کار کند)؛ رابط باید فارسی-اول با تاریخ شمسی و واحد ریال باشد؛ دو محیط جدا ارائه شود — یکی برای ورزشکار و یکی برای مدیر؛ مصدومیت‌ها و محدودیت‌های بدنی باید فیلتر سختِ برنامه‌های تمرینی باشند؛ و بخش قدیمی‌تر مخزن (پروژهٔ

Cutting Edge

) نباید هرگز دستکاری شود.

۲) قرار بود چه کنیم؟

بر اساس یک روش کار به نام

FINN-LOOP v3.0

باید به صورت خودکار و حلقه‌ای (برنامه‌ریزی، پیاده‌سازی، تست، اشکال‌زدایی، commit، عملکرد، امنیت) محصول را جامع و کامل — نه در حد دمو — می‌ساختیم. شامل:

- اپ ورزشکار: کد QR برای حضور و غیاب، وضعیت عضویت، تاریخچهٔ پرداخت‌ها، ثبت ست‌های تمرین، مشاهدهٔ مصدومیت‌ها و محدودیت‌ها.
- اپ مدیر (Studio): مدیریت اعضا، آنالیز بدن با متد JP7، برنامه‌های تمرینی، پرداخت‌ها، گزارش‌ها.
- پل اتوماسیون به

n8n

برای اعلان‌هایی مثل انقضای عضویت، بدون ارسال اطلاعات هویتی/سلامتی (PHI).

- صفحهٔ فرود سینمایی با کیفیت بصری در سطح بهترین سایت‌های دنیا.
- فایل نصبی واقعی برای ویندوز و اندروید، به‌علاوهٔ نسخهٔ وب.
- سیستم ساخت خودکار (CI) روی GitHub تا با هر تگِ نسخه، فایل‌های نصبی توسط خودِ سرورهای GitHub تولید شوند.

۳) خروجی نهایی چه شد؟

نسخهٔ

0.20.0

به صورت Release روی همان مخزن ثبت شده و دو فایل نصبی دارد: نصب‌کنندهٔ ویندوز حدود ۸۴ مگابایت (قالب NSIS با پوستهٔ Electron) و نصب‌کنندهٔ اندروید. نسخهٔ وب هم به صورت زنده کار می‌کند. بک‌اند یک پایگاه دادهٔ ۲۶ جدولی با بیش از ۲۶۰ تست دارد و فرانت بیش از ۱۵۰ تست؛ و آخرین بیلد CI (تگ

v0.20.4

) کاملاً سبز بود: job ویندوز در ۱ دقیقه و ۴۲ ثانیه و job اندروید در ۵۵ ثانیه.

نکتهٔ مهم و صادقانه: این یک نسخهٔ واقعی، نصب‌پذیر و تست‌شده است — اما نسخهٔ نهاییِ صددرصد نیست؛ بخشی از امکانات سمت مدیر و برخی توسعه‌ها در نقشهٔ راه باقی مانده‌اند، و نصب‌کنندهٔ فعلی اندروید یک پوستهٔ WebView است که در اولین اجرا آدرس سرور را می‌گیرد.

اطلاعات ورود نسخهٔ زنده: کد ورزشکار

MP-DEMO-1

با پین

1234

؛ مدیر با نام

owner

و رمز

1111

.

۴) همهٔ لینک‌های مربوط به برنامه

نقشهٔ راه (نقشهٔ مهندسی کامل):

https://github.com/yousefghorbanian98-create/Chat2DB/blob/arena/01a04e9f-chat2db/docs/MuscleParadise/ENGINEERING_MAP_FULL_v1.md

صفحهٔ Release و فایل‌های نصبی:

https://github.com/yousefghorbanian98-create/Chat2DB/releases/tag/v0.20.0

لینک مستقیم نصب‌کنندهٔ ویندوز:

https://github.com/yousefghorbanian98-create/Chat2DB/releases/download/v0.20.0/Muscle.Paradise.Setup.0.20.0.exe

لینک مستقیم نصب‌کنندهٔ اندروید:

https://github.com/yousefghorbanian98-create/Chat2DB/releases/download/v0.20.0/app-debug.apk

شاخ پروژه روی GitHub:

https://github.com/yousefghorbanian98-create/Chat2DB/tree/arena/01a04e9f-chat2db

همین متن توضیح (نسخهٔ فایل):

https://github.com/yousefghorbanian98-create/Chat2DB/blob/arena/01a04e9f-chat2db/docs/MuscleParadise/PROJECT_SUMMARY_FA.md

تاریخچهٔ تغییرات (CHANGELOG):

https://github.com/yousefghorbanian98-create/Chat2DB/blob/arena/01a04e9f-chat2db/mp-app/CHANGELOG.md

وضعیت اجرای حلقه‌های کاری (LOOP_STATE):

https://github.com/yousefghorbanian98-create/Chat2DB/blob/arena/01a04e9f-chat2db/mp-app/LOOP_STATE.md

سیستم دیزاین:

https://github.com/yousefghorbanian98-create/Chat2DB/blob/arena/01a04e9f-chat2db/mp-app/DESIGN_SYSTEM.md

گزارش نهایی:

https://github.com/yousefghorbanian98-create/Chat2DB/blob/arena/01a04e9f-chat2db/mp-app/FINAL_REPORT.md

سند پل

n8n

:

https://github.com/yousefghorbanian98-create/Chat2DB/blob/arena/01a04e9f-chat2db/docs/MuscleParadise/N8N_AUTOMATION_BRIDGE.md

صفحهٔ بیلد سبز CI:

https://github.com/yousefghorbanian98-create/Chat2DB/actions/runs/33302638581

نسخهٔ وب زنده (ورزشکار):

https://8751-irn313b2bnugyheguk8ls.e2b.app/client.html

نسخهٔ وب زنده (مدیر):

https://8751-irn313b2bnugyheguk8ls.e2b.app/index.html

صفحهٔ پیش‌نمایش تصویری:

https://8751-irn313b2bnugyheguk8ls.e2b.app/preview.html
