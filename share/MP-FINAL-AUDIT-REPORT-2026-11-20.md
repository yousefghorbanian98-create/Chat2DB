# گزارش نهایی ممیزی اجرایی‌شدهٔ MP — ۲۰۲۶‑۱۱‑۲۰

> **نوع سند:** گزارش نقصِ مبتنی بر **اجرا**، نه مرور ایستا.
> **مخزن ممیزی‌شده:** `MP` @ شاخهٔ `audit-main`، HEAD `662ff88` (۱۱۴۷ فایل ردیابی‌شده) — **فقط خواندنی**.
> **هیچ فایلی در مخزن MP تغییر نکرد، اضافه نشد و حذف نشد.** هر چه ساخته شد بیرون از آن است:
> کپی کاری `/tmp/run/MP`، محیط‌های مجازی `/tmp/run/venv*`، و ابزار/شاهدان در `/home/user/Chat2DB/audit/`.
> **اپ واقعاً بالا آورده شد** و روی `0.0.0.0:8010` سرویس داد (پیش‌نمایش زنده)، با دو پیکربندی:
> harness ابزار‌دار و **دقیقاً همان CMD داخل Dockerfile خودشان**.
> **داده‌ها تماماً مصنوعی‌اند** (شماره‌های الگوی seed خودِ پروژه، `0912…`/`0913…`). هیچ دادهٔ واقعیِ عضو/مالی استفاده نشد.
> **زبان:** فارسی، شناسه‌های فنی انگلیسی.
> **پروندهٔ همراه:** هر تست، هر عدد خام، hash هر فایل شاهد و فهرست کامل منابع در
> `share/MP-EVIDENCE-DOSSIER-2026-11-20.md` آمده است (۵۰ اجرای ثبت‌شده، ۲۹ یافته، ۶۰ فایل شاهد).
> اگر عددی در این گزارش با آن پرونده تفاوت داشت، **پروندهٔ شواهد معتبر است** و اختلاف در §۵ آن فهرست شده.

---

## ۰) فهرست مطالب

| § | موضوع |
|---|---|
| ۱ | خلاصهٔ اجرایی و جدول یافته‌ها بر حسب شدت |
| ۲ | روش‌شناسی: چه چیزی اجرا شد، با چه ابزاری، با چه دقتی |
| ۳ | محیط و نصب ابزارها (و ابزارهایی که واقعاً کار نکردند) |
| ۴ | بالا آوردن اپ روی پورت: مسیر دقیق، seed، و آنچه verify شد |
| ۵ | یافته‌های **P0/Critical** با شاهد زنده (F‑01…F‑05) |
| ۶ | یافته‌های **P1/High** (F‑06…F‑14) |
| ۷ | یافته‌های **P2/Medium** و بدهی کیفیت (F‑15…F‑24) |
| ۸ | آنچه **سالم** است — فهرست تأییدشده با اجرا |
| ۹ | صداقت: یافته‌های کاذبِ خودم که با اجرا **رد** شدند |
| ۱۰ | جدول کامل ابزارها + قابلیت اتکا |
| ۱۱ | نقشهٔ رفع: اولویت، تلاش، و **شاهد پذیرش** هر مورد |
| ۱۲ | پیوست الف: مسیر فایل‌های شاهد |
| ۱۳ | پیوست ب: دستورات بازتولید (قدم‌به‌قدم) |
| ۱۴ | پیوست پ: آمار خام اندازه‌گیری‌ها |

---

## ۱) خلاصهٔ اجرایی

اپ در لایهٔ «درستیِ منطق و قرارداد» در وضعیت بسیار خوبی است: **۱۰۹۵ تست بک‌اند پاس**، **۲۸۲ تست استودیو پاس**،
`tsc --noEmit` تمیز، `ruff` تمیز، **صفر drift** بین `api/routes.json` و OpenAPI زنده (۱۶۳ عملیات / ۱۴۱ مسیر)،
**صفر خطای ۵xx** در ۱۱۴۱ درخواستِ ماتریس مجوز، **صفر نشت stack trace**، **صفر وابستگی دوری** در استودیو،
تکرار کد فقط **۰٫۲۶٪**، مالکیت داده (member‑scope) بدون هیچ نشتی، و همهٔ مکانیزم‌های JWT
(الگوریتم `none`، امضای جعلی، انقضا، نقشِ برگرفته از DB) درست کار می‌کنند.

اما در لایهٔ **«رفتار زیر بار» و «پیکربندی استقرار»** سه نقص بحرانی وجود دارد که با اجرا اثبات شدند
و تا پیش از این **ریشه‌یابی نشده بودند** (گزارش QA صریحاً نوشته بود «root cause NOT established»):

1. **دورزدن کامل محدودیت نرخ با هدر `X-Forwarded-For`** — چون فرمان Dockerfile خودشان
   `--forwarded-allow-ips='*'` دارد و uvicorn پیش از اپ `request.client.host` را بازنویسی می‌کند؛
   در نتیجه منطق fail‑closed خودِ اپ (`app/security/proxy.py`) عملاً بی‌اثر می‌شود.
   اندازه‌گیری: **۳۰/۳۰ درخواست OTP با XFF جعلی پذیرفته شد** در برابر **۳/۱۴ بدون آن**؛
   نرخ حدس از ۳/ثانیه به **۲۲۸/ثانیه** رسید (۷۶ برابر).
2. **قفل شدن سرور زیر بار تا «نیاز به restart»** — با دو علت مستقل که هر دو اندازه‌گیری شدند:
   (الف) هر خطای مدیریت‌نشده در حالت development با `ConsoleRenderer`+`rich` رندر می‌شود و
   **event loop را برای ده‌ها ثانیه تا دقیقه‌ها می‌بندد**: لاگ **۱۴۸ مگابایت / ۸۱۷٬۰۱۲ خط برای فقط ۴ خطا**
   (≈۳۷ مگابایت به‌ازای هر خطا، ۶۵ مگابایتش فقط کد رنگ ANSI). میکروبنچمارک: **~۷٬۰۰۰ برابر** کندتر و
   **~۶۳۰ برابر** حجیم‌تر از `JSONRenderer`. در این وضعیت حتی `SIGTERM` پاسخ داده نمی‌شد (فقط `kill -9`).
   (ب) اشباع استخر اتصال: نقطهٔ شکست دقیقاً در `app/deps.py:53` است
   (`TimeoutError: QueuePool limit of size 40 overflow 20 reached, timeout 5.00`).
3. **`SystemError` در مسیر احراز مجوز زیر همزمانی** — casbin در **هر درخواست** عبارت را
   `ast.parse`/`compile` می‌کند (کش غیرفعال). با ۸۰ نخ: **۳ خطا از ۳۲٬۰۰۰ فراخوانی**
   `SystemError: AST constructor recursion depth mismatch` ⇒ HTTP 500 روی گارد مجوز.
   نمونهٔ رفعِ اندازه‌گیری‌شده: جدول تصمیم از پیش‌کامپایل‌شده با **۲۴/۲۴ تصمیم یکسان** و
   **۵۲ برابر سریع‌تر** (۱۷٫۴ میکروثانیه در برابر ۹۱۰٫۷ میکروثانیه).

نکتهٔ مهم دربارهٔ صداقت اعداد: **عدد پوشش مستند‌شده (۹۴٫۲۸٪) با اجرا رد شد** — اندازهٔ واقعی کل
پروژه **۸۳٫۷۳٪** است و ۹۴٫۲۸٪ فقط سهم دایرکتوری `app/` است (جدول §۱۴).

### ۱‑۱) جدول یافته‌ها بر حسب شدت

| شناسه | شدت | عنوان | شاهد اجرایی | وضعیت |
|---|---|---|---|---|
| **F‑01** | **Critical** | دورزدن rate‑limit با `X-Forwarded-For` (فرمان Dockerfile) | ۳۰/۳۰ در برابر ۳/۱۴؛ ۲۲۸ حدس/ثانیه | **اثبات شد** |
| **F‑02** | **Critical** | پیش‌فرض fail‑open محیط: `MP_ENVIRONMENT=development` + `MP_SMS_PROVIDER=dev` ⇒ `dev_code` در پاسخ | ۷ هویت فقط با `dev_code` وارد شدند | **اثبات شد** |
| **F‑03** | **Critical** | قفل شدن سرور زیر بار؛ رندر `rich` روی event loop | ۱۴۸MB/۴ خطا؛ `/health` تایم‌اوت ۷+ دقیقه؛ SIGTERM بی‌پاسخ | **اثبات شد** |
| **F‑04** | **High** | اشباع استخر اتصال؛ نبودِ هیچ متریک pool؛ ناسازگاری ظرفیت‌ها | `QueuePool … timeout 5.00` در `deps.py:53`؛ فروپاشی در ۸۰ کلاینت | **اثبات شد** |
| **F‑05** | **High** | `SystemError` در `casbin enforce` زیر همزمانی (compile در هر درخواست) | ۳/۳۲٬۰۰۰؛ پشتهٔ کامل تا `ast.py:50` | **اثبات شد** |
| **F‑06** | **High** | `/api/v1/metrics` بدون احراز هویت | HTTP 200 بدون توکن، ۳۴۶ خط، ۱۲ متریک | **اثبات شد** |
| **F‑07** | **High** | پوشش مستند ۹۴٫۲۸٪ در برابر واقعی ۸۳٫۷۳٪ | اجرای کامل pytest+cov (۴۶۱ ثانیه) | **اثبات شد** |
| **F‑08** | **High** | `logout-all` توکن‌های بدون `sid` را باطل نمی‌کند | توکن واقعی ۴۰۱، توکن بی‌`sid` ۲۰۰ | **اثبات شد** |
| **F‑09** | **High** | پول بزرگ: `2^53`، `2^53+1`، `10^18` پذیرفته می‌شوند + coercion رشته→عدد | HTTP 200 و بازگرداندن عین مقدار | **اثبات شد** |
| **F‑10** | **Medium‑High** | ۳۱ خطای ESLint در استودیو (هیچ lint واقعی اجرا نمی‌شد) | ESLint 9 flat config: ۳۱ error/۳ warning | **اثبات شد** |
| **F‑11** | **Medium‑High** | امتیاز جهش ۵۷٫۸٪ در ماژول پولی؛ ۳ شکاف واقعی | ۲۶/۴۵ کشته (راستی‌آزمایی دستی) | **اثبات شد** |
| **F‑12** | **Medium** | `routes.json` مجموعهٔ گاردهای واقعی را کم‌تر نشان می‌دهد ⇒ اوراکل نامعتبر | ۶۰۲ مورد «نقش مجاز ولی انکار شد» | **اثبات شد** |
| **F‑13** | **Medium** | guard تکراری روی یک مسیر (دو بار casbin enforce) | `axis-assessments/{id}/review` | **اثبات شد** |
| **F‑14** | **Medium** | `gateway-return` با شناسهٔ نامعتبر → HTTP 200 | `GET /api/v1/payments/-1/gateway-return` | **اثبات شد** |
| **F‑15** | **Medium** | ۵۵ هشدار پیچیدگی (lizard) و ۴۱ بلوک ≥C (radon)؛ بدترین درجهٔ radon **F** با CC ‏۴۷ و ۴۶ | خروجی ابزارها | **اثبات شد** |
| **F‑16** | **Medium** | ۷ محل پولِ شناور در استودیو + ۱ sentinel منفی | Semgrep با قاعدهٔ اختصاصی | **اثبات شد** |
| **F‑17** | **Medium** | ۴ خطای «except بی‌صدا» (از جمله در `api/v1/monitoring.py:18`) | Semgrep + bandit B110 | **اثبات شد** |
| **F‑18** | **Medium** | ناسازگاری ظرفیت‌ها: ۱۶۴ handler سنکرون، threadpool=40، pool=60، 4 worker | `/audit/threads` + Dockerfile | **اثبات شد** |
| **F‑19** | **Low‑Med** | ۳ لایهٔ جداگانهٔ دسترسی به داده در استودیو + `await import()` پویا در هندلر | `api.ts`/`adminApi.ts`/`session.ts`؛ `Shop.tsx:446,459` | **اثبات شد** |
| **F‑20** | **Low** | ۲ export مرده در `lib/api.ts` | اسکن tag‑aware | **اثبات شد** |
| **F‑21** | **Low** | ۵ session بدون context manager در اسکریپت‌ها | Semgrep | **اثبات شد** |
| **F‑22** | **Low** | ۴ SQL با f‑string در یک migration | Semgrep | **اثبات شد** |
| **F‑25** | **Medium** | گارد شناسه **کف** ندارد: ۱۲ endpoint با `-1`/`0`/`-0`/INT64_MIN پاسخ **۲۰۰** می‌دهند | ۴۸ سلول از ۸۷۲ سلولِ پاسِ با احراز هویت تأییدشده | **اثبات شد** |
| **F‑26** | **Medium** | دو شکلِ متفاوت برای پاکت خطا: `{"error":…}` در برابر `{"detail":…}` | ۷۰ × ۴۰۴ و ۱ × ۴۰۵ با پاکت پیش‌فرض FastAPI | **اثبات شد** |
| **F‑27** | **Medium** | پیش‌نیازِ «پروندهٔ عضو» در سبد خرید با `404 not_found` بیان می‌شود؛ سفارش به‌نیابت ممکن نیست | `shop.cart_add`/`shop.checkout` ⇒ ۴۰۴ در پاس seed | **اثبات شد** |
| **F‑28** | **Medium** | «امروز» در دو ماژول با `date.today()` (UTC کانتینر) حساب می‌شود در حالی که shop از `Asia/Tehran` استفاده می‌کند ⇒ مرزِ روز ناهمگون | `DTZ011` در ۳ محل؛ هیچ `TZ` در Dockerfileها نیست | **اثبات شد** |
| **F‑29** | **Low‑Med** | `app/sms.py`: شش `logging.error` داخل `except` (بدون traceback) + سه `urlopen` با schemes باز + ۳۹ `# noqa` بلااثر | `TRY400`×۶، `S310`×۳، `RUF100`×۳۹ | **اثبات شد** |

**محدود/بی‌اثر (Low/Info):** `journal_mode=delete` پس از alembic (WAL فقط در رویداد `connect` موتور اعمال
می‌شود) · هشدارهای `StarletteDeprecationWarning` برای `HTTP_422_UNPROCESSABLE_ENTITY` ·
۱ متغیر بلااستفاده در `modules/face_id/deep.py:74` · `len(app.routes)==7` در fastapi 0.165.0
(هر اسکریپتی که مسیرها را از `app.routes` بشمرد شکننده است؛ باید از OpenAPI خواند).

---

## ۲) روش‌شناسی

اصل حاکم: **هیچ ادعایی بدون اجرا ثبت نشده است.** هر یافته یا (الف) با مشاهدهٔ زنده روی اپِ در حال
اجرا اثبات شده، یا (ب) با اجرای ابزار روی کد، یا (پ) صریحاً به‌عنوان **BLOCKED** علامت خورده است.

### ۲‑۱) لایه‌هایی که ممیزی شدند

| # | لایه | روش | عمق |
|---|---|---|---|
| ۱ | راه‌اندازی/پیکربندی (`app/config.py`, `app/main.py`, `app/logging.py`) | خواندن کامل + اجرای دو پیکربندی (dev و CMD واقعی Dockerfile) | خط‌به‌خط |
| ۲ | احراز هویت و نشست (`modules/auth/*`, `app/security/jwt.py`, `app/deps.py`) | ورود واقعی OTP برای ۷ هویت + ۱۲ سناریوی ابطال/جعل توکن | خط‌به‌خط |
| ۳ | احراز مجوز (`security/rbac.py`, casbin) | ماتریس ۱۶۳×۷ زنده + میکروبنچمارک + بازتولید چندنخی | خط‌به‌خط |
| ۴ | قرارداد API (`api/routes.json`, OpenAPI زنده) | diff دوطرفه + مقایسهٔ رفتار مشاهده‌شده با اعلام‌شده | کامل |
| ۵ | داده/مهاجرت (`db/*`, alembic) | ساخت DB از صفر، diff ORM↔DB، PRAGMAها | کامل |
| ۶ | استخر اتصال و همزمانی (`db/base.py`) | ابزار دقیق رویدادهای pool + بار پله‌ای + py‑spy | کامل |
| ۷ | مشاهده‌پذیری (metrics/health/logging) | فراخوانی زنده + کالبدشکافی لاگ + بنچمارک رندر | کامل |
| ۸ | پول و مرزهای عددی | ۸ کلاس مقدار مرزی روی endpoint واقعی | کامل |
| ۹ | ورودی نامعتبر/خصمانه | ۱۲ شناسهٔ مخرب × همهٔ مسیرهای پارامتری + ۸ رشتهٔ خصمانه | کامل |
| ۱۰ | فرانت‌اند استودیو (دکمه‌ها/سیم‌کشی/a11y/hooks) | ESLint 9 + madge + jscpd + اسکن tag‑aware اختصاصی | کامل |
| ۱۱ | کیفیت ایستا بک‌اند | ruff, vulture, radon, lizard, bandit, semgrep (۱۷ قاعدهٔ اختصاصی) | کامل |
| ۱۲ | زنجیرهٔ تأمین | pip‑audit روی **وابستگی‌های خودِ پروژه**، detect‑secrets | کامل |
| ۱۳ | قدرت تست‌ها | پوشش واقعی + **آزمون جهش با راستی‌آزمایی دستی** | کامل |
| ۱۴ | کلاینت فلاتر (Dart) | Semgrep با قواعد Dart (چون SDK فلاتر نیست) | **نسبی/BLOCKED** |

