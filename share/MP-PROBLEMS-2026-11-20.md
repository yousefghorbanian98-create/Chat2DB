# فهرست کامل مشکلات MuscleParadise — ۲۰۲۶-۱۱-۲۰

منابع (همه خوانده و راستی‌آزمایی شدند):
`main@662ff88` · شاخهٔ `arena/da474b65-mp@0653bd1` → `docs/architecture/repowise/PROJECT-HANDOFF.md` (۴۵۹ خط) ·
`findings-main-e5c8891.md` و `findings-2026-11-20.md` (RepoWise 0.61.0) · `qa-report/FINAL-REPORT.md` ·
`qa-report/buttons.json` · `evidence/m60/*` · `docs/MuscleParadise/RELEASE-CHECKLIST.md` · ممیزی مستقیم کد
جمع: **۶۳ مشکل** — ۹ P0 · ۲۲ P1 · ۱۹ P2 · ۸ مشکل در خودِ سند تحویل · ۵ مانع محیطی

---

## الف) P0 — مانع انتشار (۹)

**A1) قفل‌شدگی کامل سرور بر اثر پر شدن استخر اتصال — ریشه‌یابی نشده**
شاهد: `qa-report/FINAL-REPORT.md` بخش ۵ («استخر `QueuePool` ظرفیت ۴۰+۲۰ پر شد، همه‌ی درخواست‌ها timeout با `pool_timeout=5s`، سرور تا ریستارت قفل ماند… **علت ریشه‌ای ثابت نشده است**»؛ اجرای ۲ = ۰ درخواست) + `PROJECT-HANDOFF.md` §۴.۴ و §۱۳.
تقویت‌کننده: grep برای `pool_size|checkedout|overflow|QueuePool` در `mp-app/backend/app` و `api` → **۰ نتیجه** = هیچ مشاهده‌پذیری‌ای از استخر وجود ندارد، پس ریشه‌یابی ممکن نیست. `/api/v1/metrics` و `/health/ready` هر دو **یک session جدید** باز می‌کنند (`api/v1/monitoring.py:14-25,31-60`) و هر scrape فشار اضافی است.
رفع: متریک استخر با event listenerهای SQLAlchemy (`checkout`/`checkin`) در Prometheus + alert؛ پیدا کردن نشت session (مظنون: مسیرهای AI/چت، `outbox`، `jobs`، پاسخ‌های جریان‌دار)؛ هارس بازتولید قطعی؛ `pool_timeout` → fail-fast با ۵۰۳ به‌جای hang؛ قرمز شدن `/health/ready` زیر فشار.

**A2) `/api/v1/metrics` کاملاً بدون احراز هویت و عمومی است**
شاهد: `mp-app/backend/api/v1/monitoring.py:14` — `@router.get("/metrics")` **هیچ dependency ندارد**؛ `api/routes.json` هم guard را `—` ثبت کرده؛ `mp-app/infra/Caddyfile` → `handle /api/* { reverse_proxy backend:8000 }` یعنی از اینترنت قابل scrape است.
چرا مهم: نرخ درخواست، تأخیر، شمار خطاها، عمق صف outbox، وضعیت worker و `checkin_slo_ok` به هر کسی داده می‌شود (اطلاعات عملیاتی/کسب‌وکار) + هر scrape یک اتصال DB می‌گیرد (تقویت A1).
رفع: `/metrics` را از مسیر عمومی Caddy خارج کن (فقط شبکهٔ داخلی/`monitoring` network) یا token/Bearer بگذار؛ اسکرپ را از Prometheus داخلی نگه دار.

**A3) `MP_TRUSTED_PROXIES` پیش‌فرض خالی است و در production اعتبارسنجی نمی‌شود → همه‌ی کاربران یک سبد rate-limit**
شاهد: `app/config.py:69` → `trusted_proxies: str = ""`؛ `app/security/proxy.py:12-13` (آدرس واقعی = `request.client.host`، XFF فقط اگر peer معتمد باشد)؛ `modules/auth/router.py:32-38`؛ و بررسی من روی `validate_production_configuration` → `trusted_proxies` **۰ بار** چک می‌شود.
چرا مهم: پشت Caddy/nginx همه‌ی درخواست‌ها از یک IP می‌آیند ⇒ `MP_OTP_RATE_LIMIT=10/minute` و `MP_LOGIN_RATE_LIMIT=10/minute` برای **کل باشگاه** جمعاً ۱۰ بار در دقیقه است ⇒ قفل‌شدگی دسته‌جمعی ورود در ساعت اوج. (سمت دیگر: اگر XFF بی‌قید اعتماد شود، دور زدن rate-limit ممکن است — کد فعلاً امن است ولی تنظیمات production اجباری نشده.)
رفع: `MP_TRUSTED_PROXIES` را به `validate_production_configuration` اضافه کن (در production پشت پراکسی الزامی) + مقدار واقعی Caddy/nginx را در `deploy.yml`/ansible ست کن + تستی که دو کلاینت مختلف دو سبد جدا داشته باشند.

**A4) `mp.db` در ریشهٔ مخزن ترک‌شده است (دیتابیس واقعی در Git)**
شاهد: `mp.db` ۸۶۴KB در ریشه؛ **۵۲ جدول** شامل `users`, `members`, `face_templates`, `payments`, `otp_codes`, `audit_logs`, `biometric_consents`, `phone_change_challenges` — امروز همه **۰ سطر**. ریشهٔ علت: `app/config.py` → `MP_DATABASE_URL` پیش‌فرض `"sqlite:///./mp.db"` (یعنی CWD = ریشهٔ مخزن). `.gitignore:63-65` فقط `mp-app/backend/*.db` را می‌پوشد، **نه ریشه**. ضمناً ۵۲ جدول در برابر **۶۴ جدول ORM** (`PROJECT-HANDOFF.md` §۵) ⇒ فایل **کهنه** هم هست.
رفع: `git rm --cached mp.db`؛ `/mp.db` و `*.db*` در `.gitignore`؛ پیش‌فرض `MP_DATABASE_URL` به مسیری ignore‌شده (مثل `var/mp.db`)؛ گیت CI که هر فایل `.db/.sqlite/.p12/.keystore/.jks/.env` ترک‌شده را رد کند و در صورت دیدن `mp.db` سطرهای جداول حساس را بشمارد.

