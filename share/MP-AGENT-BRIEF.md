# بریف اجرای کامل ممیزی و ارتقای نهایی — MuscleParadise (MP)

**نسخه:** ۱.۰ · **تاریخ:** ۲۰۲۶‑۱۱‑۱۸
**مبنای ممیزی:** کلون فقط‌خواندنی از `yousefghorbanian98-create/MP` شاخه‌ی `arena/4f336f66-mp` در کامیت `e6fa0a9`
**مخزن هدف:** `MP` · **زبان سند و خروجی‌ها:** فارسی (مطابق `AGENTS.md` و `docs/` فعلی)

---

## ۰) چگونه این سند را بخوانی

این سند جای حرف‌زدن با مالک را می‌گیرد. **هیچ سؤالی نپرس؛ همه‌ی تصمیم‌ها در بخش ۳ گرفته شده‌اند.**
ترتیب اجرا: بخش ۱ (مأموریت) → ۲ (خواسته‌ها) → ۳ (قواعد) → ۴ (وضعیت موجود، تا چیزی را دوباره نسازی) → ۵ (بسته‌های کاری WP‑00 تا WP‑16، به‌ترتیب بخش ۶) → ۷ (خط قرمزها) → ۸ (گیت نهایی).
هر بسته‌ی کاری (WP) چهار بخش دارد: **چرا / شاهد / کار / معیار پذیرش**. معیار پذیرش یعنی «وقتی تمام است که …»؛ بدون برآورده‌شدن آن، WP را بسته اعلام نکن.

---

## ۱) مأموریت

پروژه به پایان توسعه نزدیک است. مأموریت تو **یک پاس ممیزی و سخت‌سازی نهایی در سطح کلاس جهانی** است:
هر خط کد بک‌اند، کلاینت و استودیو؛ همه‌ی سیم‌کشی‌ها، موتورها و ورک‌فلوها؛ خروجی هر تابع و پارامترها؛ همبستگی کلی و جزئی؛ انیمیشن‌ها، اینترکشن‌ها، سرچ‌بارها و تک‌تک دکمه‌ها؛ کد تکراری؛ ساده‌سازی توابع؛ حذف کد مرده؛ و تست و «اورلود» (بار، آشوب، جهش) هر چیزی که باید خروجی داشته باشد.

خروجی نهایی تو **فقط گزارش نیست**: کد اصلاح‌شده، تست اضافه‌شده، گیت CI نصب‌شده و سند به‌روزشده است. گزارش، محصول جانبی است.

---

## ۲) خواسته‌های صریح مالک (بدون تغییر، بدون حذف)

۱. تمام خط‌به‌خط کدهای بک‌اند و فرانت‌اند بررسی شود.
۲. تمام سیم‌کشی‌های برنامه (اتصال کلاینت/استودیو ↔ API ↔ DB ↔ سرویس‌های بیرونی) بررسی شود.
۳. تمام موتورها و ورک‌فلوها بررسی شود.
۴. تک‌تک چیزهایی که باید خروجی داشته باشند، مشخص و تست شود.
۵. توابع و پارامترها بررسی شود.
۶. همبستگی کلی و جزئی برنامه بررسی شود.
۷. انیمیشن‌ها و اینترکشن‌ها بررسی و تست شود.
۸. همه‌چیز، از جمله سرچ‌بارها و **تک‌تک دکمه‌ها**، بررسی شود.
۹. چک شود **کدی روی کد دیگری نیفتاده باشد** (منطق تکراری/موازی).
۱۰. **توابع ساده‌سازی شوند.**
۱۱. **کد مرده نداشته باشیم.**
۱۲. هر چیزی که برنامه را در **کلاس جهانی** نگه می‌دارد، یک بار **تست و اورلود** شود.

هر WP در بخش ۵ به یک یا چند مورد از این فهرست نگاشت شده است. در پایان، در گزارش نهایی یک جدول بگذار: مورد ۱ تا ۱۲ ← کدام WP ← چه شاهد اجرایی (تست/CI/عدد).

---

## ۳) قواعد کار — تصمیم‌های از پیش گرفته‌شده (سؤال نپرس)

**۳‑۱. منبع حقیقت.** اول `AGENTS.md` مخزن، بعد نزدیک‌ترین `AGENTS.md` scoped، بعد این سند، بعد `docs/README.md` و `docs/MuscleParadise/SESSION_HANDOFF.md` و TODO جاری. ادعای «کار می‌کند» فقط با **کد، تست یا CI** اثبات می‌شود؛ مستند و نقشه راهنما هستند، نه شاهد.

**۳‑۲. وقتی مردد بودی.** کم‌خطرترین گزینه را انتخاب کن، در گزارش همان WP زیر عنوان «تصمیم خودکار» یک‌خطی بنویس (چه کردی و چرا)، و **ادامه بده**. هرگز برای رفع ابهام کار را متوقف نکن. تنها استثنائوها در بخش ۷ (خط قرمزها) هستند.

**۳‑۳. وقتی چیزی را نمی‌دانی.** با شاهد بررسی کن (فایل، تست، لاگ CI). اگر اثبات نشد، در گزارش بنویس «نامعلوم — نیاز به شاهد اجرایی» و حدس نزن. هرگز وضعیت را بی‌صدا بازنویسی نکن.

**۳‑۴. اندازه‌ی تغییر.** هر WP = یک شاخه = یک PR. کامیت‌ها کوچک و با پیام معنادار (الگوی موجود: `M98: …`). هیچ کامیت چند‌هزار خطی نزن. اگر WP بزرگ شد، به WP-فرعی (مثلاً `WP-06a`) تقسیم کن.

**۳‑۵. CI هرگز نباید قرمز بماند و هرگز نباید شل شود.**
- پایین‌آوردن `--cov-fail-under=70`، حذف گیت، یا `|| true` گذاشتن روی گیت موجود = **ممنوع**.
- هر WP باید CI را سبز تحویل بدهد؛ اگر گیتی به‌دلیل تغییر درست قرمز شد، همان WP باید گیت را اصلاح کند (نه غیرفعال).
- job‌های فعلی که باید سبز بمانند: `secret-scan`, `docs`, `backend`, `studio`, `client-flutter`, `live-contract`, `e2e-api` (فایل `.github/workflows/ci.yml`)، به‌علاوه `apk.yml`, `container.yml`, `deploy.yml`.

**۳‑۶. سیاست ابزار جدید.** فقط ابزاری اضافه کن که همه‌ی این شرایط را داشته باشد: اوپن‌سورس + کاملاً رایگان + بدون نیاز به سرویس ابری پولی + قابل اجرا در CI یا محلی.
- **لایسنس مجاز برای وابستگیِ توزیع‌شده** (چیزی که در ایمیج/APK/استودیو ship می‌شود): MIT، Apache‑2.0، BSD، ISC، MPL‑2.0. **GPL/AGPL ممنوع** — چون `LICENSE` پروژه Proprietary است.
- **لایسنس مجاز برای ابزار dev/CI** (اجرا می‌شود ولی ship نمی‌شود): GPL/AGPL هم مجاز است. پس `repowise` (AGPL)، `hadolint` (GPL)، `k6` (AGPL) به‌عنوان **ابزار** مشکلی ندارند؛ به‌عنوان **کتابخانه‌ی داخل محصول** ممنوع‌اند.
- قبل از افزودن هر وابستگی، یک خط در گزارش WP بنویس: نام، لایسنس، چرا، و اینکه «وابستگی توزیعی» است یا «ابزار dev».

**۳‑۷. حریم خصوصی و داده.** محصول داده‌ی سلامتی و **زیست‌سنجشی (چهره)** پردازش می‌کند.
- هیچ داده‌ی واقعی عضو، چهره، رسید پرداخت یا شماره‌ی واقعی در مخزن، تست، فیکسچر، آرتیفکت CI یا گزارش نگذار. فقط synthetic (`faker` در بک‌اند؛ داده‌ی ساختگی در کلاینت/استودیو).
- هیچ مقدار محرمانه‌ای را در لاگ چاپ نکن. الگوی موجود Gitleaks (`--redact` + «value withheld») را در همه‌ی گیت‌های جدید حفظ کن.
- قبل از هر تغییر در مسیر چهره/پرداخت، `docs/MuscleParadise/security/biometric-policy.md`، `FACEID-PRIVACY-TEXT.md` و `DATA-RETENTION.md` را بخوان و ناسازگاری را ثبت کن.

**۳‑۸. مستندسازی هم‌زمان.** هر WP باید در پایان:
- `docs/MuscleParadise/SESSION_HANDOFF.md` را به‌روز کند (وضعیت، قدم بعدی).
- یک گزارش در `finn/reports/<slug>.md` بنویسد (الگوی موجود: `m97-migration-drift.md`, `m98-haptics-motion.md`).
- اگر معماری/قرارداد عوض شد، ADR یا `docs/MuscleParadise/architecture/c4.md` و `module-map.md` را به‌روز کند.
- `python3 scripts/docs_gate.py` باید سبز بماند.

**۳‑۹. زبان.** مستندات، کامنت‌های توضیحی و گزارش‌ها فارسی؛ شناسه‌های کد، نام فایل، پیام کامیت و کد انگلیسی (مطابق وضعیت فعلی مخزن).

**۳‑۱۰. هزینه.** هیچ سرویس پولی، کلید API پولی یا اشتراکی اضافه نکن. اگر مسیری فقط با سرویس پولی ممکن بود، آن مسیر را در گزارش «مسدود — نیاز به تصمیم انسانی» بنویس و از مسیر رایگان/محلی جایگزین استفاده کن.

**۳‑۱۱. ترتیب ایمنی.** هیچ‌گاه ریفکتور را قبل از سبز شدن گیت‌های جهش (WP‑05) روی همان مسیر شروع نکن. اول اثبات کن تست‌ها باگ می‌گیرند، بعد ساده‌سازی کن.

**۳‑۱۲. دامنه.** فقط داخل مخزن `MP` کار کن. هیچ تغییری در مخزن‌های دیگر، در حساب کاربری، در تنظیمات GitHub (branch protection، environments، secrets) یا در زیرساخت بیرونی ایجاد نکن؛ این‌ها در بخش ۷ فهرست شده‌اند.

---

## ۴) وضعیت موجود — این‌ها هست؛ دوباره نساز

ممیزی تأیید کرد که موارد زیر **پیاده‌سازی شده‌اند**. کار تو گسترش/تعمیق این‌هاست، نه بازسازی.