### ۲‑۲) قواعد روش‌شناختی که رعایت شد

1. **گروه کنترل:** هر پدیدهٔ مربوط به بار، دو بار اجرا شد — یک بار با harness ابزار‌دار و یک بار با
   `uvicorn` خام (بدون هیچ listener) — تا معلوم شود نتیجه خاصیتِ اپ است نه سربارِ ابزارِ ممیزی.
   نتیجه: اپِ خام هم در ۸۰ کلاینت همزمان فرو می‌ریزد (جدول §۱۴).
2. **آزمون کنترل‌شدهٔ تک‌متغیری:** برای جدا کردن اثر «قالب لاگ» از «اشباع استخر»، سرور یک بار با
   `ConsoleRenderer` و یک بار با `JSONRenderer` بالا آمد (`AUDIT_LOG_FORMAT=json`).
3. **راستی‌آزمایی ابزار:** وقتی mutmut هر ۴۵ جهش را «زنده» گزارش کرد، **قبول نکردم**؛
   هر جهش را دستی اعمال کردم، pytest را اجرا کردم و فایل را با `git checkout` برگرداندم.
   نتیجهٔ واقعی ۲۶/۴۵ کشته شد (۵۷٫۸٪). گزارشِ mutmut **نادقیق** است (§۱۰).
4. **ردِ یافتهٔ کاذبِ خودم:** نسخهٔ نخستِ اسکنر دکمه‌ها با regex ساده ۷۵ دکمهٔ «بی‌سیم» گزارش کرد؛
   بررسی دستی نشان داد `onClick` در خط بعد است. اسکنر tag‑aware بازنویسی شد و عدد واقعی ۱۰/۸۴ است.
5. **تفکیک کلاس جهش:** جهش‌های «متن پیام خطا» از جهش‌های «منطق/مرز/پیش‌فرض» جدا شدند تا
   امتیاز جهش بزرگ‌نمایی نشود.
6. **دادهٔ مصنوعی:** همهٔ شماره‌ها/مبالغ/اسم‌ها ساختگی‌اند و از seederهای idempotent خودِ پروژه
   (`qa-report/tools/seed_live.py`, `scripts/seed_shop.py`, `scripts/seed_norms.py`, `scripts/seed_criteria.py`)
   استفاده شد — نه دادهٔ واقعی.
7. **عدم دست‌کاری مخزن:** هر تغییر موقت (مثلاً `mutmut apply`) در کپی `/tmp/run/MP` انجام و بلافاصله با
   `git checkout` برگردانده شد؛ `git status` در پایان **clean** بود.

---

## ۳) محیط و نصب ابزارها

### ۳‑۱) محدودیت‌های سندباکس (که دامنهٔ ممیزی را تعیین کردند)

| منبع | مقدار | پیامد |
|---|---|---|
| CPU | **۲ هسته** | آزمون جهش کامل (۱۰۹۵ تست × هر جهش) ممکن نیست ⇒ جهش روی یک ماژول + تست هدفمند |
| RAM | ~۳٫۶ گیگابایت | Chromium بی‌سر و SDK فلاتر همزمان ممکن نیست ⇒ آزمون UI مرورگری BLOCKED |
| دیسک | ۲۰ گیگابایت | نصب‌ها لاغر نگه داشته شد |
| JDK/Maven/Gradle | **نیست** | ساخت APK/AAB، R8، lintVitalRelease، JADX، apkanalyzer ⇒ BLOCKED |
| Flutter SDK | **نیست** | `flutter analyze/test`، goldens، patrol ⇒ BLOCKED |
| Docker daemon | **نیست** | Pumba/chaos، hadolint روی image واقعی، compose up ⇒ BLOCKED |
| Postgres/Valkey/Prometheus | نصب نیست | سناریوهای چنددیتابیسی و متریک‌های واقعی Prometheus ⇒ BLOCKED |
| `sqlite3` CLI | نیست | از `sqlite3` کتابخانهٔ استاندارد پایتون استفاده شد (کافی بود) |
| شبکه | فقط github/pypi/npm | `semgrep --config auto` و `--validate` (نیازمند semgrep.dev) ⇒ BLOCKED؛ قواعد **اختصاصی آفلاین** نوشته شد |
| GitHub API | `/branches/main/protection` → **403** | وضعیت branch protection قابل خواندن نیست ⇒ اقدام مالک، نه یافته |

### ۳‑۲) ابزارهایی که نصب و **با فراخوانی واقعی** تأیید شدند

| ابزار | نسخه | چگونه تأیید شد | نتیجه |
|---|---|---|---|
| fastapi | 0.165.0 | import + بالا آمدن اپ | ✅ |
| sqlalchemy | 2.1.9 | import + رویدادهای pool | ✅ |
| pydantic | 2.14.4 | import | ✅ |
| pytest | 9.2.0 | اجرای کامل سوئیت | ✅ ۱۰۹۵ پاس |
| coverage (pytest‑cov) | — | اجرای `--cov` + گزارش XML | ✅ ۸۳٫۷۳٪ |
| alembic | — | `upgrade head` روی DB خالی | ✅ head `a7c3d9e1f2b4` |
| ruff | 0.17.6 | `ruff check .` / `format --check` | ✅ تمیز |
| vulture | 2.16 | اجرا روی ۹ دایرکتوری | ✅ ۱ یافته |
| radon | 6.0.1 | `cc -s -n C` و `mi -s` | ✅ ۹۵۶ بلوک |
| lizard | 1.26.1 | اجرا با `--CCN 10 --length 60` | ✅ ۷۴۲ تابع |
| bandit | — | `-r … -f json` | ✅ ۱۰ یافتهٔ LOW |
| pip‑audit | 2.10.1 | `-r mp-deps.txt --no-deps` | ✅ بدون آسیب‌پذیری |
| detect‑secrets | 1.5.0 | `scan` روی کل مخزن | ✅ بدون رمز واقعی |
| semgrep | 1.186.0 | ۱۷ قاعدهٔ اختصاصی روی backend/studio/client | ✅ ۲۸ یافته |
| mutmut | 2.x | `run` + `show` + `apply` | ⚠️ کار کرد ولی **قضاوتش نادقیق** (§۱۰) |
| py‑spy | 0.4.4 | `dump --pid` روی پروسهٔ قفل‌شده | ✅ **کلیدی‌ترین شاهد** |
| hypothesis | 6.170.17 | import | ✅ (در پروژه declare نشده — F‑21) |
| freezegun / fakeredis / deepdiff / jsonschema / schemathesis | — | import | ✅ |
| opentelemetry (api/sdk + FastAPI/SQLAlchemy instrumentation) | 1.45.2 | import | ✅ |
| eslint | 9.x | اجرای واقعی با flat config روی ۵۳ فایل | ✅ ۳۱ error |
| typescript‑eslint / eslint‑plugin‑react‑hooks / jsx‑a11y | — | در همان اجرا | ✅ |
| jscpd | — | اجرا روی ۲۱۱ فایل (۳ زبان) | ✅ ۹ clone |
| madge | — | `--circular` روی ۵۴ فایل | ✅ بدون دور |
| vitest / tsc | — | اجرای واقعی | ✅ ۲۸۲ پاس / tsc تمیز |

### ۳‑۳) ابزارهایی که **کار نکردند** (و چرا) — صداقت ابزارها

| ابزار | مشکل دقیق | راه‌حل انجام‌شده |
|---|---|---|
| **knip** | کرش در `oxc-parser` → `createBuffer`/`ArrayBuffer` روی Node v22.22.3؛ خروجی JSON خالی | **BLOCKED**؛ جایگزین: اسکنر export/بازt‑aware اختصاصی خودم (همان خروجی با دقت کمتر ولی قابل راستی‌آزمایی) |
| **semgrep 1.186.0 در venv اپ** | `Traceback` هنگام اجرا: پین `opentelemetry-api~=1.37.0` در برابر نیاز fastapi `>=1.44` | دو venv جدا: `/tmp/run/venv` (اپ) و `/tmp/run/venv-audit` (ابزار). `pip check` در venv اپ: **No broken requirements found** |
| **mutmut 3.8.1** | `Could not figure out where the code to mutate … add source_paths` — CLI عملاً غیرقابل استفاده | پین به `mutmut<3` (v2)؛ ولی قضاوتش نادقیق ⇒ راستی‌آزمایی دستی هر ۴۵ جهش |
| **`import py_spy`** | نام import ندارد (فقط CLI) | `py-spy --version` = 0.4.4 |
| **npm نصب ترکیبی** (eslint9 + plugins + knip + madge + jscpd یک‌جا) | `ERESOLVE` | نصب تک‌تک با `--legacy-peer-deps` در prefix پرتاب‌شدنی `/tmp/run/npt` (بدون دست‌زدن به `package.json` پروژه) |
| **semgrep `--validate`** | نیازمند `semgrep.dev` (خارج از allowlist) ⇒ `SSLError` | رد شد؛ اعتبار قواعد با اجرای واقعی روی کد سنجیده شد |
| **زبان `tsx` در semgrep** | `UnknownLanguageError: unsupported language: tsx` | به `typescript` تغییر کرد (فایل‌های `.tsx` را هم پوشش می‌دهد) |
| **`len(app.routes)`** | در fastapi 0.165.0 = **۷** (به‌خاطر `_IncludedRouter` تنبل) در حالی که OpenAPI = ۱۴۱ مسیر | همهٔ شمارش‌ها از سند OpenAPI انجام شد |
| **اسکنر دکمه با regex ساده** (نسخهٔ خودم) | `onClick` چندخطی را نمی‌دید ⇒ ۷۵ یافتهٔ کاذب | بازنویسی tag‑aware با دنبال‌کردن عمق `{}`/quote ⇒ ۱۰ مورد واقعی |

---

## ۴) بالا آوردن اپ روی پورت (مسیر دقیق و قابل بازتولید)

### ۴‑۱) زنجیرهٔ راه‌اندازی

```bash
# ۱) کپی کاری از مخزن فقط‌خواندنی (مخزن اصلی دست‌نخورده ماند)
cp -a /tmp/MP /tmp/run/MP                      # ۵۶MB؛ git status در /tmp/MP = ۰ تغییر

# ۲) محیط مجازی اپ + همهٔ وابستگی‌های runtime و dev
python3 -m venv /tmp/run/venv && pip install …   # pip check ⇒ No broken requirements found

# ۳) ساخت DB از صفر با مهاجرت‌های خودِ پروژه
MP_DATABASE_URL=sqlite:////tmp/run/data/mp.db alembic upgrade head
#   ⇒ head = a7c3d9e1f2b4 ، ۶۵ جدول ، diff ORM↔DB = صفر (۶۴ در برابر ۶۴)

# ۴) seed با ابزارهای خودِ پروژه (همه idempotent، همه مصنوعی)
python qa-report/tools/seed_live.py       # admin_id=1 + ۲۵۰ عضو
python scripts/seed_shop.py               # ۴ دسته، ۴ محصول، ۴ قیمت، ۱ درگاه
python scripts/seed_criteria.py           # ۹ rubric
python scripts/seed_norms.py              # ۷۰ نُرم
```

### ۴‑۲) دو پیکربندی اجرا

| پیکربندی | فرمان | هدف |
|---|---|---|
| **harness ابزار‌دار** | `python audit/serve_backend.py` | شمارندهٔ رویدادهای pool (checkout/checkin/connect/close/detach)، `/audit/pool`، `/audit/threads`، خروجی JSONL، و OTel اختیاری |
| **کنترل خام** | `python audit/serve_plain.py` | بدون هیچ listener — برای حذف اثر ابزار از نتیجه |
| **CMD واقعی خودشان** | `uvicorn app.main:app --host 0.0.0.0 --port 8010 --workers 2 --proxy-headers --forwarded-allow-ips='*'` | دقیقاً همان چیزی که در `mp-app/backend/Dockerfile:27` نوشته شده — برای اثبات F‑01 در پیکربندی واقعی |

هر سه روی `0.0.0.0:8010` بایند شدند (برای پیش‌نمایش زنده) و پاسخ دادند.

### ۴‑۳) آنچه پس از بالا آمدن verify شد

| بررسی | نتیجه |
|---|---|
| `GET /health` | `{"status":"ok","service":"Muscle Paradise","version":"1.0.0"}` |
| `GET /api/v1/health/ready` | `ready:true, database_ok:true, rate_limit_storage_ok:true, checkin_slo_ok:true, outbox:{…}` |
| `GET /openapi.json` | HTTP 200، ۱۷۱٬۳۹۵ بایت، **۱۴۱ مسیر / ۱۶۳ عملیات** |
| `POST /api/v1/auth/otp/request` | ۲۰۰ با `dev_code` (همین راهِ ورود ۷ هویت ممیزی بود) |
| ورود کامل ۷ هویت | member, coach, reception, manager, admin, super_admin + عضو ساده — همه با OTP واقعی |
| seed زنده از طریق خودِ API | **۱۴/۱۶ موفق**: عضو، اشتراک، کوپن درصدی و ثابت، پرداخت نقدی، پرداخت با کوپن، شارژ کیف پول، هزینه، وزن، اعلان، گفت‌وگو، کلاس، عضو دوم/سوم |
| دو مورد ناموفق seed | `shop.cart_add` و `shop.checkout` با ۴۰۴ «پروندهٔ عضو یافت نشد» — چون توکنِ فراخوان نقش admin دارد و Member profile ندارد (رفتار درست برنامه، نه باگ) |
| `journal_mode` پس از alembic | **`delete`** — WAL فقط در رویداد `connect` موتور (`db/base.py`) اعمال می‌شود، نه در مهاجرت |

### ۴‑۴) نکتهٔ پیکربندی مهم که در حین راه‌اندازی کشف شد

`shop_online_purchase_enabled` **به‌طور پیش‌فرض `False`** است (`app/config.py:65`). یعنی در هر استقرارِ
بدون این متغیر، دکمهٔ خرید درون‌برنامه‌ای در استودیو/کلاینت با `409 shop_online_closed` مواجه می‌شود.
برای ممیزیِ مسیر نوشتنِ فروشگاه، harness با
`MP_SHOP_ONLINE_PURCHASE_ENABLED=true MP_SHOP_OPEN_HOUR=0 MP_SHOP_CLOSE_HOUR=23` بالا آمد
(فقط در محیط ممیزی — مخزن دست‌نخورد). این باید در `OPS-RUNBOOK.md` مستند شود: کدام کلید، چه مقدار،
و رفتار UI وقتی خاموش است (F‑18).

---

## ۵) یافته‌های P0/Critical — با شاهد زنده

### F‑01 · دورزدن کامل محدودیت نرخ با `X-Forwarded-For` (Critical)

**فرضیهٔ مهندسی:** هدر XFF کنترل‌شدهٔ کلاینت نباید بتواند سبدِ rate‑limit تازه بسازد.
**مشاهده:** ساخت. به‌طور کامل.

**اندازه‌گیری (روی دقیقاً همان CMD که در Dockerfile خودشان است، ۲ ورکر):**

| سناریو | درخواست‌ها | پذیرفته | ۴۲۹ |
|---|---|---|---|
| `POST /api/v1/auth/otp/request` با **XFF تصادفی در هر درخواست** | ۳۰ | **۳۰** | ۰ |
| همان بدون هدر پراکسی (پنجرهٔ تازه) | ۱۴ | **۳** | ۱۱ |
| نرخ حدس کد (تک‌نخ، با XFF تصادفی) | — | **۲۲۸٫۴ تلاش/ثانیه** | — |

یعنی سقف انفجاری `otp_burst_limit=3/second` و سقف `otp_rate_limit=10/minute` **هر دو** با یک هدر
قابل دور زدن‌اند (بزرگ‌نمایی اندازه‌گیری‌شده: **۷۶ برابر**). علاوه بر این، IP جعلی در لاگ ممیزی و
متریک می‌نشیند (`GET /api/v1/metrics` با `X-Forwarded-For: 1.2.3.4` → ۲۰۰).

**زنجیرهٔ علّی (لایه‌به‌لایه):**

1. `mp-app/backend/Dockerfile:27` و `mp-app/infra/Dockerfile.backend:29`:
   `exec uvicorn app.main:app … --proxy-headers --forwarded-allow-ips='*'`
   ⇒ uvicorn به XFF از **هر** peer اعتماد می‌کند.
