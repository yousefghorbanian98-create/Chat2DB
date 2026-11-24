# اعتبار منابع و snapshotها

این پوشه برای شروع بیلدری است که سابقهٔ گفتگو را ندارد؛ **source snapshot شاهد اجرای محصول نیست**.

- کد محصول در `yousefghorbanian98-create/MP` و SHA مشاهده‌شده `35d4b35184b4148c658b415bd009fc076bf24e00` است.
- checkout فعلی Chat2DB پوشهٔ `mp-app/` ندارد. هیچ clone، merge، branch switch یا تغییر در MP برای ساخت این بسته انجام نشد؛ مطالعهٔ منابع با GitHub API و `gh` بود.
- `SOURCE_MANIFEST.json` مسیر، SHA، hash و URL هر manifest/snapshot بازتوزیع‌شده را ثبت می‌کند. فایل‌های `.source.txt` **پیکربندی فعال نیستند**؛ کپی‌شان روی محصول یا اجرای دستور نصب از داخلشان خودکار مجاز نیست.
- `MP_SOURCE_INVENTORY.json` مسیرهای ۱۷ feature و تست‌های Flutter را از tree همان SHA دارد؛ **کد و خروجی تست نیست**.
- `mp-api-routes.snapshot.json` و `MP_API_OPERATIONS.csv`: ۱۴۱ path و ۱۶۳ operation اعلام‌شده در منبع. `roles`/`scopes`/`always_roles` با هم و با guard/service بررسی شوند. این فایل OpenAPI DTOها یا اثبات دسترسی live نیست.
- کاتالوگ‌های GitHub/npm/PyPI در 2026-11-24 مشاهده شدند. GitHub HEAD، commit مطالعهٔ منبع است، نه الزاماً commit همان npm/binary release. نصب باید از نسخه/lock و asset معلوم انجام شود.
- `binary-releases.json` اسامی/URL assetهای واقعی release را دارد؛ binary در بسته نیست. checksum/امضای خود release و سازگاری سیستم‌عامل قبل از اجرا بررسی شود.
- کاتالوگ npm شامل نامزدهای آیندهٔ runtime هم هست؛ workspace ابزار فقط dependencyهای `tooling/*/package.json` را پین می‌کند. این فهرست نسخه، تصمیم upgrade برنامه یا گزارش security audit نیست.
- Ruff و وابستگی‌های backend از constraints خود MP بیایند. requirements ابزار Semgrep فقط نسخهٔ top-level را پین می‌کند؛ transitive Python lock/hash کامل نیست و پس از نصب باید محیط واقعی/نسخه‌ها ثبت شوند.

## منابعی که خوانده شدند ولی عمداً به عنوان دستور فعال بسته نشدند

PRD، OWNER-DECISIONS، RELEASE-CHECKLIST، HANDOFF-PROJECT، TODO-CLOUD-FINANCE-ACCESS، PLAN-MANUAL-TRANSFER، audit decisions، AGENTS، سیاست RBAC و route policy در MP؛ و اسناد handoff تاریخی Chat2DB در commit `d3936dab8e30c17299cfd12d5f0e6ca9a33e3b4a`.

اسناد آرشیوی دربارهٔ حذف Dart/Android، auto-merge، ECC، retention ثابت، یا scopeهای قدیمی ممکن است با محدودیت فعال تناقض داشته باشند. آن‌ها داخل دستور شروع کپی نشدند. محدودیت فعلیِ **حفظ Flutter/Android** و **ثبت baseline در ADR مالک** روشن است.

D-01..D-11 گفتگوی قبلی در این snapshotها با نگاشت معتبر بازیابی نشد؛ رجیستر آن‌ها رزرو است. Q-n جدید در این بسته را با D-n/AD-n/D-00n قدیمی یکی نکن.

## مجوز و داده

- فایل LICENSE منبع MP اختصاصی است؛ public بودن مخزن به معنی OSS بودن برنامه نیست. این بسته فقط بنا بر درخواست مالک آماده شده و مجوز محصول را تغییر نمی‌دهد.
- ابزارها جداگانه OSS هستند؛ مجوز engine، rules، enterprise، plugin، model weights و داده‌ها جدا بررسی شود.
- ابزار/مدل/Chromium/SDK، secret، DB، دادهٔ شخصی و عکس/فیش/پیام عضو در بسته نیست.
- هیچ عدد تست، پوشش، بار، تعداد کاربر یا deploy قدیمی به عنوان نتیجهٔ تازهٔ این تحویل معرفی نشده است.
