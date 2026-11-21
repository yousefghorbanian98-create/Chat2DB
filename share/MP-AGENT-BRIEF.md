# بریف اجرای کامل ممیزی و ارتقای نهایی — MuscleParadise (MP)

**نسخه:** ۲.۱ · **تاریخ:** ۲۰۲۶‑۱۱‑۲۰
**مبنای ممیزی جاری:** کلون فقط‌خواندنی از `yousefghorbanian98-create/MP` شاخه‌ی `main` در کامیت `662ff88` (Merge PR #22)
**مبنای مکمل (جدید در ۲.۱):** شاخه‌ی `arena/da474b65-mp` در کامیت `0653bd1` → `docs/architecture/repowise/PROJECT-HANDOFF.md` (۴۵۹ خط) به‌همراه `findings-main-e5c8891.md`، `findings-2026-11-20.md` و `README.md` همان پوشه — **همه‌ی ادعاهای مهم این اسناد در کد راستی‌آزمایی شد**؛ سه ادعا غلط و یک جدول کلیدی خالی از آب درآمد (بخش ۴‑ت).
**فهرست مستقل ۶۳ مشکل:** `share/MP-PROBLEMS-2026-11-20.md` (هم‌نشین این سند، با شاهد خط‌به‌خط). نگاشت کامل «مشکل ← WP» در **پیوست E**.
**مبنای قبلی (نسخه‌ی ۱٫۱):** شاخه‌ی `arena/4f336f66-mp` در کامیت `e6fa0a9`
**اختلاف دو مبنا:** ۱۵۰۹ فایل تغییر کرده، ‎+44,440‎ / ‎−174,375‎ خط؛ فایل‌های ترک‌شده از ۱۶۷۸ به **۱۱۴۷** کاهش یافته
**مخزن هدف:** `MP` · **زبان سند و خروجی‌ها:** فارسی

> ✅ **وضعیت از طرف مالک:** پروژه تمام‌شده اعلام شده است. پس این سند یک **پاس سخت‌سازی و آمادگی انتشار نهایی** است، نه برنامه‌ی ساخت.
>
> ⚠️ **پنج هشدار قبل از شروع:**
> ۱. **بخش ۴‑ب را اول بخوان.** بسیاری از توصیه‌های نسخه‌ی ۱ در این مدت انجام شده‌اند (امضای Android، گیت پین SDK، بیلد وب، DAST با schemathesis، حذف `.claude`، صفر شدن stubها، `strict` و صفر `any` در استودیو). **کار انجام‌شده را دوباره انجام نده.**
> ۲. **همه‌ی شاهدها از کامیت `662ff88` هستند.** قبل از هر WP، شاهد همان WP را دوباره اندازه بگیر (قاعده‌ی ۳‑۱۳).
> ۳. **یک خطر بازِ جدی وجود دارد:** گزارش QA خودتان (`qa-report/FINAL-REPORT.md` بخش ۵) یک قفل‌شدگی کامل سرور بر اثر پر شدن استخر اتصال SQLite را ثبت کرده که **«علت ریشه‌ای ثابت نشده است»**. این WP‑01 است و بر هر کار دیگری مقدم است.
> ۴. **چهار حفره‌ی امنیتی/پیکربندی هست که در هیچ سندی ثبت نشده بود** و من در کد راستی‌آزمایی کردم: `/api/v1/metrics` کاملاً عمومی است، `MP_TRUSTED_PROXIES` پیش‌فرض خالی است و در production اعتبارسنجی نمی‌شود (یعنی کل باشگاه یک سبد rate-limit مشترک دارند)، `MP_REQUIRE_WORKER=False` است (readiness بدون worker صف سبز می‌ماند)، و `MP_DATABASE_URL` در production چک نمی‌شود. ← **WP‑22**.
> ۵. **سند تحویل تازه (`PROJECT-HANDOFF.md`) خودش ۸ نقص دارد** (جدول مجوزهای خالی، پیش‌فرض CORS به‌صورت «(»، ادعای غلط درباره‌ی تریگر `apk.yml` و تناقض با §۱۰ خودش، مسیر اشتباه روتر `face`، وصل نبودن `--check` به CI). چون این سند منبع حقیقت نشست‌های بعدی است، **WP‑24 را زود انجام بده** (ارزان و فوری) و تا اصلاحش، ادعاهایش را با کد چک کن (قاعده‌ی ۳‑۱۶).

---

## ۰) چگونه این سند را بخوانی

این سند جای حرف‌زدن با مالک را می‌گیرد. **هیچ سؤالی نپرس؛ همه‌ی تصمیم‌ها در بخش ۳ گرفته شده‌اند.**
ترتیب: ۱ (مأموریت) → ۲ (خواسته‌ها) → ۳ (قواعد) → ۴ (توانمندی‌های تأییدشده + موارد بسته‌شده) → ۵ (اعداد پایه) → ۶ (بسته‌های کاری **WP‑00…WP‑26** به ترتیب بخش ۷) → ۸ (خط قرمزها) → ۹ (گیت انتشار) → **پیوست E** (نگاشت ۶۳ مشکل ← WP؛ هیچ مشکلی بی‌صاحب نمانده).
هر WP پنج بخش دارد: **چرا / شاهد / کار / معیار پذیرش / ابزار**. بدون برآورده‌شدن معیار پذیرش، WP را بسته اعلام نکن.

---

## ۱) مأموریت

پروژه تمام شده است. مأموریت تو **رساندن آن به سطح کلاس جهانی و آماده‌ی انتشار واقعی** است، با دو اولویت هم‌زمان:

**الف) بستن خطرهای بازِ عملیاتی و انتشاری** — قفل‌شدگی استخر DB، زنجیره‌ی تأمین آرتیفکت، نبودِ گزارش خطای زمان اجرا، ۲۱ آیتم بازِ `RELEASE-CHECKLIST.md`، کلید امضای افشاشده، و فایل دیتابیس ترک‌شده در مخزن.

**ب) عمق‌بخشیدن به تضمین کیفیت** — پوشش ۹۴٫۲۸٪ یک عددِ خطوطِ اجراشده است، نه اثبات گیرنده‌ی باگ. تست جهش، تست ویژگی‌محور، رگرسیون بصری کلاینت، دسترس‌پذیری کلاینت، یکپارچگی پول و اعداد بزرگ، پلتفرم وب/PWA، و گیت‌های ضد‌رگرسیون.

خروجی تو **فقط گزارش نیست**: کد اصلاح‌شده، تست اضافه‌شده، گیت CI نصب‌شده، و سند به‌روزشده است.

---

## ۲) خواسته‌های صریح مالک (بدون تغییر)

۱. تمام خط‌به‌خط کدهای بک‌اند و فرانت‌اند بررسی شود.
۲. تمام سیم‌کشی‌های برنامه بررسی شود.
۳. تمام موتورها و ورک‌فلوها بررسی شود.
۴. تک‌تک چیزهایی که باید خروجی داشته باشند، مشخص و تست شود.
۵. توابع و پارامترها بررسی شود.
۶. همبستگی کلی و جزئی برنامه بررسی شود.
۷. انیمیشن‌ها و اینترکشن‌ها بررسی و تست شود.
۸. همه‌چیز، از جمله سرچ‌بارها و **تک‌تک دکمه‌ها**، بررسی شود.
۹. چک شود **کدی روی کد دیگری نیفتاده باشد**.
۱۰. **توابع ساده‌سازی شوند.**
۱۱. **کد مرده نداشته باشیم.**
۱۲. هر چیزی که برنامه را در **کلاس جهانی** نگه می‌دارد، یک بار **تست و اورلود** شود.

در پایان، جدول «خواسته‌ی ۱ تا ۱۲ ← WP ← شاهد اجرایی» را در `docs/MuscleParadise/AUDIT-FINAL-2026-11-20.md` بگذار. توجه: خواسته‌ی ۸ تا حد زیادی با `qa-report/buttons.json` (۱۰۱ دکمه در ۱۱ صفحه) و `qa-report/FINAL-REPORT.md` پوشش شده؛ کار تو **تکمیل و پایدارکردن** آن است (WP‑09، WP‑21).

---

## ۳) قواعد کار — تصمیم‌های از پیش گرفته‌شده (سؤال نپرس)

**۳‑۱. منبع حقیقت.** `AGENTS.md` مخزن → نزدیک‌ترین `AGENTS.md` scoped → این سند → `docs/README.md` و `SESSION_HANDOFF.md` و TODO جاری. ادعای «کار می‌کند» فقط با **کد، تست، یا CI** اثبات می‌شود. `qa-report/FINAL-REPORT.md` و `evidence/m60/STATUS.md` الگوی درستِ «شاهد یا برچسب بازبینی دستی» هستند — همان سبک را حفظ کن.

**۳‑۲. وقتی مردد بودی.** کم‌خطرترین گزینه را انتخاب کن، زیر «تصمیم خودکار» در گزارش یک خط بنویس، و **ادامه بده**. تنها استثنا: بخش ۸.

**۳‑۳. وقتی چیزی را نمی‌دانی.** با شاهد بررسی کن. اگر اثبات نشد بنویس «نامعلوم — نیاز به شاهد اجرایی». حدس نزن؛ وضعیت را بی‌صدا بازنویسی نکن.

**۳‑۴. اندازه‌ی تغییر.** هر WP = یک شاخه = یک PR. الگوی پیام کامیت موجود (`fix(client): …`, `ci(web): …`, `docs(todo): …`). مطابق `docs/MuscleParadise/BRANCH-CONSOLIDATION-2026-11-20.md`: **`main` تنها شاخه‌ی دائمی است؛ merge سپس حذف فوری شاخه.**

**۳‑۵. CI هرگز قرمز نماند و هرگز شل نشود.** `--cov-fail-under=70` (که امروز واقعاً ۹۴٫۲۸٪ است)، گیت‌های `flutter analyze`، `dart format` (M109)، پین SDK، گیت WCAG استودیو و Gitleaks را **حذف یا ضعیف نکن**. آستانه‌ها فقط upward.
jobهای فعلی که باید سبز بمانند — `ci.yml`: `secret-scan`, `docs`, `backend`, `studio`, `client-flutter`, `live-contract`, `e2e-api`, `client-pinned`؛ به‌علاوه `apk.yml`, `web.yml`, `container.yml`, `deploy.yml`, `client-format-fix.yml`, `gitleaks-fingerprints.yml`.

**۳‑۶. سیاست ابزار جدید.** اوپن‌سورس + کاملاً رایگان + بدون سرویس ابری پولی + قابل اجرا در CI یا محلی.
- **وابستگی توزیعی** (داخل ایمیج/APK/استودیو): فقط MIT، Apache‑2.0، BSD، ISC، MPL‑2.0. **GPL/AGPL ممنوع** (لایسنس پروژه Proprietary است).
- **ابزار dev/CI** (اجرا می‌شود، ship نمی‌شود): GPL/AGPL مجاز است (مثل `k6`، `hadolint`، `repowise`).
- برای هر وابستگی جدید یک خط در گزارش: نام، لایسنس، چرا، «توزیعی» یا «dev».

**۳‑۷. حریم خصوصی و داده.** محصول داده‌ی سلامتی و **زیست‌سنجشی (چهره)** پردازش می‌کند.
- هیچ داده‌ی واقعی عضو/چهره/رسید/شماره در مخزن، تست، فیکسچر، آرتیفکت CI، اسکرین‌شات یا گزارش نگذار. الگوی درستِ موجود: داده‌ی seed مصنوعی (`qa-report/tools/seed_live.py`، «عضو فیک …» در `buttons.json`).
- الگوی redaction موجود Gitleaks (`--redact`، «value withheld») را در همه‌ی گیت‌های جدید حفظ کن.
- قبل از دست‌زدن به مسیر چهره/پرداخت: `security/biometric-policy.md`, `FACEID-PRIVACY-TEXT.md`, `DATA-RETENTION.md`, `modules/privacy/`.

**۳‑۸. مستندسازی هم‌زمان.** هر WP: به‌روزرسانی `SESSION_HANDOFF.md` + گزارش در `finn/reports/<slug>.md` + (در صورت تغییر معماری) ADR یا `architecture/c4.md`/`module-map.md`. `python3 scripts/docs_gate.py` و `tools/mermaid-check` باید سبز بمانند.

**۳‑۹. زبان.** مستند/کامنت/گزارش فارسی؛ شناسه‌ها، نام فایل، پیام کامیت و کد انگلیسی.

**۳‑۱۰. هزینه.** هیچ سرویس یا کلید پولی اضافه نکن. مسیر مسدود را «مسدود — نیاز به تصمیم انسانی» ثبت کن و از جایگزین رایگان/محلی استفاده کن (الگوی درست: `scripts/dast.py` که به‌جای ZAP/nucleiِ غیرقابل‌نصب، از schemathesis استفاده کرد و دلیلش را صادقانه نوشت).

**۳‑۱۱. ترتیب ایمنی.** ریفکتور (WP‑14، WP‑21) فقط **بعد** از سبز شدن گیت جهش (WP‑07) روی همان مسیر.

**۳‑۱۲. دامنه.** فقط داخل مخزن `MP`. هیچ تغییری در تنظیمات GitHub (branch protection، environments، secrets، «automatically delete head branches»)، حساب کاربری، یا زیرساخت بیرونی نده — این‌ها در بخش ۸ آمده‌اند.

**۳‑۱۳. راستی‌آزمایی شاهد قبل از عمل (اجباری).** قبل از هر WP: دستور اندازه‌گیریِ شاهدش را روی checkout جاری اجرا کن، عدد امروز را در ستون «عدد پایه» گزارش بنویس. اگر حفره بسته شده بود → WP را «قبلاً انجام‌شده — شاهد: …» ببند و فقط **گیت ضد‌رگرسیونش** را اضافه کن. اگر بدتر شده بود → عدد جدید را پایه بگذار و علامت بزن.

**۳‑۱۴. کار تکراری نکن.** بخش ۴‑ب فهرست کارهای بسته‌شده است. اگر شاهی در آن فهرست بود، آن را دوباره اجرا نکن؛ فقط گیت پایدارساز اضافه کن.

**۳‑۱۶. سند تولیدشده را باور نکن.** `docs/architecture/repowise/PROJECT-HANDOFF.md` و خروجی‌های RepoWise **تولید خودکار** دارند و همین حالا ۸ نقص ثبت‌شده دارند (D1–D8 در بخش ۴‑ت). خودِ `docs/architecture/repowise/README.md` هم نوشته «یافته‌های RepoWise شواهدی برای بررسی‌اند، نه اثبات خطا». پس یافته‌ی ابزار = **نخِ سرنخ**، نه حکم. اگر سند و کد تناقض داشتند **کد برنده است** و سند را در WP‑24 اصلاح کن. هر عددی را که از این اسناد به گزارش خودت منتقل می‌کنی، با یک دستور روی کد تأیید کن.

**۳‑۱۵. صداقتِ شاهد.** اگر کاری نیاز به دسترسی بیرونی، secret، دستگاه واقعی یا محیط production دارد و در این محیط ممکن نیست، آن را **صریحاً `BLOCKED`** ثبت کن (الگوی `qa-report/FINAL-REPORT.md` و `evidence/m60/STATUS.md`) و سراغ بعدی برو. «انجام شد»ِ بدون شاهد، ممنوع است.

---

## ۴) وضعیت موجود

### ۴‑الف) توانمندی‌های تأییدشده (این‌ها قوی‌اند؛ خرابشان نکن)

**تست و پوشش**
- بک‌اند: `qa-report/FINAL-REPORT.md` → **۱۰۹۵ تست پاس، ۲ skip، پوشش ۹۴٫۲۸٪** (گیت `--cov-fail-under=70` در `ci.yml:131`)؛ **۱۴۴ فایل تست** شامل `integration/`, `unit/`, `regression/`, `evaluation/`, `e2e/`.
- استودیو: **۲۸۲ تست vitest پاس، ۹ skip**، `tsc --noEmit` بدون خطا، `tsconfig` → `"strict": true`، **صفر `: any` در `src/`**، گیت‌های WCAG و sync توکن‌ها، `tests/a11y.test.tsx`, `tests/apiCoverage.test.ts`, `tests/liveContract.test.ts`, `tests/topbarTitles.test.tsx`.
- کلاینت: ۲۹ فایل تست؛ job `client-pinned` با **پین Flutter 3.50.0 + بررسی drift در برابر `.devcontainer/Dockerfile`**، `flutter analyze` (خط/هشدار = شکست)، `flutter test --coverage`، **کامپایل Android debug** به‌عنوان شاهد Kotlin/Gradle، و **گیت `dart format` (M109)**.
- **صفر stub**: `NotImplementedError`/`UnsupportedOperationException`/«not implemented» = **۰** (در ممیزی قبلی ۳۶ بود).

**امنیت**
- `ci.yml` → `secret-scan`: Gitleaks با **راستی‌آزمایی checksum نسخه**، اسکن **کل تاریخچه**، `--redact`، خلاصه‌ی بدون مقدار. به‌علاوه `gitleaks-fingerprints.yml` و اثرانگشت‌گذاری در `client-format-fix.yml`.
- `bandit` + `pip-audit` + **Semgrep با `.semgrep/project-rules.yml`** در job بک‌اند.
- `mp-app/backend/app/security/headers.py`: `X-Content-Type-Options: nosniff`, `X-Frame-Options: DENY`, `Referrer-Policy: no-referrer`, `Permissions-Policy: camera=(self), microphone=(), geolocation=()`.
- `mp-app/infra/Caddyfile`: همان هدرها در لبه + `Strict-Transport-Security: max-age=63072000; includeSubDomains` + حذف `-Server` + TLS خودکار + `encode gzip zstd` + لاگ JSON.
- **امضای Android اصلاح شده**: `build.gradle.kts` از `MP_ANDROID_KEYSTORE_PATH/STORE_PASSWORD/KEY_ALIAS/KEY_PASSWORD` (PKCS12) می‌خواند و **fallback به debug حذف شده** — با کامنت صریح «A release must never silently use the public Android debug signing key».
- `security/crypto.py` → `FaceEmbeddingCipher`؛ ماژول `modules/privacy/`؛ RBAC با **تست parity** (۱۳ تست استودیو + ۱۴ تست بک‌اند) و اثبات زنده‌ی ۴۰۳ (`evidence/m60/STATUS.md` R3).
- `deploy_gate.py`: ۹ بررسی ایستا (که یک باگ واقعی پیدا کرد: `MP_JWT_SECRET` → `MP_SECRET_KEY`).
- Electron: `contextIsolation: true`, `nodeIntegration: false` در `mp-app/studio/electron/main.cjs`.

**DAST و انتشار**
- `mp-app/backend/scripts/dast.py` با **schemathesis** روی OpenAPI خودِ اپ؛ شاهد: `evidence/m60/dast.json` → **۱۲۸ عملیات، ۱۰۲۴ کیس، ۰ یافته، ۰ پاسخ 2xx بدون احراز هویت**. (عمداً خارج از pytest تا CI غیرقطعی نشود.)
- `apk.yml`: بیلد `--split-per-abi` + SHA256 + **ممیزی عمیق با apktool** (شاهد: `evidence/m60/res-*.json` برای ۳ ABI، ۴۷۳ فایل، `coverage: complete`).
- `web.yml`: بیلد وب Flutter با analyze/test/build + آرتیفکت `muscleparadise-web` + دیاگنوستیک شکست.
- `container.yml` + `deploy.yml`: push به GHCR با تگ full‑SHA → Dokploy با **readiness gate** → `rollback` با تگ صریح و readiness gate.
- `client-format-fix.yml`: اصلاح خودکار فرمت + PR، با `concurrency` و `cancel-in-progress`.