2. uvicorn `ProxyHeadersMiddleware` مقدار `request.client.host` را **پیش از اپ** بازنویسی می‌کند.
   (پیش‌فرض خودِ uvicorn هم `proxy_headers=True` و `forwarded_allow_ips="127.0.0.1,::1"` است —
   `uvicorn/config.py:225` و `:363`.)
3. `app/security/proxy.py:38-58` — `client_ip()` منطق درستی دارد: اگر `trusted` خالی باشد یا peer
   در فهرست معتمد نباشد، **فقط peer** را برمی‌گرداند و هرگز XFF را نمی‌خواند (fail‑closed).
4. اما peer **همان چیزی است که uvicorn جایگزین کرده** ⇒ منطق fail‑closed اپ روی ورودیِ آلوده
   اجرا می‌شود و همان IP جعلی را برمی‌گرداند.
5. `modules/auth/router.py:28-38` (`_rate_limit_key`) → `rate_limit_key(request, parse_trusted(settings.trusted_proxies))`
   ⇒ کلید سبد = IP جعلی ⇒ هر درخواست یک سبد تازه.
6. `app/config.py:69`: `trusted_proxies: str = ""` — و هیچ اعتبارسنج production‌ای آن را الزامی نکرده است.

**چرا این مهم‌تر از «سبد مشترک» است:** در مستندات خودشان
(`docs/MuscleParadise/DEPLOYMENT.md:43`) نوشته شده «خالی = `X-Forwarded-For` **هرگز** پذیرفته
نمی‌شود». این گزاره در لایهٔ اپ درست است ولی در استقرار واقعی **نادرست** است، چون یک لایه پایین‌تر
(uvicorn) همان هدر را می‌پذیرد. یعنی سند، احساس امنیت کاذب می‌دهد.

**آنچه درست کار کرد (و باید در گزارش بماند):** قفلِ هر کد OTP سالم است — پس از ۵ حدس اشتباه،
`400 otp_locked` برگشت و **کد واقعی هم دیگر کار نکرد**؛ بازپخش کد ممکن نبود؛ حدس اشتباه هرگز ۲۰۰ نشد.
پس دورزدن نرخ ⇒ «ورود غیرمجاز» نمی‌دهد، ولی **SMS‑bombing (هزینهٔ واقعی)، آلوده‌سازی لاگ/متریک،
و حذف همهٔ دفاع‌های مبتنی بر نرخ** را ممکن می‌کند.

**رفع (ترتیب‌دار، همه رایگان/بازمتن):**
1. منبع حقیقتِ واحد: `--forwarded-allow-ips="${MP_TRUSTED_PROXIES}"` در هر دو Dockerfile؛
   اگر خالی بود، `--proxy-headers` **حذف** شود (نه `'*'`).
2. در `validate_production_configuration` افزودن: `MP_TRUSTED_PROXIES` غیرخالی و همهٔ مقادیر IP/CIDR معتبر.
3. آزمون یکپارچگی: درخواست از peer غیرمعتمد با XFF جعلی ⇒ **۴۲۹** (نه ۲۰۰).
4. اصلاح `DEPLOYMENT.md:43` و `OPS-RUNBOOK.md` با جملهٔ دقیق: «اعتماد به XFF در لایهٔ uvicorn
   تعیین می‌شود، نه در اپ».
5. افزودن `mp_rate_limit_key_source{peer|xff}` به متریک‌ها تا در بهره‌برداری دیده شود.

**شاهد پذیرش:** ۳۰ درخواست پشت‌سرهم با XFF تصادفی ⇒ دست‌کم ۲۷ مورد `429`؛ و در لاگ، IP ثبت‌شده
برابر peer واقعی باشد نه مقدار هدر.

---

### F‑02 · پیش‌فرض fail‑open محیط: یک متغیر جاافتاده = استقرار کاملاً باز (Critical)

**مشاهدهٔ زنده:** من در همین ممیزی **۷ هویت** (member, coach, reception, manager, admin, super_admin و
یک عضو ساده) را **فقط با خواندن `dev_code` از پاسخ API** وارد کردم. هیچ رمز/پیامکی در کار نبود.

**زنجیره:**

| حلقه | شاهد | اثر |
|---|---|---|
| پیش‌فرض محیط | `app/config.py:25` → `environment: str = "development"` | اگر `MP_ENVIRONMENT` ست نشود، اپ development است |
| اعتبارسنج production فقط در production اجرا می‌شود | `app/config.py:127-135` (`if self.environment != "production": return self`) | هیچ‌کدام از ۱۲ بررسی production انجام نمی‌شود |
| پیش‌فرض پیامک | `MP_SMS_PROVIDER` پیش‌فرض `dev` | provider.name == "dev" |
| نشت کد OTP | `modules/auth/service.py:52` و `:260` → `out["dev_code"] = code` **فقط** به provider شرط شده، نه به environment | کد ورود در پاسخ HTTP برمی‌گردد ⇒ **دورزدن کامل احراز هویت** |
| CORS | `app/config.py:79-81` → allowlist پیش‌فرض localhost/127.0.0.1 | هر مرورگری روی همان ماشین دسترسی دارد |
| rate‑limit storage | `modules/auth/router.py:46` → `"memory://"` وقتی production نباشد | هر ورکر سبد جدا؛ اشتراک‌گذاری بین ورکرها ندارد |
| لاگ | `app/main.py:50` → `json_logs=settings.environment != "development"` | رندر rich روی event loop (⇒ F‑03) |
| ساخت خودکار جداول | `app/main.py:21-25` → `init_db()` فقط در development | schema بدون alembic ساخته می‌شود |

قاعدهٔ Semgrep اختصاصیِ نوشته‌شده برای همین نقص
(`mp-dev-otp-code-gated-only-by-provider`) دقیقاً روی `modules/auth/service.py:52` و `:260` fire می‌شود.

**رفع:**
1. پیش‌فرض را **`production`** بگذار (fail‑safe) یا وقتی `MP_ENVIRONMENT` ست نشده اپ **بالا نیاید**
   (با پیام روشن). این یک تغییر یک‌خطی با اثر security بحرانی است.
2. نشت `dev_code` را به دو شرط تبدیل کن: `environment == "development"` **و** `MP_ALLOW_DEV_OTP_ECHO=true`.
3. در `scripts/deploy_gate.py` یک بررسی اضافه کن: اگر روی host هدف `curl /api/v1/auth/otp/request`
   فیلد `dev_code` داشت ⇒ استقرار **رد** شود (این بررسی امروز وجود ندارد).
4. در startup یک خط لاگ با سطح WARNING چاپ کن: محیط مؤثر، provider پیامک، storage محدودیت نرخ،
   قالب لاگ، و اینکه آیا `init_db()` اجرا می‌شود.

**شاهد پذیرش:** با `MP_ENVIRONMENT` ست‌نشده، اپ یا بالا نیاید یا پاسخ `otp/request` **فاقد** `dev_code`
باشد و ورود بدون کد واقعی ممکن نباشد.

---

### F‑03 · قفل شدن سرور زیر بار؛ رندر `rich` روی event loop (Critical)

**مشاهدهٔ زنده (بدون هیچ ابزار دقیق):** با ۲۰۰ کلاینت همزمان، سرور **دقیقه‌ها پس از پایان بار**
هم هنوز قفل بود: `GET /health` → تایم‌اوت (HTTP 000) برای بیش از ۷ دقیقه؛ و `SIGTERM` را
**پاسخ نداد** — فقط با `kill -9` متوقف شد. این دقیقاً همان علامتی است که گزارش QA ثبت کرده بود
(«run 2 = 0 requests (server locked)», «locked until restart», «root cause NOT established»).

**شاهد ۱ — py‑spy روی پروسهٔ قفل‌شده (دو نمونه، ۷ دقیقه فاصله):**
```
Thread 6411 (active+gil): "MainThread"
    Text.truncate (rich/text.py:875)
    Text.wrap (rich/text.py:1248)
    Console.render (rich/console.py:1339)          ← ۴۰+ فریم رندر rich
    Table._render (rich/table.py:838)
    Console.print (rich/console.py:1731)
    RichTracebackFormatter.__call__ (structlog/dev.py:466)
    ConsoleRenderer.__call__ (structlog/dev.py:956)
    exception (structlog/_native.py:49)
    register.<locals>._unexpected (app/unhandled.py:91)   ← هندلر خطای خودِ اپ
    ServerErrorMiddleware.__call__ (starlette/middleware/errors.py:176)
```
`nlwp=84` نخ، `fd=141` (۱۲۱ تا مربوط به فایل SQLite)، CPU ‏۷۸٪. نخ اصلی همان event loop است ⇒
**در تمام این مدت هیچ درخواستی سرو نمی‌شود، حتی `/health`.**

**شاهد ۲ — کالبدشکافی لاگ:**

| اندازه | مقدار |
|---|---|
| حجم لاگ | **۱۴۸٬۱۵۴٬۱۰۵ بایت** (۸۱۷٬۰۱۲ خط) |
| تعداد `unhandled_error` | **۴** |
| حجم به‌ازای هر خطا | **≈۳۷ مگابایت** |
| فقط کد رنگ ANSI | ۱۳٬۸۸۷٬۹۰۴ escape = **۶۴٬۹۳۲٬۱۳۴ بایت** |
| کاراکتر جعبهٔ rich (`│`) | ۸٬۴۲۱٬۶۲۴ |
| نسبت دادهٔ مفید به کل | **۱ به ۱٬۰۰۰٬۰۰۰** |

**شاهد ۳ — میکروبنچمارک (`audit/bench_logging.py`) روی همان ماژول خودشان:**

| عمق پسته | ConsoleRenderer+rich (development) | JSONRenderer (production) | نسبت |
|---|---|---|---|
| ۱۰ | ۹۳٫۶ ms · ۳۵٬۹۶۱ بایت · ۲۵۳ خط | ۰٫۰۳ ms · ۲۰۲ بایت · ۱ خط | ~۳٬۱۰۰× / ~۱۷۸× |
| ۲۵ | ۱۴۸٫۶ ms · ۶۳٬۳۲۱ بایت · ۴۶۳ خط | ۰٫۰۳ ms · ۲۰۲ بایت | ~۵٬۰۰۰× / ~۳۱۳× |
| ۴۰ | ۲۱۱٫۳ ms · ۹۰٬۶۸۱ بایت · ۶۷۳ خط | ۰٫۰۴ ms · ۲۰۲ بایت | ~۵٬۳۰۰× / ~۴۴۹× |
| ۶۰ | ۲۸۷٫۳ ms · ۱۲۷٬۱۶۱ بایت · ۹۵۳ خط | ۰٫۰۳ ms · ۲۰۲ بایت | ~۹٬۶۰۰× / ~۶۳۰× |

پشتهٔ واقعیِ زیر بار ده‌ها فریمِ chained دارد، بنابراین هزینهٔ واقعی از این اعداد هم فراتر رفت
(≈۳۷ مگابایت و ≈۸۰ ثانیه برای یک خطا).

**شاهد ۴ — گروه کنترل (بدون ابزار دقیقِ ممیزی):**

| ورکر همزمان | rps | p50 | p95 | p99 | timeout کلاینت | `/health` ناموفق | زمان بازیابی |
|---|---|---|---|---|---|---|---|
| ۱۰ | ۱۹۶ | ۵۲ ms | ۱۰۳ ms | ۱۸۴ ms | ۰ | ۰/۱۰۷ | ۰٫۰۳ s |
| ۴۰ | ۲۰۹ | ۲۰۷ ms | ۳۵۱ ms | ۴۱۹ ms | ۰ | ۰/۸۹ | ۰٫۰۳ s |
| ۶۰ | ۲۰۲ | ۳۱۷ ms | ۵۱۶ ms | ۵۷۸ ms | ۰ | ۰/۸۰ | ۰٫۰۳ s |
| **۸۰** | **۹۵** | ۴۶۷ ms | ۸۰۲ ms | **۳۰٬۰۲۸ ms** | **۸۰** | **۱۱/۴۷** | **۴۳٫۶ s** |

در همان پلهٔ ۸۰، لاگ سرورِ خام هم **۳۷٬۰۴۴٬۵۰۴ بایت** شد — از **یک** خطا.
پس فروپاشی، اثر ابزار ممیزی نیست.

**رفع:**
1. در پروسهٔ سرویس‌دهنده **هرگز** `ConsoleRenderer`/`RichTracebackFormatter` استفاده نشود؛
   اگر خوانایی dev لازم است: `ConsoleRenderer(exception_formatter=PlainTextTracebackFormatter())`.
2. لاگ را از event loop جدا کن: `logging.handlers.QueueHandler` + `QueueListener` (یا
   `structlog.WriteLoggerFactory` به یک صف) ⇒ رندر/نوشتن در نخ دیگر.
3. سقف حجم: `Console(width=…)` بی‌معناست؛ بهتر است `max_exception_length` و حذف locals.
4. گیت CI: آتوماسیون بررسی کند در پیکربندی غیر‑test، `json_logs=True` است.
5. بودجهٔ لاگ در CI: اگر یک اجرای بارِ استاندارد بیش از N مگابایت لاگ تولید کرد ⇒ شکست.
6. `SIGTERM` را تست کن: زیر بار، پروسه باید در ≤۱۰ ثانیه خاموش شود.

**شاهد پذیرش:** همان بار ۸۰‌کلاینتی ⇒ لاگ < ۵ مگابایت، `/health` در تمام مدت < ۵۰۰ ms،
بازیابی < ۲ ثانیه، و خاموش‌شدن با SIGTERM < ۱۰ ثانیه.

---

### F‑04 · اشباع استخر اتصال و نبودِ کاملِ مشاهده‌پذیری pool (High)

**نقطهٔ شکست دقیق (از لاگ خودِ اپ):**
```
app/deps.py:53 in get_current_user  →  user = db.get(User, int(payload["sub"]))
  → sqlalchemy/orm/session.py:2432 _execute_internal → :2255 _connection_for_bind
  → sqlalchemy/engine/base.py:3303 raw_connection → pool/base.py:460 connect
  → pool/base.py:728 checkout → pool/impl.py:165 _do_get
sqlalchemy.exc.TimeoutError: QueuePool limit of size 40 overflow 20 reached,
                             connection timed out, timeout 5.00
```
یعنی نخستین تماس با DB در **وابستگی احراز هویت** رخ می‌دهد؛ وقتی استخر پر است، حتی
`get_current_user` شکست می‌خورد ⇒ ۵۰۰ روی همهٔ مسیرهای محافظت‌شده.

**پیکربندی فعلی (`db/base.py`):** `_POOL_SIZE=40`, `_MAX_OVERFLOW=20`, `_POOL_TIMEOUT=5`,
`_POOL_RECYCLE=1800`, `pool_pre_ping=True`؛ برای SQLite فایل‌محور
`connect_args={"check_same_thread": False, "timeout": 15}` + pragmaهای
`journal_mode=WAL`, `synchronous=NORMAL`, `busy_timeout=15000`, `foreign_keys=ON`.

**ناسازگاری ظرفیت‌ها (همه اندازه‌گیری شدند):**

| لایه | مقدار | منبع |
|---|---|---|
| هندلرهای سنکرون (`def`) در روترها | **۱۶۴** (در برابر ۲ `async def`) | شمارش روی `modules/*/router.py` |
| سقف threadpool ‏(anyio) | **۴۰ توکن** | `/audit/threads` (زنده) |
| ظرفیت استخر هر پروسه | **۶۰** (۴۰+۲۰) | `db/base.py` |
| ورکرهای uvicorn در استقرار | **۴** (`WEB_CONCURRENCY:-4`) | `Dockerfile:27` |
| ⇒ حداکثر اتصال همزمان روی یک فایل SQLite | **۲۴۰** | محاسبه |
| `pool_timeout` | ۵ ثانیه ⇒ پاسخ **۵۰۰** (نه ۵۰۳) | مشاهده |

**نبود مشاهده‌پذیری (اثبات زنده):** خروجی `GET /api/v1/metrics` شامل **۱۲ خانوادهٔ متریک** است:
`mp_http_requests_total`, `mp_http_requests_created`, `mp_http_request_duration_seconds_{bucket,count,sum,created}`,
`mp_outbox_{pending,sending,sent,dead,dead_letters,oldest_pending_seconds,worker_stale}`.
جست‌وجوی `pool|connection|session|sqlite|queue` در همان خروجی: **۰ تطبیق**.
پس پیش از این ممیزی **هیچ** راهی برای دیدن اشباع استخر وجود نداشت — دقیقاً همان چیزی که
گزارش QA را به «root cause NOT established» رساند.

**رفع:**
1. گیج‌های pool را صادر کن: `mp_db_pool_size`, `mp_db_pool_checkedout`, `mp_db_pool_overflow`,
   `mp_db_pool_wait_total`, `mp_db_pool_timeout_total`, `mp_db_connection_held_seconds` (histogram) —
   با listenerهای `checkout/checkin/connect/close/detach` (الگوی آماده در `audit/serve_backend.py`).
