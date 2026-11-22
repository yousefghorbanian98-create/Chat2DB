# چک‌لیستِ مالک — کلِ کارهای پیشِ رو در شش دسته

- **تاریخ:** ۲۰۲۶‑۱۱‑۲۱ · **منبعِ تصمیم‌ها:** باکسِ سؤالِ شش‌گانه (پاسخِ مالک) + الحاقیهٔ `MP-SCENARIO-A1.4-2026-11-21.md`
- **قاعدهٔ این سند:** هر قلم یا «سنجه‌شده» است یا صریحاً «باید سنجیده شود». هیچ عددِ تخمینی به‌عنوانِ واقعیت نیامده.
- **مخاطب:** مالکِ محصول. بخشِ بیلدر در `MP-SCENARIO-A1.4-2026-11-21.md` بخشِ B است.

## دستهٔ ۱ — فقط تو می‌توانی انجام دهی (کلید، حساب، تصمیم، merge)

| # | کار | چرا فقط تو | وضعیت |
|---|---|---|---|
| ۱٫۱ | ~~پاک‌کردنِ چهار secretِ امضای اندروید + variableِ `MP_ANDROID_CERT_SHA256`~~ — **باطل شد؛ چیزی برای پاک‌کردن نیست** | **سنجهٔ مالک در `2026-11-21`:** همهٔ صفحه‌های secrets/variables **خالی** بودند. تأییدِ من از خودِ مخزن: گامِ «Prepare dedicated release signing material» با `set -euo pipefail` و `test -n "$KEYSTORE_B64" && … \|\| exit 1` نوشته شده ⇒ در نبودِ secret **به‌طورِ قطعی** شکست می‌خورد. گاه‌شمار: گیتِ امضا در `8e72de9` @ `2026-11-18 20:28:12` آمد، اولین قرمزی `20:28:25` (۱۳ ثانیه بعد)، آخرین سبز `2026-11-16` یعنی **پیش از** گیت ⇒ `apk.yml` ساختاراً غیرقابلِ موفقیت است. **خبرِ خوب:** مادهٔ امضا هرگز در GitHub نبوده ⇒ صفر نشتی، صفر پنجرهٔ تعرض، چیزی برای rotate کردن نیست | **بسته — بی‌اثر** |
| ۱٫۲ | تأییدِ نهاییِ حذفِ `.github/workflows/apk.yml` (۴ `uses:`) **و اختیارِ `AD‑21`** (حذفِ یک تست در همان commit) | حذفِ workflow یک تغییرِ دامنهٔ محصولی است؛ سنجه شد که حذفش `test_release_signing_policy.py::test_release_build_is_guarded_and_audits_all_output_apks` را با `FileNotFoundError` می‌شکند و فهرستِ ممنوعه «حذفِ تست» را منع کرده ⇒ بدونِ اختیارِ تو بیلدر در بن‌بست می‌ماند | باز — بیلدر اجرا می‌کند |
| ۱٫۳ | ~~آیا MP زنده است؟~~ — **جواب داده شد: «تا امروز حتی یک عضو هم نداشته، فقط خودم یک بار تستش کردم»** | — | **بسته · `2026-11-21`** ⇒ سنجهٔ پشتیبانِ من: `deploy.yml` **`total_count = 0` اجرا** و `environments = 0` در حالی که خودِ workflow ‏`environment: ${{ inputs.target }}` و `APP_URL`/`DOKPLOY_WEBHOOK` غیرخالی را الزام می‌کند ⇒ **MP هرگز هیچ‌جا استقرار نیافته**. نتیجه: هیچ سطحِ حملهٔ زنده‌ای وجود ندارد و `F‑01`/`F‑02`/`F‑06`/`F‑08`/`F‑09` امروز توسط هیچ‌کس قابلِ سوءاستفاده نیستند |
| ۱٫۴ | تصمیمِ `card_number` در `C1`: رمزنگاریِ کامل یا فقط mask ذخیره‌شدن | تصمیمِ محصولی؛ بیلدر به‌شکلِ `AD-n` ثبت می‌کند | باز |
| ۱٫۵ | روشن‌کردنِ تصمیمِ بازِ کیوسک/گیتِ ورود (تصمیمِ ۲ = «نامعلوم») | فقط تو می‌دانی؛ با یک آزمونِ دستگاه بسته می‌شود | باز — تا بسته نشود، PWA باید کیوسک‌پذیر بماند |
| ۱٫۶ | merge در **دو دسته + یک کارزار**، فقط پس از داوریِ عددیِ من | سیاستِ انتخابیِ خودت (`review_then_merge`) | جاری |
| ۱٫۷ | دامنه/HTTPS/مقصدِ استقرار برای سطحِ وبِ عضو (`B0`) | زیرساختِ بیرونِ مخزن | باز — `web.yml` artifactِ `muscleparadise-web` را می‌سازد ولی compose هیچ سرویسی برای serve کردنش ندارد |
| ۱٫۸ | اگر روزی Play/App Store خواستی: حساب و هزینه (۲۵ دلار یک‌بار / ۹۹ دلار سالانه) + انطباقِ target API 36 | حسابِ انسانی | در سناریوی فعلی **منتفی** |
| ۱٫۹ | **روشن‌کردنِ Dependabot alerts** از تبِ **Security** مخزن | — | ✅ **انجام شد · `2026-11-21T23:39Z`** — اثباتِ سنجه‌شده: همان endpoint پاسخِ «**Dependabot alerts are disabled for this repository**» را به «**Resource not accessible by integration**» (`403`) تغییر داد. پیامِ اول فقط وقتی برمی‌گردد که قابلیت **خاموش** باشد؛ پیامِ دوم یعنی قابلیت **روشن** است و توکنِ ممیزی scope خواندنش را ندارد. اکنون رفتارش با `secret-scanning/alerts` و `code-scanning/alerts` یکی شده (هر سه `403`) |
| ۱٫۹٫۱ | **«Dependabot security updates» را روشن نکن** (همان تب، کلیدِ دوم) | این کلید PRِ **bumpِ خودکارِ وابستگی** می‌سازد ⇒ مستقیماً با ممنوعیتِ «bump وابستگی» و با `AD‑22` (فریزِ نسخه‌ها در `constraints.txt`) تضاد دارد. سنجهٔ الان: ‏`security_and_analysis` هر دو فیلد `null` · **PR بازِ dependabot = ۰** از ۱ PR باز ⇒ فعلاً روشن نیست. alerts (دیدن) لازم داری، security updates (تغییر دادن) نه | ⚠️ **روشن نکن** |
| ۱٫۱۰ | **روشن‌کردنِ secret scanning و push protection** اگر خاموش‌اند (برای مخزنِ public رایگان است) | عاملِ ممیزی `403` می‌گیرد و نمی‌تواند وضعیتش را بخواند ⇒ فقط تو می‌بینی | باز |
| ۱٫۱۰٫۱ | ~~اجازهٔ allowlist برای `secret-scan`~~ — **`AD‑23` صادر شد** با پنج شرط؛ مکانیزم `.gitleaksignore` و تستِ سلامتِ گیت از قبل در مخزن بود | جزئیات در A1.4 §B‑۴٫۶ | ✅ صادر شد |
| ۱٫۱۰٫۲ | تصمیم دربارهٔ **`F‑33`**: اسکنرِ secret در CI ضعیف‌تر از تستِ خودش است (چهار پرچمِ `--log-opts=--all`، `--redact=100`، `--ignore-gitleaks-allow`، `--gitleaks-ignore-path` را ندارد) | سنجه شد؛ هم‌ترازی یک‌خطی است ولی سطحِ سخت‌گیریِ گیت را عوض می‌کند ⇒ اختیارِ جدا می‌خواهد | باز |
| ۱٫۱۱ | ~~تصمیم دربارهٔ `F‑32`~~ — **`AD‑22` صادر شد** (`2026-11-21` شب) | جزئیاتِ اجرا در A1.4 §B‑۴٫۶ | ✅ صادر شد — بیلدر اجرا می‌کند |
| ۱٫۱۲ | تصمیم دربارهٔ افزودنِ **CodeQL** (code scanning) | **سنجه شد:** از هفت workflow هیچ‌کدام CodeQL نیست ⇒ اسکنِ کد اصلاً پیکربندی نشده | باز — کم‌اولویت‌تر از ۱٫۹ چون ممیزیِ من semgrep را دستی اجرا کرد |

## ⚠️ هشدارِ فوریِ `2026-11-21T23:40Z` — PR #23 باز، غیرِ draft، و `main` هیچ گیتِ اجباری ندارد

| سنجه | مقدار |
|---|---|
| PR باز | **`#23`** · `arena/da474b65-mp` → `main` · ساخته‌شده `2026-11-20T20:52:51Z` · عنوان: «دیاگرام‌های وضعیت فعلی (diagram-design) — **بدون merge**» |
| `draft` | **`false`** |
| `mergeable` | **`true`** |
| `mergeable_state` | **`unstable`** |
| اندازه | **۴۶ commit** · **+۱۰۳٬۱۰۹/−۶۶۶** در **۲۸۶ فایل** |
| checks روی tip | **۸ failure · ۲ skipped · ۶ success** |
| `rulesets` روی مخزن | **`[]`** — یعنی خالی (این یکی را توانستم بخوانم، `403` نبود) |
| `branches/main/protection` | `403` برای توکنِ ممیزی ⇒ قابلِ تعیین نیست |
| `allow_auto_merge` / `allow_merge_commit` / … | همه `null` در پاسخِ API |

**استنتاج (صریحاً به‌عنوانِ استنتاج، نه سنجهٔ مستقیم):** در API گیت‌هاب `mergeable_state = unstable` یعنی «قابلِ merge با checkهای **قرمزِ غیرِ اجباری**»؛ اگر آن checkها **required** بودند وضعیت `blocked` می‌شد. پس به‌احتمالِ قوی **`main` هیچ status check اجباری ندارد** و `rulesets` هم خالی است ⇒ **این PR با ۸ گیتِ قرمز، یک کلیک با merge شدن فاصله دارد.**

**سه اقدام، به ترتیبِ اولویت:**