**کیفیت UI و بار**
- `qa-report/FINAL-REPORT.md`: مرور ۱۱ صفحه با Chromium بی‌سر (`@sparticuz/chromium`) → **۰ خطای کنسول، ۰ پاسخ 4xx/5xx، ۰ استثنای صفحه، ۰ سرریز افقی**؛ **۱۰۱ دکمه‌ی یکتا شناسایی و ۴۵ مورد کلیک شد** (`qa-report/buttons.json`) با ۰ خطا.
- انیمیشن با framer-motion و **احترام به `prefers-reduced-motion`**.
- Locust با ۲۰۰ کاربر همزمان: ۱۰٬۸۴۷ درخواست، **۰٪ خطا**، p50=38ms، **p95=210ms**، p99=330ms (`qa-report/load/locust_stats*.csv`، نمودار `qa-report/graphs/load-latency-200users.png`).
- `mp-app/tests/load/k6-gate.js` با SLO `p(95)<2000ms` و `errors<0.05`.

**داده و معماری**
- پول به‌درستی **عدد صحیح ریال** است: `amount_rial`, `price_rial`, `unit_price_rial`, `total_rial`, `discount_rial`, `payments_total_rial`, `expenses_total_rial` همگی `Mapped[int] = mapped_column(Integer)`؛ `Numeric: 0`, `BigInteger: 0`, و `Float: 11` فقط برای اندازه‌گیری‌ها (`grams`, `weight_kg`, `score`, `percentile`, `raw_value`, `sdc`). **هیچ پول شناوری وجود ندارد.**
- زمان: **صفر `datetime.now()` naive**؛ ۱۵ ارجاع به `zoneinfo`/`Asia/Tehran`/`timezone.utc`؛ ۲۵ فایل با منطق جلالی.
- SQLite سخت‌شده در `db/base.py`: `journal_mode=WAL`, `synchronous=NORMAL`, `busy_timeout=15000`, `foreign_keys=ON`.
- Alembic + تست‌های drift/بکاپ: `test_migrations.py`, `test_m47_migration_drift.py`, `test_m97_migrations_and_backup.py`, `test_backup_drill.py`, `tests/unit/test_backup.py`.
- ۲۴ ماژول بک‌اند شامل `payments`, `expenses`, `shop`, `membership`, `face_id`, `privacy`, `outbox`, `notification`, `reporting`, `population`, `updates` و ۱۹ موتور در `engine/`.
- تست‌های مالی: `test_payments_deep.py`, `test_m83_wallet_ledger.py`, `test_g2_coupons.py`, `test_classes_finance.py`, `test_m59_shop.py`, `test_phase6c_expenses.py`, `test_qf06_expense_receipt.py`.
- `NOTICE-THIRD-PARTY.md` **دقیق و با شاهد**: `yuhonas/free-exercise-db` با **The Unlicense** + commit `f00c92c` + sha256 + `SOURCE.md`؛ و `REA skill` با MIT + commit `bb5278c`.
- `docs/MuscleParadise/` با ۱۶۷ سند شامل ADRها، `architecture/c4.md`, `module-map.md`, خروجی‌های **RepoWise**، `OWNER-DECISIONS.md`, `OPS-RUNBOOK.md`, `PLAN-CLOUD-PRODUCTION.md`, `DATA-RETENTION.md`.

### ۴‑ب) موارد بسته‌شده از زمان ممیزی قبلی (`e6fa0a9`) — دوباره انجام نده

| مورد در نسخه‌ی ۱ | وضعیت امروز | شاهد |
|---|---|---|
| fallback امضای release به کلید debug | **بسته شد** | `build.gradle.kts:34-49` — env var + PKCS12، بدون fallback |
| نبودِ پین نسخه‌ی SDK و drift | **بسته شد** | job `client-pinned` با `flutter-version: "3.50.0"` + بررسی انطباق با devcontainer + گیت `dart format` |
| نبودِ بیلد وب | **بسته شد** | `web.yml` (analyze/test/build/artifact/diagnostics) |
| `strict` نبودن TypeScript استودیو | **بسته شد** | `tsconfig.json:14` → `"strict": true`؛ **`: any` = ۰** در `src/` |
| ۳۶ کد stub/نیمه‌تمام | **بسته شد** | شمارش امروز = **۰** |
| نبودِ DAST | **بسته شد** | `scripts/dast.py` + `evidence/m60/dast.json` (۱۰۲۴ کیس، ۰ یافته) |
| نبودِ ممیزی عمیق APK | **بسته شد** | `apk.yml` → apktool؛ `evidence/m60/res-*.json` (۳ ABI، ۴۷۳ فایل) |
| نبودِ provenance برای دارایی ثالث | **بسته شد** | `NOTICE-THIRD-PARTY.md` + `data/external/free_exercise_db/SOURCE.md` |
| سنگینی مخزن (`.claude/` با ۹۳۱ فایل) | **بسته شد** | فایل‌های ترک‌شده ۱۶۷۸ → **۱۱۴۷** |
| نبودِ سرچشمه‌ی معماری/بهداشت کد | **بسته شد** | RepoWise در `docs/MuscleParadise/architecture/` و `BUILDER-START-AND-REPOWISE.md` |
| نبودِ اتوماسیون فرمت/اثرانگشت | **بسته شد** | `client-format-fix.yml`, `gitleaks-fingerprints.yml`, `tools/mermaid-check` |

### ۴‑پ) نقص‌های بازِ ثبت‌شده توسط QA خودتان (باید بسته شوند)

از `qa-report/FINAL-REPORT.md`:
1. **قفل‌شدگی استخر اتصال SQLite** (`QueuePool` ظرفیت ۴۰+۲۰، `pool_timeout=5s`) → همه‌ی درخواست‌ها timeout و سرور تا ریستارت قفل؛ **غیرقابل بازتولید، علت ریشه‌ای ثابت نشده**؛ تعداد fd ثابت (۱۱۸). ← **WP‑01**
2. بنر به‌روزرسانی روی محتوای صفحه می‌افتد (نمایشی). ← **WP‑09**
3. ایموجی ❤️/💚 در فوتر به‌صورت جعبه رندر می‌شود (فونت). ← **WP‑15**
4. `nutrition/food-logs/member/-1/daily` با شناسه‌ی `−1` → پاسخ **200 با مقدار placeholder** (باید 404/422 باشد). ← **WP‑10**
5. دکمه‌های مالی/مخرب در مرورگر کلیک نشدند (`BLOCKED` — نیاز به محیط و داده‌ی جدا). ← **WP‑12/WP‑11** با محیط ایزوله
6. `JADX` مسدود (هیچ JDK در محیط نیست؛ `jdk4py` فقط JRE است). ← **BLOCKED** بماند و ثبت شود

### ۴‑ت) نقص‌های تازه‌ی راستی‌آزمایی‌شده در کد (۲۰۲۶‑۱۱‑۲۰) — در هیچ سند پروژه‌ای نبودند

اینها را مستقیماً در کد تأیید کردم؛ منبعشان نه `PROJECT-HANDOFF.md` است نه `qa-report/`:

| # | نقص | شاهد خط‌به‌خط | WP |
|---|---|---|---|
| A2 | `GET /api/v1/metrics` **بدون هیچ گاردی** و از اینترنت قابل scrape (نرخ درخواست، تأخیر، شمار خطا، عمق صف outbox، وضعیت worker)؛ ضمناً هر scrape یک session جدید DB باز می‌کند و به فشار A1 اضافه می‌کند | `mp-app/backend/api/v1/monitoring.py:14` (بدون dependency) · `api/routes.json` guard=`—` · `mp-app/infra/Caddyfile` → `handle /api/* { reverse_proxy backend:8000 }` | **WP‑22** |
| A3 | `MP_TRUSTED_PROXIES` پیش‌فرض خالی و در production **اعتبارسنجی نمی‌شود** ⇒ پشت Caddy همه‌ی کاربران یک سبد rate-limit مشترک (`otp_rate_limit=10/minute` برای **کل باشگاه** = قفل دسته‌جمعی ورود در ساعت اوج) | `app/config.py:69` · `app/security/proxy.py:12-13` · `modules/auth/router.py:32-38` · `validate_production_configuration` → `trusted_proxies` ۰ بار | **WP‑22** |
| B17 | `MP_REQUIRE_WORKER=False` و `worker_ok = True` پیش‌فرض ⇒ اگر worker اجرا نشود صف `outbox` و `dead_letters` بی‌صدا رشد می‌کنند ولی `/health/ready` **سبز** می‌ماند و Dokploy ترافیک را قطع نمی‌کند | `app/config.py:71` · `api/v1/monitoring.py:61` → `if settings.require_worker:` | **WP‑22** |
| B18 | `MP_DATABASE_URL` در production اعتبارسنجی نمی‌شود (در برابر Valkey که loopback بودنش رد می‌شود) ⇒ production می‌تواند بی‌صدا روی SQLite بماند و ADR‑002 باز بماند | `validate_production_configuration` → `database_url` ۰ بار · `PROJECT-HANDOFF.md` §۱۳ | **WP‑22** |
| B2 | گارد مجوز **تکراری**: هم روی روتر و هم روی پارامتر endpoint ⇒ دو بار ارزیابی در یک درخواست (خواسته‌ی ۹: کد روی کد) | `modules/axis_assessment/router.py:14-17` و خط ۴۹ · `routes.json` guard=`permission, permission` · شمارش: `classes/router.py`=۴، `axis_assessment`=۲، بقیه=۱ | **WP‑25** |
| B3 | استودیو شناسه‌ی sentinel `1-` را به API می‌فرستد و سرور **۲۰۰ با placeholder** برمی‌گرداند (باید ۴۲۲/۴۰۴) | `mp-app/studio/src/pages/Nutrition.tsx:50` → `fetchDailyNutrition(memberId ?? -1, …)` · `qa-report/FINAL-REPORT.md` §۳ | **WP‑25** (+WP‑10) |
| B1 | **کیوسک وجود ندارد** ولی مستند و تصویر تبلیغش می‌کنند: استودیو ۱۲ صفحه دارد و هیچ‌کدام کیوسک نیست؛ `kiosk` در کل مخزن ۱۰ ارجاع (در استودیو فقط `src/lib/update.ts`) | `PROJECT-HANDOFF.md` §۸ و §۱۳ · `docs/MuscleParadise/ui-previews/03-kiosk-face-gate.png` (۱٫۷MB) | **WP‑23** |
| B13 | وابستگی **اعلام‌نشده**: `hypothesis` در `dast.py` import می‌شود ولی در dev extra نیست ⇒ DAST روی محیط تازه می‌شکند؛ و `dast.py` به هیچ job زمان‌بند وصل نیست | `mp-app/backend/scripts/dast.py:89` · dev deps در `pyproject.toml` | **WP‑08** |
| B19 | سه `except Exception: pass` بی‌صدا در مسیر مانیتورینگ (مجموع بک‌اند ۱۱ → ۲۲) | `api/v1/monitoring.py` (۳ مورد با `# noqa: BLE001`) | **WP‑19** |