2. `TimeoutError` استخر را به **۵۰۳ + `Retry-After`** نگاشت کن (نه ۵۰۰) تا کلاینت‌ها طوفان تلاش مجدد نسازند.
3. `/api/v1/health/ready` را وقتی `checkedout ≥ 0.9 × capacity` برای N ثانیه پایدار بود **قرمز** کن.
4. حساب ظرفیت را مستند و گیت کن: `workers × (pool_size + max_overflow) ≤ بودجهٔ اتصال DB`؛
   برای SQLite تک‌فایل، عملاً **۱ ورکر نوشتن** یا مهاجرت به Postgres.
5. همزمانی ورودی را ببند: `--limit-concurrency` در uvicorn یا تبدیل مسیرهای داغ به `async def`.
6. گیت بار در CI با همان سناریویی که QA استفاده کرد (۲۰۰ همزمان) و آستانهٔ `p95`/`error_rate`.

---

### F‑05 · `SystemError` در گارد مجوز زیر همزمانی؛ `compile()` در هر درخواست (High)

**پشتهٔ کامل (از لاگ خودِ اپ):**
```
app/deps.py:135 in _guard          → if not enforce(user.role, request.url.path, request.method)
security/rbac.py:264 in enforce    → return bool(get_enforcer().enforce(role, path, method))
casbin/core_enforcer.py:386 enforce → :436 enforce_ex
  → :545 _get_expression → SimpleEval(expr, functions)
casbin/util/expression.py:34 __init__ → ast.parse(expr.strip()).body[0].value
/usr/lib/python3.11/ast.py:50 parse → compile(...)
SystemError: AST constructor recursion depth mismatch (before=39, after=34)
```

**چرا اتفاق می‌افتد:** `security/rbac.py:231-252` یک Enforcer تک‌نمونه با **۱۳۶ policy** می‌سازد،
ولی `enable_cache` **هیچ‌جا** فراخوانی نمی‌شود ⇒ casbin در هر `enforce()` عبارت را
`ast.parse`/`compile` می‌کند. این کار (الف) گران است و (ب) زیر همزمانیِ نخی،
شمارشِ عمقِ بازگشتِ کامپایلر CPython را به هم می‌ریزد ⇒ `SystemError` ⇒ ۵۰۰ روی مسیر احراز مجوز.

**هزینهٔ اندازه‌گیری‌شدهٔ هر `enforce()`:**

| مسیر | میانه | میانگین | بیشینه |
|---|---|---|---|
| `GET /api/v1/members` | ۲۸۹٫۲ µs | ۳۰۶٫۷ µs | ۷۱۰٫۵ µs |
| `GET /api/v1/shop/products` | ۹۱۶٫۱ µs | ۹۷۸٫۷ µs | ۴٬۲۰۸٫۳ µs |
| `GET /api/v1/admin/analytics/churn-risk` | ۹۱۱٫۱ µs | ۹۴۰٫۵ µs | ۲٬۰۱۴٫۲ µs |
| زیر ۸۰ نخ همزمان | ۱٬۰۴۱ µs | — | **p95 = ۳۳۱ ms · max = ۲٬۹۱۳ ms** |

**بازتولید بدون HTTP (`audit/repro_rbac_systemerror.py`):**

| نخ | عمق پشته | فراخوانی | `SystemError` |
|---|---|---|---|
| ۱ | ۴۰ | ۳۰۰ | **۰** |
| ۲۰ | ۴۰ | ۶٬۰۰۰ | ۲ |
| ۸۰ | ۵ | ۲۴٬۰۰۰ | ۳ |
| ۸۰ | ۴۰ | ۱۲٬۰۰۰ | ۷ |
| ۸۰ | ۴۰ | ۳۲٬۰۰۰ | ۳ |

⇒ عامل، **همزمانی نخی** است نه عمق پشته (در عمق ۵ هم رخ می‌دهد؛ در تک‌نخ هرگز).
نرخ خطا ≈ ۰٫۰۳–۰٫۰۶٪ فراخوانی‌ها ⇒ در بار واقعی یعنی ۵۰۰های پراکنده و غیرقابل بازتولید.

**نمونهٔ رفعِ اندازه‌گیری‌شده:** جدول تصمیم از پیش‌ساخته (الگوهای regex یک‌بار کامپایل +
نگاشت نقش‌ها) روی همان POLICIES/DENIES/ROLE_INHERITANCE:

| | casbin فعلی | جدول پیش‌کامپایل |
|---|---|---|
| درستی تصمیم‌ها | — | **۲۴/۲۴ یکسان** |
| میانهٔ زمان | ۹۱۰٫۷ µs | **۱۷٫۴ µs** (۵۲× سریع‌تر) |
| `compile()` در هر درخواست | بله | خیر ⇒ کلاس `SystemError` حذف می‌شود |

**رفع (به‌ترتیب اثر/هزینه):**
1. `enforcer.enable_cache(True)` (یک خط) یا بهتر: ساخت جدول تصمیم در زمان import.
2. حلقهٔ `DENIES` را با regexهای از پیش کامپایل‌شده اجرا کن (امروز `key_match2` در هر درخواست
   الگو را بازسازی می‌کند).
3. آزمون رگرسیون همزمانی: N نخ × M فراخوانی `enforce` ⇒ هیچ `SystemError`/۵۰۰.
4. متریک `mp_rbac_decisions_total{role,decision}` و `mp_rbac_errors_total` + هشدار.
5. ادغام middlewareها (امروز زنجیره ۳۰+ فریم است: `id_guard` → `correlation` → `metrics` →
   `security headers` → `CORS` → telemetry) تا عمق پشته و هزینهٔ هر درخواست کم شود.

---

### F‑06 · `/api/v1/metrics` بدون احراز هویت (High)

**مشاهده:** `GET /api/v1/metrics` بدون هیچ توکنی ⇒ **HTTP 200**، ۳۴۶ خط، ۶٬۵۲۹ بایت،
۱۲ خانوادهٔ متریک. در `api/routes.json` هم `guards: []` ثبت شده (یعنی سهوی نیست، طراحی است).

**چه چیزی نشت می‌کند:** الگوی همهٔ مسیرها (`route="/auth/otp/request"` …)، توزیع statusها،
هیستوگرام تأخیر، و **عمق صف outbox** (`mp_outbox_pending`, `mp_outbox_dead`,
`mp_outbox_oldest_pending_seconds`, `mp_outbox_worker_stale`) ⇒ نقشهٔ کامل سطح حمله +
وضعیت داخلی سرویس، رایگان.

**شاهد دوم:** `api/v1/monitoring.py:18` و `:24` دارای `try/except: pass` هستند
(Semgrep قاعدهٔ `mp-silent-except-pass` + bandit `B110`) ⇒ اگر خودِ مسیر متریک خطا دهد،
بی‌صدا می‌شکند و کسی نمی‌فهمد.

**رفع:** `require_permission("monitoring.read")` روی مسیر، یا بایند کردن متریک روی
اینترفیس/پورت داخلی، و مسدودسازی `/metrics` در Caddy برای host عمومی + آزمون «بدون توکن ⇒ ۴۰۱».

---

## ۶) یافته‌های P1/High

### F‑07 · پوشش تست مستند‌شده با اجرا رد شد (۹۴٫۲۸٪ ⟵ ۸۳٫۷۳٪)

اجرای کامل: **۱۰۹۵ پاس / ۲ skip / ۳۸ warning در ۴۶۱٫۸۲ ثانیه** (بخش «تعداد تست» دقیقاً درست است).
اما پوشش با `--cov=.` برابر **۸۳٫۷۳٪** است (۹٬۰۲۳ از ۱۰٬۷۷۶ عبارت)، نه ۹۴٫۲۸٪.

| دایرکتوری | پوشش | پوشش‌یافته/کل |
|---|---|---|
| `engine/` | ۹۷٫۲۴٪ | ۱۰۵۸/۱۰۸۸ |
| `security/` | ۹۶٫۶۱٪ | — |
| **`app/`** | **۹۴٫۲۸٪** | ۷۲۵/۷۶۹ |
| `api/` | ۹۳٫۸۱٪ | — |
| `modules/` | ۹۲٫۲۸٪ | ۴۷۴۶/۵۱۴۳ |
| `devtools/` | ۹۱٫۷۳٪ | — |
| `jobs/` | ۸۴٫۵۵٪ | — |
| `eval/` | ۸۲٫۵۶٪ | — |
| `cache/` | ۷۶٫۶۰٪ | — |
| `db/` | ۷۰٫۴۰٪ | ۱۲۱۳/۱۷۲۳ |
| `scripts/` | **۴۶٫۲۲٪** | ۵۶۲/۱۲۱۶ |
| **کل** | **۸۳٫۷۳٪** | ۹٬۰۲۳/۱۰٬۷۷۶ |
| فقط کد محصول (app+api+modules+db+engine+security+jobs+cache) | **۸۸٫۶۸٪** | — |

**ریشهٔ اختلاف:** عدد ۹۴٫۲۸٪ **دقیقاً** سهم `app/` است. یعنی عدد درست است ولی **دامنه‌اش مستند نشده**.
فایل‌های با پوشش صفر در `scripts/`: `attach_exercise_media.py`, `build_exercise_gifs.py`, `dast.py`,
`deploy_gate.py`, `export_routes.py`, `locust_m39c3.py`, `seed_s3c_m39.py`, `seed_shop.py`
— توجه اینکه `deploy_gate.py` و `dast.py` خودشان ابزار گیت‌اند و تست‌شده نیستند.

**رفع:** کنار هر عدد پوشش، **فرمان و دامنهٔ دقیق** نوشته شود؛ XML پوشش به‌عنوان artifact در CI منتشر شود؛
به‌جای یک آستانهٔ سراسری ۷۰، آستانهٔ **هر دایرکتوری** (مثلاً `modules ≥ 90`, `db ≥ 80`, `scripts ≥ 60`)
گیت شود. `--cov-fail-under=70` امروز نباید پایین‌تر برود.

### F‑08 · `logout-all` توکن‌های بدون `sid` را باطل نمی‌کند (High)

`app/deps.py:75-95` صریحاً توکن بدون `sid` را «موقتاً سازگار» نگه می‌دارد و
`app/deps.py:60-73` توکن بدون `ver` را تا وقتی `user.auth_version == 0` است می‌پذیرد.

**آزمون زنده:**

| اقدام | توکن واقعی (با `sid`) | توکن بدون `sid` |
|---|---|---|
| حالت پایه | ۲۰۰ | **۲۰۰** |
| پس از `POST /auth/logout-all` | **۴۰۱** ✅ | **۲۰۰** ⚠️ |
| پس از bump شدن `auth_version` | — | ۴۰۱ ✅ |
| پس از `is_active=0` | ۴۰۱ ✅ | ۴۰۱ ✅ |
| پس از `DELETE /auth/sessions/{id}` | ۴۰۱ ✅ | ۴۰۱ ✅ |
| `sid` ساختگی / `ver` نامعتبر | ۴۰۱ ✅ | — |

**تولیدکننده‌های توکن بدون `sid` در کد خودشان (دقیقاً ۲ مورد، با Semgrep تأیید شد):**
`scripts/dast.py:66` و `scripts/seed_s3c_m39.py:28` — هر دو توکن `super_admin` می‌سازند و
دومی آن را **روی stdout چاپ می‌کند**.

**آنچه سالم است (باید حفظ شود):** `alg=none` → ۴۰۱؛ امضای دستکاری‌شده → ۴۰۱؛ امضای بریده → ۴۰۱؛
توکن منقضی → ۴۰۱؛ نقشِ دروغین در claim (توکن `super_admin` ولی DB ‏`member`) → **۴۰۳** (DB برنده است).

**رفع:** یا `sid` را در access token **الزامی** کن (فقدان ⇒ ۴۰۱)، یا `logout-all` را طوری تغییر بده که
`auth_version` را bump کند (تا واقعاً kill‑switch باشد) + گیت CI/Semgrep که
`create_access_token(` بدون `session_id=` بیرون از تست‌ها ممنوع شود + اصلاح آن دو اسکریپت +
تاریخ انقضای صریح برای «پنجرهٔ سازگاری».

### F‑09 · مرزهای پولی: `2^53+1` و `10^18` پذیرفته می‌شوند؛ رشته به عدد تبدیل می‌شود (High)

`POST /api/v1/payments` با نقش super_admin:

| `amount_rial` ارسال‌شده | HTTP | بازگردانده‌شده | قضاوت |
|---|---|---|---|
| `2^53−1` = ۹۰۰۷۱۹۹۲۵۴۷۴۰۹۹۱ | ۲۰۰ | عیناً | ✅ (مرز امن) |
| `2^53` = ۹۰۰۷۱۹۹۲۵۴۷۴۰۹۹۲ | **۲۰۰** | عیناً | ⚠️ ناامن برای JSON/دارت/TS |
| `2^53+1` | **۲۰۰** | عیناً | ❌ باید ۴۲۲ شود |
| `10^18` | **۲۰۰** | عیناً | ❌ باید ۴۲۲ شود |
| `-5000` | ۴۲۲ | — | ✅ |
| `0` | ۴۲۲ | — | ✅ |
| `1500.75` (اعشاری) | ۴۲۲ | — | ✅ |
| `"1500000"` (**رشته**) | **۲۰۰** | `1500000` | ⚠️ coercion؛ schema سخت‌گیرانه نیست |

خودِ پروژه مرز را می‌شناسد ولی فقط برای شناسه‌ها اعمال کرده است:
`app/deps.py:36` → `MAX_SAFE_ID = 9_007_199_254_740_991` و `:39` → `PathId = Annotated[int, Path(ge=1, le=MAX_SAFE_ID)]`.
همان سقف برای **مبالغ** وجود ندارد.

Semgrep (قاعدهٔ `mp-ts-float-money`) ۷ محل پولِ شناور در استودیو پیدا کرد:
`components/PaymentPanel.tsx:69`, `pages/Analytics.tsx:101`, `pages/Analytics.tsx:105`,
`pages/Shop.tsx:624`, `pages/Shop.tsx:671`, `pages/Shop.tsx:785`, `pages/Shop.tsx:786`؛
و `mp-money-division` دو محل در بک‌اند: `modules/admin/analytics.py:157` و `:325`.

**رفع:** `amount_rial: int = Field(..., gt=0, le=9007199254740991)` روی همهٔ schemaهای پولی
(یا یک نوع `Rial = Annotated[int, …]` مشترک)؛ `strict=True` برای فیلدهای پولی تا رشته→عدد
coercion حذف شود؛ مستندسازی قاعدهٔ گرد‌کردن؛ آزمون property با hypothesis
(ماندهٔ کیف پول == Σ دفتر کل؛ رفت‌وبرگشت JSON در `2^53−1` دقیق بماند)؛
و اصلاح آن ۷ محل استودیو به قالب‌بندی صحیح ریال بدون `parseFloat`/`Number`.

### F‑10 · استودیو هیچ lint واقعی ندارد: ۳۱ خطا در نخستین اجرا (High)

ESLint 9 با flat config استاندارد (`@eslint/js` recommended + `typescript-eslint` recommended +
`react-hooks` + `jsx-a11y`) روی ۵۳ فایل `src` اجرا شد — **نخستین اجرای واقعی lint در این پروژه**:

| قاعده | تعداد |
|---|---|
| `react-hooks/set-state-in-effect` | **۱۸** |
| `jsx-a11y/label-has-associated-control` | **۱۲** |
| `@typescript-eslint/no-unused-vars` | ۲ |
| `jsx-a11y/no-autofocus` | ۱ |
| **جمع** | **۳۱ error / ۳ warning** |

بدترین فایل‌ها: `src/pages/Expenses.tsx` (۵)، `src/components/CouponPanel.tsx` (۴+۱w)،
`src/components/AdminPermissions.tsx` (۴)، `src/pages/Chat.tsx` (۲)،
`src/components/PaymentPanel.tsx` (۱+۱w)، `DeviceSessions.tsx`/`ExerciseLibrary.tsx`/`FoodLibrary.tsx` (۱).

`set-state-in-effect` یعنی state مستقیماً داخل `useEffect` ست می‌شود ⇒ رندر اضافی و
در مواردی حلقهٔ اثر؛ `label-has-associated-control` یعنی فرم‌ها برای صفحه‌خوان/کیبورد
برچسبِ برنامه‌نویسی‌شده ندارند (a11y).

**رفع:** همان flat config را در مخزن commit کن (نسخهٔ آماده در `audit/eslint-studio.flat.mjs`)،
`npm run lint` را به آن وصل کن و در CI گیت بگذار؛ ابتدا `--max-warnings` را آزاد و
خطاها را با یک PR تفکیک‌شده صفر کن (۱۸ مورد hooks + ۱۲ مورد a11y هر دو مکانیکی‌اند).

### F‑11 · امتیاز جهشِ راستی‌آزمایی‌شده روی ماژول پولی: ۵۷٫۸٪ (High)

هدف: `modules/payments/manual_transfer_policy.py` (ماشین حالت کارت‌به‌کارت، ۱۱۷ خط)
با تست اختصاصی خودش `tests/regression/test_manual_transfer_policy.py` (۱۴ آزمون، ۵۴ مورد پارامتریک، ۰٫۰۸ ثانیه).