**A5) زنجیرهٔ تأمین آرتیفکت صفر گیت دارد**
شاهد: grep روی کل `.github/workflows/` برای `sbom|trivy|grype|hadolint|cosign|syft|dependency-review|codeql|zap|oasdiff` → **۰ نتیجه**، در حالی که `container.yml` به GHCR push می‌کند و `deploy.yml` همان تگ SHA را با Dokploy بالا می‌برد.
رفع: hadolint روی ۳ Dockerfile · Trivy/Grype با `--severity CRITICAL,HIGH --exit-code 1` · SBOM CycloneDX · cosign sign + **verify در `deploy.yml` پیش از Dokploy** · `dependency-review` روی PR · job هفتگی اسکن مجدد SBOM.

**A6) هیچ گزارش خطا/crash در زمان اجرا وجود ندارد**
شاهد: grep `sentry|glitchtip|rollbar|bugsnag` در `mp-app` → **۰**. با وجود حادثهٔ A1 که «غیرقابل بازتولید» ثبت شده، یعنی در production کور هستید.
رفع: GlitchTip خودمیزبان در `docker-compose.yml`/ansible + SDK در بک‌اند (با `release=SHA` و اتصال به `request_id`) + کلاینت Flutter + استودیو وب/Electron + `before_send` برای redaction (موبایل/نام/embedding چهره/کارت) + تست redaction + alert در `alerts.yml`.

**A7) `Content-Security-Policy` هیچ‌جا تعریف نشده**
شاهد: `app/security/headers.py:10-14` و `mp-app/infra/Caddyfile:11-15` بقیهٔ هدرها را دارند (`nosniff`, `DENY`, `no-referrer`, `Permissions-Policy`, HSTS) ولی **CSP غایب است**؛ استودیو یک SPA/PWA با `public/sw.js` است.
رفع: CSP سخت‌گیرانه در هر دو لایه (`default-src 'self'`، `img-src` با `data:`/`blob:` برای GIF حرکات، `connect-src` برای API، بدون `unsafe-inline` در صورت امکان) + **تست مرورگری** که صفحه با CSP واقعی کار کند.

**A8) بیلد release اندروید بدون shrink/obfuscation و بدون AAB**
شاهد: `mp-app/client/android/app/build.gradle.kts` → هیچ `isMinifyEnabled`/`isShrinkResources`/`proguardFiles` نیست؛ grep `appbundle|.aab` در workflows → **۰**. (امضا **درست** شده: `MP_ANDROID_*` + PKCS12 و بدون fallback به debug — این بخش مشکل ندارد.)
رفع: R8 + shrink + قواعد ProGuard سازگار با Flutter؛ `flutter build appbundle` در `apk.yml` با SHA256؛ گیت اندازهٔ بیلد؛ `--analyze-size` به‌عنوان آرتیفکت؛ مقایسه با apktool-audit موجود که چیزی لازم حذف نشده.

**A9) ۲۱ آیتم باز در `RELEASE-CHECKLIST.md` (تعریف خودتان از «آمادهٔ انتشار»)**
شاهد: ۲۱ `[ ]` در برابر ۱۹ `[x]`. مهم‌ترین‌ها: خط ۱۲ **چرخش/ابطال کلید signing افشاشده** (حذف از HEAD کافی نیست) · ۱۴ کلید JWT و بیومتریک مجزای ۳۲ بایتی + secret manager · ۱۶ Valkey سالم + **rate-limit storage مشترک بین workerها** · ۱۷ `alembic upgrade head` روی scratch و clone امن backup · ۱۸ backup از `/data/mp.db` + **restore drill** + نسخهٔ رمزنگاری‌شده خارج از میزبان · ۱۹ Alertmanager با **test notification** · ۲۰ تمرین واقعی push/deploy/rollback روی staging · ۲۵-۳۲ تأییدیهٔ REA روی APK (شناسایی بیلد، امضای v1/v2/v3، عدم افشای source map/debug symbol/credential، هم‌خوانی `versionName` با تگ، `INTERNET` و `networkSecurityConfig` در مانیفست **release**، `debuggable="false"`، `ApiClient` فقط loopback/RFC1918 با HTTP) · ۳۵-۳۸ بهداشت شاخه‌ها.
رفع: هر مورد را یا با شاهد ببند، یا `BLOCKED` با دلیل و پیش‌نیاز دقیق ثبت کن (سه دسته: ایجنت / نیاز به secret یا دستگاه / فقط مالک).

---

## ب) P1 — خطر جدی و نقص کارکردی (۲۲)

**B1) کیوسک / چک‌این انتها‌به‌انتها ناقص است**
شاهد: `PROJECT-HANDOFF.md` §۱۳ («کیوسک / چک‌این مسیر ناقص است و اتصال انتها‌به‌انتها کامل نشده») + راستی‌آزمایی من: استودیو **۱۲ صفحه** دارد (§۸: dashboard, members, programs, nutrition, assessment, chat, checkin, finance, expenses, analytics, settings, shop) و **هیچ صفحهٔ کیوسک نیست**؛ `kiosk` در کل مخزن فقط ۱۰ ارجاع دارد و در استودیو فقط در `src/lib/update.ts`؛ ولی `docs/MuscleParadise/ui-previews/03-kiosk-face-gate.png` (۱٫۷MB) یک «کیوسک گیت چهره» را تبلیغ می‌کند.
رفع: یا کیوسک را پیاده و تست کن (جریان: چهره → تطبیق → چک‌این → `POST /face/checkin`) یا تصویر/ادعای مستند را اصلاح کن. این مستقیماً خواستهٔ ۲ (سیم‌کشی) است.