| # | اقدام | چرا |
|---|---|---|
| ۱ | ~~PR #23 را merge نکن / Convert to draft بزن~~ — **مالک آن را بست** | ✅ **انجام شد · `closed_at = 2026-11-21T23:44:31Z`** و این **محکم‌تر** از draft است: PR بسته بدونِ بازگشایی merge نمی‌شود. سه آزمونِ سلامت: (الف) `merged = false` و `merged_at = null` ⇒ **هر زمان قابلِ بازگشایی** است و چیزی از دست نرفته؛ (ب) شاخهٔ `arena/da474b65-mp` سرِ جایش است، tip همان `9bfc99d6f27f` @ `23:22:15Z`، **۴۶ جلو / ۰ عقب** نسبت به `main`؛ (ج) ‏`ci.yml` تریگرِ `push: branches: [main, "arena/**"]` دارد **علاوه بر** `pull_request` ⇒ CI با بسته‌شدنِ PR از کار نمی‌افتد. پاداش: پیش‌تر هر push **دو** اجرا می‌ساخت (`event=push` و `event=pull_request` در `23:22:22Z` و `23:22:18Z`)؛ از این پس **یک** اجرا ⇒ مصرفِ runner نصف و قرمزیِ تکراری حذف |
| ۲ | روی `main` **required status checks** بگذار: ‏`backend` · `live-contract` · `secret-scan` · `studio` · `client-flutter` · `Documentation links and handoff` · `e2e-api` · `Client — pinned SDK…` | مسیر: Settings ← Branches ← Branch protection rules ← ‏`main` ← «Require status checks to pass before merging» ← «Require branches to be up to date». این همان معیارِ «گیتِ بلاک‌کننده» است که در دستهٔ ۶ به‌عنوانِ هدفِ کلاسِ جهانی آمده. توکنِ من `403` می‌گیرد ⇒ فقط تو می‌توانی |
| ۳ | بازبینیِ این PR را **با diff نخوان** | ‏۱۰۳٬۱۰۹ خط افزوده که بخشِ عمده‌اش dumpِ ماشین‌ساختِ شاهد است (`WP 0.1` به‌تنهایی ۸۲٬۶۱۲ خط در ۱۱۵ فایل). هیچ انسانی این را بازبینی نمی‌کند ⇒ بازبینی باید **گیت‌محور** باشد (همان روشِ داوریِ عددیِ من)، نه diff‌محور |
| ۴ | **هشدارِ باقی‌مانده: بستنِ PR از `main` محافظت نمی‌کند** | ‏`rulesets = []` سنجه شد و `branches/main/protection` برای توکنِ ممیزی `403` است ⇒ به‌احتمالِ قوی pushِ مستقیم به `main` و همچنین ساختنِ یک PR تازه و merge کردنش با checkهای قرمز هنوز ممکن است. **اقدامِ ۲ (required status checks) حالا مهم‌تر از پیش است، نه کم‌تر** |
| ۵ | تأییدِ جانبیِ روشن‌شدنِ Dependabot | سنجهٔ تصادفی ولی قاطع: اجرای `event=dynamic` به نام **«Graph Update: pip in /mp-app/backend»** روی `main` در `2026-11-21T23:30:39Z` با نتیجهٔ **success** — یعنی گیت‌هاب همین الان دارد وابستگی‌های پایتونِ بک‌اند را برای Dependabot فهرست می‌کند. این تأییدِ مستقلِ اقدامِ ۱٫۹ است، قوی‌تر از تغییرِ پیامِ `403` |

**یک نکتهٔ ترتیبی:** تا وقتی required checks گذاشته نشده، هر push تازهٔ بیلدر می‌تواند روی شاخه‌ای بنشیند که یک کلیک با `main` فاصله دارد. پس اقدامِ ۲ پیش از ادامهٔ حلقه انجام شود.

## دروازهٔ اولین عضو — حداقلِ مطلق پیش از اولین استقرار یا اولین عضوِ واقعی

چون سنجه شد که MP **هرگز استقرار نیافته** و **صفر عضو** دارد، فوریت از «امشب» به «پیش از اولین عضو» تغییر می‌کند. این **فرصت** است نه خطر: هیچ داده‌ای برای از دست دادن نیست.

| # | قلم | چرا برای اولین عضو لازم است | وضعیت |
|---|---|---|---|
| ۱ | `F‑02` — پیش‌فرضِ fail-open و echo شدنِ `dev_code` | بدونِ آن هر کسی می‌تواند برای هر شماره‌ای حساب بسازد | باز (`WP 1.2`) |
| ۲ | `F‑01` — اعتماد به `X-Forwarded-For` در rate-limit | ۳۰/۳۰ OTP پذیرفته، ۲۲۸٫۴ حدس/ثانیه ⇒ اولین عضو یعنی اولین هدف | باز (`WP 1.1`) |
| ۳ | `F‑06` — `/api/v1/metrics` بدونِ احراز | ۳۴۶ خط و ۱۲ خانوادهٔ متریک به هر رهگذر | باز (`WP 1.4`) |
| ۴ | `F‑09` — مبلغ در `2^53+1` | اولین پرداختِ واقعی | باز (`WP 1.5`) |
| ۵ | `F‑08` — `logout-all` بدونِ `sid` | اولین نشستِ واقعی | باز (`WP 1.3`) |
| ۶ | **سبز شدنِ هر سه jobِ قرمزِ CI** | ‏`live-contract` با exit 7 یعنی ممکن است اپ اصلاً بالا نیاید | ❌ قرمز روی `9bfc99d6f27f` |
| ۷ | `B0` — مقصدِ استقرار برای artifactِ موجودِ وب | تا این نباشد «اولین عضو» هیچ راهِ ورودی ندارد | باز |

**چیزهایی که با صفر عضو از فهرستِ فوری خارج می‌شوند** (نه نادیده — فقط عقب‌تر):

- **خطرِ کارزارِ `C` فرو می‌ریزد.** دادهٔ تولیدی نیست ⇒ **هیچ مهاجرتِ داده‌ای، هیچ پنجرهٔ cutover، هیچ dual-write و هیچ تمرینِ بازیابی روی دادهٔ واقعی لازم نیست.** ترسناک‌ترین بخشِ `C3` باطل است؛ تمرینِ بازیابی فقط روی دادهٔ مصنوعی معنا دارد.
- **`F‑30` (ذخیرهٔ plaintextِ `card_number`) و همهٔ قلم‌های حریمِ خصوصی (`face_templates`, `biometric_consents`) امروز صفر تعرضِ واقعی دارند** چون آن جدول‌ها خالی‌اند ⇒ `C1` به «پیش از اولین پرداخت» موکول می‌شود، نه «همین حالا».
- **تصمیمِ ③ تأیید و قوی‌تر شد:** هیچ APK‌ای پخش نشده ⇒ تغییرِ قرارداد (۲۰۰→۴۲۲/۴۰۴) بدونِ `min_client_version` آزاد است.
- **`C2` و `B1` می‌توانند موازی شوند** (پیش‌تر «دو کارزار هم‌زمان ممنوع» بود) چون ریسکِ داده‌ایِ `C` با صفر عضو نزدیکِ صفر است. این **گزینه** است نه دستور؛ اگر ترتیبی را ترجیح می‌دهی همان ترتیبِ قبلی درست است.
- **`AD‑23`** (allowlist مشروط برای `secret-scan`) را در بخشِ B‑۴٫۵ سندِ A1.4 ببین — تا صادر نکنی، بیلدر حق ندارد گیت را دست بزند.

## دستهٔ ۲ — بیلدرِ بی‌ناظر (با گیتِ عددی، یک commit به ازای هر بسته)

**۲‑الف · فوری (پیش از هر بستهٔ تازه):**
1. بستنِ دو `PARTIAL`: ‏`WP 2.5` (اجرای semgrep روی `mp-silent-except-pass` + سه محلِ `scripts/dast.py:79,174,180` + نامِ `mp_metrics_scrape_errors_total` + بازتابِ `/health/ready`) و `WP 3.2` (افزودنیِ پراب برای `fastapi_default_detail`، عددِ ۷۱ → ۰، ثبتِ شعاعِ تأثیرِ ۴ `raise HTTPException` در `devtools/sandbox_bank.py`).
2. تفکیکِ `WP 4.6`: نیمهٔ استودیو انجام شود (`pages/Nutrition.tsx:50`، `mp-ts-float-money`)؛ نیمهٔ دارت (چهار قاعدهٔ `mp-dart-*`) ‏`DEFERRED(D-n)`.
3. فریزِ عملکردیِ `mp-app/client` در `DECISIONS.md`.

**۲‑ب · سپس:** ‏`WP 3.1` (F‑25) با `app/id_floor.py` پس از مسیریابی، `422` و `code="invalid_id"` ⇒ `unexpected_2xx_on_bad_id` از **۴۸** به **۰**.

**۲‑ج · سپس:** ‏`WP 0.1` (۴۹ ردیف، سه وضعیتِ مجاز، بدونِ `PARTIAL`) · `WP 0.2` (ماتریسِ ۱۶۳×۷ ⇒ **۶۰۲** مخالفت به **۰** در ۱٬۱۴۱ سلول) · فازِ ۱ (پنج Critical).

**⟵ نقطهٔ بررسیِ ۱:** داوریِ عددیِ من → merge دستهٔ ۱ (فازِ ۰ + فازِ ۱) → **تازه** A1.4 را به بیلدر بده (چون آن سند ممنوعیتِ `HARD-STOP` روی schema/migration را برمی‌دارد و این اجازه نباید پیش از بسته‌شدنِ Criticalها فعال شود).

**۲‑د · پس از نقطهٔ بررسیِ ۱:** ‏`D1` (حذفِ `apk.yml` + SHA-pinning ‏**۳۸/۳۸** + پینِ `flutter-version` در `web.yml` و `client-format-fix.yml`) · `C0` (سندِ دسته‌بندیِ ۶۵ ردیفی + دو تستِ گیت + خطِ پایهٔ تخلفِ مرزِ ماژول) · فازِ ۲ · فازِ ۳ · فازِ ۴ (نیمهٔ استودیو) · `C1` (**پس از** `WP 1.2`/`F‑02`، چون کلیدِ رمز از `settings.secret_key` مشتق می‌شود: `security/crypto.py:52`) · `B0` (سرویسِ `client-web` یا مسیرِ static در `infra/Caddyfile` + smoke test).

**⟵ نقطهٔ بررسیِ ۲:** داوریِ من → merge دستهٔ ۲.

## دستهٔ ۳ — من (ممیزی و داوری)

1. **داوریِ عددی در هر نقطهٔ بررسی** — از روی diff و خروجیِ خام، نه از روی گزارشِ بیلدر. دلیلِ سنجه‌شدهٔ این قاعده: دو commitِ `0afd240` و `8926fcd` هر دو «انجام شد» گزارش شدند و هر دو PARTIAL بودند.
2. **نگهداریِ اسنادِ ماندگار** در `handoff/` — کیتِ منجمد (`486,358` بایت / `9a192500…`؛ بازتولید با ژنراتور همان بایت‌ها می‌دهد) + الحاقیه‌ها.
3. **تصحیحِ علنیِ سندِ خودم وقتی غلط است.** تا امروز سه مورد: شمارِ `RUF100` (۷۲/۵۹/۳۹ وابسته به پیکربندی)، الگوی `lstrip("+-")` برای کفِ شناسه (‏`-1` را `1` می‌کرد و می‌پذیرفت)، و شدتِ `F‑30` (که «نشت از API» نیست چون مسیرِ خواندن هم کارت را mask می‌کند هم `secret_key` را برنمی‌گرداند).
4. **سنجهٔ تازه وقتی لازم شود** — مانند ۴۲ `uses:` با ۰ پینِ SHA، ۵۹ path param با `int` خام در برابرِ ۶ رشته‌ای، ۱۸ فایلِ مدلِ دامنه‌محور برای ۶۴ جدول، ۲۳ `batch_alter_table`.
5. **نوشتنِ برنامهٔ عددیِ کارزارهای بزرگ** (‏`C` و `B`) با گیت به ازای هر مرحله، پیش از شروعِ آن‌ها.

## دستهٔ ۴ — دو کارزارِ بزرگ (بازبینیِ جدا، ترتیبِ اجباری)

### کارزارِ C — Postgres و مرزهای داده
خطِ پایهٔ سنجه‌شده: **۰ سرویسِ Postgres در `infra/docker-compose.yml`** (امروز: `backend`, `studio`, `backup`, `valkey 9.1.3`, `valkey-exporter`, `prometheus v3.16.0`, `ollama 0.40.16`) · **۳۸ migration** · **۲۳ `batch_alter_table`** · **۲۳ `pragma`** · **۱٬۲۵۲ تست سبز روی SQLite** · پوششِ لایهٔ `db` ‏**۷۰٫۴۰٪** (ضعیف‌ترین پس از `scripts` ‏۴۶٫۲۲٪) · سناریوهای چنددیتابیسی در ممیزی **BLOCKED** بودند.