**۸ نقص خودِ سند تحویل (D1–D8) ← همه در WP‑24:** D1 جدول مجوزها (§۷) **خالی** چاپ شده در حالی که `app/security/grants.py:34` → `KNOWN_PERMISSIONS` پنج کلید دارد (`finance.write`, `finance.read`, `reports.confidential`, `roles.manage`, `flags.write`) · D2 پیش‌فرض `MP_CORS_ORIGINS` به‌صورت «(» (رشته‌ی چندخطی در `app/config.py:79`) · D3 §۱۳ می‌گوید «`web.yml` و `apk.yml` فقط `workflow_dispatch`» ولی `apk.yml` روی `push: tags:["v*"]` هم اجرا می‌شود و §۱۰ همان سند درست نوشته (**تناقض داخلی**) · D4 §۲ می‌گوید پیشوندهای بی‌پوشه «در `api/` یا `app/`» هستند ولی روتر `face` در `modules/face_id/router.py` است (فقط پیشوند با نام پوشه فرق دارد) · D5 سند روی شاخه‌ی مرج‌نشده و `scripts/repowise_handoff.py --check` به هیچ گیت CI وصل نیست · D6 §۱۱ مسیر اسکرین‌شات‌ها را `docs/MuscleParadise/screenshots/` می‌گوید؛ واقعی `qa-report/screenshots/` است · D7 اختلاف اعداد بین سه snapshot (`b194e96`, `e5c8891`, `c06e353`) بدون تعیین سند معتبر (۲۷۳ در برابر ۲۷۶ لینک؛ بدترین فایل `Shop.tsx` در برابر بی‌نام) · D8 جدول §۲ ناقص (۲۳ ردیف برای ۲۴ پوشه) و «۰ مسیر API هم‌نام» برای `face_id`/`notification`/`membership` گمراه‌کننده است.

**راستی‌آزمایی کردم و سالم بودند** (تا اشتباهی «رفع» نشوند): اعتبارسنجی production واقعاً قوی است (`app/config.py:127-243`: حداقل بایت `MP_SECRET_KEY` و رد `DEFAULT_DEV_SECRET`/`change-me`/`example`؛ `MP_BIOMETRIC_KEY` الزامی + Base64 + **دقیقاً ۳۲ بایت** + **جدا از `MP_SECRET_KEY`**؛ `MP_SMS_PROVIDER=dev` ممنوع + فیلدهای اجباری هر provider + HTTPS بدون credential؛ Valkey غیر‑loopback؛ CORS بدون `*` و فقط HTTPS؛ `gateway=mock|sandbox` در production ممنوع؛ `manual`+`sandbox=true` رد) · `app/security/proxy.py` پارس XFF را fail-safe پیاده کرده (فقط تنظیمش در production اجباری نشده) · `modules/face_id/service.py:148-162` مالکیت را با `ensure_member_scope` + `audit` رعایت می‌کند · Electron پایه‌ی امن دارد (`contextIsolation:true`, `nodeIntegration:false`) · پول همه‌جا `Integer` ریال است · صفر `datetime.now()` naive · گیت‌های `interaction_map.py --check` و `docs_gate.py` پاس.

---

## ۵) اعداد پایه‌ی امروز (کامیت `662ff88`) — مبنای گیت ضد‌رگرسیون

این جدول را در `.ci-baseline.json` (یا معادل) commit کن. هر گیت ضد‌رگرسیون باید **فقط کاهش** را بپذیرد.

| سنجه | مقدار امروز | روند نسبت به `e6fa0a9` |
|---|---|---|
| فایل‌های ترک‌شده | ۱۱۴۷ | ↓ (از ۱۶۷۸) ✅ |
| تست‌های بک‌اند (فایل) | ۱۴۴ | ↑ (از ۱۱۸) ✅ |
| پوشش بک‌اند | ۹۴٫۲۸٪ (گیت ۷۰٪) | ✅ |
| تست‌های استودیو | ۲۸۲ پاس / ۹ skip | — |
| تست‌های کلاینت (فایل) | ۲۹ | ↑ (از ۲۸) |
| golden تست کلاینت (`matchesGoldenFile`) | **۰** | بدون تغییر ❌ |
| `integration_test` / patrol کلاینت | **۰ / ۰** | بدون تغییر ❌ |
| فایل‌های دارای `Semantics` در `client/lib` | **۳** | بدون تغییر ❌ |
| `dynamic` در `client/lib` | **۱۹۷** | بدون تغییر ❌ |
| کست `as` در `client/lib` | **۱۹۲** | ↑ جزئی (از ۱۹۱) ❌ |
| `// ignore` در `client/lib` | ۰ | ✅ |
| `: any` در `studio/src` | **۰** | ✅ |
| `strict` در tsconfig استودیو | true | ✅ |
| فایل‌های l10n/ARB/intl | **۰** | بدون تغییر ❌ |
| آستانه‌ی پوشش کلاینت | **ندارد** (فقط جمع‌آوری) | ❌ |
| `print()` در کد غیرتست بک‌اند | **۴۱** | بدون تغییر ❌ |
| `except Exception` در بک‌اند | **۲۲** | ↑ (از ۱۱) ⚠️ |
| `TODO/FIXME/HACK` در `mp-app` | **۴۸** | ↑ (از ۴۲) ⚠️ |
| تست‌های skip/disabled | **۶** | ↑ (از ۲) ⚠️ |
| stub / `NotImplementedError` | **۰** | ↓ (از ۳۶) ✅ |
| ابزار mutation | **۰** | بدون تغییر ❌ |
| تست property (دایرکتوری/فایل) | **۰** (فقط `dast.py` از hypothesis استفاده می‌کند) | ❌ |
| `hypothesis` در dev deps | **اعلام نشده** ⚠️ | — |
| گیت‌های زنجیره‌ی تأمین آرتیفکت (sbom/trivy/grype/hadolint/cosign/codeql/dependency-review) | **۰** | بدون تغییر ❌ |
| گزارش خطا/crash (sentry/glitchtip/rollbar/bugsnag) | **۰** | بدون تغییر ❌ |
| `Content-Security-Policy` (Caddyfile و `security/headers.py`) | **۰** | ❌ |
| `openapi.json` ترک‌شده / گیت oasdiff | **۰ / ۰** | بدون تغییر ❌ |
| ابزار آشوب (toxiproxy/respx/vcrpy) | **۰** | بدون تغییر ❌ |
| سناریوهای k6 (اندپوینت) | **۲** | بدون تغییر ❌ |
| `isMinifyEnabled` / `isShrinkResources` / `.aab` | **۰ / ۰ / ۰** | بدون تغییر ❌ |
| `npm ci \|\| npm install` | **۲ مورد** (`ci.yml:178`, `ci.yml:392`) | بدون تغییر ❌ |
| ESLint در devDeps استودیو / فایل کانفیگ | **۰ / ۰** (اسکریپت `lint` مرده است) | ❌ |
| `mp.db` ترک‌شده در ریشه | **۱ فایل ۸۶۴KB، ۵۲ جدول، همه خالی (۰ سطر)** | جدید ⚠️ |
| آیتم‌های باز `RELEASE-CHECKLIST.md` | **۲۱ باز / ۱۹ انجام** | ⚠️ |
| قوانین Semgrep | ۱ فایل (`project-rules.yml`) | — |
| گارد `/api/v1/metrics` | **هیچ** — از اینترنت قابل scrape | جدید ❌ |
| `MP_TRUSTED_PROXIES` پیش‌فرض / چک در production | `""` / **۰ بار** | جدید ❌ |
| مشاهده‌پذیری استخر اتصال (`pool_size`/`checkedout`/`overflow`/`QueuePool`) | **۰** ارجاع در `app/` و `api/` | جدید ❌ |
| `MP_REQUIRE_WORKER` پیش‌فرض / چک در production | `False` / **۰ بار** | جدید ❌ |
| `MP_DATABASE_URL` چک در production | **۰ بار** | جدید ❌ |
| صفحه‌ی کیوسک در استودیو | **۰** (از ۱۲ صفحه) | جدید ❌ |
| گارد تکراری `require_permission` | `classes/router.py`=۴، `axis_assessment/router.py`=۲ | جدید ❌ |
| شناسه‌ی sentinel `1-` در استودیو | ≥۱ مورد (`Nutrition.tsx:50`) | جدید ❌ |
| `except Exception` در `api/v1/monitoring.py` | **۳** (بی‌صدا) | جدید ⚠️ |
| یافته‌ی سلامت RepoWise (`e5c8891`) | **۶۷۰** (۲۵ critical، ۷۰ high، ۴۱۶ medium، ۱۵۹ low) · میانگین ۹٫۲۶ · بدترین `studio/src/pages/Shop.tsx`=۶٫۰ | — |
| کد مرده RepoWise | **۳۵** (۲۹ `unused_export` + ۶ `unreachable_file`)، ۲ مورد اطمینان بالا | — |
| رانش مستندات RepoWise | **۲۵** مورد در ۱۴ سند (از ۲۰۲ سند / ۴٬۰۴۸ ارجاع) | — |
| نقص در سند تحویل تازه | **۸** مورد (D1–D8) | جدید ❌ |

---

## ۶) بسته‌های کاری

> **P0** = مانع انتشار · **P1** = عمق کیفیت · **P2** = کلاس جهانی. شماره‌ی WP را در پیام کامیت بیاور.

### WP‑00 · صف و راستی‌آزمایی — P0
**چرا:** بدون صفِ راستی‌آزمایی‌شده، کار تکراری و ترتیب غلط می‌شود.
**شاهد:** بخش ۵ این سند (اعداد `662ff88`).
**کار:**
1. `git status --short --branch` و HEAD را ثبت کن؛ اختلاف با `662ff88` را فهرست کن.
2. هر ۲۱ آیتم بازِ `docs/MuscleParadise/RELEASE-CHECKLIST.md` را به سه دسته تقسیم کن: **(a)** ایجنت می‌تواند انجام دهد، **(b)** نیاز به secret/دستگاه واقعی/production دارد → `BLOCKED` با دلیل دقیق، **(c)** فقط مالک می‌تواند (تنظیمات GitHub، چرخش کلید).
3. همه‌ی اعداد بخش ۵ را دوباره اندازه بگیر و در `docs/MuscleParadise/AUDIT-FINAL-2026-11-20.md` به‌عنوان «عدد پایه‌ی راستی‌آزمایی‌شده» ثبت کن.
4. صف اجرایی بساز: WP‑01…WP‑21 با اولویت، وابستگی، و ستون وضعیت.
5. `python3 scripts/docs_gate.py` و `tools/mermaid-check` را سبز کن.
**معیار پذیرش:** سند صف commit شده؛ هر ۲۱ آیتم چک‌لیست دسته‌بندی شده؛ اعداد پایه راستی‌آزمایی شده؛ docs_gate سبز.

---

### WP‑01 · ریشه‌یابی و رفع قفل‌شدگی استخر اتصال — P0 · بحرانی‌ترین مورد
**چرا:** یک حادثه‌ی **قفل‌شدگی کامل سرور** در تست بار ثبت شده که تا ریستارت ادامه داشته و علتش ثابت نشده. در production یعنی باشگاه خاموش می‌شود. این تنها موردی است که می‌تواند همه‌ی بقیه را بی‌ارزش کند.
**شاهد:** `qa-report/FINAL-REPORT.md` بخش ۵ — «استخر اتصال SQLite (`QueuePool` با ظرفیت ۴۰+۲۰) پر شد و تمام درخواست‌ها timeout گرفتند (`pool_timeout=5s`). سرور تا ریستارت قفل ماند… **علت ریشه‌ای ثابت نشده است**»؛ اجرای ۲ = ۰ درخواست؛ fd ثابت ۱۱۸. `db/base.py` → WAL + `busy_timeout=15000`. ADR‑002 = SQLite با مسیر مهاجرت به Postgres.
**کار:**
1. **مشاهده‌پذیری استخر (اول از همه، چون بدون آن ریشه‌یابی ممکن نیست):** متریک‌های `pool_size`, `checked_out`, `overflow`, `wait_time`, `timeout_count` را با event listenerهای SQLAlchemy (`checkout`/`checkin`/`connect`) به Prometheus موجود (`mp-app/infra/monitoring/prometheus.yml`) اضافه کن + alert در `alerts.yml` روی «اشباع استخر» و «افزایش checkout بدون checkin».
2. **نشت نشست را پیدا کن:** یک تست/اسکریپت تشخیصی بنویس که پس از هر درخواست تعداد sessionهای باز را بشمارد؛ middleware یا dependency ای که session را در مسیر استثنا/پاسخ جریان‌دار (streaming/SSE)/پس‌زمینه (`jobs/`, `outbox/`) باز نگه می‌دارد، شناسایی کن. مظنون‌های اول: مسیرهای AI/چت، `outbox`، `jobs`، هر ژنراتور/`BackgroundTask` که بعد از پاسخ DB نگه می‌دارد.
3. **هارنس بازتولید:** یک اسکریپت بار موازی بنویس (Locust موجود یا k6) با ترکیب: نوشتن‌های همزمان + تراکنش‌های طولانی + مسیر AI + قطع ناگهانی کلاینت (connection reset وسط درخواست) + checkpoint WAL. هدف: **بازتولید قطعی** حادثه، نه تصادفی.
4. **سخت‌سازی:** `pool_timeout` را از ۵s به مقدار منطقی + **fail fast با پاسخ ۵۰۳ قابل بازیابی** عوض کن (نه hang)؛ `pool_recycle`؛ سقف `max_overflow`؛ statement/lock timeout؛ و یک **watchdog** که اشباع پایدار را گزارش و در صورت نیاز worker را بازیابی کند.
5. **تصمیم معماری را با شاهد ببند:** ADR‑002 را با نتیجه‌ی بارِ Postgres به‌روز کن — یک job CI (یا دستور مستند) که همان سناریوی بار را روی **Postgres** اجرا کند و اعداد را کنار SQLite بگذارد. اگر production روی SQLite می‌ماند، شرایط و سقف‌هایش را صریح در `PLAN-CLOUD-PRODUCTION.md` بنویس.
6. **رفتار زیر فشار را تست کن:** وقتی DB قفل/پر است، `/api/v1/health/ready` باید **غیرسبز** شود تا Caddy/Dokploy ترافیک را قطع کند و `rollback` عمل کند؛ این را با تست اثبات کن.
**معیار پذیرش:** متریک‌های استخر در Prometheus + alert فعال؛ نشتی جلسه **پیدا و رفع** شده با تست بازتولید (قبل/بعد)؛ هارس بازتولید commit شده؛ پاسخ ۵۰۳ fail-fast به‌جای hang؛ `health/ready` زیر فشار قرمز می‌شود (تست)؛ ADR‑002 با اعداد Postgres به‌روز؛ یک گزارش `finn/reports/…` با عدد p95/p99 قبل و بعد. اگر ریشه پیدا نشد: `BLOCKED` صریح با فهرست مظنون‌های رد‌شده و شاهد هرکدام — **بدون ادعای رفع**.

---

### WP‑02 · زنجیره‌ی تأمین آرتیفکت — P0
**چرا:** گیت‌های سطح کد عالی‌اند (Gitleaks/bandit/pip-audit/Semgrep/npm audit) ولی **آرتیفکت** بی‌دروازه است، در حالی که ایمیج‌ها به GHCR می‌روند و با Dokploy deploy می‌شوند.
**شاهد:** grep روی کل `.github/workflows/` برای `sbom|trivy|grype|hadolint|cosign|syft|dependency-review|codeql|zap|oasdiff` → **۰ نتیجه**. `container.yml` بیلد و push می‌کند؛ `deploy.yml` همان تگ SHA را deploy می‌کند.
**کار:**
1. job `artifact-scan` اضافه کن: **hadolint** روی `mp-app/backend/Dockerfile` و `mp-app/infra/Dockerfile.backend` و `mp-app/studio/Dockerfile`.
2. **Trivy** (یا Grype) روی هر ایمیج ساخته‌شده با گیت صریح `CRITICAL,HIGH --exit-code 1` (بدون `|| true`) و آپلود گزارش.
3. **SBOM** CycloneDX برای هر ایمیج + آرتیفکت نسخه‌دار؛ و یک job **زمان‌بند هفتگی** که SBOM را دوباره اسکن کند تا CVEهای پس از انتشار هم دیده شوند.
4. **cosign**: امضا + SLSA provenance با `GITHUB_TOKEN`؛ و در `deploy.yml` یک مرحله‌ی **verify قبل از Dokploy** تا فقط ایمیج امضاشده deploy شود.
5. `actions/dependency-review-action` روی `pull_request`.
**معیار پذیرش:** هر بیلد ایمیج: lint + CVE + SBOM + امضا دارد؛ یک CVE بحرانی بیلد را قرمز می‌کند؛ `deploy.yml` بدون attestation معتبر deploy نمی‌کند؛ job هفتگی فعال.
**ابزار:** `aquasecurity/trivy` (Apache‑2.0، ⭐39.5k) · `anchore/grype` (Apache‑2.0، ⭐13.3k) · `anchore/sbom-action` (Apache‑2.0) · `hadolint/hadolint` (GPL‑3.0، dev) · `sigstore/cosign` (Apache‑2.0، ⭐6.4k).

---

### WP‑03 · گزارش خطای زمان اجرا + CSP — P0
**چرا:** هیچ crash/error tracking نیست؛ با وجود یک حادثه‌ی قفل‌شدگیِ **غیرقابل بازتولید**، این بزرگ‌ترین کوری عملیاتی است. ضمناً تنها هدر امنیتیِ غایب، CSP است.
**شاهد:** grep برای `sentry|glitchtip|rollbar|bugsnag` در `mp-app` → **۰**. هدرهای موجود در `app/security/headers.py` و `Caddyfile` کامل‌اند **به‌جز `Content-Security-Policy`**. استودیو PWA است (`public/sw.js`, `manifest.webmanifest`) و کیوسک/وب هم دارد.
**کار:**
1. **GlitchTip** self‑host را به `mp-app/infra/docker-compose.yml` و `ansible/playbook.yml` اضافه کن (کنار Prometheus موجود).
2. بک‌اند: SDK + `release=git SHA` + `environment` + اتصال به `request_id` موجود + `before_send` برای **redaction** (موبایل، نام، embedding چهره، داده‌ی کارت).
3. کلاینت Flutter و استودیو (وب + Electron): گزارش خطا با همان DSN؛ در کلاینت **رضایت و سیاست حریم خصوصی** مطابق `FACEID-PRIVACY-TEXT.md` و `biometric-policy.md`.
4. **تست redaction**: payload ارسالی نباید هیچ PII واقعی داشته باشد (تست واحد روی تابع redact + یک نمونه‌ی anonymized در `evidence/`).
5. **CSP** را به `app/security/headers.py` و `Caddyfile` اضافه کن (سیاست سخت‌گیرانه برای SPA/PWA: `default-src 'self'`، `img-src` شامل `data:`/`blob:` برای GIF حرکات، `connect-src` برای API، و `script-src` بدون `unsafe-inline` در صورت امکان) + **تست** که صفحه با CSP واقعی کار می‌کند (نه فقط هدر وجود دارد).
6. `alerts.yml` را با «رشد نرخ خطای جدید» گسترش بده و در `OPS-RUNBOOK.md` یک بخش triage اضافه کن.
**معیار پذیرش:** خطای عمدی در staging به GlitchTip می‌رسد با SHA و محیط؛ تست redaction سبز؛ CSP در لبه و در اپ فعال و **با تست مرورگری تأیید شده**؛ runbook به‌روز.
**ابزار:** `burke-software/GlitchTip` (MIT، self‑host).

---

### WP‑04 · بستن ۲۱ آیتم بازِ `RELEASE-CHECKLIST.md` — P0
**چرا:** خودِ پروژه فهرست آماده‌سازی انتشار دارد و **۲۱ مورد باز** است؛ این‌ها تعریف «آماده‌ی انتشار» هستند.
**شاهد:** `docs/MuscleParadise/RELEASE-CHECKLIST.md` → ۲۱ `[ ]` در برابر ۱۹ `[x]`. نمونه‌های باز: خط ۱۲ (چرخش کلید signing افشاشده)، ۱۳ (Gitleaks روی کل history بدون baseline/allowlist پنهان)، ۱۴ (`.env` production با کلید JWT و کلید بیومتریک **مجزای ۳۲ بایتی**، CORS/TLS، secret manager)، ۱۵ (SMS واقعی/HTTPS و سیاست merchant/sandbox پرداخت؛ **`dev_code` و gateway mock در production ممنوع**)، ۱۶ (Valkey سالم، `health/ready` سبز، **rate-limit storage مشترک بین workerها**)، ۱۷ (`alembic upgrade head` روی scratch و روی clone امن backup + بررسی duplicate gateway authority)، ۱۸ (backup از `/data/mp.db` + **restore drill** + نسخه‌ی رمزنگاری‌شده‌ی خارج از میزبان)، ۱۹ (Prometheus/exporter/alerts دیده شوند + **Alertmanager با test notification**)، ۲۰ (تمرین واقعی push/deploy/rollback روی staging)، ۲۵‑۳۲ (تأییدیه‌های REA روی APK: شناسایی بیلد، امضای v1/v2/v3، عدم افشای source map/debug symbol/credential، هم‌خوانی `versionName` با تگ، `INTERNET` و `networkSecurityConfig` در مانیفست **release**، `android:debuggable="false"`، `ApiClient` فقط loopback/RFC1918 با HTTP، گزارش `rea/<date>-REA-GAP-CLOSURE.md`)، ۳۵‑۳۸ (بهداشت شاخه‌ها).
**کار:**
1. هر ۲۱ مورد را طبق WP‑00 دسته‌بندی کن: (a) انجام‌دادنی، (b) `BLOCKED` با دلیل دقیق، (c) فقط مالک.
2. موارد (a) را **با شاهد** ببند: مثلاً گیت CI که `dev_code`/gateway mock را در پیکربندی production رد کند؛ تست اینکه `networkSecurityConfig` و `INTERNET` در مانیفست release حاضرند؛ تست `ApiClient` برای loopback/RFC1918؛ اسکریپت restore drill که **برابری داده‌ها** را assert کند (نه فقط وجود فایل)؛ بررسی Alertmanager با ارسال test notification و ثبت رسید.
3. موارد (b) را در یک فایل `docs/MuscleParadise/RELEASE-BLOCKED-2026-11-20.md` با دلیل، پیش‌نیاز دقیق، و دستور آماده‌ی اجرا برای مالک بنویس.
4. موارد (c) را در همان فایل به‌عنوان «اقدام مالک» با دستور دقیق بیاور (بخش ۸ را ببین).
**معیار پذیرش:** صفر آیتم بازِ «انجام‌دادنی»؛ هر `BLOCKED` با دلیل و پیش‌نیاز دقیق؛ چک‌لیست به‌روز با شاهد (لینک CI run یا مسیر `evidence/`) برای هر بسته.

---

### WP‑05 · بهداشت مخزن: `mp.db` و فایل‌های ناخواسته — P0
**چرا:** یک فایل دیتابیس ۸۶۴KB در ریشه‌ی مخزن ترک‌شده است. امروز **خالی است** (۵۲ جدول، همه ۰ سطر) پس نشتی داده نیست — ولی یک تصادف تا commit شدن داده‌ی واقعی عضو/چهره/پرداخت فاصله دارد.
**شاهد:** `mp.db` در ریشه (۸۶۴KB)؛ `.gitignore:63-65` فقط `mp-app/backend/*.db`, `*.db-shm`, `*.db-wal` را می‌پوشد، **نه ریشه را**. بزرگ‌ترین فایل‌های ترک‌شده: `docs/MuscleParadise/ui-previews/07-client-home-grid.png` (۲٫۱MB) و ۷ تصویر دیگر، `data/external/free_exercise_db/exercises.json` (۹۸۴KB).
**کار:**
1. `git rm --cached mp.db` + افزودن `/mp.db`, `*.db`, `*.db-shm`, `*.db-wal` (بدون محدودسازی به یک پوشه) به `.gitignore`.
2. **گیت CI** اضافه کن: هیچ فایل با پسوند `.db/.sqlite/.db-wal/.p12/.keystore/.jks/.env` نباید ترک‌شده باشد؛ و اگر `mp.db` دید شد، **تعداد سطرهای جداول حساس** (`users`, `members`, `face_templates`, `payments`, `otp_codes`, `biometric_consents`, `audit_logs`) شمرده و در صورت غیرصفر بودن، بیلد قرمز شود (بدون چاپ محتوای داده).
3. تصاویر بزرگ را با `mp-app/infra/scripts/compress-media.sh` موجود بهینه کن یا به Git LFS ببر؛ اندازه‌ی مخزن را ثبت کن.
4. `.gitignore` را برای خروجی ابزارهای ممیزی (`.audit/`, `build/`, `reports/`) و آرتیفکت‌های محلی کامل کن.
**معیار پذیرش:** `mp.db` از ایندکس خارج و ignore شده؛ گیت CI فعال و سبز؛ اندازه‌ی مخزن کاهش یافته و ثبت شده.

---

### WP‑06 · انتشار Android: R8، AAB، بودجه‌ی اندازه — P0
**چرا:** امضا اصلاح شده ولی بیلد release هنوز **بدون shrinking/obfuscation** است و **`.aab` ساخته نمی‌شود** (برای Google Play لازم است).
**شاهد:** در `build.gradle.kts` هیچ `isMinifyEnabled`/`isShrinkResources`/`proguardFiles` نیست؛ grep برای `appbundle|.aab` در workflows → **۰**؛ `apk.yml` فقط `flutter build apk --release --split-per-abi`.
**کار:**
1. `release { isMinifyEnabled = true; isShrinkResources = true; proguardFiles(...) }` با قواعد سازگار با Flutter و پلاگین‌ها؛ سپس APK را با همان **apktool audit موجود** در `apk.yml` مقایسه کن که چیزی لازم حذف نشده (شاهد قبل/بعد در `evidence/`).
2. افزودن `flutter build appbundle --release` به `apk.yml` با SHA256 و آرتیفکت.
3. **گیت اندازه‌ی بیلد**: آستانه‌ی صریح برای APK (به تفکیک ABI) و AAB؛ عدد پایه از بیلد امروز + سقف ۵٪.
4. `flutter build apk --analyze-size` را به‌عنوان آرتیفکت ثبت کن.
5. `defaultConfig` را از کامنت قالب Flutter پاک کن و `versionName`/`versionCode` را با تگ ریلیز هم‌خوان کن (آیتم ۲۸ چک‌لیست).
**معیار پذیرش:** release با R8 و shrink سبز و apktool-audit شده؛ `.aab` در CI؛ گیت اندازه فعال؛ `analyze-size` به‌عنوان آرتیفکت.
**ابزار:** `bundletool`، `apksigner verify`، `apkanalyzer`، `git-filter-repo` (فقط برای WP‑04/بخش ۸).

---

### WP‑07 · تست جهش (mutation) — P1
**چرا:** پوشش ۹۴٫۲۸٪ عالی است ولی فقط «خطوط اجرا شده» را می‌سنجد. برای ۱۹ موتور عددی + مسیرهای پول و ایمنی، باید اثبات شود تست‌ها **باگ می‌گیرند**. طبق قاعده‌ی ۳‑۱۱، ریفکتور (WP‑14/WP‑21) تا سبز شدن این گیت شروع نمی‌شود.
**شاهد:** هیچ ابزار/کانفیگ mutation در مخزن نیست (`mutmut|cosmic.ray|stryker|mutation` → ۰ فایل).
**کار:**
1. بک‌اند: **mutmut** یا **cosmic-ray** را به `[project.optional-dependencies] dev` اضافه کن؛ ابتدا روی `engine/` (به‌ویژه `safety.py`, `scoring.py`, `volume.py`, `axis_prescription.py`, `autoreg.py`, `readiness.py`, `sync_lww.py`) و `modules/payments/`, `modules/expenses/`, `modules/shop/`, `security/`.
2. اسکریپت قابل تکرار (`scripts/mutation_gate.py`) که **mutation score** را گزارش کند و **آستانه‌ی پایه** را در `.ci-baseline.json` قفل کند (فقط رشد مجاز).
3. استودیو: **stryker-js** روی `src/` حیاتی (مالی، auth، فرم‌ها) با آستانه‌ی پایه.
4. جهش‌های بازمانده را فهرست کن: یا تست بنویس، یا دلیل بیاور («این جهش معنایی ندارد»).
5. job **زمان‌بند هفتگی** (نه هر PR — کند است) + گزارش در `finn/reports/`.
6. برای Dart ابزار بالغ mutation نیست → در WP‑09 **fault injection** هدفمند روی `ApiClient`، `outbox` و `engine`-مصرف‌کننده‌ها جایگزین کن و دلیل را در گزارش بنویس.
**معیار پذیرش:** mutation score اندازه‌گیری و قفل‌شده برای `engine/`، ماژول‌های مالی و `security/`؛ آستانه در اسکریپت/CI؛ فهرست بازمانده‌ها تعیین تکلیف شده؛ job هفتگی فعال.
**ابزار:** `boxed/mutmut` (BSD‑3، ⭐1.5k) · `sixty-north/cosmic-ray` (MIT) · `stryker-mutator/stryker-js` (Apache‑2.0، ⭐3.4k).

---

### WP‑08 · تست ویژگی‌محور (property‑based) + اعلام `hypothesis` — P1
**چرا:** دامنه‌ی محصول عددی/فیزیولوژیک/مالی است؛ باگ‌های واقعی در **نقض نامتغیر** و حالات لبه‌اند. ضمناً یک وابستگی **اعلام‌نشده** وجود دارد.
**شاهد:** هیچ دایرکتوری/فایل تست property نیست. `mp-app/backend/scripts/dast.py:89` → `import hypothesis.strategies as st`، ولی `hypothesis` در `[project.optional-dependencies] dev` **نیست** → روی محیط تازه، DAST می‌شکند. dev deps فعلی: setuptools, pytest, pytest-cov, pytest-asyncio, ruff, bandit, pip-audit, faker, pyyaml, Pillow.
**کار:**
1. `hypothesis` را به dev deps اضافه کن (و در مستند `dast.py` بنویس که از همین extra می‌آید) — این **باگ واقعی** است، پس اول انجامش بده.
2. `mp-app/backend/tests/property/` بساز و برای **هر ۱۹ موتور** حداقل یک property بنویس. نامتغیرهای پیشنهادی (اگر با کد ناسازگار بود، نامتغیر درست را از کد استخراج و در گزارش ثبت کن):
   - `safety.py`: هیچ خروجی‌ای پرچم ایمنی را **پایین نمی‌آورد**؛ ورودی در فهرست ممنوعه ⇒ خروجی حتماً رد/محدود. (مهم‌ترین تست پروژه.)
   - `volume.py`: حجم = Σ(ست×تکرار×وزنه)؛ ≥ ۰؛ یکنوا صعودی نسبت به هر سه عامل.
   - `scoring.py`: کران‌دار؛ قطعی (ورودی یکسان ⇒ خروجی یکسان)؛ بی‌حساسیت به فیلدهای بی‌ربط.
   - `autoreg.py`/`readiness.py`/`set_feedback.py`/`feedback_apply.py`: خروج از سقف/کف مطلق ممنوع؛ **idempotency** اعمال دوباره‌ی همان فیدبک.
   - `sync_lww.py`: **همگرایی** — هر ترتیبی از همان رویدادها ⇒ وضعیت یکسان (commutativity + idempotency)؛ هیچ نوشتن گم‌شده‌ای.
   - `catalog_sync.py`: همگام‌سازی دوطرفه داده گم نمی‌کند؛ اجرای مجدد بدون اثر جانبی.
   - `axis_prescription.py`/`axis_rules.py`/`axis_map.py`/`segmental.py`/`gender_plans.py`: پوشش کامل نگاشت؛ بدون `KeyError`/`None` غیرمنتظره.
   - `adaptive_nutrition.py`/`nutrition.py`: کالری/ماکرو منفی، NaN یا بی‌نهایت نمی‌شود؛ جمع ماکروها با کالری کل سازگار (± تلورانس صریح).
   - `churn_risk.py`: خروجی در `[0,1]`؛ یکنواختی نسبت به سیگنال‌های قطعی.
   - `reminders.py`: زمان‌ها در آینده/بازه‌ی معتبر؛ **منطقه‌ی زمانی و DST** نتیجه را نمی‌شکند (با زمان منجمد — WP‑19).
   - `workout.py`: حالت‌های نامعتبر (ست منفی، تکرار صفر، وزنه‌ی NaN) رد می‌شوند.
3. **propertyهای پولی** (مرتبط با WP‑11): جمع اجزا = کل؛ تخفیف هرگز کل را منفی یا بیشتر از ۱۰۰٪ نمی‌کند؛ گردکردن `discount_pct` **جهت ثابت و مستند** دارد؛ refund هرگز از مبلغ پرداختی بیشتر نمی‌شود؛ مانده‌ی کیف‌پول = Σ دفتر کل (با `amount_rial` مثبت/منفی مطابق کامنت `db/models` «مثبت: شارژ، منفی: برداشت»).
4. همه‌ی propertyها با `deadline=None` و `derandomize=True` (یا seed ثبت‌شده) → **قطعی**؛ سه اجرای پیاپی بدون flake.
5. استودیو: `fast-check` برای محاسبه‌های مالی/فرم‌ها/auth.
6. یک property برای **سریال‌سازی API**: هر پاسخ با schema سازگار است و round‑trip داده را عوض نمی‌کند (از همان spec که در WP‑10 commit می‌شود).
**معیار پذیرش:** ≥۱ property برای هر ۱۹ موتور + propertyهای پولی + مسیرهای حیاتی استودیو؛ همه سبز و قطعی؛ `hypothesis` در dev deps و `dast.py` روی محیط تازه اجرا می‌شود؛ هر property یک کامنت فارسی «چرا این نامتغیر» دارد.
**ابزار:** `HypothesisWorks/hypothesis` (MPL‑2.0، ⭐9.2k) · `dubzzz/fast-check` (MIT، ⭐5.3k).

---

### WP‑09 · عمق تست کلاینت Flutter: بصری، روی‌دستگاه، a11y، نوع — P1
**چرا:** استودیو عمیق تست شده (۲۸۲ تست + a11y + WCAG + QA مرورگری)، ولی **کلاینت عضو/کیوسک** نازک‌ترین لایه است؛ خواسته‌های ۷ و ۸ (انیمیشن، اینترکشن، تک‌تک دکمه‌ها) آنجا بی‌شاهدِ پایدارند.
**شاهد:** `matchesGoldenFile` = **۰ فایل**؛ `integration_test` = **۰**؛ patrol در `pubspec.yaml` = **۰**؛ `Semantics` فقط در **۳ فایل** از `lib/`؛ `analysis_options.yaml` = فقط `flutter_lints` + `prefer_const_constructors` + `prefer_final_locals` (بدون `strict-casts`/`strict-raw-types`/`strict-inference`)؛ `dynamic` = **۱۹۷**، `as` = **۱۹۲**؛ `flutter test --coverage` اجرا می‌شود ولی **هیچ آستانه‌ای ندارد** (بک‌اند ۷۰٪ دارد)؛ دو نقص بازِ QA: افتادن بنر به‌روزرسانی روی محتوا و رندر جعبه‌ای ایموجی ❤️/💚.
**کار:**
1. **Golden tests** با `matchesGoldenFile` داخلی (بدون وابستگی جدید) برای هر صفحه و هر وضعیت: `default / loading / empty / error / disabled / pressed / focus / RTL / فونت ۲۰۰٪ / dark`؛ فایل‌ها در `mp-app/client/test/goldens/` commit شوند؛ گیت CI که تفاوت golden ⇒ قرمز (`--update-goldens` فقط با کامیت جدا و صریح).
2. **آستانه‌ی پوشش کلاینت**: عدد امروز را از `flutter test --coverage` بگیر و `--cov-fail-under`-معادل (اسکریپت پارس `lcov.info`) را در `client-pinned` بگذار؛ فقط رشد مجاز.
3. **تست روی دستگاه** با **patrol**: ورود با OTP → چک‌این (کیوسک/چهره) → دیدن برنامه‌ی تمرین → ثبت ست → آفلاین/سینک (`offline_feedback_outbox_test.dart` را به جریان واقعی روی دستگاه گسترش بده). تعامل با dialogهای permission واقعی فقط با patrol ممکن است.
4. **سرشماری UI پایدار**: `qa-report/buttons.json` (۱۰۱ دکمه در ۱۱ صفحه‌ی **استودیو**) را به یک `docs/MuscleParadise/UI-INVENTORY.md` دو‌بخشی تبدیل کن: استودیو + **کلاینت**؛ ستون‌ها: شناسه، صفحه، نوع، مسیر فایل، stateها، تست widget، golden، on-device، a11y، l10n، رفتار خطا، وضعیت. هیچ ستونی خالی نماند.
5. **دسترس‌پذیری کلاینت**: `Semantics`/`semanticLabel` روی همه‌ی کنترل‌های تعاملی؛ تست با guidelineهای داخلی `flutter_test` (`androidTapTargets`, `iOSTapTargets`, `labeledTapTargets`, `textContrastGuideline`) روی **همه‌ی صفحات**؛ تست `textScaler: 2.0` بدون سرریز؛ تست صریح RTL.
6. **سخت‌گیری نوع**: فعال‌کردن `strict-casts`/`strict-raw-types`/`strict-inference` + قواعد ایمنی (`avoid_dynamic_calls`, `always_declare_return_types`, `use_build_context_synchronously`, `cancel_subscriptions`, `close_sinks`)؛ رفع **واقعی** خطاها (نه `// ignore:`)؛ گیت ضد‌رگرسیون روی تعداد `dynamic`/`as` (پایه: ۱۹۷/۱۹۲، فقط کاهش). `dart fix --apply` در کامیت جدا.
7. **دو نقص بازِ QA** را رفع کن: تداخل بنر به‌روزرسانی با محتوا (با golden قفلش کن) و جعبه‌شدن ایموجی (با WP‑15: فونت/فالبک ایموجی).
**معیار پذیرش:** golden برای همه‌ی صفحات اصلی + stateها؛ آستانه‌ی پوشش کلاینت در CI؛ ≥۱ تست patrol سبز روی امولاتور در CI؛ تست‌های a11y guideline روی همه‌ی صفحات سبز؛ strict modes فعال و عدد پایه قفل‌شده؛ `UI-INVENTORY.md` کامل بدون ستون خالی؛ دو نقص QA بسته با golden شاهد.
**ابزار:** `flutter_test` (داخلی) · `leancodepl/patrol` (Apache‑2.0، ⭐1.5k، فعال).

---

### WP‑10 · قرارداد API: spec، گیت تغییر شکننده، و ماتریس مجوز — P1
**چرا:** DAST با schemathesis عالی کار می‌کند (۱۲۸ عملیات/۱۰۲۴ کیس/۰ یافته) ولی **spec در مخزن commit نشده**، پس **تغییر شکننده** پیش از انتشار دیده نمی‌شود؛ و `live-contract` فقط **استودیو** را پوشش می‌دهد، نه کلاینت Flutter را. ضمناً یک نقص قراردادِ واقعی باز است.
**شاهد:** `git ls-files | grep -i openapi|swagger` → **۰**؛ `ci.yml` job `live-contract` فقط `mp-app/studio/tests/liveContract.test.ts` را اجرا می‌کند؛ `qa-report/FINAL-REPORT.md` → `nutrition/food-logs/member/-1/daily` با شناسه‌ی `−1` پاسخ **200 با placeholder** می‌دهد؛ `scripts/dast.py` به CI/زمان‌بند وصل نیست.
**کار:**
1. `openapi.json` را از FastAPI با اسکریپت قابل تکرار استخراج و **commit** کن؛ گیت CI: «spec commit‌شده == spec تولیدشده از کد» (ضد drift).
2. **oasdiff** به‌عنوان گیت PR: هر تغییر **breaking** بدون نسخه‌ی جدید ⇒ قرمز؛ خلاصه در step summary.
3. `live-contract` را به **کلاینت Dart** گسترش بده (یک لایه‌ی کلاینت API یا تست Dart در برابر همان API زنده با seed موجود).
4. `dast.py` را به یک job **زمان‌بند شبانه** وصل کن (خودِ اسکریپت صریحاً گفته دستی/شبانه است — همان را رسمی کن) و گزارش را در `evidence/` بگذار.
5. **ماتریس مجوز و ورودی نامعتبر**: یک تست پارامتری‌شده که برای endpointهای حساس، ترکیب {نقش × مالکیت منبع × شناسه‌ی نامعتبر} را بزند و کد وضعیت درست را assert کند — شامل **شناسه‌ی منفی/صفر/بسیار بزرگ/رشته‌ای** که باید `404`/`422` بدهد نه `200 placeholder`. این هم نقص `-1` را می‌بندد هم گیت R2 (`unauthenticated_2xx`) را پویا نگه می‌دارد.
6. سیاست نسخه‌بندی + **حداقل نسخه‌ی کلاینت پشتیبانی‌شده** + تست سازگاری کلاینت قدیمی؛ و **کلید idempotency** برای POSTهای حساس (پرداخت، چک‌این، ثبت ست، refund) — `_settle_shop_order` سه تست idempotency دارد، همان الگو را به بقیه تعمیم بده.
**معیار پذیرش:** `openapi.json` commit‌شده + گیت drift + گیت oasdiff؛ تست قرارداد زنده برای کلاینت Dart؛ `dast.py` زمان‌بند با گزارش در `evidence/`؛ ماتریس مجوز/ورودی نامعتبر سبز و نقص `-1` بسته؛ تست idempotency برای ≥۴ مسیر حساس.
**ابزار:** `oasdiff/oasdiff` (Apache‑2.0، ⭐1.5k) + `oasdiff-action` · `schemathesis` (MIT، موجود) · `Orange-OpenSource/hurl` (Apache‑2.0) · `stoplightio/prism` (Apache‑2.0).

---

### WP‑11 · یکپارچگی پول و اعداد بزرگ — P1
**چرا:** طراحی پول **درست** است (همه‌ی مبالغ `Integer` ریال، صفر `Numeric`/`Float` پولی) — پس ریسک باقی‌مانده در **مرزهای انتقال** و **قواعد گردکردن** است، و یک نمونه‌ی واقعی هم رخ داده.
**شاهد:** `db/models/*` → `amount_rial`, `price_rial`, `unit_price_rial`, `total_rial`, `discount_rial`, `payments_total_rial`, `expenses_total_rial` همه `Mapped[int]`؛ `Float` فقط برای `grams`, `weight_kg`, `score`, `percentile`, `raw_value`, `sdc`. کامیت `e56db60` → «fix(client): بیلد وب — **سقف شناسهٔ دفتر کیف‌پول 2^53-1**». تست‌های مالی موجود: `test_payments_deep`, `test_m83_wallet_ledger`, `test_g2_coupons`, `test_classes_finance`, `test_m59_shop`, `test_phase6c_expenses`, `test_qf06_expense_receipt`. منطق جلالی در ۲۵ فایل و `Asia/Tehran` در ۱۵ مورد؛ صفر `datetime.now()` naive.
**کار:**
1. **مرز ۲^۵۳−۱ را سیستماتیک ببند** (نه موردی): یک تست مرزی که برای هر فیلد پولی/شناسه‌ای که از JSON عبور می‌کند، مقادیر `2^53−2`, `2^53−1`, `2^53`, `2^63−1` را در هر سه لایه (Python → JSON → Dart و TypeScript) round‑trip کند و **برابری دقیق** را assert کند. اگر مسیری از `Number` JS عبور می‌کند، یا سریال‌سازی رشته‌ای کن یا سقف صریح + خطای خوانا بگذار (الگوی همان کامیت `e56db60` را به یک قاعده‌ی عمومی تبدیل کن).
2. یک قاعده‌ی **Semgrep** (در `.semgrep/project-rules.yml` موجود) اضافه کن: هر `float(...)`/`Float` روی فیلد پولی، یا هر محاسبه‌ی پولی با `float` در Python/Dart/TS ⇒ قرمز.
3. **قواعد گردکردن** را مستند و تست کن: `discount_pct` (درصد صحیح) چگونه روی `total_rial` اعمال می‌شود (جهت گردکردن، ترتیب اعمال چند تخفیف، سقف استفاده از کد تخفیف)؛ مالیات/کارمزد؛ و **تقسیم** مبلغ بین آیتم‌ها (اختلاف باقی‌مانده به کدام آیتم می‌رسد).
4. گزارش سود/زیان دوره‌ای (QF‑10) با **تست‌های زمانی منجمد** روی مرزهای جلالی/تهران: ابتدای دوره، پایان دوره، سال کبیسه‌ی جلالی، تغییر روز/ماه، و refund بین‌دوره‌ای.
5. propertyهای پولی WP‑08 را اجرا کن و نتایج را اینجا ارجاع بده.
6. **ممیزی حسابرسی**: هر تغییر پولی باید ردیف `audit_logs` و (برای کیف‌پول) ردیف دفتر کل داشته باشد؛ یک تست که پس از هر عملیات مالی، `مانده = Σ دفتر کل` و `audit log موجود` را assert کند.
**معیار پذیرش:** تست مرزی ۲^۵۳−۱ سبز در هر سه لایه؛ قاعده‌ی Semgrep پولی فعال و سبز؛ قواعد گردکردن مستند + تست‌شده؛ تست‌های زمانی جلالی/تهران سبز؛ تست همسانی مانده/دفترکل/audit log برای همه‌ی عملیات مالی.

---

### WP‑12 · پلتفرم وب، PWA و Electron — P1
**چرا:** دو سطح جدید اضافه شده (بیلد وب Flutter و PWA استودیو) که گیت اختصاصی ندارند؛ و دکمه‌های مالی/مخرب در QA مرورگری `BLOCKED` ماندند.
**شاهد:** `web.yml` فقط analyze/test/build/artifact دارد (بدون تست مرورگری، بدون بودجه‌ی باندل، بدون Lighthouse). `mp-app/studio/public/sw.js` → cache-first برای assets هش‌دار، network-first برای HTML/مانیفست، `skipWaiting` + reload. `mp-app/studio/electron/main.cjs` → `contextIsolation: true`, `nodeIntegration: false` ولی **بدون `sandbox`، بدون `setWindowOpenHandler`، بدون guard برای `will-navigate`**. `qa-report/FINAL-REPORT.md` → دکمه‌های مالی/مخرب کلیک نشدند (`BLOCKED`).
**کار:**
1. **Playwright** را برای استودیو اضافه کن: E2E روی بیلد واقعی (Vite build) شامل **جریان‌های مالی و مخرب** در یک محیط ایزوله با داده‌ی seed مصنوعی (همان `qa-report/tools/seed_live.py`) — این `BLOCKED` را می‌بندد. شامل: ثبت پرداخت، تأیید رسید، ارسال، حذف، تأیید نهایی، کد تخفیف، گزارش سود/زیان.
2. در همان Playwright: `axe-core` برای a11y، **رگرسیون بصری** (`toHaveScreenshot`)، ماتریس viewport، و رفتار **آفلاین/بازیابی** (قطع شبکه وسط فرم مالی).
3. **بودجه‌ی وب**: `rollup-plugin-visualizer` (یا معادل Vite) برای نقشه‌ی باندل + گیت اندازه؛ **Lighthouse CI** روی بیلد استودیو و (اگر وب کلاینت منتشر می‌شود) روی بیلد `web.yml` با بودجه‌ی صریح perf/a11y/best-practices/SEO.
4. **Service Worker را امن کن**: هیچ پاسخ API/داده‌ی حساس cache نشود (فقط assets هش‌دار)؛ یک تست که پس از logout هیچ داده‌ی حساس در `caches` نماند؛ و رفتار نسخه‌ی قدیمی SW در برابر API جدید (ناسازگاری نسخه) تست شود.
5. **Electron hardening**: `sandbox: true`، `setWindowOpenHandler` → deny، guard برای `will-navigate`/`will-attach-webview`، مرور سطح `preload.cjs` (کمترین سطح ممکن). چون `doyensec/electronegativity` **آرشیو شده**، این‌ها را به‌صورت **تست vitest** روی کانفیگ main process قفل کن.
6. **وبِ کلاینت**: یک گیت که `dart:io` در کد وب‌سازگار وارد نشود (کامیت `ae3e260` همین را رفع کرد — پس گیت ضد‌رگرسیون لازم است) + تست اینکه وب کلاینت در حداقل یک مرورگر واقعی بالا می‌آید و جریان اصلی کار می‌کند.
**معیار پذیرش:** Playwright E2E با پوشش جریان‌های مالی/مخرب سبز در CI (با داده‌ی مصنوعی)؛ axe + رگرسیون بصری فعال؛ بودجه‌ی باندل و Lighthouse در CI؛ تست‌های SW و Electron hardening سبز؛ گیت ضد‌رگرسیون `dart:io` در وب.
**ابزار:** `microsoft/playwright` (Apache‑2.0، ⭐100.5k) · `dequelabs/axe-core` (MPL‑2.0) · `GoogleChrome/lighthouse-ci` (Apache‑2.0، ⭐7.2k) · `GoogleChrome/web-vitals` (Apache‑2.0).

---

### WP‑13 · قطعیت CI و لینتر استودیو — P1
**چرا:** دو حفره‌ی تکرارپذیری: نصب غیرقطعی npm، و اسکریپت lint استودیو که **قابل اجرا نیست**.
**شاهد:** `ci.yml:178` و `ci.yml:392` → `npm ci || npm install` در حالی که `mp-app/studio/package-lock.json` ترک‌شده است. `package.json` → `"lint": "eslint src --ext .ts,.tsx"` ولی **`eslint` در `devDependencies` نیست** (devDeps: @testing-library/react, @testing-library/user-event, @types/react, @types/react-dom, @vitejs/plugin-react, autoprefixer, jsdom, postcss, tailwindcss, typescript, vite, vitest) و **هیچ فایل کانفیگ eslint** ترک‌شده نیست ⇒ اسکریپت مرده است و job `studio` هم lint را اجرا نمی‌کند (فقط test/build/audit).
**کار:**
1. هر دو `npm ci || npm install` → `npm ci` خالص؛ ناسازگاری lockfile باید بیلد را **قرمز** کند.
2. تصمیم صریح (و ثبت در گزارش) درباره‌ی lint استودیو:
   - **راه الف (ترجیحی):** ESLint 9 + flat config + `typescript-eslint` + `eslint-plugin-react-hooks` + قواعد a11y را نصب کن، `npm run lint` را درست کن و به job `studio` **قبل از test** اضافه کن. خطاهای موجود را رفع کن یا عدد پایه بگذار و گیت ضد‌رگرسیون بزن.
   - **راه ب:** اگر lint نخواسته‌ایم، اسکریپت مرده را از `package.json` حذف کن و در گزارش دلیل بیاور (اسکریپت مرده = گمراه‌کننده).
3. سینتکس `--ext` مربوط به ESLint 8 است؛ با مهاجرت به flat config باید اصلاح شود.
4. نسخه‌ی Node را در همه‌ی jobها صریح و یکسان کن (امروز `"22"`؛ `22.x.y` مشخص یا `engines`/`.nvmrc`) — الگوی درستِ موجود: `client-pinned` که Flutter را پین و drift را بررسی می‌کند. همان انضباط را برای Node/Python اعمال کن.
5. `concurrency` + `cancel-in-progress` برای بقیه‌ی workflowها (الگوی موجود در `client-format-fix.yml`).
**معیار پذیرش:** صفر `npm ci || npm install`؛ lint استودیو یا واقعاً اجرا و گیت شده، یا اسکریپت مرده حذف شده؛ پین نسخه‌های Node/Python/Flutter یکدست و بدون drift؛ CI سبز.

---

### WP‑14 · کد تکراری، کد مرده، پیچیدگی — P2
**چرا:** خواسته‌های ۹، ۱۰ و ۱۱. امروز هیچ ابزار سنجش تکرار/مرده/پیچیدگی در مخزن نیست.
**شاهد:** هیچ `jscpd`/`knip`/`vulture`/`lizard`/`radon`/`import-linter`/`dependency-cruiser` در مخزن یا CI نیست. RepoWise برای معماری و بهداشت کد استفاده شده (`docs/MuscleParadise/architecture/repowise-*`, `BUILDER-START-AND-REPOWISE.md`) — پس بستر آماده است. ۲۴ ماژول بک‌اند و ۱۹ موتور ⇒ خطر **منطق موازی** بین `engine/` و `modules/*` واقعی است.
**کار (فقط بعد از سبز شدن WP‑07 — قاعده‌ی ۳‑۱۱):**
1. **تکرار:** `jscpd` با آستانه‌ی صریح روی **هر سه زیرپروژه همزمان** (py + dart + ts/tsx) تا منطق موازیِ بین‌لایه‌ای دیده شود. علاوه بر تکرار متنی، **تکرار معنایی** را دستی بررسی کن: دو ماژول که یک قاعده‌ی کسب‌وکاری را جدا پیاده کرده‌اند (به‌ویژه مالی/تخفیف/کیف‌پول در `modules/` در برابر `engine/`). هر یافته ⇒ ادغام با تست، یا ثبت دلیلِ جدا بودن.
2. **کد مرده:** پایتون → `ruff` (F401/F811/F841) + **vulture** + endpointهای ثبت‌شده بدون مصرف‌کننده؛ استودیو → **knip** + `depcheck`؛ کلاینت → `dart analyze` (`unused_element`, `unused_import`, `unused_field`, `dead_code`) + دارایی‌های بی‌مصرف در `pubspec.yaml`/`assets/`؛ گراف → **import-linter** برای ممنوعیت لایه‌شکنی (`api → modules → engine/db`، ممنوعیت import معکوس).
3. **پیچیدگی:** `lizard` (چندزبانه) و `radon` (پایتون) برای فهرست توابع پیچیده؛ گیت CI با آستانه (مثلاً cyclomatic ≤ ۱۰) که برای **کد جدید** سخت‌گیر و برای موجود، عدد پایه را قفل کند.
4. **ساده‌سازی:** برای هر مورد بالای آستانه → استخراج تابع، حذف پارامتر بی‌استفاده، یکسان‌سازی امضاها، **بدون تغییر رفتار** و با گیت جهش/property سبز.
5. خروجی RepoWise را برای dead code و برنامه‌ی ریفکتور بخوان و در گزارش ارجاع بده (ابزار dev، AGPL — مجاز طبق ۳‑۶).
**معیار پذیرش:** گزارش jscpd با تعیین تکلیف **همه‌ی** یافته‌های بالای آستانه؛ صفر کد مرده‌ی قطعی (یا دلیل مستند)؛ صرخ چرخه‌ی وابستگی/لایه‌شکنی با گیت CI؛ گیت پیچیدگی فعال؛ ریفکتورها با تست جهش سبز.
**ابزار:** `kucherenko/jscpd` (MIT، ⭐6.6k، ۲۲۰+ زبان) · `webpro-nl/knip` (ISC، ⭐12.7k) · `terryyin/lizard` (MIT) · `rubik/radon` (MIT) · `vulture` (PyPI) · `import-linter/import-linter` (BSD‑2) · `pahen/madge` (MIT) · `repowise-dev/repowise` (AGPL، dev).

---

### WP‑15 · i18n/l10n و فونت — P2
**چرا:** هیچ زیرساخت ترجمه‌ای نیست و یک نقص واقعیِ فونت/ایموجی باز است.
**شاهد:** grep برای `\.arb$|l10n|intl|translations` → **۰**. نقص بازِ QA: «در فوتر، ایموجی ❤️/💚 به‌صورت جعبه نمایش داده می‌شود (فونت)». رشته‌ها hardcode‌اند.
**کار:**
1. کلاینت: `flutter_localizations` + `flutter gen-l10n` با `lib/l10n/app_fa.arb` و `app_en.arb`؛ استخراج همه‌ی رشته‌های hardcode (اسکریپت + بازبینی دستی)؛ `pubspec.yaml` → `generate: true`.
2. استودیو: `i18next` + `react-i18next` با **ICU** برای جمع‌بندی و قالب عدد/تاریخ/ارز (`Intl`)؛ کلیدها در `locales/fa.json` و `en.json`. اعداد پولی (ریال) با قالب locale-aware و **بدون اعشار**.
3. **فونت/ایموجی**: یک فونت فارسی کامل + فالبک ایموجی (مثلاً Noto Color Emoji) را به باندل اضافه کن و نقص ❤️/💚 را ببند؛ تست golden (WP‑09) که رندر ایموجی را قفل کند. لایسنس فونت را در `NOTICE-THIRD-PARTY.md` ثبت کن (الگوی موجود: Unlicense/MIT با commit و sha256).
4. **pseudo-localization**: اسکریپت/تستی که رشته‌ها را ۳۰٪ کشیده‌تر کند و golden بگیرد ⇒ رشته‌های hardcode و سرریز متن لو می‌روند (همان نقص «بنر روی محتوا» را هم می‌گیرد).
5. گیت CI: هیچ رشته‌ی کاربر‌نمای hardcode جدید (قاعده‌ی lint/Semgrep) و هیچ کلید ترجمه‌ی گم‌شده (`fa` بدون `en` یا برعکس).
6. قالب تاریخ جلالی و منطقه‌ی زمانی تهران را در یک ماژول مشترک و با **تست property زمانی** (WP‑08/WP‑19) بگذار.
**معیار پذیرش:** همه‌ی رشته‌های کاربر‌نما از منبع l10n؛ تست کلید گم‌شده سبز؛ نقص ایموجی بسته با golden شاهد؛ pseudo-locale اجرا و بازبینی شده؛ لایسنس فونت در NOTICE.

---

### WP‑16 · آشوب و حالت تنزل — P2
**چرا:** خواسته‌ی ۱۲ («اورلود») و پشتیبانِ WP‑01. امروز هیچ تست خرابیِ عمدی نیست.
**شاهد:** grep برای `toxiproxy|chaos|respx|vcrpy` → **۰**. سخت‌سازی SQLite و `rollback.sh` و `test_backup_drill.py` موجودند؛ حادثه‌ی استخر در `qa-report/FINAL-REPORT.md` ثبت شده.
**کار:**
1. **Toxiproxy** در پروفایل `chaos` در `docker-compose.yml`: تأخیر/قطعی برای DB، سرویس AI، SMS/OTP، درگاه پرداخت، سرویس چهره، Valkey.
2. برای هر سناریو یک تست که **رفتار انتظار‌رفته** را اثبات کند: پیام کاربری درست، صف `outbox` کار کند، retry با backoff، circuit breaker، **بدون گم‌شدن یا دوباره‌نوشتن داده** (با propertyهای `sync_lww` در WP‑08).
3. سناریوهای محلی: دیسک پر، DB قفل‌شده (`database is locked`)، فایل WAL خراب، Valkey پایین (⇒ rate-limit storage مشترک چه می‌شود؟ آیتم ۱۶ چک‌لیست)، `pool` اشباع‌شده (مستقیماً به WP‑01 وصل است).
4. upstreamهای خارجی را با `respx`/`vcrpy` شبیه‌سازی کن تا تست‌ها قطعی بمانند.
5. **دریل بازیابی واقعی**: `test_backup_drill.py` را طوری گسترش بده که **restore** روی DB جدید انجام شود و **برابری داده‌ها** assert شود، و سپس `alembic upgrade head` روی DB بازیابی‌شده (آیتم ۱۷‑۱۸ چک‌لیست).
6. نتایج را در `OPS-RUNBOOK.md` به‌عنوان «سناریوهای خرابی و پاسخ» ثبت کن.
**معیار پذیرش:** پروفایل chaos با یک دستور اجرا می‌شود؛ ≥۶ سناریوی خرابی با تست سبز؛ دریل restore با assert برابری داده؛ سناریوی Valkey/pool با رفتار مستند.
**ابزار:** `Shopify/toxiproxy` (MIT، ⭐12.5k) · `respx`/`vcrpy` · `pytest-rerunfailures`.

---

### WP‑17 · گسترش گیت بار — P2
**چرا:** گیت k6 فقط دو اندپوینت سبک را می‌کوبد؛ Locust ۲۰۰ کاربر اجرا شده ولی صریحاً نوشته «تأیید production نیست» و روی SQLite/یک worker بوده.
**شاهد:** `mp-app/tests/load/k6-gate.js` → فقط `GET /api/v1/health/ready` و `POST /api/v1/auth/otp/request`. `qa-report/FINAL-REPORT.md` بخش ۵ (چهار اجرا، p95=210ms، اجرای ۲ = ۰ درخواست). `finn/reports/load/M22-smoke_*`, `M36c2-smoke_*`.
**کار:**
1. سناریوهای k6 با آستانه‌ی صریح برای مسیرهای سنگین: چک‌این/تطبیق چهره، تولید یا بازخوانی تجویز AI، ثبت ست/تمرین، تجمیع داشبورد و گزارش سود/زیان، سرو مدیا (`/media/*` در Caddyfile و `static/exercises/*.gif`) با بررسی **hit rate کش**.
2. همان سناریوها را یک بار روی **Postgres** اجرا کن و اعداد را کنار SQLite بگذار (ورودی ADR‑002 و WP‑01).
3. **گیت N+1**: شمارش کوئری برای endpointهای فهرست/تجمیع با event listener روی SQLAlchemy؛ آستانه‌ی صریح.
4. پروفایل بک‌اند با **py-spy** در job زمان‌بند؛ گزارش در `finn/reports/load/`.
5. یک گزارش بار جدید با الگوی `docs/MuscleParadise/LOAD-TEST-…` و **صراحت درباره‌ی اعتبار** (همان سبک صادقانه‌ی موجود: چه چیزی تأیید production است و چه چیزی نیست).
**معیار پذیرش:** ≥۵ سناریوی جدید با آستانه سبز؛ مقایسه‌ی SQLite/Postgres مستند؛ گیت N+1 در CI؛ گزارش بار جدید با اعداد واقعی و بیان صریح دامنه‌ی اعتبار.
**ابزار:** `grafana/k6` (AGPL، dev) · `locustio/locust` (MIT، موجود) · `py-spy` · `hatoo/oha` (MIT).

---

### WP‑18 · گیت خودکار لایسنس وابستگی‌ها — P2
**چرا:** دارایی‌های ثالث **عالی** مستند شده‌اند (`NOTICE-THIRD-PARTY.md` با Unlicense/MIT + commit + sha256)، ولی **وابستگی‌های نرم‌افزاری** گیت خودکار ندارند و لایسنس محصول Proprietary است.
**شاهد:** grep برای `license-checker|pip-licenses|license` در workflows → فقط `::notice` های بی‌ربط؛ هیچ گیت لایسنسی نیست. `pip-audit`/`npm audit` فقط آسیب‌پذیری می‌بینند.
**کار:**
1. job `license-gate`: بک‌اند → `pip-licenses` (خروجی JSON) + فهرست ممنوعه (`GPL*`, `AGPL*`, `SSPL*`, `CPAL*`) برای **وابستگی توزیعی**؛ استودیو → `license-checker-rseidelsohn --production` + همان فهرست (با گیت **شکننده**، نه فقط `--summary`)؛ کلاینت → `flutter pub deps` + استخراج لایسنس پکیج‌ها.
2. تفکیک صریح «وابستگی توزیعی» در برابر «ابزار dev/CI» (قاعده‌ی ۳‑۶) در یک فایل کانفیگ، تا ابزارهای AGPL مثل k6/repowise به‌اشتباه قرمز نشوند.
3. **ORT** یا **ScanCode** به‌عنوان job زمان‌بند برای کل زنجیره (شامل دارایی‌ها) و آرتیفکت گزارش.
4. `NOTICE-THIRD-PARTY.md` را با خروجی خودکار تکمیل کن و هر مورد بدون لایسنس مشخص را علامت بزن.
**معیار پذیرش:** job لایسنس با گیت شکننده سبز؛ تفکیک توزیعی/dev در کانفیگ؛ گزارش ORT/ScanCode به‌عنوان آرتیفکت؛ NOTICE کامل و همگام با خروجی خودکار.
**ابزار:** `oss-review-toolkit/ort` (Apache‑2.0، ⭐2.1k) · `aboutcode-org/scancode-toolkit` (⭐2.7k) · `pip-licenses` · `RSeidelsohn/license-checker-rseidelsohn` (BSD‑3).

---

### WP‑19 · بهداشت کد، قطعیت تست و ضد‌رگرسیون — P2
**چرا:** چند سنجه از زمان ممیزی قبلی **بدتر** شده‌اند و هیچ گیتی جلویشان را نمی‌گیرد.
**شاهد:** `except Exception` **۱۱ → ۲۲**؛ `TODO/FIXME/HACK` **۴۲ → ۴۸**؛ تست‌های skip **۲ → ۶** (به‌علاوه ۹ skip در استودیو و ۲ skip در بک‌اند طبق گزارش QA)؛ `print()` غیرتست **۴۱** (بدون تغییر). هیچ `freezegun`/`time-machine` در dev deps نیست در حالی که منطق جلالی/تهران در ۲۵ فایل وجود دارد. `.semgrep/project-rules.yml` موجود است (پس بستر قاعده‌گذاری آماده است).
**کار:**
1. هر ۴۱ `print()` → logger ساخت‌یافته؛ قاعده‌ی Semgrep که `print(`/`debugPrint(`/`console.log` در کد غیرتست را قرمز کند.
2. هر ۲۲ `except Exception:` تعیین تکلیف: استثنای دقیق، یا لاگ+بازفرستادن، یا کامنت دلیلِ صریح. **صفر بلعیدن بی‌صدا.**
3. هر ۴۸ `TODO/FIXME/HACK` → یا انجام، یا ردیف در `BUILD-QUEUE.md` با مسئول و دلیل. صفر TODO بی‌تکلیف.
4. هر ۶ تست skip + ۹ skip استودیو → تعیین تکلیف: یا فعال کن، یا دلیل `BLOCKED` دقیق بنویس (الگوی `qa-report/FINAL-REPORT.md`).
5. **قطعیت زمانی:** `freezegun` یا `time-machine` به dev deps؛ تست‌های زمانی برای جلالی/تهران، DST، انقضای OTP، پنجره‌های `DATA-RETENTION.md`، و دوره‌های گزارش مالی.
6. **ضد flake:** اجرای سه‌باره‌ی یک زیرمجموعه‌ی حساس در CI (یا `pytest-rerunfailures` با گزارش) تا flaky بودن دیده شود؛ و یک قاعده: تست flaky = باگ.
7. **گیت‌های ضد‌رگرسیون**: فایل `.ci-baseline.json` با همه‌ی سنجه‌های بخش ۵ و یک step در CI که هر **افزایش** در سنجه‌های بد (print/except/TODO/skip/dynamic/as) و هر **کاهش** در سنجه‌های خوب (پوشش، تعداد تست) را قرمز کند.
**معیار پذیرش:** صفر `print` غیرتست با گیت Semgrep؛ صفر `except Exception` بی‌تکلیف؛ صفر TODO بی‌تکلیف؛ همه‌ی skipها تعیین تکلیف؛ تست‌های زمانی منجمد سبز؛ `.ci-baseline.json` + گیت ضد‌رگرسیون فعال.

---

### WP‑20 · حریم خصوصی، PII و provenance تصاویر — P2
**چرا:** داده‌ی سلامتی/زیست‌سنجشی داری و تصاویر زیادی در مخزن commit شده؛ باید **قابل اثبات** باشد که مصنوعی‌اند.
**شاهد:** `docs/MuscleParadise/ui-previews/*.png` → ۸ تصویر بزرگ شامل `03-kiosk-face-gate.png` (۱٫۷MB)، `04-payment-receipt.png` (۱٫۷MB)، `05-member-profile.png` (۶۱۶KB)، `07-client-home-grid.png` (۲٫۱MB). `qa-report/screenshots/*.png` → ۱۱ تصویر از محیط اجرا با داده‌ی seed. `qa-report/buttons.json` شامل شماره‌های seed مثل `09120000001` و نام‌های «عضو فیک …» ⇒ **مصنوعی بودن محتمل و مطلوب است ولی مستند نشده**. `mp.db` ترک‌شده (WP‑05).
**کار:**
1. `docs/MuscleParadise/ui-previews/PROVENANCE.md` و `qa-report/PROVENANCE.md`: برای **هر تصویر** یک ردیف — چگونه تولید شده، از چه محیطی، چه داده‌ای دارد، آیا چهره/رسید/شماره‌ی **واقعی** دارد، و چگونه مصنوعی بودنش اثبات می‌شود.
2. اگر داده‌ی واقعی پیدا شد: **حذف نکن** (بازنویسی تاریخچه destructive است)؛ در گزارش «مسدود — نیاز به تأیید انسانی» با گزینه‌ها و پیشنهاد بنویس (بخش ۸).
3. یک **قاعده‌ی CI** اضافه کن: seed داده‌ی QA فقط از `qa-report/tools/seed_live.py` با الگوی شماره‌های مصنوعی (`0912…`) و نام «عضو فیک»؛ هر اسکرین‌شات/آرتیفکت جدید باید از همان seed باشد.
4. بررسی کن هیچ PII در `evidence/*.json`، `qa-report/load/*.csv`، لاگ‌های CI یا `finn/reports/` نباشد (یک اسکریپت پویش با regex موبایل/کد ملی/ایمیل + خروجی بدون مقدار، مطابق الگوی redaction موجود).
5. `modules/privacy/` و `DATA-RETENTION.md` را در برابر کد **راستی‌آزمایی** کن: آیا حذف/انقضای داده واقعاً پیاده و تست شده؟ (یک تست که چرخه‌ی عمر داده را اثبات کند: ثبت → انقضا → حذف/ناشناس‌سازی.)
6. `.claude/` حذف شده (خوب) — بررسی کن transcript یا توکنی در `finn/` یا `.finn/` باقی نمانده باشد.
**معیار پذیرش:** هر دو فایل PROVENANCE کامل؛ اسکریپت پویش PII سبز و به‌عنوان گیت در CI؛ تست چرخه‌ی عمر retention سبز؛ فهرست موارد مسدود (احتمالاً خالی).

---

### WP‑21 · ممیزی خط‌به‌خط نهایی و بستن خواسته‌های ۱ تا ۱۲ — P1/P2
**چرا:** این جمع‌بندیِ خواسته‌ی اصلی مالک است و باید **آخر** انجام شود (بعد از WP‑07/08/09).
**کار:**
1. **نقشه‌ی کامل و همبستگی:** خروجی RepoWise را به‌روز بگیر (گراف فراخوانی، health score، dead code، blast radius، C4) و `docs/MuscleParadise/architecture/c4.md` و `module-map.md` را با آن همگام کن؛ fan‑in/fan‑out هر ماژول و ۵ نقطه‌ی پرتراکم را با دلیل مستند کن.
2. **جدول ممیزی هر ماژول** (پیوست ب) را برای همه‌ی ۲۴ ماژول بک‌اند، ۱۹ موتور، و هر بخش کلاینت/استودیو پر کن.
3. **خروجی‌ها (خواسته‌ی ۴):** برای هر چیزی که خروجی تولید می‌کند — رسید سفارش/عضو، گزارش مربی، گزارش سود/زیان دوره‌ای، خروجی ارزیابی، export فایل، پیامک/اعلان، QR/کد تخفیف، پاسخ API — یک **تست طلایی/تصویب (approval)** بنویس که خروجی واقعی را در فایل مرجع قفل کند. این `OUTPUT-AUDIT-2026-11-14.md` را اجرایی و پایدار می‌کند.
4. **سیم‌کشی‌ها (خواسته‌ی ۲):** یک دیاگرام sequence برای هر ورک‌فلوی اصلی (ثبت‌نام→OTP→چک‌این→تمرین→پرداخت→رسید؛ کد تخفیف؛ هزینه/رسید هزینه؛ کیف‌پول؛ سینک آفلاین؛ به‌روزرسانی PWA) تولید کن و با `tools/mermaid-check` اعتبارسنجی کن.
5. **تک‌تک دکمه‌ها (خواسته‌ی ۸):** `UI-INVENTORY.md` (WP‑09) را کامل کن و وضعیت هر ردیف را با شاهد (تست/golden/E2E) پر کن؛ ۴۵ دکمه‌ی کلیک‌شده در QA را به پوشش خودکار دائمی تبدیل کن تا رگرسیون دیده شود.
6. **جدول نهایی:** «خواسته‌ی ۱ تا ۱۲ ← WP ← شاهد اجرایی (تست/CI run/عدد)» در `docs/MuscleParadise/AUDIT-FINAL-2026-11-20.md`.
**معیار پذیرش:** جدول ممیزی همه‌ی ماژول‌ها پر؛ تست طلایی برای هر خروجی؛ دیاگرام‌های sequence اعتبارسنجی‌شده؛ `UI-INVENTORY.md` کامل با شاهد؛ جدول نهایی خواسته‌ها بدون خانه‌ی خالی.

### WP‑22 · امنیت سطح تماس و اعتبارسنجی پیکربندی production — P0
**چرا:** چهار حفره‌ی راستی‌آزمایی‌شده که در هیچ سند پروژه‌ای نبودند و هر چهار **ارزان** رفع می‌شوند (بیشترشان چند شرط در `validate_production_configuration` و چند تست). دو تای اول مستقیماً می‌توانند در production باعث خاموشی یا نشت اطلاعات عملیاتی شوند.
**شاهد:** A2 `api/v1/monitoring.py:14` (`/metrics` بدون dependency) + `Caddyfile` → `handle /api/*` (عمومی) · A3 `app/config.py:69` + `app/security/proxy.py:12-13` + `modules/auth/router.py:32-38` و صفر چک در اعتبارسنجی · B17 `app/config.py:71` + `api/v1/monitoring.py:61` و `worker_ok = True` پیش‌فرض · B18 صفر چک روی `database_url`.
**کار:**
1. **A2:** `/metrics` را از مسیر عمومی خارج کن — یا یک `handle` جدا در `Caddyfile` که فقط از شبکه‌ی داخلی/`monitoring` پاسخ دهد، یا Bearer token با secret. تست بگذار: درخواست از بیرون ⇒ `401/404`؛ اسکرپ داخلی ⇒ `200`. `prometheus.yml` موجود را متناسب به‌روز کن.
2. **A3:** `MP_TRUSTED_PROXIES` را به `validate_production_configuration` اضافه کن (در production اگر پشت پراکسی است ⇒ الزامی و غیرخالی). مقدار واقعی Caddy/nginx را در `deploy.yml`/ansible ست کن. دو تست: (a) دو کلاینت مختلف پشت پراکسی معتمد ⇒ **دو سبد جدا** rate-limit؛ (b) هدر `X-Forwarded-For` از peer **غیرمعتمد** ⇒ نادیده گرفته شود (ضد دور زدن rate-limit).
3. **B17:** `require_worker` را در production الزامی کن؛ `/health/ready` باید با heartbeat مرده/صف انباشته **قرمز** شود (نه `worker_ok = True` پیش‌فرض)؛ alert روی عمق صف outbox و رشد `outbox_dead_letters` در `alerts.yml`.
4. **B18:** تصمیم صریح و ثبت‌شده درباره‌ی `MP_DATABASE_URL` در production: یا SQLite با شروط و سقف‌های مستند (حداکثر عضو، تک‌writer، `PLAN-CLOUD-PRODUCTION.md`) یا الزام URL غیر‑SQLite. `ADR‑002` را با نتیجه‌ی بارِ Postgres در برابر SQLite (ورودی از WP‑17) به‌روز کن.
5. **سایر کلیدهای بی‌اعتبارسنجی را کامل کن:** `receipts_dir` (وجود و قابل نوشتن بودن)، `public_base_url` (HTTPS در production)، سازگاری `shop_online_purchase_enabled` با `payment_gateway`، و `shop_timezone`.
6. مستند کن: یک جدول «کلید محیط ← آیا در production اعتبارسنجی می‌شود؟ ← چرا» در `docs/MuscleParadise/OPS-RUNBOOK.md`.
**معیار پذیرش:** `/metrics` از بیرون غیرقابل دسترس (تست)؛ `trusted_proxies` در production اجباری + تست دو سبد + تست نادیده‌گرفتن XFF غیرمعتمد؛ readiness با worker مرده قرمز (تست)؛ `database_url`/`receipts_dir`/`public_base_url` در اعتبارسنجی؛ ADR‑002 به‌روز؛ جدول OPS-RUNBOOK کامل.
**ابزار:** همه داخلی (FastAPI/Pydantic/Caddy/Prometheus) — بدون وابستگی جدید.

---

### WP‑23 · کیوسک / چک‌این انتها‌به‌انتها — P1
**چرا:** خودِ سند تحویل می‌گوید «کیوسک / چک‌این مسیر ناقص است و اتصال انتها‌به‌انتها کامل نشده» (§۱۳)، در حالی که یک تصویر ۱٫۷MB در مستندات یک «کیوسک گیت چهره» را نشان می‌دهد. سمت سرور آماده است (۱۰ عملیات `/api/v1/face/*`)؛ پس یا سمت کلاینت وصل می‌شود یا ادعا اصلاح — **بی‌تکلیف نماند**. این خواسته‌ی ۲ (سیم‌کشی) و ۸ (دکمه‌ها) است.
**شاهد:** `PROJECT-HANDOFF.md` §۱۳ و §۸ (۱۲ صفحه‌ی استودیو، هیچ‌کدام کیوسک نیست) · راستی‌آزمایی من: `kiosk` در کل مخزن ۱۰ ارجاع و در استودیو فقط `src/lib/update.ts` · `docs/MuscleParadise/ui-previews/03-kiosk-face-gate.png` · endpointهای آماده: `POST /face/checkin`, `/face/checkin-qr`, `/face/checkins/{id}/exit`, `/face/enroll`, `/face/consent`, `/face/qr-token`, `/face/deep-status` (`modules/face_id/router.py`).
**کار:**
1. **تصمیم صریح** (قاعده‌ی ۳‑۲، کم‌خطرترین): کیوسک = حالتِ تمام‌صفحه‌ی استودیو (روی دستگاه لمسی ورودی) یا صفحه‌ی مستقل Flutter؟ تصمیم و دلیل را در گزارش و `OWNER-DECISIONS.md` ثبت کن.
2. جریان کامل را وصل کن: شناسایی چهره → تطبیق → `POST /face/checkin` → نمایش نتیجه → `POST /face/checkins/{id}/exit`. مسیر جایگزین QR (`/face/qr-token` + `/face/checkin-qr`) برای وقتی که چهره ثبت نشده یا دوربین خراب است.
3. **همه‌ی حالت‌های شکست** با پیام کاربری و بدون crash: چهره‌ی ثبت‌نشده، تطبیق ناموفق، عضو بدون membership فعال، consent لغوشده، دوربین/دسترسی رد شده، شبکه قطع، پاسخ کند (timeout) — هرکدام با golden (WP‑09) و تست.
4. تست E2E: Playwright برای حالت کیوسک استودیو (WP‑12) یا patrol برای کلاینت (WP‑09) — با داده‌ی seed مصنوعی (`qa-report/tools/seed_live.py`) و **بدون چهره‌ی واقعی**.
5. اگر کیوسک در دامنه‌ی انتشار نیست: تصویر و ادعای مستند را اصلاح کن، مورد را در `BUILD-QUEUE.md` ثبت کن و در `PROVENANCE.md` (WP‑20) بنویس که آن تصویر چه چیزی را نشان می‌دهد.
**معیار پذیرش:** یا جریان کیوسک با تست E2E سبز + golden همه‌ی حالت‌های شکست + مستند، یا ادعای مستند/تصویر اصلاح و در `BUILD-QUEUE.md` ثبت شده. صفر «کیوسک» بی‌تکلیف در مخزن.

---

### WP‑24 · اصلاح سند تحویل و اسکریپت تولیدش — P1 (ارزان، زود انجام بده)
**چرا:** `PROJECT-HANDOFF.md` قرار است منبع حقیقت نشست‌های بعدی AI باشد و **از روز اول ۸ نقص دارد**؛ اگر ایجنت بعدی به آن اعتماد کند، کاتالوگ مجوزها را نمی‌بیند، مقدار پیش‌فرض CORS را اشتباه می‌خواند و برای روتر `face` به مسیر اشتباه می‌رود. ریشه‌ی همه‌ی اینها یک اسکریپت تولید است که **خودش تست ندارد**.
**شاهد:** D1–D8 در بخش ۴‑ت (جدول §۷ خالی در برابر `grants.py:34`؛ §۶ «(» در برابر `config.py:79`؛ §۱۳ در برابر `apk.yml` `on: push: tags:["v*"]` و تناقض با §۱۰؛ §۲ در برابر `modules/face_id/router.py`؛ `--check` بی‌گیت؛ §۱۱ در برابر `qa-report/screenshots/`؛ سه snapshot بدون تعیین معتبر؛ جدول §۲ با ۲۳ ردیف برای ۲۴ پوشه).
**کار:**
1. پارسر `scripts/repowise_handoff.py` را اصلاح کن: **AST به‌جای regex** برای دیکشنری/مقدارهای چندخطی (`KNOWN_PERMISSIONS`, `cors_origins`)، و خواندن رویدادهای workflow از خودِ YAML (نه حدس).
2. **برای خودِ اسکریپت تولید سند، تست واحد بنویس** (این مهم‌ترین بخش است): خروجی تولیدشده را با حقیقتِ کد مقایسه کند — تعداد ردیف‌های جدول مجوزها > ۰ و برابر `len(KNOWN_PERMISSIONS)`؛ هر مسیر `api/routes.json` در سند حاضر باشد؛ رویدادهای هر workflow با YAML برابر باشد؛ هیچ مقدار پیش‌فرضی «(» یا خالیِ بی‌دلیل نباشد؛ هر مسیر فایلی که سند نام می‌برد واقعاً وجود داشته باشد.
3. `scripts/repowise_handoff.py --check` را به job `docs` در `ci.yml` وصل کن تا رانش سند **قرمز** شود (الگوی موجود: `docs_gate.py`).
4. D3/D4/D6/D7/D8 را اصلاح کن و به هر سند RepoWise یک خط «snapshot معتبر: `<sha>` — تاریخ: …» اضافه کن تا ایجنت بعدی بداند کدام عدد جاری است.
5. سند را (با CI سبز) مرج کن و شاخه را حذف کن — مطابق `docs/MuscleParadise/BRANCH-CONSOLIDATION-2026-11-20.md` و آیتم ۳۵‑۳۷ چک‌لیست.
**معیار پذیرش:** §۷ پنج مجوز را نشان می‌دهد؛ §۶ مقدار واقعی CORS؛ صفر تناقض داخلی و صفر مسیر ناموجود؛ تست واحد اسکریپت سبز (و عمداً یک بار خرابش کن تا ببینی گیت می‌گیرد)؛ `--check` در `ci.yml`؛ سند روی `main`.

---

### WP‑25 · گارد تکراری، شناسه‌ی sentinel و قواعد Semgrep جدید — P1
**چرا:** دو نقص ساختاری کوچک ولی **سیستماتیک** (دو بار ارزیابی مجوز؛ فرستادن `1-` به API) که بدون قاعده‌ی خودکار دوباره برمی‌گردند، به‌علاوه‌ی نبودِ قواعدی که جلوی پول شناور و `print` را بگیرند. این مستقیماً خواسته‌های ۹ (کد روی کد) و ۲ (سیم‌کشی) است.
**شاهد:** B2 `modules/axis_assessment/router.py:14-17` + خط ۴۹ · `routes.json` guard=`permission, permission` · شمارش `Depends(require_permission`: `classes/router.py`=۴، `axis_assessment/router.py`=۲، بقیه=۱. B3 `studio/src/pages/Nutrition.tsx:50` → `fetchDailyNutrition(memberId ?? -1, …)` و پاسخ ۲۰۰ placeholder. C18 `.semgrep/project-rules.yml` = فقط یک فایل قاعده.
**کار:**
1. **الگوی گارد را یکدست کن:** router-level برای مجوز عمومی ماژول؛ endpoint-level فقط وقتی نقش/مالکیت خاصی لازم است. گارد تکراری را حذف کن و **تست** بگذار که مجوز در یک درخواست **دقیقاً یک بار** ارزیابی می‌شود (شمارش فراخوانی با counter/spy روی `require_permission`).
2. قاعده‌ی Semgrep/AST: روتری که `dependencies=[Depends(require_permission())]` دارد نباید در پارامترها همان را بگیرد ⇒ قرمز.
3. **B3 را ریشه‌ای ببند:** در استودیو وقتی `memberId` null است **درخواست نزن** (state خالی با پیام، مطابق الگوی صفحه‌های دیگر)؛ در بک‌اند `member_id <= 0` ⇒ `422`؛ و الگوی sentinel را از همه‌جای استودیو حذف کن (grep برای `?? -1`، `|| -1`، و `= -1` به‌عنوان شناسه) + قاعده‌ی ESLint/lint که عدد منفی به‌عنوان شناسه به لایه‌ی API نرود.
4. **قاعده‌های Semgrep جدید** (حداقل ۵): پول شناور (`float(...)`/`Float` روی فیلد `*_rial`) · `print(`/`debugPrint(`/`console.log` در کد غیرتست · `except Exception` بدون لاگ یا بازفرستادن · شناسه‌ی sentinel منفی · گارد تکراری (بند ۲).
5. همه‌ی قواعد جدید را با یک نمونه‌ی مثبت و منفی در `tests/` (یا `.semgrep/tests`) قفل کن تا خودِ قاعده رگرسیون نکند.
**معیار پذیرش:** صفر گارد تکراری (با گیت CI)؛ تست «مجوز یک بار ارزیابی می‌شود» سبز؛ صفر sentinel منفی در استودیو و `422` در بک‌اند برای شناسه‌ی ≤۰؛ ≥۵ قاعده‌ی Semgrep جدید فعال با تست نمونه؛ `semgrep --config .semgrep/` سبز در job بک‌اند.

---

### WP‑26 · بسته‌ی موانع محیطی برای مالک (X1–X5) — P1
**چرا:** پنج مانع هست که بدون secret/دستگاه/دسترسی بیرونی حل نمی‌شود. به‌جای توقف، باید **بسته‌ی آماده‌ی اجرا** بسازی تا مالک در یک نشست کوتاه همه را ببندد — و دو موردشان (X3, X5) در واقع **در CI قابل حل‌اند**، نه فقط محلی.
**شاهد:** X1 secretهای `MP_ANDROID_*` و `MP_ANDROID_CERT_SHA256` تنظیم نشده (`PROJECT-HANDOFF.md` §۱۱) · X2 کلید signing افشاشده و چرخش‌نشده (`RELEASE-CHECKLIST.md:12`) · X3 `pub.dev`/`storage.googleapis.com` مسدود ⇒ Flutter فقط در Codespace/CI · X4 دستگاه واقعی، پرداخت بانکی، push/SMS، Valkey، PostgreSQL، Prometheus در دسترس نیستند (دکمه‌های مالی/مخرب در مرورگر و همزمانی کوپن روی Postgres را BLOCKED کرده) · X5 هیچ JDK در sandbox نیست ⇒ JADX مسدود (`evidence/m60/STATUS.md` «مسدود (دقیق)»).
**کار:**
1. سند `docs/MuscleParadise/OWNER-ACTION-PACK-2026-11-20.md` را بساز؛ برای **هر** مانع: (a) دقیقاً چه چیزی لازم است، (b) گام‌به‌گام (مسیر کلیک در GitHub یا دستور)، (c) نام secretها و محلشان (GitHub → Settings → Secrets and variables → Actions) **بدون نوشتن هیچ مقداری در سند**، (d) پس از انجام، کدام WP/آیتم چک‌لیست بسته می‌شود و با **چه دستوری** راستی‌آزمایی شود.
2. **X5 را در CI حل کن** (نه محلی): GitHub Actions می‌تواند `actions/setup-java` بگیرد، پس `JADX`/`apkanalyzer` را به عنوان یک job اختیاری (`workflow_dispatch`) در `apk.yml` اضافه کن تا بازرسی باینری APK که در sandbox مسدود بود، آنجا بسته شود. اگر نصبشدنی نبود، `BLOCKED` دقیق با دلیل ثبت کن.
3. **X3 را با devcontainer پوشش بده:** `.devcontainer/Dockerfile` موجود را بررسی کن که Flutter پین‌شده (۳٫۵۰٫۰)، `patrol`، و تولید golden را پوشش دهد؛ اگر نداد، اضافه کن تا ایجنت بعدی در Codespace بتواند WP‑09 را کامل کند (job `client-pinned` هم drift را چک می‌کند).
4. برای X4 یک **compose پروفایل `staging`** بساز (Postgres + Valkey + Prometheus + GlitchTip) که مالک با یک دستور بالا بیاورد و WP‑12/WP‑16/WP‑17/WP‑22 روی آن تست واقعی شوند؛ دستور اجرا و راستی‌آزمایی را در همان سند بگذار.
5. X2 را **اجرا نکن** (خط قرمز ۱ و ۲): فقط دستور اجرایی گام‌به‌گام «rotate/revoke → بازنویسی تاریخچه → ابطال توکن/کش → تأیید» را آماده کن و منتظر تأیید مالک بمان.
**معیار پذیرش:** `OWNER-ACTION-PACK` با پنج بخش کامل و هر بخش دارای «دستور راستی‌آزمایی پس از انجام»؛ job اختیاری JADX/apkanalyzer در `apk.yml` (یا BLOCKED مستند)؛ devcontainer پوشش‌دهنده‌ی patrol/golden؛ compose پروفایل `staging` با یک دستور اجرا؛ **صفر secret در سند**.

---

## ۷) ترتیب اجرا

```
WP-00 (صف، راستی‌آزمایی، دسته‌بندی ۲۱ آیتم چک‌لیست)
WP-24 (اصلاح سند تحویل) — ارزان و فوری؛ قبل از اعتماد به هر سند تولیدشده
  └─ P0: WP-01 (قفل‌شدگی استخر — بحرانی) → WP-22 (/metrics عمومی + trusted_proxies
        + require_worker + database_url) → WP-05 (mp.db/بهداشت) → WP-02 (زنجیرهٔ تأمین)
        → WP-03 (خطا + CSP) → WP-06 (R8/AAB) → WP-04 (چک‌لیست انتشار)
  └─ P1: WP-25 (گارد تکراری + sentinel + Semgrep) → WP-13 (قطعیت CI + lint)
        → WP-07 (جهش) → WP-08 (property + hypothesis + زمان‌بندی DAST)
        → WP-09 (کلاینت: golden/patrol/a11y/نوع/آستانهٔ پوشش) → WP-10 (قرارداد API
        + ماتریس مجوز + ورودی نامعتبر) → WP-11 (پول + ۲^۵۳−۱ + همزمانی کوپن)
        → WP-23 (کیوسک/چک‌این انتها‌به‌انتها) → WP-12 (وب/PWA/Electron + گیت web.yml)
        → WP-26 (بستهٔ موانع محیطی برای مالک)
  └─ P2: WP-14 (تکرار/مرده/پیچیدگی) · WP-15 (l10n/فونت/ایموجی) · WP-16 (آشوب + دریل restore)
        · WP-17 (بار + مقایسهٔ Postgres) · WP-18 (لایسنس) · WP-19 (بهداشت/ضدرگرسیون)
        · WP-20 (PII/provenance/رانش مستندات)
WP-21 (ممیزی خط‌به‌خط و جمع‌بندی خواسته‌های ۱ تا ۱۲) — همیشه آخر، بعد از سبز شدن WP-07/08/09
```

قواعد:
- **WP‑01 بر همه مقدم است** (تنها خطر بازِ با سابقه‌ی حادثه‌ی واقعی)، و **WP‑22 بلافاصله بعد از آن** (ارزان‌ترین کاهش خطر امنیتی/عملیاتی).
- **WP‑24 را زود انجام بده** (ارزان است و اعتماد به سند تحویل را برای بقیه‌ی نشست‌ها برمی‌گرداند) و **WP‑25** را قبل از WP‑14 (تا گارد تکراری و sentinel وارد آمار کد تکراری نشوند).
- **WP‑26 هر وقت secret لازم شد**: هر WP که به مانع محیطی خورد، یک ردیف در `OWNER-ACTION-PACK` می‌گیرد و ایجنت بدون توقف به WP بعدی می‌رود.
- هر P0 قبل از هر P1؛ WP‑14 و WP‑21 فقط بعد از WP‑07 (قاعده‌ی ۳‑۱۱).
- WP‑08 قبل از WP‑11 (propertyهای پولی پیش‌نیاز یکپارچگی پول‌اند).
- WP‑13 را زود انجام بده (ارزان است و قطعیت بقیه‌ی CI را تضمین می‌کند).
- WP‑15 بعد از WP‑09 تا goldenها با کلیدهای ترجمه بازنویسی نشوند.
- WP‑16/17/18/19/20 مستقل‌اند و می‌توانند موازی بروند.
- اگر وقت نرسید: به ترتیب اولویت برو و در `SESSION_HANDOFF.md` دقیقاً بنویس چه ماند و از کجا ادامه یابد.

---

## ۸) خط قرمزها — فقط با تأیید صریح مالک

در این موارد **متوقف شو و بپرس**؛ در بقیه‌ی موارد تصمیم بگیر و ادامه بده (۳‑۲).

1. **بازنویسی تاریخچه‌ی git** (`git filter-repo`/BFG/force‑push) — برای حذف کلید امضای افشاشده (`RELEASE-CHECKLIST.md:12`) یا هر تصویر/فایل حاوی داده‌ی واقعی. **آماده‌سازی کن، اجرا نکن**: یک سند اجرایی گام‌به‌گام با ترتیب «rotate/revoke → بازنویسی → ابطال توکن/کش → تأیید» بنویس.
2. **چرخش/ابطال هر کلید یا credential** (امضا، JWT، بیومتریک، GHCR، Dokploy، SMS، درگاه پرداخت) و هر تغییر در secrets.
3. **deploy واقعی، انتشار عمومی، ساخت release، یا push مستقیم به `main`** (فقط شاخه‌ی کاری + PR؛ `main` تنها شاخه‌ی دائمی است و merge باید با CI سبز باشد).
4. **حذف/تغییر داده‌ی کاربر** در هر محیطی، و هر مهاجرت مخرب (drop column/table) بدون مسیر رفت‌وبرگشت تست‌شده.
5. **تغییر `LICENSE`، متن‌های حقوقی/حریم خصوصی** (`FACEID-PRIVACY-TEXT.md`, `security/biometric-policy.md`, `DATA-RETENTION.md`) یا بخش حقوقی `NOTICE-THIRD-PARTY.md` — پیشنهاد بنویس، اعمال نکن.
6. **شل‌کردن هر گیت CI** یا کاهش هر آستانه (پوشش، WCAG، امنیتی، اندازه، پیچیدگی).
7. **افزودن وابستگی GPL/AGPL به آرتیفکت توزیعی**، یا هر سرویس/کلید پولی.
8. **تغییر تنظیمات GitHub** (branch protection، environments، «automatically delete head branches» — آیتم ۳۸ چک‌لیست صریحاً می‌گوید فقط مالک می‌تواند).
9. **دست‌زدن به داده‌ی واقعی پرداخت/کیف‌پول** در هر محیط غیرکاملاً ایزوله.

اگر موردی از این فهرست سر راه یک WP بود: بقیه‌ی WP را تا جایی که ممکن است انجام بده، آن بخش را `BLOCKED` با دلیل و گزینه‌ها ثبت کن (قاعده‌ی ۳‑۱۵) و به WP بعدی برو. **هرگز بیکار نمان.**

---

## ۹) گیت انتشار (تعریف انجام‌شدن کل پروژه)

کار وقتی تمام است که همه‌ی این‌ها **با شاهد اجرایی** برقرار باشند:

**خطرهای باز**
- [ ] ریشه‌ی قفل‌شدگی استخر SQLite پیدا و رفع شده، با تست بازتولید قبل/بعد و متریک+alert (WP‑01). اگر نیافت شد: `BLOCKED` با فهرست مظنون‌های رد‌شده.
- [ ] هر ۲۱ آیتم بازِ `RELEASE-CHECKLIST.md` بسته یا `BLOCKED` مستند (WP‑04).
- [ ] `mp.db` از مخزن خارج + گیت CI علیه commit شدن DB/keystore/.env (WP‑05).

**زنجیره‌ی تأمین و زمان اجرا**
- [ ] هر ایمیج: hadolint + Trivy/Grype + SBOM + cosign؛ `deploy.yml` فقط ایمیج امضاشده (WP‑02).
- [ ] GlitchTip فعال در بک‌اند/کلاینت/استودیو با تست redaction؛ CSP فعال و تست‌شده (WP‑03).
- [ ] release با R8/shrink + `.aab` + گیت اندازه + `analyze-size` (WP‑06).

**عمق تست**
- [ ] mutation score برای `engine/`، ماژول‌های مالی و `security/` اندازه‌گیری و قفل‌شده (WP‑07).
- [ ] ≥۱ property برای هر ۱۹ موتور + propertyهای پولی؛ `hypothesis` در dev deps و `dast.py` قابل اجرا روی محیط تازه (WP‑08).
- [ ] golden برای همه‌ی صفحات کلاینت + آستانه‌ی پوشش کلاینت + ≥۱ تست patrol در CI (WP‑09).
- [ ] `openapi.json` commit‌شده + گیت drift + oasdiff + قرارداد زنده‌ی کلاینت Dart + `dast.py` زمان‌بند + ماتریس مجوز/ورودی نامعتبر (نقص `-1` بسته) (WP‑10).
- [ ] تست مرزی ۲^۵۳−۱ در سه لایه + قاعده‌ی Semgrep پولی + قواعد گردکردن مستند/تست‌شده + همسانی مانده/دفترکل/audit log (WP‑11).
- [ ] Playwright E2E با جریان‌های مالی/مخرب روی داده‌ی مصنوعی (بستن `BLOCKED` گزارش QA) + axe + رگرسیون بصری + Lighthouse/بودجه‌ی باندل + تست‌های SW و Electron (WP‑12).
- [ ] صفر `npm ci || npm install`؛ lint استودیو فعال یا اسکریپت مرده حذف‌شده (WP‑13).

**کلاس جهانی**
- [ ] گزارش jscpd/knip/vulture/lizard با تعیین تکلیف همه‌ی یافته‌ها؛ گیت پیچیدگی و لایه‌بندی (WP‑14).
- [ ] l10n کامل + نقص ایموجی/فونت بسته + pseudo-locale (WP‑15).
- [ ] ≥۶ سناریوی آشوب + دریل restore با assert برابری داده (WP‑16).
- [ ] ≥۵ سناریوی بار جدید + مقایسه‌ی SQLite/Postgres + گیت N+1 (WP‑17).
- [ ] گیت خودکار لایسنس وابستگی‌ها + NOTICE همگام (WP‑18).
- [ ] صفر print/except/TODO/skip بی‌تکلیف + `.ci-baseline.json` + گیت ضد‌رگرسیون (WP‑19).
- [ ] PROVENANCE برای همه‌ی تصاویر + پویش PII به‌عنوان گیت + تست چرخه‌ی عمر retention (WP‑20).
- [ ] جدول ممیزی همه‌ی ماژول‌ها + تست طلایی هر خروجی + دیاگرام‌های sequence + `UI-INVENTORY.md` کامل + جدول «خواسته‌ی ۱ تا ۱۲ ← WP ← شاهد» (WP‑21).

**امنیت سطح تماس و پیکربندی (جدید در ۲.۱)**
- [ ] `/api/v1/metrics` از بیرون غیرقابل دسترس (تست)؛ اسکرپ فقط داخلی (WP‑22).
- [ ] `MP_TRUSTED_PROXIES` در production اجباری + تست دو سبد rate-limit + تست نادیده‌گرفتن XFF غیرمعتمد (WP‑22).
- [ ] `/health/ready` با worker مرده یا صف انباشته قرمز می‌شود؛ `require_worker` در production اجباری؛ alert روی `outbox_dead_letters` (WP‑22).
- [ ] `database_url`/`receipts_dir`/`public_base_url` در `validate_production_configuration`؛ ADR‑002 با اعداد Postgres در برابر SQLite به‌روز (WP‑22 + WP‑17).
- [ ] کیوسک/چک‌این: یا جریان کامل با تست E2E و golden حالت‌های شکست، یا ادعای مستند/تصویر اصلاح و در `BUILD-QUEUE.md` ثبت (WP‑23).
- [ ] `PROJECT-HANDOFF.md` بدون جدول خالی، بدون ادعای غلط، بدون تناقض داخلی + تست واحد برای `repowise_handoff.py` + `--check` در `ci.yml` + سند روی `main` (WP‑24).
- [ ] صفر گارد تکراری `require_permission` با گیت؛ تست «مجوز یک بار ارزیابی می‌شود»؛ صفر شناسه‌ی sentinel منفی و `422` برای شناسه‌ی ≤۰؛ ≥۵ قاعده‌ی Semgrep جدید با تست نمونه (WP‑25).
- [ ] `OWNER-ACTION-PACK` با هر ۵ مانع محیطی، هرکدام با دستور راستی‌آزمایی پس از انجام، و **صفر secret در سند**؛ job اختیاری JADX/apkanalyzer در `apk.yml` یا BLOCKED مستند (WP‑26).

**فرایند**
- [ ] `scripts/docs_gate.py` و `tools/mermaid-check` سبز؛ `SESSION_HANDOFF.md` به‌روز؛ یک گزارش `finn/reports/…` برای هر WP؛ `main` با CI سبز روی همان SHA (آیتم ۳۷ چک‌لیست).

---

## ۱۰) قالب گزارش هر WP

فایل: `finn/reports/wp<NN>-<slug>.md`

```markdown
# WP-<NN> — <عنوان>
تاریخ: <ISO> · شاخه/PR: <…> · اولویت: P0/P1/P2 · وضعیت: انجام‌شد / بخشی / BLOCKED

## چه شد
<۳ تا ۸ خط، فعل‌محور>

## شاهد اجرایی
- دستور: `<دقیق>` → خروجی/عدد: `<…>`
- CI run: <id/لینک> · تست‌های جدید: <نام‌ها> · گیت‌های اضافه: <job/step>
- مسیر evidence: <…>   (الگوی موجود: evidence/m60/*.json)

## پوشش خواسته‌های مالک
<کدام یک از موارد ۱ تا ۱۲>

## عدد پایه (قبل → بعد)
<coverage / mutation score / dynamic / as / print / except / TODO / skip / duplication / complexity / p95 / APK size / bundle size>

## تصمیم‌های خودکار
- <تصمیم> — چرا: <یک خط>

## BLOCKED — نیاز به تأیید انسانی
- <مورد> — دلیل دقیق: <…> — گزینه‌ها: <…> — پیشنهاد: <…>

## قدم بعدی برای نشست بعد
- <دقیق و قابل اجرا>
```

سبک شاهد را مطابق `evidence/m60/STATUS.md` نگه دار: «هر ادعا یا شاهد دارد (تست/CI/curl) یا برچسب **بازبینی دستی** می‌خورد.»

---

## پیوست A — ابزار اوپن‌سورس رایگان (راستی‌آزمایی‌شده، ۲۰۲۶‑۱۱‑۲۰)

> «dev» = ابزار توسعه/CI (GPL/AGPL مجاز) · «dist» = داخل آرتیفکت توزیعی (فقط MIT/Apache/BSD/ISC/MPL)
> موجود در پروژه: Gitleaks، Semgrep، bandit، pip-audit، schemathesis، Locust، k6، apktool، RepoWise، mermaid-check، Vitest، pytest، ruff.

| ابزار | لایسنس | ستاره | برای چه |
|---|---|---|---|
| `aquasecurity/trivy` | Apache‑2.0 (dev) | 39.5k | CVE ایمیج/وابستگی/IaC + SBOM + رازها |
| `anchore/grype` | Apache‑2.0 (dev) | 13.3k | اسکن CVE ایمیج/فایل‌سیستم |
| `anchore/sbom-action` | Apache‑2.0 (dev) | 0.3k | SBOM در Actions |
| `hadolint/hadolint` | GPL‑3.0 (dev) | 12.5k | لینت Dockerfile |
| `sigstore/cosign` | Apache‑2.0 (dev) | 6.4k | امضا + provenance ایمیج |
| `burke-software/GlitchTip` | MIT (dev) | 0.2k | error/crash tracking خودمیزبان |
| `boxed/mutmut` | BSD‑3 (dev) | 1.5k | mutation پایتون |
| `sixty-north/cosmic-ray` | MIT (dev) | 0.7k | mutation موازی پایتون |
| `stryker-mutator/stryker-js` | Apache‑2.0 (dev) | 3.4k | mutation TS |
| `HypothesisWorks/hypothesis` | MPL‑2.0 (dev) | 9.2k | property پایتون (+ رفع وابستگی اعلام‌نشده‌ی `dast.py`) |
| `dubzzz/fast-check` | MIT (dev) | 5.3k | property TS |
| `leancodepl/patrol` | Apache‑2.0 (dev) | 1.5k | تست on‑device فلاتر با dialogهای permission |
| `microsoft/playwright` | Apache‑2.0 (dev) | 100.5k | E2E استودیو/وب + رگرسیون بصری + axe |
| `dequelabs/axe-core` | MPL‑2.0 (dev) | 7.8k | a11y |
| `GoogleChrome/lighthouse-ci` | Apache‑2.0 (dev) | 7.2k | بودجه‌ی perf/a11y/SEO |
| `GoogleChrome/web-vitals` | Apache‑2.0 | 8.7k | متریک واقعی کاربر |
| `oasdiff/oasdiff` (+action) | Apache‑2.0 (dev) | 1.5k | گیت تغییر شکننده‌ی API |
| `Orange-OpenSource/hurl` | Apache‑2.0 (dev) | 19.3k | تست HTTP متنی با assert |
| `stoplightio/prism` | Apache‑2.0 (dev) | 5.1k | mock + اعتبارسنجی OpenAPI |
| `keploy/keploy` | Apache‑2.0 (dev) | 19.9k | ضبط ترافیک واقعی → تست + mock |
| `Shopify/toxiproxy` | MIT (dev) | 12.5k | تزریق latency/قطعی (آشوب) |
| `kucherenko/jscpd` | MIT (dev) | 6.6k | کد تکراری در ۲۲۰+ زبان (py+dart+ts همزمان) |
| `webpro-nl/knip` | ISC (dev) | 12.7k | کد مرده‌ی TS/React |
| `terryyin/lizard` | MIT (dev) | 2.6k | پیچیدگی cyclomatic چندزبانه |
| `rubik/radon` | MIT (dev) | 2.0k | متریک پیچیدگی پایتون |
| `vulture` (PyPI) | MIT (dev) | — | کد مرده‌ی پایتون |
| `import-linter/import-linter` | BSD‑2 (dev) | 1.3k | قوانین لایه‌بندی پایتون به‌صورت تست |
| `pahen/madge` | MIT (dev) | 10.2k | چرخه‌های وابستگی JS/TS |
| `repowise-dev/repowise` | AGPL‑3.0 (dev) | 8.2k | گراف/health/dead code/blast radius/C4 (در پروژه استفاده شده) |
| `oss-review-toolkit/ort` | Apache‑2.0 (dev) | 2.1k | انطباق لایسنس زنجیره |
| `aboutcode-org/scancode-toolkit` | Apache‑2.0 (dev) | 2.7k | لایسنس/کپی‌رایت دارایی‌ها |
| `pip-licenses` (PyPI) | MIT (dev) | — | لایسنس وابستگی‌های پایتون |
| `RSeidelsohn/license-checker-rseidelsohn` | BSD‑3 (dev) | 0.2k | لایسنس وابستگی‌های npm |
| `newren/git-filter-repo` | MIT (dev) | — | بازنویسی تاریخچه (**فقط با تأیید مالک**) |
| `zaproxy/zaproxy` | Apache‑2.0 (dev) | 16.2k | DAST کلاسیک (اگر در محیط نصب شد؛ جایگزین فعلی: `dast.py`) |
| `OpenHands/OpenHands` | MIT (dev) | 93.7k | ایجنت خودران برای پاس‌های حجیم |
| `Qwen/Qwen3-Coder-30B-A3B-Instruct` (HF) | Apache‑2.0 | — | مدل کد محلی رایگان برای پاس‌های حجیم ریفکتور |

**استفاده نکن (آرشیو/رکود):** `lost-pixel/lost-pixel` · `apiaryio/dredd` · `doyensec/electronegativity` · `CoatiSoftware/Sourcetrail` · `qodo-ai/qodo-cover` (unmaintained از ۲۰۲۵‑۰۶‑۱۵) · `EvoSuite/evosuite` · `danvk/source-map-explorer` · `jeremylong/DependencyCheck`.

---

## پیوست B — چک‌لیست ممیزی خط‌به‌خط

**برای هر ماژول/موتور** (۲۴ ماژول + ۱۹ موتور + بخش‌های کلاینت/استودیو) این جدول را در `docs/MuscleParadise/AUDIT-FINAL-2026-11-20.md` پر کن:

| ستون | محتوا |
|---|---|
| ماژول/مسیر | مثلاً `mp-app/backend/engine/safety.py` |
| اندازه | فایل/خط/تابع |
| ورودی‌ها و خروجی‌ها | توابع عمومی + امضا + نوع خروجی (خواسته‌های ۴ و ۵) |
| مصرف‌کننده‌ها | کدام endpoint/صفحه/موتور صدایش می‌زند (خواسته‌ی ۲ و ۶) |
| وابستگی‌ها | چه import می‌کند؛ چرخه دارد؟ |
| پوشش تست | واحد / یکپارچه / property / mutation / golden / E2E |
| تکرار | منطقش جای دیگری هم پیاده شده؟ (خواسته‌ی ۹) |
| کد مرده | تابع/پارامتر/شاخه‌ی بی‌استفاده (خواسته‌ی ۱۱) |
| پیچیدگی | عدد cyclomatic + اقدام ساده‌سازی (خواسته‌ی ۱۰) |
| پول/عدد بزرگ | فیلد ریالی؟ عبور از ۲^۵۳−۱؟ گردکردن؟ (WP‑11) |
| خطاها | همه‌ی مسیرهای شکست چه می‌کنند؟ بلعیده می‌شوند؟ |
| ایمنی/حریم خصوصی | داده‌ی حساس لمس می‌شود؟ redaction درست است؟ |
| عملکرد | کوئری/حلقه/همزمانی مشکوک؟ N+1؟ session باز؟ (WP‑01) |
| a11y و l10n | semantic label، کنتراست، اندازه‌ی هدف، ترجمه، RTL |
| اقدام | چه شد / چه باید بشود |
| شاهد | تست، CI run، عدد، مسیر evidence |

**برای هر عنصر UI** (خواسته‌ی ۸): یک ردیف در `docs/MuscleParadise/UI-INVENTORY.md` — شناسه · صفحه · نوع (دکمه/ورودی/سرچ‌بار/سوئیچ/لینک/انیمیشن) · مسیر فایل · stateها · تست widget · golden · on-device · E2E · a11y · l10n · رفتار خطا · وضعیت. پایه‌ی این جدول: `qa-report/buttons.json` (۱۰۱ دکمه در ۱۱ صفحه‌ی استودیو).

---

## پیوست C — دستورات آماده

```bash
# --- آماده‌سازی ---
git status --short --branch && git log --oneline -1
python3 scripts/docs_gate.py
(cd tools/mermaid-check && npm ci --no-audit --no-fund && node check.mjs)
pip install -e "mp-app/backend[dev]"
(cd mp-app/studio && npm ci)
(cd mp-app/client && flutter pub get)

# --- گیت‌های موجود (باید سبز بمانند) ---
cd mp-app/backend && ruff check . && ruff format --check . \
  && pytest --cov=. --cov-report=xml --cov-fail-under=70 && bandit -r . -q && pip-audit
(cd mp-app/studio && npm test && npm run build)
(cd mp-app/client && flutter analyze --no-fatal-infos && dart format --output=none --set-exit-if-changed . && flutter test --coverage)

# --- اندازه‌گیری اعداد پایه (بخش ۵) ---
git ls-files | wc -l
grep -rl 'matchesGoldenFile' mp-app/client | wc -l
grep -rl 'Semantics' mp-app/client/lib | wc -l
grep -rIn '\bdynamic\b' mp-app/client/lib | wc -l
grep -rInE ':\s*any\b' mp-app/studio/src | wc -l
grep -rIn 'print(' mp-app/backend --include=*.py | grep -v tests | wc -l
grep -rInE 'except Exception' mp-app/backend --include=*.py | wc -l
grep -rInE '(TODO|FIXME|HACK)' mp-app --include=*.py --include=*.dart --include=*.ts --include=*.tsx | wc -l
grep -rInE '(sbom|trivy|grype|hadolint|cosign|codeql|dependency-review|oasdiff)' .github/workflows/ | wc -l
grep -c '\- \[ \]' docs/MuscleParadise/RELEASE-CHECKLIST.md

# --- ابزارهای جدید (پس از نصب) ---
pip install mutmut hypothesis vulture radon import-linter pip-licenses freezegun
npx --yes jscpd --threshold 3 --reporters consoleFull,html --output .audit/jscpd \
  mp-app/backend mp-app/client/lib mp-app/studio/src
(cd mp-app/studio && npx --yes knip --reporter json > ../../.audit/knip.json)
lizard mp-app/backend mp-app/client/lib -C 15 -T cyclomatic_complexity=15 > .audit/lizard.txt
radon cc mp-app/backend -s -n C > .audit/radon.txt
mutmut run --paths-to-mutate mp-app/backend/engine && mutmut results
python3 mp-app/backend/scripts/dast.py --max-examples 20 --report evidence/dast-$(date +%F).json
trivy image <ghcr/.../backend:sha-…> --severity CRITICAL,HIGH --exit-code 1
oasdiff breaking docs/api/openapi.json docs/api/openapi.json --fail-on ERR
k6 run mp-app/tests/load/k6-gate.js --env BASE_URL=<staging>
repowise init --yes --no-prose && repowise export --format markdown   # در .audit/
```

## پیوست D — چرخه‌ی عمر این سند

**حالت ۱ — همه‌ی WPها باز:** از WP‑00 شروع کن و طبق بخش ۷ پیش برو.
**حالت ۲ — یک WP قبلاً انجام شده:** با راستی‌آزمایی شاهد (۳‑۱۳) «قبلاً انجام‌شده» ثبت کن و فقط گیت ضد‌رگرسیونش را اضافه کن.
**حالت ۳ — مخزن جلوتر از `662ff88` رفته:** اول `git diff --stat 662ff88..HEAD` را بخوان، سپس اعداد بخش ۵ را دوباره اندازه بگیر و سند را با اعداد تازه به‌روز کن.

**دستور بازتولید (برای مالک/ایجنت بیرونی):**
```
یک کلون فقط‌خواندنی از yousefghorbanian98-create/MP شاخه main در کامیت <sha> بگیر و این
اندازه‌گیری‌ها را دوباره انجام بده، سپس نسخه‌ی جدید سند را با اعداد تازه بنویس:
۱) فهرست workflowها و jobهای هرکدام
۲) grep برای sbom|trivy|grype|hadolint|cosign|codeql|dependency-review|oasdiff در workflows
۳) matchesGoldenFile، integration_test، patrol، شمارش Semantics در client/lib
۴) شمارش dynamic / as / ignore در client/lib و : any در studio/src
۵) analysis_options.yaml و tsconfig.json و strict بودنشان
۶) dev deps بک‌اند (hypothesis؟ mutmut؟ freezegun؟) و مقدار cov-fail-under
۷) grep برای sentry|glitchtip|rollbar|bugsnag و Content-Security-Policy
۸) isMinifyEnabled/isShrinkResources در build.gradle.kts و وجود .aab در CI
۹) print() غیرتست، except Exception، TODO/FIXME، تست‌های skip، stub
۱۰) فایل‌های l10n/ARB/intl
۱۱) سناریوهای k6 و آستانه‌ها + گزارش‌های load در qa-report/finn
۱۲) چک‌باکس‌های باز در RELEASE-CHECKLIST.md
۱۳) بزرگ‌ترین فایل‌های ترک‌شده، mp.db، تصاویر ui-previews و qa-report/screenshots
۱۴) ستون‌های پول در db/models (Integer/Numeric/Float)
۱۵) وضعیت «قفل‌شدگی استخر» در qa-report/FINAL-REPORT.md (بسته شد یا نه)
۱۶) گارد /api/v1/metrics (عمومی است یا نه) + تعداد sessionهایی که مانیتورینگ باز میکند
۱۷) MP_TRUSTED_PROXIES / MP_REQUIRE_WORKER / MP_DATABASE_URL در validate_production_configuration چک میشوند یا نه
۱۸) شمارش Depends(require_permission در هر روتر (گارد تکراری) + شناسه‌های sentinel منفی در استودیو
۱۹) تعداد صفحه‌های استودیو و وجود/نبود صفحهٔ کیوسک
۲۰) نقایص سند تحویل (PROJECT-HANDOFF.md): جدول مجوزها خالی؟ پیش‌فرض «(»؟ تناقض با §۱۰ خودش؟ مسیر اسکرین‌شات‌ها؟
هر حفره‌ای که بسته شده بود، WP مربوطه را «انجام‌شده» علامت بزن؛ هر حفره‌ی تازه، یک WP جدید بساز.
```

---

## پیوست E — نگاشت کامل ۶۳ مشکل ← بسته‌ی کاری

منبع فهرست: `share/MP-PROBLEMS-2026-11-20.md` (با شاهد خط‌به‌خط). **هیچ مشکلی بی‌صاحب نیست.**

**P0 (۹):** A1 قفل‌شدگی استخر ← **WP‑01** · A2 `/metrics` عمومی ← **WP‑22** · A3 `trusted_proxies` خالی/بی‌اعتبارسنجی ← **WP‑22** · A4 `mp.db` ترک‌شده ← **WP‑05** · A5 زنجیره‌ی تأمین صفر گیت ← **WP‑02** · A6 نبود crash reporting ← **WP‑03** · A7 نبود CSP ← **WP‑03** · A8 نبود R8/AAB ← **WP‑06** · A9 ۲۱ آیتم باز چک‌لیست ← **WP‑04** (+WP‑26)

**P1 (۲۲):** B1 کیوسک ناقص ← **WP‑23** · B2 گارد تکراری ← **WP‑25** · B3 sentinel `1-` ← **WP‑25** (+WP‑10) · B4 همزمانی کوپن روی Postgres ← **WP‑11** (+WP‑17) · B5 مرز `2^53−1` ← **WP‑11** · B6 قواعد گردکردن ← **WP‑11** (+WP‑08) · B7 نبود golden/آستانه پوشش کلاینت ← **WP‑09** · B8 نبود integration/patrol ← **WP‑09** · B9 a11y کلاینت ← **WP‑09** · B10 سخت‌گیری نوع Dart ← **WP‑09** · B11 اسکریپت lint مرده ← **WP‑13** · B12 `npm ci || npm install` ← **WP‑13** · B13 `hypothesis` اعلام‌نشده + DAST بی‌زمان‌بند ← **WP‑08** · B14 نبود `openapi.json`/oasdiff ← **WP‑10** · B15 live-contract فقط استودیو ← **WP‑10** · B16 ماتریس مجوز/مالکیت ← **WP‑10** · B17 `require_worker` ← **WP‑22** · B18 `database_url` ← **WP‑22** · B19 سه `except Exception: pass` ← **WP‑19** · B20 `web.yml` فقط dispatch ← **WP‑12** · B21 Electron/SW سخت‌سازی ← **WP‑12** · B22 گیت بار نازک ← **WP‑17**

**P2 (۱۹):** C1 ۶۷۰ یافته‌ی سلامت ← **WP‑14** (+WP‑21) · C2 شش نقطه‌ی داغ critical ← **WP‑14** · C3 توابع بزرگ ← **WP‑14** (+WP‑21 ساده‌سازی) · C4 `io_in_loop` ← **WP‑14** · C5 ۳۵ کد مرده ← **WP‑14** · C6 ۲۵ رانش مستندات ← **WP‑20** (+WP‑24) · C7 نبود ابزار تکرار/مرده/پیچیدگی در CI ← **WP‑14** · C8 نبود mutation ← **WP‑07** · C9 نبود property ← **WP‑08** · C10 نبود l10n ← **WP‑15** · C11 بنر به‌روزرسانی + ایموجی ← **WP‑15** (+WP‑09 برای بنر) · C12 ۴۱ `print()` ← **WP‑19** · C13 ۴۸ TODO ← **WP‑19** · C14 ۶ تست skip ← **WP‑19** · C15 نبود گیت لایسنس ← **WP‑18** · C16 نبود آشوب + دریل restore ← **WP‑16** · C17 provenance تصاویر ← **WP‑20** · C18 قواعد Semgrep ناقص ← **WP‑25** · C19 فایل‌های سنگین/حجم مخزن ← **WP‑05**

**نقص‌های سند تحویل (۸):** D1 جدول مجوزهای خالی · D2 پیش‌فرض CORS «(» · D3 ادعای غلط تریگر `apk.yml` و تناقض با §۱۰ · D4 مسیر اشتباه روتر `face` · D5 مرج‌نشده و `--check` بی‌گیت · D6 مسیر اشتباه اسکرین‌شات‌ها · D7 سه snapshot بدون تعیین معتبر · D8 جدول ماژول‌های ناقص/گمراه‌کننده ← **همه WP‑24**

**موانع محیطی (۵):** X1 secretهای `MP_ANDROID_*` · X2 چرخش کلید signing افشاشده (**خط قرمز ۱ و ۲ — اجرا نکن، فقط آماده کن**) · X3 Flutter در sandbox · X4 دستگاه واقعی/پرداخت/SMS/Valkey/PostgreSQL/Prometheus · X5 نبود JDK برای JADX ← **همه WP‑26** (+WP‑04 برای X1/X2)

**پوشش خواسته‌های ۱ تا ۱۲ مالک:** ۱ خط‌به‌خط ← WP‑21 (+WP‑14) · ۲ سیم‌کشی ← WP‑23, WP‑10, WP‑21 · ۳ موتورها/ورک‌فلوها ← WP‑07, WP‑08, WP‑21 · ۴ خروجی‌ها ← WP‑21 (تست طلایی هر خروجی) · ۵ توابع/پارامترها ← WP‑14, WP‑21 · ۶ همبستگی کلی/جزئی ← WP‑14 (import-linter/madge/نقشه‌ی ماژول), WP‑21 · ۷ انیمیشن/اینتراکشن ← WP‑09 (golden/patrol/فریم‌ریت), WP‑12 · ۸ سرچ‌بارها و تک‌تک دکمه‌ها ← WP‑09, WP‑12, WP‑21 (`UI-INVENTORY.md` بر پایه‌ی `qa-report/buttons.json`) · ۹ کد روی کد ← WP‑14 (jscpd), WP‑25 (گارد تکراری) · ۱۰ ساده‌سازی توابع ← WP‑14, WP‑21 · ۱۱ کد مرده ← WP‑14, WP‑19 · ۱۲ تست و اورلود ← WP‑16 (آشوب), WP‑17 (بار), WP‑07/08/09/10/12

---

**پایان سند.** از WP‑00 شروع کن، **WP‑24 را زود انجام بده** (سند تحویل را قابل اعتماد می‌کند)، و **WP‑01 (قفل‌شدگی استخر اتصال) را بر هر کار دیگری مقدم بدان** و بلافاصله بعد از آن **WP‑22**. همه‌ی ۲۷ بسته (WP‑00…WP‑26) را انجام بده، گزارش هرکدام را در `finn/reports/wp<NN>-<slug>.md` بنویس، و در پایان جدول «خواسته‌ی ۱ تا ۱۲ ← WP ← شاهد» را در `docs/MuscleParadise/AUDIT-FINAL-2026-11-20.md` بگذار. هیچ سؤالی از مالک نپرس مگر در موارد بخش ۸؛ موانع محیطی را به‌جای توقف، در `OWNER-ACTION-PACK-2026-11-20.md` (WP‑26) جمع کن.
