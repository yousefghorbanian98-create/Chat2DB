# اعتبارسنجی بستهٔ v2.0.0 — نه QA یا Go محصول

**تاریخ:** 2026-11-24. **محیط:** مخزن تحویل Chat2DB، شاخهٔ `arena/d885a3c9-chat2db`، والد تحویل پیشین `be46f1c8773f249db75665eefd6d0c0db478a325`. **منبع محصول:** MP در `c46e792657e361cd09799c896c47149b4a5c4d86`؛ فقط tree/blob و metadata خوانده شد. هیچ تست محصول روی آن SHA اجرا نشده است.

## نتیجهٔ محدود و قابل استناد

**۶۹ تست خود بسته موفق‌اند: ۲۵ تست تاریخی v1 + ۴۴ تست جدید v2.** نتیجه فقط یکپارچگی، بازتولیدپذیری، خواندنی‌بودن preflight و حفظ دامنهٔ طرح ارسالی را نشان می‌دهد؛ نه اجرای ۵۰ میکرولوپ، نه QA محصول و نه review مستقل. حذف آزمایشی هر یک از ۵۰ کارت نیز در subtest جدا توسط validator رد می‌شود؛ این ۵۰ subtest تعداد unittestها را به «۱۱۹» تبدیل نمی‌کند.

### فرمان‌ها و مشاهدات واقعاً اجراشده

| محدوده | فرمان / مشاهده | نتیجه و مرز |
|---|---|---|
| runtime ابزار تحویل | `node --version` / `npm --version` / `python3 --version` | Node 22.22.3، npm 10.9.8، Python 3.11.2؛ نه انتخاب SDK محصول |
| dependency مستندات | `python3 -m venv handoff/.venv-docs` و pip با `handoff/requirements-docs.txt` | فقط Markdown 3.11.3 در venv جدا نصب؛ هیچ dependency محصول تغییر نکرد |
| ابزارهای اختیاری Node | `npm install --package-lock-only --ignore-scripts --no-audit --no-fund` و `npm ci --dry-run --ignore-scripts --no-audit --no-fund` در `tooling/node` | lock/resolve موفق؛ **dry-run نصب نیست**؛ ابزارهای این پوشه اجرا نشدند |
| renderer مستندات | lock update و `npm ci --ignore-scripts --no-audit --no-fund` در `tooling/diagram` | ۱۲ package واقعاً نصب؛ lifecycle خاموش؛ Viz 3.31.0 با Graphviz WASM 16.1.0 و Sharp 0.35.5 اجرا شدند |
| همگامی source | `python3 .../scripts/sync_plan.py --check` | ۵۰ ID غیرپیوسته، همهٔ عنوان‌ها و متن کامل AC حفظ؛ فازهای ۶/۸/۵/۱۶/۸/۷؛ بدون حذف/ادغام/renumber |
| منبع roadmap | `python3 .../scripts/make_roadmap.py --check` | DOT/Mermaid نقشه با همان ۵۰ ID/عنوان همگام؛ PNG/SVG از DOT است، نه رندر Mermaid |
| render چرخه | `node scripts/render_diagram.mjs diagrams/PWA_Finn_Loop_Flow.fa.dot diagrams/PWA_Finn_Loop_Flow.fa.png 4200` از ریشهٔ payload | PNG نهایی 4200×2888 و SVG؛ فقط تصویر سند |
| render نقشه | `node scripts/render_diagram.mjs diagrams/PWA_50_Microloops.fa.dot diagrams/PWA_50_Microloops.fa.png 5200` | PNG نهایی 5200×1945 و SVG؛ هر ۵۰ task node مجزا |
| syntax | `node --check` renderer و config؛ compile منابع Python با `compile(..., 'exec')` در تست | syntax بدون اجرای محصول؛ gate سازگاری ابزار روی MP نیست |
| ساخت نسخه‌پذیر | `handoff/.venv-docs/bin/python handoff/build_pwa_handoff.py --version 2.0.0` | HTML آفلاین، manifests و ZIP deterministic ساخته؛ validator = `PACKAGE_OK_NOT_QA` |
| مجموعهٔ تست تحویل | `handoff/.venv-docs/bin/python -m unittest discover -s handoff/tests -v` | **۶۹ تست، صفر failure/error**؛ نه product tests |
| validator قابل‌حمل | `python3 scripts/validate_package.py` | hash/inventory/source/title/AC/۱:۱ trace/D definitions/gates بررسی؛ `PACKAGE_OK_NOT_QA` |
| آزمون ZIP استخراج‌شده | استخراج به temporary directory و اجرای `sync_plan.py --check`، `make_roadmap.py --check`، `validate_package.py` | هر سه exit 0، بدون checkout Git، node_modules، source runtime MP یا تکیه به cache میزبان |
| preflight واقعیِ همین checkout | `python3 handoff/pwa-arena-v2/scripts/preflight.py --repo .` | **exit 2 / BLOCKED مورد انتظار** چون Chat2DB، `mp-app/` ندارد؛ این QA failure محصول نیست |
| preflight روی fixture | خواندن allowlist دو manifest، static role reconciliation، Git root و symlink منفی | inventory موفق هم `INVENTORY_OK_NOT_QA` و نه AGENT-READY؛ `.env`/DB/دادهٔ عضو خوانده نمی‌شود |
| تمامیت فایل/آرشیو | manifests، SHA-256، ZIP CRC/member contents/order/time/permissions و ساخت مجدد | داده‌ها byte-for-byte کنترل می‌شوند؛ hash خود ZIP بیرون ZIP در `.zip.sha256` است تا self-reference نباشد |
| حفاظت نسخهٔ قبلی | payload/ZIP v1 با تست تاریخی و checksum ثابت | v1 ZIP همچنان `019c3cefb570897fcebc0da82827d99301df28a90a41854f7ea7b4de790acff8`؛ artifact تاریخی دست‌نخورده |

