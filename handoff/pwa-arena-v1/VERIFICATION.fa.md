# اعتبارسنجی این بسته — نه تأیید محصول

**تاریخ:** 2026-11-24 UTC · **محیط:** Linux، Python 3.11.2، Node 22.22.3، npm 10.9.8

## انجام‌شده با خروجی واقعی

| بررسی | فرمان/روش اجراشده | نتیجه و دامنه |
|---|---|---|
| هویت source محصول | `gh repo view` و GitHub API درخت/فایل MP | مخزن MP عمومی، snapshot `35d4b35184b4148c658b415bd009fc076bf24e00`؛ هیچ checkout/تغییر branch یا نوشتن در MP انجام نشد |
| inventory منبع | شمارش tree و routes.json پین‌شده | ۱۷ حوزه، ۱۴۱ path، ۱۶۳ operation اعلام‌شده؛ **نه live evidence** |
| مسیرهای طرح | تطبیق همهٔ source_paths طرح با tree پین‌شده | ۶۰ مسیر موجود بررسی شد؛ مسیر PWA جدید همچنان پیشنهادی است |
| منابع ابزار | API GitHub و registry npm/PyPI | منبع، مجوز هسته، HEAD و نسخه/engine/asset ثبت شدند؛ security audit کامل نیست |
| قفل Node ابزار | `npm install --package-lock-only --ignore-scripts --no-audit --no-fund` در هر دو workspace | موفق؛ dependency graph/lock تولید شد؛ ابزارها یا browser نصب و اجرا نشدند |
| سازگاری manifest و lock | `npm ci --dry-run --ignore-scripts --no-audit --no-fund` در هر دو workspace | موفق؛ **dry-run است، نه نصب واقعی**؛ در workspace ترسیم `PUPPETEER_SKIP_DOWNLOAD=1` نیز تنظیم بود |
| ساخت HTML و ZIP | `python handoff/build_pwa_handoff.py` با Markdown 3.11.3 در محیط مجزای docs | موفق؛ HTML آفلاین با تصویر embedشده، manifest داخلی و checksum بیرونی ساخته شدند |
| تست‌های تحویل | `python -m unittest discover -s handoff/tests -v` | **۲۵ تست، صفر failure/error/skip**؛ فقط ساختار طرح، scope، رجیستر، local links، locks، preflight، hash و ZIP |
| منطق fail-closed preflight | `python3 scripts/preflight.py --repo <Chat2DB checkout>` | **exit 2 / BLOCKED مورد انتظار**: این checkout فاقد source محصول MP است؛ به اسم محیط آماده قبول نشد |
| سینتکس JavaScript | `node --check` برای renderer و parse نمونهٔ dependency-cruiser با `vm.Script` | موفق؛ sample هنوز روی محصول/ابزار تحلیل اجرا نشده است |
| تصاویر | header PNG و XML parser برای SVG؛ مقایسهٔ بایت با تصاویر انتخاب‌شدهٔ قبلی | PNG برابر 3600×802؛ SVG معتبر؛ PNG/SVG/Mermaid اصلی عیناً حفظ شدند |
| HTML در Chromium | Puppeteer موجودِ محیط روی فایل HTML محلی، با مسدودکردن تمام درخواست‌های غیر file/data | desktop 1280 و mobile 390؛ RTL، decode تصویر و نبود overflow سند تأیید شد؛ **هیچ API/سرویس MP اجرا نشد** |
| سلامت ZIP | CRC، اسامی امن، تطبیق همهٔ payloadها با manifest و ساخت دوباره | موفق؛ دو ساخت با بایت یکسان؛ hash ZIP خارج ZIP است |
| الگوهای حساس | بررسی payload برای private-key block و الگوهای token GitHub، و منع DB/APK/EXE/KEY/PEM/node_modules | چیزی با این الگوها نبود؛ **این یک Gitleaks کامل یا گواهی نبود هر نوع secret نیست** |

سینتکس/منطق نمونه‌ها فقط در محدودهٔ بالا تأیید شده است. فایل‌های `.example` پیکربندی فعال محصول یا SAST کامل نیستند.

## عمداً اجرا نشده / UNKNOWN

- هیچ PWA محصول ساخته یا boot نشده است؛ همهٔ PWA-00..27 در JSON `PROPOSED` هستند.
- تست backend/Studio/Flutter/Android، contract live، RBAC runtime، دوربین/قفل دستگاه، پرداخت/فیش، service worker واقعی محصول و آزمون دستگاه اجرا نشده‌اند.
- Semgrep/dependency-cruiser/Knip/Playwright/k6/OSV/Gitleaks این طرح روی محصول اجرا نشده‌اند؛ ساخت lock یا syntax check جای آن‌ها نیست.
- نصب/اجرای OpenHands یا inference مدل، reviewer مستقل، بررسی مالی/حقوقی/بالینی و تأیید مالک برای تصمیم‌های باز انجام نشده‌اند.
- هیچ حساب/secret/DB تولیدی، پرداخت یا پیامک واقعی، deploy/rollback، تغییر grant/schema/retention یا حذف Flutter/Android در این کار انجام نشده است.
- hash و عدد تست تاریخ‌دار این سند را برای SHA دیگری به‌صورت خودکار معتبر فرض نکن؛ بیلدر محصول باید دوباره بسنجند.

## اثر خارجی مجاز و نحوهٔ انتشار

درخواست مالک فقط انتشار **این بسته** در GitHub است. روش تحویل: commit انتخابی و push به شاخهٔ همین نشست Chat2DB، سپس لینک raw پین‌شده به commit در پیام نهایی. **هیچ PR/merge/tag/Release/deploy محصول بخشی از این کار نیست.** SHA commit و نتیجهٔ تأیید بایت‌های remote بعد از push در پیام تحویل اعلام می‌شود؛ عمداً داخل خود ZIP self-reference ساخته نمی‌شود.

در authoring محلی، یک برچسب اضافی در مولد موقت طرح باعث `NameError` شد؛ اصلاح شد و ساخت و ۲۵ تست نهایی از نو موفق اجرا شدند. آن مولد موقت یا cacheهای پژوهش جزو بسته نیستند.