**هشدار ابزار:** mutmut 2.x **هر ۴۵ جهش را «زنده» گزارش کرد**. راستی‌آزمایی دستی
(اعمال جهش با `mutmut apply`، اجرای pytest، بازگرداندن با `git checkout`) نشان داد
**۲۶ جهش واقعاً کشته می‌شوند**. ⇒ گزارش خودکار mutmut در این محیط **نادقیق** است و نباید مبنای گیت قرار گیرد.

| کلاس جهش | تعداد | زنده | قضاوت |
|---|---|---|---|
| معکوس‌سازی boolean / and‑or / `is not` | ۱۲ | ۱ (`#36`) | تقریباً پوشیده |
| enum → `None` | ۱۱ | ۰ | پوشیده ✅ |
| مقدار enum → `"XX…XX"` | ۱۱ | **۱۱** | شکاف واقعی: مقدار **پایدارشده/قراردادی** enum تست نشده |
| متن پیام خطا | ۱۶ | ۱۶ | نیمه‌معادل (تست‌ها `code` را نمی‌سنجند) |
| مرز عددی / پیش‌فرض | ۶ | **۲** | شکاف واقعی |
| **جمع** | **۴۵** | **۱۹** | **امتیاز جهش = ۲۶/۴۵ = ۵۷٫۸٪** |

**سه شکاف منطقیِ واقعی (هر کدام یک تست جدید می‌خواهد):**

| # | خط | جهش | چرا خطرناک است |
|---|---|---|---|
| `#27` | ~۳۹ | `value > 0` ⟶ `value >= 0` | مرز **مبلغ صفر** تست نشده؛ مبلغ ۰ می‌تواند وارد منطق مالی شود |
| `#31` | ~۴۹ | `bank_verified: bool = False` ⟶ `True` | **پیش‌فرض fail‑closed** تست نشده؛ اگر پیش‌فرض عوض شود تأیید بدون راستی‌آزمایی بانکی ممکن می‌شود |
| `#36` | ~۶۲ | `not isinstance(state…) or not isinstance(action…)` ⟶ `and` | گارد نوع فقط وقتی هر دو نامعتبر باشند خطا می‌دهد ⇒ حالت «یکی نامعتبر» پوشش ندارد |

**رفع:** سه تست مرزی بالا + تستی که **مقادیر رشته‌ای** `TransferState`/`TransferAction`
(آنچه در DB و API می‌نشیند) را قفل می‌کند + assert روی `code` خطاها (نه message) +
گیت جهش در CI روی ماژول‌های پولی با مجموعه تستِ سریع و هدفمند (نه کل سوئیت) +
راستی‌آزمایی تصادفی چند جهش با `mutmut apply` تا ابزار کالیبره بماند.

### F‑12 · `api/routes.json` مجموعهٔ گاردهای واقعی را نشان نمی‌دهد ⇒ اوراکل نامعتبر (Medium‑High)

**بخش سالم:** diff دوطرفهٔ `routes.json` با OpenAPI زنده **صفر** است (۱۶۳ عملیات، ۱۴۱ مسیر،
هیچ‌کدام اضافه/کم نیست) ⇒ فایل قرارداد **به‌روز** است.

**بخش ناسالم:** فیلد `roles` در آن فایل، مجموعهٔ **مؤثر** گاردها را نشان نمی‌دهد.
در ماتریس زندهٔ ۱۶۳×۷ (=۱٬۱۴۱ درخواست) **۶۰۲ مورد** پیش آمد که نقش «مجاز» اعلام شده بود
ولی سرور انکار کرد (۴۰۱/۴۰۳). علل واقعی (با شاهد):

| علت | نمونهٔ زنده | پیام سرور |
|---|---|---|
| بررسی مالک سیستم در بدنهٔ هندلر (بیرون از casbin) | `GET /api/v1/admin/retention` برای admin/manager ⇒ ۴۰۳ | «نگهداری داده فقط برای مالک سیستم مجاز است» |
| همان | `GET /api/v1/admin/users`, `POST/DELETE /admin/users/{id}/role` برای admin ⇒ ۴۰۳ | «فقط مالک سیستم (super_admin) می‌تواند نقش بدهد» |
| grant سطح پارامتر که در `roles` منعکس نیست | `POST /api/v1/admin/permissions` برای admin ⇒ ۴۰۳ | «نقش admin … مجاز نیست» |
| نیاز به توکنِ مقید به نشست (`sid`) | `GET /api/v1/auth/sessions`, `POST /auth/phone-change/*` برای همه ⇒ ۴۰۱ | «نشست معتبر نیست» |
| member‑scope / نقش عضویت واقعی | `GET /api/v1/assessments/member/{id}` برای عضو ⇒ ۴۰۳ | — |

**پیامد:** هر آزمون/گیتی که `routes.json` را اوراکل مجوز بداند (مثل `interaction_map.py --check`
و `tests/integration/test_route_guards.py`) **اطمینان کاذب** می‌دهد: قرارداد می‌گوید مجاز،
سرور انکار می‌کند، و هیچ‌کس متوجه نمی‌شود.

**رفع:** `routes.json` را از خودِ اپ **تولید** کن (نه دستی) و گاردهای مؤثر را کامل encode کن:
`permission` + `grant:*` + `owner_scope` + `super_admin_only` + `requires_bound_session`؛
سپس ماتریس ۱۶۳×۷ را به یک آزمون CI تبدیل کن که «مشاهده‌شده == اعلام‌شده» را assert کند
(اسکریپت آماده: `audit/probe_contract.py`).

### F‑13 · guard تکراری روی یک مسیر ⇒ دو بار `casbin enforce` (Medium)

`api/routes.json` برای `POST /api/v1/axis-assessments/{assessment_id}/review` مقدار
`guards: ["permission", "permission"]` دارد. ریشه در کد:

* `modules/axis_assessment/router.py:17` → `dependencies=[Depends(require_permission())]` (سطح روتر)
* `modules/axis_assessment/router.py:49` → `user: Annotated[User, Depends(require_permission())]` (سطح پارامتر)

یعنی در همان مسیر، گارد مجوز **دو بار** اجرا می‌شود: ~۱٫۸ ms هزینهٔ اضافی در هر درخواست
(با عدد اندازه‌گیری‌شدهٔ F‑05) و **دو برابر شدن سطح تماس** با `SystemError` همان یافته.

**رفع:** یکی از دو وابستگی حذف شود + `test_route_guards.py` طوری توسعه یابد که
«هر مسیر دقیقاً یک گارد مجوز» را assert کند (امروز فقط «حداقل یک گارد» را می‌سنجد).

### F‑14 · `gateway-return` با شناسهٔ نامعتبر → HTTP 200 (Medium)

`GET /api/v1/payments/-1/gateway-return` (بدون احراز هویت) ⇒ **HTTP 200** با صفحهٔ HTML
«پرداخت تأیید نشد / پرداخت یافت نشد». از دید کاربر رفتار درستی است، ولی:

* متریک‌ها `status=200` ثبت می‌کنند ⇒ خطای درگاه در داشبورد **دیده نمی‌شود**؛
* مانیتورهای uptime/SEO آن را «سالم» می‌شمارند؛
* در ماتریس ورودی نامعتبرِ من، تنها مورد «۲xx غیرمنتظره» همین بود (۱ از ۱٬۲۰۰+).

**گسترهٔ واقعی (پس از بازاجرای معتبر):** این فقط `-1` نیست — هر چهار مقدار `-1`, `0`, `-0` و
INT64_MIN روی همین مسیر ۲۰۰ می‌دهند، و همان الگو در ۱۱ مسیر دیگر هم هست ⇒ **F‑25**.

**رفع:** همان HTML با status **404** (یا 422) برگردانده شود + برچسب متریک مجزا
(`route="/payments/{id}/gateway-return", status="404"`) + یک آزمون.

---

## ۷) یافته‌های P2/Medium و بدهی کیفیت

### F‑15 · پیچیدگی: ۵۵ هشدار lizard و ۴۱ بلوک ≥C در radon

* lizard: **۷۴۲ تابع**، میانگین CCN ‏۳٫۵، **۵۵ هشدار** (CCN>۱۰ یا طول>۶۰ خط) — یعنی ۷٫۳٪ توابع.
* radon cc: **۹۵۶ بلوک**، میانگین **A (۲٫۹۸)**، **۴۱ بلوک C و بدتر** = C×31 · D×7 · E×1 · **F×2**.
* radon mi: ۱۹۵ فایل بررسی شد.

بدترین‌ها (با شاهد خط):

| تابع | فایل:خط | CCN (lizard) | درجه (radon) | NLOC / طول |
|---|---|---|---|---|
| `validate_production_configuration` | `app/config.py:128` | **۴۶** | **F (۴۷)** | ۱۰۰ / ۱۱۶ خط |
| `prescribe_axis_work` | `engine/axis_prescription.py:43` | — | **F (۴۶)** | — |
| `next_transfer_state` | `modules/shop/service.py:45` | — | **E (۳۴)** | — |
| `estimate_percentile` | `engine/scoring.py:33` | ۲۸ | — | ۴۸ / ۶۰ |
| `analyze` | `engine/segmental.py:66` | ۲۶ | — | ۸۵ / ۹۶ |
| `screen` | `engine/safety.py:94` | ۲۲ | — | ۶۴ / ۷۶ |
| `jp7_trend` | `modules/assessment/service.py:146` | ۲۱ | **D (۲۱)** | ۱۲۸ / ۱۵۴ |
| `get_current_user` | `app/deps.py:42` | ۱۷ | C (۱۷) | ۴۲ / ۵۵ |
| `members_summary` | `modules/admin/analytics.py:342` | ۱۷ | C (۱۷) | ۷۲ / ۸۸ |
| `process_set_feedback` | `engine/set_feedback.py:24` | ۱۶ | — | ۶۴ / ۸۲ |
| `log_food` | `modules/nutrition/service.py:103` | ۱۵ | C (۱۵) | ۵۷ / ۶۵ |
| `daily_summary` | `modules/nutrition/service.py:170` | ۱۵ | C (۱۵) | ۱۰۶ / ۱۱۸ |
| `adaptive_nutrition_report` | `modules/nutrition/service.py:372` | ۱۴ | C (۱۴) | ۶۷ / ۸۶ |
| `plan` | `engine/reminders.py:37` | ۱۴ | — | ۹۴ / ۱۰۸ |
| `confirm_phone_change` | `modules/auth/service.py:338` | ۱۳ | C (۱۳) | ۶۷ / ۷۷ |
| `client_ip` | `app/security/proxy.py:42` | ۱۲ | C (۱۲) | ۱۵ / ۱۹ |
| `collect_member_facts` | `modules/admin/analytics.py:199` | ۱۲ | C (۱۲) | ۵۱ / ۷۶ |
| `update` | `modules/expenses/service.py:72` | ۱۲ | C (۱۲) | ۴۵ / ۴۸ |
| `create_app` | `app/main.py:44` | ۴ | — | ۵۶ / **۱۱۱ خط** (طول، نه پیچیدگی) |

نکتهٔ مهم: `validate_production_configuration` با CCN ‏۴۶ هم **مهم‌ترین** تابع از نظر امنیت استقرار است
و هم بدترین از نظر پیچیدگی؛ در F‑01/F‑02 دیدیم که چند کلید حیاتی (`MP_TRUSTED_PROXIES`,
`MP_DATABASE_URL`, `MP_REQUIRE_WORKER`, `MP_RECEIPTS_DIR`, `MP_PUBLIC_BASE_URL`, `MP_SHOP_*`)
اصلاً در آن بررسی نمی‌شوند. ⇒ تفکیک به توابع کوچکِ «هر خانوادهٔ پیکربندی یک اعتبارسنج» هم
پیچیدگی را کم می‌کند هم جای طبیعیِ افزودن بررسی‌های غایب است.

### F‑16 · ایمنی ایستا: یافته‌ها کم‌شدت‌اند (نتیجهٔ مثبت با یک استثنا)

* **bandit**: ۱۰ یافته، **همه LOW** — `B105` ×۳ (از جمله `app/config.py:16` →
  `Possible hardcoded password: 'dev-secret-change-in-production-x'` که همان `DEFAULT_DEV_SECRET` است
  و در F‑02 نقش دارد)، `B112` ×۳ (try/except/pass)، `B101` ×۲ (`assert` در
  `scripts/build_exercise_gifs.py:108` و …)، `B110` ×۱ (`api/v1/monitoring.py:24`)، `B107` ×۱.
* **pip‑audit** روی **وابستگی‌های خودِ پروژه** (۲۹ نیازمندی از `pyproject.toml`، با `--no-deps`):
  **«No known vulnerabilities found»** ✅
  (هشدارهای `pip 23.0.1` و `mcp 1.29.0` که در محیط ابزارِ ممیزی دیده شد مربوط به **ابزارها** است،
  نه وابستگی‌های محصول — و عمداً از گزارش اصلی کنار گذاشته شد تا عدد کاذب نسازد.)
* **detect‑secrets**: ۶۴ فایل علامت‌خورده؛ بررسی دستی هر دو مورد `Secret Keyword` نشان داد
  **نام متغیرِ secret در سند** است نه مقدار آن:
  `docs/MuscleParadise/OPS-RUNBOOK.md:15` (فهرست نام کلیدها) و
  `finn/reports/m112-release-signing-hardening.md:38` (نام `MP_ANDROID_KEYSTORE_BASE64`).
  بقیه رشته‌های hex با آنتروپی بالا، hash امضای APK و دادهٔ گزارش‌اند.
  ⇒ **هیچ اعتبارنامهٔ واقعی در مخزن نیست** ✅ (مکملِ گیت Gitleaks خودشان).
* **vulture** (اطمینان ≥۸۰٪): فقط **۱** یافته — `modules/face_id/deep.py:74` متغیر بلااستفادهٔ `image_bgr`.
* **ruff**: `All checks passed!` و `378 files already formatted` ✅

### F‑17 · خطاهای بی‌صدا و `except: pass` (۴ محل)

Semgrep (`mp-silent-except-pass`) + bandit (`B110`/`B112`):

| محل | چرا مهم است |
|---|---|
| `api/v1/monitoring.py:18` (و `:24`) | مسیر **خودِ مشاهده‌پذیری**؛ اگر بشکند بی‌صدا می‌شود و F‑06/F‑04 قابل تشخیص نیستند |
| `scripts/dast.py:79` | ابزار DAST خطا را قورت می‌دهد ⇒ «۰ یافته» می‌تواند نتیجهٔ سکوت باشد نه سلامت |
| `scripts/dast.py:174`, `:180` | همان |

**رفع:** هر سه مورد `dast.py` باید حداقل `logger.warning` + شمارندهٔ `mp_dast_errors_total` داشته باشند؛
`monitoring.py` باید خطا را در متریکِ `mp_metrics_scrape_errors_total` بشمارد و در `/health/ready` منعکس کند.

### F‑18 · ناسازگاری ظرفیت و پیکربندی استقرار (جمع‌بندی چند لایه)

| لایه | وضعیت فعلی | خطر |
|---|---|---|
| `WEB_CONCURRENCY:-4` ورکر × ۶۰ اتصال | تا **۲۴۰ اتصال** روی **یک فایل SQLite** | اشباع/`database is locked`؛ امروز فقط `TimeoutError` استخر دیده شد چون threadpool=40 گلوگاه نخست بود |
| threadpool ‏(anyio) | ۴۰ توکن (اندازه‌گیری زنده) | صفِ پنهان؛ p99 در بار = ۳۰ ثانیه (تایم‌اوت کلاینت) |
| `pool_timeout=5` | ۵۰۰ برمی‌گرداند | کلاینت تلاش مجدد می‌کند ⇒ تشدید |
| محدودیت نرخ در غیرproduction | `memory://` **در هر ورکر جدا** | با ۲ ورکر اندازه‌گیری شد: سهمیه عملاً ۲ برابر؛ با ۴ ورکر ۴ برابر |
| `MP_TRUSTED_PROXIES=""` | هیچ اعتبارسنجی ندارد | F‑01 |
| `MP_DATABASE_URL` | در production اعتبارسنجی نمی‌شود | می‌توان ناخواسته روی SQLite رفت |
| `MP_REQUIRE_WORKER=False` | پیش‌فرض خاموش | jobها در همان پروسهٔ وب |
| `shop_online_purchase_enabled=False` | پیش‌فرض خاموش | دکمهٔ خرید در UI ⇒ `409 shop_online_closed` (در ممیزی مشاهده شد) |
| `journal_mode` پس از alembic | **`delete`** (WAL فقط در رویداد `connect` موتورِ `db/base.py` ست می‌شود) | هر ابزاری که بیرون از موتور وصل شود (alembic، اسکریپت‌ها) نه WAL دارد نه `foreign_keys=ON` ⇒ تضمین‌های ناهمگون |