| مرحله | خروجیِ تحویلی | گیت |
|---|---|---|
| `C2` | **یک عدد**: «X تست از ۱٬۲۵۲ روی Postgres شکست» | تا این عدد ثبت نشود، `C3` شروع نشود؛ هیچ کدِ محصولی جز تنظیماتِ اتصال عوض نشود |
| `C3` | خنثی‌سازیِ ۲۳ `batch_alter_table` و ۲۳ `pragma` · جایگزینیِ `journal_mode=wal`/`foreign_keys=1` · سرویسِ `backup` از «کپیِ فایلِ SQLite» به `pg_dump` | ‏`alembic upgrade head` روی Postgres بدونِ خطا + هر ۱٬۲۵۲ تست سبز + `EXPLAIN` روی سه پرس‌وجوی داغ + **یک تمرینِ بازیابیِ کامل با زمانِ سنجه‌شده** |
| `C4` | هفت schema مطابقِ ۱۸ فایلِ مدل · نقشِ DB محدود (اپ روی `auth.*` جز از view/تابعِ باریک `SELECT` ندارد) · partition ماهانهٔ ۱۴ جدولِ پرحجم · `pg_dump -n` برای retention تفکیک‌شده | گیتِ دسترسی: اتصالِ اپ **نمی‌تواند** `auth.otp_codes` را مستقیم بخواند |
| قانونِ شواهد | اعدادِ بار/زمان‌بندیِ موجود در `04-evidence/raw/` همه روی SQLite سنجه شده‌اند | پس از `C3` **re-baseline** کن و برچسبِ «دورانِ SQLite» بزن؛ اعدادِ قدیمی را به‌عنوانِ ستونِ «قبل» نگه دار |

### کارزارِ B — کلاینتِ عضو با TypeScript/PWA
سنجهٔ کاری که جایگزین می‌شود: **۷۳ فایلِ دارت / ۱۷٬۲۲۹ خط** (که ۴۴ فایل / ۱۱٬۸۴۵ خطش در `client/lib` است) در **۱۷ حوزهٔ عملکردی** با ۲۹ فایلِ تست — یعنی هم‌اندازهٔ کلِ استودیو (۱۰۱ فایلِ TS/TSX / ۱۷٬۱۵۳ خط).

| مرحله | محتوا | گیت |
|---|---|---|
| `B0` | مقصدِ استقرار برای artifactِ **موجودِ** `muscleparadise-web` | یک URL واقعی + smoke test در CI — بدونِ نوشتنِ یک خط کلاینتِ تازه |
| `B1` | اسکلتِ PWA (فقط npm ⇒ **در همین چت قابلِ توسعه و تست**) + کلاینتِ تولیدشده از OpenAPI (۱۶۳ عملیات) + manifestِ نصب‌پذیر و کیوسک‌پذیر | ‏`tsc` ۰ خطا + تستِ واحد + Lighthouse/PWA معیارِ مشخص |
| `B2..Bn` | ۱۷ حوزه به ترتیبِ اولویت | هر حوزه فقط وقتی مهاجرت‌شده است که آزمونِ برابریِ قراردادش سبز باشد |
| پایانِ B | حذفِ `mp-app/client` + `client-format-fix.yml` (۵ `uses:`) + چهار قاعدهٔ `mp-dart-*` از `semgrep-mp.yml` + **سه فایلِ تست در همان commit** | ‏`pytest --collect-only -q` ⇒ **۰ خطایِ جمع‌آوری** و `N_after == N_before − 59` · گیتِ `WP 0.8` از **۳۸/۳۸** به **۳۳/۳۳** — سنجه شد که حذفِ `client` سه خطایِ جمع‌آوری می‌دهد و pytest پیش‌فرض **کلِ سوئیت را `Interrupted` می‌کند** |

**اولویتِ ۱۷ حوزه:** ‏`auth` ← `home`/`today`/`checkin` ← `progress`/`nutrition`/`assessment14`/`bodycomp` ← `classes`/`intake`/`feedback` ← `notifications`/`chat`/`profile`/`shell` ← **`wallet` و `shop` آخر از همه**. دلیلِ سنجه‌شده: سه جهشِ *زندهٔ* ممیزی دقیقاً در ماژولِ پول بود (`#27` مرزِ مبلغِ صفر، `#31` پیش‌فرضِ `bank_verified`، `#36` ‏`or`→`and`).

**وابستگیِ اجباری:** ‏`B2..Bn` فقط **پس از merge فازِ ۳** (که شکلِ قرارداد را عوض می‌کند: ۲۰۰→۴۲۲/۴۰۴ و پاکتِ خطا). ساختنِ کلاینتِ تازه روی قراردادِ در حالِ تغییر = دوبارکاری.

## یادداشتِ مهم دربارهٔ «چیزی پیدا نشد»

صفحه‌های خالیِ GitHub سه علتِ کاملاً متفاوت دارند و فقط یکی‌شان خبرِ خوب است:

| صفحه | علتِ سنجه‌شده | معنا |
|---|---|---|
| Secrets / Variables | واقعاً خالی‌اند (مالک نگاه کرد) | ✅ خبرِ خوب: مادهٔ حساسی هرگز در GitHub نبوده |
| Dependabot alerts | **غیرفعال** — پیامِ صریحِ API | ⚠️ «چیزی پیدا نشد» یعنی «نگاه نکرد» |
| Code scanning / CodeQL | هیچ workflow پیکربندی نشده | ⚠️ همین |
| Secret scanning | برای من `403` ⇒ قابلِ تعیین نیست | ❓ باید خودت نگاه کنی |

**و مهم‌تر از همه:** حتی اگر هر چهار اسکنر روشن باشند، هیچ‌کدام **یک** مورد از یافته‌های ممیزی را پیدا نمی‌کنند. اسکنرهای GitHub دنبالِ دو چیزند: CVEِ شناخته‌شده در وابستگی‌ها، و secretِ commit‌شده. ‏`F‑01` (اعتماد به XFF ⇒ ۳۰/۳۰ OTP پذیرفته، ۲۲۸٫۴ حدس در ثانیه)، `F‑02` (پیش‌فرضِ fail-open + echo شدنِ `dev_code`)، `F‑06` (`/api/v1/metrics` بدونِ احراز، ۳۴۶ خط و ۱۲ خانوادهٔ متریک)، `F‑08` و `F‑09` (مبلغ در `2^53+1`) نقصِ **طراحی، پیکربندی و مجوز**‌اند و در هیچ پایگاهِ CVE‌ای ثبت نشده‌اند. سنجهٔ مستقلِ من روی ۱۸ نسخهٔ نصب‌شدهٔ خودِ MP: ‏`pip-audit` ⇒ **«No known vulnerabilities found»** — یعنی وابستگی‌هایت امروز پاک‌اند؛ خطرِ واقعیِ تو آن پنج Critical است که هیچ اسکنری نمی‌بیندشان.

**یک تفکیکِ انتساب که باید ثبت بماند:** اسکنِ اولِ من ۶ CVE نشان داد (`mcp 1.29.0` ×۵ و `wcmatch 8.5.2` ×۱). این‌ها **ابزارِ خودِ ممیزی** بودند نه محصولِ تو — آزمونِ انتساب: هیچ‌کدام در `mp-app/backend/pyproject.toml` نیستند (۰ وقوع) و `Required-by` هر دو خالی است. هرگز این شش CVE را به MP نسبت نده.

## دستهٔ ۵ — هرگز نکن (با دلیلِ سنجه‌شده)

| ممنوع | دلیلِ سنجه‌شده |
|---|---|
| بازنویسی در Go / Elixir / Rust | همهٔ registryها **http=000** (`proxy.golang.org`, `hex.pm`, `repo.hex.pm`, `builds.hex.pm`, `crates.io`, `static.crates.io`) و هیچ toolchain نصب نیست ⇒ کیفیت «اعلام‌شده» می‌شود نه «سنجیده‌شده». و هیچ‌کدام پنج Critical را حل نمی‌کنند |
| دیتابیس/سرویسِ جدا به ازای هر دستهٔ داده | تراکنشِ `payments`↔`ledger_entries`↔`wallet_transactions`↔`orders` می‌شکند · FKها (`members.user_id`, `face_templates.member_id`) از بین می‌روند · `F‑04` امروز هم در ظرفیتِ ۶۰ و ۸۰ ورکر **۹۰ نمونه از ۱۴۵** را به سقف رساند |
| merge بر مبنای گزارشِ خودِ بیلدر | دو موردِ `PARTIAL` که «انجام شد» گزارش شدند |
| شروعِ `C2` پیش از بسته‌شدنِ فازِ ۱ | ‏`F‑01`/`F‑02` امروز قابلِ سوءاستفاده‌اند؛ مهاجرتِ DB هفته‌ها کارِ دیگر را فریز می‌کند |
| دادنِ اجازهٔ schema/migration به حلقهٔ بی‌ناظر پیش از نقطهٔ بررسیِ ۱ | تنها ترکیبِ واقعاً خطرناک: عاملِ بی‌ناظر + دسترسی به schema + امنیتِ نبسته |
| افزودنِ قابلیتِ تازه به کلاینتِ دارت | ۱۷٬۲۲۹ خطی که جایگزین می‌شود؛ هر قابلیتِ تازه = دوبارکاری |
| نگه‌داشتنِ هم‌زمانِ دو کارزارِ بزرگ (‏`C` و `B`) در یک هفته | هیچ‌کدام تمام نمی‌شود |

## دستهٔ ۶ — معیارِ «کلاسِ جهانی» و وضعیتِ امروزِ تو

| قلم | وضعیتِ سنجه‌شده |
|---|---|
| گیتِ عددی به ازای هر بستهٔ کاری | ✅ داری (ستونِ چهارمِ ۳۰ ردیفِ برنامه + الحاقیه) |
| اسکنرِ آسیب‌پذیریِ وابستگی (Dependabot) | ❌ **غیرفعال** — پیامِ خودِ API |
| اسکنِ کد (CodeQL) | ❌ هیچ workflow ندارد |
| پینِ وابستگی‌های بک‌اند | ❌ **۱۹ از ۱۹ بازه‌ای** (`>=`)، ۰ `==`، بدونِ lock/constraints؛ در برابرِ استودیو که `package-lock.json` دارد و دارت که `pubspec.lock` **ندارد** |
| پینِ ابزارِ امنیتی | ✅ ‏`gitleaks-fingerprints.yml` نسخهٔ **۸٫۳۰٫۱** را «verified» نصب می‌کند — تنها جایی که پروژه چیزی را پین کرده |
| امضا **و وارسیِ امضا در CI** | ✅ الگویش را داری (`apksigner verify --print-certs` با گواهیِ پین‌شده · `umask 077` · پاکسازی با `if: always()`) — با حذفِ کانالِ اندروید بی‌استفاده می‌شود؛ همان الگو را برای imageهای Docker و artifact وب نگه دار |
| پینِ toolchain | ❌ `channel: stable` بدونِ `flutter-version` در `apk.yml:29` و `web.yml:21` |
| SHA-pinning اقدام‌ها | ❌ **۰ از ۴۲** |
| build بازتولیدپذیر + SBOM + checksum | ❌ (برای imageها و artifact وب لازم است) |
| آزمونِ خودکارِ قرارداد روی ۱۶۳ عملیات | ⚠️ ابزارش هست (`probe_invalid_authed.py`) ولی هنوز آزمونِ CI نشده — همان `WP 3.5` |
| انتشارِ پله‌ای + گزارشِ خرابی | ❌ |