**B2) `POST /api/v1/axis-assessments/{id}/review` و روتر `classes` گارد تکراری دارند (کد روی کد)**
شاهد: `modules/axis_assessment/router.py:14-17` → `dependencies=[Depends(require_permission())]` روی کل روتر **و** خط ۴۹ → `user: Annotated[User, Depends(require_permission())]` روی همان endpoint ⇒ **دو بار** ارزیابی مجوز در یک درخواست. `routes.json` هم guard را `permission, permission` ثبت کرده. شمارش من: `classes/router.py` = **۴** ارجاع `Depends(require_permission`، `axis_assessment/router.py` = **۲**، بقیهٔ روترها = ۱.
رفع: یک لایه (روتر یا پارامتر) را حذف کن و الگو را یکدست کن؛ گیت CI/قاعدهٔ Semgrep که «روتر با `dependencies=[require_permission]` نباید در endpoint هم همان را بگیرد».

**B3) استودیو شناسهٔ نامعتبر `1-` را به API می‌فرستد و سرور ۲۰۰ می‌دهد**
شاهد: `mp-app/studio/src/pages/Nutrition.tsx:50` → `fetchDailyNutrition(memberId ?? -1, date, undefined, s)`؛ `qa-report/FINAL-REPORT.md` («درخواست `nutrition/food-logs/member/-1/daily` با شناسهٔ `-1`… پاسخ 200 است ولی مقدار placeholder است») و `PROJECT-HANDOFF.md` §۱۳.
رفع: در کلاینت وقتی عضو انتخاب نشده درخواست نزن (state خالی)؛ در بک‌اند شناسهٔ ≤۰ → `422`/`404`؛ یک تست پارامتری‌شدهٔ «ورودی نامعتبر» برای همهٔ endpointها با شناسهٔ منفی/صفر/بسیار بزرگ/رشته‌ای.

**B4) همزمانی کوپن روی PostgreSQL تست نشده (فقط SQLite)**
شاهد: `PROJECT-HANDOFF.md` §۱۱ («همزمانی کوپن روی PostgreSQL: تست نشده») + `_apply_coupon` در `modules/payments/service.py` + کوپن «با کلید idempotency یک‌بار مصرف می‌شود» (§۴.۲).
چرا مهم: کوپن **پول** است؛ سقف استفاده و انقضا زیر race در SQLite (که نوشتن را سریالی می‌کند) پنهان می‌ماند و در Postgres می‌تواند چندبار مصرف شود.
رفع: تست همزمانی روی Postgres واقعی (`SELECT … FOR UPDATE`/constraint یکتا) در CI؛ property تست روی «مصرف همزمان N بار ⇒ دقیقاً ۱ بار».

**B5) پول/شناسه‌ها از مرز `2^53−1` در لایهٔ JS رد می‌شوند — فقط یک مورد اصلاح شده**
شاهد: کامیت `e56db60` («fix(client): بیلد وب — سقف شناسهٔ دفتر کیف‌پول `2^53-1`»)؛ پول در بک‌اند درست است (`amount_rial`/`price_rial`/`total_rial`/`discount_rial`/`payments_total_rial`/`expenses_total_rial` همه `Mapped[int]`، `Numeric`/`BigInteger` = ۰) ولی `wallet_ledger.dart` یکی از فایل‌های **critical** RepoWise است.
رفع: یک تست مرزی سیستماتیک برای **هر** فیلد پولی/شناسه‌ای که از JSON عبور می‌کند (`2^53−2`, `2^53−1`, `2^53`, `2^63−1`) در سه لایهٔ Python→JSON→Dart/TS با assert برابری دقیق؛ قاعدهٔ Semgrep علیه `float`/`Float` روی فیلد ریالی.

**B6) قواعد گردکردن و تقسیم پول مستند/تست نشده**
شاهد: `discount_pct: Mapped[int]` (درصد صحیح) و `discount_rial`؛ حداقل مبلغ پس از تخفیف ۱٬۰۰۰ ریال (§۴.۲)؛ ولی جهت گردکردن، ترتیب اعمال چند تخفیف، و تخصیص باقی‌ماندهٔ تقسیم بین آیتم‌های سفارش (`order_items`) جایی مستند/تست نشده.
رفع: مستند + property تست (جمع اجزا = کل؛ تخفیف هرگز کل را منفی/بیش از ۱۰۰٪ نمی‌کند؛ refund ≤ مبلغ پرداختی؛ مانده = Σ دفتر کل).

**B7) هیچ تست طلایی/رگرسیون بصری برای کلاینت Flutter نیست**
شاهد: `matchesGoldenFile` → **۰ فایل**؛ آستانهٔ پوشش کلاینت **ندارد** (`flutter test --coverage` فقط جمع‌آوری می‌کند در حالی که بک‌اند `--cov-fail-under=70` دارد و واقعاً ۹۴٫۲۸٪ است).
رفع: golden برای هر صفحه × وضعیت (`default/loading/empty/error/disabled/pressed/focus/RTL/فونت ۲۰۰٪/dark`) + آستانهٔ پوشش از عدد امروز.

**B8) هیچ تست روی‌دستگاه (integration/patrol) وجود ندارد**
شاهد: `integration_test` → **۰**، `patrol` در `pubspec.yaml` → **۰**. پس جریان‌های واقعی (OTP → چک‌این → برنامه → ثبت ست → آفلاین/سینک) و dialogهای permission هرگز اجرا نشده‌اند.
رفع: patrol در CI روی امولاتور با حداقل یک جریان انتها‌به‌انتها.