**رفع:** یک جدول «حساب ظرفیت» در `OPS-RUNBOOK.md`:
`workers × (pool_size + max_overflow) ≤ بودجهٔ اتصال`؛ برای SQLite تک‌فایل ⇒ **۱ ورکر** یا مهاجرت به
Postgres؛ pragmaها را در `alembic/env.py` هم اعمال کن؛ و هر ۸ کلید بالا را به
`validate_production_configuration` اضافه کن (هر کدام با یک آزمون).

### F‑19 · سه لایهٔ جداگانهٔ دسترسی به داده در استودیو + `await import()` پویا در هندلر

| ماژول | تعداد export | مصرف‌کننده |
|---|---|---|
| `src/lib/api.ts` | **۸۱** | بیشتر صفحه‌ها/کامپوننت‌ها |
| `src/lib/session.ts` | ۱۶ | `pages/Login.tsx` |
| `src/lib/adminApi.ts` | ۱۰ | `pages/Analytics.tsx` |

و دو فراخوانی **پویا** داخل هندلر کلیک:
`pages/Shop.tsx:446` → `const { fetchOrderReceipt } = await import("../lib/api")` و
`pages/Shop.tsx:459` → `await import("../lib/api").then((m) => m.markOrderStatus(o.id, "delivered"))`.

**پیامد واقعی (در همین ممیزی دیده شد):** این دو تابع در اسکن ایستای import **بلااستفاده** به نظر
رسیدند و فقط با بررسی دستی معلوم شد زنده‌اند ⇒ هر ابزار dead‑code (vulture/knip/depcheck) روی این
پروژه **یافتهٔ کاذب** می‌دهد و اگر کسی به آن اعتماد کند، کد زنده را پاک می‌کند.
به‌علاوه bundle تقسیم می‌شود و خطای شبکه در لحظهٔ کلیک (نه در بارگذاری صفحه) رخ می‌دهد.

**رفع:** یک لایهٔ واحد API (یا حداقل یک index که هر سه را صادر کند)؛ حذف `await import()` پویا از
هندلرها؛ و اگر code‑splitting لازم است، آن را در سطح route انجام بده نه داخل onClick.

### F‑20 · exportهای مرده در `lib/api.ts` (۲ مورد از ۸۱)

پس از حذف مواردِ پویا (F‑19)، فقط این دو واقعاً مرده‌اند:

| export | محل |
|---|---|
| `updateProduct` | `src/lib/api.ts:1558` |
| `getToken` | `src/lib/api.ts` |

**رفع:** حذف یا اتصال به UI (اگر `updateProduct` باید صفحهٔ ویرایش محصول داشته باشد، این یک
**قابلیت نیمه‌کاره** است نه فقط کد مرده — باید تصمیم مالک ثبت شود).

### F‑21 · ۵ session بدون context manager در اسکریپت‌ها (شدت پایین — با تصحیح صادقانه)

Semgrep این ۵ محل را علامت زد: `scripts/build_progressions.py:241`,
`scripts/import_exercise_catalog.py:145`, `scripts/seed_criteria.py:107`,
`scripts/seed_norms.py:276`, `scripts/tag_axis_coverage.py:675`.

**تصحیح صادقانه:** بررسی دستیِ هر ۵ مورد نشان داد همه `try/…/finally: session.close()` دارند
⇒ **نشت واقعی وجود ندارد**. این یک یافتهٔ **سبک/نگهداشت‌پذیری** است (نه نشت):
الگوی `with get_session_factory()() as db:` (که در `scripts/seed_shop.py:128` و
`jobs/outbox_relay.py:41` درست استفاده شده) باید یکدست شود تا قاعدهٔ Semgrep بتواند بدون
استثنا اجرا شود و در آینده نشت واقعی پنهان نماند.

همچنین: `scripts/dast.py:89` از `hypothesis` استفاده می‌کند ولی این بسته در
`pyproject.toml` **declare نشده** ⇒ در محیط تمیز، `dast.py` با `ImportError` می‌میرد
(و چون F‑17 خطا را قورت می‌دهد، ممکن است بی‌صدا رد شود).

### F‑22 · SQL با f‑string در یک مهاجرت

`db/migrations/versions/c3f01ab129e2_m47_c1_align_indexes_and_nullability_.py:67, :165, :169, :171`.
این‌ها DDL با نام جدول/ستون‌اند (نه ورودی کاربر) ⇒ خطر تزریق عملی نیست، ولی:
(الف) قاعدهٔ «هرگز SQL با f‑string» باید بدون استثنا باشد تا گیت معنادار بماند؛
(ب) اگر نام جدول از دادهٔ runtime بیاید، همان الگو خطرناک می‌شود.
**رفع:** استفاده از `sqlalchemy.sql.quoted_name` یا `op.execute(sa.text(...).bindparams(...))` +
یک `# nosemgrep` مستند‌شده با دلیل، فقط همان‌جا.

### F‑23 · ۱۰ دکمه بدون `onClick` (موجودی، نه لزوماً نقص)

اسکن tag‑aware (پس از ردِ نسخهٔ regex که ۷۵ یافتهٔ کاذب داد):

**۸۴ دکمه** در `src/**/*.tsx` · **۷۴** با `onClick` · **۱۰** بدون `onClick` · **۰** با `onClick` تهی.

| # | محل |
|---|---|
| 1 | `components/AdminPermissions.tsx:246` |
| 2 | `components/DeviceSessions.tsx:117` |
| 3 | `components/PhoneChangeDialog.tsx:173` |
| 4 | `components/ReceiptQueue.tsx:129` |
| 5 | `components/TopBar.tsx:8` |
| 6 | `pages/Expenses.tsx:332` |
| 7 | `pages/Shop.tsx:651` |
| 8 | `pages/Shop.tsx:696` |
| 9 | `pages/Shop.tsx:741` |
| 10 | `pages/Shop.tsx:820` |

این ۱۰ مورد باید دستی مرور شوند: ممکن است `type="submit"` داخل `<form>` باشند (که سالم است)
یا دکمهٔ نمایشی/غیرفعال (که نقص UI است). چون در محیط sandbox مرورگر بی‌سر ممکن نیست
(RAM ‏۳٫۶GB و نبود Chromium)، این مرور **BLOCKED** است و باید با Playwright در CI انجام شود.
فهرست توابع API که هرگز import نشده‌اند: `fetchOrderReceipt`, `getToken`, `markOrderStatus`, `updateProduct` (که دو مورد آن در F‑19 تصحیح شد).
صفحه‌های بدون import مستقیم از `api.ts`: `pages/Analytics.tsx`, `pages/Assessment.tsx`, `pages/Login.tsx` — هر سه از لایه‌های دیگر
(`adminApi.ts`, `session.ts`, `stores/appStore`) داده می‌گیرند ⇒ **صفحهٔ مرده نیستند** (یافتهٔ کاذبِ رد‌شده).

### F‑24 · هشدارهای انباشتهٔ runtime

* `StarletteDeprecationWarning: 'HTTP_422_UNPROCESSABLE_ENTITY' is deprecated` — در اجرای بار
  **صدها بار** تکرار شد (یک بار به‌ازای هر ۴۲۲). منبع: استفاده از ثابت منسوخ در مسیر پاسخ خطا.
  ⇒ در نسخهٔ بعدی Starlette می‌شکند؛ امروز هم لاگ را پر می‌کند.
* `len(app.routes) == 7` در fastapi 0.165.0 در حالی که `app.openapi()["paths"] == 141` است
  (به‌خاطر `_IncludedRouter` تنبل) ⇒ هر اسکریپت/تستی که مسیرها را از `app.routes` بشمارد
  با ارتقای fastapi **بی‌صدا غلط** می‌شود. (در همین ممیزی اتفاق افتاد و اصلاح شد.)
* دو هشدار deprecation در `npm ci` استودیو: `whatwg-encoding` و `recharts 2.15.4`.

---

## ۸) آنچه **سالم** است — فهرست تأییدشده با اجرا

این فهرست عمداً دقیق است تا تیم بداند چه چیزی را **نباید** دوباره ممیزی یا «اصلاح» کند.

| # | مورد | شاهد اجرایی |
|---|---|---|
| ۱ | سوئیت تست بک‌اند واقعاً سبز است | ۱۰۹۵ پاس / ۲ skip در ۴۶۱٫۸۲ ثانیه |
| ۲ | سوئیت استودیو دقیقاً مطابق ادعا | ۲۸۲ پاس / ۹ skip، ۴۴ فایل پاس + ۱ skip؛ `tsc --noEmit` exit 0 |
| ۳ | مهاجرت‌ها از صفر سالم‌اند | `alembic upgrade head` روی DB خالی ⇒ head `a7c3d9e1f2b4`، ۶۵ جدول |
| ۴ | **صفر drift** بین ORM و DB | diff جدول‌ها: ۶۴ در برابر ۶۴، هیچ اختلافی |
| ۵ | قرارداد API به‌روز است | `routes.json` ⟷ OpenAPI زنده: ۱۶۳ عملیات/۱۴۱ مسیر، diff دوطرفه = **۰** |
| ۶ | هیچ ۵xx در ماتریس مجوز | ۱٬۱۴۱ درخواست: ۹۵۵ انکار، ۹۵ مجاز، ۵۷ ‏4xx کاری، **۰ خطای سرور** |
| ۷ | هیچ نشت stack trace به کلاینت | در ۱٬۹۶۱ رکورد (شامل ورودی خصمانه) **۰ مورد** |
| ۸ | پاکت خطا یکدست است | همهٔ ≥۴۰۰ با `{"error": {code, message, details}}` — **۰** پاکت ناهنجار |
| ۹ | **سقفِ** شناسه‌ها کار می‌کند (نه کف آن) | `99999999999999999999999` ⇒ ۷۰ × ۴۲۲ `invalid_id` (رفع DAST ‏M60/R18 تأیید شد)؛ `abc`/`null`/`1e5`/`1.5` ⇒ ۴۲۲/۴۰۴. **اما `-1`/`0`/`-0`/INT64_MIN ⇒ ۴۸ × ۲۰۰ ⇒ F‑25** |
| ۱۰ | مالکیت داده نشت ندارد | ۱۶ درخواست بین‌عضوی با توکن عضو ⇒ **۰ پاسخ ۲۰۰** |
| ۱۱ | JWT سخت‌گیرانه است | `alg=none`→۴۰۱، امضای جعلی→۴۰۱، امضای بریده→۴۰۱، منقضی→۴۰۱، `sid` جعلی→۴۰۱، `ver` نامعتبر→۴۰۱ |
| ۱۲ | claim نقش بر DB غلبه نمی‌کند | توکن با `role=super_admin` ولی DB ‏`member` ⇒ **۴۰۳** |
| ۱۳ | OTP یک‌بارمصرف و قفل‌شونده است | ۵ حدس اشتباه ⇒ `400 otp_locked` و کد واقعی هم رد شد؛ بازپخش ⇒ ۴xx |
| ۱۴ | idempotency پرداخت کار می‌کند | دو POST با کلید یکسان ⇒ `id` یکسان (۹ و ۹) |
| ۱۵ | کوپن تکراری رد می‌شود | ساخت کد تکراری ⇒ `409 conflict` |
| ۱۶ | **CSP وجود دارد** (یافتهٔ ایستای قبلی رد شد) | `content-security-policy: default-src 'self'; img-src 'self' data:; style-src 'self' 'unsafe-inline'; script-src 'self'; frame-ancestors 'none'` + `X-Frame-Options: DENY`, `nosniff`, `no-referrer`, `Permissions-Policy`, `COOP`, `CORP`؛ HSTS فقط در production (به‌طور عمد) |
| ۱۷ | CORS ‏fail‑closed است | Origin غیرمجاز ⇒ **۴۰۰** بدون `allow-origin`؛ `null` ⇒ ۴۰۰ |
| ۱۸ | وابستگی دوری در استودیو ندارد | madge روی ۵۴ فایل: **No circular dependency found** |
| ۱۹ | تکرار کد بسیار کم است | jscpd: ۹ clone، ۱۰۱ خط، **۰٫۲۶٪** از ۳۹٬۲۷۳ خط |
| ۲۰ | ruff/format تمیز است | `All checks passed!` · `378 files already formatted` |
| ۲۱ | وابستگی‌های محصول آسیب‌پذیر نیستند | pip‑audit روی ۲۹ نیازمندی خودِ پروژه: **No known vulnerabilities** |
| ۲۲ | رمز واقعی در مخزن نیست | detect‑secrets: هر دو `Secret Keyword` فقط **نام متغیر** در سند بودند |
| ۲۳ | اسکریپت‌ها session را می‌بندند | هر ۵ مورد علامت‌خورده `finally: session.close()` دارند (F‑21 را ببین) |
| ۲۴ | seed‌ها idempotent‌اند | `seed_shop`/`seed_criteria`/`seed_norms` بدون خطا و با گزارش JSON اجرا شدند |
| ۲۵ | نوشتن‌های اصلیسرتاسر کار می‌کنند | ۱۴/۱۶ عملیات seed زنده موفق (عضو، اشتراک، کوپن، پرداخت، کیف پول، هزینه، وزن، اعلان، چت، کلاس) |
| ۲۶ | `print()` در `lib/` کلاینت نیست | قاعدهٔ Dart semgrep: **۰** یافته (عدد «۴۱» در گزارش‌های قبلی مربوط به scripts/tests بود) |
| ۲۷ | `dangerouslySetInnerHTML` ندارد | semgrep: ۰ ⇒ مسیر XSS از این راه بسته است |

---

## ۹) صداقت: یافته‌های کاذب/نادرستِ **خودم** که با اجرا رد شدند

این بخش عمداً نگه داشته شده است. یک ممیزی که فقط «یافته» گزارش کند و اشتباهاتش را پنهان کند،
برای تیم بعدی خطرناک‌تر از نبودِ ممیزی است.

| # | ادعای قبلی (ایستا) | نتیجهٔ اجرا | قضاوت نهایی |
|---|---|---|---|
| ۱ | «CSP وجود ندارد» | هدر CSP در پاسخ‌های واقعی حاضر است (`app/security/headers.py:15-18`) | **رد شد** — از فهرست مشکلات حذف شود |
| ۲ | «پوشش بک‌اند ۹۴٫۲۸٪» | کل پروژه **۸۳٫۷۳٪**؛ ۹۴٫۲۸٪ فقط `app/` | **تصحیح شد** (F‑07) |
| ۳ | «۴۱ `print()` در کلاینت» | در `lib/` **صفر**؛ بقیه در scripts/tests | **رد شد** |
| ۴ | «۷۵ دکمهٔ بی‌سیم در استودیو» | regex من `onClick` چندخطی را نمی‌دید؛ عدد واقعی **۱۰ از ۸۴** | **رد شد** (F‑23) |
| ۵ | «همه پشت پراکسی یک سبد مشترک دارند» | بدتر از آن: با `--forwarded-allow-ips='*'` هر XFF جعلی **سبد تازه** می‌سازد (۳۰/۳۰) | **جایگزین شد** (F‑01) |
| ۶ | «مظنون نشت session: استریم AI/chat» | **هیچ** `StreamingResponse` در کل بک‌اند نیست؛ هیچ `BackgroundTasks` هم نیست | **رد شد** |
| ۷ | «احتمال نشت اتصال در اسکریپت‌ها» | همهٔ ۵ مورد `finally: close()` دارند | **رد شد** |
| ۸ | «mutmut امتیاز جهش را می‌دهد» | mutmut هر ۴۵ را «زنده» گفت؛ راستی‌آزمایی دستی: ۲۶ کشته | **ابزار نادقیق** (F‑11) |
| ۹ | «`len(app.routes)` = تعداد مسیرها» | در fastapi 0.165.0 = ۷ در برابر ۱۴۱ مسیر واقعی | **روش اصلاح شد** |
| ۱۰ | «`journal_mode=WAL` همیشه فعال است» | پس از alembic = `delete`؛ WAL فقط در رویداد `connect` موتور | **تصحیح شد** (F‑18) |
| ۱۱ | «صفحه‌های Analytics/Assessment/Login مرده‌اند» | از `adminApi.ts`/`session.ts`/`appStore` داده می‌گیرند | **رد شد** |
| ۱۲ | «`fetchOrderReceipt`/`markOrderStatus` کد مرده‌اند» | با `await import()` پویا در `Shop.tsx:446,459` استفاده می‌شوند | **رد شد** (F‑19) |
| ۱۳ | «پاس ورودی خصمانه با احراز هویت اجرا شد» | **نشد**: ۶۶۴ سلول از ۸۰۴ `401 «نشست معتبر نیست»` گرفتند چون توکن در پاس قبل با `logout-all` باطل شده بود ⇒ آن پاس **نادرس‌نتیجه** بود. با اسکریپت جدید `audit/probe_invalid_authed.py` (canary قبل/بعد، ۰ ورود مجدد) بازاجرا شد: ۸۷۲ سلول معتبر ⇒ سه یافتهٔ تازه F‑25/F‑26/F‑27 | **نقص روش‌شناختیِ خودم — اصلاح شد** |

**مواردی که BLOCKED ماندند (و نباید «سالم» فرض شوند):**