**هدفِ قابلِ سنجه:** پس از `D1` و `B`، تعدادِ زبان‌های محصول از ۴ (پایتون، TypeScript، دارت، Kotlin DSL) به **۲** می‌رسد، toolchainهای CI از **۶** (پایتون، نود، فلاتر، JDK از `jdk4py`، apktool از npm، داکر) به **۳**، workflowها از **۷** به **۵**، و سطحِ بی‌گیت از **۳** (دارت، Kotlin DSL، YAML) به **۰**.

## فهرستِ فشردهٔ زمانی

| بازه | کار |
|---|---|
| **همین امروز** | ۱٫۱ (پاک‌کردنِ secrets) · ۱٫۳ (جوابِ «زنده است یا نه») · paste کردنِ سه بندِ فوری برای بیلدر (‏`handoff/MP-BUILDER-RESPONSE-2026-11-21.md` §۴ + تفکیکِ `WP 4.6` + «A1.4 را در نقطهٔ بررسیِ ۱ بگیر») |
| **این هفته** | بسته‌شدنِ دو `PARTIAL` + `WP 3.1` + `WP 0.1`/`0.2` + فازِ ۱ ⟵ نقطهٔ بررسیِ ۱ ⟵ merge دستهٔ ۱ |
| **پس از آن** | ‏`D1` + `C0` + فازهای ۲–۴ + `C1` + `B0` ⟵ نقطهٔ بررسیِ ۲ ⟵ merge دستهٔ ۲ |
| **کارزارها** | `C2` → `C3` → `C4` (با تمرینِ بازیابی) · سپس `B1` → `B2..Bn` → پایانِ B |
---

## پیوستِ لینک‌ها — `2026-11-21T23:50Z`

**راهنمای صداقت:** گیت‌هاب به درخواستِ **بی‌هویت** برای همهٔ صفحه‌های `settings/*` کدِ `404` می‌دهد، پس `404`ِ من دلیلِ خرابیِ لینک نیست. ستونِ «سنجهٔ من» فقط آن‌هایی را `200` نشان می‌دهد که **بدونِ نشست** هم دیده می‌شوند؛ بقیه در مرورگرِ واردشدهٔ تو کار می‌کنند.

### الف) محافظتِ `main` — اقدامِ ۲، مهم‌ترینِ مانده

| لینک | سنجهٔ من |
|---|---|
| `https://github.com/yousefghorbanian98-create/MP/settings/branches` (branch protection کلاسیک) | `404` بی‌هویت ⇒ در مرورگرِ تو باز می‌شود |
| `https://github.com/yousefghorbanian98-create/MP/settings/rules` (Rulesets — مسیرِ جدیدتر و پیشنهادی) | `404` بی‌هویت |
| `https://github.com/yousefghorbanian98-create/MP/rules` (**صفحهٔ وارسی**: پس از ذخیره اینجا فهرست می‌شود) | ✅ `200` |

تنظیماتِ لازم در فرم: الگو `main` · «Require a pull request before merging» **اختیاری** (اگر بزنی، بیلدر دیگر نمی‌تواند مستقیم به `main` push کند که خوب است، ولی خودت هم باید از PR بروی) · «Require status checks to pass before merging» **الزامی** · «Require branches to be up to date before merging» **الزامی** · «Do not allow force pushes» **الزامی** (سیاستِ ما هم force-push را ممنوع کرده).

**هشت check با نامِ دقیق** (از jobهای اجرای `44961471336` استخراج شد؛ همین‌ها را در کادرِ جست‌وجو تایپ کن):

1. `backend`
2. `live-contract`
3. `secret-scan`
4. `studio`
5. `client-flutter`
6. `e2e-api`
7. `Documentation links and handoff`
8. `Client — pinned SDK · format gate · Android debug compile`

### ب) امنیت و Dependabot

| لینک | سنجهٔ من |
|---|---|
| `https://github.com/yousefghorbanian98-create/MP/security` (هابِ امنیت — از اینجا به همهٔ بخش‌ها می‌روی) | ✅ `200` |
| `https://github.com/yousefghorbanian98-create/MP/security/dependabot` (شمارِ هشدارها — همان عددی که از تو خواستم) | `404` بی‌هویت |
| `https://github.com/yousefghorbanian98-create/MP/security/secrets` (secret scanning) | `404` بی‌هویت |
| `https://github.com/yousefghorbanian98-create/MP/security/code-scanning` (CodeQL — انتظار دارم «پیکربندی نشده» ببینی) | `404` بی‌هویت |
| `https://github.com/yousefghorbanian98-create/MP/security/policy` | ✅ `200` |
| ~~`https://github.com/yousefghorbanian98-create/MP/settings/security`~~ | **این را استفاده نکن** — مالک گزارش کرد که حتی واردشده هم `404` داد؛ برای مخزنِ publicِ حسابِ شخصی، این کنترل‌ها زیرِ تبِ **Security** هستند نه Settings |

### ج) PR و CI

| لینک | سنجهٔ من |
|---|---|
| `https://github.com/yousefghorbanian98-create/MP/pull/23` (دکمهٔ **Reopen** برای نقطهٔ بررسیِ ۱؛ `merged=false` پس بازگشایی ممکن است) | ✅ `200` |
| `https://github.com/yousefghorbanian98-create/MP/actions` | ✅ `200` |
| `https://github.com/yousefghorbanian98-create/MP/actions/runs/44961471336` (اجرای قرمزِ چهارگانه روی tip بیلدر) | ✅ `200` |
| `https://github.com/yousefghorbanian98-create/MP/actions/runs/44962138925` (**«Graph Update: pip in /mp-app/backend»** — سندِ زندهٔ روشن‌شدنِ Dependabot) | ✅ `200` |
| `https://github.com/yousefghorbanian98-create/MP/settings/actions` (مجوزهای workflow) | `404` بی‌هویت |

### د) شاخهٔ بیلدر و فایل‌هایی که در `AD‑22`/`AD‑23` به آن‌ها ارجاع دادم

| لینک | سنجهٔ من |
|---|---|
| `https://github.com/yousefghorbanian98-create/MP/tree/arena/da474b65-mp` | ✅ `200` |
| `https://github.com/yousefghorbanian98-create/MP/commits/arena/da474b65-mp` | `429` (rate-limitِ موقتِ من) — در مرورگر کار می‌کند |
| `https://github.com/yousefghorbanian98-create/MP/blob/arena/da474b65-mp/.gitleaksignore` (سیاستِ انگشت‌نگاری، ۲۰ خط) | ✅ `200` |
| `https://github.com/yousefghorbanian98-create/MP/blob/arena/da474b65-mp/scripts/test_retired_signing_scan.py` (تستِ سلامتِ گیت) | ✅ `200` |
| `https://github.com/yousefghorbanian98-create/MP/blob/arena/da474b65-mp/docs/MuscleParadise/audit/evidence/before/detect-secrets.json` (منبعِ مثبتِ کاذب) | در مرورگر |
| `https://github.com/yousefghorbanian98-create/MP/blob/arena/da474b65-mp/mp-app/backend/pyproject.toml` (۱۹ وابستگیِ بازه‌ای) | ✅ `200` |

### ه) اسنادِ ممیزی (مخزنِ Chat2DB، شاخهٔ `arena/2cde32d6-chat2db`)

| لینک | محتوا |
|---|---|
| `https://github.com/yousefghorbanian98-create/Chat2DB/tree/arena/2cde32d6-chat2db/handoff` | فهرستِ همهٔ ۸ سند |
| `https://github.com/yousefghorbanian98-create/Chat2DB/blob/arena/2cde32d6-chat2db/handoff/MP-OWNER-CHECKLIST-2026-11-21.md` | **همین سند** — شش دستهٔ کاری + دروازهٔ اولین عضو + پیوستِ لینک‌ها |
| `https://github.com/yousefghorbanian98-create/Chat2DB/blob/arena/2cde32d6-chat2db/handoff/MP-SCENARIO-A1.4-2026-11-21.md` | سناریوی کامل؛ ‏§B‑۴٫۵ اصلاحات و §B‑۴٫۶ متنِ `AD‑21`/`AD‑22`/`AD‑23` |
| `https://github.com/yousefghorbanian98-create/Chat2DB/blob/arena/2cde32d6-chat2db/handoff/MP-BUILDER-RESPONSE-2026-11-21.md` | داوریِ دو commit و فهرستِ PARTIALها در §۴ |
| `https://github.com/yousefghorbanian98-create/Chat2DB/blob/arena/2cde32d6-chat2db/handoff/MP-BUILDER-KIT-2026-11-21.zip` | کیتِ منجمدِ بیلدر (`486,358` بایت / `9a192500…`) |

**بازیابیِ بدونِ توکنِ هر سند** (برای بیلدر یا هر محیطِ دیگری):
`curl -fsS -H "Accept: application/vnd.github.raw" "https://api.github.com/repos/yousefghorbanian98-create/Chat2DB/contents/handoff/<نامِ فایل>?ref=arena/2cde32d6-chat2db"`

### یک نکتهٔ مجوز که باید بدانی

توکنِ ممیزیِ من روی مخزنِ MP ‏`permissions.admin = true` گزارش می‌شود، ولی `branches/main/protection` را با `403 Resource not accessible by integration` رد می‌کند ⇒ آن installation مجوزِ ریزدانهٔ «Administration» را ندارد. پس **من نمی‌توانم** branch protection یا ruleset بسازم؛ این کار فقط با نشستِ مرورگریِ تو انجام می‌شود. اگر خواستی، می‌توانم یک‌بار `POST /repos/.../rulesets` را **با اجازهٔ صریحِ تو** امتحان کنم و نتیجه را دقیق گزارش دهم — ولی بدونِ اجازه دست نمی‌زنم، چون یک rulesetِ بدپیکربندی می‌تواند بیلدر را از push کردن قفل کند.
---

## وارسیِ `2026-11-22T08:5xZ` — ruleset ساخته شد ولی **کار نمی‌کند**، و دسته‌بندیِ کاملِ ۱۳ هشدار

### الف) ruleset «Main» (id ‏`27826883`): نیمه‌درست — دو تنظیم، آن را بی‌اثر گذاشته

| قلم | وضعیتِ سنجه‌شده |
|---|---|
| چهار نوعِ قاعده | ✅ `deletion` · `non_fast_forward` · `pull_request` · `required_status_checks` |
| هشت checkِ اجباری | ✅ **هر هشت** دقیقاً فهرست شده‌اند، با `strict_required_status_checks_policy: true` (یعنی «up to date» هم روشن است) |
| **`enforcement`** | ❌ **`disabled`** ⇒ هیچ‌چیز اعمال نمی‌شود |
| **`conditions.ref_name.include`** | ❌ **`[]`** خالی ⇒ ruleset به **هیچ شاخه‌ای** هدف نگرفته؛ حتی با enforcement فعال هم بی‌اثر است |
| آزمونِ عملی | PR #23 بازگشایی شد و `mergeable_state = unstable` ماند، نه `blocked` ⇒ تأییدِ مستقلِ بی‌اثر بودن |