**B9) دسترس‌پذیری کلاینت Flutter تقریباً وجود ندارد**
شاهد: `Semantics` فقط در **۳ فایل** از `mp-app/client/lib`؛ هیچ تست guideline (`androidTapTargets`/`labeledTapTargets`/`textContrastGuideline`) نیست؛ `PROJECT-HANDOFF.md` §۱۱ «انیمیشن: فریم‌ریت روی دستگاه اندازه‌گیری نشده» (خواستهٔ ۷).
رفع: `Semantics`/`semanticLabel` روی همهٔ کنترل‌ها + تست guideline روی همهٔ صفحات + تست `textScaler: 2.0` + تست RTL + اندازه‌گیری فریم‌ریت.

**B10) سخت‌گیری نوع در Dart فعال نیست**
شاهد: `analysis_options.yaml` = فقط `flutter_lints` + `prefer_const_constructors` + `prefer_final_locals` (بدون `strict-casts`/`strict-raw-types`/`strict-inference`)؛ `dynamic` = **۱۹۷**، `as` = **۱۹۲** (`// ignore` = ۰ که خوب است).
رفع: فعال‌کردن strict modes + قواعد ایمنی (`avoid_dynamic_calls`, `use_build_context_synchronously`, `cancel_subscriptions`, `close_sinks`) + رفع واقعی + گیت ضد‌رگرسیون روی ۱۹۷/۱۹۲.

**B11) اسکریپت `lint` استودیو مرده است**
شاهد: `mp-app/studio/package.json` → `"lint": "eslint src --ext .ts,.tsx"` ولی **`eslint` در `devDependencies` نیست** (devDeps: testing-library×2، types/react×2، vite plugin، autoprefixer، jsdom، postcss، tailwindcss، typescript، vite، vitest) و **هیچ فایل کانفیگ eslint** ترک‌شده نیست؛ job `studio` هم فقط test/build/audit را اجرا می‌کند.
رفع: ESLint 9 + flat config + `typescript-eslint` + `react-hooks` + a11y و وصل کردنش به job `studio`، یا حذف اسکریپت مرده. (`--ext` سینتکس ESLint 8 است.)

**B12) نصب غیرقطعی در CI**
شاهد: `ci.yml:178` و `ci.yml:392` → `npm ci || npm install` با وجود `mp-app/studio/package-lock.json` ترک‌شده.
رفع: `npm ci` خالص؛ ناسازگاری lockfile باید بیلد را قرمز کند.

**B13) وابستگی اعلام‌نشده: DAST روی محیط تازه می‌شکند**
شاهد: `mp-app/backend/scripts/dast.py:89` → `import hypothesis.strategies as st` ولی `hypothesis` در `[project.optional-dependencies] dev` **نیست** (dev deps: setuptools، pytest، pytest-cov، pytest-asyncio، ruff، bandit، pip-audit، faker، pyyaml، Pillow).
رفع: افزودن `hypothesis` به dev extra + تست smoke که `dast.py --max-examples 1` روی محیط تازه اجرا شود. (ضمناً `dast.py` به هیچ job زمان‌بندی وصل نیست.)

**B14) `openapi.json` در مخزن commit نشده ⇒ تغییر شکننده دیده نمی‌شود**
شاهد: `git ls-files | grep -iE 'openapi|swagger'` → **۰**؛ قرارداد در `mp-app/backend/api/routes.json` (۱۴۱ مسیر/۱۶۳ عملیات) نگه داشته می‌شود و گیت `scripts/interaction_map.py --check` پاس است، ولی **گیت breaking-change** وجود ندارد.
رفع: استخراج و commit `openapi.json` + گیت drift + `oasdiff breaking` روی PR + سیاست نسخه‌بندی و حداقل نسخهٔ کلاینت.

**B15) `live-contract` فقط استودیو را پوشش می‌دهد، نه کلاینت Flutter**
شاهد: `ci.yml` job `live-contract` → `mp-app/studio/tests/liveContract.test.ts`؛ کلاینت Dart هیچ تست قرارداد زنده ندارد (با ۴۴ فایل Dart در `lib`).
رفع: یک لایهٔ کلاینت API یا تست Dart در برابر همان API زنده با seed موجود.

**B16) ماتریس مجوز/مالکیت به‌صورت سیستماتیک تست نشده**
شاهد: مسیرهای حساس با نقش‌های گسترده: `DELETE /api/v1/face/enroll/{member_id}` و `POST /api/v1/face/enroll` نقش `member` را می‌پذیرند (مالکیت در `service.delete_face` با `ensure_member_scope` درست رعایت شده ✅)، `POST /api/v1/payments/{payment_id}/callback` **بدون هیچ گارد** است (فقط `authority` + `callback_token`)، `GET /api/v1/payments/coupons` با `grant:finance.write` ولی نقش `member` مجاز است، `GET /api/v1/reports/confidential/{member_id}` با نقش `coach`.
رفع: یک تست پارامتری‌شده {نقش × مالکیت منبع × ورودی نامعتبر} برای همهٔ مسیرهای مالی/چهره/محرمانه؛ تست صریح اینکه `callback` وقتی `MP_PAYMENT_GATEWAY=manual` است رد شود و امضای مبلغ واقعاً بررسی شود؛ کلید idempotency برای POSTهای حساس (الگوی `_settle_shop_order` را تعمیم بده).

**B17) `MP_REQUIRE_WORKER=False` ⇒ readiness می‌تواند بدون worker صف سبز شود**
شاهد: `app/config.py:71` → `require_worker: bool = False`؛ `api/v1/monitoring.py:61` → `if settings.require_worker:` یعنی بررسی heartbeat worker **اختیاری** است و در `validate_production_configuration` هم چک نمی‌شود. `worker_ok = True` پیش‌فرض است.
چرا مهم: اگر worker اجرا نشود، صف `outbox` (SMS/اعلان) بی‌صدا پر می‌شود و `dead_letters` رشد می‌کند در حالی که `/health/ready` سبز است و Dokploy ترافیک را قطع نمی‌کند.
رفع: در production `require_worker` را الزامی کن (اعتبارسنجی config) + alert روی عمق صف و heartbeat.