**CI و گیت‌ها (`.github/workflows/ci.yml`)**
- `secret-scan`: نصب Gitleaks با **راستی‌آزمایی checksum نسخه‌ی 8.30.1**، اسکن **کل تاریخچه** با `--redact`، خلاصه‌ی بدون مقدار در `GITHUB_STEP_SUMMARY` و annotation روی خط.
- `docs`: `python3 scripts/docs_gate.py` (پیوندهای محلی، دیاگرام‌ها، handoff).
- `backend`: `ruff check` + `ruff format --check` + `pytest --cov=. --cov-report=xml --cov-fail-under=70` + **bandit + pip-audit** + **Semgrep با قواعد اختصاصی `.semgrep/`** + جمع‌آوری و آپلود دیاگنوستیک در صورت شکست.
- `studio`: `npm test` (Vitest، **شامل گیت‌های WCAG و sync توکن‌ها**) + `npm run build` (`tsc -b && vite build`) + `npm audit` با گیت «بدون بحرانی».
- `client-flutter`: `flutter analyze` با گیت روی error/warning (نه info) + fallback پارس machine-format + annotation و sidecar JSON برای نام تست‌های شکست‌خورده (`tools/ci_test_failures.py`) + `flutter test`.
- `live-contract`: seed دیتابیس → اجرای واقعی API با uvicorn → تست **کلاینت TS استودیو در برابر API زنده** (`tests/liveContract.test.ts`) با توکن JWT واقعی.
- `e2e-api`: `pytest tests/integration` روی مسیرهای حیاتی (ثبت‌نام ← پرداخت ← چک‌این + تأیید برنامه).

**انتشار و عملیات**
- `apk.yml`: بیلد `flutter build apk --release --split-per-abi` با build-number/name + SHA256 + **ممیزی عمیق APK با apktool** + آرتیفکت دیاگنوستیک.
- `container.yml`: بیلد و push ایمیج backend و studio به GHCR با تگ full‑SHA.
- `deploy.yml`: `preflight` (الزام dispatch از شاخه‌ی محافظت‌شده) → `build-and-push` → `deploy` روی Dokploy با **readiness gate** → `rollback` با **تگ صریح + readiness gate**.
- `mp-app/infra/`: `Caddyfile`, `Dockerfile.backend`, `docker-compose.yml`, `ansible/{inventory.ini,playbook.yml}`, `monitoring/{prometheus.yml,alerts.yml}`, `scripts/{healthcheck.sh,rollback.sh,compress-media.sh}`.
- گیت بار: `mp-app/tests/load/k6-gate.js` با SLO `p(95)<2000ms` و `errors<0.05`.

**دیتابیس و تست**
- Alembic با چندین migration + تست‌های drift و بکاپ: `tests/integration/test_migrations.py`, `test_m47_migration_drift.py`, `test_m97_migrations_and_backup.py`, `test_backup_drill.py`, `tests/unit/test_backup.py`.
- سخت‌سازی SQLite در `mp-app/backend/db/base.py:118-121`: `journal_mode=WAL`, `synchronous=NORMAL`, `busy_timeout=15000`, `foreign_keys=ON`.
- RBAC: `tests/regression/test_rbac.py`, `tests/unit/test_rbac_policies.py`, `tests/integration/test_m67_studio_auth.py`.
- رمزینه‌نگاری زیست‌سنجشی: `security/crypto.py` شامل `FaceEmbeddingCipher`.
- موتور ارزیابی AI: `mp-app/backend/eval/` + `tests/evaluation/test_eval_harness.py`, `test_prescription_eval.py`, `test_scoring_eval.py`.
- ۱۱۸ فایل تست بک‌اند، ۲۸ فایل تست کلاینت، تست‌های استودیو شامل `a11y.test.tsx`, `apiCoverage.test.ts`, `authFlow.test.tsx`, `liveContract.test.ts`.
- آفلاین: `mp-app/client/test/offline_feedback_outbox_test.dart` + `docs/MuscleParadise/ANDROID-OFFLINE-PLAN.md` + `finn/reports/m86-offline-contract.md`, `m87-android-feedback-outbox.md`.

**مستندات و فرایند**
- `AGENTS.md` فارسی با پروتکل شروع نشست و اولویت منبع حقیقت؛ `docs/MuscleParadise/` با ۱۱۷ سند شامل `SESSION_HANDOFF.md`, `TODO-2026-11-16.md`, `MASTER_MAP.md`, `BUILD-QUEUE.md`, `RELEASE-CHECKLIST.md`, `OPS-RUNBOOK.md`, `TOOLING-RUNBOOK.md`, `DEPLOYMENT.md`, `PRD.md`, `CHANGELOG.md`, `architecture/c4.md`, `architecture/module-map.md`, `adr/001-modular-monolith.md`, `adr/002-sqlite-with-postgres-migration.md`.
- امنیت و حریم خصوصی مستند: `SECURITY-AUDIT-2026-11-15.md`, `SECURITY-REVIEW-2026-11-15.md`, `security/owasp-checklist.md`, `security/biometric-policy.md`, `DATA-RETENTION.md`, `FACEID-PRIVACY-TEXT.md`.
- ممیزی‌های قبلی: `AUDIT-2026-11-15.md`, `ACCESS-AUDIT-2026-11-15.md`, `OUTPUT-AUDIT-2026-11-14.md`, `COMPETITIVE-UX-AUDIT-2026-11-16.md`, `LOAD-TEST-2026-11-15.md`.
- `NOTICE-THIRD-PARTY.md` و حلقه‌ی `F.I.N.N` با گزارش‌های `finn/reports/`.
- سیستم ایجنتی `.claude/` با ۶۳۰ skill، ۱۲۲ rule، ۹۸ command، ۷۱ agent، ۹ hook.

**موتورها (هدف اصلی تست عمیق)** — `mp-app/backend/engine/` شامل ۱۹ ماژول:
`adaptive_nutrition`, `autoreg`, `axis_map`, `axis_prescription`, `axis_rules`, `catalog_sync`, `churn_risk`, `feedback_apply`, `gender_plans`, `nutrition`, `readiness`, `reminders`, `safety`, `scoring`, `segmental`, `set_feedback`, `sync_lww`, `volume`, `workout`.

---

## ۵) بسته‌های کاری

> اولویت: **P0** = قبل از هر انتشار؛ **P1** = عمق تست و نوع؛ **P2** = کلاس جهانی.
> شماره‌ی WP را در پیام کامیت و نام شاخه بیاور (مثلاً `wp02: trivy + sbom + hadolint + cosign gates`).

### WP‑00 · آماده‌سازی و صف اجرا — P0
**چرا:** بدون صف صریح، ترتیب و پوشش خواسته‌های ۱۲گانه گم می‌شود.
**شاهد:** `AGENTS.md` می‌گوید وضعیت را از TODO جاری بگیر؛ `docs/MuscleParadise/TODO-2026-11-16.md` و `LOOP-PLAN-M100-M106.md` وجود دارند.
**کار:**
1. `git status --short --branch` و آخرین کامیت را ثبت کن.
2. `SESSION_HANDOFF.md` و TODO جاری و `LOOP-PLAN-M100-M106.md` را بخوان؛ این سند را با صف موجود آشتی بده (اگر WP با یک M تداخل دارد، WP را زیر همان M ثبت کن و در گزارش بنویس).
3. یک فایل صف جدید بساز: `docs/MuscleParadise/AUDIT-FINAL-QUEUE-2026-11-18.md` با جدول WP‑01…WP‑16، اولویت، وابستگی، وضعیت.
4. `python3 scripts/docs_gate.py` را اجرا و سبز کن.
**معیار پذیرش:** فایل صف commit شده؛ `docs_gate.py` سبز؛ `SESSION_HANDOFF.md` به این سند و صف ارجاع می‌دهد.

---

### WP‑01 · یکپارچگی امضا و بیلد Android — P0
**چرا:** یک بیلد «release» می‌تواند **بی‌صدا با کلید debug** امضا شود و هیچ shrinking/obfuscation یا AAB وجود ندارد.
**شاهد:**
- `mp-app/client/android/app/build.gradle.kts:52-55` → `signingConfig = if (…storeFile != null) release else debug`.
- در `buildTypes.release` هیچ `isMinifyEnabled` / `isShrinkResources` / `proguardFiles` نیست.
- در هیچ workflow ای `.aab`/`appbundle` ساخته نمی‌شود (فقط `flutter build apk`).
- `defaultConfig` هنوز کامنت قالب Flutter («TODO: Specify your own unique Application ID») دارد.
- `docs/MuscleParadise/RELEASE-CHECKLIST.md:12` → «کلید signing افشاشده rotate/revoke … **حذف فایل از HEAD کافی نیست**» (باز).
**کار:**
1. fallback به debug را **به شکست صریح** تبدیل کن: اگر `keystore.properties` یا فیلدهایش نبود، بیلد release با پیام خوانا **fail** شود. هیچ مسیر بی‌صدایی باقی نماند.
2. `release { isMinifyEnabled = true; isShrinkResources = true; proguardFiles(…) }` + قواعد ProGuard/R8 سازگار با Flutter و هر پلاگین استفاده‌شده؛ سپس APK را با `apkanalyzer`/apktool بررسی کن که چیزی لازم حذف نشده.
3. ساخت **`.aab`** را به `apk.yml` اضافه کن (`flutter build appbundle --release`) با SHA256 و آرتیفکت، در کنار APK موجود.
4. گیت اندازه‌ی بیلد: آستانه‌ی صریح برای حجم APK/AAB (عدد پایه را از بیلد فعلی بگیر و ۵٪ سقف بگذار) تا رشد ناخواسته‌ی باندل قرمز شود.
5. کامنت قالب TODO در `defaultConfig` را پاک کن.
6. **چرخش کلید و بازنویسی تاریخچه را انجام نده** — فقط یک سند اجرایی دقیق آماده کن (بخش ۷).
**معیار پذیرش:** بیلد release بدون keystore معتبر **شکست می‌خورد** (نه امضای debug)؛ `isMinifyEnabled`/`isShrinkResources` فعال و APK ممیزی‌شده؛ `.aab` در CI ساخته و SHA256 ثبت می‌شود؛ گیت اندازه سبز؛ `apk.yml` کامل سبز.
**ابزار:** `bundletool`، `apksigner verify`، `apkanalyzer` (همه رایگان/Android SDK)، `git-filter-repo` (MIT) فقط برای سند.

---

### WP‑02 · زنجیره‌ی تأمین آرتیفکت (ایمیج، SBOM، امضا) — P0
**چرا:** گیت‌های موجود **سطح کد** را پوشش داده‌اند (Gitleaks/bandit/pip-audit/npm audit/Semgrep)، ولی **آرتیفکت** پوشش ندارد؛ در حالی که ایمیج‌ها به GHCR push و روی Dokploy deploy می‌شوند.
**شاهد:** grep روی کل `.github/workflows/` برای `sbom|trivy|grype|hadolint|cosign|syft|dependency-review|codeql` → **صفر نتیجه**. `container.yml` بیلد و push می‌کند؛ `deploy.yml` همان تگ SHA را deploy می‌کند.
**کار:**
1. در `container.yml` (یا یک job جدید `artifact-scan`) اضافه کن:
   - **hadolint** روی `mp-app/backend/Dockerfile` و `mp-app/infra/Dockerfile.backend`.
   - **Trivy** یا **Grype** روی هر ایمیج ساخته‌شده، با گیت صریح روی `CRITICAL`/`HIGH` (بدون `|| true`) و آپلود گزارش به‌عنوان آرتیفکت.
   - **SBOM** CycloneDX برای هر ایمیج + آرتیفکت نسخه‌دار (مانند الگوی `chat2db-community-sbom` در پروژه‌های مشابه: `anchore/sbom-action`).
   - **cosign** برای امضا و attestation (SLSA provenance) با `GITHUB_TOKEN` موجود؛ `deploy.yml` باید **فقط ایمیج امضاشده/معتبر** را deploy کند (verify قبل از Dokploy).