### پوشش معنی‌دار تست‌های v2

- oracle مستقل از output: فهرست literal هر ۵۰ ID/عنوان و digest ثابت `SOURCE_PLAN.fa.md`؛ تساوی متن کامل source AC با JSON/Markdown؛ نه استخراج انتظار از planی که خودش تولید شده است.
- ۱:۱ بودن CSV، همهٔ nodeهای DOT/Mermaid/SVG، count هر فاز؛ regression چیدمان top-aligned roadmap پس از مشاهدهٔ تصویری.
- DAG بدون cycle/orphan؛ کار مستقل PWA-01/04/05؛ PWA-3F محفوظ و BLOCKED و defer فقط با پاسخ صریح مالک.
- D-01…D-11 مطابق **خطوط 68–78 منبع اصلی**، نه placeholder/نگاشت حدسی؛ owner approval جعلی رد می‌شود.
- هر parent و template فرزند، ۹ حوزهٔ Finn و پنج domain gate مستقل، بودجهٔ ۳ تلاش کل/۲ retry، ۹۰ دقیقهٔ پیشنهادی نیازمند approval و هزینهٔ مکمل بدون اذن صفر دارد.
- ۱۷ feature و ۸۰ path مرجع در tree بررسی‌شده؛ ۲۷ snapshot pin/hashدار و ۱۴۱ مسیر/۱۶۳ operation صرفاً metadata، بدون ادعای authorization runtime.
- mutationهای حذف هر کارت، تغییر عنوان/AC، cycle و approval ساختگی fail می‌شوند؛ مانع برگشت خطای v1 «جایگزینی دامنه بدون تطبیق» هستند.
- HTML بدون script/asset شبکه‌ای، دو PNG تعبیه‌شده، تمام ۵۰ heading، IDهای HTML یکتا؛ گزارش browser به hash HTML و recipe همین نسخه متصل است.
- lockهای دقیق/private، عدم بسته‌بندی runtime/private artifacts، پالایش امضاهای رایج credential، local links، manifests و ZIP round-trip/reproducibility. بررسی patternهای secret جای Gitleaks/SAST کامل نیست.

## smoke واقعیِ فقط HTML تحویل — جدا از محصول و دستگاه

برای خوانایی تحویل، `@sparticuz/chromium@153.0.0` و `playwright-core@1.65.1` در scratch جدا با `npm install --ignore-scripts --no-audit --no-fund` نصب شدند (۲۰ package)، نه در runtime محصول و نه در `tooling/node`. هیچ system/global package نصب نشد. binary/lib/fontهای استخراج‌شده و node_modules وارد ZIP/Git نیستند. recipe متنی و metadata/version/integrity منبع در references مانده‌اند.