**B18) `MP_DATABASE_URL` در production اعتبارسنجی نمی‌شود**
شاهد: بررسی من روی `validate_production_configuration` → `database_url` **۰ بار** چک می‌شود (در برابر Valkey که loopback بودنش رد می‌شود). یعنی production می‌تواند بی‌صدا روی SQLite بماند؛ ADR‑002 هم مسیر مهاجرت به Postgres را دارد ولی تصمیم بسته نشده (`PROJECT-HANDOFF.md` §۱۳: «PostgreSQL، Valkey، pgBackRest، Prometheus در نقشه‌اند و در این مخزن به‌صورت کامل اجرا و تأیید نشده‌اند»).
رفع: یا SQLite را با شروط صریح و سقف‌های مستند مجاز کن، یا در production URL غیر‑SQLite را الزامی کن؛ ADR‑002 را با اعداد بارِ Postgres در برابر SQLite به‌روز کن.

**B19) سه `except Exception: pass` بی‌صدا در مسیر مانیتورینگ**
شاهد: `api/v1/monitoring.py` → ۳ مورد (`# noqa: BLE001`)؛ مجموع `except Exception` در بک‌اند از **۱۱ به ۲۲** رسیده (بدون گیت).
رفع: تفکیک استثنای دقیق، لاگ ساخت‌یافته با سطح، و متریک «scrape degraded» تا خرابی DB در `/metrics` پنهان نماند؛ قاعدهٔ Semgrep علیه بلعیدن بی‌صدا.

**B20) وبِ کلاینت هرگز در PR/push گیت نمی‌شود**
شاهد: `.github/workflows/web.yml` → فقط `on: workflow_dispatch:` (برخلاف `apk.yml` که `push: tags: ["v*"]` هم دارد). کامیت `ae3e260` یک باگ واقعی وب (`dart:io` در کد وب‌سازگار) را رفع کرد ⇒ رگرسیون محتمل است.
رفع: `web.yml` را روی `pull_request`/`push` (حداقل برای تغییرات `mp-app/client`) اجرا کن + گیت ضد‌رگرسیون «`dart:io` در کد وب وارد نشود» + یک تست مرورگری روی بیلد وب.

**B21) Electron و Service Worker سخت‌سازی/تست نشده‌اند**
شاهد: `mp-app/studio/electron/main.cjs` → `contextIsolation: true`, `nodeIntegration: false` ✅ ولی **بدون `sandbox`، بدون `setWindowOpenHandler`، بدون guard برای `will-navigate`/`will-attach-webview`**؛ `public/sw.js` → cache-first برای assets و `skipWaiting`+reload، ولی هیچ تستی ندارد که پس از logout دادهٔ حساسی در `caches` نماند و ناسازگاری نسخهٔ SW با API جدید چه می‌کند.
رفع: `sandbox: true` + deny برای window.open + guard ناوبری + تست vitest روی کانفیگ main process (چون `doyensec/electronegativity` آرشیو شده) + تست چرخهٔ logout/SW.

**B22) تست بار فقط ۲ اندپوینت سبک را می‌کوبد و فقط روی SQLite/یک worker معتبر است**
شاهد: `mp-app/tests/load/k6-gate.js` → فقط `GET /api/v1/health/ready` و `POST /api/v1/auth/otp/request`؛ `qa-report/FINAL-REPORT.md` صریحاً «این عددها روی SQLite و یک worker در sandbox است و **تأیید production نیستند**»؛ هیچ گیت N+1 و هیچ پروفایلی (py-spy) نیست.
رفع: ≥۵ سناریوی سنگین (چک‌این/تطبیق چهره، تجویز AI، ثبت ست، تجمیع داشبورد و گزارش سود/زیان، سرو `/media/*` و `static/exercises/*.gif` با سنجش hit rate کش) + گیت شمارش کوئری + اجرای موازی روی Postgres.

---

## ج) P2 — کیفیت، بهداشت و کلاس جهانی (۱۹)