2. یک job `dependency-review` روی `pull_request` اضافه کن.
3. اسکن SBOM با Grype را به‌عنوان job زمان‌بند (هفتگی) اضافه کن تا CVEهای جدید بعد از انتشار هم دیده شوند.
**معیار پذیرش:** هر PR که ایمیج می‌سازد، گزارش lint + CVE + SBOM + امضا دارد؛ یک CVE بحرانی بیلد را قرمز می‌کند؛ `deploy.yml` بدون attestation معتبر، deploy نمی‌کند.
**ابزار:** `aquasecurity/trivy` (Apache‑2.0، ⭐39.5k) · `anchore/grype` (Apache‑2.0، ⭐13.3k) · `anchore/sbom-action` (Apache‑2.0) · `hadolint/hadolint` (GPL‑3.0 — ابزار dev، مجاز) · `sigstore/cosign` (Apache‑2.0، ⭐6.4k) · `actions/dependency-review-action`.

---

### WP‑03 · قطعیت و کامل‌بودن CI — P0
**چرا:** دو حفره‌ی تکرارپذیری: نصب غیرقطعی npm، و نبودِ گیت lint برای استودیو.
**شاهد:**
- `ci.yml` job `studio`: `run: npm ci || npm install` (و همین الگو در job `live-contract`) در حالی که `mp-app/studio/package-lock.json` ترک‌شده وجود دارد → اگر lockfile ناسازگار باشد CI **بی‌صدا نسخه‌ی دیگری نصب می‌کند و سبز می‌شود**.
- job `studio` مراحل `Install → npm test → npm run build → npm audit` را دارد ولی **`npm run lint` (ESLint) را اجرا نمی‌کند**، در حالی که اسکریپت `lint` در `package.json` تعریف شده است.
- `package.json` → `"lint": "eslint src --ext .ts,.tsx"` (سینتکس ESLint 8؛ با ESLint 9/flat config سازگار نیست).
**کار:**
1. هر دو `npm ci || npm install` را به `npm ci` خالص تغییر بده؛ اگر lockfile ناسازگار بود، بیلد باید **قرمز** شود.
2. `npm run lint` را به job `studio` اضافه کن (قبل از test). اگر اسکریپت lint با نسخه‌ی نصب‌شده‌ی ESLint کار نمی‌کند، همان WP باید آن را درست کند (مهاجرت به flat config یا پین کردن نسخه‌ی سازگار) — نه اینکه گیت را حذف کند.
3. نسخه‌ی Node را در همه‌ی jobها یکسان و صریح پین کن (الان `"22"` است؛ `22.x.y` مشخص یا `node-version-file` از یک فایل `.nvmrc`/`package.json#engines`).
4. یک فایل پین ابزار اضافه کن: `.tool-versions` یا `engines` در `package.json` + `requires-python` (که هست: py311) + نسخه‌ی Flutter (از `flutter-action`؛ صریح با `flutter-version`/`cache`).
5. `concurrency` با `cancel-in-progress` برای push/PR اضافه کن (اگر نیست) تا اجراهای موازی روی یک شاخه همدیگر را مخدوش نکنند.
**معیار پذیرش:** `npm ci` بدون fallback؛ lint استودیو به‌عنوان گیت در CI؛ نسخه‌های Node/Python/Flutter صریح و یکسان؛ CI سبز.

---

### WP‑04 · گزارش خطا و crash در زمان اجرا — P0
**چرا:** محصول روی کیوسک و موبایل در باشگاه اجرا می‌شود؛ امروز **هیچ سیگنال خطای زمان اجرایی** جز Prometheus وجود ندارد.
**شاهد:** grep برای `sentry|glitchtip|rollbar|bugsnag` در کل `mp-app` → **صفر**. `mp-app/backend/app/logging.py` و `tests/integration/test_monitoring.py` و `mp-app/infra/monitoring/{prometheus,alerts}.yml` وجود دارند (پس لایه‌ی متریک هست، لایه‌ی خطا نیست).
**کار:**
1. یک نمونه‌ی self‑host **GlitchTip** (سازگار با SDKهای Sentry، MIT) به `mp-app/infra/docker-compose.yml` و ansible اضافه کن (کنار Prometheus موجود).
2. بک‌اند: یکپارچه‌سازی با SDK (ASGI middleware) + `before_send` برای **redaction** (شماره موبایل، نام، `face embedding`، هر فیلد حساس) + `environment` و `release=git SHA` + اتصال `request_id` موجود در لاگ.
3. کلاینت Flutter: افزودن crash reporting با همان DSN و **رضایت/سیاست حریم خصوصی** مطابق `FACEID-PRIVACY-TEXT.md` و `biometric-policy.md`؛ هیچ داده‌ی زیست‌سنجشی در payload نباشد.
4. استودیو: `window.onerror` + `unhandledrejection` + خطای Electron main/process.
5. **تست redaction** بنویس: payload ارسالی باید شامل هیچ شماره/نام/embedding واقعی نباشد (تست واحد روی تابع redact).
6. `alerts.yml` را با قاعده‌ی «رشد نرخ خطای جدید» گسترش بده و در `OPS-RUNBOOK.md` یک بخش «تریage خطای زمان اجرا» اضافه کن.
**معیار پذیرش:** یک خطای عمدی در staging به GlitchTip می‌رسد با SHA و محیط درست؛ تست redaction سبز؛ هیچ PII در نمونه‌ی payload (شاهد: خروجی تست)؛ runbook به‌روز.
**ابزار:** `burke-software/GlitchTip` (MIT) · `sentry_python`/`sentry_flutter` (SDKها) · OpenTelemetry اگر tracing خواستی (Apache‑2.0).

---

### WP‑05 · تست جهش (mutation) روی موتورهای حیاتی — P1
**چرا:** گیت `--cov-fail-under=70` فقط **اجرای خطوط** را اثبات می‌کند، نه **گیرنده‌ی باگ بودن** تست‌ها. خواسته‌ی ۱۲ («تست و اورلود شود») بدون این، ناقص است. و طبق قاعده‌ی ۳‑۱۱، تا این گیت سبز نشده ریفکتور (WP‑16) شروع نمی‌شود.
**شاهد:** `[project.optional-dependencies] dev` شامل pytest/pytest-cov/pytest-asyncio/ruff/bandit/pip-audit/faker/pyyaml/Pillow است — **هیچ ابزار mutation نیست**. هیچ `stryker` در استودیو نیست.
**کار:**
1. بک‌اند: **mutmut** یا **cosmic-ray** را به dev deps اضافه کن و ابتدا روی دو مسیر بحرانی اجرا کن: `mp-app/backend/engine/` (به‌ویژه `safety.py`, `scoring.py`, `volume.py`, `axis_prescription.py`, `autoreg.py`, `readiness.py`) و `mp-app/backend/security/`.
2. یک اسکریپت قابل تکرار بساز (`mp-app/backend/scripts/mutation_gate.py` یا Makefile) که **mutation score** را برای آن مسیرها گزارش کند و یک **آستانه‌ی پایه** ثبت کند (عدد واقعی امروز را اندازه بگیر، سپس آستانه را روی همان عدد یا ۲٪ بالاتر بگذار تا فقط رشد ممکن باشد).
3. استودیو: **stryker-js** را با محدود کردن مسیر (`src/**` حیاتی، مثلاً محاسبه‌ها/فرم‌ها/auth) نصب کن؛ آستانه‌ی پایه ثبت شود.
4. جهش‌های بازمانده (survived mutants) را فهرست کن و برای هرکدام یا تست بنویس یا در گزارش دلیل بیاور («این جهش معنایی ندارد»).
5. یک job زمان‌بند هفتگی در CI (نه روی هر PR — کند است) اضافه کن و نتیجه را در `finn/reports/` بنویس.
**معیار پذیرش:** mutation score اندازه‌گیری و ثبت شده برای `engine/` و `security/` و مسیرهای حیاتی استودیو؛ آستانه در CI/اسکریپت قفل شده؛ فهرست mutantهای بازمانده با تعیین تکلیف؛ گزارش در `finn/reports/`.
**ابزار:** `boxed/mutmut` (BSD‑3، ⭐1.5k) یا `sixty-north/cosmic-ray` (MIT) · `stryker-mutator/stryker-js` (Apache‑2.0، ⭐3.4k). برای Dart ابزار بالغِ mutation نیست → در WP‑07 با **fault injection** دستی روی مسیرهای حیاتی جایگزین کن و در گزارش توضیح بده.

---

### WP‑06 · تست property‑based روی ۱۹ موتور — P1
**چرا:** دامنه‌ی محصول عددی/فیزیولوژیک است؛ باگ‌های واقعی در **نقض نامتغیرها** و حالات لبه‌اند، نه در مثال‌های دستی. خواسته‌های ۴ و ۵ (خروجی توابع و پارامترها) دقیقاً اینجا بسته می‌شوند.
**شاهد:** در dev deps فقط `faker` هست؛ **`hypothesis` نیست**. موتورهای `engine/` (۱۹ فایل) و `engine/sync_lww.py` (حل تعارض آفلاین) و `engine/safety.py` (ایمنی سلامتی) بدون تست نامتغیرند.
**کار:**
1. `hypothesis` را به dev deps اضافه کن و یک دایرکتوری `mp-app/backend/tests/property/` بساز.
2. برای **هر ۱۹ موتور** حداقل یک property بنویس. فهرست نامتغیرهای پیشنهادی (اگر با کد واقعی ناسازگار بود، نامتغیر درست را از کد استخراج کن و در گزارش بنویس):
   - `volume.py`: حجم = Σ(ست × تکرار × وزنه)؛ همواره ≥ ۰؛ با افزایش ست/تکرار/وزنه **یکنوا نزولی نیست** (یکنوا صعودی است).
   - `scoring.py`: امتیاز کران‌دار است؛ ورودی یکسان → خروجی یکسان (قطعی بودن)؛ ترتیب‌ناپذیری نسبت به فیلدهای بی‌ربط.
   - `safety.py`: هیچ خروجی‌ای پرچم ایمنی را **پایین نمی‌آورد**؛ اگر ورودی در فهرست ممنوعه است، خروجی حتماً رد/محدود است (این مهم‌ترین تست پروژه است).
   - `autoreg.py`/`readiness.py`/`set_feedback.py`/`feedback_apply.py`: تنظیم خودکار هرگز از سقف/کف مطلق خارج نمی‌شود؛ دو بار اعمال‌کردن فیدبک یکسان (idempotency) نتیجه را خراب نمی‌کند.
   - `axis_prescription.py`/`axis_rules.py`/`axis_map.py`/`segmental.py`/`gender_plans.py`: پوشش کامل نگاشت (هر ورودی معتبر یک خروجی معتبر دارد)؛ هیچ `KeyError`/`None` غیرمنتظره.
   - `adaptive_nutrition.py`/`nutrition.py`: کالری/ماکرو منفی یا NaN یا بی‌نهایت نمی‌شود؛ جمع ماکروها با کالری کل سازگار است (± تلورانس صریح).
   - `churn_risk.py`: خروجی در `[0,1]`؛ یکنواختی نسبت به سیگنال‌های قطعی.
   - `sync_lww.py`: **همگرایی** — اعمال همان مجموعه‌ی رویداد با هر ترتیبی به وضعیت یکسان می‌رسد (commutativity/idempotency)؛ هیچ نوشتن گم‌شده‌ای.
   - `catalog_sync.py`: همگام‌سازی دوطرفه داده را گم نمی‌کند؛ اجرای مجدد بدون اثر جانبی.
   - `reminders.py`: زمان‌ها همیشه در آینده/بازه‌ی معتبر؛ منطقه‌ی زمانی و DST نتیجه را نمی‌شکند.
   - `workout.py`: وضعیت‌های نامعتبر (ست منفی، تکرار صفر، وزنه‌ی NaN) رد می‌شوند.