- Chromium گزارش‌شده: **153.0.8010.0**؛ local `file://`، context آفلاین، HTTP abort، SW block؛ فقط فایل ساخته‌شدهٔ خود تحویل.
- viewportهای **1280×920، 390×844 و 320×780**: RTL، دقیقاً ۵۰ task heading، هر دو embedded image کامل، بدون overflow افقی صفحه، anchor یکتا و صفر script خود صفحه.
- درخواست خارجی مشاهده‌شده: **۰**؛ page error: **۰**. این کنترل‌ها هیچ اتصال به MP/backend/API یا cloud/model ندارند.
- سند/recipe دقیق در [HANDOFF_HTML_SMOKE.json](references/HANDOFF_HTML_SMOKE.json) و [recipe متنی](references/HANDOFF_HTML_SMOKE.recipe.mjs.txt) با hash ثبت‌اند. راهنمای بازتولید اختیاری در [TOOLCHAIN](TOOLCHAIN.fa.md) است.
- `--no-sandbox` محدودیت اجرای مرورگر در این sandbox است؛ نه policy محصول، نه مجوز صفحهٔ نامطمئن و نه proof امنیت یا accessibility. viewport شبیه‌سازی‌شده، دستگاه واقعی نیست.
- بازبینی بصری PNGها و screenshotهای HTML توسط **همین عامل** انجام شد؛ این self-review سند است، نه reviewer مستقل.

## خطاهای حین ساخت که پنهان نشده‌اند

1. invocation اولیهٔ sync با cwd داخل payload ولی prefix تکراری `handoff/pwa-arena-v2/`، `can't open file`/exit 2 داد؛ پیش از نوشتن متوقف و با مسیر `scripts/...` اصلاح شد.
2. رندر اولیهٔ roadmap چیدمان نامناسب داشت؛ `newrank=true` و RTL صریح افزوده، دوباره render و تست regression هم‌ترازی نوشته شد؛ معیار حذف نشد.
3. validator اولیه SVG را روی byte خام برای `PWA-00` می‌گشت و به‌درستی build را BLOCKED کرد؛ Graphviz hyphen را `&#45;` می‌نویسد. decode XML entity پیش از **همان مقایسهٔ دقیق ۵۰ ID** افزوده شد، نه ضعیف‌کردن coverage.
4. نخستین smoke browser بعد از context اول با `unsettled top-level await`/exit 13 قطع شد و fontconfig بستهٔ serverless هم مسیر فونت این sandbox را نمی‌دید؛ report نهایی PASS تولید نشد. یک context مشترک و fontconfig محلی `/etc/fonts` استفاده و smoke کامل با سه viewport تکرار شد. خروجی نهایی با متن فارسی بازبینی شد.
5. یک خواندن diagnostic از cacheِ metadataِ ازقبل پالایش‌شده انتظار shape کامل API داشت و `KeyError: commit` داد؛ پیش از آن ۶۸ تست PASS شده بودند، ولی کل command exit 1 بود. shape واقعی flat خوانده و metadata همان‌طور در `MP_SOURCE_COMMIT.json` ثبت شد؛ هیچ درخواست/تغییر محصولی در آن command نبود.

## چه چیزهایی اصلاً انجام نشده‌اند

- هیچ تغییر کد، install/build/test/CI محصول MP؛ هیچ E2E محصول، OTP/QR/receipt/payment/API authorization runtime، SAST/load/security/privacy/legal/product acceptance.
- هیچ نصب واقعی PWA، offline/update/cache proof محصول، accessibility certification، device test یا Flutter/Android regression تازه.
- هیچ reviewer مستقل، approval مالک برای taskهای محصول، branch-protection enforcement، PR/merge یا Go/No-Go محصول.
- هیچ deploy/staging/production/release/rollback/DB mutation، پرداخت واقعی، credential/دادهٔ واقعی عضو یا ارسال کد/داده به مدل/telemetry مکمل.

انتشار این **handoff** در GitHub طبق درخواست مالک، صرفاً تحویل اسناد/ZIP روی شاخهٔ مجاز است؛ مجوز MP write/release یا ادعای پایان PWA نیست. شناسه و نتیجهٔ انتشار تحویل در پاسخ نهایی و commit مخزن تحویل قابل پیگیری است؛ self-commit/hash آرشیو داخل خودش جعل نشده است.