| مورد | دلیل |
|---|---|
| `flutter analyze` / `flutter test` / goldens / patrol | Flutter SDK نیست |
| ساخت APK/AAB، R8، `lintVitalRelease`، JADX، apkanalyzer | JDK/Gradle نیست |
| آشوب‌سازی کانتینری (Pumba)، hadolint روی image واقعی، `docker compose up` | Docker daemon نیست |
| Postgres / Valkey / Prometheus واقعی | نصب نیستند ⇒ سناریوی « SQLite در برابر Postgres» و «اشتراک سبد بین ورکرها» آزمایش نشد |
| آزمون UI مرورگری (Playwright/axe/Lighthouse) | Chromium بی‌سر در ۳٫۶GB RAM ممکن نیست |
| `knip` | کرش oxc‑parser روی Node 22.22.3 |
| قواعد آمادهٔ semgrep (`--config auto`, `p/python`) | دسترسی به semgrep.dev مسدود ⇒ قواعد اختصاصی آفلاین نوشته شد |
| آزمون جهش روی کل سوئیت | ۱۰۹۵ تست × ۴۶۱ ثانیه بر هر جهش ⇒ روی ۲ هسته ناممکن |
| وضعیت branch protection ‏`main` | GitHub API ⇒ **403** |
| مرور دستی ۱۰ دکمهٔ بدون onClick | نیاز به مرورگر دارد |

---

## ۱۰) جدول ابزارها و قابلیت اتکا (برای انتخاب تیم در CI)

| ابزار | نسخه | کار کرد؟ | قابلیت اتکا در این پروژه | توصیه |
|---|---|---|---|---|
| pytest + coverage | 9.2.0 | ✅ | بالا | گیت اصلی؛ دامنهٔ `--cov` را صریح بنویسید |
| ruff | 0.17.6 | ✅ | بالا | همین که هست |
| radon cc/mi | 6.0.1 | ✅ | بالا (برای روند) | آستانهٔ `cc -n C -nc` در CI |
| lizard | 1.26.1 | ✅ | بالا | `--CCN 10 --length 60 -w` به‌عنوان هشدار |
| vulture | 2.16 | ✅ | متوسط (یافتهٔ کم) | فقط با whitelist |
| bandit | — | ✅ | متوسط | مفید برای B110/B112/B105 |
| pip‑audit | 2.10.1 | ✅ | بالا — **به شرط `-r` روی نیازمندی‌های خودِ پروژه** | اگر روی محیطِ ابزار اجرا شود، یافتهٔ کاذب می‌دهد (pip/mcp) |
| detect‑secrets | 1.5.0 | ✅ | متوسط (false positive روی اسناد) | مکمل Gitleaks؛ baseline لازم دارد |
| semgrep | 1.186.0 | ✅ | **بالا با قواعد اختصاصی**؛ `auto` مسدود است | ۱۷ قاعدهٔ آماده در `audit/semgrep-mp.yml` |
| mutmut | 2.x | ⚠️ اجرا شد، **قضاوت نادرست** | پایین بدون راستی‌آزمایی دستی | هرگز بی‌راستی‌آزمایی گیت نشود |
| mutmut | 3.8.1 | ❌ CLI غیرقابل استفاده | — | استفاده نکنید |
| py‑spy | 0.4.4 | ✅ | **بسیار بالا** (ریشهٔ F‑03 را یافت) | حتماً در جعبه‌ابزار بماند |
| ESLint 9 + plugins | 9.x | ✅ | بالا | نخستین اجرای واقعی ⇒ ۳۱ خطا |
| jscpd | — | ✅ | بالا | آستانهٔ ۳٪ امن است (امروز ۰٫۲۶٪) |
| madge | — | ✅ | بالا | گیت «بدون وابستگی دوری» |
| knip | — | ❌ کرش | — | جایگزین: اسکنر اختصاصی یا `ts-prune` |
| vitest / tsc | — | ✅ | بالا | همین که هست |
| schemathesis | 4.33.4 | نصب شد | استفادهٔ کامل نکردم (ماتریس اختصاصی دقیق‌تر بود) | برای شبانه مناسب است |
| OpenTelemetry SDK | 1.45.2 | ✅ (import/سازگاری) | — | فقط با پینِ سازگار با fastapi نصب شود |

**قاعدهٔ کلی که از این ممیزی بیرون آمد:** هر ابزارِ «امتیازدهنده» (coverage، mutation score،
health score) باید **دستی راستی‌آزمایی** شود؛ در این پروژه دو مورد (coverage و mutation) عددِ
گمراه‌کننده دادند و یک مورد (knip) اصلاً کار نکرد.

---

## ۱۱) نقشهٔ رفع — اولویت، تلاش، و شاهد پذیرش

ترتیب بر اساس «اثر بر ریسک واقعی ÷ هزینه». هر ردیف یک PR جداگانه باشد.

| # | اقدام | یافته | تلاش | شاهد پذیرش (قابل اجرا در CI) |
|---|---|---|---|---|
| ۱ | `--forwarded-allow-ips="${MP_TRUSTED_PROXIES}"` + حذف `'*'`؛ الزام غیرخالی در production | F‑01 | ۱–۲ ساعت | ۳۰ درخواست با XFF تصادفی ⇒ ≥۲۷ ‏**۴۲۹** |
| ۲ | پیش‌فرض `environment` را fail‑safe کن + `dev_code` را دوشرطی | F‑02 | ۲ ساعت | بدون `MP_ENVIRONMENT`: یا بالا نیاید یا `dev_code` در پاسخ نباشد |
| ۳ | لاگ سرویس‌دهنده همیشه JSON؛ رندر در نخِ صف (`QueueHandler`) | F‑03 | ۳–۴ ساعت | بار ۸۰ کلاینتی ⇒ لاگ < ۵MB، `/health` < ۵۰۰ms، SIGTERM < ۱۰s |
| ۴ | متریک‌های pool + نگاشت `TimeoutError`→۵۰۳ + قرمزی `/health/ready` | F‑04 | ۴–۶ ساعت | `mp_db_pool_checkedout` در `/metrics`؛ بار سنگین ⇒ ۵۰۳ نه ۵۰۰ |
| ۵ | جدول تصمیم RBAC از پیش‌کامپایل (یا `enable_cache(True)`) + آزمون چندنخی | F‑05 | ۴ ساعت | ۸۰ نخ × ۴۰۰ فراخوانی ⇒ **۰** `SystemError`؛ میانهٔ `enforce` < ۵۰µs |
| ۶ | محافظت از `/api/v1/metrics` | F‑06 | ۱ ساعت | بدون توکن ⇒ **۴۰۱/۴۰۳** |
| ۷ | اصلاح عدد/دامنهٔ پوشش در اسناد + آستانهٔ هر دایرکتوری | F‑07 | ۲ ساعت | CI عدد را با دامنهٔ صریح چاپ کند؛ `db ≥ 80`, `modules ≥ 90` |
| ۸ | الزام `sid` یا bump ‏`auth_version` در `logout-all` + گیت Semgrep | F‑08 | ۳ ساعت | پس از `logout-all`: هر توکنی ⇒ ۴۰۱ |
| ۹ | سقف `le=2^53−1` و `gt=0` برای همهٔ مبالغ + strict برای پول | F‑09 | ۳ ساعت | `amount_rial=2^53+1` ⇒ **۴۲۲**؛ `"1500000"` ⇒ **۴۲۲** |
| ۱۰ | commit کردن flat config ‏ESLint + وصل کردن `npm run lint` به CI | F‑10 | ۴–۶ ساعت | `eslint .` ⇒ **۰ error** |
| ۱۱ | سه تست مرزی جهش + قفل مقادیر enum + assert روی `code` | F‑11 | ۳ ساعت | جهش‌های `#27/#31/#36` ⇒ **killed** |
| ۱۲ | تولید `routes.json` از اپ + ماتریس ۱۶۳×۷ به‌عنوان تست | F‑12 | ۶–۸ ساعت | «مشاهده‌شده == اعلام‌شده» برای هر ۱٬۱۴۱ جفت |
| ۱۳ | حذف guard تکراری + تست «یک گارد per route» | F‑13 | ۳۰ دقیقه | `routes.json` برای آن مسیر ⇒ `["permission"]` |
| ۱۴ | `gateway-return` ⇒ ۴۰۴ با همان HTML | F‑14 | ۳۰ دقیقه | `GET /payments/-1/gateway-return` ⇒ **۴۰۴** |
| ۱۵ | تفکیک `validate_production_configuration` + افزودن ۸ کلید غایب | F‑15/F‑18 | ۶ ساعت | هر کلید با یک تست؛ CCN تابع < ۱۵ |
| ۱۶ | رفع ۴ `except: pass` با لاگ + متریک | F‑17 | ۲ ساعت | Semgrep ⇒ ۰ یافته |
| ۱۷ | یکدست‌سازی لایهٔ API استودیو + حذف `await import()` در هندلر | F‑19 | ۶–۸ ساعت | grep ⇒ ۰ `await import(` در `src/**` غیر از سطح route |
| ۱۸ | تعیین تکلیف `updateProduct`/`getToken` | F‑20 | ۱ ساعت | یا حذف، یا UI + تست |
| ۱۹ | `with` برای session در ۵ اسکریپت + declare کردن `hypothesis` | F‑21 | ۱ ساعت | Semgrep ⇒ ۰ یافته؛ `python scripts/dast.py --help` در محیط تمیز کار کند |
| ۲۰ | pragmaها در `alembic/env.py` | F‑18 | ۱ ساعت | پس از `upgrade head`: `journal_mode=wal`, `foreign_keys=1` |
| ۲۱ | حذف ثابت منسوخ ۴۲۲ + اصلاح شمارش مسیرها از OpenAPI | F‑24 | ۲ ساعت | اجرای بار بدون `StarletteDeprecationWarning` |
| ۲۲ | Playwright + axe در CI (مرور ۱۰ دکمه، a11y، جریان‌های مالی روی دادهٔ مصنوعی) | F‑23/F‑10 | ۲–۳ روز | گزارش axe ⇒ ۰ خطای critical |
| ۲۳ | افزودن **کف** به گارد شناسه (`v < 1` ⇒ ۴۲۲) در `app/id_guard.py` یا اعمال `PathId` در ۵۵ امضا | F‑25 | ۲ ساعت | `probe_invalid_authed.py` ⇒ `unexpected_2xx_on_bad_id == 0` |
| ۲۴ | هندلر `StarletteHTTPException` برای نگاشت ۴۰۴/۴۰۵ مسیریابی به پاکت پروژه | F‑26 | ۱ ساعت | `fastapi_default_detail == 0` در همان پراب |
| ۲۵ | تبدیل `NotFoundError` در `_own_member` به خطای اختصاصی `409 member_profile_required` + تصمیم دربارهٔ سفارش به‌نیابت | F‑27 | ۲ ساعت (+تصمیم محصول) | `POST /shop/cart` بدون پروندهٔ عضو ⇒ ۴۰۹ با کد اختصاصی |
| ۲۶ | جایگزینی `date.today()` با `datetime.now(UTC).astimezone(ZoneInfo(settings.shop_timezone)).date()` در ۳ محل + تستِ مرزیِ نیمه‌شب؛ و ست‌کردن `ENV TZ=Asia/Tehran` در Dockerfileها (ترجیحاً هر دو) | F‑28 | ۱–۲ ساعت | `grep -rn "date.today()" modules app engine jobs` ⇒ **۰** مورد؛ تست با ساعت ۲۲:۰۰ UTC ⇒ روزِ ثبت غذایی `2026-11-22` |
| ۲۷ | `logging.error` → `logging.exception` در ۶ بلاک `except` ‏`app/sms.py`؛ allowlist از schemes برای `urlopen`؛ پاک‌سازی ۳۹ `# noqa` بلااثر با `ruff check --select RUF100 --fix` | F‑29 | ۱ ساعت | `ruff check --select TRY400,RUF100` ⇒ **۰** مورد؛ یک خطای ساختگیِ SMS با traceback کامل در لاگ ثبت شود |

---

## ۱۲) پیوست الف — فایل‌های شاهد (همه در این مخزن، شاخهٔ `arena/2cde32d6-chat2db`)

| فایل | محتوا |
|---|---|
| `audit/serve_backend.py` | لانچر ابزار‌دار: شمارندهٔ رویدادهای pool، `/audit/pool`، `/audit/threads`، OTel اختیاری |
| `audit/serve_plain.py` | لانچر **کنترل** بدون هیچ ابزار دقیق |
| `audit/harness_common.py` | ورود واقعی OTP برای ۷ هویت، mint توکن، ساخت کاربر مصنوعی در DB |
| `audit/probe_contract.py` | ماتریس ۱۶۳ عملیات × ۷ principal + پاس ورودی نامعتبر/خصمانه |
| `audit/probe_concurrency.py` | سناریوهای بار ۲۰۰‌کلاینتی با نمونه‌برداری pool |
| `audit/probe_load.py` | بار پله‌ای (۱۰/۲۰/۴۰/۶۰/۸۰/۱۲۰/۲۰۰) + اندازه‌گیری زمان بازیابی |
| `audit/probe_live_security.py` | باتری T1–T10 (rate‑limit، OTP، پول، idempotency، مالکیت، CORS، نشت، replay، هدرها) |
| `audit/probe_otp_limits.py` | آزمون‌های دقیق OTP با پنجرهٔ زمانی جدا (A–E) |
| `audit/repro_rbac_systemerror.py` | بازتولید حداقلی `SystemError` بدون HTTP |
| `audit/bench_logging.py` | میکروبنچمارک هزینهٔ رندر لاگ (rich در برابر JSON) |
| `audit/scan_ui_wiring.py` | اسکنر tag‑aware دکمه→هندلر→API |
| `audit/semgrep-mp.yml` | **۱۷ قاعدهٔ اختصاصی** Semgrep (آفلاین) — آمادهٔ commit در CI خودشان |
| `audit/eslint-studio.flat.mjs` | flat config ‏ESLint 9 آمادهٔ commit در استودیو |
| `audit/evidence/backend-coverage.xml` | گزارش کامل پوشش (مبنای F‑07) |
| `audit/evidence/openapi-live.json` | سند OpenAPI زنده (۱۴۱ مسیر/۱۶۳ عملیات) |
| `audit/evidence/metrics-noauth.txt` | خروجی `/metrics` بدون احراز هویت (F‑06) |
| `audit/evidence/contract-matrix-raw.json` | ۱٬۹۶۱ رکورد خام ماتریس مجوز + ورودی نامعتبر |
| `audit/evidence/contract-rbac-findings.json` | خلاصهٔ یافته‌های ماتریس (۶ مجازِ بدون احراز هویت، ۲ بیش‌ازحد مجاز، ۶۰۲ انکارِ مخالف قرارداد) |
| `audit/evidence/contract-invalid-findings.json` | پاس ورودی خصمانهٔ **نخست** (نادرس‌نتیجه — توکن باطل؛ فقط به‌عنوان شاهدِ نقص روش نگه داشته شده) |
| `audit/probe_invalid_authed.py` | پاس ورودی خصمانهٔ **معتبر** با canary احراز هویت (T‑34) |
| `audit/evidence/contract-invalid-authed.json` | ۸۷۲ سلول معتبر: ۰ × 5xx، ۴۸ × ۲۰۰ روی شناسهٔ غیرمجزا (F‑25)، ۷۰ × پاکت پیش‌فرض (F‑26) |
| `audit/evidence/pathid-scan.json` | اسکن گارد شناسه: ۰ کاربرد `PathId`، ۵۵ پارامتر `int` بدون گارد بازه |
| `audit/evidence/contract-diff.json` | diff قرارداد و توزیع گاردها |
| `audit/evidence/load-plain-dev.json` | بار پله‌ای روی سرور کنترل (F‑03/F‑04) |
| `audit/evidence/logging-cost.json` | جدول هزینهٔ رندر لاگ |
| `audit/evidence/rbac-systemerror-repro.json` | ماتریس نخ×عمق برای `SystemError` |
| `audit/evidence/mutmut-verified.json` | **نتیجهٔ راستی‌آزمایی‌شدهٔ** هر ۴۵ جهش |
| `audit/evidence/mutmut-manual-transfer-policy.json` | گزارش خام mutmut (برای مقایسه) |
| `audit/evidence/live-security-verdicts.json` | قضاوت‌های T1–T10 |
| `audit/evidence/live-security-raw.json` | دادهٔ خام همان باتری |
| `audit/evidence/otp-ratelimit-verdicts.json` | آزمون‌های A–E |
| `audit/evidence/otp-bruteforce.json` | ۶۰ حدس + نرخ حدس + `otp_locked` |
| `audit/evidence/xff-dockerfile-cmd.json` | آزمون XFF روی CMD واقعی Dockerfile |
| `audit/evidence/semgrep-backend.json` / `semgrep-studio.json` / `semgrep-client.json` / `semgrep-summary.txt` | خروجی کامل Semgrep با file:line |
| `audit/evidence/eslint-studio.json` | خروجی کامل ESLint 9 |
| `audit/evidence/jscpd-out/jscpd-report.json` | گزارش تکرار کد |
| `audit/evidence/studio-ui-wiring.json` | موجودی دکمه‌ها و سیم‌کشی |
| `audit/evidence/studio-dead-exports.json` | اسکن exportهای بلااستفاده |
| `audit/evidence/ruff-recommended-findings.txt` (۴۳۰ ردیف) / `ruff-recommended-stats.txt` (۵۲ قاعده) / `ruff-all-rules.txt` (۱۰۸ قاعده) / `ruff-all-families.txt` | خروجی ruff با پیکربندی پیشنهادی و با `--select ALL` — شاهد F‑28/F‑29 |
| `audit/ruff-recommended.toml` | پیکربندی پیشنهادی ruff (۴۳۰ یافته در برابر ۱۱٬۷۷۸ با `ALL`) — آمادهٔ جایگزینی در `pyproject.toml` |
| `audit/evidence/vulture.txt` / `radon-cc.txt` / `radon-mi.txt` / `lizard.txt` / `lizard-warnings.txt` / `bandit.json` / `detect-secrets.json` | خروجی خام ابزارها |