3. برای همه‌ی propertyها `deadline=None` و `derandomize` (یا seed ثبت‌شده) تنظیم کن تا CI **قطعی** بماند و flaky نشود.
4. استودیو: `fast-check` را اضافه کن و برای محاسبه‌های عددی/فرم‌ها/منطق auth property بنویس.
5. یک property هم برای **سریال‌سازی API** بنویس: هر پاسخ مدل، با schema تعریف‌شده سازگار است و round‑trip (serialize→deserialize) داده را عوض نمی‌کند.
**معیار پذیرش:** حداقل یک property برای هر ۱۹ موتور + مسیرهای حیاتی استودیو؛ همه سبز و قطعی (۳ اجرای پیاپی بدون flake)؛ هر property یک کامنت فارسی دارد که «چرا این نامتغیر» را می‌گوید.
**ابزار:** `HypothesisWorks/hypothesis` (MPL‑2.0، ⭐9.2k) · `dubzzz/fast-check` (MIT، ⭐5.3k).

---

### WP‑07 · رگرسیون بصری و تست روی دستگاه برای کلاینت — P1
**چرا:** خواسته‌های ۷ و ۸ (انیمیشن، اینترکشن، تک‌تک دکمه‌ها، سرچ‌بار) در کلاینت **بدون شاهد اجرایی** است.
**شاهد:** `matchesGoldenFile` در **۰ فایل**؛ دایرکتوری `integration_test` وجود ندارد؛ ۲۸ فایل widget test موجود است.
**کار:**
1. **Golden tests:** برای هر صفحه و هر کامپوننت پرکاربرد، با `matchesGoldenFile` داخلی `flutter_test` (بدون وابستگی جدید) وضعیت‌ها را پوشش بده: `default / loading / empty / error / disabled / pressed / focus / RTL / فونت ۲۰۰٪ / dark`. فایل‌های طلایی را در `mp-app/client/test/goldens/` commit کن و در CI یک گیت بگذار که تفاوت golden → قرمز (با `--update-goldens` فقط به‌صورت صریح و با کامیت جدا).
2. **سرشماری UI:** یک فایل `docs/MuscleParadise/UI-INVENTORY.md` بساز با یک ردیف برای **هر دکمه، هر فیلد، هر سرچ‌بار، هر انیمیشن** در کلاینت و استودیو؛ ستون‌ها: شناسه، مسیر فایل، stateها، تست widget، golden، تست on-device، a11y، i18n، وضعیت. این فایل همان «تک تک دکمه‌ها» را قابل حسابرسی می‌کند و ستون «وضعیت» نباید خالی بماند.
3. **تست روی دستگاه:** `integration_test` را با **patrol** راه بینداز و حداقل این جریان‌ها را end‑to‑end پوشش بده: ورود با OTP → چک‌این (کیوسک/چهره) → دیدن برنامه‌ی تمرین → ثبت ست → فیدبک/آفلاین→سینک. تعامل با dialogهای permission واقعی (دوربین/بیومتریک) فقط با patrol ممکن است.
4. **انیمیشن‌ها:** هر انیمیشن را با golden در چند فریم (یا `flutter test` با کنترل `WidgetTester.pump(duration)`) قفل کن؛ رفتار haptics را مطابق `finn/reports/m98-haptics-motion.md` حفظ کن.
5. **fault injection (جایگزین mutation در Dart):** در تست‌ها یک‌بار API را timeout/500، یک‌بار DB محلی را پر، و یک‌بار شبکه را قطع کن و رفتار offlinе outbox را اثبات کن (`offline_feedback_outbox_test.dart` را گسترش بده).
**معیار پذیرش:** golden برای همه‌ی صفحات اصلی + stateهای فهرست‌شده؛ `UI-INVENTORY.md` کامل بدون ستون خالی؛ حداقل یک تست patrol که روی امولاتور در CI اجرا و سبز می‌شود؛ گیت golden در `ci.yml`.
**ابزار:** `flutter_test` (داخلی) · `leancodepl/patrol` (Apache‑2.0، ⭐1.5k، فعال).

---

### WP‑08 · سخت‌گیری نوع در Dart و TypeScript — P1
**چرا:** «همبستگی جزئی» (خواسته‌ی ۶) باید در **کامپایل** کشف شود نه زمان اجرا.
**شاهد:**
- `mp-app/client/analysis_options.yaml` فقط `include: package:flutter_lints/flutter.yaml` + دو قاعده (`prefer_const_constructors`, `prefer_final_locals`)؛ `strict-casts`/`strict-raw-types`/`strict-inference` **خاموش**؛ CI با `--no-fatal-infos`.
- در `mp-app/client/lib/`: **۱۹۱ کست `as`**، **۱۹۷ `dynamic`**، ۴ `!.`.
- استودیو: `npm run lint` در CI اجرا نمی‌شود (WP‑03).
**کار:**
1. در `analysis_options.yaml` فعال کن: `language: { strict-casts: true, strict-raw-types: true, strict-inference: true }` + مجموعه‌ی قواعد `flutter_lints` و قواعد ایمنی (`avoid_dynamic_calls`, `always_declare_return_types`, `unnecessary_await_in_return`, `use_build_context_synchronously`, `cancel_subscriptions`, `close_sinks`).
2. خطاهای ناشی را **واقعاً رفع کن** (نه `// ignore:`). اگر حجم زیاد است، به‌ترتیب پوشه پیش برو و در گزارش درصد پیشرفت بنویس؛ در پایان هیچ `dynamic`/کست بدون دلیل نماند.
3. یک **گیت ضد‌رگرسیون** بگذار: اسکریپتی در CI که تعداد `dynamic` و `as` و `// ignore:` را می‌شمارد و اگر از عدد پایه **بیشتر** شد، قرمز می‌کند (عدد پایه = وضعیت پس از پاکسازی؛ در یک فایل `.ci-baseline.json` commit شود).
4. استودیو: `tsconfig.json` را بررسی کن و `strict`، `noUncheckedIndexedAccess`، `noImplicitOverride`، `exactOptionalPropertyTypes` را فعال کن (هرکدام که بدون شکستن بیلد ممکن است؛ بقیه را با گیت ضد‌رگرسیون برای `any` کنترل کن). تعداد `any` را بشمار، کاهش بده و عدد پایه را قفل کن.
5. `dart fix --apply` و `eslint --fix` را اجرا کن (کامیت جدا: «fixes مکانیکی»).
**معیار پذیرش:** strict modes فعال؛ صفر `dynamic`/`as` بدون کامنت دلیل؛ گیت ضد‌رگرسیون در CI؛ `flutter analyze` و `tsc -b` و `npm run lint` سبز.

---

### WP‑09 · دسترس‌پذیری کلاینت — P1
**چرا:** استودیو گیت WCAG دارد ولی کلاینت ندارد؛ عضو با TalkBack/VoiceOver عملاً نمی‌تواند کار کند.
**شاهد:** فقط **۳ فایل** در `mp-app/client/lib/` از `Semantics` استفاده می‌کنند؛ **۴ فایل** به `textScaler`/`Directionality`/`rtl` اشاره دارند؛ هیچ تست a11y در `mp-app/client/test/` نیست. در مقابل، `mp-app/studio/tests/a11y.test.tsx` و گیت WCAG در Vitest وجود دارد.
**کار:**
1. به همه‌ی کنترل‌های تعاملی `Semantics`/`semanticLabel` بده (طبق `UI-INVENTORY.md` از WP‑07 — همان فهرست، چک‌لیست a11y است).
2. تست خودکار با guidelineهای داخلی `flutter_test` بنویس: `androidTapTargets`, `iOSTapTargets`, `labeledTapTargets`, `textContrastGuideline` و اجرای آن روی **همه‌ی صفحات**.
3. تست scale فونت: همه‌ی صفحات با `textScaler: 2.0` بدون سرریز/بریدگی رندر شوند (golden در WP‑07 این را قفل می‌کند).
4. RTL را صریح تست کن (چیدمان، آیکون‌های جهت‌دار، انیمیشن‌های ورود/خروج).
5. یک پاس دستی با TalkBack انجام بده و نتیجه را در `docs/MuscleParadise/ACCESS-AUDIT-…` (الگوی موجود: `ACCESS-AUDIT-2026-11-15.md`) به‌عنوان نسخه‌ی جدید ثبت کن.
6. استودیو: گیت WCAG موجود را به همه‌ی صفحات/مودال‌ها گسترش بده و `axe-core` را در تست Playwright (WP‑14) هم اجرا کن.
**معیار پذیرش:** تست‌های guideline روی همه‌ی صفحات سبز؛ همه‌ی ردیف‌های `UI-INVENTORY.md` ستون a11y پر دارند؛ سند access-audit جدید با تاریخ امروز.
**ابزار:** `flutter_test` (داخلی) · `dequelabs/axe-core` (MPL‑2.0، ⭐7.8k) · `pa11y/pa11y` (LGPL‑3.0 — ابزار dev) · `GoogleChrome/lighthouse-ci` (Apache‑2.0، ⭐7.2k).

---

### WP‑10 · قرارداد API: نسخه‌بندی، دیف، و گسترش به کلاینت — P1
**چرا:** خواسته‌ی ۲ (سیم‌کشی‌ها). `live-contract` عالی است ولی **فقط استودیو** را پوشش می‌دهد و **هیچ گیت تغییر شکننده** وجود ندارد.
**شاهد:** هیچ فایل OpenAPI ترک‌شده‌ای در مخزن نیست (grep `openapi|swagger` → صفر)؛ `live-contract` فقط `mp-app/studio/tests/liveContract.test.ts` را اجرا می‌کند؛ کلاینت Flutter پوشش قرارداد زنده ندارد.
**کار:**
1. spec OpenAPI را از FastAPI **به‌صورت فایل commit‌شده** استخراج کن (`openapi.json` در مسیر مشخص، تولید با اسکریپت قابل تکرار) و یک گیت CI بگذار که «spec commit‌شده == spec تولیدشده از کد» باشد (جلوگیری از drift).
2. **oasdiff** را به‌عنوان گیت PR اضافه کن: هر تغییر **breaking** بدون برچسب/نسخه‌ی جدید → قرمز. خروجی را در خلاصه‌ی step بگذار.
3. `live-contract` را به **کلاینت Flutter** گسترش بده: یک لایه‌ی کلاینت API (یا یک تست Dart) که در برابر API زنده همان seed اجرا می‌شود و contract را اثبات می‌کند.
4. سیاست نسخه‌بندی و **حداقل نسخه‌ی کلاینت پشتیبانی‌شده** را تعریف کن و یک فیلد/هدر نسخه در API اضافه کن + تست اینکه کلاینت قدیمی پاسخ سازگار می‌گیرد.
5. تست idempotency برای POSTهای حساس (پرداخت، چک‌این، ثبت ست) با کلید idempotency.
**معیار پذیرش:** `openapi.json` commit‌شده + گیت drift + گیت oasdiff؛ یک تست قرارداد زنده برای کلاینت Dart؛ تست idempotency برای سه مسیر حساس؛ سند سیاست نسخه در `docs/`.
**ابزار:** `oasdiff/oasdiff` (Apache‑2.0، ⭐1.5k) + `oasdiff/oasdiff-action` · `schemathesis/schemathesis` (MIT، ⭐3.8k) برای فازی‌کردن endpointها از روی همان spec · `Orange-OpenSource/hurl` (Apache‑2.0، ⭐19.3k) برای سناریوهای HTTP خوانا · `stoplightio/prism` (Apache‑2.0) برای mock/validate.