**دو کلیکِ باقی‌مانده:** در صفحهٔ ruleset ← (۱) **Target branches** ← Include ← `refs/heads/main` (یا `~DEFAULT_BRANCH`) ← Add ← (۲) بالای صفحه **Enforcement status** را از `Disabled` به **`Active`** ← Save. بعد به من بگو تا دوباره بخوانم: باید `enforcement=active` و include غیرخالی و PR #23 ‏`blocked` شود.

`required_approving_review_count: 0` برای مالکِ تنها قابلِ قبول است؛ اگر روزی همکاری اضافه شد، ۱ بگذار.

### ب) ۱۳ هشدارِ Dependabot — دسته‌بندیِ کامل از روی اسکرین‌شاتِ مالک + یک سنجهٔ قطعی‌کننده

| قلم | عدد |
|---|---|
| کل | **۱۳** · `#1`…`#13` |
| شدت | **۱ High** (`#8` ‏launch-editor `fs.existsSync()` روی Windows) · ۱۰ Moderate · ۲ Low (`#11` vite cross-origin، `#13` katex) |
| Manifest | **۱۲** در `mp-app/studio/package-lock.json` · **۱** در `tools/mermaid-check/package-lock.json` (`#13` katex) |
| Direct / Transitive | ۹ Direct · ۴ Transitive (`#1` esbuild، `#5` و `#12` ‏`@vitest/mocker`، `#13` katex) |
| Development / Runtime | **۱۳ Development · ۰ Runtime** |
| بسته‌های درگیر | `vite` (۷) · `launch-editor` (۴) · `vitest`/`@vitest/mocker` (۳… با #6,#5,#12) · `esbuild` (۱) · `katex` (۱) |

**سنجهٔ قطعی‌کننده (چرا همه‌شان امروز صفر تعرض دارند):** ‏`mp-app/studio/Dockerfile` دو مرحله‌ای است — مرحلهٔ build ‏`npm ci && npm run build` (یعنی `tsc -b && vite build`؛ vite فقط **ابزارِ build** است) و مرحلهٔ runtime ‏**`nginx:1.27-alpine`** که `dist/` را serve می‌کند و `EXPOSE 80`. و compose (`mp-app/deploy/docker-compose.yml:44-51`) همان Dockerfile را build می‌کند و پورت را به **`127.0.0.1:${STUDIO_PORT:-8080}:80`** می‌بندد ⇒ **loopback-only**. پس در production **هیچ vite dev server‌ای اجرا نمی‌شود**؛ مسیرهای آسیب‌پذیر (`server.fs.allow/deny`، optimizer `.map`، mocker redirect، launch-editor، پراکسیِ dev serverِ esbuild) در artifactِ سروشده **وجود ندارند**.

**پیامدها:**
- هیچ‌کدام از ۱۳ به **دروازهٔ اولین عضو** تعلق ندارند. اولویتشان **پایین** است.
- تنها تعرضِ واقعی: **ماشینِ توسعه‌دهنده‌ای که روی Windows ‏`npm run dev` می‌زند** — مخصوصاً `#8` (High) و چهار موردِ Windows-محورِ دیگر (`#3`,`#4`,`#7`,`#9`). یعنی یک خطرِ *محیطِ توسعه* است، نه *محصول*.
- `#13` (katex) فقط در ابزارِ CI رسمِ دیاگرام است ⇒ کم‌اولویت‌ترین.
- بنابراین `AD‑24` (کارزارِ npm-تنها) **فوری نیست**؛ ولی وقتی انجام شد، `#8` باید اولین bump باشد چون تنها High است.
- یک هشدارِ صادقانه: `npm ci` در مرحلهٔ build همان lock را resolve می‌کند، پس بسته‌های آسیب‌پذیر در **imageِ build** نصب می‌شوند (هرچند به imageٔ runtime نمی‌رسند). این یک نکتهٔ زنجیرهٔ تأمینِ مرحلهٔ build است، نه یک آسیب‌پذیریِ runtime.

### ج) compose جابه‌جا شده بود — تصحیحِ ارجاعِ خودم

مسیرِ درستِ compose روی `main` ‏**`mp-app/deploy/docker-compose.yml`** است (نه `infra/docker-compose.yml` که در سنجه‌های قدیمی‌ترم به آن ارجاع دادم؛ آن مسیر اکنون `404` است). `mp-app/infra/Caddyfile` هم موجود است. همهٔ ارجاع‌های آینده باید از مسیرِ تازه باشند.
---

## وارسیِ `2026-11-22` پس از «ست شد» — ruleset **فعال و درست** است، ولی PR #23 به شاخهٔ کهنه وصل است

### الف) ruleset ‏`27826883` — تأیید شد ✅

| قلم | مقدارِ سنجه‌شده |
|---|---|
| `enforcement` | ✅ **`active`** (قبلاً `disabled`) |
| `conditions.ref_name.include` | ✅ **`["~DEFAULT_BRANCH"]`** (قبلاً `[]`) |
| انواعِ قاعده | ✅ `deletion` · `non_fast_forward` · `pull_request` · `required_status_checks` |
| تعدادِ check | ✅ **۸ از ۸**، verbatim |
| `strict_required_status_checks_policy` | ✅ `true` |
| آزمونِ عملی | ✅ PR #23 از `unstable` به **`mergeable_state = blocked`** پرید |
| ruleset‌های مخزن | فقط همین یکی (پس تعارض یا تکراری در کار نیست) |

**یک خبرِ خوبِ سنجه‌شده:** ‏`review_decision = null` روی PR #23 ⇒ قاعدهٔ `pull_request` با `required_approving_review_count: 0` از تو مرور نمی‌خواهد، و `require_extra_approval_for_unattributed_changes: true` هم مانعی برای مالکِ تنها نساخته. یعنی **blocked بودن فقط به خاطرِ check‌های قرمز است** — نه یک بن‌بستِ مروری. وقتی هر هشت سبز شوند، خودت می‌توانی merge کنی.

**هزینهٔ `strict: true` را بدان:** چون «up to date with main» روشن است، هر بار که `main` جلو برود، PR باید از `main` به‌روزرسانی شود و **هر هشت job ‏دوباره اجرا می‌شوند** (backend ‏تنهایی ~۴۶۰ ثانیه). پس بهتر است merge ‏وقتی انجام شود که `main` تکان نخورده باشد.

### ب) چرا هنوز `blocked` است — چهار job قرمز روی tipِ PR

روی head ‏PR #23 یعنی `9bfc99d6f` ‏(۲۴ check-run): قرمز = `backend` · `live-contract` · `secret-scan` · `Documentation links and handoff` · سبز = `studio` · `client-flutter` · `Client — pinned SDK…` · `e2e-api` ‏skipped (چون `needs: [backend]` و backend قرمز بود).

### ج) ⚠ یافتهٔ مهم: PR #23 پنج commit عقب‌تر از کارِ بیلدر است

| قلم | مقدار |
|---|---|
| head ‏PR #23 | شاخهٔ `arena/da474b65-mp` @ `9bfc99d6f` |
| شاخهٔ کاریِ بیلدر | `arena/5a1e37b3-mp` @ `db37b1bc0` |
| `compare` | `status=ahead · ahead_by=5 · behind_by=0` ⇒ **fast-forward خالص** |
| پنج commitِ جا مانده | `1ec787180` · `b9a65050c` · `3251145e4` · `3eaed4231` · `db37b1bc0` |
| عواقب | روی `9bfc99d6f` ‏`backend` و `live-contract` **قرمز**اند؛ روی `db37b1bc0` **سبز** ⇒ merge کردنِ PR #23 به وضعیتِ امروز یعنی merge کردنِ کدِ با backendِ قرمز |

**درمان (یک فرمان، در دستورِ کارِ بیلدر گذاشته شد):** ‏`git push origin arena/5a1e37b3-mp:arena/da474b65-mp` ⇒ PR #23 خودبه‌خود جلو می‌آید، شماره و تاریخچه‌اش حفظ می‌شود، PR تازه لازم نیست. ruleset ‏هم جلوی این push را نمی‌گیرد چون `deletion` و `non_fast_forward` فقط به `~DEFAULT_BRANCH` می‌خورند.

### د) وضعیتِ CI روی `db37b1bc0` ‏در لحظهٔ وارسی

سبز (۵): `backend` · `live-contract` · `studio` · `client-flutter` · `Client — pinned SDK · format gate · Android debug compile`
در حالِ اجرا (۱): `e2e-api` · قرمز (۲): `secret-scan` · `Documentation links and handoff`
هر دو قرمز در الحاقیه پاسخ گرفته‌اند ⇒ **هیچ‌کدام نیاز به تصمیمِ تو ندارند.**

### هـ) شرطِ توقفِ من فعال شد — و یک اشتباهِ خودم اصلاح شد

`secret-scan` بعد از دورِ اول، ده finding ‏در **مسیرِ دوم** نشان داد: ‏`docs/MuscleParadise/audit/evidence/**after**/detect-secrets.json` (من در `AD‑23` نوشته بودم «یک مسیر»). آن جمله از دادهٔ ناقص نوشته شده بود: سقفِ annotation ‏ده‌تا را نشان می‌داد. سنجهٔ ماهیت: هر دو baseline **فقط hash** دارند (`171/171` و `169/169` ‏`hashed_secret`، همه sha1ِ ۴۰-هگز، صفر plaintext) ⇒ یک کلاس‌اند. `AD‑23` به **دو مسیر** اصلاح شد و مرزِ سخت سرِ جای خودش ماند.

**کاری از تو نمی‌خواهد:** فرمولِ fingerprint ‏داده شده و بیلدر ده موردِ دورِ دوم را خودش می‌سازد؛ dispatch تازه لازم نیست (workflow ‏`423857407` یک بار اجرا شد: `2026-11-22T05:37:02Z`، `workflow_dispatch`، `success`).

### و) علتِ دقیقِ قرمزیِ `Documentation links and handoff` — هر چهار دروازه locally زده شد

| دروازه | نتیجه |
|---|---|
| `scripts/docs_gate.py` | ✅ PASS — «18 Markdown files, 276 local links, 15 Mermaid diagram block(s), handoff headings, README entrypoints, SVG XML» |
| `scripts/interaction_map.py --check` | ❌ FAIL — «نقشهٔ سطح تعامل کهنه است» |
| `tools/mermaid-check` | ⚠ **هرگز اجرا نشده** — job در گامِ قبل متوقف می‌شود |
| `scripts/repo_hygiene_gate.py` | ✅ PASS |

یعنی تنها علتِ قرمزی، کهنه بودنِ نقشه است — همان چیزی که پاسخِ من دستورِ بازتولیدش را داد. و یک هشدارِ صادقانه: دروازهٔ mermaid **تا امروز یک بار هم اجرا نشده**، پس بعد از بازتولیدِ نقشه برای اولین بار اجرا می‌شود و ممکن است قرمزیِ تازه‌ای بدهد.

### ز) بازتولیدِ نقشه را خودم از قبل انجام دادم — داوریِ عددیِ پیش‌دستانه

در cloneِ موقت، بدون commit: ‏`31 سطح · رانش قرارداد 0 · بی‌تست 6` (از ۷). تغییر: ‏`interaction-map-2026-11-19.md` ‏(+۲۱/−۲۱) و `interaction-map.json` ‏(−۱۲/+۴۹)؛ در json هیچ کلیدی اضافه/حذف نشده، فقط `roles` و `tests`.

**حسابِ شش نقش که بدون باقی‌مانده بسته می‌شود** (آزمونِ اصلیِ «بازتولید چیزی را پنهان نکرده»):

| نقش | قدیم | تازه | تفاوت | تجزیه |
|---|---|---|---|---|
| `admin` | 102 | 103 | **+1** | −۳ تنگ‌شدن +۴ عمومی |
| `manager` | 102 | 103 | **+1** | −۳ +۴ |
| `super_admin` | 106 | 110 | **+4** | −۰ +۴ |
| `coach` | 65 | 73 | **+8** | +۴ عمومی +۱ `sessions` +۳ `phone-change` |
| `reception` | 42 | 50 | **+8** | +۴ +۱ +۳ |
| `member` | 69 | 76 | **+7** | +۴ +۳ (`sessions` را داشت) |

دسته‌بندی: **۳ تنگ‌شدن** (`admin/users*` به فقط `super_admin`) · **۴ اصلاحِ نمایش** (`otp/request`, `otp/verify`, `refresh`, `logout` که واقعاً عمومی‌اند — هیچ‌کدام `AuthenticatedUser` ندارند) · **۴ گشادشدنِ واقعی** (`sessions` و سه `phone-change`) · **صفر swap**.

**گشادشدن‌ها IDOR نیستند — خواندم:** ‏`router.py:142` ⇒ `list_sessions(db, user_id=user.id, …)` · `service.py:174` ⇒ `row.user_id != user_id` · هر سه `phone-change` ‏(`router.py:88/101/114`) هیچ پارامترِ id از درخواست نمی‌خوانند و مالکیتِ `challenge_id` در `service.py:220-232` **در خودِ query** ‏(`AND user_id == user.id`) با ۴۰۴ سنجیده می‌شود. `service.py:414` هم که `db.get` بدون فیلتر به نظر می‌رسد، داخلِ هندلرِ `IntegrityError` و **بعد از** همان واکشیِ مالکیت‌سنجیده است. ⇒ محدود بودنِ `phone-change` به سه نقشِ مدیریتی یک **باگِ کارکردی** بود (عضو نمی‌توانست شمارهٔ خودش را عوض کند)، نه یک کنترلِ امنیتی.

**یک پرچمِ اشتباهِ خودم را پس می‌گیرم:** ‏regex ‏من «هیچ بررسیِ مالکیتی در `verify_old_phone_change_otp`» چاپ کرد؛ بررسی در helper ‏است نه inline. آن خروجیِ ابزار بود، نه یافته.
---

## وارسیِ `2026-11-22` دورِ سوم — سؤالِ توقفِ بیلدر، و اصلاحِ دومِ `AD‑23` (سه مسیر)

**سؤالِ بیلدر چه بود:** «کدام فایل‌ها مجازند fingerprint بگیرند؟» با سه گزینه. **پاسخِ من به تو: گزینهٔ سوم** (`before/` + بالاسری + `after/`)، و الحاقیهٔ ۲ همین را به بیلدر می‌دهد.

**چرا سوم — سنجه‌های من روی `ea1efe524`:**

| فایل | بایت | finding | `hashed_secret` | `is_verified:true` |
|---|---|---|---|---|
| `evidence/detect-secrets.json` (بالاسری) | 53,680 | 173 | 173/173 | **0** |
| `evidence/before/detect-secrets.json` | 52,573 | 169 | 169/169 | **0** |
| `evidence/after/detect-secrets.json` | 53,157 | 171 | 171/171 | **0** |

هر سه فقط hash‌اند (sha1ِ ۴۰-هگز)، صفر plaintext، و خودِ detect-secrets هیچ‌کدام را secretِ زنده تأیید نکرده. ترکیبِ rule‌ها هم یکسان است (Hex High Entropy ۱۷ + Secret Keyword ۷ تا ۱۱ + Basic Auth ۲ + Base64 ۲ + JWT ۱). گزینهٔ اول حلقه را هرگز همگرا نمی‌کرد؛ گزینهٔ دوم خودتضاد بود (after/ را با سنجهٔ یکسان stop نگه می‌داشت).

**اعترافِ دومِ من:** «یک مسیر» غلط بود، «دو مسیر» هم ناقص بود. واقعیت **سه** baseline است. `AD‑23` نسخهٔ ۳ = همین سه مسیر، و مرزِ سخت سرِ جای خودش: findingِ بیرونِ این سه ⇒ بایست و گزارش بده. و استثنا سطحِ fingerprint می‌ماند، نه path allowlist در `.gitleaks.toml`، تا secretِ واقعیِ آینده در همین فایل‌ها هنوز گیر بیفتد.

**همگراییِ یک‌ضربه‌ای به‌جای ده‌ها dispatch:** سقفِ annotation ‏ده‌تاست، پس حلقهٔ batch‌ی به ~۵۰ دور نیاز داشت. الحاقیهٔ ۲ به بیلدر یک اسکریپتِ commit‌شده می‌دهد (`scripts/gen_evidence_fingerprints.py`) که مجموعهٔ کاملِ ~۵۱۳ fingerprint را از خودِ سه فایل deterministic می‌سازد (خطِ هر `hashed_secret` با جست‌وجوی رشته، نه حدس) ⇒ حلقه در **یک push** بسته می‌شود. entry‌های اضافه بی‌اثرند ولی هیچ سطرِ flag‌شده‌ای جا نمی‌ماند.

**تأییدِ انضباطِ بیلدر:** ‏`.gitleaksignore` بین `db37b1bc0` و `ea1efe524` بایت‌به‌بایت یکسان است ⇒ در دورهای ۲ و ۳ هیچ fingerprint بیرون از `before/` اضافه نشده. commit ‏`37a829db5` فقط `EXECUTION-LOG.md` ‏+۱۱ خط است و شماره‌های run ‏اش (`44990174499`، `44990769317`، `44990830149`) با سنجه‌های من هم‌خوان است. یک تصحیحِ کوچک بر سندِ او هم در الحاقیهٔ ۲ آمده (annotation‌ها مسیر/خط **می‌دهند**؛ آنچه پنهان می‌ماند مقدار است).

**CI روی `ea1efe524` = هفت سبز، یک قرمز:** ‏`backend` · `live-contract` · `studio` · `client-flutter` · `Client — pinned SDK…` · `e2e-api` · و **`Documentation links and handoff`** سبز شدند. با سبز شدنِ job ‏docs، دروازهٔ mermaid **برای اولین بار در تاریخِ مخزن** اجرا شد و pass شد. تنها قرمز: `secret-scan`.

**بازتولیدِ نقشهٔ بیلدر با سنجهٔ مستقلِ من تطبیق دارد:** او +۲۱/−۲۲ و +۴۹/−۲؛ من در scratch ‏+۲۱/−۲۱ و +۴۹/−۱۲. تفاوتِ یک خط ناچیز است و چون دروازه سبز است و حسابِ شش نقش بسته می‌ماند پذیرفته شد. `D-9` و `D-10` در `DECISIONS.md` ثبت شده‌اند ⇒ شرطِ انتساب اجرا شده.

**یادداشتِ جانبی بدونِ اقدام:** دو entry ‏برای `mp-app/client/android/keystore/keystore.properties` از پیش روی `main` بوده‌اند ولی خودِ فایل روی شاخهٔ بیلدر `404` است ⇒ بی‌اثرند. دست‌نخورده می‌مانند؛ فقط یک خطِ ثبتِ stale در `EXECUTION-LOG` خواسته شده.

**کاری که از تو می‌خواهم:** در کارتِ سؤالِ بیلدر **گزینهٔ سوم** را Submit کن، بعد الحاقیهٔ ۲ را paste کن:
`handoff/MP-BUILDER-ADDENDUM2-2026-11-22.txt`
---

## داوریِ دو commit ‏«guard» (سؤالِ دومِ بیلدر) — پاسخ: **نگه‌دار** (گزینهٔ اول)

بیلدر پرسید آیا `b9e88e5` و `fae50c5` عمدی‌اند. هر دو diff را خط‌به‌خط خواندم؛ نه از روی پیامِ commit.

### `b9e88e5` — حذفِ گاردِ **تکراری**، نه حذفِ گارد

| سنجه | مقدار |
|---|---|
| گاردِ سطحِ روتر | `APIRouter(dependencies=[Depends(require_permission())])` در `modules/axis_assessment/router.py:14` — روی **همهٔ** مسیرهای ماژول، از جمله `review` |
| گاردِ حذف‌شده | پارامترِ `user: Annotated[User, Depends(require_permission())]` روی `review_assessment` — **همان** گارد، همان آرگومان |
| آرگومان‌پذیری | `def require_permission():` در `app/deps.py:129` **هیچ آرگومانی نمی‌گیرد**؛ casbin را با `(نقش، مسیر، متد)` اجرا می‌کند ⇒ خطرِ «دو گارد با مجوزِ متفاوت» وجود ندارد |
| `routes.json` | `"guards": ["permission","permission"]` ⇒ `["permission"]` — تصحیحِ داده، نه تغییرِ مجوز |
| تست | دو تستِ تازه: `test_wp03_axis_single_guard.py` ‏(+۵۸) و `test_no_duplicate_guard.py` ‏(+۵۰) که تکرارِ هم‌نوع را برای همیشه ممنوع می‌کند |

⇒ مجوزِ مؤثر **عوض نشده**؛ فقط یک `enforce` اضافهٔ پرهزینه حذف شده. جهت: خنثی.

### `fae50c5` — بستنِ یک مسیرِ **عمومی**، با سه لایه

| سنجه | مقدار |
|---|---|
| قبل | `/api/v1/metrics` با `"guards": []` و `"roles": []` ⇒ **عمومی** |
| لایهٔ اپ | `require_metrics_token`: توکن تنظیم‌نشده ⇒ **۴۰۳** (fail-closed) · هدر/توکن غلط ⇒ ۴۰۱ · مقایسه با `hmac.compare_digest` (ثابت‌زمان) |
| لایهٔ لبه | `Caddyfile`: ‏`handle /api/v1/metrics { respond 404 }` ⇒ حتی با توکنِ لو رفته هم از اینترنت در دسترس نیست؛ Prometheus مستقیم به `backend:8000` می‌زند |
| لایهٔ استقرار | `docker-compose.yml`: ‏`MP_METRICS_TOKEN: ${MP_METRICS_TOKEN:?…}` روی **هم** backend **هم** prometheus ⇒ بدون توکن، Compose بالا نمی‌آید |
| راز در مخزن؟ | **نه.** grep سراسری: مقدار فقط از محیط می‌آید؛ `prometheus.yml` هم `credentials: ${MP_METRICS_TOKEN}` (expand-env). تنها رشتهٔ سخت‌کدشده، توکنِ مصنوعیِ تست است (`test-metrics-token-0123456789abcdef`) که با fixture ‏autouse ‏monkeypatch می‌شود |
| تست‌ها | `test_wp13_metrics_auth.py` ‏(+۷۵) + به‌روزرسانیِ چهار تستِ موجود به هدرِ `METRICS_AUTH` |

⇒ جهت: **تنگ‌شدنِ محض**. برگرداندنش یعنی باز کردنِ دوبارهٔ `/metrics` به اینترنت.

### نتیجه و یک نکتهٔ مدل‌سازی

هر دو عمدی‌اند، هر دو تست دارند، و هر دو در `DECISIONS.md` راهنمای برگرداندن هم دارند (خطِ ۱۱). **صفر گشادشدن.** پاسخ به بیلدر: گزینهٔ اول («Yes, keep them»).

نکتهٔ صادقانه برای ثبت در D‑10: ‏`routes.json` برای `/metrics` ‏نقش‌های `manager, admin, super_admin` مدل کرده، در حالی که اجرای واقعی **توکن‌محور** است نه نقش‌محور. این یک انتخابِ مدل‌سازی برای نقشه است نه حفرهٔ امنیتی — توکن از نقش مشتق نمی‌شود. وقتی نقشه را داوریِ عددی می‌کنم (نقطهٔ بررسیِ ۱) همین را هم می‌سنجم.
---

## وارسیِ همگراییِ `AD‑23` — تأییدِ کامل، و **یک کارِ دو-ضربه‌ای که فقط تو می‌توانی**

### الف) حلقهٔ همگرایی — با سنجهٔ من تأیید شد ✅

| قلم | مقدارِ سنجه‌شده |
|---|---|
| commit‌های حلقه پس از `ea1efe524` | **۴۹** = ۴۸ دورِ fingerprint + ۱ commit سند (`6c204ec`) |
| فایل‌های عوض‌شده در کلِ حلقه | فقط `.gitleaksignore` ‏(+۷۲/−) + `DECISIONS.md` ‏(+۹) + `EXECUTION-LOG.md` ‏(+۱۲) |
| `.gitleaksignore` روی tip | ۵۰ خط · **۴۰ fingerprint** · **صفر تکراری** · صفر خطِ نامعتبر |
| سه مسیرِ مجاز | ۱۶۲ بالاسری + ۱۵ `before/` + ۶۱ `after/` = **۴۸۲** · همه با commit ‏`839500de…` و rule ‏`generic-api-key` |
| حسابِ بسته | ۴۸۲ − ۱۰ (دورِ اول که از قبل بود) = **۴۷۲** = دقیقاً آنچه compare نشان می‌دهد |
| entry‌های بیرونِ سه مسیر | فقط ۸ موردِ از پیش موجود (fixture‌های تست + REPORT) ⇒ مرزِ سخت شکسته نشد |

### ب) CI — هر هشت check، روی **هر دو** tip، سبز ✅

روی `4272eae` ‏(نوکِ حلقه) و روی `6c204ec` ‏(commit سند): `backend` · `live-contract` · `secret-scan` · `studio` · `client-flutter` · `e2e-api` · `Documentation links and handoff` · `Client — pinned SDK · format gate · Android debug compile` — همه `completed/success`. (`gitleaks-fingerprints` هم success.)
این **اولین باری** است که هر هشت با هم سبزند. دروازهٔ ruleset حالا معنای کاملش را دارد.

### ج) ⚠ تنها گرهٔ باقی‌مانده: head ‏PR #23 — و فقط تو می‌توانی بازیش کنی

| سنجه | مقدار |
|---|---|
| PR #23 | `head = arena/da474b65-mp @ 9bfc99d6f` · `state = open` · `mergeable_state = blocked` |
| فاصله تا tip سبز | `ahead_by = 56 · behind_by = 0` ⇒ fast-forward خالص |
| بیلدر | push به `arena/da474b65-mp` را **نپذیرفت** (سیاستِ شاخهٔ کاریِ خودش) — درست هم می‌گفت |
| من | `git push --dry-run` با توکنِ خودم ⇒ **403 Permission denied** ⇒ من هم نمی‌توانم |

**پس راهِ UI است، دو ضربه:**
1. در صفحهٔ مخزنِ MP، شاخه را به `arena/5a1e37b3-mp` ببر و دکمهٔ **«Create PR»** (همان که در اسکرین‌شاتِ خودت کنارِ `+103373 −700` بود) را بزن؛ base = `main`. عنوان پیشنهادی: «ممیزی A1.4 + AD-23: هر هشت گیت سبز». PR تازه **همان لحظه هر هشت check سبز** را نشان می‌دهد چون check-run‌ها روی `6c204ec` از قبل موجودند.
2. بعد PR #23 را **Close** کن. محتوایش زیرمجموعهٔ کاملِ PR تازه است (fast-forward) و گفتگوهایش روی PR بسته هم خواندنی می‌مانند.

چرا نه force و نه دست‌کاریِ دیگر: قواعدِ `deletion` و `non_fast_forward` روی `main` فعال‌اند و هیچ‌کس نباید تاریخچه را بازنویسی کند؛ ساختنِ PR تازه هیچ قانونی را نمی‌شکند.

### د) آنچه بیلدر بعد از این انجام می‌دهد (خودش فهرست کرده)

بخش‌های ۲ تا ۶ دستور: بستنِ `WP 2.5`/`WP 3.2` · `AD‑12` (پین‌های freeze — با نامِ درستش `requirements.txt`، نه `constraints.txt`) · `AD‑11` (حذفِ `apk.yml` و آن یک تستِ گارد) · `B‑4.5`/`B‑4.6` در Chat2DB.
تا آن کارها تمام نشده، **merge نمی‌کنیم**: اول داوریِ عددیِ من (نقطهٔ بررسیِ ۱)، بعد merge با تو.

یک یادداشتِ ثبتی: بیلدر نوشته `share/MP-BUILDER-HANDOFF-A1.3.md` در sandbox‌اش untracked بوده و با reset محیط از بین رفته. در مخزنِ **من** آن فایل commit شده و سالم است (`handoff/MP-BUILDER-HANDOFF-A1.3.md`، ۲۷٬۹۰۸ بایت) ⇒ هیچ چیزِ تحویلی گم نشده؛ فقط کپیِ محلیِ او رفت.
---

## وارسیِ دو ضربهٔ تو ✅ و یک قفلِ پنهان در ruleset که فقط تو می‌توانی بازیش کنی

### الف) هر دو ضربه درست انجام شد

| قلم | سنجه |
|---|---|
| PR تازه | **#24** · `state=open` · `head=arena/5a1e37b3-mp @ 6c204ec` · `base=main` · عنوان دقیقاً «ممیزی A1.4 + AD-23: هر هشت گیت سبز» · ۱۰۲ commit · ۲۸۹ فایل · +۱۰۳٬۸۶۶/−۷۰۰ |
| PR #23 | `state=closed` · `closed_at=2026-11-22T08:55:07Z` · **`merged=false`** ⇒ درست بسته شد، نه merge |
| هشت check روی head ‏#24 | همه `success` |

### ب) ولی `mergeable_state = blocked` با وجودِ هشت check سبز — علت را سنجه‌ام

GraphQL: ‏`mergeStateStatus=BLOCKED` · `reviewDecision=null` · base جلو نزده (`behind_by=0`) · PR draft نیست.
پس مانع check نیست، مرورِ عادی هم نیست. مانع این پرچم در ruleset ‏`27826883` است:
**`require_extra_approval_for_unattributed_changes: true`**

چرا فعال می‌شود — سنجهٔ هویتِ نویسندگان در ۱۰۲ commitِ PR:
  · **۲۰ commit با نویسندهٔ `arena-agent`** (یک کاربرِ جداگانهٔ GitHub، نه همکارِ این مخزن)
  · ۲۳ commit با ایمیلِ بی‌پیوندِ `agent@arena.ai` · ۱ commit با `ci@muscleparadise.local`
  · ۱۰۰ commit از ۱۰۰ تایِ بررسی‌شده trailer ‏`Co-authored-by: arena-agent` دارند
یعنی بخشِ بزرگی از diff از دیدِ GitHub «unattributed» است ⇒ قواعد می‌گویند **یک تأییدِ اضافه از شخصی دیگر** لازم است.
در مخزنِ یک‌نفره آن شخص وجود ندارد ⇒ این پرچم اینجا یک **قفلِ ابدی** است، نه یک کنترل.

### ج) کاری که از تو می‌خواهم — فقط یک تیک

1. باز کن: **https://github.com/yousefghorbanian98-create/MP/settings/rules/27826883**
2. در بخشِ قاعدهٔ **Pull request**، تیکی که متنش دربارهٔ «unattributed changes» / تأییدِ اضافه برای تغییراتِ بی‌انتساب است را **بردار**.
3. پایین صفحه **Save** بزن.
4. به من بگو «تیک برداشته شد».

**به هیچ چیزِ دیگرِ آن صفحه دست نزن:** هر هشت check باید بماند · `strict` باید روشن بماند · enforcement باید `active` بماند · include باید `~DEFAULT_BRANCH` بماند · «Required number of approvals» باید **۰** بماند.

### د) چرا برداشتنش امن است — کنترل‌های جبرانی که سرِ جایشان‌اند

  · هر هشت checkِ اجباری + سیاستِ strict (مانعِ فنیِ واقعی) · قواعدِ `deletion` و `non_fast_forward` روی main
  · داوریِ عددیِ من پیش از هر merge (نقطهٔ بررسیِ ۱) · و خودِ قاعدهٔ ایستاده: **merge فقط با تو**
  آن پرچم فقط یک «تأییدِ انسانیِ دوم» می‌خواست که در مخزنِ تک‌نفره غیرممکن است؛ برداشتنش هیچ گیتِ فنی‌ای را کم نمی‌کند.

بعد از Save، انتظارم `mergeable_state = clean` است؛ خودم دوباره می‌خوانم و ثبت می‌کنم. و باز هم: **merge نمی‌کنیم** تا داوریِ عددی تمام شود.
---

## لایهٔ دومِ قفل: یک branch protection ‏legacy روی `main` — سنجه‌شده، محتوایش نامعلوم

| سنجه | مقدار |
|---|---|
| `GET /branches/main` | **`protected = true`** ⇒ یک قاعدهٔ branch protection قدیمی، **موازیِ** ruleset فعال است |
| `GET /branches/arena/5a1e37b3-mp` | `protected = false` |
| خواندنِ جزئیاتِ قاعده با توکنِ من | **403** ⇒ محتوایش را نمی‌بینم؛ فقط صفحهٔ Settings مالک می‌بیند |
| `mergeable_state` پس از برداشتنِ تیکِ unattributed | هنوز `blocked` (با هشت check سبز و `reviewDecision=null`) |
| status‌های legacy روی head | `state=pending` با **صفر** context |

نتیجهٔ منطقی: قاعدهٔ legacy احتمالاً «Require status checks to pass before merging» را با نامِ check‌های **قدیمی** روشن دارد که هیچ‌وقت گزارش نمی‌شوند ⇒ PR برای همیشه منتظر می‌ماند. (گزینه‌های دیگر مثل «required reviews» با `reviewDecision=null` ناسازگارند.)

**درمانِ درخواستی از مالک:** ‏Settings → Branches → قاعدهٔ `main` → Edit:
در بخشِ «Require status checks to pass before merging» هر context تیک‌خورده را **بردار/پاک کن**؛ اگر بخشِ «Require pull request reviews» تیک دارد و شمارش غیرصفر است، صفرش کن یا تیکش را بردار؛ به «Restrict who can push» و «Allow force pushes / deletions» **دست نزن**؛ Save.
اگر صفحه چیزی غیر از این‌ها نشان داد، به‌جای حدس، اسکرین‌شات بفرست تا دقیق بگویم.

بعد از آن انتظار: ‏`mergeable_state = clean`. خودم می‌خوانم و ثبت می‌کنم. merge همچنان ممنوع تا داوریِ عددی.
---

## پاسخ به «قاعده‌ای نیست، یکی بسازم؟» — **نه.** و تصحیحِ فرضِ «لایهٔ دوم» از خودم

### الف) صفحهٔ Branches خالی، **درست** است

هیچ قاعدهٔ legacy نساز. سیستمِ حفاظتِ این مخزن **فقط** همان ruleset ‏`27826883` است و باید تنها بماند.
آن `protected=true` که از API دیدم اثرِ **خودِ ruleset** روی `main` بوده، نه یک قاعدهٔ موازی.
فرضِ «branch protection قدیمی با check‌های مرده» که در بخشِ قبلی نوشتم **غلط بود** و آن را پس می‌گیرم.

### ب) علتِ واقعیِ `blocked` — ساده و بی‌خطر

باز شدنِ PR #24 یک runِ **دوم** از `mp-ci` راه انداخت (`event=pull_request`، ساعت ۰۸:۵۴:۲۷)، جدا از runِ اولِ `event=push` (۰۸:۱۳).
تا وقتی runِ دوم در جریان بود، check‌های اجباری از دیدِ PR ‏«pending» بودند ⇒ `mergeable_state=blocked`.
وقتی runِ دوم سبز تمام شد، قفل خودبه‌خود باز شد.

| سنجهٔ نهایی | مقدار |
|---|---|
| run‌های `mp-ci` روی head | دو تا: push ‏۰۸:۱۳ و pull_request ‏۰۸:۵۴ — هر دو `completed/success` |
| check-suite‌ها | دو تا، هر دو `completed/success`، هر دو وصل به PR #24 |
| check-run‌ها | ۱۶ مورد (دو موجِ هشت‌تایی)، همه سبز |
| `mergeable_state` | **`clean`** · GraphQL: **`CLEAN`** · `reviewDecision=null` |

### ج) درسِ ثبتی برای خودم

`blocked` با check‌های سبز لزوماً یعنی «قفلِ پنهان» نیست؛ می‌تواند یعنی «یک موجِ دومِ CI هنوز در راه است».
دفعهٔ بعد اول ترتیبِ زمانیِ run‌ها را ببینم (رویدادِ push و pull_request جدا)، بعد دنبالِ قفل بگردم.

### د) وضعیتِ دربِ merge

هیچ مانعِ **فنی** باقی نمانده: هر هشت check سبز · strict راضی · approvals لازم صفر ·merge box ‏clean.
مانعِ باقی‌مانده فقط **فرآیندی** است و عمدی: داوریِ عددیِ من روی بخش‌های ۲ تا  کارِ بیلدر، بعد merge با تو.
هیچ قاعدهٔ تازه‌ای نساز، هیچ تیکِ دیگری نزن، هیچ چیزی را merge نکن.
---

## ارزیابیِ ابزارِ بیرونی: ‏Graphify (سؤالِ مالک، `2026-11-22`) — تصمیم: **الان نه**

سنجه‌ها: مخزن `Graphify-Labs/graphify` · مجوز **Apache-2.0** (فایل LICENSE خوانده شد) · ۱۵۱٬۷۲۶ ستاره · Python · فعال (push ‏۲۰۲۶‑۱۱‑۲۱) · بستهٔ PyPI با نامِ **`graphifyy`** نسخهٔ `0.9.115`، `requires_python >=3.11.5`.
کارش: تبدیلِ کد+داکیومنت+اسکیما+PDF به گرافِ دانشِ قابلِ پرس‌وجو؛ AST محلیِ deterministic با tree-sitter؛ بدون vector store؛ به‌صورت skill برای Claude Code/Cursor/Codex/Gemini CLI و یک سرور MCP محلی (`graphify-mcp`، بدون اکانت).

**«تماماً رایگان؟» — با تفکیک:**
  · بخشِ متن‌باز/محلی: **بله**، Apache-2.0، بدون اکانت؛ حالتِ code-only کاملاً آفلاین و بدون API key («nothing leaves your machine»).
  · استثنا ۱: استخراجِ معناییِ docs/PDF/تصویر محتوا را به یک ارائه‌دهندهٔ LLM می‌فرستد (اولویت: Gemini → Kimi → Claude → OpenAI → Bedrock) ⇒ کلید و هزینهٔ توکن با تو، و داده از ماشین خارج می‌شود.
  · استثنا ۲: سرویسِ ابریِ تجاریِ اختیاری «Graphify Cloud» با مدلِ freemium («Start free, no card required» تیرِ آزمایشی است نه رایگانِ همیشگی).

**به کارِ MP می‌آید؟ صادقانه: الان نه.**
  · MP همین حالا «نقشه از کد» را به‌صورت **گیتِ اجباری در CI** دارد: `interaction_map.py` + گیتِ drift · `route_guard_gate` · `export_routes` · `docs_gate` · گیتِ mermaid · مولدِ inventory. graphify هم‌پوشانی دارد ولی جای آن در CIِ MP خالی نیست.
  · ارزشِ احتمالی‌اش کاوش است («چه کسی این را صدا می‌زند»)؛ در داوریِ من شاهدِ grep/AST مستقیم قابلِ اتکاتر است.
  · ریسک‌ها: منبعِ حقیقتِ موازی (گرافِ cache‌شده با schema bump) · فرستادنِ شواهدِ ممیزی به بیرون در حالتِ docs/PDF (تضاد با محرمانگیِ همین پرونده) · وابستگیِ تازهٔ Python ≥3.11.5 · طراحی برای skill‌های IDE، نه Arena.
  · مجوز Apache-2.0 با قاعدهٔ ایستادهٔ «فقط ابزار آزاد/متن‌باز» سازگار است؛ و چون هرگز نباید وارد artifact توزیعی شود، بحثِ GPL/AGPL هم پیش نمی‌آید.

**تصمیم:** نصب/اتصال نداریم. بعد از بسته شدنِ نقطهٔ بررسیِ ۱ و merge، اگر مالک خواست، فقط حالتِ code-only محلی روی MP آزمایش شود — بدون docs/PDF، بدون Cloud. برگشت‌پذیر و بی‌هزینه.
---

## داوریِ دورِ بیلدر پس از reset دوم: ‏AD‑21 و AD‑22 تأیید · و معمای «+۱» را **من حل کردم**

### الف) AD‑21 (commit ‏`7bbccfa`) — تأیید ✅

| سنجه | مقدار |
|---|---|
| `.github/workflows/apk.yml` | حذف شده (−۱۸۰ خط) · روی tip وجود ندارد |
| تستِ گاردِ APK | حذف شده (−۲۷ خط از `test_release_signing_policy.py`) · grep سراسری: نیافت |
| تستِ signing گریدل | **باقی** · ۶ تابعِ test در همان فایل |
| شمارش | بیلدر: ۱۲۷۶ → ۱۲۷۵ · collect مستقلِ من روی tip: **۱۲۷۵** |

### ب) AD‑22 (commit ‏`7fefb6f`) — تأیید ✅

| سنجه | مقدار |
|---|---|
| `requirements.txt` | ۸۶ خط = ۲ هدر + **۸۴ پینِ `==`** · صفر ورودیِ غیر `==` |
| بررسیِ URL | آن سه موردِ اولِ grep من false-positive بود: `httpcore`/`httptools`/`httpx` نامِ بسته‌اند نه URL |
| پین‌های کلیدی | `fastapi==0.165.0` · `ruff==0.17.6` · و resolve تازهٔ **من** در venv مستقل همین دو را داد ⇒ «صفر تغییر نسخه» مستقل تأیید شد |
| `ci.yml` | دقیقاً **۳** گامِ install به `pip install -c mp-app/backend/requirements.txt -e …` عوض شده (backend · یک گام میانی · e2e-api) |
| DECISIONS | هر دو تصمیم با دلیل، شمارش و «نحوهٔ برگرداندن» ثبت‌اند؛ AD‑22 خودش تصحیحِ نامِ `constraints.txt` → `requirements.txt` را یادداشت کرده |
| CI روی `7fefb6f` | **هر هشت سبز** · PR #24: `head=7fefb6f` · `mergeable_state=clean` |

### ج) معمای «+۱» — حل شد، با مکانیسم و نامِ مقصر

بیلدر ثبت کرده بود: collect ‏۱۲۷۵ ولی خلاصهٔ اجرا ۱۲۷۴ passed + 2 skipped = ۱۲۶، و نتوانسته بود توضیح دهد.
سنجهٔ من در venv مستقل (pytest ‏9.2.0):
  · collect با هر ترکیبِ پرچم: **۱۲۷۵** و فهرستِ node-id‌ها یکسان
  · اجرای `-v`: ‏**۱۲۷۴ خطِ PASSED + دقیقاً ۱ خطِ SKIPPED** = ۱۲۷ نتیجه · صفر node-id تکراری · تفاوتِ مجموعه‌ای با collect = **صفر**
  · پس نتیجهٔ دومِ «skipped» یک **skip در سطحِ ماژول** است: `tests/regression/test_dart_gate.py:25-26` با `pytest.importorskip("tree_sitter", …)` — ماژولی که tree-sitter ندارد، **صفر آیتم collect می‌کند ولی در خلاصه یک skipped شمرده می‌شود**
  · حسابِ بسته: ۱۲۷۵ آیتم = ۱۲۷۴ passed + ۱ skipِ آیتمی (`test_real_apks_pass_the_deep_audit`)؛ خلاصه +۱ skipِ ماژولی = ۱۲۷۶
  ⇒ **هیچ تستِ شبحی وجود ندارد**؛ تفاوت، قراردادِ شمارشِ pytest است نه پنهان‌کاری. بندِ «باز» بیلدر با این مکانیسم بسته می‌شود.

### د) بدهیِ باقی‌ماندهٔ بیلدر: یک commit سند برای اشاره‌های کهنه به `apk.yml`

۱۴ فایل هنوز `apk.yml` را mention می‌کنند. تفکیکِ من:
  · **باید اصلاح شوند** (سندِ عملیاتی‌اند و دستورِ اجرا می‌دهند): `guides/flutter-codespace.md` · `runbooks/codespaces-execution.md` · `RELEASE-CHECKLIST.md` · `READY-TO-BUILD-2026-11-15.md` · `SESSION_HANDOFF.md` · `docs/architecture/repowise/PROJECT-HANDOFF.md` · دو فایلِ `architecture/repowise-*-scope-2026-11-18.txt` · `audit/CHECKLIST.md`
  · **باید بمانند** (رکوردِ تاریخی‌اند؛ بازنویسیِ تاریخ ممنوع): `CHANGELOG.md` · `audit/DECISIONS.md` · `audit/EXECUTION-LOG.md` · `audit/INVENTORY.md` · `audit/findings.json`

### هـ) فایلِ گم‌شدهٔ بیلدر

`share/MP-BUILDER-HANDOFF-A1.3.md` در sandbox او untracked بود و با reset رفت. نسخهٔ commit‌شده در مخزنِ من سالم است و او می‌تواند از همین نشانی بازیابی کند:
`https://github.com/yousefghorbanian98-create/Chat2DB/blob/arena/2cde32d6-chat2db/handoff/MP-BUILDER-HANDOFF-A1.3.md`

**merge همچنان ممنوع:** بیلدر هنوز آیتم‌های READY/TODO لوپ را دارد (۲٫۱، ۲٫۲، ۲٫۳، ٫۳، ۴٫۴ و بقیه) + همین commit سند؛ بعد از آنها داوریِ عددیِ من، بعد merge با تو.