---

## ۱۳) پیوست ب — دستورات بازتولید (قدم‌به‌قدم، بدون هیچ نکتهٔ پنهان)

```bash
# ۰) پیش‌نیاز: پایتون ۳٫۱۱، Node ‏۲۲، ۲ هسته، ~۴GB RAM، ۲۰GB دیسک
#    مخزن MP را فقط‌خواندنی نگه دارید؛ همه‌چیز در /tmp/run انجام می‌شود.

# ۱) کپی کاری
cp -a /tmp/MP /tmp/run/MP && cd /tmp/run/MP && git status --porcelain | wc -l   # باید ۰ باشد

# ۲) محیط‌ها
python3 -m venv /tmp/run/venv && /tmp/run/venv/bin/pip install -U pip
/tmp/run/venv/bin/pip install -e /tmp/run/MP/mp-app/backend            # وابستگی‌های اپ
/tmp/run/venv/bin/pip install pytest pytest-cov hypothesis freezegun fakeredis deepdiff jsonschema
/tmp/run/venv/bin/pip check                                            # ⇒ No broken requirements found
python3 -m venv /tmp/run/venv-audit
/tmp/run/venv-audit/bin/pip install semgrep "mutmut<3" vulture radon lizard detect-secrets

# ۳) DB از صفر
cd /tmp/run/MP/mp-app/backend
MP_DATABASE_URL=sqlite:////tmp/run/data/mp.db /tmp/run/venv/bin/alembic upgrade head

# ۴) seed (همه مصنوعی و idempotent)
MP_ENVIRONMENT=development MP_DATABASE_URL=sqlite:////tmp/run/data/mp.db \
  PYTHONPATH=/tmp/run/MP/mp-app/backend /tmp/run/venv/bin/python /tmp/run/MP/qa-report/tools/seed_live.py

# ۵) بالا آوردن اپ (پورت ۸۰۱۰، بایند ۰٫۰٫۰٫۰)
MP_ENVIRONMENT=development MP_DATABASE_URL=sqlite:////tmp/run/data/mp.db \
MP_SECRET_KEY="audit-harness-only-secret-0123456789abcdef" MP_SMS_PROVIDER=dev \
MP_PAYMENT_GATEWAY=manual MP_RECEIPTS_DIR=/tmp/run/data/receipts MP_TRUSTED_PROXIES= \
MP_SHOP_ONLINE_PURCHASE_ENABLED=true MP_SHOP_OPEN_HOUR=0 MP_SHOP_CLOSE_HOUR=23 \
  /tmp/run/venv/bin/python /home/user/Chat2DB/audit/serve_backend.py
curl -s http://127.0.0.1:8010/health
curl -s http://127.0.0.1:8010/audit/threads     # ظرفیت threadpool در برابر pool

# ۶) آزمون‌ها
/tmp/run/venv/bin/python audit/probe_contract.py all          # ماتریس ۱۶۳×۷ + ورودی خصمانه
/tmp/run/venv/bin/python audit/probe_live_security.py         # T1–T10
/tmp/run/venv/bin/python audit/probe_otp_limits.py all        # OTP دقیق (۵ دقیقه، به‌خاطر پنجره‌های نرخ)
/tmp/run/venv/bin/python audit/bench_logging.py               # هزینهٔ رندر لاگ
/tmp/run/venv/bin/python audit/repro_rbac_systemerror.py 80 40 400
/tmp/run/venv/bin/python audit/scan_ui_wiring.py
/tmp/run/venv/bin/python audit/probe_load.py plain-dev 40 60 80 10   # روی serve_plain.py

# ۷) ابزارهای ایستا
cd /tmp/run/MP/mp-app/backend && /tmp/run/venv/bin/ruff check .
/tmp/run/venv-audit/bin/vulture app modules db engine security jobs cache api scripts devtools --min-confidence 80
/tmp/run/venv-audit/bin/radon cc app modules db engine security jobs cache api -s -n C --total-average
/tmp/run/venv/bin/lizard app modules db engine security jobs cache api --CCN 10 --length 60 -w
/tmp/run/venv/bin/bandit -r app modules db engine security jobs cache api scripts -f json -o bandit.json -q
/tmp/run/venv/bin/pip-audit -r /tmp/run/mp-deps.txt --no-deps --progress-spinner off
/tmp/run/venv-audit/bin/semgrep --config audit/semgrep-mp.yml --metrics=off --json .

# ۸) بازتولید CMD واقعی Dockerfile (برای F‑01)
/tmp/run/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8010 --workers 2 \
  --proxy-headers --forwarded-allow-ips='*'
for i in $(seq 1 30); do curl -s -o /dev/null -w "%{http_code} " \
  -H "X-Forwarded-For: 203.0.113.$((RANDOM % 250 + 1))" \
  -H 'content-type: application/json' -d '{"phone":"0913'$RANDOM$RANDOM'"}' \
  http://127.0.0.1:8010/api/v1/auth/otp/request; done; echo
# انتظار یافته: ۳۰ بار «200»  ⇒ F‑01

# ۹) آزمون جهش با راستی‌آزمایی دستی (mutmut تنها قابل اتکا نیست)
cd /tmp/run/MP/mp-app/backend
/tmp/run/venv-audit/bin/mutmut run --paths-to-mutate modules/payments/manual_transfer_policy.py \
  --runner "/tmp/run/venv/bin/python -m pytest -x -q tests/regression/test_manual_transfer_policy.py" \
  --no-progress --simple-output
for id in 27 31 36; do /tmp/run/venv-audit/bin/mutmut apply $id; \
  /tmp/run/venv/bin/python -m pytest -q tests/regression/test_manual_transfer_policy.py; git checkout -- modules/payments/manual_transfer_policy.py; done
```

---

## ۱۴) پیوست پ — آمار خام اندازه‌گیری‌ها

### ۱۴‑۱) ماتریس مجوز (۱۶۳ عملیات × ۷ principal = ۱٬۱۴۱ درخواست)

| طبقه‌بندی | تعداد |
|---|---|
| `denied` (۴۰۱/۴۰۳) | ۹۸۹ |
| `allowed_2xx` | ۹۵ |
| `reached_4xx` (مجوز رد شد، کار ۴xx داد) | ۵۷ |
| `server_error_5xx` | **۰** |
| نشت stack trace | **۰** |
| پاسخ کندتر از ۱۵۰۰ms | **۰** |

توزیع status: `401`×۹۰۵ · `403`×۸۴ · `200`×۹۵ · `422`×۴۴ · `404`×۸ · `429`×۴ · `400`×۱

۶ عملیاتی که بدون احراز هویت ۲xx دادند (همه `guards: []` در قرارداد):
`POST /auth/logout` · `POST /auth/otp/request` · `GET /health/ready` · `GET /metrics` ·
`GET /payments/{payment_id}/gateway-return` · `GET /health`
⇒ فقط `GET /metrics` (F‑06) و `gateway-return` (F‑14) نیاز به تصمیم دارند.

۲ مورد «بیش‌ازحد مجاز» در برابر قرارداد: `POST /auth/logout-all` برای `coach` و `reception`
⇒ قرارداد `roles` ناقص است (F‑12)، نه حفرهٔ امنیتی (endpoint عمداً auth‑only است).

**پاس ورودی خصمانه — نسخهٔ معتبر (۸۷۲ سلول، با canary احراز هویت):**

| status | تعداد | | status | تعداد |
|---|---|---|---|---|
| ۴۲۲ | ۵۳۱ | | ۴۰۳ | ۳۴ |
| ۴۰۴ | ۲۲۰ (۱۵۰ با پاکت پروژه، **۷۰ با پاکت پیش‌فرض** ⇒ F‑26) | | ۴۰۰ | ۲۴ |
| **۲۰۰** | **۵۵** (۴۸ شناسهٔ غیرمجزا ⇒ F‑25، ۷ بدنهٔ خصمانه در `expenses.note`) | | ۴۰۹ | ۸ |
| **۵xx** | **۰** | | نشت `Traceback` | **۰** |

پاس نخست (۸۰۴ سلول) به‌دلیل توکنِ باطل‌شده **نادرس‌نتیجه** بود و بایگانی شد (§۹ ردیف ۱۳).

### ۱۴‑۲) توزیع گاردها در قرارداد (۱۶۳ عملیات)

| گاردها | تعداد |
|---|---|
| `("permission",)` | ۱۲۹ |
| `("grant:finance.write", "permission")` | ۱۲ |
| `()` — بدون گارد | ۹ |
| `("authenticated",)` | ۶ |
| `("grant:finance.read", "permission")` | ۵ |
| `("permission", "permission")` — **تکراری** | **۱** (F‑13) |
| `("grant:reports.confidential", "permission")` | ۱ |

### ۱۴‑۳) بار پله‌ای روی سرور کنترل (بدون ابزار دقیق، لاگ dev)

| ورکر | rps | p50 | p95 | p99 | max | timeout کلاینت | health ناموفق | بازیابی |
|---|---|---|---|---|---|---|---|---|
| ۱۰ | ۱۹۶٫۰ | ۵۲٫۲ ms | ۱۰۳٫۲ ms | ۱۸۳٫۷ ms | ۴۰۹٫۶ ms | ۰ | ۰/۱۰۷ | ۰٫۰۳ s |
| ۴۰ | ۲۰۸٫۸ | ۲۰۷٫۲ ms | ۳۵۱٫۳ ms | ۴۱۸٫۹ ms | ۸۱۶٫۰ ms | ۰ | ۰/۸۹ | ۰٫۰۳ s |
| ۶۰ | ۲۰۲٫۴ | ۳۱۶٫۶ ms | ۵۱۵٫۹ ms | ۵۷۷٫۷ ms | ۷۲۶٫۵ ms | ۰ | ۰/۸۰ | ۰٫۰۳ s |
| **۸۰** | **۹۴٫۷** | ۴۶۶٫۹ ms | ۸۰۲٫۰ ms | **۳۰٬۰۲۷٫۵ ms** | ۳۰٬۴۸۶٫۶ ms | **۸۰** | **۱۱/۴۷** | **۴۳٫۶۳ s** |

### ۱۴‑۴) سناریوی ۲۰۰ کلاینت (سرور ابزار‌دار، لاگ dev)

* همهٔ درخواست‌ها `ReadTimeout` (۳۰ ثانیه) ⇒ p99 = ۳۰٬۰۸۵٫۸ ms
* `/health` در حین بار: **۳/۳ ناموفق**، بیشترین تأخیر ۱۰٬۱۵۶ ms
* پس از پایان بار: `/audit/pool` و `/health` هر دو تایم‌اوت ⇒ **بازیابی نکرد**
* لاگ: ۱۴۸٬۱۵۴٬۱۰۵ بایت / ۸۱۷٬۰۱۲ خط برای ۴ خطا
* `nlwp=84`، `fd=141` (۱۲۱ SQLite)، CPU ‏۷۸٪، SIGTERM بی‌پاسخ ⇒ `kill -9`

### ۱۴‑۵) پوشش تست (اجرای کامل)

۱۰۹۵ پاس · ۲ skip · ۳۸ warning · ۴۶۱٫۸۲ ثانیه · ۱۰٬۷۷۶ عبارت · ۹٬۰۲۳ پوشش · **۸۳٫۷۳٪**
(جدول تفکیکی در F‑07)

### ۱۴‑۶) خلاصهٔ ابزارهای ایستا

| ابزار | خروجی |
|---|---|
| ruff | All checks passed · ۳۷۸ فایل format‌شده |
| vulture (≥۸۰٪) | ۱ |
| radon cc | ۹۵۶ بلوک · میانگین A (۲٫۹۸) · ۴۱ ≥C |
| lizard | ۷۴۲ تابع · میانگین CCN ‏۳٫۵ · ۵۵ هشدار |
| bandit | ۱۰ (همه LOW) |
| pip‑audit (وابستگی‌های پروژه) | ۰ |
| detect‑secrets | ۶۴ فایل علامت‌خورده · **۰ رمز واقعی** |
| semgrep (۱۷ قاعدهٔ اختصاصی) | backend ۱۹ · studio ۸ · client ‏(Dart) ۱ |
| ESLint 9 | ۳۱ error · ۳ warning در ۵۳ فایل |
| madge | ۰ وابستگی دوری |
| jscpd | ۹ clone · ۱۰۱ خط · ۰٫۲۶٪ |
| knip | **BLOCKED** (کرش oxc‑parser) |
| mutmut | ۴۵ جهش · گزارش خودش «۴۵ زنده» · راستی‌آزمایی دستی: **۲۶ کشته / ۱۹ زنده = ۵۷٫۸٪** |

### ۱۴‑۷) اعداد کلیدی اپ (از اجرای زنده)

| کمیت | مقدار |
|---|---|
| مسیرهای OpenAPI | ۱۴۱ |
| عملیات | ۱۶۳ |
| `include_router` در `api/v1/api.py` | ۲۴ |
| جدول‌های DB پس از alembic | ۶۵ (۶۴ + `alembic_version`) |
| head مهاجرت | `a7c3d9e1f2b4` |
| هندلر سنکرون / async در روترها | ۱۶۴ / ۲ |
| سقف threadpool ‏(anyio) | ۴۰ توکن |
| pool_size / max_overflow / pool_timeout / pool_recycle | ۴۰ / ۲۰ / ۵s / ۱۸۰۰s |
| ورکرهای uvicorn در Dockerfile | `WEB_CONCURRENCY:-4` |
| خانواده‌های متریکِ عمومی | **۱۲** (۶ `mp_http_*` + ۶ `mp_outbox_*`)؛ هیچ‌کدام مربوط به pool |
| دکمه‌ها در استودیو | ۸۴ (۷۴ با onClick، ۱۰ بدون، ۰ تهی) |
| exportهای `lib/api.ts` | ۸۱ |

---

### امضای سند

* **تاریخ:** ۲۰۲۶‑۱۱‑۲۰ (UTC)
* **مخزن ممیزی‌شده:** `MP` @ `audit-main` / HEAD `662ff88` — **بدون هیچ تغییر**
  (`git status --porcelain` در پایان هر مرحله = ۰)
* **محیط اجرا:** sandbox ‏Arena — ۲ vCPU، ~۳٫۶GB RAM، پایتون ۳٫۱۱٫۲، Node ‏۲۲٫۲۲٫۳
* **اپ اجراشد:** `0.0.0.0:8010` در سه پیکربندی (ابزار‌دار / کنترل خام / CMD واقعی Dockerfile)
* **داده‌ها:** کاملاً مصنوعی
* **تعداد یافته:** ۲۹ (۳ Critical، ۶ High، **۱۰ Medium**، ۱۰ Low/Info) + ۱۲ یافتهٔ کاذبِ رد‌شده + ۱ نقص روش‌شناختیِ اصلاح‌شده
* **ابزارِ کمکیِ کشف F‑28/F‑29:** ruff ‏۰٫۱۷٫۶ با پیکربندی پیشنهادی `audit/ruff-recommended.toml`
  (۵۲ قاعده، **۴۳۰ یافته** در برابر ۱۱٬۷۷۸ مورد با `--select ALL`) — یعنی با روشن‌کردنِ قواعدِ درست،
  ruff به‌تنهایی ۶ یافتهٔ این ممیزی را بازتولید می‌کند (F‑15, F‑17, F‑13, بخشی از F‑02, کد مرده، `limiter._storage`)
  و **دو باگِ تازه** (F‑28, F‑29) را آشکار کرد. چیزی که ruff **نمی‌گیرد**: F‑04 (فراخوانی سنکرون در مسیر پرداخت،
  چون هندلرها `def`‌اند نه `async def` ⇒ `ASYNC100/ASYNC230` = صفر) و F‑22 (ruff با `S608` حتی با `--ignore-noqa`
  روی `op.execute(f"DROP INDEX …")` fire نمی‌شود ⇒ فقط قاعدهٔ اختصاصیِ semgrep آن را می‌گیرد).
  + ۱۱ مورد BLOCKED