---

### WP‑11 · i18n/l10n — P2
**چرا:** هیچ زیرساخت ترجمه‌ای وجود ندارد؛ رشته‌ها hardcode‌اند. این هم بدهی فنی است هم منبع باگ سرریز متن.
**شاهد:** grep برای `\.arb$|l10n|intl|translations` در `git ls-files` → **صفر**. `RELEASE-CHECKLIST.md:45` می‌گوید «RTL/فارسی + جزئیات میکرو» انجام شده، یعنی RTL هست ولی l10n ساخت‌یافته نیست.
**کار:**
1. کلاینت: `flutter_localizations` + `flutter gen-l10n` با فایل‌های `lib/l10n/app_fa.arb` و `app_en.arb`؛ همه‌ی رشته‌های hardcode را استخراج کن (با اسکریپت و سپس بررسی دستی)؛ `pubspec.yaml` → `generate: true`.
2. استودیو: `i18next` + `react-i18next` با **ICU** برای جمع‌بندی و قالب عدد/تاریخ/ارز (`Intl`)؛ کلیدها در `locales/fa.json` و `en.json`.
3. قالب‌های locale-aware: تاریخ شمسی/میلادی، عدد فارسی، ارز (ریال/تومان) — یک ماژول مشترک و **تست property** برای آن (مرتبط با WP‑06).
4. **pseudo-localization:** یک اسکریپت/تست که رشته‌ها را با نسخه‌ی کشیده (مثلاً ۳۰٪ بلندتر + کاراکترهای تشخیصی) جایگزین کند و goldenها را بگیرد → رشته‌های hardcode و سرریز متن را لو می‌دهد.
5. گیت CI: هیچ رشته‌ی کاربر‌نمای hardcode جدید (قاعده‌ی lint/semgrep) و هیچ کلید ترجمه‌ی گم‌شده (`fa` بدون `en` یا برعکس) پذیرفته نشود.
**معیار پذیرش:** همه‌ی رشته‌های کاربر‌نما از منبع l10n می‌آیند؛ تست کلیدهای گم‌شده سبز؛ golden با pseudo-locale تولید و بازبینی شده؛ سند کوتاه در `docs/`.

---

### WP‑12 · گیت لایسنس و دارایی‌های ثالث — P2
**چرا:** `LICENSE` پروژه **Proprietary** است؛ `NOTICE-THIRD-PARTY.md` دستی است و گیت خودکار ندارد. دارایی‌های ثالث commercial‑sensitive در مخزن‌اند.
**شاهد:** `pip-audit`/`npm audit` فقط آسیب‌پذیری می‌بینند، نه لایسنس. `mp-app/backend/data/external/free_exercise_db/exercises.json` (۹۸۴KB) + **۳۴ jpg و ۱۷ gif** در `mp-app/backend/static/exercises/` + فونت‌ها/تصاویر برند در `assets/` و `docs/ui-previews/`.
**کار:**
1. یک job `license-gate` اضافه کن:
   - بک‌اند: `pip-licenses` (خروجی JSON) + فهرست ممنوعه (`GPL*`, `AGPL*`, `SSPL*`, `CPAL*`) → در صورت وجود در **وابستگی توزیعی**، قرمز.
   - استودیو: `license-checker-rseidelsohn --production --summary` + همان فهرست ممنوعه (الگوی موجود `license-checker` در پروژه‌های مشابه را با گیت **شکننده** جایگزین کن، نه `--summary` تنها).
   - کلاینت: `flutter pub deps` → استخراج لایسنس پکیج‌ها و همان گیت.
2. **ORT** یا **ScanCode** را به‌صورت job زمان‌بند اجرا کن تا لایسنس/کپی‌رایت **دارایی‌ها** (تصاویر، GIF، فونت، دیتاست) هم اسکن شود؛ نتیجه در آرتیفکت.
3. برای هر دارایی ثالث یک ردیف در `NOTICE-THIRD-PARTY.md` اضافه/تکمیل کن: نام، منبع، لایسنس، **آیا استفاده‌ی تجاری مجاز است**، آیا attribution لازم است، و اینکه attribution کجا نمایش داده می‌شود.
4. اگر دارایی‌ای لایسنس نامشخص یا غیرتجاری داشت: در گزارش علامت بزن «مسدود — نیاز به تصمیم انسانی» و یک جایگزین آزاد پیشنهاد بده (ولی خودسرانه حذف نکن).
5. بررسی کن هیچ پکیج GPL/AGPL **داخل محصول** link نشده باشد (ابزارهای AGPL در CI/dev مجازند — قاعده‌ی ۳‑۶).
**معیار پذیرش:** job لایسنس با گیت شکننده سبز؛ `NOTICE-THIRD-PARTY.md` برای همه‌ی دارایی‌های ثالث کامل؛ گزارش ORT/ScanCode به‌عنوان آرتیفکت؛ فهرست موارد مسدود (احتمالاً خالی).
**ابزار:** `oss-review-toolkit/ort` (Apache‑2.0، ⭐2.1k) · `aboutcode-org/scancode-toolkit` (⭐2.7k) · `pip-licenses` (PyPI) · `RSeidelsohn/license-checker-rseidelsohn` (BSD‑3).

---

### WP‑13 · آشوب و حالت تنزل — P2
**چرا:** خواسته‌ی ۱۲ («اورلود»). زیرساخت سخت‌سازی SQLite و rollback و backup drill داری، ولی **رفتار برنامه زیر خرابی** تست نشده.
**شاهد:** `db/base.py:118-121` (WAL/busy_timeout=15000/foreign_keys) · `infra/scripts/rollback.sh` · `tests/integration/test_backup_drill.py` · `tests/integration/test_m97_migrations_and_backup.py` — ولی هیچ تستی برای «DB قفل/دیسک پر/سرویس AI timeout/SMS down/face-match down/Caddy TLS fail» نیست.
**کار:**
1. **Toxiproxy** را به `docker-compose.yml` (پروفایل `chaos`) اضافه کن و سناریوهای تأخیر/قطعی برای: DB، سرویس AI، SMS/OTP، سرویس چهره، و upstreamهای خارجی.
2. برای هر سناریو یک تست بنویس که **رفتار انتظار‌رفته** را اثبات کند: پیام کاربری درست، صف آفلاین کار کند، retry با backoff، circuit breaker، و اینکه هیچ داده‌ای گم/دوبار نوشته نشود (مرتبط با propertyهای `sync_lww` در WP‑06).
3. **دیسک پر / DB قفل / فایل خراب:** تست‌های واحد با mock/monkeypatch؛ اثبات کن `busy_timeout` و fallback درست عمل می‌کند و خطا به کاربر به شکل قابل فهم می‌رسد.
4. **دریل بازیابی واقعی:** `test_backup_drill.py` را طوری گسترش بده که **restore** روی یک DB جدید انجام شود و **برابری داده‌ها** (نه فقط وجود فایل) assert شود؛ و `alembic upgrade head` روی آن DB بازیابی‌شده (مطابق `RELEASE-CHECKLIST.md:17-18`) اجرا و سبز شود.
5. مسیر **SQLite → Postgres** (ADR‑002) را حداقل در یک job CI با Postgres واقعی اجرا کن (خدمات `postgres` در GitHub Actions رایگان است) تا انحصار SQLite تست‌ها شکسته شود.
6. نتایج را در `OPS-RUNBOOK.md` به‌عنوان «سناریوهای خرابی و پاسخ» ثبت کن.
**معیار پذیرش:** پروفایل chaos قابل اجرا با یک دستور؛ حداقل ۶ سناریوی خرابی با تست سبز؛ دریل restore با assert برابری داده؛ یک job CI با Postgres سبز.
**ابزار:** `Shopify/toxiproxy` (MIT، ⭐12.5k) · `respx`/`vcrpy` (شبیه‌سازی upstream در پایتون) · `pytest-xdist`/`pytest-rerunfailures` برای قطعیت.

---

### WP‑14 · گسترش گیت بار و بودجه‌های عملکرد — P2
**چرا:** گیت بار فعلی فقط دو اندپوینت سبک را می‌کوبد؛ مسیرهای سنگین و بودجه‌های سمت کلاینت پوشش ندارند.
**شاهد:** `mp-app/tests/load/k6-gate.js` فقط `GET /api/v1/health/ready` و `POST /api/v1/auth/otp/request`؛ آستانه‌ها `p(95)<2000ms` و `errors<0.05`؛ مراحل ۲۰→۲۰→۶۰ VU. هیچ گیتی برای اندازه‌ی APK، زمان استارت‌اپ، jank یا باندل استودیو نیست.
**کار:**
1. سناریوهای k6 اضافه کن (هرکدام با آستانه‌ی صریح): تطبیق چهره/چک‌این، تولید یا بازخوانی تجویز AI، ثبت ست/تمرین، تجمیع داشبورد استودیو، سرو مدیا (`/static/exercises/*.gif` ~۴۰۰KB) با بررسی **هدرهای cache** و فشرده‌سازی، و سناریوی ترکیبی «ساعت شلوغ باشگاه» مطابق ظرفیت واقعی.
2. هدرهای cache/CDN برای `static/` را بررسی و در صورت نبود اصلاح کن (`Caddyfile` + FastAPI static) و با k6 اثبات کن hit rate.
3. **پروفایل بک‌اند:** `py-spy` روی مسیرهای سنگین در یک job زمان‌بند؛ یک گیت **تعداد کوئری** برای endpointهای فهرست/داشبورد (با event listener روی SQLAlchemy) تا N+1 قرمز شود.
4. **بودجه‌های کلاینت:** اندازه‌ی APK/AAB (در WP‑01)، زمان استارت‌اپ و frame-drop با patrol/DevTools در حالت profile، و یک آستانه‌ی صریح برای هرکدام. `flutter build apk --analyze-size` را به‌عنوان آرتیفکت ثبت کن.
5. **بودجه‌های استودیو:** `rollup-plugin-visualizer` یا معادل Vite برای نقشه‌ی باندل + گیت اندازه؛ اجرای Lighthouse CI روی بیلد استودیو با بودجه‌ی صریح (perf/a11y/best-practices/SEO)؛ `web-vitals` در زمان اجرا.
6. گزارش عددی را در الگوی موجود `docs/MuscleParadise/LOAD-TEST-…` به‌عنوان نسخه‌ی جدید بنویس.
**معیار پذیرش:** k6 با ≥۵ سناریوی جدید و آستانه‌های صریح سبز؛ گیت N+1 و گیت اندازه‌ی باندل/APK در CI؛ گزارش بار جدید با اعداد واقعی.
**ابزار:** `grafana/k6` (AGPL — ابزار dev، مجاز) · `locustio/locust` (MIT) جایگزین · `hatoo/oha` (MIT) · `py-spy` · `GoogleChrome/lighthouse-ci` (Apache‑2.0) · `GoogleChrome/web-vitals` (Apache‑2.0).