**C1) ۶۷۰ یافتهٔ سلامت کد (۲۵ critical، ۷۰ high)** — `findings-main-e5c8891.md`. میانگین ۹٫۲۶/۱۰، میانگین کد تولیدی ۸٫۹۵ (۲۸۷ فایل)، بدترین فایل `mp-app/studio/src/pages/Shop.tsx` = **۶٫۰**.
**C2) شش نقطهٔ داغ critical:** `client/lib/core/app_state.dart` (۳)، `client/lib/core/offline_feedback_outbox.dart` (۳)، `backend/app/config.py` (۲)، `studio/src/pages/Shop.tsx` (۲)، `client/lib/features/wallet/wallet_ledger.dart` (۲)، `client/lib/features/chat/member_chat_data.dart` (۲) — دو تای آخر مستقیماً پول و چت‌اند.
**C3) توابع بیش‌ازحد بزرگ:** `large_method` در `studio/src/pages/Nutrition.tsx` (بدترین نمرهٔ high، ‑۰٫۸۰)، `backend/app/config.py::validate_production_configuration`، `backend/engine/axis_prescription.py::prescribe_axis_work` ⇒ خواستهٔ ۱۰ (ساده‌سازی).
**C4) `io_in_loop` در چند اسکریپت ابزار و importer** (بسیاری خارج از مسیر تولید — باید تفکیک و مستند شوند تا نویز از سیگنال جدا شود).
**C5) ۳۵ یافتهٔ کد مرده:** ۲۹ `unused_export` + ۶ `unreachable_file`. اطمینان بالا ۲ مورد؛ **`UpdateService` در `mp-app/client/lib/core/updater/update_service.dart` دستی تأیید شد که هیچ callerی در `lib/` ندارد** (و ضمناً بنر به‌روزرسانی استودیو روی محتوا می‌افتد — یعنی مسیر «به‌روزرسانی» هم کد مرده دارد هم باگ UI). `modules/shop/service.py::checkout/list_orders/mark_order` علامت خورده‌اند ولی **احتمالاً از مسیر پویا صدا زده می‌شوند** — قبل از حذف بررسی کن (۳۳ مورد با اطمینان متوسط/پایین ۰٫۴).
**C6) ۲۵ یافتهٔ رانش مستندات در ۱۴ سند** (از ۲۰۲ سند و ۴٬۰۴۸ ارجاع): ارجاع به فایل‌های ناموجود مثل `docs/apk-signature.md` و `finn/reports/2026-11-14-global-report.md` ⇒ یا اصلاح مسیر یا علامت‌گذاری صریح «سند تاریخی».
**C7) هیچ ابزار سنجش تکرار/مرده/پیچیدگی در CI نیست:** `jscpd`/`knip`/`vulture`/`lizard`/`radon`/`import-linter`/`dependency-cruiser` → ۰. خواسته‌های ۹، ۱۰، ۱۱ بدون گیت‌اند. خطر واقعی: منطق موازی بین `engine/` (۱۹ موتور) و `modules/*` (۲۴ ماژول).
**C8) هیچ تست جهش (mutation) نیست** ⇒ پوشش ۹۴٫۲۸٪ اثبات نمی‌کند تست‌ها باگ می‌گیرند (برای ۱۹ موتور عددی + `engine/safety.py` حیاتی است).
**C9) هیچ تست ویژگی‌محور (property) نیست** (`tests/property/` وجود ندارد) ⇒ نامتغیرهای ایمنی/حجم/امتیاز/سینک LWW/تغذیه/ریسک ریزش اثبات نشده‌اند.
**C10) هیچ l10n/i18n نیست:** فایل‌های `.arb`/`l10n`/`intl` → **۰**؛ همهٔ رشته‌ها hardcode؛ تست کلید گم‌شده و pseudo-localization هم نیست.
**C11) دو نقص نمایشی بازِ QA:** بنر به‌روزرسانی روی محتوای صفحه می‌افتد؛ ایموجی ❤️/💚 در فوتر به‌صورت جعبه رندر می‌شود (فونت/فالبک ایموجی) — `qa-report/FINAL-REPORT.md` §۳ و `PROJECT-HANDOFF.md` §۱۳.
**C12) ۴۱ `print()` در کد غیرتست بک‌اند** (بدون logger ساخت‌یافته، بدون گیت).
**C13) ۴۸ `TODO/FIXME/HACK` در `mp-app`** (از ۴۲ بیشتر شده) — هیچ‌کدام به `BUILD-QUEUE.md` وصل نیستند.
**C14) ۶ تست skip/disabled در بک‌اند + ۹ skip در استودیو + ۲ skip گزارش‌شده** — هیچ‌کدام دلیل `BLOCKED` مستند ندارند.
**C15) هیچ گیت خودکار لایسنس وابستگی‌ها نیست** (`pip-licenses`/`license-checker` → ۰ در workflows) در حالی که لایسنس محصول Proprietary است و `pip-audit`/`npm audit` فقط آسیب‌پذیری می‌بینند. (دارایی‌های ثالث **عالی** مستند شده‌اند: `NOTICE-THIRD-PARTY.md` با Unlicense برای `yuhonas/free-exercise-db` + commit `f00c92c` + sha256، و MIT برای REA skill.)
**C16) هیچ ابزار آشوب/تنزل نیست:** `toxiproxy|chaos|respx|vcrpy` → **۰**؛ سناریوهای «DB قفل»، «دیسک پر»، «AI timeout»، «SMS پایین»، «چهره پایین»، «Valkey پایین» تست نشده‌اند؛ `test_backup_drill.py` **برابری داده‌های restore** را assert نمی‌کند (آیتم ۱۸ چک‌لیست).
**C17) provenance تصاویر مستند نشده:** `docs/MuscleParadise/ui-previews/*.png` (۸ تصویر تا ۲٫۱MB، شامل `03-kiosk-face-gate.png`، `04-payment-receipt.png`، `05-member-profile.png`) و `qa-report/screenshots/*.png` (۱۱ تصویر از محیط اجرا) در مخزن‌اند؛ دادهٔ seed مصنوعی است (`qa-report/tools/seed_live.py`، شماره‌های `0912…`، «عضو فیک …» در `buttons.json`) ولی **هیچ سندی اثبات نمی‌کند** چهره/رسید/شماره واقعی نیستند.
**C18) `.semgrep/project-rules.yml` فقط یک فایل قاعده دارد** و هیچ قاعده‌ای برای پول شناور، `print`، `debugPrint`، `console.log`، بلعیدن استثنا، یا گارد تکراری (B2) ندارد.
**C19) فایل‌های سنگین و بزرگ‌ترین‌های ترک‌شده:** ۱۲۶ PNG + ۳۴ JPG + ۱۷ GIF؛ `ui-previews/07-client-home-grid.png` ۲٫۱MB، `data/external/free_exercise_db/exercises.json` ۹۸۴KB، `mp.db` ۸۶۴KB ⇒ حجم مخزن ۸۳٫۹MB؛ بهینه‌سازی/LFS و گیت اندازه لازم است.

---

## د) مشکلات خودِ `PROJECT-HANDOFF.md` و ابزار تولیدش (۸)

این‌ها مهم‌اند چون این سند قرار است **منبع حقیقت نشست‌های بعدی AI** باشد و از روز اول ۳ ادعای نادرست دارد.