---

### WP‑15 · حریم خصوصی، نشتی و بهداشت مخزن — P2
**چرا:** داده‌ی سلامتی/زیست‌سنجشی داری؛ چند نشانه‌ی نشتی احتمالی در خود مخزن هست.
**شاهد (اعداد اندازه‌گیری‌شده):**
- **۴۱ `print()`** در کد غیرتست بک‌اند → احتمال نشت PII به stdout/لاگ.
- **۱۱ `except Exception:`** واسع → بلعیدن خطا.
- **۴۲ `TODO/FIXME/HACK`** در `mp-app`.
- `docs/MuscleParadise/ui-previews/`: `03-kiosk-face-gate.png` (۱.۷MB)، `05-member-profile.png` (۶۱۶KB)، `04-payment-receipt.png` (۱.۷MB)، `07-client-home-grid.png` (۲.۱MB) و ۴ تصویر دیگر — commit‌شده در گیت.
- `.claude/` با ۹۳۱ فایل (۶۳۰ skill، ۱۲۲ rule، ۹۸ command، ۷۱ agent، ۹ hook).
**کار:**
1. همه‌ی `print()`ها را به logger ساخت‌یافته تبدیل کن؛ یک قاعده‌ی **Semgrep** (در `.semgrep/` موجود) اضافه کن که `print(`/`debugPrint(`/`console.log` در کد غیرتست را قرمز کند.
2. یک قاعده‌ی Semgrep و یک تست **redaction** اضافه کن: لاگ‌ها و payloadهای خطا نباید شامل موبایل، کد ملی، نام کامل، embedding چهره، یا داده‌ی کارت باشند (با الگوی regex + تست روی logger).
3. هر ۱۱ `except Exception:` را تعیین تکلیف کن: یا استثنا را دقیق کن، یا لاگ+بازفرستادن، یا با کامنت دلیلِ صریح. هیچ بلعیدن بی‌صدایی نماند.
4. ۴۲ `TODO/FIXME` را به صف قابل ردیابی تبدیل کن: یا انجام بده، یا یک issue/ردیف در `BUILD-QUEUE.md` با مسئول و دلیل بساز. TODO بی‌تکلیف نماند.
5. **اثبات synthetic بودن** تصاویر `ui-previews`: برای هر تصویر یک خط در `docs/MuscleParadise/ui-previews/PROVENANCE.md` بنویس (چگونه تولید شده، چه داده‌ای دارد، آیا چهره/رسید واقعی است). اگر داده‌ی واقعی دارد → در گزارش «مسدود — نیاز به تصمیم انسانی» (حذف از تاریخچه destructive است و در بخش ۷ است).
6. `.claude/` را مرور کن: هیچ transcript نشست، توکن، یا داده‌ی واقعی عضو در آن نباشد؛ اگر هست، گزارش بده (حذف نکن).
7. بهداشت مخزن: تصاویر بزرگ را با `infra/scripts/compress-media.sh` موجود بهینه کن یا به Git LFS منتقل کن؛ `.gitignore` را برای `*.keystore`, `keystore.properties`, `.env`, آرتیفکت‌های بیلد و خروجی ابزارهای ممیزی (`.audit/`, `reports/`) کامل کن.
**معیار پذیرش:** صفر `print` در کد غیرتست (با گیت Semgrep)؛ تست redaction سبز؛ همه‌ی `except Exception:` تعیین تکلیف؛ صفر TODO بی‌تکلیف؛ `ui-previews/PROVENANCE.md` کامل؛ `.gitignore` به‌روز.

---

### WP‑16 · ممیزی جامع خط‌به‌خط و ساده‌سازی (خواسته‌های ۱، ۵، ۶, ۹, ۱۰, ۱۱) — P1/P2
**چرا:** این هسته‌ی خواسته‌ی مالک است و باید **آخر** و با گیت‌های WP‑05/06/07 فعال انجام شود (قاعده‌ی ۳‑۱۱).
**کار (به‌ترتیب، هر مرحله با کامیت جدا):**
1. **نقشه‌ی کامل:** یک ایندکس محلی از کدبیس بساز تا همبستگی کلی و جزئی قابل پرسش شود — `repowise init --yes --no-prose` (AGPL، فقط به‌عنوان ابزار dev، هیچ API key لازم نیست) و سپس `repowise export --format markdown`؛ خروجی را در `.audit/` (gitignore‌شده) نگه دار و **خلاصه‌اش** را در `docs/MuscleParadise/architecture/` به‌روز کن. از `AGENTS.md`/`CLAUDE.md` تولیدی آن فقط اگر با `AGENTS.md` موجود تداخل نداشت استفاده کن؛ در غیر این صورت تولیدش را خاموش کن.
2. **کد تکراری (خواسته‌ی ۹):** `jscpd` را با آستانه‌ی صریح روی **هر سه زیرپروژه همزمان** اجرا کن (py + dart + ts/tsx) تا منطق موازی بین بک‌اند/کلاینت/استودیو هم دیده شود. علاوه بر تکرار متنی، **تکرار معنایی** را دستی بررسی کن: دو ماژول که یک قاعده‌ی biznesی را جداگانه پیاده کرده‌اند (به‌ویژه بین `engine/` و ماژول‌های `modules/*`). هر یافته → یا ادغام با تست، یا ثبت دلیل جدا بودن.
3. **کد مرده (خواسته‌ی ۱۱):**
   - پایتون: `ruff` (F401/F811/F841) + **vulture** + `pip check` برای وابستگی‌های نصب‌شده ولی استفاده‌نشده + endpointهای ثبت‌شده ولی بدون مصرف‌کننده.
   - استودیو: **knip** (فایل/export/وابستگی استفاده‌نشده) + `depcheck`.
   - Dart: `dart analyze` (`unused_element`, `unused_import`, `unused_field`, `dead_code`) + دارایی‌های بی‌مصرف در `pubspec.yaml` و `assets/`.
   - وابستگی‌های گراف: **import-linter** (پایتون) برای ممنوعیت لایه‌شکنی، **dependency-cruiser** یا **madge** برای استودیو (چرخه‌ها)، و یک تست معماری پایتون معادل ArchUnit (قرارداد لایه‌ها: `api → modules → engine/db`، ممنوعیت import معکوس).
   - خروجی: فهرست قطعی «حذف شد / نگه داشته شد چون …».
4. **همبستگی (خواسته‌ی ۶):** گراف وابستگی ماژول‌ها را تولید و در `docs/MuscleParadise/architecture/module-map.md` به‌روز کن؛ چرخه‌های وابستگی را بشکن (با گیت CI که چرخه‌ی جدید = قرمز)؛ fan‑in/fan‑out هر ماژول را گزارش کن و ۵ نقطه‌ی پرتراکم را با دلیل مستند کن.
5. **ساده‌سازی توابع (خواسته‌ی ۱۰):** با **lizard** (چندزبانه) و **radon** (پایتون) فهرست توابع با پیچیدگی بالا یا طول زیاد تولید کن؛ برای هر مورد بالای آستانه: استخراج تابع، حذف پارامترهای بی‌استفاده، یکسان‌سازی امضاها. **بدون تغییر رفتار** و با گیت جهش/property سبز. یک آستانه‌ی پیچیدگی (مثلاً cyclomatic ≤ 10) به‌عنوان گیت CI اضافه کن که فقط برای **کد جدید** سخت‌گیر باشد و برای موجود، عدد پایه را قفل کند (ضد‌رگرسیون).
6. **خروجی‌ها (خواسته‌ی ۴):** برای هر چیزی که خروجی تولید می‌کند (رسید، گزارش مربی، خروجی ارزیابی، export فایل، پیامک/اعلان، پاسخ API) یک **تست تصویب/طلایی (approval/golden)** بنویس: خروجی واقعی را در فایل مرجع قفل کن تا تغییر ناخواسته قرمز شود. این همان «OUTPUT-AUDIT» را اجرایی می‌کند.
7. **خط‌به‌خط (خواسته‌ی ۱):** یک پاس بازبینی ساخت‌یافته روی هر ماژول با چک‌لیست پیوست B؛ نتیجه را در یک جدول در `docs/MuscleParadise/AUDIT-FINAL-2026-11-18.md` ثبت کن (ماژول / تعداد فایل / یافته‌ها / اقدام / شاهد).
**معیار پذیرش:** گزارش jscpd با تعیین تکلیف همه‌ی یافته‌های بالای آستانه؛ صفر کد مرده قطعی (یا دلیل مستند)؛ صفر چرخه‌ی وابستگی؛ گیت پیچیدگی و ضد‌رگرسیون در CI؛ تست طلایی برای همه‌ی خروجی‌های فهرست‌شده؛ جدول ممیزی خط‌به‌خط کامل.
**ابزار:** `repowise-dev/repowise` (AGPL — ابزار dev) · `kucherenko/jscpd` (MIT، ⭐6.6k، ۲۲۰+ زبان) · `webpro-nl/knip` (ISC، ⭐12.7k) · `terryyin/lizard` (⭐2.6k) · `rubik/radon` (MIT) · vulture (PyPI) · `import-linter/import-linter` (BSD‑2، ⭐1.3k) · `sverweij/dependency-cruiser` (MIT، ⭐7.4k) · `pahen/madge` (MIT، ⭐10.2k).

---

## ۶) ترتیب اجرا

```
WP-00 (صف)
  ├─ P0: WP-01 (امضا/بیلد) → WP-02 (آرتیفکت) → WP-03 (قطعیت CI) → WP-04 (خطای زمان اجرا)
  ├─ P1: WP-05 (جهش) → WP-06 (property) → WP-07 (golden/on-device) → WP-08 (نوع) → WP-09 (a11y) → WP-10 (قرارداد API)
  └─ P2: WP-11 (i18n) · WP-12 (لایسنس) · WP-13 (آشوب) · WP-14 (بار/عملکرد) · WP-15 (حریم خصوصی)
WP-16 (ممیزی خط‌به‌خط و ساده‌سازی) — همیشه آخر، بعد از سبز شدن WP-05/06/07
```
قواعد ترتیب:
- هر P0 قبل از هر P1؛ هر P1 قبل از WP‑16.
- WP‑11 می‌تواند بعد از WP‑07 انجام شود تا goldenها با کلیدهای ترجمه بازنویسی نشوند.
- WP‑12 و WP‑15 مستقل‌اند و می‌توانند موازی بروند.
- اگر زمانی برای انجام همه نبود، به‌ترتیب اولویت پیش برو و در `SESSION_HANDOFF.md` دقیقاً بنویس کدام WP ناتمام ماند و از کجا ادامه یابد.

---

## ۷) خط قرمزها — فقط با تأیید صریح انسان (هیچ‌وقت خودسرانه انجام نده)

این‌ها تنها مواردی هستند که **باید** متوقف شوی و بپرسی. در همه‌ی موارد دیگر، تصمیم بگیر و ادامه بده (قاعده‌ی ۳‑۲).

1. **بازنویسی تاریخچه‌ی git** (`git filter-repo`/BFG/force-push) — برای حذف کلید امضای افشاشده یا تصاویر حاوی داده‌ی واقعی. **آماده‌سازی کن، اجرا نکن.** یک سند اجرایی گام‌به‌گام با دستورهای دقیق، ریسک‌ها، و ترتیب «rotate/revoke → بازنویسی → ابطال توکن/کش» بنویس و منتظر تأیید بمان. (`RELEASE-CHECKLIST.md:12` صریحاً می‌گوید حذف از HEAD کافی نیست.)
2. **چرخش/ابطال کلید امضا یا هر credential** و تغییر secrets در GitHub/Dokploy/GHCR.
3. **هر deploy واقعی، انتشار عمومی، ساخت release، یا push به شاخه‌ی محافظت‌شده‌ی اصلی** (خودت را به شاخه‌های کاری و PR محدود کن).
4. **حذف یا تغییر داده‌ی کاربر/عضو** در هر محیطی، و هر مهاجرت مخرب (drop column/table) بدون مهاجرت رفت‌وبرگشت تست‌شده.
5. **تغییر `LICENSE`، `NOTICE-THIRD-PARTY.md` در بخش حقوقی، یا هر متن حقوقی/حریم خصوصی کاربر** (`FACEID-PRIVACY-TEXT.md`, `biometric-policy.md`, `DATA-RETENTION.md`) — می‌توانی **پیشنهاد** بنویسی، اعمال نکن.
6. **شل‌کردن هر گیت CI** یا پایین‌آوردن آستانه‌ی پوشش/امنیت.
7. **افزودن وابستگی با لایسنس GPL/AGPL به آرتیفکت توزیعی**، یا هر سرویس/کلید پولی.
8. **ویرایش `AGENTS.md` یا `.claude/` به شکلی که قرارداد ایجنت‌ها را عوض کند** (افزودن skill جدید مجاز است؛ تغییر قواعد اولویت منبع حقیقت نه).

اگر موردی از این فهرست سر راه یک WP بود: بقیه‌ی WP را تا جایی که ممکن است انجام بده، آن بخش را در گزارش «مسدود — نیاز به تأیید انسانی» با دلیل و گزینه‌های پیشنهادی بنویس، و به WP بعدی برو. **متوقف نمان.**

---

## ۸) تعریف انجام‌شدن (گیت نهایی کل پروژه)

کار وقتی تمام است که همه‌ی این‌ها با **شاهد اجرایی** برقرار باشند:

- [ ] همه‌ی jobهای `ci.yml` (secret-scan, docs, backend, studio, client-flutter, live-contract, e2e-api) + `apk.yml` + `container.yml` سبز — بدون `|| true` روی گیت‌های معنادار.
- [ ] پوشش بک‌اند ≥ ۷۰٪ **و** mutation score برای `engine/` و `security/` اندازه‌گیری و قفل شده (WP‑05).
- [ ] برای هر ۱۹ موتور حداقل یک تست property سبز و قطعی (WP‑06).
- [ ] golden برای همه‌ی صفحات کلاینت + حداقل یک جریان patrol روی امولاتور سبز (WP‑07).
- [ ] `UI-INVENTORY.md` کامل: هر دکمه/فیلد/سرچ‌بار/انیمیشن یک ردیف، بدون ستون خالی (WP‑07/09/11).
- [ ] strict-casts/raw-types/inference در Dart و `strict` در TS فعال؛ عدد پایه‌ی `dynamic`/`any` قفل شده و رو به کاهش (WP‑08).
- [ ] تست‌های guideline دسترس‌پذیری روی همه‌ی صفحات سبز + سند ACCESS‑AUDIT جدید (WP‑09).
- [ ] `openapi.json` commit‌شده + گیت drift + گیت oasdiff + قرارداد زنده برای کلاینت Dart (WP‑10).
- [ ] صفر رشته‌ی کاربر‌نمای hardcode؛ تست pseudo-locale سبز (WP‑11).
- [ ] گیت لایسنس سبز؛ `NOTICE-THIRD-PARTY.md` کامل شامل دارایی‌ها (WP‑12).
- [ ] ≥۶ سناریوی آشوب سبز + دریل restore با assert برابری داده + یک job CI روی Postgres (WP‑13).
- [ ] ≥۵ سناریوی بار جدید با آستانه + گیت N+1 + بودجه‌ی اندازه‌ی APK و باندل (WP‑14).
- [ ] صفر `print` در کد غیرتست؛ تست redaction سبز؛ صفر `except Exception:` بی‌تکلیف؛ صفر TODO بی‌تکلیف؛ `ui-previews/PROVENANCE.md` کامل (WP‑15).
- [ ] گزارش jscpd/knip/vulture/lizard با تعیین تکلیف **همه‌ی** یافته‌ها؛ صفر چرخه‌ی وابستگی؛ گیت پیچیدگی فعال؛ تست طلایی برای هر خروجی (WP‑16).
- [ ] `python3 scripts/docs_gate.py` سبز؛ `SESSION_HANDOFF.md` به‌روز؛ یک گزارش `finn/reports/…` برای هر WP.
- [ ] جدول نهایی «خواسته‌ی ۱ تا ۱۲ ← WP ← شاهد» در گزارش نهایی.
- [ ] فهرست «مسدود — نیاز به تأیید انسانی» (احتمالاً شامل بازنویسی تاریخچه/چرخش کلید).

---

## ۹) قالب گزارش (برای هر WP)

فایل: `finn/reports/wp<NN>-<slug>.md`

```markdown
# WP-<NN> — <عنوان>
تاریخ: <ISO> · شاخه/PR: <…> · اولویت: P0/P1/P2 · وضعیت: انجام‌شد / بخشی / مسدود

## چه شد
<۳ تا ۸ خط، فعل‌محور>

## شاهد اجرایی
- دستور: `<دقیق>` → خروجی/عدد: `<…>`
- CI run: <شناسه/لینک> · تست‌های جدید: <نام‌ها> · گیت‌های اضافه: <job/step>

## پوشش خواسته‌های مالک
<کدام یک از موارد ۱ تا ۱۲>

## تصمیم‌های خودکار
- <تصمیم> — چرا: <یک خط>

## اعداد پایه (برای گیت ضد‌رگرسیون)
<coverage / mutation score / dynamic count / any count / duplication % / complexity / APK size / bundle size / p95>

## مسدود — نیاز به تأیید انسانی
- <مورد> — گزینه‌ها: <…> — پیشنهاد: <…>

## قدم بعدی برای نشست بعد
- <دقیق و قابل اجرا>
```

در پایان هر نشست: `docs/MuscleParadise/SESSION_HANDOFF.md` را به‌روز کن (وضعیت WPها، قدم بعدی، اعداد پایه) تا نشست بعدی بدون حرف‌زدن با مالک ادامه دهد.

---

## پیوست A — کاتالوگ ابزار اوپن‌سورس رایگان (راستی‌آزمایی‌شده در ۲۰۲۶‑۱۱‑۱۸)

> ستاره/لایسنس از GitHub API. «dev» = فقط ابزار توسعه/CI (GPL/AGPL مجاز)؛ «dist» = داخل آرتیفکت توزیعی (فقط MIT/Apache/BSD/ISC/MPL).

**مستندسازی، دیاگرام، انتقال context**
| ابزار | لایسنس | ستاره | نقش |
|---|---|---|---|
| `repowise-dev/repowise` | AGPL‑3.0 (dev) | 8.2k | گراف فراخوانی ۲۸ زبان، ویکی هر فایل/سمبل، کد مرده، health score، blast radius، C4/Structurizr، برنامه‌ی ریفکتور، نوشتن AGENTS.md، ۱۰ ابزار MCP، بدون API key |
| `AsyncFuncAI/deepwiki-open` | MIT (dev) | 18.5k | ویکی + دیاگرام Mermaid خودکار + Ask با RAG + خروجی Markdown |
| `langchain-ai/openwiki` | MIT (dev) | 18.0k | نوشتن و **نگهداری** مستندات ایجنت + ارجاع در AGENTS.md |
| `ahmedkhaleel2004/gitdiagram` | MIT (dev) | 19.0k | دیاگرام تعاملی معماری از مخزن |
| `oraios/serena` | GPL‑3.0 (dev) | 31.5k | دسترسی سطح سمبل از طریق MCP؛ کاهش مصرف توکن |
| `yamadashy/repomix` | MIT (dev) | 29.3k | کل مخزن در یک فایل AI‑ready |
| `coderamp-labs/gitingest` | MIT (dev) | 16.2k | `hub`→`ingest` برای prompt مخزن |
| `The-Pocket/PocketFlow-Tutorial-Codebase-Knowledge` | MIT (dev) | 12.8k | مخزن → آموزش گام‌به‌گام |

**ارکستراتور و کیفیت**
| ابزار | لایسنس | ستاره | نقش |
|---|---|---|---|
| `oxsecurity/megalinter` | AGPL‑3.0 (dev) | 2.7k | ۶۸ زبان، ۱۲۴ لینتر، شامل COPYPASTE(jscpd)؛ یک `docker run` |
| `SonarSource/sonarqube` | LGPL‑3.0 (dev) | 11.2k | Quality Gate دائمی (اختیاری؛ خود-hosted) |
| `reviewdog/reviewdog` | MIT (dev) | 9.8k | تبدیل خروجی لینترها به کامنت روی خط PR |
| `pre-commit/pre-commit` | MIT (dev) | 15.7k | گیت قبل از کامیت |
| `The-PR-Agent/pr-agent` | Apache‑2.0 (dev) | 16.4k | بازبین خودکار PR |

**معماری و همبستگی**
| ابزار | لایسنس | ستاره | نقش |
|---|---|---|---|
| `import-linter/import-linter` | BSD‑2 | 1.3k | قوانین لایه‌بندی پایتون به‌صورت تست |
| `sverweij/dependency-cruiser` | MIT | 7.4k | قواعد وابستگی + گراف برای TS/JS |
| `pahen/madge` | MIT | 10.2k | چرخه‌های وابستگی JS/TS |
| `TNG/ArchUnit` | Apache‑2.0 | 3.9k | تست معماری (اگر مسیر JVM اضافه شد) |
| `jQAssistant/jqassistant` | GPL‑3.0 (dev) | 0.3k | کدبیس JVM → Neo4j + Cypher |