**D1) جدول مجوزها (§۷) خالی چاپ شده** — در حالی که `app/security/grants.py:34` → `KNOWN_PERMISSIONS` پنج کلید دارد (`finance.write`, `finance.read`, `reports.confidential`, `roles.manage`, `flags.write`) و §۳ همان‌ها را به‌صورت `grant:…` روی مسیرها نشان می‌دهد ⇒ پارسر `scripts/repowise_handoff.py` دیکشنری چندخطی را نمی‌خواند. **بدترین نوع drift: سند مرجع، کاتالوگ مجوزها را ندارد.**
**D2) §۶ مقدار پیش‌فرض `MP_CORS_ORIGINS` را `(` نشان می‌دهد** — چون مقدار یک رشتهٔ چندخطی داخل پرانتز است (`app/config.py:79`) ⇒ همان باگ پارسر؛ مقدار واقعی در سند نیست.
**D3) §۱۳ می‌گوید «`web.yml` و `apk.yml` فقط `workflow_dispatch` دارند»** — غلط: `apk.yml` علاوه بر dispatch روی `push: tags: ["v*"]` هم اجرا می‌شود (و §۱۰ همان سند درست نوشته) ⇒ **تناقض داخلی سند**. (بخش درست ادعا: `web.yml` واقعاً فقط dispatch است — B20.)
**D4) §۲ می‌گوید پیشوندهای بی‌پوشه «در `api/` یا `app/` تعریف شده‌اند»** — برای `face` نادرست است: روتر در `modules/face_id/router.py` است و فقط **پیشوند با نام پوشه فرق دارد** (`/face` در برابر `face_id`) ⇒ سند، خواننده را به مسیر اشتباه می‌فرستد.
**D5) سند روی شاخهٔ مرج‌نشده است** (`arena/da474b65-mp`، ۲ کامیت جلوتر از `main`، فقط ۹۹۵ خط سند/اسکریپت) و `scripts/repowise_handoff.py --check` به **هیچ گیت CI** وصل نیست ⇒ به‌محض مرج، اولین تغییر کد آن را کهنه می‌کند (همان بلایی که سر D1‑D4 آمد).
**D6) §۱۱ می‌گوید اسکرین‌شات‌ها در `docs/MuscleParadise/screenshots/`** در حالی که مسیر واقعی `qa-report/screenshots/` و `docs/MuscleParadise/ui-previews/` است (۲۶ PNG در `docs/MuscleParadise`) ⇒ ارجاع نادرست.
**D7) اختلاف اعداد بین دو سند RepoWise:** `findings-main-e5c8891.md` → ۲۷۳ لینک محلی / بدترین فایل `Nutrition.tsx`؛ `PROJECT-HANDOFF.md` §۱۱ → ۲۷۶ لینک؛ `findings-2026-11-20.md` → بدترین فایل ۶٫۰ بدون نام در برابر `findings-main-e5c8891.md` → `Shop.tsx`. سه snapshot مختلف (`b194e96`، `e5c8891`، `c06e353`) بدون اینکه بگویند کدام معتبر است ⇒ گیج‌کننده برای ایجنت بعدی.
**D8) §۲ فهرست ماژول‌ها ناقص است:** `modules/` امروز ۲۴ پوشه دارد (`ai`, `ai_engine`, `admin`, `assessment`, `auth`, `axis_assessment`, `classes`, `content`, `exercises`, `expenses`, `face_id`, `membership`, `notification`, `nutrition`, `outbox`, `payments`, `population`, `privacy`, `programs`, `reporting`, `reports`, `shop`, `updates`) و جدول سند ۲۳ ردیف دارد؛ ضمناً ۱۱ ماژول با **۰ مسیر API هم‌نام** نشان داده شده‌اند که برای `face_id`/`notification`/`membership` ناشی از همان اختلاف پیشوند است (نه نبودِ API) ⇒ خطر نتیجه‌گیری اشتباه.

---

## ه) مواردی که مشکل **نیستند** (تا دوباره انجام نشوند)