**کد مرده، تکراری، پیچیدگی**
| ابزار | لایسنس | ستاره | نقش |
|---|---|---|---|
| `webpro-nl/knip` | ISC | 12.7k | کد مرده‌ی TS/React |
| `kucherenko/jscpd` | MIT | 6.6k | کپی/پیست در ۲۲۰+ زبان (py+dart+ts همزمان) |
| `terryyin/lizard` | MIT | 2.6k | پیچیدگی cyclomatic چندزبانه |
| `rubik/radon` | MIT | 2.0k | متریک پیچیدگی پایتون |
| `vulture` (PyPI) | MIT | — | کد مرده‌ی پایتون |
| `semgrep/semgrep` | LGPL‑2.1 (dev) | 17.8k | قواعد سفارشی (PII در لاگ، print ممنوع) |
| `openrewrite/rewrite` | Apache‑2.0 | 4.0k | ریفکتور مکانیکی انبوه (مسیر JVM) |

**تست عمیق**
| ابزار | لایسنس | ستاره | نقش |
|---|---|---|---|
| `boxed/mutmut` | BSD‑3 | 1.5k | mutation پایتون |
| `sixty-north/cosmic-ray` | MIT | 0.7k | mutation موازی پایتون |
| `stryker-mutator/stryker-js` | Apache‑2.0 | 3.4k | mutation TS/JS |
| `HypothesisWorks/hypothesis` | MPL‑2.0 | 9.2k | property‑based پایتون |
| `dubzzz/fast-check` | MIT | 5.3k | property‑based TS |
| `leancodepl/patrol` | Apache‑2.0 | 1.5k | تست on‑device فلاتر (dialogهای permission) |
| `schemathesis/schemathesis` | MIT | 3.8k | فازی‌کردن API از روی OpenAPI |
| `oasdiff/oasdiff` (+`oasdiff-action`) | Apache‑2.0 | 1.5k | گیت تغییر شکننده‌ی API |
| `keploy/keploy` | Apache‑2.0 | 19.9k | ضبط ترافیک واقعی → تست + mock |
| `Orange-OpenSource/hurl` | Apache‑2.0 | 19.3k | تست HTTP متنی با assert |
| `stoplightio/prism` | Apache‑2.0 | 5.1k | mock + اعتبارسنجی OpenAPI |
| `vitest-dev/vitest` | MIT | 17.4k | موجود در پروژه |
| `jacoco/jacoco` | EPL | 4.6k | پوشش JVM (در صورت نیاز) |

**UI، a11y، پرفورمنس**
| ابزار | لایسنس | ستاره | نقش |
|---|---|---|---|
| `microsoft/playwright` | Apache‑2.0 | 100.5k | E2E مرورگری برای استودیو + رگرسیون بصری + axe |
| `storybookjs/storybook` | MIT | 91.6k | ایزوله‌سازی هر کامپوننت و state |
| `garris/BackstopJS` | MIT | 7.2k | رگرسیون بصری سناریومحور |
| `dequelabs/axe-core` | MPL‑2.0 | 7.8k | موتور a11y |
| `pa11y/pa11y` | LGPL‑3.0 (dev) | 4.6k | a11y خودکار صفحات |
| `GoogleChrome/lighthouse-ci` | Apache‑2.0 | 7.2k | بودجه‌ی perf/a11y/SEO در CI |
| `GoogleChrome/web-vitals` | Apache‑2.0 | 8.7k | متریک واقعی کاربر |
| `webpack/webpack-bundle-analyzer` | MIT | 12.7k | تحلیل باندل (برای Vite: `rollup-plugin-visualizer`) |

**بار، آشوب**
| ابزار | لایسنس | ستاره | نقش |
|---|---|---|---|
| `grafana/k6` | AGPL‑3.0 (dev) | 32.3k | موجود در پروژه |
| `locustio/locust` | MIT | 28.3k | جایگزین/تکمیل k6 |
| `hatoo/oha` | MIT | 10.7k | بار سریع یک endpoint |
| `mcollina/autocannon` | MIT | 8.5k | بنچمارک Node |
| `Shopify/toxiproxy` | MIT | 12.5k | تزریق latency/قطعی |
| `apache/jmeter` · `gatling/gatling` | Apache‑2.0 | 9.6k / 7.0k | سناریوهای سنگین |

**امنیت و زنجیره‌ی تأمین**
| ابزار | لایسنس | ستاره | نقش |
|---|---|---|---|
| `aquasecurity/trivy` | Apache‑2.0 | 39.5k | CVE ایمیج/وابستگی/IaC + SBOM + رازها |
| `anchore/grype` | Apache‑2.0 | 13.3k | اسکن CVE ایمیج/فایل‌سیستم |
| `anchore/sbom-action` | Apache‑2.0 | 0.3k | SBOM در GitHub Actions |
| `hadolint/hadolint` | GPL‑3.0 (dev) | 12.5k | لینت Dockerfile |
| `sigstore/cosign` | Apache‑2.0 | 6.4k | امضا و attestation ایمیج |
| `gitleaks/gitleaks` | MIT | 31.2k | موجود در پروژه |
| `zaproxy/zaproxy` | Apache‑2.0 | 16.2k | DAST روی اپ deploy‌شده |
| `PyCQA/bandit` | Apache‑2.0 | 8.4k | موجود در پروژه |
| `burke-software/GlitchTip` | MIT | 0.2k | error/crash tracking خود‌میزبان |

**لایسنس و انطباق**
| ابزار | لایسنس | ستاره | نقش |
|---|---|---|---|
| `oss-review-toolkit/ort` | Apache‑2.0 | 2.1k | انطباق لایسنس کل زنجیره |
| `aboutcode-org/scancode-toolkit` | Apache‑2.0/NOASSERTION | 2.7k | لایسنس/کپی‌رایت **دارایی‌ها** |
| `pip-licenses` (PyPI) | MIT | — | لایسنس وابستگی‌های پایتون |
| `RSeidelsohn/license-checker-rseidelsohn` | BSD‑3 | 0.2k | لایسنس وابستگی‌های npm |
| `newren/git-filter-repo` | MIT | — | بازنویسی تاریخچه (**فقط با تأیید انسان**) |

**ایجنت و مدل رایگان (برای پاس‌های حجیم ریفکتور)**
| ابزار | لایسنس | ستاره | نقش |
|---|---|---|---|
| `OpenHands/OpenHands` | MIT | 93.7k | ایجنت خودران برای کارهای حجیم |
| `Aider-AI/aider` | Apache‑2.0 | 50.2k | ریفکتور چندفایلی git‑native |
| `Qwen/Qwen3-Coder-30B-A3B-Instruct` (HF) | Apache‑2.0 | — | مدل کد محلی، رایگان، با GGUF روی سخت‌افزار معمولی |

**استفاده نکن (آرشیو/رکود):** `lost-pixel/lost-pixel` · `apiaryio/dredd` · `CoatiSoftware/Sourcetrail` · `doyensec/electronegativity` · `qodo-ai/qodo-cover` (unmaintained از ۲۰۲۵‑۰۶‑۱۵) · `EvoSuite/evosuite` · `danvk/source-map-explorer` · `jeremylong/DependencyCheck`.

---

## پیوست B — چک‌لیست ممیزی خط‌به‌خط (خواسته‌ی ۱ و ۸)

برای **هر ماژول** این جدول را در `docs/MuscleParadise/AUDIT-FINAL-2026-11-18.md` پر کن:

| ستون | محتوا |
|---|---|
| ماژول/مسیر | مثلاً `mp-app/backend/engine/safety.py` |
| اندازه | تعداد فایل/خط/تابع |
| ورودی‌ها و خروجی‌ها | فهرست توابع عمومی + امضا + نوع خروجی (خواسته‌های ۴ و ۵) |
| مصرف‌کننده‌ها | چه ماژول/endpoint/صفحه‌ای صدایش می‌زند (خواسته‌ی ۲ و ۶) |
| وابستگی‌ها | چه چیزی import می‌کند؛ آیا چرخه دارد؟ |
| پوشش تست | واحد / یکپارچه / property / mutation / golden |
| تکرار | آیا منطقش جای دیگری هم پیاده شده؟ (خواسته‌ی ۹) |
| کد مرده | تابع/پارامتر/شاخه‌ی بی‌استفاده (خواسته‌ی ۱۱) |
| پیچیدگی | عدد cyclomatic و اقدام ساده‌سازی (خواسته‌ی ۱۰) |
| خطاها | همه‌ی مسیرهای شکست چه رفتاری دارند؟ آیا بلعیده می‌شوند؟ |
| ایمنی/حریم خصوصی | داده‌ی حساس لمس می‌شود؟ لاگ/redaction درست است؟ |
| عملکرد | کوئری/حلقه/همزمانی مشکوک؟ N+1؟ |
| a11y و i18n | (برای UI) semantic label، کنتراست، اندازه‌ی هدف، ترجمه، RTL |
| اقدام | چه شد / چه باید بشود |
| شاهد | تست، CI run، عدد |

و برای **هر عنصر رابط کاربری** (خواسته‌ی ۸) یک ردیف در `docs/MuscleParadise/UI-INVENTORY.md`:
شناسه · صفحه · نوع (دکمه/ورودی/سرچ‌بار/سوئیچ/لینک/انیمیشن) · مسیر فایل · stateها · تست widget · golden · on-device · a11y · i18n · رفتار خطا · وضعیت.

---

## پیوست C — دستورات آماده

```bash
# --- آماده‌سازی ---
git status --short --branch
python3 scripts/docs_gate.py
pip install -e "mp-app/backend[dev]"
cd mp-app/studio && npm ci && cd -
cd mp-app/client && flutter pub get && cd -

# --- گیت‌های موجود (باید سبز بمانند) ---
cd mp-app/backend && ruff check . && ruff format --check . \
  && pytest --cov=. --cov-report=xml --cov-fail-under=70 \
  && bandit -r . -q && pip-audit
cd mp-app/studio && npm run lint && npm test && npm run build
cd mp-app/client && flutter analyze --no-fatal-infos && flutter test

# --- ابزارهای جدید (پس از نصب) ---
pip install mutmut hypothesis vulture radon import-linter pip-licenses
npx --yes jscpd --threshold 3 --reporters consoleFull,html --output .audit/jscpd \
  mp-app/backend mp-app/client/lib mp-app/studio/src
npx --yes knip --reporter json > .audit/knip.json          # در mp-app/studio
lizard mp-app/backend mp-app/client/lib -C 15 -T cyclomatic_complexity=15 > .audit/lizard.txt
radon cc mp-app/backend -s -n C > .audit/radon.txt
import-linter --config .importlinter                        # قوانین لایه‌بندی
mutmut run --paths-to-mutate mp-app/backend/engine          # سپس mutmut results
hypothesis: در تست‌ها (profile=ci, derandomize=True, deadline=None)
repowise init --yes --no-prose && repowise export --format markdown   # در .audit/
trivy image <ghcr/.../backend:sha-…> --severity CRITICAL,HIGH --exit-code 1
oasdiff breaking docs/api/openapi.json docs/api/openapi.json --fail-on ERR
k6 run mp-app/tests/load/k6-gate.js --env BASE_URL=<staging>
```

**پایان سند.** همه‌ی ۱۶ بسته‌ی کاری را انجام بده، گزارش هرکدام را بنویس، و در پایان جدول «خواسته‌ی ۱ تا ۱۲ ← WP ← شاهد» را در `docs/MuscleParadise/AUDIT-FINAL-2026-11-18.md` بگذار. هیچ سؤالی از مالک نپرس مگر در موارد بخش ۷.