- **امضای Android:** `build.gradle.kts:34-49` از `MP_ANDROID_KEYSTORE_PATH/_STORE_PASSWORD/_KEY_ALIAS/_KEY_PASSWORD` با `storeType PKCS12` می‌خواند و **fallback به کلید debug حذف شده** (با کامنت صریح). تنها مانع، تنظیم نشدن secretهاست (§۱۱).
- **اعتبارسنجی پیکربندی production قوی است** (`app/config.py:127-243`): حداقل بایت `MP_SECRET_KEY` و رد `DEFAULT_DEV_SECRET`/`change-me`/`example`؛ `MP_BIOMETRIC_KEY` الزامی + Base64 معتبر + **دقیقاً ۳۲ بایت** + **باید از `MP_SECRET_KEY` جدا باشد**؛ `MP_SMS_PROVIDER=dev` ممنوع + فیلدهای اجباری هر provider + HTTPS بدون credential در URL؛ Valkey غیر‑loopback؛ CORS allowlist بدون `*` و فقط HTTPS؛ `MP_PAYMENT_GATEWAY=mock` و `sandbox` در production ممنوع؛ `manual` + `MP_PAYMENT_SANDBOX=true` رد می‌شود. (کمبودش فقط A3/B17/B18 است.)
- **پول همه‌جا عدد صحیح ریال است** (`Numeric`/`BigInteger` = ۰؛ `Float` فقط برای `grams`, `weight_kg`, `score`, `percentile`, `raw_value`, `sdc`).
- **زمان:** صفر `datetime.now()` naive؛ ۱۵ ارجاع `zoneinfo`/`Asia/Tehran`/`timezone.utc`؛ ۲۵ فایل منطق جلالی.
- **XFF/پراکسی امن پیاده شده** (`app/security/proxy.py` — fail-safe با allowlist)؛ فقط تنظیمش در production اجباری نشده (A3).
- **مالکیت در مسیر چهره رعایت شده** (`service.delete_face:148-162` → `ensure_member_scope` + `audit`).
- **Electron پایه امن است** (`contextIsolation: true`, `nodeIntegration: false`)؛ فقط سخت‌سازی تکمیلی مانده (B21).
- **هدرهای امنیتی بک‌اند و Caddy کامل‌اند** (`app/security/headers.py` + `Caddyfile` با HSTS دو ساله و حذف `-Server`)؛ فقط CSP مانده (A7).
- **کد stub وجود ندارد:** `NotImplementedError`/`UnsupportedOperationException`/«not implemented» = **۰** (در ممیزی قبلی ۳۶ بود).
- **استودیو type-safe است:** `tsconfig` → `"strict": true` و **`: any` = ۰** در `src/`؛ ۲۸۲ تست پاس.
- **پین SDK و drift حل شده:** job `client-pinned` با Flutter `3.50.0` + بررسی انطباق با `.devcontainer/Dockerfile` + گیت `dart format` (M109) + کامپایل Android debug به‌عنوان شاهد Gradle.
- **DAST انجام شده:** `scripts/dast.py` با schemathesis → `evidence/m60/dast.json` = ۱۲۸ عملیات، ۱۰۲۴ کیس، **۰ یافته، ۰ پاسخ 2xx بدون احراز هویت**.
- **گیت‌های موجود سبز و ارزشمندند:** `interaction_map.py --check` (۳۱ سطح، ۱۶۳ مسیر، رانش صفر)، `docs_gate.py` (۱۸ سند، ۲۷۳+ لینک، ۱۵ بلوک Mermaid)، Gitleaks با راستی‌آزمایی checksum روی کل تاریخچه و `--redact`، `deploy_gate.py` (۹ بررسی — که باگ واقعی `MP_JWT_SECRET`→`MP_SECRET_KEY` را پیدا کرد)، Semgrep، bandit، pip-audit، apktool audit (۴۷۳ فایل در ۳ ABI).
- **کیفیت QA مرورگری خوب است:** ۱۱ صفحه با ۰ خطای کنسول/۰ 4xx-5xx/۰ استثنا/۰ سرریز افقی؛ **۱۰۱ دکمهٔ یکتا شناسایی و ۴۵ کلیک شد** با ۰ خطا.

---

## و) موانع محیطی (BLOCKED — بدون تو حل نمی‌شوند)

۱. **APK امضاشده:** secretهای `MP_ANDROID_*` و `MP_ANDROID_CERT_SHA256` تنظیم نشده‌اند (§۱۱).
۲. **چرخش کلید signing افشاشده** (چک‌لیست خط ۱۲) + بازنویسی تاریخچه — فقط با تأیید تو.
۳. **اجرای Flutter در sandbox:** `pub.dev` و `storage.googleapis.com` مسدود ⇒ golden/patrol/`flutter test` فقط در Codespace یا CI.
۴. **دستگاه واقعی، پرداخت بانکی، push/SMS، Valkey، PostgreSQL، Prometheus** در دسترس نیستند ⇒ دکمه‌های مالی/مخرب در مرورگر، همزمانی کوپن روی Postgres، و تست‌های زمان اجرا BLOCKED.
۵. **JADX/بازبینی باینری APK:** هیچ JDK در محیط نیست (`jdk4py` فقط JRE است) — `evidence/m60/STATUS.md` هم آن را «مسدود (دقیق)» ثبت کرده.

---

## ز) خلاصهٔ عددی (مبنای گیت ضد‌رگرسیون)

| سنجه | امروز (`main@662ff88`) | روند |
|---|---|---|
| فایل‌های ترک‌شده | ۱۱۴۷ | ↓ از ۱۶۷۸ ✅ |
| تست بک‌اند (فایل / پاس / پوشش) | ۱۴۴ / ۱۰۹۵ / ۹۴٫۲۸٪ (گیت ۷۰٪) | ✅ |
| تست استودیو | ۲۸۲ پاس، ۹ skip، ۴۶ فایل تست | ✅ |
| تست کلاینت | ۲۹ فایل تست برای ۴۴ فایل Dart در `lib` | ⚠️ |
| golden / integration / patrol | ۰ / ۰ / ۰ | ❌ |
| `Semantics` در `client/lib` | ۳ فایل | ❌ |
| `dynamic` / `as` / `// ignore` | ۱۹۷ / ۱۹۲ / ۰ | ❌ |
| l10n / ARB / intl | ۰ | ❌ |
| mutation / property | ۰ / ۰ | ❌ |
| گیت زنجیرهٔ تأمین / crash reporting / CSP | ۰ / ۰ / ۰ | ❌ |
| `openapi.json` commit‌شده / گیت oasdiff | ۰ / ۰ | ❌ |
| سناریو k6 / آشوب | ۲ / ۰ | ❌ |
| `print()` غیرتست / `except Exception` / TODO / skip | ۴۱ / ۲۲ / ۴۸ / ۶ | ❌ (سه‌تای آخر بدتر شده) |
| یافتهٔ سلامت RepoWise | ۶۷۰ (۲۵ critical، ۷۰ high) | ⚠️ |
| کد مرده RepoWise | ۳۵ (۲ high-confidence) | ⚠️ |
| رانش مستندات | ۲۵ مورد در ۱۴ سند | ⚠️ |
| آیتم باز `RELEASE-CHECKLIST.md` | ۲۱ (در برابر ۱۹ انجام) | ❌ |
| `mp.db` در مخزن | ۱ فایل ۸۶۴KB، ۵۲ جدول (همه خالی) | ❌ |
| حجم مخزن | ۸۳٫۹MB | ⚠️ |

**ترتیب پیشنهادی رفع:** A1 → A4 → A2 → A3 → B17/B18 → A5 → A6 → A7 → A8 → A9 → B1‑B6 → B7‑B12 → D1‑D8 (ارزان و فوری) → C1‑C19.
