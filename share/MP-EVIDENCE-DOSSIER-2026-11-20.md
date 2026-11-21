# پروندهٔ کامل تست‌ها، شواهد و منابع — ممیزی اجرایی‌شدهٔ MP

**تاریخ:** ۲۰۲۶‑۱۱‑۲۰ (UTC) · **مخزن ممیزی‌شده:** `MP` @ شاخهٔ `audit-main`، HEAD `662ff88` (فقط‌خواندنی، بدون هیچ تغییر)
**مخزن میزبان این پرونده:** `yousefghorbanian98-create/Chat2DB` @ شاخهٔ `arena/2cde32d6-chat2db`
**نوع سند:** پروندهٔ شواهد (evidence dossier) — مکملِ `share/MP-FINAL-AUDIT-REPORT-2026-11-20.md`
**زبان:** فارسی، با شناسه‌های فنی انگلیسی

---

## ۰) این سند چیست و چگونه خوانده شود

سه سند تحویلی وجود دارد و هر کدام کار متفاوتی می‌کنند:

| سند | نقش | چه کسی می‌خواند |
|---|---|---|
| `share/MP-FINAL-AUDIT-REPORT-2026-11-20.md` | **گزارش یافته‌ها** — ۲۴+۳ یافته با زنجیرهٔ علّی و نقشهٔ رفع | مالک، مهندس ارشد، AI مجری |
| **`share/MP-EVIDENCE-DOSSIER-2026-11-20.md` (این سند)** | **پروندهٔ شواهد** — هر تستی که اجرا شد، با فرمان دقیق، خروجی خام، قضاوت، و hash فایل شاهد؛ به‌علاوهٔ منابع و ردیابی کامل | ممیز بعدی، CI، هر کسی که می‌خواهد ادعاها را **بازآزمایی** کند |
| `share/MP-PROBLEMS-2026-11-20.md` | فهرست یکپارچهٔ ۶۳ مشکل برای کپی/پیست | AI مجریِ رفع |

**قاعدهٔ حاکم بر این پرونده:** هیچ عددی در این سند تایپ دستی نشده است. هر جدول یا از فایل شاهد
(`audit/evidence/*`) با اسکریپت استخراج شده، یا خروجی مستقیم همان فرمان است. اگر عددی با گزارش اصلی
متفاوت است، **این پرونده معتبر است** و اختلاف در §۵ صریحاً فهرست شده است.

**پنج یافتهٔ جدید در همین دور اضافه شد** (F‑25 … F‑29 در §۴) که نتیجهٔ بازاجرای یک پاس تستِ
معیوب است؛ §۵ همهٔ تصحیحات وارد‌شده بر گزارش اصلی را فهرست می‌کند.

---

## ۱) شناسنامهٔ اجرا (chain of custody)

### ۱‑۱) هدف ممیزی و تضمین دست‌نخورده بودن آن

| مورد | مقدار | شاهد |
|---|---|---|
| مخزن ممیزی‌شده | `/tmp/MP` (کلون فقط‌خواندنی) | — |
| شاخه / HEAD | `audit-main` / **`662ff88`** | `git rev-parse --short HEAD` |
| تغییرات در مخزن اصلی | **۰** | `git status --porcelain \| wc -l` = **0** (در پایان هر مرحله و در پایان کار) |
| `git diff --stat HEAD` | **۰ خط** | همان |
| کپی کاری (scratch) | `/tmp/run/MP` | تنها جایی که ابزارها نوشتند (mutmut) و پس از هر جهش با `git checkout --` بازگردانده شد |
| پایگاه‌داده | `/tmp/run/data/mp.db` (بیرون از هر دو مخزن) | — |
| داده‌ها | **کاملاً مصنوعی** — از `qa-report/tools/seed_live.py` خودِ پروژه + کاربران مصنوعی هارنس | هیچ دادهٔ واقعیِ عضو/مالی خوانده یا نوشته نشد |

### ۱‑۲) اثر انگشت محیط

| جزء | نسخه |
|---|---|
| CPU / RAM / دیسک | ۲ vCPU · ~۳٫۶ GB · ۲۰ GB |
| پایتون | ۳٫۱۱٫۲ (`/tmp/run/venv` = محیط اپ، `/tmp/run/venv-audit` = محیط ابزار) |
| Node / npm | v22.22.3 / 10.9.8 |
| fastapi / starlette | 0.165.0 / 1.10.0 |
| sqlalchemy / alembic | 2.1.9 / 1.20.1 |
| pydantic | 2.14.4 |
| uvicorn | 0.54.0 |
| casbin | 1.43.0 |
| structlog / rich | 26.1.0 / 15.0.0 |
| limits | 5.8.0 |
| httpx | 0.28.1 |
| prometheus-client | (از طریق `app/metrics.py`) |
| opentelemetry-sdk | 1.45.2 |
| pytest / pytest-cov / coverage | 9.2.0 / 7.1.0 / 7.17.4 |
| ruff | 0.17.6 |
| hypothesis | 6.170.17 (**در `pyproject.toml` پروژه declare نشده** ⇒ F‑21) |
| semgrep | 1.186.0 |
| mutmut | 2.5.1 (نسخهٔ ۳٫۸٫۱ هم نصب و **رد** شد) |
| radon / lizard / vulture | 6.0.1 / 1.26.1 / 2.16 |
| detect-secrets | 1.5.0 |
| schemathesis | 4.33.4 (نصب شد؛ استفادهٔ کامل نشد — §۸) |
| py-spy | 0.4.4 |
| deepdiff / freezegun / fakeredis / jsonschema | 9.2.1 / 1.5.5 / 2.40.0 / 4.25.1 |

### ۱‑۳) سه پیکربندی سرور که اپ واقعاً در آن‌ها اجرا شد

| # | پیکربندی | فرمان | پورت | چرا |
|---|---|---|---|---|
| S1 | ابزار‌دار (instrumented) | `audit/serve_backend.py` (لاگرهای pool + `/audit/pool` + `/audit/threads` + قالب لاگ قابل انتخاب) | ۸۰۱۰ | اندازه‌گیری اشباع استخر و ظرفیت threadpool |
| S2 | **کنترل خام** | `audit/serve_plain.py` — بدون هیچ ابزار دقیقِ ممیزی | ۸۰۱۰ | اثبات اینکه فروپاشی زیر بار اثر هارنس ممیزی نیست |
| S3 | **CMD واقعی استقرار** | عینِ `mp-app/backend/Dockerfile:27`: `uvicorn app.main:app --host 0.0.0.0 --port … --workers 2 --proxy-headers --forwarded-allow-ips='*'` | ۸۰۱۰ | آزمون XFF در شرایط واقعی (F‑01) |

متغیرهای محیطی مشترک (همه مصنوعی):
`MP_ENVIRONMENT=development` · `MP_DATABASE_URL=sqlite:////tmp/run/data/mp.db` ·
`MP_SECRET_KEY=audit-harness-only-secret-…` · `MP_SMS_PROVIDER=dev` · `MP_PAYMENT_GATEWAY=manual` ·
`MP_RECEIPTS_DIR=/tmp/run/data/receipts` · `MP_TRUSTED_PROXIES=` (خالی) ·
و در S1/S2 additionally `MP_SHOP_ONLINE_PURCHASE_ENABLED=true`, `MP_SHOP_OPEN_HOUR=0`, `MP_SHOP_CLOSE_HOUR=23`.
**تفاوت S3 با S1/S2 عمداً حفظ شد** چون همان چیزی است که در استقرار واقعی اجرا می‌شود؛
پیامدش در §۳‑۲۱ (سلول‌های `409 shop_online_closed`) ثبت شده است.

### ۱‑۴) پیش از هر آزمون: آنچه verify شد

```
$ curl -s http://127.0.0.1:8010/health
{"status":"ok","service":"Muscle Paradise","version":"1.0.0"}
$ curl -s http://127.0.0.1:8010/api/v1/health/ready
{"status":"ready", … "rate_limit_storage_ok":true, …}
$ curl -s http://127.0.0.1:8010/audit/threads      # ظرفیت threadpool ‏(anyio)
{"total_tokens":40, …}
$ curl -s http://127.0.0.1:8010/openapi.json | jq '.paths | length'
141
```

### ۱‑۵) تایم‌لاین واقعی اجرا (از mtime فایل‌های شاهد، UTC)

| زمان (UTC) | فایل شاهد | اندازه |
|---|---|---|
| 11-20 22:10:03 | `backend-coverage.xml` | 426,890 |
| 11-20 22:17:49 | `metrics-noauth.txt` | 6,529 |
| 11-20 22:17:49 | `openapi-live.json` | 171,395 |
| 11-20 22:30:41 | `contract-rbac-findings.json` | 73,763 |
| 11-20 22:30:44 | `contract-invalid-findings.json` | 227 |
| 11-20 22:30:44 | `contract-matrix-raw.json` | 850,104 |
| 11-20 22:33:56 | `pool-events.jsonl` | 23,476 |
| 11-20 22:38:37 | `logging-cost.json` | 1,933 |
| 11-20 22:48:29 | `load-plain-dev.json` | 2,196 |
| 11-20 22:52:11 | `rbac-systemerror-repro.json` | 3,240 |
| 11-20 22:58:56 | `live-security-raw.json` | 17,051 |
| 11-20 22:58:56 | `live-security-verdicts.json` | 4,678 |
| 11-20 23:01:05 | `vulture.txt` | 74 |
| 11-20 23:01:06 | `radon-cc.txt` | 2,283 |
| 11-20 23:01:08 | `radon-mi.txt` | 8,513 |
| 11-20 23:01:08 | `lizard-warnings.txt` | 6,316 |
| 11-20 23:01:09 | `lizard.txt` | 85,468 |
| 11-20 23:01:27 | `bandit.json` | 88,436 |
| 11-20 23:01:59 | `detect-secrets.json` | 51,599 |
| 11-20 23:05:05 | `otp-ratelimit-verdicts.json` | 1,960 |
| 11-20 23:06:36 | `semgrep-backend.json` | 18,984 |
| 11-20 23:07:10 | `semgrep-client.json` | 3,428 |
| 11-20 23:08:46 | `semgrep-summary.txt` | 2,891 |
| 11-20 23:09:01 | `semgrep-studio.json` | 6,573 |
| 11-20 23:11:11 | `otp-bruteforce.json` | 213 |
| 11-20 23:13:42 | `xff-dockerfile-cmd.json` | 462 |
| 11-20 23:14:29 | `eslint-studio.json` | 227,239 |
| 11-20 23:14:31 | `jscpd-out/jscpd-report.json` | 13,131 |
| 11-20 23:14:56 | `knip-err.txt` | 1,132 |
| 11-20 23:14:56 | `contract-diff.json` | 661 |
| 11-20 23:15:37 | `studio-dead-exports.json` | 351 |
| 11-20 23:15:37 | `studio-buttons-wiring.json` | 4,120 |
| 11-20 23:16:28 | `studio-ui-wiring.json` | 3,349 |
| 11-20 23:21:13 | `mutmut-manual-transfer-policy.json` | 4,444 |
| 11-20 23:23:46 | `mutmut-verified.json` | 9,751 |
| 11-21 04:45:02 | `contract-invalid-authed.json` | 477,652 |

**پنجرهٔ اجرا:** 2026-11-20 22:10 تا 2026-11-21 04:45 UTC (≈ ۶ ساعت و ۳۵ دقیقه). آخرین ردیف، پاس ورودی خصمانهٔ بازاجراشده با احراز هویت تأییدشده است (T‑34).

---

## ۲) فهرست کامل تست‌ها — هر چیزی که واقعاً اجرا شد

۴۹ اجرا در ۶ دسته. ستون «شاهد» مسیر فایل خام است؛ ستون «قضاوت» نتیجهٔ نهایی.

### ۲‑۱) دستهٔ A — سوئیت‌های تست خودِ پروژه

| ID | تست | فرمان (خلاصه) | دامنه | زمان | نتیجه | شاهد | قضاوت |
|---|---|---|---|---|---|---|---|
| T‑01 | سوئیت کامل بک‌اند + پوشش | `pytest --cov=. --cov-report=xml` | کل بک‌اند | ۴۶۱٫۸۲ s | **۱۰۹۵ پاس / ۲ skip / ۳۸ warning** · پوشش **۸۳٫۷۳٪** (۹٬۰۲۳/۱۰٬۷۷۶) | `evidence/backend-coverage.xml` | ✅ سبز — ولی عدد پوششِ مستند‌شده غلط است (F‑07) |
| T‑02 | مهاجرت از DB خالی | `alembic upgrade head` روی SQLite تازه | ۳۸ مهاجرت | — | head = **`a7c3d9e1f2b4`** · **۶۵ جدول** | لاگ alembic | ✅ |
| T‑03 | diff ‏ORM ⟷ DB | مقایسهٔ `Base.metadata` با `sqlite_master` | ۶۴ در برابر ۶۴ | — | **صفر اختلاف** | — | ✅ |
| T‑04 | type-check استودیو | `npx tsc --noEmit` | ۵۳ فایل `src` | — | **۰ خطا** (exit 0) | — | ✅ |
| T‑05 | سوئیت تست استودیو | `npx vitest run` | ۴۵ فایل | — | **۲۸۲ پاس / ۹ skip** | — | ✅ (دقیقاً مطابق ادعای مستندات) |
| T‑06 | lint ‏+ format بک‌اند | `ruff check . && ruff format --check .` | ۳۷۸ فایل | — | **All checks passed** · **378 files already formatted** | — | ✅ |

### ۲‑۲) دستهٔ B — تحلیل ایستا

| ID | تست | ابزار | نتیجه | شاهد | قضاوت |
|---|---|---|---|---|---|
| T‑07 | پیچیدگی چرخه‌ای | radon cc `-s -n C --total-average` | **۹۵۶ بلوک** · میانگین **A (۲٫۹۸)** · **۴۱ بلوک ≥C** = C×31 · D×7 · E×1 · **F×2** | `evidence/radon-cc.txt` | ⚠️ دو تابع با درجهٔ **F** |
| T‑08 | قابلیت نگهداشت | radon mi | **۱۹۵ فایل** · A×194 · B×1 · **بدون C یا بدتر** | `evidence/radon-mi.txt` | ✅ |
| T‑09 | پیچیدگی/طول توابع | lizard `--CCN 10 --length 60 -w` | **۷۴۲ تابع** · ۱۷٬۱۱۱ NLOC · میانگین CCN ‏۳٫۵ · **۵۵ هشدار** | `evidence/lizard.txt`, `lizard-warnings.txt` | ⚠️ بدترین CCN ‏**۴۶** |
| T‑10 | کد مرده | vulture `--min-confidence 80` | **۱** یافته (`modules/face_id/deep.py:74` متغیر `image_bgr`) | `evidence/vulture.txt` | ✅ |
| T‑11 | ایمنی ایستا | bandit `-r` روی ۹ دایرکتوری | **۱۰ یافته، همه LOW** · ۲۱٬۳۴۰ LOC · SEVERITY.HIGH = **0** | `evidence/bandit.json` | ✅ |
| T‑12 | آسیب‌پذیری وابستگی‌ها | `pip-audit -r mp-deps.txt --no-deps` | **No known vulnerabilities found** (۲۹ نیازمندی) | — | ✅ |
| T‑13 | رمزِ نشت‌کرده | detect-secrets scan | ۶۴ فایل علامت‌خورده · **۷** اصابت `Secret Keyword` · **۰ رمز واقعی** (همه نام متغیر در سند) | `evidence/detect-secrets.json` | ✅ |
| T‑14 | قواعد اختصاصی بک‌اند | semgrep با `audit/semgrep-mp.yml` | **۱۹** یافته | `evidence/semgrep-backend.json` | ⚠️ |
| T‑15 | قواعد اختصاصی استودیو | همان | **۸** یافته (۷ پولِ شناور + ۱ sentinel منفی) | `evidence/semgrep-studio.json` | ⚠️ |
| T‑16 | قواعد اختصاصی کلاینت Dart | همان | **۱** یافته (`core/api_client.dart:191` cast پویا) | `evidence/semgrep-client.json` | ⚠️ |
| T‑17 | lint واقعی استودیو | ESLint 9 flat config (نخستین اجرای واقعی lint در این پروژه) | **۳۱ error / ۳ warning** در ۵۳ فایل | `evidence/eslint-studio.json` | ❌ (F‑10) |
| T‑18 | وابستگی دوری | madge `--circular` | ۵۴ فایل · **No circular dependency found** | — | ✅ |
| T‑19 | تکرار کد | jscpd `--min-tokens 70` | **۲۱۱ منبع / ۳۹٬۲۷۳ خط / ۹ clone / ۰٫۲۵۷۲٪** | `evidence/jscpd-out/jscpd-report.json` | ✅ |
| T‑20 | مرده‌کایی TS | knip | **کرش در oxc-parser** ⇒ خروجی خالی | `evidence/knip-err.txt` | 🚫 BLOCKED |
| T‑21 | امتیاز جهش | mutmut 2.5.1 + **راستی‌آزمایی دستی** | ۴۵ جهش · گزارش خودِ ابزار «۴۵ زنده» · راستی‌آزمایی: **۲۶ کشته / ۱۹ زنده = ۵۷٫۸٪** | `evidence/mutmut-verified.json` | ⚠️ (F‑11) + ابزار نادقیق |
| T‑22 | سیم‌کشی UI | `audit/scan_ui_wiring.py` (tag-aware) | **۸۴ دکمه** · ۷۴ با `onClick` · **۱۰ بدون** · ۰ تهی · ۸۱ export در `lib/api.ts` · ۴ بی‌import (۲ تای آن‌ها پویا ⇒ **۲ مرده واقعی**) | `evidence/studio-ui-wiring.json` | ⚠️ (F‑19/F‑20/F‑23) |
| T‑23 | اسکن گارد شناسه | `PathId`/`Annotated[int, Path]` در همهٔ روترها | **۰ امضا از `PathId` استفاده می‌کند** · **۵۵ پارامتر مسیر `int` بدون گارد بازه** | `evidence/pathid-scan.json` | ❌ ریشهٔ F‑25 |

### ۲‑۳) دستهٔ C — پراب‌های زنده روی اپِ در حال اجرا

| ID | پراب | اسکریپت | حجم | نتیجهٔ کلیدی | شاهد |
|---|---|---|---|---|---|
| T‑30 | دود (smoke) پس از boot | curl | ۶ درخواست | `/health` ۲۰۰ · `/health/ready` آماده · **`/metrics` ۲۰۰ بدون احراز هویت (۶٬۵۲۹ B)** · OpenAPI ۱۴۱ مسیر · هدرهای امنیتی حاضر · `dev_code` در پاسخ OTP | `evidence/metrics-noauth.txt`, `evidence/openapi-live.json` |
| T‑31 | پاس seed (نوشتن‌های واقعی) | `probe_contract.py seed` | **۱۶ عملیات** | **۱۴ ✅ / ۲ ⚠️** — `shop.cart_add` و `shop.checkout` ⇒ `404 «پروندهٔ عضو یافت نشد»` | `evidence/contract-matrix-raw.json` (pass=`seed`) |
| T‑32 | ماتریس مجوز | `probe_contract.py matrix` | **۱٬۱۴۱ سلول** = ۱۶۳ عملیات × ۷ principal | ۹۸۹ denied · ۹۵ allowed_2xx · ۵۷ reached_4xx · **۰ × 5xx** · **۶۰۲ سلول** که قرارداد «مجاز» گفته ولی سرور انکار کرده | `evidence/contract-matrix-raw.json`, `contract-rbac-findings.json` |
| T‑33 | پاس ورودی خصمانه (نسخهٔ ۱) | `probe_contract.py invalid` | ۸۰۴ سلول | **نادرس‌نتیجه**: ۶۶۴ سلول `401 «نشست معتبر نیست»` چون توکن در پاس قبل با `logout-all` باطل شده بود | `evidence/contract-invalid-findings.json` |
| T‑34 | **پاس ورودی خصمانه (نسخهٔ ۲ — با احراز هویت تأییدشده)** | `probe_invalid_authed.py` (جدید) | **۸۷۲ سلول** | **۰ × 5xx** · **۰ نشت stack trace** · **۴۸ سلول ۲۰۰ روی شناسهٔ غیرمجزا** · ۷۰ × ۴۲۲ `invalid_id` · canary قبل/بعد = ۲۰۰ · **۰ ورود مجدد** | `evidence/contract-invalid-authed.json` |
| T‑35 | باتری امنیت زنده | `probe_live_security.py` | T1–T10 | S1 bypass بدون `sid` · **`/metrics` بی‌احراز هویت** · `amount_rial` تا `10^18` پذیرفته شد · **۰/۱۶** نشت بین‌عضوی · idempotency سالم | `evidence/live-security-verdicts.json`, `live-security-raw.json` |
| T‑36 | محدودیت نرخ OTP | `probe_otp_limits.py` | A–E | A/B **PASS** `[401,401,401,429]` · **C FAIL: ۳۰/۳۰ پذیرفته با XFF** · D ۳/۱۴ · E بدون برچسب IP در متریک | `evidence/otp-ratelimit-verdicts.json` |
| T‑37 | حدس انفجاری OTP | `probe_otp_limits.py bruteforce` | ۶۰ حدس در ۰٫۳ s | **۵۵ × ۴۰۰ `otp_locked` + ۵ × ۴۰۱** · کد واقعی پس از آن ⇒ ۴۰۰ · بازپخش ⇒ ۴۰۰ · **۲۲۸٫۴ حدس/ثانیه** | `evidence/otp-bruteforce.json` |
| T‑38 | **XFF روی CMD واقعی Dockerfile** | curl × ۴۴ روی S3 | ۴۴ درخواست | **۳۰/۳۰ پذیرفته با XFF تصادفی** در برابر **۳/۱۴** پایه ⇒ ضریب تکثیر سبد **۳×** (۲ ورکر) | `evidence/xff-dockerfile-cmd.json` |
| T‑39 | بار ۲۰۰ کلاینت همزمان | `probe_concurrency.py` | ۲۰۰ × چند ثانیه | سرور **قفل** · `/health` تایم‌اوت بیش از ۷ دقیقه · **SIGTERM بی‌پاسخ** ⇒ `kill -9` · لاگ **۱۴۸٬۱۵۴٬۱۰۵ B / ۸۱۷٬۰۱۲ خط برای ۴ خطا** · `py-spy` ⇒ `rich/text.py:760` روی MainThread | `evidence/pool-events.jsonl` + لاگ خام |
| T‑40 | بار پله‌ای روی سرور کنترل | `probe_load.py plain-dev 10 40 60 80` | ۴ پله × ۶۰ s | ۱۰→۱۹۶ rps · ۴۰→۲۰۸٫۸ · ۶۰→۲۰۲٫۴ · **۸۰→۹۴٫۷ rps با p99 ‏۳۰٬۰۲۷ ms و ۸۰ تایم‌اوت و ۱۱/۴۷ ‏`/health` ناموفق و بازیابی ۴۳٫۶۳ s** · **۰ × 5xx در همهٔ پله‌ها** | `evidence/load-plain-dev.json` |
| T‑41 | میکروبنچمارک هزینهٔ لاگ | `bench_logging.py` | ۴ عمق × ۲ رندر × ۵ تکرار | rich: ۹۳٫۶→۲۸۷٫۳ ms و ۳۵٬۹۶۱→۱۲۷٬۱۶۱ B · JSON: ۰٫۰۳ ms و ۲۰۲ B ⇒ تا **~۹٬۶۰۰×** زمان و **~۶۳۰×** حجم | `evidence/logging-cost.json` |
| T‑42 | بازتولید `SystemError` | `repro_rbac_systemerror.py` | ۵ پیکربندی، تا ۳۲٬۰۰۰ فراخوانی | تک‌نخ ⇒ **۰ خطا** · ۸۰ نخ ⇒ **۳–۷ خطا** · حتی در عمق ۵ ⇒ عامل **همزمانی** است نه عمق | `evidence/rbac-systemerror-repro.json` |
| T‑43 | تأخیر `enforce()` | همان اسکریپت | ۳ مسیر × ۳۰۰ فراخوانی | میانه **۲۸۹٫۲ / ۹۱۶٫۱ / ۹۱۱٫۱ µs** · زیر ۸۰ نخ p95 ‏**۳۳۱ ms** و max ‏**۲٬۹۱۳ ms** | همان |
| T‑44 | اثباتِ رفع (جدول پیش‌کامپایل) | PoC داخلی | ۲۴ تصمیم | **۲۴/۲۴ تصمیم یکسان** · **۱۷٫۴ µs در برابر ۹۱۰٫۷ µs (~۵۲×)** | همان |
| T‑45 | diff قرارداد ⟷ OpenAPI زنده | اسکریپت اختصاصی | ۱۶۳ عملیات | **صفر drift در هر دو جهت** · هیستوگرام گاردها · ۹ عملیات بدون گارد · **۰ گارد با نقش تهی** · ۱ گارد تکراری | `evidence/contract-diff.json` |
| T‑46 | مشاهده‌پذیری استخر | `serve_backend.py` + listenerها | ۱۴۵ رویداد | **۹۰ نمونه با `checked_out = 60` = ظرفیت کامل (۴۰+۲۰)** · `held_ms` میانه ۱٬۳۲۳٫۷ و بیشینه ۱٬۹۹۶٫۷ | `evidence/pool-events.jsonl` |
| T‑47 | یکپارچگی DB و بازتاب خروجی پس از حمله | sqlite3 + curl | ۳ بررسی | **۶۵ جدول سالم، `users` = ۲۶۱ ردیف** (هیچ `DROP`ی اثر نکرد) · `note` با `max_length=1000` سقف دارد (`modules/expenses/schemas.py:27`) · رشته‌های خصمانه در هیچ خروجی HTML/CSV بازتاب نشدند · `dangerouslySetInnerHTML` = **۰** | §۳‑۲۴ |
| T‑48 | رفتار وابسته به پیکربندی shop | curl روی S3 در برابر S1 | ۸ سلول | روی S3 (بدون override) ⇒ `409 shop_online_closed` · روی S1 (با `…ENABLED=true`) ⇒ `404 «پروندهٔ عضو یافت نشد»` برای هویت بدون پروندهٔ عضو | `evidence/contract-invalid-authed.json`, `contract-matrix-raw.json` |
| T‑49 | canary زنده بودن توکن | `probe_invalid_authed.py` | ۴ درخواست | قبل و بعد از ۸۷۲ سلول ⇒ **۲۰۰** · `tokens_live_throughout = true` · **۰ ورود مجدد** | همان |
| **T‑50** | **ruff با پیکربندی پیشنهادی** | `ruff 0.17.6 --config audit/ruff-recommended.toml` | **۳۷۶ فایل** | پیکربندی فعلی پروژه ⇒ **۰** یافته؛ `--select ALL` ⇒ ۱۱٬۷۷۸/۱۰۸ قاعده؛ پیشنهادی ⇒ **۴۳۰/۵۲ قاعده** (۴۷ قابل‌رفع خودکار، ۲۱۰ unsafe) | `ruff-recommended-{stats,findings}.txt`، `ruff-all-{rules,families}.txt` |

---

## ۳) نتایج خام هر تست (بدون تفسیر — تفسیر در گزارش اصلی است)

### ۳‑۱) T‑01 · پوشش تست، تفکیک‌شده از `backend-coverage.xml`

| بسته | پوشش | پوشیده/کل | نپوشیده |
|---|---|---|---|
| `engine` | 97.24% | 1,058/1,088 | 30 |
| `security` | 96.61% | 57/59 | 2 |
| `app` | 94.28% | 725/769 | 44 |
| `api` | 93.81% | 91/97 | 6 |
| `modules/*` | 92.28% | 4,746/5,143 | 397 |
| `devtools` | 91.73% | 122/133 | 11 |
| `jobs` | 84.55% | 93/110 | 17 |
| `eval` | 82.56% | 284/344 | 60 |
| `cache` | 76.60% | 72/94 | 22 |
| `db` | 70.40% | 1,213/1,723 | 510 |
| `scripts` | 46.22% | 562/1,216 | 654 |

**۸ فایل با پوشش صفر** (همه در `scripts/`):
`attach_exercise_media.py` · `build_exercise_gifs.py` · `dast.py` · `deploy_gate.py` ·
`export_routes.py` · `locust_m39c3.py` · `seed_s3c_m39.py` · `seed_shop.py`
⇒ دو تای آن‌ها (`dast.py`, `deploy_gate.py`) **خودشان ابزار گیت‌اند** و تست نشده‌اند.

**کم‌پوشش‌ترین فایل‌های ≥۲۰ خط:**

| فایل | پوشش | پوشیده/کل |
|---|---|---|
| `scripts/attach_exercise_media.py` | 0.0% | 0/47 |
| `scripts/build_exercise_gifs.py` | 0.0% | 0/76 |
| `scripts/dast.py` | 0.0% | 0/99 |
| `scripts/deploy_gate.py` | 0.0% | 0/132 |
| `scripts/export_routes.py` | 0.0% | 0/53 |
| `scripts/seed_shop.py` | 0.0% | 0/59 |
| `db/migrations/versions/39f0cd2d8531_initial_schema.py` | 4.9% | 9/183 |
| `db/migrations/versions/c3f01ab129e2_m47_c1_align_indexes_and_nullability_.py` | 19.2% | 10/52 |
| `db/migrations/versions/b7c9d1e2f3a4_m59_shop.py` | 22.0% | 11/50 |
| `db/migrations/versions/0691adce99d0_m51_c1_chat.py` | 29.0% | 9/31 |
| `db/migrations/versions/d2e3f4a5b6c7_qf09_card_to_card.py` | 37.9% | 11/29 |
| `db/migrations/versions/a7c3d9e1f2b4_g2_coupons.py` | 41.7% | 10/24 |

### ۳‑۲) T‑32 · ماتریس مجوز — ۱٬۱۴۱ سلول، تفکیک بر نقش

| نقش | کل | denied | allowed_2xx | reached_4xx | قرارداد «مجاز» ولی سرور انکار کرد |
|---|---|---|---|---|---|
| `None` | 163 | 155 | 6 | 2 | **1** |
| `member` | 163 | 149 | 7 | 7 | **79** |
| `coach` | 163 | 141 | 13 | 9 | **72** |
| `reception` | 163 | 151 | 9 | 3 | **69** |
| `manager` | 163 | 134 | 18 | 11 | **128** |
| `admin` | 163 | 134 | 18 | 11 | **129** |
| `super_admin` | 163 | 125 | 24 | 14 | **124** |
| **جمع** | 1141 | 989 | 95 | 57 | **602** |

توزیع status در این ۱٬۱۴۱ سلول: `401`×۹۰۵ · `200`×۹۵ · `403`×۸۴ · `422`×۴۴ · `404`×۸ · `429`×۴ · `400`×۱ · **`5xx`×۰**
کل زمان اجرا: **۵۶٫۴ ثانیه**. کندترین سلول: `GET /api/v1/metrics` با **۴۳٫۴ ms** (جمع‌آوری prometheus).

**۲۵ مسیرِ نخست در میان ۶۰۲ سلولِ مخالفِ قرارداد:**

| مسیر | تعداد |
|---|---|
| `/api/v1/members/me` | 12 |
| `/api/v1/members/{member_id}` | 11 |
| `/api/v1/shop/cart` | 11 |
| `/api/v1/chat/conversations` | 10 |
| `/api/v1/chat/conversations/{conversation_id}/messages` | 10 |
| `/api/v1/classes` | 10 |
| `/api/v1/members` | 10 |
| `/api/v1/payments` | 10 |
| `/api/v1/payments/{payment_id}/receipt` | 10 |
| `/api/v1/shop/cart/{item_id}` | 10 |
| `/api/v1/shop/change-requests` | 10 |
| `/api/v1/shop/gateways` | 10 |
| `/api/v1/shop/prices` | 10 |
| `/api/v1/shop/products` | 10 |
| `/api/v1/shop/products/{product_id}` | 10 |
| `/api/v1/payments/coupons` | 9 |
| `/api/v1/expenses` | 6 |
| `/api/v1/expenses/{expense_id}` | 6 |
| `/api/v1/expenses/{expense_id}/receipt` | 6 |
| `/api/v1/face/checkin` | 6 |
| `/api/v1/face/checkin-qr` | 6 |
| `/api/v1/face/consent` | 6 |
| `/api/v1/face/consent/revoke` | 6 |
| `/api/v1/face/deep-status` | 6 |
| `/api/v1/face/privacy-notice` | 6 |

شکل گاردها در همان سلول‌های مخالف:
`("permission",)` ×۵۱۹ · `("grant:finance.write","permission")` ×۴۴ · `("authenticated",)` ×۱۷ ·
`("grant:finance.read","permission")` ×۱۵ · `("permission","permission")` ×۳ (F‑13) ·
`("grant:reports.confidential","permission")` ×۳ · `()` ×۱

### ۳‑۳) T‑31 · پاس seed — ۱۶ نوشتن واقعی

| label | درخواست | status | |
|---|---|---|---|
| `member.create` | `POST /api/v1/members` | 200 | ✅ |
| `member.create2` | `POST /api/v1/members` | 200 | ✅ |
| `membership.create` | `POST /api/v1/members/memberships` | 200 | ✅ |
| `coupon.percent` | `POST /api/v1/payments/coupons` | 201 | ✅ |
| `coupon.fixed` | `POST /api/v1/payments/coupons` | 201 | ✅ |
| `payment.cash` | `POST /api/v1/payments` | 200 | ✅ |
| `payment.with_coupon` | `POST /api/v1/payments` | 200 | ✅ |
| `wallet.charge` | `POST /api/v1/payments/wallet/charge` | 200 | ✅ |
| `expense.create` | `POST /api/v1/expenses` | 200 | ✅ |
| `shop.cart_add` | `POST /api/v1/shop/cart` | 404 | ⚠️ |
| `shop.checkout` | `POST /api/v1/shop/checkout` | 404 | ⚠️ |
| `nutrition.weight` | `POST /api/v1/nutrition/weight-logs` | 200 | ✅ |
| `notification.create` | `POST /api/v1/notifications` | 200 | ✅ |
| `chat.conversation` | `POST /api/v1/chat/conversations` | 200 | ✅ |
| `class.create` | `POST /api/v1/classes` | 200 | ✅ |
| `member.create3_for_shop` | `POST /api/v1/members` | 200 | ✅ |

دو ردیف ناموفق، هر دو با بدنهٔ یکسان:
`{"code":"not_found","message":"پروندهٔ عضو یافت نشد — ابتدا پروفایل را کامل کنید"}`
ریشهٔ کدی: `modules/shop/service.py:293-298` → تابع `_own_member(db, user)` که `Member` را با
`user_id` صداکننده پیدا می‌کند و در صورت نبود، `NotFoundError` می‌دهد ⇒ **F‑27**.

### ۳‑۴) T‑33 در برابر T‑34 · دو پاس ورودی خصمانه (و چرا نسخهٔ دوم لازم بود)

| | نسخهٔ ۱ (T‑33) | نسخهٔ ۲ (T‑34) |
|---|---|---|
| اسکریپت | `probe_contract.py invalid` | `probe_invalid_authed.py` |
| سلول‌ها | ۸۰۴ | **۸۷۲** |
| احراز هویت | توکنِ **باطل‌شده** با `logout-all` در پاس قبل | ورود واقعی OTP + canary قبل/بعد |
| `401 «نشست معتبر نیست»` | **۶۶۴** | **۰** |
| ورود مجدد لازم | — | **۰** |
| `tokens_live_throughout` | — | **true** |
| زمان | — | ۷۷٫۶ ثانیه |
| قضاوت | **نادرس‌نتیجه** | معتبر |

**نتیجهٔ نسخهٔ معتبر (۸۷۲ سلول با احراز هویت تأییدشده):**

| status | تعداد |
|---|---|
| ۴۲۲ | ۵۳۱ |
| ۴۰۴ | ۲۲۰ |
| **۲۰۰** | **۵۵** |
| ۴۰۳ | ۳۴ |
| ۴۰۰ | ۲۴ |
| ۴۰۹ | ۸ |
| **۵xx** | **۰** |
| نشت `Traceback` | **۰** |

تفکیک بر نوع تزریق:

| نوع ورودی خصمانه | تعداد | توزیع status | ۲xx |
|---|---|---|---|
| `bad_path_id` | 780 | 401×640, 422×71, 404×65, 200×4 | **4** |
| `hostile_body` | 24 | 401×24 | ۰ |

**۱۲ مقدار تزریقی و سرنوشت هر کدام (دقیق):**

| مقدار تزریقی | سلول‌ها | نتیجه | چرا |
|---|---|---|---|
| `99999999999999999999999` (۲۳ رقم) | ۷۰ | **۴۲۲ `invalid_id`** | `app/id_guard.py:_too_big` → طول > ۱۹ ⇒ گارد سقف کار کرد ✅ |
| `-1` | ۴۸ | **۲۰۰** (۱۲ مسیر) + ۳۶ × ۴۰۴ | `"-1".isdigit() == False` ⇒ گارد اصلاً اجرا نشد ❌ |
| `0` | ۴۸ | **۲۰۰** (۱۲ مسیر) + ۳۶ × ۴۰۴ | گارد فقط **سقف** دارد، کف ندارد ❌ |
| `-0` | ۴۸ | **۲۰۰** (۱۲ مسیر) + ۳۶ × ۴۰۴ | همان ❌ |
| `-9223372036854775808` (INT64_MIN) | ۴۸ | **۲۰۰** (۱۲ مسیر) + ۳۶ × ۴۰۴ | همان ❌ |
| `%2e%2e%2f%2e%2e%2fetc%2fpasswd` | ۷۰ | **۴۰۴** با پاکت `{"detail":"Not Found"}` | مسیر مطابقت نکرد ⇒ F‑26 |
| `abc` / `null` / `1e5` / `1.5` / `1%20OR%201=1` / `1;DROP%20TABLE%20users` | هر کدام ۱ | **۴۰۴** با پاکت پیش‌فرض FastAPI | مبدل `int` رد کرد ⇒ F‑26 |
| ۸ رشتهٔ خصمانه در بدنه | ۳۲ | ۲۵ × ۴۲۲ · **۷ × ۲۰۰** | فقط `expenses.note` متن آزاد است ⇒ §۳‑۲۴ |

**۱۲ مسیری که شناسهٔ غیرمجزا را با HTTP 200 پذیرفتند (F‑25):**

`/api/v1/assessments/jp7/member/{member_id}/trend` · `/api/v1/assessments/member/{member_id}` ·
`/api/v1/axis-assessments/member/{member_id}` · `/api/v1/members/{member_id}/memberships` ·
`/api/v1/notifications/member/{member_id}` · `/api/v1/nutrition/food-logs/member/{member_id}/daily` ·
`/api/v1/nutrition/member/{member_id}/adaptive` · `/api/v1/nutrition/plans/member/{member_id}` ·
`/api/v1/payments/{payment_id}/gateway-return` · `/api/v1/programs/member/{member_id}` ·
`/api/v1/programs/member/{member_id}/readiness` · `/api/v1/programs/member/{member_id}/volume`

**شکل پاکت خطا در ۷۲۲ سلولِ ≥۴۰۰ (F‑26):**

| status | پاکت پروژه `{"error":{code,message,details}}` | پاکت پیش‌فرض `{"detail":…}` |
|---|---|---|
| ۴۰۰ | ۲۴ | ۰ |
| ۴۰۳ | ۳۴ | ۰ |
| ۴۰۴ | **۱۵۰** | **۷۰** |
| ۴۰۹ | ۸ | ۰ |
| ۴۲۲ | ۵۳۱ | ۰ |

### ۳‑۵) T‑35 · باتری امنیت زنده (T1–T10)

```json
[
 {
  "id": "T1",
  "hypothesis": "هر IP یک سبد مستقل ۱۰/دقیقه دارد",
  "observed": "3 درخواست از ۱۴ پذیرفته شد، نخستین ۴۲۹ در درخواست شمارهٔ 4",
  "status": "PASS",
  "fix": ""
 },
 {
  "id": "T2",
  "hypothesis": "با MP_TRUSTED_PROXIES='' هدرهای پراکسی نادیده گرفته می‌شوند (پس همهٔ کاربران پشت یک پراکسی **یک سبد مشترک** دارند)",
  "observed": "X-Forwarded-For تصادفی نتیجه را عوض کرد ⇒ accepted=14 (در برابر 3 بدون هدر)",
  "status": "PASS",
  "fix": "MP_TRUSTED_PROXIES را در production الزامی و اعتبارسنجی کن؛ در OPS-RUNBOOK مقدار واقعی پراکسی (Caddy) را مستند کن و آزمون بگذار که بدون آن ۴۲۹ نادرست ندهد."
 },
 {
  "id": "T3",
  "hypothesis": "کد اشتباه نباید هرگز پذیرفته شود و پس از سقف تلاش، کد باطل شود",
  "observed": "12 حدس اشتباه ⇒ هیچ‌کدام ۲۰۰ نشد",
  "status": "PASS",
  "fix": ""
 },
 {
  "id": "T3b",
  "hypothesis": "پس از N حدس ناموفق، کد واقعی باید قفل شده باشد (otp_max_attempts=5)",
  "observed": "کد واقعی پس از 12 حدس ناموفق ⇒ HTTP 429",
  "status": "PASS",
  "fix": "اگر ۲۰۰ است: قفل حدس (attempt counter) روی کد اعمال نمی‌شود؛ شمارنده را در جدول otp_codes نگه دار و پس از ۵ تلاش کد را باطل کن."
 },
 {
  "id": "T4",
  "hypothesis": "مقادیر بزرگ‌تر از 2^53−1 باید رد شوند (422) چون JSON/دارت/TS آن‌ها را دقیق نگه نمی‌دارند",
  "observed": "3 مورد ناامن با موفقیت پذیرفته شد: ['2^53', '2^53+1 (ناامن)', '10^18']",
  "status": "FAIL",
  "fix": "سقف amount_rial را در schema با le=2**53-1 ببند و آزمون مرزی بگذار."
 },
 {
  "id": "T4b",
  "hypothesis": "مبلغ منفی/صفر باید رد شود",
  "observed": "منفی ⇒ HTTP 422, صفر ⇒ HTTP 422",
  "status": "PASS",
  "fix": ""
 },
 {
  "id": "T5",
  "hypothesis": "دو درخواست با کلید idempotency یکسان باید یک رکورد بسازند",
  "observed": "HTTP 200/200 با id=9 و id=9 ⇒ یکسان",
  "status": "PASS",
  "fix": ""
 },
 {
  "id": "T6",
  "hypothesis": "توکن یک عضو نباید دادهٔ عضو دیگر را بخواند (۴۰۳/۴۰۴ انتظار می‌رود)",
  "observed": "0 پاسخ ۲۰۰ از 16 درخواست بین‌عضوی",
  "status": "PASS",
  "fix": "روی هر مسیر عضو‌محور `ensure_member_scope` بگذار و ماتریس permission×ownership را در تست بیاور."
 },
 {
  "id": "T7",
  "hypothesis": "Origin غیرمجاز نباید بازتاب داده شود (fail-closed)",
  "observed": "[{\"origin\": \"https://evil.example.com\", \"status\": 400, \"allow_origin\": null, \"allow_creds\": \"true\"}, {\"origin\": \"http://127.0.0.1:5173\", \"status\": 200, \"allow_origin\": \"http://127.0.0.1:5173\", \"allow_creds\": \"true\"}, {\"o",
  "status": "FAIL",
  "fix": ""
 },
 {
  "id": "T8",
  "hypothesis": "پاسخ خطا نباید جزئیات فنی/مسیر فایل نشت دهد",
  "observed": "HTTP 404 markers=[] body={\"error\":{\"code\":\"not_found\",\"message\":\"عضو یافت نشد\",\"details\":[]}}",
  "status": "PASS",
  "fix": ""
 },
 {
  "id": "T8b",
  "hypothesis": "/api/v1/metrics باید پشت احراز هویت/شبکهٔ داخلی باشد",
  "observed": "HTTP 200 بدون هیچ توکنی؛ 346 خط، 14 متریک از جمله نام مسیرها و وضعیت outbox",
  "status": "FAIL",
  "fix": "مسیر را با require_permission محافظت کن یا فقط روی پورت/اینترفیس داخلی ببند؛ در Caddy هم مسیر /metrics را از دسترس عمومی خارج کن."
 },
 {
  "id": "T9",
  "hypothesis": "کد OTP باید یک‌بارمصرف باشد",
  "observed": "بار اول HTTP 429، بار دوم HTTP 429",
  "status": "PASS",
  "fix": ""
 },
 {
  "id": "T10",
  "hypothesis": "همهٔ هدرهای امنیتی روی پاسخ ۲۰۰ حاضر باشند",
  "observed": "HTTP 200; حاضر: ['content-security-policy', 'x-frame-options', 'x-content-type-options', 'referrer-policy', 'permissions-policy', 'cross-origin-opener-policy']; غایب: ['strict-transport-security']",
  "status": "NOTE",
  "fix": "در production باید HSTS هم باشد (فقط وقتی environment=production)."
 }
]
```

> **هشدار تفسیری:** در این فایل، `status: "PASS"` یعنی «آزمون اجرا شد و پاسخ قطعی داد».
> در مورد **T2** پاسخ قطعی این بود که **فرضیه رد شد** (هدر XFF نتیجه را عوض کرد) ⇒ همان چیزی که
> در گزارش اصلی به‌عنوان F‑01 آمده است. این تلهٔ معنایی عمداً در پرونده ثبت می‌شود تا خوانندهٔ بعدی
> `PASS` را با «سالم» اشتباه نگیرد.

### ۳‑۶) T‑36 · آزمون‌های A–E محدودیت نرخ OTP

```json
[
 {
  "test": "A",
  "phone": "09138589669",
  "wrong_guesses": [
   401,
   401,
   401,
   429
  ],
  "real_code_after_4_wrong": 429,
  "real_code_replay": 429,
  "replay_body": "{\"error\":{\"code\":\"rate_limited\",\"message\":\"تعداد درخواست‌ها زیاد است؛ کمی بعد تلاش کنید\",\"details\":[]}}",
  "verdict_one_time": "PASS",
  "verdict_under_limit": "NOTE"
 },
 {
  "test": "B",
  "wrong_guess_statuses": [
   401,
   401,
   401,
   429
  ],
  "real_code_after": 429,
  "real_body": "{\"error\":{\"code\":\"rate_limited\",\"message\":\"تعداد درخواست‌ها زیاد است؛ کمی بعد تلاش کنید\",\"details\":[]}}",
  "verdict": "PASS",
  "note": "429 یعنی سبد rate-limit؛ 4xx دیگر یعنی قفلِ شمارندهٔ تلاش"
 },
 {
  "test": "C",
  "label": "سرور جاری",
  "requests": 30,
  "accepted": 30,
  "limited": 0,
  "statuses": [
   200,
   200,
   200,
   200,
   200,
   200,
   200,
   200,
   200,
   200,
   200,
   200
  ],
  "verdict": "FAIL",
  "note": "اگر تقریباً همه پذیرفته شوند ⇒ کلید سبد از هدرِ کنترل‌شدهٔ کلاینت می‌آید"
 },
 {
  "test": "D",
  "requests": 14,
  "accepted": 3,
  "statuses": [
   200,
   200,
   200,
   429,
   429,
   429,
   429,
   429,
   429,
   429,
   429,
   429,
   429,
   429
  ],
  "note": "سقف انتظار: ۱۰ در دقیقه (otp_rate_limit) + ۳ در ثانیه (burst)"
 },
 {
  "test": "E",
  "metrics_lines": 24,
  "sample": [
   "mp_http_requests_total{method=\"GET\",route=\"unmatched\",status=\"404\"} 20764.0",
   "mp_http_requests_total{method=\"POST\",route=\"/auth/otp/request\",status=\"200\"} 71.0",
   "mp_http_requests_total{method=\"POST\",route=\"/auth/otp/verify\",status=\"200\"} 14.0"
  ],
  "note": "متریک برچسب IP ندارد ⇒ نمی‌توان کلاینت متخلف را از متریک پیدا کرد"
 }
]
```

### ۳‑۷) T‑37 · حدس انفجاری OTP

```json
{
 "phone": "09137777627",
 "wrong_attempts": 60,
 "status_distribution": {
  "400": 55,
  "401": 5
 },
 "real_code_after_60_wrong": 400,
 "replay_status": 400,
 "guess_rate_per_second": 228.4,
 "elapsed_s": 0.3
}
```

### ۳‑۸) T‑38 · XFF روی CMD واقعی Dockerfile

```json
{
 "server": "exact Dockerfile CMD (2 workers, --proxy-headers --forwarded-allow-ips='*')",
 "xff_spoof_accepted": 30,
 "xff_spoof_total": 30,
 "baseline_accepted": 3,
 "baseline_total": 14,
 "baseline_statuses": [
  200,
  200,
  200,
  429,
  429,
  429,
  429,
  429,
  429,
  429,
  429,
  429,
  429,
  429
 ],
 "xff_statuses": [
  200,
  200,
  200,
  200,
  200,
  200,
  200,
  200,
  200,
  200,
  200,
  200
 ],
 "per_worker_bucket_multiplication": 3
}
```

### ۳‑۹) T‑40 · بار پله‌ای روی سرور کنترل

```json
{
 "tag": "plain-dev",
 "rows": [
  {
   "tag": "plain-dev",
   "workers": 40,
   "step_seconds": 60.2,
   "requests": 12564,
   "rps": 208.8,
   "status_counts": {
    "200": 6646,
    "404": 5918
   },
   "error_kinds": {},
   "p50_ms": 207.2,
   "p95_ms": 351.3,
   "p99_ms": 418.9,
   "max_ms": 816.0,
   "client_timeouts": 0,
   "server_errors_5xx": 0,
   "max_pool_checkedout_observed": null,
   "pool_samples": 0,
   "health_during_load": {
    "probes": 89,
    "failed_probes": 0,
    "max_health_ms": 356.6
   },
   "recovery_seconds": 0.03
  },
  {
   "tag": "plain-dev",
   "workers": 60,
   "step_seconds": 60.2,
   "requests": 12191,
   "rps": 202.4,
   "status_counts": {
    "200": 6628,
    "404": 5563
   },
   "error_kinds": {},
   "p50_ms": 316.6,
   "p95_ms": 515.9,
   "p99_ms": 577.7,
   "max_ms": 726.5,
   "client_timeouts": 0,
   "server_errors_5xx": 0,
   "max_pool_checkedout_observed": null,
   "pool_samples": 0,
   "health_during_load": {
    "probes": 80,
    "failed_probes": 0,
    "max_health_ms": 515.3
   },
   "recovery_seconds": 0.03
  },
  {
   "tag": "plain-dev",
   "workers": 80,
   "step_seconds": 63.9,
   "requests": 6049,
   "rps": 94.7,
   "status_counts": {
    "200": 3275,
    "404": 2694,
    "None": 80
   },
   "error_kinds": {
    "timeout": 80
   },
   "p50_ms": 466.9,
   "p95_ms": 802.0,
   "p99_ms": 30027.5,
   "max_ms": 30486.6,
   "client_timeouts": 80,
   "server_errors_5xx": 0,
   "max_pool_checkedout_observed": null,
   "pool_samples": 0,
   "health_during_load": {
    "probes": 47,
    "failed_probes": 11,
    "max_health_ms": 5054.7
   },
   "recovery_seconds": 43.63
  },
  {
   "tag": "plain-dev",
   "workers": 10,
   "step_seconds": 60.0,
   "requests": 11770,
   "rps": 196.0,
   "status_counts": {
    "200": 5962,
    "404": 5808
   },
   "error_kinds": {},
   "p50_ms": 52.2,
   "p95_ms": 103.2,
   "p99_ms": 183.7,
   "max_ms": 409.6,
   "client_timeouts": 0,
   "server_errors_5xx": 0,
   "max_pool_checkedout_observed": null,
   "pool_samples": 0,
   "health_during_load": {
    "probes": 107,
    "failed_probes": 0,
    "max_health_ms": 180.6
   },
   "recovery_seconds": 0.03
  }
 ],
 "updated_at": "22:48:29"
}
```


### ۳‑۱۰) T‑41 · هزینهٔ رندر لاگ

```json
{
 "note": "زمان‌ها روی نخ event loop صرف می‌شوند؛ یعنی در همان مدت هیچ درخواست دیگری (حتی /health) سرو نمی‌شود.",
 "rows": [
  {
   "renderer": "ConsoleRenderer+rich (development)",
   "traceback_depth": 10,
   "repeats": 5,
   "mean_ms": 93.56,
   "median_ms": 96.85,
   "max_ms": 109.21,
   "bytes_per_error": 35961,
   "lines_per_error": 253
  },
  {
   "renderer": "JSONRenderer (production)",
   "traceback_depth": 10,
   "repeats": 5,
   "mean_ms": 0.03,
   "median_ms": 0.02,
   "max_ms": 0.09,
   "bytes_per_error": 202,
   "lines_per_error": 1
  },
  {
   "renderer": "ConsoleRenderer+rich (development)",
   "traceback_depth": 25,
   "repeats": 5,
   "mean_ms": 148.59,
   "median_ms": 157.4,
   "max_ms": 168.43,
   "bytes_per_error": 63321,
   "lines_per_error": 463
  },
  {
   "renderer": "JSONRenderer (production)",
   "traceback_depth": 25,
   "repeats": 5,
   "mean_ms": 0.03,
   "median_ms": 0.02,
   "max_ms": 0.09,
   "bytes_per_error": 202,
   "lines_per_error": 1
  },
  {
   "renderer": "ConsoleRenderer+rich (development)",
   "traceback_depth": 40,
   "repeats": 5,
   "mean_ms": 211.31,
   "median_ms": 209.58,
   "max_ms": 227.04,
   "bytes_per_error": 90681,
   "lines_per_error": 673
  },
  {
   "renderer": "JSONRenderer (production)",
   "traceback_depth": 40,
   "repeats": 5,
   "mean_ms": 0.04,
   "median_ms": 0.02,
   "max_ms": 0.08,
   "bytes_per_error": 202,
   "lines_per_error": 1
  },
  {
   "renderer": "ConsoleRenderer+rich (development)",
   "traceback_depth": 60,
   "repeats": 5,
   "mean_ms": 287.33,
   "median_ms": 293.6,
   "max_ms": 306.33,
   "bytes_per_error": 127161,
   "lines_per_error": 953
  },
  {
   "renderer": "JSONRenderer (production)",
   "traceback_depth": 60,
   "repeats": 5,
   "mean_ms": 0.03,
   "median_ms": 0.01,
   "max_ms": 0.09,
   "bytes_per_error": 202,
   "lines_per_error": 1
  }
 ]
}
```

### ۳‑۱۱) T‑42/T‑43/T‑44 · بازتولید `SystemError` و اثبات رفع

```json
[
 {
  "threads": 80,
  "stack_depth": 40,
  "calls_per_thread": 400,
  "total_calls": 32000,
  "elapsed_s": 33.2,
  "throughput_calls_per_s": 964.2,
  "errors": {
   "SystemError": 3
  },
  "error_samples": [
   "SystemError: AST constructor recursion depth mismatch (before=159, after=154)",
   "SystemError: AST constructor recursion depth mismatch (before=159, after=155)",
   "SystemError: AST constructor recursion depth mismatch (before=159, after=154)"
  ],
  "latency_ms": {
   "p50": 1.041,
   "p95": 331.47,
   "max": 2912.88
  },
  "note": "casbin روی هر enforce عبارت را compile/eval می‌کند؛ enable_cache در security/rbac.py فعال نشده است."
 },
 {
  "threads": 1,
  "stack_depth": 40,
  "calls_per_thread": 300,
  "total_calls": 300,
  "elapsed_s": 0.2,
  "throughput_calls_per_s": 1216.3,
  "errors": {},
  "error_samples": [],
  "latency_ms": {
   "p50": 0.906,
   "p95": 1.01,
   "max": 2.747
  },
  "note": "casbin روی هر enforce عبارت را compile/eval می‌کند؛ enable_cache در security/rbac.py فعال نشده است."
 },
 {
  "threads": 80,
  "stack_depth": 5,
  "calls_per_thread": 300,
  "total_calls": 24000,
  "elapsed_s": 25.2,
  "throughput_calls_per_s": 953.1,
  "errors": {
   "SystemError": 3
  },
  "error_samples": [
   "SystemError: AST constructor recursion depth mismatch (before=54, after=49)",
   "SystemError: AST constructor recursion depth mismatch (before=54, after=49)",
   "SystemError: AST constructor recursion depth mismatch (before=54, after=49)"
  ],
  "latency_ms": {
   "p50": 1.049,
   "p95": 331.002,
   "max": 2169.117
  },
  "note": "casbin روی هر enforce عبارت را compile/eval می‌کند؛ enable_cache در security/rbac.py فعال نشده است."
 },
 {
  "threads": 20,
  "stack_depth": 40,
  "calls_per_thread": 300,
  "total_calls": 6000,
  "elapsed_s": 6.1,
  "throughput_calls_per_s": 983.0,
  "errors": {
   "SystemError": 2
  },
  "error_samples": [
   "SystemError: AST constructor recursion depth mismatch (before=159, after=154)",
   "SystemError: AST constructor recursion depth mismatch (before=159, after=155)"
  ],
  "latency_ms": {
   "p50": 1.018,
   "p95": 134.617,
   "max": 488.296
  },
  "note": "casbin روی هر enforce عبارت را compile/eval می‌کند؛ enable_cache در security/rbac.py فعال نشده است."
 },
 {
  "threads": 80,
  "stack_depth": 40,
  "calls_per_thread": 150,
  "total_calls": 12000,
  "elapsed_s": 12.5,
  "throughput_calls_per_s": 957.4,
  "errors": {
   "SystemError": 7
  },
  "error_samples": [
   "SystemError: AST constructor recursion depth mismatch (before=159, after=154)",
   "SystemError: AST constructor recursion depth mismatch (before=159, after=154)",
   "SystemError: AST constructor recursion depth mismatch (before=159, after=153)",
   "SystemError: AST constructor recursion depth mismatch (before=159, after=158)",
   "SystemError: AST constructor recursion depth mismatch (before=159, after=155)"
  ],
  "latency_ms": {
   "p50": 1.022,
   "p95": 176.33,
   "max": 895.62
  },
  "note": "casbin روی هر enforce عبارت را compile/eval می‌کند؛ enable_cache در security/rbac.py فعال نشده است."
 }
]
```

### ۳‑۱۲) T‑45 · diff قرارداد ⟷ OpenAPI زنده

```json
{
 "only_in_routes_json": [],
 "only_in_live": [],
 "guard_distribution": {
  "('permission',)": 129,
  "('grant:finance.write', 'permission')": 12,
  "()": 9,
  "('authenticated',)": 6,
  "('grant:finance.read', 'permission')": 5,
  "('permission', 'permission')": 1,
  "('grant:reports.confidential', 'permission')": 1
 },
 "no_guard": [
  "POST /api/v1/auth/logout",
  "POST /api/v1/auth/otp/request",
  "POST /api/v1/auth/otp/verify",
  "POST /api/v1/auth/refresh",
  "GET /api/v1/health/ready",
  "GET /api/v1/metrics",
  "GET /api/v1/payments/{payment_id}/gateway-return",
  "GET /api/v1/updates/manifest",
  "GET /health"
 ],
 "guard_without_roles": []
}
```

### ۳‑۱۳) T‑46 · رویدادهای استخر اتصال (سرور ابزار‌دار)

کل ۱۴۵ رویداد، همه از نوع `held_over_1s`:

* بیشینهٔ `checked_out` = **۶۰** = ظرفیت کامل (`pool_size=40` + `max_overflow=20`)
* **۹۰ نمونه از ۱۴۵** در وضعیت `checked_out = 60` (اشباع کامل)
* کمینهٔ مشاهده‌شده ۲۷
* `held_ms`: میانه **۱٬۳۲۳٫۷** · بیشینه **۱٬۹۹۶٫۷**

نخستین و آخرین رویداد:

```json
{"t": 1795214029.8725, "kind": "held_over_1s", "held_ms": 1149.1, "checked_out": 27,
 "overflow": -13, "pool_size": 40, "pool_checkedout": 27, "pool_overflow": -13}
{"t": 1795214036.0976, "kind": "held_over_1s", "held_ms": 1996.7, "checked_out": 60,
 "overflow": 20, "pool_size": 40, "pool_checkedout": 60, "pool_overflow": 20}
```

### ۳‑۱۴) T‑30 · خانواده‌های متریکِ عمومی (`GET /api/v1/metrics` بدون احراز هویت)

**۱۲ خانواده** (۳۴۶ خط، ۶٬۵۲۹ بایت) — و جست‌وجوی `pool|conn|session|sqlite|queue` در آن: **۰ تطبیق**.

| خانواده |
|---|
| `mp_http_request_duration_seconds_bucket` |
| `mp_http_request_duration_seconds_count` |
| `mp_http_request_duration_seconds_created` |
| `mp_http_request_duration_seconds_sum` |
| `mp_http_requests_created` |
| `mp_http_requests_total` |
| `mp_outbox_dead` |
| `mp_outbox_dead_letters` |
| `mp_outbox_oldest_pending_seconds` |
| `mp_outbox_pending` |
| `mp_outbox_sending` |
| `mp_outbox_worker_stale` |

### ۳‑۱۵) T‑07 · radon cc — ۴۱ بلوک ≥C (از بدترین)

| بلوک | محل | نوع | درجه | CC |
|---|---|---|---|---|
| `Settings.validate_production_configuration` | `app/config.py:128` | M | **F** | 47 |
| `prescribe_axis_work` | `engine/axis_prescription.py:43` | F | **F** | 46 |
| `next_transfer_state` | `modules/payments/manual_transfer_policy.py:45` | F | **E** | 34 |
| `estimate_percentile` | `engine/scoring.py:33` | F | **D** | 28 |
| `analyze` | `engine/segmental.py:66` | F | **D** | 26 |
| `build_confidential_report` | `modules/reporting/service.py:30` | F | **D** | 25 |
| `assess_member_risk` | `engine/churn_risk.py:22` | F | **D** | 22 |
| `screen` | `engine/safety.py:94` | F | **D** | 22 |
| `jp7_trend` | `modules/assessment/service.py:146` | F | **D** | 21 |
| `apply_suggestions` | `engine/feedback_apply.py:54` | F | **D** | 21 |
| `get_current_user` | `app/deps.py:42` | F | **C** | 17 |
| `members_summary` | `modules/admin/analytics.py:342` | F | **C** | 17 |
| `upsert_gateway` | `modules/shop/service.py:558` | F | **C** | 17 |
| `process_set_feedback` | `engine/set_feedback.py:24` | F | **C** | 16 |
| `log_food` | `modules/nutrition/service.py:103` | F | **C** | 15 |
| `daily_summary` | `modules/nutrition/service.py:170` | F | **C** | 15 |
| `weekly_volume_report` | `modules/programs/service.py:267` | F | **C** | 15 |
| `sync_set_feedback` | `modules/programs/service.py:517` | F | **C** | 15 |
| `create_product` | `modules/shop/service.py:207` | F | **C** | 15 |
| `add_to_cart` | `modules/shop/service.py:301` | F | **C** | 15 |
| `weight_trend` | `engine/adaptive_nutrition.py:132` | F | **C** | 15 |
| `adaptive_nutrition_report` | `modules/nutrition/service.py:372` | F | **C** | 14 |
| `checkout` | `modules/shop/service.py:391` | F | **C** | 14 |
| `plan` | `engine/reminders.py:37` | F | **C** | 14 |
| `confirm_phone_change` | `modules/auth/service.py:338` | F | **C** | 13 |
| `list_programs_summary` | `modules/programs/service.py:211` | F | **C** | 13 |
| `readiness_report` | `modules/programs/service.py:369` | F | **C** | 13 |
| `_safety_gate` | `modules/programs/service.py:474` | F | **C** | 13 |
| `suggest_calorie_adjustment` | `engine/adaptive_nutrition.py:286` | F | **C** | 13 |
| `aggregate_axis_scores` | `engine/axis_map.py:31` | F | **C** | 13 |
| `client_ip` | `app/security/proxy.py:42` | F | **C** | 12 |
| `update` | `modules/expenses/service.py:72` | F | **C** | 12 |
| `collect_member_facts` | `modules/admin/analytics.py:199` | F | **C** | 12 |
| `verify_with_gateway` | `modules/payments/service.py:249` | F | **C** | 12 |
| `list_products` | `modules/shop/service.py:132` | F | **C** | 12 |
| `suggest_next_weight` | `engine/autoreg.py:19` | F | **C** | 12 |
| `Settings` | `app/config.py:19` | C | **C** | 11 |
| `next_questions` | `modules/population/intake.py:102` | F | **C** | 11 |
| `assess_readiness` | `engine/readiness.py:206` | F | **C** | 11 |
| `resolve` | `engine/sync_lww.py:45` | F | **C** | 11 |
| `generate_program` | `engine/workout.py:223` | F | **C** | 11 |

توزیع درجه‌ها (فقط ۴۱ بلوک ≥C از میان ۹۵۶ بلوک تحلیل‌شده):

| درجه | تعداد |
|---|---|
| C | 31 |
| D | 7 |
| E | 1 |
| F | 2 |

میانگین پیچیدگی کل: **A (۲٫۹۸۲۲)**. ⇒ دو تابع با درجهٔ **F** وجود دارد:
`app/config.py:128 Settings.validate_production_configuration` ‏(CC ۴۷) و
`engine/axis_prescription.py:43 prescribe_axis_work` ‏(CC ۴۶).

### ۳‑۱۶) T‑08 · radon mi — ۱۴ فایل با پایین‌ترین شاخص نگهداشت

| فایل | درجه | MI |
|---|---|---|
| `modules/shop/service.py` | B | 13.45 |
| `modules/face_id/service.py` | A | 29.57 |
| `modules/auth/service.py` | A | 31.03 |
| `modules/payments/service.py` | A | 32.68 |
| `modules/nutrition/service.py` | A | 33.93 |
| `modules/programs/service.py` | A | 35.84 |
| `modules/admin/analytics.py` | A | 38.04 |
| `modules/axis_assessment/service.py` | A | 40.09 |
| `modules/membership/service.py` | A | 40.52 |
| `modules/assessment/service.py` | A | 41.34 |
| `app/config.py` | A | 41.97 |
| `modules/payments/receipts.py` | A | 42.26 |
| `modules/classes/service.py` | A | 42.72 |
| `app/security/jwt.py` | A | 43.32 |

از ۱۹۵ فایل: **A×194 · B×1 · C و بدتر = ۰**.

### ۳‑۱۷) T‑09 · lizard — ۵۵ هشدار، مرتب بر حسب CCN

| تابع | محل | NLOC | CCN | token | طول |
|---|---|---|---|---|---|
| `validate_production_configuration` | `app/config.py:128` | 100 | **46** | 1 | 116 |
| `prescribe_axis_work` | `engine/axis_prescription.py:43` | 122 | **46** | 3 | 147 |
| `next_transfer_state` | `modules/payments/manual_transfer_policy.py:45` | 60 | **34** | 10 | 73 |
| `estimate_percentile` | `engine/scoring.py:33` | 48 | **28** | 3 | 60 |
| `analyze` | `engine/segmental.py:66` | 85 | **26** | 3 | 96 |
| `build_confidential_report` | `modules/reporting/service.py:30` | 157 | **25** | 2 | 174 |
| `assess_member_risk` | `engine/churn_risk.py:22` | 60 | **22** | 1 | 81 |
| `screen` | `engine/safety.py:94` | 64 | **22** | 4 | 76 |
| `jp7_trend` | `modules/assessment/service.py:146` | 128 | **21** | 3 | 154 |
| `apply_suggestions` | `engine/feedback_apply.py:54` | 93 | **21** | 4 | 113 |
| `get_current_user` | `app/deps.py:42` | 42 | **17** | 2 | 55 |
| `members_summary` | `modules/admin/analytics.py:342` | 72 | **17** | 2 | 88 |
| `upsert_gateway` | `modules/shop/service.py:558` | 49 | **17** | 4 | 49 |
| `process_set_feedback` | `engine/set_feedback.py:24` | 64 | **16** | 1 | 82 |
| `log_food` | `modules/nutrition/service.py:103` | 57 | **15** | 4 | 65 |
| `daily_summary` | `modules/nutrition/service.py:170` | 106 | **15** | 4 | 118 |
| `weekly_volume_report` | `modules/programs/service.py:267` | 76 | **15** | 3 | 95 |
| `sync_set_feedback` | `modules/programs/service.py:517` | 86 | **15** | 4 | 104 |
| `create_product` | `modules/shop/service.py:207` | 50 | **15** | 4 | 51 |
| `add_to_cart` | `modules/shop/service.py:301` | 38 | **15** | 5 | 38 |
| `weight_trend` | `engine/adaptive_nutrition.py:132` | 65 | **15** | 1 | 80 |
| `adaptive_nutrition_report` | `modules/nutrition/service.py:372` | 67 | **14** | 3 | 86 |
| `checkout` | `modules/shop/service.py:391` | 65 | **14** | 4 | 73 |
| `plan` | `engine/reminders.py:37` | 94 | **14** | 5 | 108 |
| `confirm_phone_change` | `modules/auth/service.py:338` | 67 | **13** | 4 | 77 |
| `list_programs_summary` | `modules/programs/service.py:211` | 40 | **13** | 3 | 49 |
| `readiness_report` | `modules/programs/service.py:369` | 75 | **13** | 2 | 100 |
| `_safety_gate` | `modules/programs/service.py:474` | 24 | **13** | 3 | 36 |
| `suggest_calorie_adjustment` | `engine/adaptive_nutrition.py:286` | 89 | **13** | 5 | 103 |
| `aggregate_axis_scores` | `engine/axis_map.py:31` | 21 | **13** | 1 | 26 |
| `client_ip` | `app/security/proxy.py:42` | 15 | **12** | 2 | 19 |
| `update` | `modules/expenses/service.py:72` | 45 | **12** | 4 | 48 |
| `collect_member_facts` | `modules/admin/analytics.py:199` | 51 | **12** | 2 | 76 |
| `verify_with_gateway` | `modules/payments/service.py:249` | 31 | **12** | 5 | 42 |
| `list_products` | `modules/shop/service.py:132` | 34 | **12** | 6 | 35 |
| `suggest_next_weight` | `engine/autoreg.py:19` | 33 | **12** | 4 | 41 |
| `next_questions` | `modules/population/intake.py:102` | 13 | **11** | 3 | 15 |
| `assess_readiness` | `engine/readiness.py:206` | 71 | **11** | 8 | 84 |
| `resolve` | `engine/sync_lww.py:45` | 61 | **11** | 3 | 78 |
| `generate_program` | `engine/workout.py:223` | 48 | **11** | 5 | 52 |
| `create_assessment` | `modules/axis_assessment/service.py:72` | 79 | **10** | 5 | 83 |
| `build_order_receipt` | `modules/payments/invoice.py:92` | 48 | **10** | 3 | 61 |
| `reverse` | `modules/payments/ledger.py:123` | 58 | **10** | 5 | 64 |
| `decide_axis` | `engine/axis_rules.py:52` | 54 | **10** | 4 | 61 |
| `estimate_tdee` | `engine/adaptive_nutrition.py:214` | 58 | **9** | 3 | 70 |
| `upgrade` | `db/migrations/versions/c3f01ab129e2_m47_c1_align_indexes_and_nullability_.py:42` | 66 | **8** | 0 | 83 |
| `approve_payment` | `modules/payments/receipts.py:167` | 65 | **7** | 3 | 70 |
| `create_program_from_engine_output` | `modules/programs/service.py:74` | 55 | **6** | 4 | 73 |
| `submit_receipt` | `modules/payments/receipts.py:85` | 61 | **5** | 5 | 66 |
| `create_app` | `app/main.py:44` | 56 | **4** | 0 | 111 |
| `upgrade` | `db/migrations/versions/d2e3f4a5b6c7_qf09_card_to_card.py:26` | 59 | **1** | 0 | 62 |
| `upgrade` | `db/migrations/versions/0691adce99d0_m51_c1_chat.py:21` | 70 | **1** | 0 | 72 |
| `upgrade` | `db/migrations/versions/39f0cd2d8531_initial_schema.py:21` | 646 | **1** | 0 | 648 |
| `downgrade` | `db/migrations/versions/39f0cd2d8531_initial_schema.py:672` | 95 | **1** | 0 | 97 |
| `upgrade` | `db/migrations/versions/b7c9d1e2f3a4_m59_shop.py:41` | 188 | **1** | 0 | 199 |

تمرکز هشدارها بر حسب فایل:

| فایل | تعداد هشدار |
|---|---|
| `modules/programs/service.py` | 6 |
| `modules/shop/service.py` | 5 |
| `modules/nutrition/service.py` | 3 |
| `engine/adaptive_nutrition.py` | 3 |
| `modules/admin/analytics.py` | 2 |
| `modules/payments/receipts.py` | 2 |
| `db/migrations/versions/39f0cd2d8531_initial_schema.py` | 2 |
| `app/config.py` | 1 |
| `engine/axis_prescription.py` | 1 |
| `modules/payments/manual_transfer_policy.py` | 1 |
| `engine/scoring.py` | 1 |
| `engine/segmental.py` | 1 |

### ۳‑۱۸) T‑14/T‑15/T‑16 · semgrep — هر ۲۸ یافته با `file:line`

۱۷ قاعدهٔ اختصاصی آفلاین در `audit/semgrep-mp.yml` (قابل commit مستقیم در CI خودشان).

**بک‌اند (۱۹):**

| قاعده | فایل | خط |
|---|---|---|
| `mp-dev-otp-code-gated-only-by-provider` | `modules/auth/service.py` | 52 |
| `mp-dev-otp-code-gated-only-by-provider` | `modules/auth/service.py` | 260 |
| `mp-jwt-without-session-binding` | `scripts/dast.py` | 66 |
| `mp-jwt-without-session-binding` | `scripts/seed_s3c_m39.py` | 28 |
| `mp-money-division` | `modules/admin/analytics.py` | 157 |
| `mp-money-division` | `modules/admin/analytics.py` | 325 |
| `mp-raw-sql-fstring` | `db/migrations/versions/c3f01ab129e2_m47_c1_align_indexes_and_nullability_.py` | 67 |
| `mp-raw-sql-fstring` | `db/migrations/versions/c3f01ab129e2_m47_c1_align_indexes_and_nullability_.py` | 165 |
| `mp-raw-sql-fstring` | `db/migrations/versions/c3f01ab129e2_m47_c1_align_indexes_and_nullability_.py` | 169 |
| `mp-raw-sql-fstring` | `db/migrations/versions/c3f01ab129e2_m47_c1_align_indexes_and_nullability_.py` | 171 |
| `mp-session-without-context-manager` | `scripts/build_progressions.py` | 241 |
| `mp-session-without-context-manager` | `scripts/import_exercise_catalog.py` | 145 |
| `mp-session-without-context-manager` | `scripts/seed_criteria.py` | 107 |
| `mp-session-without-context-manager` | `scripts/seed_norms.py` | 276 |
| `mp-session-without-context-manager` | `scripts/tag_axis_coverage.py` | 675 |
| `mp-silent-except-pass` | `api/v1/monitoring.py` | 18 |
| `mp-silent-except-pass` | `scripts/dast.py` | 79 |
| `mp-silent-except-pass` | `scripts/dast.py` | 174 |
| `mp-silent-except-pass` | `scripts/dast.py` | 180 |

**استودیو (۸):**

| قاعده | فایل | خط |
|---|---|---|
| `mp-ts-float-money` | `components/PaymentPanel.tsx` | 69 |
| `mp-ts-float-money` | `pages/Analytics.tsx` | 101 |
| `mp-ts-float-money` | `pages/Analytics.tsx` | 105 |
| `mp-ts-float-money` | `pages/Shop.tsx` | 624 |
| `mp-ts-float-money` | `pages/Shop.tsx` | 671 |
| `mp-ts-float-money` | `pages/Shop.tsx` | 785 |
| `mp-ts-float-money` | `pages/Shop.tsx` | 786 |
| `mp-ts-negative-sentinel-member-id` | `pages/Nutrition.tsx` | 50 |

**کلاینت Dart (۱):**

| قاعده | فایل | خط |
|---|---|---|
| `mp-dart-dynamic-cast` | `core/api_client.dart` | 191 |

### ۳‑۱۹) T‑17 · ESLint 9 — توزیع قاعده‌ها و بدترین فایل‌ها

| قاعده | تعداد |
|---|---|
| `react-hooks/set-state-in-effect` | 18 |
| `jsx-a11y/label-has-associated-control` | 12 |
| `@typescript-eslint/no-unused-vars` | 2 |
| `None` | 1 |
| `jsx-a11y/no-autofocus` | 1 |

| فایل | تعداد پیام |
|---|---|
| `CouponPanel.tsx` | 5 |
| `Expenses.tsx` | 5 |
| `AdminPermissions.tsx` | 4 |
| `PaymentPanel.tsx` | 2 |
| `Chat.tsx` | 2 |
| `DeviceSessions.tsx` | 1 |
| `ExerciseLibrary.tsx` | 1 |
| `FoodLibrary.tsx` | 1 |
| `LedgerPanel.tsx` | 1 |
| `PeriodReportPanel.tsx` | 1 |
| `PhoneChangeDialog.tsx` | 1 |
| `ReceiptQueue.tsx` | 1 |
| `RemindersPanel.tsx` | 1 |
| `RoleManager.tsx` | 1 |

### ۳‑۲۰) T‑19 · jscpd — هر ۹ clone

| خط | محل نخست | محل دوم | زبان |
|---|---|---|---|
| 14 | `features/nutrition/adaptive_nutrition_card.dart:15` | `features/nutrition/nutrition_page.dart:140` | dart |
| 14 | `components/ExerciseLibrary.tsx:41` | `components/FoodLibrary.tsx:29` | tsx |
| 13 | `features/shop/my_orders_sheet.dart:33` | `features/shop/order_receipt_sheet.dart:63` | dart |
| 13 | `features/shop/my_orders_sheet.dart:33` | `features/shop/shop_page.dart:388` | dart |
| 11 | `features/chat/member_chat_page.dart:174` | `features/chat/member_chat_page.dart:268` | dart |
| 10 | `reports/period.py:80` | `reports/schedule.py:55` | python |
| 9 | `features/wallet/wallet_page.dart:96` | `features/wallet/wallet_page.dart:366` | dart |
| 9 | `lib/api.ts:583` | `lib/api.ts:604` | typescript |
| 8 | `admin/router.py:107` | `admin/schemas.py:37` | python |

### ۳‑۲۱) T‑21 · آزمون جهش — هر ۴۵ جهش با قضاوت راستی‌آزمایی‌شده

ماژول هدف: `modules/payments/manual_transfer_policy.py` (۱۱۷ خط) ·
تست: `tests/regression/test_manual_transfer_policy.py` (۱۴ آزمون، ۵۴ مورد پارامتریک، ۰٫۰۸ s) ·
**امتیاز راستی‌آزمایی‌شده: ۲۶/۴۵ = ۵۷٫۸٪** ·
یادداشت ابزار: *«mutmut 2.x خودش همهٔ ۴۵ را «زنده» گزارش کرد؛ هر جهش دستی اعمال و با pytest راستی‌آزمایی شد.»*

| # | خط | جهش | کشته شد؟ |
|---|---|---|---|
| `1` | 12 | `AWAITING_PROOF = "awaiting_proof"` ⟶ `AWAITING_PROOF = "XXawaiting_proofXX"` | ❌ خیر |
| `2` | 12 | `AWAITING_PROOF = "awaiting_proof"` ⟶ `AWAITING_PROOF = None` | ✅ بله |
| `3` | 13 | `PENDING_REVIEW = "pending_review"` ⟶ `PENDING_REVIEW = "XXpending_reviewXX"` | ❌ خیر |
| `4` | 13 | `PENDING_REVIEW = "pending_review"` ⟶ `PENDING_REVIEW = None` | ✅ بله |
| `5` | 14 | `REJECTED = "rejected"` ⟶ `REJECTED = "XXrejectedXX"` | ❌ خیر |
| `6` | 14 | `REJECTED = "rejected"` ⟶ `REJECTED = None` | ✅ بله |
| `7` | 15 | `APPROVED = "approved"` ⟶ `APPROVED = "XXapprovedXX"` | ❌ خیر |
| `8` | 15 | `APPROVED = "approved"` ⟶ `APPROVED = None` | ✅ بله |
| `9` | 16 | `EXPIRED = "expired"` ⟶ `EXPIRED = "XXexpiredXX"` | ❌ خیر |
| `10` | 16 | `EXPIRED = "expired"` ⟶ `EXPIRED = None` | ✅ بله |
| `11` | 17 | `CANCELLED = "cancelled"` ⟶ `CANCELLED = "XXcancelledXX"` | ❌ خیر |
| `12` | 17 | `CANCELLED = "cancelled"` ⟶ `CANCELLED = None` | ✅ بله |
| `13` | 21 | `SUBMIT = "submit"` ⟶ `SUBMIT = "XXsubmitXX"` | ❌ خیر |
| `14` | 21 | `SUBMIT = "submit"` ⟶ `SUBMIT = None` | ✅ بله |
| `15` | 22 | `APPROVE = "approve"` ⟶ `APPROVE = "XXapproveXX"` | ❌ خیر |
| `16` | 22 | `APPROVE = "approve"` ⟶ `APPROVE = None` | ✅ بله |
| `17` | 23 | `REJECT = "reject"` ⟶ `REJECT = "XXrejectXX"` | ❌ خیر |
| `18` | 23 | `REJECT = "reject"` ⟶ `REJECT = None` | ✅ بله |
| `19` | 24 | `EXPIRE = "expire"` ⟶ `EXPIRE = "XXexpireXX"` | ❌ خیر |
| `20` | 24 | `EXPIRE = "expire"` ⟶ `EXPIRE = None` | ✅ بله |
| `21` | 25 | `CANCEL = "cancel"` ⟶ `CANCEL = "XXcancelXX"` | ❌ خیر |
| `22` | 25 | `CANCEL = "cancel"` ⟶ `CANCEL = None` | ✅ بله |
| `23` | 34 | `isinstance(value, datetime) and value.tzinfo` ⟶ `isinstance(value, datetime) and value.tzinfo` | ✅ بله |
| `24` | 34 | `isinstance(value, datetime) and value.tzinfo` ⟶ `isinstance(value, datetime) and value.tzinfo` | ✅ بله |
| `25` | 34 | `isinstance(value, datetime) and value.tzinfo` ⟶ `isinstance(value, datetime) or value.tzinfo ` | ✅ بله |
| `26` | 39 | `return type(value) is int and value > 0` ⟶ `return type(value) is not int and value > 0` | ✅ بله |
| `27` | 39 | `return type(value) is int and value > 0` ⟶ `return type(value) is int and value >= 0` | ❌ خیر |
| `28` | 39 | `return type(value) is int and value > 0` ⟶ `return type(value) is int and value > 1` | ✅ بله |
| `29` | 39 | `return type(value) is int and value > 0` ⟶ `return type(value) is int or value > 0` | ✅ بله |
| `30` | 48 | `order_open: bool = True,` ⟶ `order_open: bool = False,` | ✅ بله |
| `31` | 49 | `bank_verified: bool = False,` ⟶ `bank_verified: bool = True,` | ❌ خیر |
| `32` | 52 | `bank_reference: str = "",` ⟶ `bank_reference: str = "XXXX",` | ❌ خیر |
| `33` | 53 | `rejection_reason: str = "",` ⟶ `rejection_reason: str = "XXXX",` | ❌ خیر |
| `34` | 62 | `if not isinstance(state, TransferState) or n` ⟶ `if  isinstance(state, TransferState) or not ` | ✅ بله |
| `35` | 62 | `if not isinstance(state, TransferState) or n` ⟶ `if not isinstance(state, TransferState) or  ` | ✅ بله |
| `36` | 62 | `if not isinstance(state, TransferState) or n` ⟶ `if not isinstance(state, TransferState) and ` | ❌ خیر |
| `37` | 63 | `raise TransferPolicyError("invalid state or ` ⟶ `raise TransferPolicyError("XXinvalid state o` | ❌ خیر |
| `38` | 64 | `if not _aware(now) or not _aware(deadline):` ⟶ `if  _aware(now) or not _aware(deadline):` | ✅ بله |
| `39` | 64 | `if not _aware(now) or not _aware(deadline):` ⟶ `if not _aware(now) or  _aware(deadline):` | ✅ بله |
| `40` | 64 | `if not _aware(now) or not _aware(deadline):` ⟶ `if not _aware(now) and not _aware(deadline):` | ✅ بله |
| `41` | 65 | `raise TransferPolicyError("timestamps must b` ⟶ `raise TransferPolicyError("XXtimestamps must` | ❌ خیر |
| `42` | 66 | `if type(order_open) is not bool or type(bank` ⟶ `if type(order_open) is  bool or type(bank_ve` | ✅ بله |
| `43` | 66 | `if type(order_open) is not bool or type(bank` ⟶ `if type(order_open) is not bool or type(bank` | ✅ بله |
| `44` | 66 | `if type(order_open) is not bool or type(bank` ⟶ `if type(order_open) is not bool and type(ban` | ✅ بله |
| `45` | 67 | `raise TransferPolicyError("boolean inputs re` ⟶ `raise TransferPolicyError("XXboolean inputs ` | ❌ خیر |

### ۳‑۲۲) T‑11/T‑13/T‑10 · bandit، detect-secrets، vulture

**bandit (۱۰ یافته، همه LOW):**

| test_id | شدت | اطمینان | فایل | خط |
|---|---|---|---|---|
| `B110` | LOW | `HIGH` | api/v1/monitoring.py | `24` |
| `B105` | LOW | `MEDIUM` | app/config.py | `16` |
| `B105` | LOW | `MEDIUM` | modules/auth/service.py | `100` |
| `B105` | LOW | `MEDIUM` | modules/auth/service.py | `130` |
| `B107` | LOW | `MEDIUM` | modules/payments/service.py | `249` |
| `B101` | LOW | `HIGH` | scripts/build_exercise_gifs.py | `108` |
| `B101` | LOW | `HIGH` | scripts/build_exercise_gifs.py | `109` |
| `B112` | LOW | `HIGH` | scripts/dast.py | `81` |
| `B112` | LOW | `HIGH` | scripts/dast.py | `176` |
| `B112` | LOW | `HIGH` | scripts/dast.py | `187` |

**detect-secrets — ۷ اصابت `Secret Keyword` (بررسی دستی همه: نام متغیر در سند، نه مقدار):**

| فایل | نوع | خط |
|---|---|---|
| `docs/MuscleParadise/OPS-RUNBOOK.md` | Secret Keyword | 15 |
| `finn/reports/m112-release-signing-hardening.md` | Secret Keyword | 38 |
| `mp-app/backend/app/config.py` | Secret Keyword | 16 |
| `mp-app/backend/tests/integration/test_m59_shop.py` | Secret Keyword | 237 |
| `mp-app/backend/tests/regression/test_production_ops.py` | Secret Keyword | 25 |
| `mp-app/backend/tests/regression/test_production_ops.py` | Secret Keyword | 44 |
| `mp-app/backend/tests/regression/test_production_ops.py` | Secret Keyword | 54 |

**vulture (اطمینان ≥۸۰٪):**

```
modules/face_id/deep.py:74: unused variable 'image_bgr' (100% confidence)
```

### ۳‑۲۳) T‑22 · سیم‌کشی UI استودیو

```json
{
 "buttons_total": 84,
 "buttons_with_onClick": 74,
 "buttons_without_onClick": 10,
 "buttons_without_onClick_list": [
  "components/AdminPermissions.tsx:246",
  "components/DeviceSessions.tsx:117",
  "components/PhoneChangeDialog.tsx:173",
  "components/ReceiptQueue.tsx:129",
  "components/TopBar.tsx:8",
  "pages/Expenses.tsx:332",
  "pages/Shop.tsx:651",
  "pages/Shop.tsx:696",
  "pages/Shop.tsx:741",
  "pages/Shop.tsx:820"
 ],
 "buttons_empty_onClick": [],
 "buttons_onClick_without_api_call": [
  "components/Feedback.tsx:98 → () => dismiss(t.id)}\n              aria-label=\"بستن پیام\"\n  ",
  "components/AdminPermissions.tsx:140 → () => void loadUsersAndKeys()",
  "components/AdminPermissions.tsx:197 → () => void submit()",
  "components/FoodLibrary.tsx:76 → () => {\n            setCategory(null);\n            setQuery(",
  "components/FoodLibrary.tsx:105 → () => setCategory(category === cat ? null : cat)",
  "components/LedgerPanel.tsx:164 → () => {\n                        setReversing(row);\n         ",
  "components/PaymentPanel.tsx:262 → reset",
  "components/PhoneChangeDialog.tsx:156 → restart",
  "components/PhoneChangeDialog.tsx:165 → onClose",
  "components/ReceiptQueue.tsx:133 → () => setRejecting(row)",
  "components/RoleManager.tsx:89 → () => revokeUserRole(u.id).then(load).catch((e) => setError(",
  "components/Sidebar.tsx:62 → () => setPage(item.id)",
  "components/Sidebar.tsx:91 → () => void signOut()",
  "components/TopBar.tsx:107 → () => setPhoneChangeOpen(true)",
  "components/ExerciseLibrary.tsx:81 → () => setGroup(null)",
  "components/ExerciseLibrary.tsx:88 → () => setGroup(g === group ? null : g)",
  "components/ExerciseLibrary.tsx:109 → () => setOpen(isOpen ? null : r.exercise_id)}\n              ",
  "components/MemberTable.tsx:58 → reload",
  "components/UpdateBanner.tsx:27 → apply",
  "components/VolumePanel.tsx:94 → () => setLevel(l.key)",
  "pages/Expenses.tsx:314 → () => {\n                        setEditing(row);\n           ",
  "pages/Expenses.tsx:337 → () => setRemoving(row)",
  "pages/Finance.tsx:106 → fetchSummary",
  "pages/Finance.tsx:109 → downloadCsv",
  "pages/Finance.tsx:161 → calculateCommission",
  "pages/Shop.tsx:161 → () => setTab(t.id)",
  "pages/Shop.tsx:211 → () => setFilter(\"\")",
  "pages/Shop.tsx:219 → () => setFilter(c.slug)",
  "pages/Shop.tsx:338 → () => window.print()",
  "pages/Shop.tsx:409 → () => setConfirmCheckout(true)",
  "pages/Shop.tsx:512 → () => setPendingApproval(r)",
  "pages/Nutrition.tsx:257 → () => setSelected(f)",
  "pages/Chat.tsx:171 → () => {\n                setActiveId(c.id);\n                s",
  "pages/CheckIn.tsx:66 → () => setScanning((s) => !s)",
  "pages/Login.tsx:85 → () => void requestCode()",
  "pages/Login.tsx:117 → () => void verifyCode()",
  "pages/Login.tsx:125 → () => void requestCode()",
  "pages/Members.tsx:70 → () => setGenderFilter(t.key)",
  "pages/Members.tsx:185 → () => setPage(\"programs\")",
  "pages/Programs.tsx:102 → () => setStatus(f.key)"
 ],
 "api_functions_exported": 79,
 "api_functions_never_imported": [
  "fetchOrderReceipt",
  "getToken",
  "markOrderStatus",
  "updateProduct"
 ],
 "pages_without_any_api_import": [
  "pages/Analytics.tsx",
  "pages/Assessment.tsx",
  "pages/Login.tsx"
 ]
}
```



### ۳‑۲۴) T‑47 · یکپارچگی داده پس از رشته‌های خصمانه

۷ رشتهٔ خصمانه در `POST /api/v1/expenses` ⇒ **HTTP 200** و ذخیرهٔ عینی در ستون `note`:

| id | طول | مقدار ذخیره‌شده |
|---|---|---|
| ۶ | ۱۱ | `' OR 1=1 --` |
| ۷ | ۲۳ | `"; DROP TABLE users; --` |
| ۸ | ۲۵ | `<script>alert(1)</script>` |
| ۹ | ۱۶ | `../../etc/passwd` |
| ۱۰ | ۳ | `%00` |
| ۱۱ | ۱۸ | `\r\nInjected: header` |
| ۱۲ | ۷ | `{{7*7}}` |

**آزمون‌های تکمیلی و نتیجهٔ هر کدام:**

| پرسش | آزمون | نتیجه |
|---|---|---|
| آیا `DROP TABLE users` اثر کرد؟ | `select count(*) from sqlite_master where type='table'` و `select count(*) from users` | **۶۵ جدول سالم · `users` = ۲۶۱ ردیف** ⇒ پارامتری‌سازی SQLAlchemy درست است ✅ |
| آیا ورودی بدون سقف طول ذخیره می‌شود؟ | ارسال رشتهٔ ۵٬۰۰۰ کاراکتری + `select count(*) where length(note)>1000` | **۴۲۲** و **۰ ردیف بلند** ⇒ `note: str = Field("", max_length=1000)` در `modules/expenses/schemas.py:27` ✅ |
| آیا مقدار خصمانه در خروجی HTML بازتاب می‌شود؟ | `GET /api/v1/expenses/6/receipt` | **۴۰۴ `«این هزینه فیش ندارد»`** ⇒ هیچ بازتابی رخ نداد ✅ |
| آیا در CSV بازتاب می‌شود؟ | `GET /api/v1/payments/finance/export.csv` | ۲۰۰ · ۴۹۶ بایت · فقط ستون‌های پرداخت؛ **هیچ‌کدام از ۵ نشانگر خصمانه در آن نیست** ✅ |
| آیا مسیر XSS در وب باز است؟ | `grep -rc dangerouslySetInnerHTML studio/src` | **۰** ⇒ React به‌طور پیش‌فرض escape می‌کند ✅ |

**نتیجهٔ دقیق:** ذخیرهٔ عینیِ متن آزاد **طراحی درست** است (پارامتری، سقف‌دار، بدون بازتاب).
ریسک باقی‌مانده **آینده‌نگر** است: به محض افزودن هر خروجی جدید که `note` را رندر می‌کند
(PDF فیش، CSV هزینه‌ها، ICS، عنوان اعلان push) این مقادیر به بردار تزریق تبدیل می‌شوند ⇒
پیشنهاد: «قرارداد encode‌کردن در خروجی» + یک آزمون رگرسیون که همین ۷ نشانگر را در هر خروجی
جدید بررسی کند (نه اصلاح امروز).

### ۳‑۲۵) T‑23 · اسکن گارد شناسه در سطح کد

| کمیت | مقدار |
|---|---|
| تعریف `PathId` | `app/deps.py:39` → `Annotated[int, Path(ge=1, le=MAX_SAFE_ID)]` |
| **کاربرد `PathId` در امضای روترها** | **۰** |
| اشاره‌های دیگر به `PathId` | فقط در docstringهای `app/id_guard.py` و `app/ids.py` (توضیحِ اینکه چرا middleware انتخاب شد) |
| پارامتر مسیر `int` بدون گارد بازه | **۵۵** |
| بیشترین تمرکز | `modules/payments/router.py` (۱۱) · `modules/shop/router.py` (۸) · `modules/programs/router.py` (۶) |

تصمیم معماریِ خودِ پروژه (نقل از docstring `app/id_guard.py`):
> «`PathId` راه درست در سطح تایپ است، اما نیاز به تغییر ۴۱ امضا دارد و هر endpoint جدیدی که فراموش
> کند دوباره سوراخ می‌شود. این middleware همان قاعده را یک‌جا اعمال می‌کند…»

یعنی انتخاب middleware **آگاهانه و مستند** بوده؛ نقص امروز این است که آن middleware **فقط سقف** را
اعمال می‌کند و `isdigit()` مقادیر منفی را اصلاً نمی‌بیند (§۴‑۱).


### ۳‑۲۶) T‑50 · ruff ‏۰٫۱۷٫۶ روی ۳۷۶ فایل بک‌اند — سه پیکربندی در برابر هم

اجرا در `/tmp/run/MP/mp-app/backend` (کپیِ دست‌نخوردهٔ `MP` ‏HEAD `662ff88`)، همیشه با `--no-cache`
تا کشِ ruff نتیجه را خوش‌بینانه نکند. زمان‌ها با `time.perf_counter()` روی همان فرمان‌ها:

| پیکربندی | یافته | قاعدهٔ درگیر | زمان | exit code |
| --- | --- | --- | --- | --- |
| `pyproject.toml` فعلی پروژه (`E,F,W,I,N,UP,B,SIM`) | **۰** — «All checks passed!» | ۸ خانواده | **۵۳٫۳ ms** | ۰ |
| `audit/ruff-recommended.toml` (پیشنهادِ این ممیزی) | **۴۳۰** | **۵۲ قاعده** | **۱۰۱٫۳ ms** | ۱ |
| `--select ALL` (همهٔ خانواده‌ها) | **۱۱٬۷۷۸** | **۱۰۸ قاعده** | **۳۴۳٫۱ ms** | ۱ |
| `ruff format --check` | **۰** — «۳۷۸ فایل پیشاپیس قالب‌بندی‌شده» | — | **۵۹٫۹ ms** | ۰ |

**سه نتیجهٔ مستقیم از این جدول:**

1. **گیتِ lint امروز «سبزِ توخالی» است.** صفر یافته نه به معنای صفر مشکل، که به معنای
   «فقط ۸ خانواده از ~۵۰ خانواده روشن است». با روشن‌کردنِ خانواده‌های باگ‌یاب، عدد از ۰ به **۴۳۰** می‌رود
   و دو باگِ واقعی (F‑28, F‑29) بیرون می‌آید.
2. **هزینهٔ زمانی عملاً صفر است.** کلِ بررسی با ۵۲ قاعده **۱۰۱ ms** است در برابر **۴۶۱٫۸۲ ثانیه**
   برای pytest بک‌اند — یعنی دروازه‌گذاریِ ruff در CI هیچ بهانه‌ای از نظر زمان ندارد
   (۰٫۰۲٪ زمانِ پایپ‌لاین).
3. **`ruff format` رایگان است.** خروجی `--check` روی همهٔ ۳۷۸ فایل «already formatted» است ⇒
   افزودنِ `ruff format --check` به CI **هیچ diff** تولید نمی‌کند و فقط از بازگشتِ نامرتب‌شدگی جلوگیری می‌کند.

**توزیع ۴۳۰ یافته بر پایهٔ دایرکتوری** (برای فازبندیِ مهاجرت):

| دایرکتوری | یافته | دایرکتوری | یافته |
| --- | --- | --- | --- |
| `modules/` | **۱۸۰** | `scripts/` | ۳۸ |
| `tests/` | ۸۸ | `app/` | ۳۸ |
| `db/` | ۴۶ | `engine/` | ۱۷ |
| `eval/` | ۱۴ | `security/` | ۴ |
| `cache/` | ۲ | `jobs/`, `devtools/`, `api/` | ۱+۱+۱ |

**چرا `--select ALL` به‌عنوان گیت رد شد (۱۱٬۷۷۸ یافته):**

| خانواده | تعداد | چرا قابل‌فعال‌کردن نیست |
| --- | --- | --- |
| `S101` (`assert`) | **۲٬۷۳۶** | همه در تست‌ها؛ pytest عمداً از `assert` استفاده می‌کند ⇒ با per-file-ignore حل شد |
| `RUF001/002/003` («ambiguous unicode») | **۱٬۴۹۵** | متنِ فارسیِ رشته‌ها و docstringها (نیم‌فاصلهٔ U+200C و `؟`) — کدبیس فارسی است، این یافته‌ها کاذب‌اند |
| `D` (docstring) | ۱٬۴۹۹ | ارزش دارد ولی یک پروژهٔ جداست؛ فاز ۲ |
| `ANN` (type-hint) | ۱٬۲۵۹ | mypy/pyright این کار را بهتر می‌کند |
| `PLR2004` (magic value) | ۹۴۴ | بیشترش در تست‌ها و معادلاتِ علمی (`engine/`) — نویز |
| `PLC0415` (import تنبل) | ۹۸۸ | الگوی رایج و بی‌ضرر این کدبیس (import داخل تابع برای شکستنِ وابستگی دوری) |
| `COM` | ۸۶۵ | با `ruff format` تضادِ رسمی دارد |
| `TRY003` + `EM101/EM102` | **۷۲۰** (۳۶۰+۳۰۹+۵۱) | پیامِ خطای فارسیِ inline الگوی عمدیِ پروژه است |

**شاهدِ خام:** `audit/evidence/ruff-recommended-findings.txt` (۴۳۰ ردیف `file:line: RULE`)،
`ruff-recommended-stats.txt` (۵۲ قاعده با شمارش)، `ruff-all-rules.txt` (۱۰۸ قاعده)،
`ruff-all-families.txt` (تجمیع بر پایهٔ خانواده)، و پیکربندی `audit/ruff-recommended.toml`.


---

## ۴) پنج یافتهٔ جدید این دور (F‑25 … F‑29)

این سه مورد در گزارش اصلی نبودند، چون پاس ورودی خصمانهٔ نخست (T‑33) با توکن باطل‌شده اجرا شده بود
و عملاً چیزی نمی‌سنجید؛ بازاجرای معتبر (T‑34) آن‌ها را آشکار کرد.
**F‑28 و F‑29** از راه دیگری پیدا شدند: روشن‌کردنِ قواعد ruff که پروژه امروز خاموش نگه داشته است (T‑50 در §۳).

### ۴‑۱) F‑25 · گارد شناسه **کف** ندارد: ۱۲ endpoint با شناسهٔ منفی/صفر/INT64_MIN پاسخ `200` می‌دهند (Medium)

**فرضیهٔ مهندسی:** شناسهٔ رکوردی که نمی‌تواند وجود داشته باشد (`-1`, `0`, `-0`, INT64_MIN) باید
`4xx` بگیرد، نه «پاسخ موفقِ تهی».

**مشاهدهٔ زنده (شاهد حداقلی، با توکن admin زنده، روی سرور S3 در `:8010`):**

```console
$ curl -s -o- -w '  -> %{http_code}\n' -H "Authorization: Bearer $TOK" \
      http://127.0.0.1:8010/api/v1/assessments/member/-1
[]  -> 200
$ … /assessments/member/0                      []  -> 200
$ … /assessments/member/-0                     []  -> 200
$ … /assessments/member/-9223372036854775808   []  -> 200
$ … /assessments/member/99999999999999999999999
   {"error":{"code":"invalid_id","message":"شناسهٔ مسیر خارج از بازهٔ مجاز است."}}  -> 422   ✅ گارد سقف کار می‌کند
$ … /assessments/member/abc
   {"error":{"code":"validation_error", …}}  -> 422                                          ✅ مبدل int
```

**اندازهٔ مسئله:** ۴۸ سلول = **۱۲ مسیر × ۴ مقدار** (§۳‑۴). فهرست کامل ۱۲ مسیر در همان بخش.

**بدنهٔ واقعیِ آن `200`ها (سه الگو):**

| الگو | نمونهٔ بازگردانده |
|---|---|
| آرایهٔ تهی | `[]` (برای `assessments/member/-1`, `axis-assessments/member/-1`, `members/-1/memberships`, `notifications/member/-1`, `nutrition/plans/member/-1`, `programs/member/-1`) |
| گزارشِ ساخته‌شده با **بازتاب شناسهٔ نامعتبر** | `{"member_id":-1,"measurements":[],"trend":null,"interpretation":{"status":"insufficient","headline":"برای تفسیر روند حداقل دو اندازه‌گیری لازم است", …}}` |
| گزارشِ صفر‌شدهٔ تغذیه | `{"member_id":-1,"date":"2026-11-21","items":[],"totals":{"kcal":0.0,"protein_g":0.0,"carbs_g":0.0,"fat_g":0.0}, …}` |
| صفحهٔ HTML درگاه | `<!doctype html>… «پرداخت یافت نشد»` (برای `payments/{id}/gateway-return` ⇒ F‑14) |

**زنجیرهٔ علّی (لایه‌به‌لایه، با `file:line`):**

1. `app/deps.py:39` → `PathId = Annotated[int, Path(ge=1, le=MAX_SAFE_ID)]` تعریف شده ولی
   **در هیچ امضای روتری استفاده نمی‌شود** (اسکن T‑23: صفر کاربرد، ۵۵ پارامتر `int` بدون گارد).
2. تیم به‌جای آن `app/id_guard.py` را به‌صورت middleware نوشته — تصمیمی **آگاهانه و مستند**
   («نیاز به تغییر ۴۱ امضا دارد»).
3. `app/id_guard.py:47-52` → `_too_big(segment)` با
   `if not segment.isdigit() or not segment.isascii(): return False` شروع می‌شود.
   در پایتون `"-1".isdigit() == False` و `"-9223372036854775808".isdigit() == False`
   ⇒ **هر مقدار منفی بدون بررسی رد می‌شود**.
4. همان تابع فقط **سقف** می‌سنجد (`len(segment) > 16 or int(segment) > MAX_SAFE_ID`) ⇒
   `"0"` هم رد می‌شود چون از سقف کمتر است. **هیچ‌جا `>= 1` بررسی نمی‌شود.**
5. در لایهٔ سرویس، این ۱۲ مسیر الگوی «فهرست با فیلتر `member_id`» دارند
   (`select(...).where(member_id == -1)`) ⇒ نتیجهٔ تهی ⇒ **`200 []`**.
   در مقابل، مسیرهای «دریافت با شناسه» (`db.get(Model, id)`) ⇒ `None` ⇒ **`404 not_found`**
   (۳۶ سلول به‌ازای هر مقدار منفی). یعنی **رفتار ناهمگون بین دو دسته مسیر**.

**چرا این «نقص» است و نه «طراحی»:**

* کلاینت نمی‌تواند «عضو وجود ندارد» را از «این عضو داده‌ای ندارد» تشخیص دهد ⇒ یک شناسهٔ غلط
  (off‑by‑one، عضو حذف‌شده، باگ کلاینت) به‌جای خطا، **گزارش تهیِ معتبر** رندر می‌کند.
* `member_id: -1` در بدنه **بازتاب** می‌شود ⇒ اگر کلاینت آن را ذخیره/ارسال کند، مقدار نامعتبر
  در گردش می‌ماند.
* `-9223372036854775808` در JSON بازتاب می‌شود ولی در `double` جاوااسکریپت/دارت **دقیقاً
  قابل نمایش نیست** ⇒ رفت‌وبرگشت آن در کلاینت فاسد می‌شود (همان دلیلی که خودِ پروژه
  `MAX_SAFE_ID = 2^53−1` را انتخاب کرده است).
* ناهمگونی با `PathId` که `ge=1` دارد: یعنی **قاعدهٔ اعلام‌شدهٔ پروژه با قاعدهٔ اجراشده یکی نیست**.

**چه چیزی سالم است (و نباید اغراق شود):**
با نقش `member` روی همان مسیرهای member‑scoped: **۰ × 200** (۴۰۳×۱۲ · ۴۲۲×۳۵ · ۴۰۴×۱۳)
⇒ `ensure_member_scope` درست کار می‌کند و **هیچ نشت دادهٔ بین‌عضوی رخ نداد**.
پس این یافته **نفوذ نیست**؛ نقصِ درستی/استحکام است (به همین دلیل Medium نه High).

**رفع:**
1. در `_too_big` کف اضافه شود — الگوی دقیق:
   ```python
   def _bad_id(segment: str) -> bool:
       s = segment.strip()
       if not s or s[0] in "+-" or not s.lstrip("+-").isdigit() or not s.isascii():
           return False                     # غیرعدد ⇒ به مبدل int واگذار شود
       try:
           v = int(s)
       except ValueError:
           return False
       return v < 1 or v > MAX_SAFE_ID      # ← کف و سقف با هم
   ```
   (دقت: `s[0] in "+-"` ⇒ مقادیر منفی **به مبدل int می‌رسند** و آن‌جا `422 validation_error` می‌گیرند؛
   اگر بخواهیم همهٔ مقادیر غیرمجزا `invalid_id` یکدست بگیرند، باید `v < 1` را قبل از آن بررسی کرد.)
2. بهتر و کم‌هزینه‌تر: همان `PathId` را در ۵۵ امضا اعمال کن (کاری که docstring از آن پرهیز کرد) —
   چون middleware **نمی‌تواند** بدنهٔ JSON را ببیند و خودِ docstring هم این را «بدهی باقی‌مانده» نامیده.
3. آزمون قرارداد: برای **هر** مسیر پارامتردار، چهار مقدار `-1`, `0`, `-0`, INT64_MIN باید `4xx` بدهند
   (اسکریپت آماده: `audit/probe_invalid_authed.py`؛ در CI به یک آزمون تبدیل شود).
4. در پاسخ‌های «داده‌ای نیست» شناسهٔ ورودی بازتاب نشود، یا اگر می‌شود، فقط پس از اعتبارسنجی.

**شاهد پذیرش:** اجرای `probe_invalid_authed.py` ⇒ `unexpected_2xx_on_bad_id == 0`
و `id_guard_rejections == ۴ × (تعداد مسیرهای پارامتردار)`.

### ۴‑۲) F‑26 · دو شکلِ متفاوت برای پاکت خطا: `{"error":…}` در برابر `{"detail":…}` (Medium)

**مشاهده (۷۲۲ سلول ≥۴۰۰ در پاس معتبر):**

| status | پاکت پروژه (فارسی، `error.code/message/details`) | پاکت پیش‌فرض FastAPI/Starlette (انگلیسی، `detail`) |
|---|---|---|
| ۴۰۰ | ۲۴ | ۰ |
| ۴۰۳ | ۳۴ | ۰ |
| **۴۰۴** | **۱۵۰** | **۷۰** |
| ۴۰۵ | ۰ | **۱** (شاهد تازه: `GET /api/v1/expenses/-1` ⇒ `{"detail":"Method Not Allowed"}`) |
| ۴۰۹ | ۸ | ۰ |
| ۴۲۲ | ۵۳۱ | ۰ |

**ریشه:** خطاهایی که **سرویس** می‌سازد (`NotFoundError`, `ForbiddenError`, …) از هندلرهای
`app/unhandled.py`/`app/errors.py` عبور می‌کنند و پاکت پروژه را می‌گیرند؛ اما خطاهایی که
**مسیریابی** می‌سازد (هیچ route‌ای مطابقت نکرد ⇒ `404 {"detail":"Not Found"}`،
متد مطابقت نکرد ⇒ `405`) هرگز به آن هندلرها نمی‌رسند.

**پیامد واقعی:**
* کلاینت باید **دو** شکل خطا را پارس کند؛ استودیو و کلاینت دارت امروز فقط `error.code` را می‌خوانند
  ⇒ در آن ۷۰ سلول، پیام خامِ انگلیسیِ `Not Found` به کاربر نشان داده می‌شود (یا `undefined`).
* آزمون‌هایی که «یکدستی پاکت» را assert می‌کنند فقط خطاهای سرویس را پوشش می‌دهند ⇒ **احساس اطمینان کاذب**.
* تزریق `%2e%2e%2f%2e%2e%2fetc%2fpasswd` (۷۰ سلول) دقیقاً همین شکل پیش‌فرض را گرفت ⇒
  همان مسیرهایی که یک اسکنر امنیتی می‌زند، پاسخ ناهمگون می‌دهند.

**رفع:** یک هندلر برای `StarletteHTTPException` (و `RequestValidationError` که امروز درست است) ثبت شود
که `404`/`405`/`406`/`415`/`501` را به پاکت پروژه نگاشت کند؛ به‌علاوهٔ یک آزمون که
برای هر مسیرِ موجود، یک مسیرِ **ناموجود** و یک **متد ناموجود** را صدا بزند و شکل پاکت را assert کند.

**شاهد پذیرش:** در خروجی `probe_invalid_authed.py` ⇒ `fastapi_default_detail == 0`.

### ۴‑۳) F‑27 · پیش‌نیازِ «پروندهٔ عضو» در سبد خرید با `404 not_found` بیان می‌شود؛ سفارش‌گذاری توسط کارکنان ممکن نیست (Medium)

**مشاهده:** در پاس seed (T‑31) دو نوشتن شکست خورد:

| عملیات | status | بدنه |
|---|---|---|
| `POST /api/v1/shop/cart` | **۴۰۴** | `{"code":"not_found","message":"پروندهٔ عضو یافت نشد — ابتدا پروفایل را کامل کنید"}` |
| `POST /api/v1/shop/checkout` | **۴۰۴** | همان |

**ریشهٔ کدی:** `modules/shop/service.py:293-298`

```python
def _own_member(db: Session, user: User) -> Member:
    m = db.scalar(select(Member).where(Member.user_id == user.id))
    if m is None:
        raise NotFoundError("پروندهٔ عضو یافت نشد — ابتدا پروفایل را کامل کنید")
    return m
```

**دو مسئلهٔ جدا در یک تابع:**

1. **معنای HTTP غلط.** «فراخوان پروندهٔ عضو ندارد» یک **پیش‌نیازِ شکست‌خورده** است، نه «منبع یافت نشد».
   `404` به کلاینت می‌گوید «چنین چیزی وجود ندارد» ⇒ کلاینت معمولاً پیام «یافت نشد» نشان می‌دهد یا
   تلاش مجدد می‌کند، در حالی که پیام درست «ابتدا پروفایل را کامل کنید» است. کدِ خطا هم `not_found`
   عمومی است، نه یک کد اختصاصی مثل `member_profile_required` که UI بتواند بر اساس آن
   کاربر را به صفحهٔ تکمیل پروفایل ببرد.
2. **شکاف کارکردی: سفارش به‌نیابت ممکن نیست.** چون `_own_member` عضویت را از `user.id`
   **فراخوان** می‌گیرد، کاربر کارکنان (reception/admin) که پروندهٔ عضو ندارد **نمی‌تواند** برای یک عضو
   سبد ببندد یا تسویه کند. در حالی که نقش `reception` در قرارداد برای مسیرهای shop listed است و
   UI استودیو صفحهٔ سفارش‌ها را دارد ⇒ باید تصمیم مالک ثبت شود: یا «سفارش به‌نیابت» با
   `member_id` صریح پشتیبانی شود، یا این محدودیت در سند محصول صریح نوشته شود.

**رفتار وابسته به پیکربندی (T‑48):** روی سرور S3 که **بدون** override اجرا شد
(`MP_SHOP_ONLINE_PURCHASE_ENABLED` پیش‌فرض `False`)، همان مسیرها `409 shop_online_closed` می‌دهند
(۸ سلول). یعنی رفتار shop به **دو** پیکربندی مستقل وابسته است و پیام خطای هر کدام متفاوت —
که برای پشتیبانی، تشخیص علت را سخت می‌کند.

**رفع:**
1. `NotFoundError` ⟶ یک خطای اختصاصی با کد `member_profile_required` و status **۴۰۹** (یا ۴۲۲).
2. اگر سفارش به‌نیابت مطلوب است: `_own_member` را به `_member_for(user, explicit_member_id=None)`
   تبدیل کن و مجوز `shop.order_on_behalf` را با casbin تعریف کن.
3. در `deploy_gate.py` یک بررسی: اگر `shop_online_purchase_enabled=False` است، UI نباید دکمهٔ خرید فعال نشان دهد
   (امروز دکمه هست و کاربر `409` می‌گیرد).
4. مستندسازی در `PROJECT-HANDOFF.md`: «مسیرهای سبد خرید به پروندهٔ عضوِ خودِ فراخوان نیاز دارند».

**شاهد پذیرش:** `POST /shop/cart` با هویت بدون پروندهٔ عضو ⇒ **۴۰۹ با `code=member_profile_required`**
(نه `404 not_found`)؛ و آزمون جدید برای سفارش به‌نیابت (اگر پذیرفته شود).


### ۴‑۴) F‑28 · «امروز» در دو ماژول با ساعتِ UTC حساب می‌شود در حالی که shop از `Asia/Tehran` استفاده می‌کند (Medium)

**ابزار کاشف:** ruff 0.17.6، قاعدهٔ `DTZ011` از خانوادهٔ `flake8-datetimez` — که در `pyproject.toml`
پروژه **روشن نیست**. این یک باگِ منطقی است، نه یک ایرادِ سبکی.

| محل | کد | چه چیزی را «امروز» می‌گیرد |
| --- | --- | --- |
| `modules/axis_assessment/service.py:31` | `today = date.today()` | **سنِ عضو** در ارزیابی محور‌ها |
| `modules/nutrition/service.py:124` | `day = entry.get("logged_for_date") or date.today().isoformat()` | روزِ پیش‌فرض **ثبت غذایی** |
| `modules/nutrition/service.py:182` | `day = day or date.today().isoformat()` | روزِ پیش‌فرض ثبت غذایی (شاخهٔ دوم) |
| `modules/shop/service.py:61-62` | `zone = ZoneInfo(settings.shop_timezone)` / `moment = (now or datetime.now(UTC)).astimezone(zone)` | **درست** — الگوی مرجع داخل همان پروژه |
| `app/config.py:67,91-99` | `shop_timezone: str = "Asia/Tehran"` + اعتبارسنج با `ZoneInfo` | **درست** — تنظیم و اعتبارسنجی موجود است |

**چرا خطاست (محاسبه):** ایران UTC+3:30 است. `date.today()` از ساعتِ **محلیِ فرایند** استفاده می‌کند و
در کانتینرها آن ساعت معمولاً UTC است. شاهد:

| شاهد | نتیجه |
| --- | --- |
| `grep -n "TZ\|timezone\|tzdata"` روی `mp-app/infra/Dockerfile.backend`، `infra/docker-compose.yml`، `backend/Dockerfile`، `infra/ansible/` | **۰ مورد** ⇒ TZ کانتینر = UTC |
| `grep -rn "datetime.now()"` در `modules app engine jobs` | بقیه همه `datetime.now(UTC)`‌اند؛ فقط همین ۳ محل `date.today()` بی‌منطقه‌اند |
| بازهٔ خرابی در تهران | هر شب از **۰۰:۰۰ تا ۰۳:۳۰** به وقت محلی، «امروز» در nutrition و axis_assessment **دیروزِ UTC** است |

**تأثیر کاربری (نه فنی):** در آن سه‌ونیم ساعت، ثبت غذاییِ بدون `logged_for_date` روی **تاریخ دیروز** می‌نشیند
(تقویرِ کالری/وزن یک روز جابه‌جا می‌شود) و سنِ عضو در ارزیابی محور‌ها **دیرتر از موعد** یک سال بالا می‌رود —
یعنی اگر تولدش همان روز باشد، تا سه‌ونیم ساعت بعد از نیمه‌شب تهران ارزیابی با سنِ سالِ قبل انجام می‌شود.
همزمان `shop` با منطقهٔ زمانیِ درست کار می‌کند ⇒ **سه برداشتِ متفاوت از «امروز» در یک محصول.**

**اثباتِ مرز (اجرای واقعی در همین جلسه):**

```console
$ python3 - <<'PY'
from zoneinfo import ZoneInfo
from datetime import datetime, UTC
now = datetime(2026, 11, 21, 22, 0, tzinfo=UTC)          # ۰۱:۳۰ بامداد ۲۲ آبان در تهران
print("UTC    :", now.date())
print("Tehran :", now.astimezone(ZoneInfo("Asia/Tehran")).date())
PY
UTC    : 2026-11-21        # چیزی که date.today() در کانتینر می‌دهد ⇒ غلط
Tehran : 2026-11-22        # چیزی که کاربر و ماژول shop انتظار دارند
```

الگوی اصلاح، بدون تغییرِ API عمومی:

```python
from datetime import UTC, date, datetime
from zoneinfo import ZoneInfo
from app.config import settings

def _today_in_shop_zone() -> date:
    return datetime.now(UTC).astimezone(ZoneInfo(settings.shop_timezone)).date()
```

**درگاه پذیرش:** `grep -rn "date.today()" modules app engine jobs` ⇒ ۰ مورد، به‌علاوهٔ یک تستِ مرزی که
با `TZ=UTC` و ساعت ۲۲:۰۰ UTC، روزِ ثبت غذایی را `2026-11-22` انتظار داشته باشد.

---

### ۴‑۵) F‑29 · `app/sms.py`: شش `logging.error` داخل `except` بدون traceback، سه `urlopen` با schemes باز، و ۳۹ `# noqa` بلااثر (Low‑Medium)

**ابزار کاشف:** ruff، قواعد `TRY400`، `S310`، `RUF100` — هر سه در پیکربندی فعلی پروژه خاموش‌اند.

**(الف) traceback دور ریخته می‌شود.** `TRY400` شش مورد در **یک فایل** داد:

```console
app/sms.py:66:13: TRY400 Use `logging.exception` instead of `logging.error`
app/sms.py:69:13 / 72:13 / 99:13 / 102:13 / 105:13  — همان پیام
```

`logging.error()` داخل بلاک `except` **فقط پیام** را ثبت می‌کند و زنجیرهٔ فراخوانی را دور می‌ریزد؛
`logging.exception()` همان پیام را **به‌همراه traceback** می‌نویسد. نتیجه: هرگاه فراهم‌کنندهٔ SMS خطا دهد،
در لاگ‌ها «ارسال ناموفق» دیده می‌شود ولی **ریشه (کد خطای HTTP، timeout، DNS، بدنهٔ پاسخ)** نیست —
دقیقاً همان چیزی که برای تفکیکِ «باگِ ما» از «قطعیِ فراهم‌کننده» لازم است. این مورد با **F‑03**
(رندرِ `rich` روی حلقهٔ رویداد) ترکیب می‌شود: SMS پرخطاترین مسیرِ خروجیِ شبکه است و کم‌لاگ‌ترین.

**(ب) schemes باز.** `S310` شش مورد: `app/sms.py:52,61,94` و `eval/llm_column.py:59,100,107`.
`urllib.request.urlopen` به‌طور پیش‌فرض `file://` و `ftp://` را هم می‌پذیرد؛ اگر host از یک setting بیاید
(`sms_provider_url`)، مقدارِ دست‌کاری‌شده می‌تواند به خواندن فایل محلی بینجامد. شدتِ عملی **کم** است
چون مقدار از محیط خوانده می‌شود نه از ورودی کاربر؛ ولی یک allowlist از schemes یا یک `# noqa: S310` مستند
هزینهٔ صفر دارد.

**(ج) `# noqa`های مرده — و یک تصحیحِ مهم بر F‑22.** `RUF100` در پیکربندی پیشنهادی **۳۹ مورد** داد
(۴ موردش در migration) و خودش دلیل را می‌گوید:

```console
db/migrations/versions/c3f01ab129e2_…py:67:68: RUF100 [*] Unused `noqa` directive (non-enabled: `S608`)
db/migrations/versions/c3f01ab129e2_…py:165:52 / :169:67 / :171:71  — همان پیام
```

**تصحیح بر F‑22:** در گزارش اصلی نوشتم آن ۴ خط «SQL با f-string» هستند و `# noqa: S608` دارند.
آزمونِ مستقیم نشان داد **ruff حتی با `--ignore-noqa` هم روی این خطوط `S608` نمی‌دهد**:

```console
$ ruff check --no-cache --select S608 --ignore-noqa .
All checks passed!
```

یعنی (۱) آن `# noqa`ها امروز **هیچ اثری ندارند** (چون خانوادهٔ `S` خاموش است — همان چیزی که `RUF100` می‌گوید)
و (۲) `S608` روی `op.execute(f"DROP INDEX IF EXISTS ix_{table}_updated_at")` fire نمی‌شود، چون ruff آن را
SQLِ قابل‌تزریقِ «کامل» تشخیص نمی‌دهد (فقط `DROP INDEX` است، نه `SELECT/INSERT` با شرط).
**نتیجهٔ روش‌شناختی:** F‑22 را **فقط قاعدهٔ اختصاصیِ semgrep** در `audit/semgrep-mp.yml` می‌گیرد، نه ruff —
پس برای آن مورد، ruff جایگزینِ semgrep نیست و هر دو باید در CI بمانند. شدتِ واقعیِ F‑22 هم پایین‌تر از چیزی است
که عنوان «SQL با f-string» القا می‌کند: متغیرها از `sa.inspect()` می‌آیند نه از ورودی کاربر.

| شاهد | نتیجه |
| --- | --- |
| `ruff check --select TRY400` | ۶ مورد، همه در `app/sms.py` |
| `ruff check --select S310` | ۶ مورد (`app/sms.py` ×۳، `eval/llm_column.py` ×۳) |
| `ruff check --select RUF100` | **۳۹** `# noqa` بلااثر (۴ موردش `S608` در migration) |
| `ruff check --select S608 --ignore-noqa` | **۰** مورد ⇒ F‑22 با ruff قابل‌کشف نیست |
| `ruff check --select S110,S112` | `api/v1/monitoring.py:24` (S110) + `scripts/dast.py:81,176,187` (S112) — هم‌پوشانی با F‑17 |
| `ruff check --select S105,S106` | `app/config.py:16:22` «رمز سخت‌کدشدهٔ `DEFAULT_DEV_SECRET`» — مؤیدِ ریشهٔ **F‑02** |
| `ruff check --select SLF001` | `modules/auth/router.py:55:30` دسترسی به `limiter._storage` — مؤیدِ **F‑13** |
| `ruff check --select C901` | ۱۵ تابع >۱۰؛ بالاترین `app/config.py:128 validate_production_configuration` **(۲۸)** — همان **F‑15** با radon F(47) |
| `ruff check --select PLW0603` | ۷ `global` در `app/logging.py`، `app/observability.py`، `app/profiling.py` — سطحِ تماس F‑03 |

**شاهدِ خام:** `audit/evidence/ruff-recommended-findings.txt` (۴۳۰ ردیف با مسیرهای نسبی)
+ `ruff-recommended-stats.txt` (۵۲ قاعده) + `ruff-all-rules.txt` (۱۰۸ قاعده با `--select ALL` = ۱۱٬۷۷۸ مورد)
+ `ruff-all-families.txt` (تجمیع بر پایهٔ خانواده) + پیکربندی `audit/ruff-recommended.toml`.

---

---

## ۵) تصحیحاتِ وارد‌شده بر گزارش اصلی (شفاف و کامل)

این جدول دلیل وجودِ این پرونده است: اعداد باید از **فایل شاهد** بیایند، نه از حافظهٔ جلسه.
هر ردیف یک اختلاف واقعی بود که پیدا و اصلاح شد.

| # | محل در گزارش اصلی | مقدار قبلی | مقدارِ راستی‌آزمایی‌شده | منبع اختلاف |
|---|---|---|---|---|
| ۱ | §۱۴‑۱ | «۶۰۱ سلول مخالف قرارداد» | **۶۰۲** (۶۰۱ با نقش نام‌دار + ۱ با principal ناشناس) | شمارش دستی در برابر استخراج از `contract-matrix-raw.json` |
| ۲ | §۵ F‑14 | «`gateway-return` با `-1` → ۲۰۰» | **۴ مقدار** (`-1`, `0`, `-0`, INT64_MIN) × **۱۲ مسیر** = ۴۸ سلول ⇒ F‑25 | پاس نخست با توکن باطل اجرا شده بود |
| ۳ | §۸ مورد ۹ | «سقف شناسه‌ها کار می‌کند (تأیید DAST ‏M60/R18)» | **فقط سقف** کار می‌کند (۷۰ × ۴۲۲)؛ **کف وجود ندارد** (۴۸ × ۲۰۰) | `app/id_guard.py:47-52` و `isdigit()` |
| ۴ | §۷ F‑15 | «بدترین radon: `next_transfer_state` ‏E(34)» | دو تابع با درجهٔ **F**: `app/config.py:128` ‏**F(47)** و `engine/axis_prescription.py:43` ‏**F(46)**؛ سپس `next_transfer_state` ‏E(34) | پارس نشدن خروجی radon در دور قبل |
| ۵ | §۱۴‑۷ | «۱۴ خانوادهٔ متریک» | **۱۲ خانواده** (۶ `mp_http_*` + ۶ `mp_outbox_*`) | شمارش دستی در برابر `awk` روی `metrics-noauth.txt` |
| ۶ | §۹ (جدول صداقت) | — | ردیف جدید: **پاس سوم `probe_contract.py` نادرست‌نتیجه بود** (۶۶۴ سلول `401` با توکن باطل‌شده) و با اسکریپت جدید بازاجرا شد | نقص روش‌شناختیِ خودم |
| ۷ | §۱۴‑۱ | فقط آمار ۱٬۱۴۱ سلول | آمار پاس معتبرِ **۸۷۲ سلول** اضافه شد | اجرای جدید |
| ۸ | §۱۲ (پیوست الف) | — | سه فایل شاهد جدید: `contract-invalid-authed.json`, `pathid-scan.json`, `probe_invalid_authed.py` | اجرای جدید |
| ۹ | §۱ جدول شدت‌ها | ۲۴ یافته | **۲۷ یافته** (F‑25 Medium, F‑26 Medium, F‑27 Medium) | یافته‌های جدید |
| ۱۰ | §۱۱ نقشهٔ رفع | ۲۲ ردیف | **۲۵ ردیف** (سه اقدام جدید با شاهد پذیرش) | یافته‌های جدید |
| **۱۱** | **§۵ F‑22 و §۴‑۵** | **«۴ خط SQL با f-string که `# noqa: S608` دارند»** | **ruff `S608` روی این ۴ خط fire نمی‌شود — حتی با `--ignore-noqa` ⇒ «All checks passed!». آن `# noqa`ها امروز بلااثرند (`RUF100` ×۴). F‑22 را فقط قاعدهٔ اختصاصیِ semgrep می‌گیرد** | **اجرای مستقیم `ruff check --select S608 --ignore-noqa` در T‑50** |
| **۱۲** | **§۱ جدول شدت‌ها** | **۲۷ یافته** | **۲۹ یافته** (F‑28 Medium: `date.today()` با UTC در برابر `Asia/Tehran`؛ F‑29 Low‑Med: `logging.error` بدون traceback در `app/sms.py`) | یافته‌های جدید از T‑50 |
| **۱۳** | **§۱۲ پیوست الف** | **۵۵ فایل شاهد** | **۶۰ فایل شاهد** (۴ خروجی ruff + ۱ پیکربندی پیشنهادی) | اجرای جدید |

**چیزی که تغییر نکرد** (و دوباره تأیید شد): صفر drift قرارداد، صفر `5xx` در **هر دو** ماتریس
(۱٬۱۴۱ + ۸۷۲ سلول)، صفر نشت stack trace، سالم بودن JWT/OTP/idempotency، نبودِ `dangerouslySetInnerHTML`،
پاک بودن `pip-audit` روی وابستگی‌های محصول، و دست‌نخورده بودن مخزن `MP`.

---

## ۶) فهرست شواهد با hash — برای بازآزماییِ مستقل

هر فایل شاهد در مخزن commit شده است. ستون «لینک مستقیم» همان فایل روی GitHub است
(شاخهٔ `arena/2cde32d6-chat2db`). اگر hash فایلی با آنچه در جدول زیر است تفاوت داشت،
یعنی فایل دست‌کاری شده یا نسخهٔ دیگری اجرا شده است.

| فایل | اندازه (بایت) | SHA‑256 (۱۶ رقم نخست) |
|---|---|---|
| `audit/.gitignore` | 19 | `862263fa1f46c20f…` |
| `audit/bench_logging.py` | 3,951 | `3eaec1b8b785987a…` |
| `audit/eslint-studio.flat.mjs` | 633 | `613bd388f35229e6…` |
| `audit/evidence/backend-coverage.xml` | 426,890 | `4bee93f485ddd96c…` |
| `audit/evidence/bandit.json` | 88,436 | `e8873e4e62be0a0f…` |
| `audit/evidence/contract-diff.json` | 661 | `007efc700ea858a2…` |
| `audit/evidence/contract-invalid-authed.json` | 477,652 | `83f99bcd8cd7608b…` |
| `audit/evidence/contract-invalid-findings.json` | 227 | `8ec588731b3e813e…` |
| `audit/evidence/contract-matrix-raw.json` | 850,104 | `3d58413631bd741f…` |
| `audit/evidence/contract-rbac-findings.json` | 73,763 | `7a1615c7a80490bc…` |
| `audit/evidence/detect-secrets.err` | 0 | `e3b0c44298fc1c14…` |
| `audit/evidence/detect-secrets.json` | 51,599 | `c81a5c71ed768029…` |
| `audit/evidence/eslint-stderr.txt` | 0 | `e3b0c44298fc1c14…` |
| `audit/evidence/eslint-studio.json` | 227,239 | `f4bc1e42425fae5c…` |
| `audit/evidence/jscpd-out/jscpd-report.json` | 13,131 | `b24d9fafa1c9a5f8…` |
| `audit/evidence/knip-err.txt` | 1,132 | `39bd484355b70f7d…` |
| `audit/evidence/knip-studio.json` | 0 | `e3b0c44298fc1c14…` |
| `audit/evidence/live-security-raw.json` | 17,051 | `5fee5dc9e6712414…` |
| `audit/evidence/live-security-verdicts.json` | 4,678 | `e469e8204e6943ab…` |
| `audit/evidence/lizard-warnings.txt` | 6,316 | `60a06161a1227e87…` |
| `audit/evidence/lizard.txt` | 85,468 | `ea8036705318f2bc…` |
| `audit/evidence/load-plain-dev.json` | 2,196 | `8cfe7d99c701c551…` |
| `audit/evidence/logging-cost.json` | 1,933 | `5aa00c80012a0554…` |
| `audit/evidence/metrics-noauth.txt` | 6,529 | `5e91cabc0603eb7f…` |
| `audit/evidence/mutmut-manual-transfer-policy.json` | 4,444 | `8e342556a3dc07ef…` |
| `audit/evidence/mutmut-verified.json` | 9,751 | `f2efa6755909765f…` |
| `audit/evidence/openapi-live.json` | 171,395 | `b6154d165d910be0…` |
| `audit/evidence/otp-bruteforce.json` | 213 | `4578fbefd881fe19…` |
| `audit/evidence/otp-ratelimit-verdicts.json` | 1,960 | `bb4367a3ce256c36…` |
| `audit/evidence/pathid-scan.json` | 6,485 | `786af49a7e77d4e6…` |
| `audit/evidence/pool-events.jsonl` | 23,476 | `f6ddcb801ee235d5…` |
| `audit/evidence/radon-cc.txt` | 2,283 | `40dd187d192ab682…` |
| `audit/evidence/radon-mi.txt` | 8,513 | `a7b72e7fd226eeb8…` |
| `audit/evidence/rbac-systemerror-repro.json` | 3,240 | `4fd047831fcce31b…` |
| `audit/evidence/ruff-all-families.txt` | 501 | `76f308417919b4bc…` |
| `audit/evidence/ruff-all-rules.txt` | 4,857 | `cf6019cda5a780d0…` |
| `audit/evidence/ruff-recommended-findings.txt` | 42,414 | `693ab7332acb8ac6…` |
| `audit/evidence/ruff-recommended-stats.txt` | 2,153 | `2e3ee2e813ba0c55…` |
| `audit/evidence/semgrep-backend.json` | 18,984 | `9dbfae3187f91bb1…` |
| `audit/evidence/semgrep-client.json` | 3,428 | `f01227ccc53d73a9…` |
| `audit/evidence/semgrep-studio.json` | 6,573 | `453fe65667f5e7b6…` |
| `audit/evidence/semgrep-summary.txt` | 2,891 | `0256bb78099c0ffa…` |
| `audit/evidence/studio-buttons-wiring.json` | 4,120 | `2a2471ca2049a7a1…` |
| `audit/evidence/studio-dead-exports.json` | 351 | `10d3269172162426…` |
| `audit/evidence/studio-ui-wiring.json` | 3,349 | `83098cbeef9940da…` |
| `audit/evidence/vulture.txt` | 74 | `e2ad653f7ae18595…` |
| `audit/evidence/xff-dockerfile-cmd.json` | 462 | `20220d5e4f5eba62…` |
| `audit/harness_common.py` | 7,825 | `9204e48d0a8e168d…` |
| `audit/probe_concurrency.py` | 9,709 | `26762cc833f5008a…` |
| `audit/probe_contract.py` | 25,534 | `b93b37548097d46d…` |
| `audit/probe_invalid_authed.py` | 10,772 | `edd3c25cd06a53d8…` |
| `audit/probe_live_security.py` | 16,650 | `0b7326b2b10aacf7…` |
| `audit/probe_load.py` | 7,721 | `940089b867e6446e…` |
| `audit/probe_otp_limits.py` | 6,356 | `662906b965d4801e…` |
| `audit/repro_rbac_systemerror.py` | 4,829 | `4d0cfbe573652b38…` |
| `audit/ruff-recommended.toml` | 4,564 | `fea43dd72bb10be8…` |
| `audit/scan_ui_wiring.py` | 7,088 | `64e64c20bfe2b1f5…` |
| `audit/semgrep-mp.yml` | 7,002 | `d58146b4f372ca82…` |
| `audit/serve_backend.py` | 10,139 | `fc1f4e3644718f19…` |
| `audit/serve_plain.py` | 2,073 | `fe6a735f3ce45fb5…` |
| `share/MP-AGENT-BRIEF.md` | 140,046 | `af8ef690c394ad92…` |
| `share/MP-BUILDER-ADDENDUM-2026-11-21.md` | 35,148 | `fc3b322d2f63b1f0…` |
| `share/MP-BUILDER-PROMPT-2026-11-21.md` | 40,447 | `9ffc5853019026d2…` |
| `share/MP-EVIDENCE-DOSSIER-2026-11-20.md` | 154,747 | `5c009419556867ec…` |
| `share/MP-FINAL-AUDIT-REPORT-2026-11-20.md` | 114,110 | `1f292decfd592051…` |
| `share/MP-PROBLEMS-2026-11-20.md` | 40,422 | `a2e7910817bac975…` |

**جمع: 55 فایلِ hash‌شده · 3,019,018 بایت** (به‌علاوهٔ خودِ این پرونده).

### ۶‑۱) لینک مستقیم هر فایل شاهد روی GitHub

پایهٔ آدرس:
`https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/2cde32d6-chat2db/`

| فایل | لینک مستقیم |
|---|---|
| `audit/.gitignore` | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/2cde32d6-chat2db/audit/.gitignore |
| `audit/bench_logging.py` | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/2cde32d6-chat2db/audit/bench_logging.py |
| `audit/eslint-studio.flat.mjs` | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/2cde32d6-chat2db/audit/eslint-studio.flat.mjs |
| `audit/evidence/backend-coverage.xml` | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/2cde32d6-chat2db/audit/evidence/backend-coverage.xml |
| `audit/evidence/bandit.json` | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/2cde32d6-chat2db/audit/evidence/bandit.json |
| `audit/evidence/contract-diff.json` | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/2cde32d6-chat2db/audit/evidence/contract-diff.json |
| `audit/evidence/contract-invalid-authed.json` | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/2cde32d6-chat2db/audit/evidence/contract-invalid-authed.json |
| `audit/evidence/contract-invalid-findings.json` | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/2cde32d6-chat2db/audit/evidence/contract-invalid-findings.json |
| `audit/evidence/contract-matrix-raw.json` | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/2cde32d6-chat2db/audit/evidence/contract-matrix-raw.json |
| `audit/evidence/contract-rbac-findings.json` | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/2cde32d6-chat2db/audit/evidence/contract-rbac-findings.json |
| `audit/evidence/detect-secrets.json` | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/2cde32d6-chat2db/audit/evidence/detect-secrets.json |
| `audit/evidence/eslint-studio.json` | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/2cde32d6-chat2db/audit/evidence/eslint-studio.json |
| `audit/evidence/jscpd-out/jscpd-report.json` | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/2cde32d6-chat2db/audit/evidence/jscpd-out/jscpd-report.json |
| `audit/evidence/knip-err.txt` | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/2cde32d6-chat2db/audit/evidence/knip-err.txt |
| `audit/evidence/live-security-raw.json` | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/2cde32d6-chat2db/audit/evidence/live-security-raw.json |
| `audit/evidence/live-security-verdicts.json` | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/2cde32d6-chat2db/audit/evidence/live-security-verdicts.json |
| `audit/evidence/lizard-warnings.txt` | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/2cde32d6-chat2db/audit/evidence/lizard-warnings.txt |
| `audit/evidence/lizard.txt` | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/2cde32d6-chat2db/audit/evidence/lizard.txt |
| `audit/evidence/load-plain-dev.json` | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/2cde32d6-chat2db/audit/evidence/load-plain-dev.json |
| `audit/evidence/logging-cost.json` | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/2cde32d6-chat2db/audit/evidence/logging-cost.json |
| `audit/evidence/metrics-noauth.txt` | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/2cde32d6-chat2db/audit/evidence/metrics-noauth.txt |
| `audit/evidence/mutmut-manual-transfer-policy.json` | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/2cde32d6-chat2db/audit/evidence/mutmut-manual-transfer-policy.json |
| `audit/evidence/mutmut-verified.json` | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/2cde32d6-chat2db/audit/evidence/mutmut-verified.json |
| `audit/evidence/openapi-live.json` | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/2cde32d6-chat2db/audit/evidence/openapi-live.json |
| `audit/evidence/otp-bruteforce.json` | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/2cde32d6-chat2db/audit/evidence/otp-bruteforce.json |
| `audit/evidence/otp-ratelimit-verdicts.json` | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/2cde32d6-chat2db/audit/evidence/otp-ratelimit-verdicts.json |
| `audit/evidence/pathid-scan.json` | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/2cde32d6-chat2db/audit/evidence/pathid-scan.json |
| `audit/evidence/pool-events.jsonl` | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/2cde32d6-chat2db/audit/evidence/pool-events.jsonl |
| `audit/evidence/radon-cc.txt` | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/2cde32d6-chat2db/audit/evidence/radon-cc.txt |
| `audit/evidence/radon-mi.txt` | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/2cde32d6-chat2db/audit/evidence/radon-mi.txt |
| `audit/evidence/rbac-systemerror-repro.json` | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/2cde32d6-chat2db/audit/evidence/rbac-systemerror-repro.json |
| `audit/evidence/semgrep-backend.json` | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/2cde32d6-chat2db/audit/evidence/semgrep-backend.json |
| `audit/evidence/semgrep-client.json` | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/2cde32d6-chat2db/audit/evidence/semgrep-client.json |
| `audit/evidence/semgrep-studio.json` | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/2cde32d6-chat2db/audit/evidence/semgrep-studio.json |
| `audit/evidence/semgrep-summary.txt` | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/2cde32d6-chat2db/audit/evidence/semgrep-summary.txt |
| `audit/evidence/studio-buttons-wiring.json` | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/2cde32d6-chat2db/audit/evidence/studio-buttons-wiring.json |
| `audit/evidence/studio-dead-exports.json` | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/2cde32d6-chat2db/audit/evidence/studio-dead-exports.json |
| `audit/evidence/studio-ui-wiring.json` | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/2cde32d6-chat2db/audit/evidence/studio-ui-wiring.json |
| `audit/evidence/vulture.txt` | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/2cde32d6-chat2db/audit/evidence/vulture.txt |
| `audit/evidence/xff-dockerfile-cmd.json` | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/2cde32d6-chat2db/audit/evidence/xff-dockerfile-cmd.json |
| `audit/harness_common.py` | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/2cde32d6-chat2db/audit/harness_common.py |
| `audit/probe_concurrency.py` | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/2cde32d6-chat2db/audit/probe_concurrency.py |
| `audit/probe_contract.py` | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/2cde32d6-chat2db/audit/probe_contract.py |
| `audit/probe_invalid_authed.py` | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/2cde32d6-chat2db/audit/probe_invalid_authed.py |
| `audit/probe_live_security.py` | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/2cde32d6-chat2db/audit/probe_live_security.py |
| `audit/probe_load.py` | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/2cde32d6-chat2db/audit/probe_load.py |
| `audit/probe_otp_limits.py` | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/2cde32d6-chat2db/audit/probe_otp_limits.py |
| `audit/repro_rbac_systemerror.py` | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/2cde32d6-chat2db/audit/repro_rbac_systemerror.py |
| `audit/scan_ui_wiring.py` | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/2cde32d6-chat2db/audit/scan_ui_wiring.py |
| `audit/semgrep-mp.yml` | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/2cde32d6-chat2db/audit/semgrep-mp.yml |
| `audit/serve_backend.py` | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/2cde32d6-chat2db/audit/serve_backend.py |
| `audit/serve_plain.py` | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/2cde32d6-chat2db/audit/serve_plain.py |
| `share/MP-AGENT-BRIEF.md` | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/2cde32d6-chat2db/share/MP-AGENT-BRIEF.md |
| `share/MP-FINAL-AUDIT-REPORT-2026-11-20.md` | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/2cde32d6-chat2db/share/MP-FINAL-AUDIT-REPORT-2026-11-20.md |
| `share/MP-PROBLEMS-2026-11-20.md` | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/2cde32d6-chat2db/share/MP-PROBLEMS-2026-11-20.md |
| `share/MP-EVIDENCE-DOSSIER-2026-11-20.md` | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/2cde32d6-chat2db/share/MP-EVIDENCE-DOSSIER-2026-11-20.md |

---

## ۷) منابع — هر چیزی که خوانده شد و دقیقاً چه چیزی از آن بیرون آمد

### ۷‑۱) منابع داخلی مخزن `MP` (با مسیر دقیق)

| منبع | شاخه/مسیر | چه چیزی از آن گرفته شد | در کدام یافته استفاده شد |
|---|---|---|---|
| `PROJECT-HANDOFF.md` | `arena/da474b65-mp` → `docs/architecture/repowise/` | جدول ۲۳ ماژول، ۱۴۱ مسیر/۱۶۳ عملیات، ۶۴ جدول ORM/۳۸ مهاجرت، همهٔ پیش‌فرض‌های محیطی، جریان‌های OTP/کوپن/پرداخت/کیف پول، نقش‌ها، §۱۳ کاستی‌ها | F‑02, F‑07, F‑12, F‑18 |
| `qa-report/FINAL-REPORT.md` | `arena/71d7d803-mp` | خط پایهٔ A1: ۱۰۱ دکمه/۴۵ کلیک‌شده/۰ خطا، چهار اجرای Locust با ۲۰۰ کلاینت، «run 2 = 0 requests (server locked)»، «QueuePool 40+20 filled»، «root cause NOT established» | F‑03, F‑04 (ریشهٔ همان علامت‌ها پیدا شد) |
| `qa-report/tools/seed_live.py` | همان | seed استاندارد: `KNOWN_PERMISSIONS`، admin با `09120000001`، ۲۵۰ عضو | همهٔ پراب‌های زنده |
| `evidence/m60/STATUS.md` | تاریخ ۲۰۲۶‑۱۱‑۱۶ | ادعاهای R3/R4/R5/R8/R18، «DAST ۱۰۲۴ درخواست/۱۲۸ عملیات/**۰ یافته**»، `deploy_gate.py` با ۹ بررسی، باگ `android:debuggable` | §۵ ردیف ۳ (ادعای R18 ناقص است — F‑25) |
| `finn/reports/findings-main-e5c8891.md` | — | ۵۸۲ فایل، health ۹٫۲۶/۱۰، بدترین `Shop.tsx` ‏۶٫۰، ۶۷۰ یافته، ۳۵ کد مرده، ۲۵ doc drift | F‑15, F‑20 (بررسی مستقل) |
| `finn/reports/findings-2026-11-20.md` | snapshot `b194e96` | گراف ۱٬۵۶۷ گره/۴٬۹۳۰ یال، ۴۲۱ صفحه wiki، بدترین `large_method`ها، «`UpdateService` بدون فراخوان» | F‑15, F‑20 |
| `api/routes.json` | HEAD `662ff88` | اوراکل قرارداد: ۱۶۳ عملیات، `guards`، `roles` | F‑12, F‑13, T‑32, T‑45 |
| `README` | — | اعداد «۱۲۱ مسیر/۱۳۷ عملیات» ⇒ **کهنه** (زنده: ۱۴۱/۱۶۳) | F‑07 (doc drift) |
| `mp-app/backend/Dockerfile:27` | — | `--proxy-headers --forwarded-allow-ips='*'` و `WEB_CONCURRENCY:-4` | **F‑01**, F‑18 |
| `mp-app/infra/Dockerfile.backend:29` | — | همان | **F‑01** |
| `mp-app/infra/Caddyfile:26,29,34` | — | `reverse_proxy` بدون `header_up X-Real-IP`/trust تنظیم‌شده | F‑01 (تناقض با مستندات) |
| `docs/MuscleParadise/DEPLOYMENT.md:43` | — | «خالی = `X-Forwarded-For` **هرگز** پذیرفته نمی‌شود» | F‑01 (گزاره در لایهٔ اپ درست، در استقرار نادرست) |
| `docs/MuscleParadise/OPS-RUNBOOK.md:15` | — | فهرست نام کلیدهای محیطی | §۳‑۲۲ (false positive ‏detect-secrets) |
| `finn/reports/m112-release-signing-hardening.md:38` | — | نام `MP_ANDROID_KEYSTORE_BASE64` | §۳‑۲۲ (false positive) |
| `.github/workflows/*.yml` | ۷ workflow | `ci.yml` شامل `docs_gate.py` → `interaction_map.py --check`، `mermaid-check`، `repo_hygiene_gate.py`؛ **`repowise_handoff.py --check` نیست**؛ `web.yml` فقط dispatch؛ همهٔ **۴۲** `uses:` با tag متحرک و **۰** SHA‑pin | F‑07, F‑10 (نبود lint در CI) |

### ۷‑۲) کد منبعی که خط‌به‌خط خوانده شد (نه grep)

| فایل | چرا خوانده شد |
|---|---|
| `app/deps.py` | `MAX_SAFE_ID:36`, `PathId:39`, `get_current_user:42-96` (پذیرش توکن بدون `ver`/`sid`)، `_guard:135` |
| `app/id_guard.py` | کل فایل (۶۵ خط) — ریشهٔ **F‑25** |
| `app/ids.py` | ارجاع به `le=MAX_SAFE_ID` |
| `app/main.py` | `init_db():21-25`, `configure_logging(json_logs=…):50`, `create_app:44` (۱۱۱ خط) |
| `app/config.py` | پیش‌فرض‌ها (`:25 environment`, `:65 shop_online…`, `:69 trusted_proxies`, `:79 CORS`) و `validate_production_configuration:127-…` |
| `app/unhandled.py` | `_unexpected:91` — همان‌جا که rich روی event loop رندر می‌شود (**F‑03**) |
| `app/logging.py` | ساختار structlog و انتخاب رندر |
| `app/security/proxy.py` | `client_ip:38-58` — منطق درستِ fail‑closed |
| `app/security/rbac.py` | `:230-290` — `_enforcer` تنبل بدون lock، `enforce:264`، نبودِ `enable_cache` (**F‑05**) |
| `db/base.py` | `_POOL_SIZE/_MAX_OVERFLOW/_POOL_TIMEOUT/_POOL_RECYCLE`, `pool_pre_ping`, pragmaها، `connect_args` (**F‑04**, F‑18) |
| `modules/auth/router.py` | `_rate_limit_key:28-38`, `storage_uri:46`, health با `limiter._storage.check():52`, دو سقف OTP `:65-66` |
| `modules/auth/service.py` | `:52-53` و `:260-261` — گیت `dev_code` فقط به provider (**F‑02**) |
| `modules/shop/service.py` | `_own_member:293-298` — ریشهٔ **F‑27**؛ `next_transfer_state:45` (radon **E 34**) |
| `modules/shop/router.py` | ۸ پارامتر `int` بدون گارد؛ `checkout:206`, `orders:219`, `order_receipt:224` |
| `modules/axis_assessment/router.py` | `:17` و `:49` — گارد تکراری (**F‑13**) |
| `modules/payments/gateway.py` | `:97, :114, :164` — `httpx.Client` سنکرون در مسیر async (**F‑04**) |
| `modules/payments/manual_transfer_policy.py` | کل ۱۱۷ خط — هدف آزمون جهش (**F‑11**) |
| `modules/expenses/schemas.py` | `:27 note: Field("", max_length=1000)` — سقف طول (T‑47) |
| `modules/admin/analytics.py` | `:157, :325` تقسیم پول؛ `:199 collect_member_facts`؛ `:342 members_summary` |
| `api/v1/monitoring.py` | `:18, :24` — `except: pass` در مسیر خودِ مشاهده‌پذیری (**F‑17**) |
| `jobs/outbox_relay.py` | `:41` — الگوی درستِ `with get_session_factory()()` |
| `scripts/dast.py` | `:66` توکن بدون `sid` (**F‑08**)، `:79,:174,:180` `except: pass`، `:89` وابستگی به `hypothesis` (declare نشده) |
| `scripts/deploy_gate.py` | ۹ بررسی موجود؛ نبودِ بررسی `dev_code`/`TRUSTED_PROXIES` (**F‑02**) |
| `scripts/seed_s3c_m39.py` | `:28` توکن بدون `sid` که روی stdout چاپ می‌شود (**F‑08**) |
| `db/migrations/versions/c3f01ab129e2_…py` | `:67,:165,:169,:171` — SQL با f‑string (**F‑22**) |
| `tests/regression/test_manual_transfer_policy.py` | ۱۴ آزمون/۵۴ مورد پارامتریک — سنگ محک آزمون جهش |
| `tests/integration/test_route_guards.py` | چگونه `routes.json` را اوراکل می‌گیرد (**F‑12**) |

### ۷‑۳) منابع بیرونی (GitHub / Hugging Face) — با وضعیت مجوز

قاعدهٔ مالک: **همهٔ ابزارها کاملاً رایگان و بازمتن**؛ و چون `MP` مجوز اختصاصی دارد،
هر ابزار **GPL/AGPL/LGPL فقط به‌عنوان ابزار توسعه/CI** مجاز است و هرگز داخل artifact توزیعی نمی‌رود.

**الف) ابزارهایی که در این ممیزی نصب و اجرا شدند:**

| ابزار | مخزن | مجوز | وضعیت در این اجرا |
|---|---|---|---|
| ruff | `astral-sh/ruff` | MIT | ✅ اجرا شد |
| bandit | `PyCQA/bandit` | Apache‑2.0 | ✅ |
| radon | `rubik/radon` | MIT | ✅ |
| lizard | `terryyin/lizard` | BSD | ✅ |
| vulture | `jendrikseipp/vulture` | MIT | ✅ |
| detect-secrets | `Yelp/detect-secrets` | Apache‑2.0 | ✅ |
| pip-audit | `pypa/pip-audit` | Apache‑2.0 | ✅ (با `-r` روی وابستگی‌های پروژه) |
| semgrep | `semgrep/semgrep` | LGPL‑2.1 (CLI) ⇒ **فقط dev/CI** | ✅ با قواعد اختصاصی آفلاین |
| mutmut | `boxed/mutmut` | BSD | ⚠️ قضاوت نادقیق |
| py-spy | `benfred/py-spy` | MIT | ✅ (ریشهٔ F‑03 را یافت) |
| ESLint + `typescript-eslint` + `eslint-plugin-react-hooks` + `eslint-plugin-jsx-a11y` | `eslint/eslint` و … | MIT | ✅ |
| madge | `pahen/madge` | MIT | ✅ |
| jscpd | `kucherenko/jscpd` | MIT | ✅ |
| knip | `webpro-nl/knip` | ISC | 🚫 کرش |
| schemathesis | `schemathesis/schemathesis` | MIT | نصب شد؛ استفادهٔ کامل نشد |
| hypothesis | `HypothesisWorks/hypothesis-python` | MPL‑2.0 | در محیط ممیزی نصب شد (پروژه آن را declare نکرده) |

**ب) ابزارهایی که برای CI بعدی ارزیابی و تأیید شدند** (همه رایگان/بازمتن، همه بررسی آرشیو شدند):

| دسته | ابزارها |
|---|---|
| SBOM/زنجیرهٔ تأمین | `ossf/scorecard`, `anchore/syft`, `anchore/grype`, `anchore/sbom-action`, `sigstore/cosign`, `pypa/pip-audit`, `google/osv-scanner`, `slsa-framework/slsa-github-generator` |
| SAST/ IaC | `semgrep/semgrep`, `Checkmarx/kics`, `aquasecurity/trivy`, `github/codeql-action`, `stoplightio/spectral`, `squawk` (Postgres) |
| پین کردن Actions | `peter-evans/pin-github-action`, `dependabot-core` |
| Python | `astral-sh/ruff`, `PyCQA/bandit`, `pre-commit/pre-commit`, `import-linter/import-linter`, `rubik/radon`, `terryyin/lizard`, `jendrikseipp/vulture`, `boxed/mutmut`, `sixty-north/cosmic-ray`, `HypothesisWorks/hypothesis-python` |
| JS/TS | `webpro-nl/knip`, `kucherenko/jscpd`, `pahen/madge`, `dubzzz/fast-check`, `stryker-mutator/stryker-js` |
| تست UI/موبایل | `microsoft/playwright`, `dequelabs/axe-core`, `GoogleChrome/lighthouse-ci`, `GoogleChromeLabs/web-vitals`, `flutter/patrol` (leancodepl/patrol), `hurl` (Orange‑OpenSource), `locustio/locust` |
| آشوب‌سازی و مشاهده‌پذیری | `gremlins/pumba`, `shopify/toxiproxy`, `open-telemetry/opentelemetry-python`, `jaegertracing/jaeger`, `burke-software/GlitchTip`, `benfred/py-spy`, `hatoo/oha` |
| مجوز/انطباق | `oss-review-toolkit/ORT`, `scanoss/scancode-toolkit`, `license-checker-rseidelhoen` |
| AI (با مجوز سازگار) | `All-Hands-AI/OpenHands`, `The-PR-Agent/pr-agent`, `Aider-AI/aider`, `Qwen/Qwen3-Coder-30B-A3B-Instruct` (Hugging Face, apache‑2.0) |
| **فقط dev/CI به‌خاطر AGPL/LGPL/GPL** | `baunes/repowise` (AGPL), `grafana/loki` (AGPL), `grafana/k6` (AGPL), `trufflesecurity/trufflehog` (AGPL), `renovatebot/renovate`, `SonarSource/sonarqube` (LGPL + بدون پشتیبانی Dart), `hadolint/hadolint` (GPL) |
| **هرگز استفاده نشود** | `dart-code-checker/dart-code-metrics` (NOASSERTION + آرشیو ۲۰۲۳‑۰۷‑۱۶), `doyensec/electronegativity` (آرشیو) |

### ۷‑۴) قواعد/استانداردهایی که به آن‌ها استناد شد

| استاندارد | کجا استفاده شد |
|---|---|
| `Number.MAX_SAFE_INTEGER = 2^53−1` (ECMAScript) | F‑09, F‑25 — هم‌خوان با `MAX_SAFE_ID` خودِ پروژه |
| RFC 9110 (HTTP Semantics): تفاوت `404` در برابر `409` در برابر `422` | F‑14, F‑26, F‑27 |
| قرارداد نام‌گذاری Prometheus (`mp_<domain>_<name>_<unit>`) | F‑04 — پیشنهاد گیج‌های pool |
| OWASP: rate limiting و trusting client-supplied headers | F‑01 |
| uvicorn `--proxy-headers` / `forwarded_allow_ips` (پیش‌فرض `127.0.0.1,::1`) | F‑01 — `uvicorn/config.py:225, :363` |
| Python `str.isdigit()` (فقط ارقام، بدون علامت) | F‑25 — ریشهٔ نقص |
| structlog `ConsoleRenderer` / `RichTracebackFormatter` در برابر `JSONRenderer` | F‑03 |
| casbin `enforcer.enable_cache` | F‑05 |
| WCAG 2.1 (برچسب کنترل فرم، autofocus) | F‑10 — ۱۲ + ۱ خطای `jsx-a11y` |

### ۷‑۵) آنچه **منبع قرار نگرفت** (و چرا)

| منبع | دلیل |
|---|---|
| اعداد مستند‌شدهٔ خودِ پروژه (۹۴٫۲۸٪ پوشش، ۱۲۱/۱۳۷ مسیر، «DAST ۰ یافته») | با اجرا رد یا ناقص شدند (§۵) |
| امتیاز health ‏RepoWise (۹٫۲۶/۱۰) | متدولوژیِ آن مستقل قابل بازآزمایی نیست؛ فقط فهرست فایل‌های بدترش به‌عنوان **سرنخ** استفاده شد |
| یافته‌های ایستای قبلیِ خودم (CSP، `print()`ها، ۷۵ دکمهٔ بی‌سیم، نشت session) | با اجرا رد شدند — در §۹ گزارش اصلی فهرست شده‌اند |
| خروجی خام `mutmut results` | نادقیق بودنش اثبات شد |
| حافظهٔ جلسه برای هر عدد | همهٔ اعداد از فایل شاهد استخراج شدند (قاعدهٔ §۰) |

---

## ۸) قابلیت اتکای ابزارها و مرزهای اجرای این ممیزی

### ۸‑۱) جدول قابلیت اتکا (نتیجهٔ تجربهٔ مستقیم در این اجرا، نه از مستندات ابزار)

| ابزار | نصب | اجرا | قضاوتِ قابل اتکا؟ | درس عملیاتی |
|---|---|---|---|---|
| pytest + coverage | ✅ | ✅ | ✅ بالا | `--cov=.` دامنه را عوض می‌کند؛ همیشه دامنه را در گزارش بنویسید |
| ruff | ✅ | ✅ | ✅ بالا | — |
| radon cc | ✅ | ✅ | ✅ بالا | خروجی `path - GRADE (SCORE)` است؛ regex معکوس پارس نمی‌شود |
| radon mi | ✅ | ✅ | ✅ | ۱۹۵ فایل، همه A/B |
| lizard | ✅ | ✅ | ✅ | `-w` فقط هشدارها را می‌دهد؛ برای آمار کامل بدون `-w` اجرا کنید |
| vulture | ✅ | ✅ | ⚠️ متوسط | فقط ۱ یافته ⇒ حساسیت پایین؛ با whitelist استفاده شود |
| bandit | ✅ | ✅ | ⚠️ متوسط | همه LOW؛ برای B110/B112/B105 مفید است |
| pip-audit | ✅ | ✅ | ✅ **به شرط `-r` روی نیازمندی‌های پروژه** | اجرای آن روی محیطِ ابزار، یافتهٔ کاذب می‌دهد (pip/mcp) |
| detect-secrets | ✅ | ✅ | ⚠️ متوسط | روی اسنادی که **نام** secret را می‌نویسند FP می‌دهد؛ baseline لازم است |
| semgrep | ✅ | ✅ | ✅ بالا با قواعد اختصاصی | `--config auto` و `--validate` نیاز به شبکه دارند (اینجا مسدود)؛ `tsx` پشتیبانی نمی‌شود (باید `typescript` نوشت) |
| mutmut 2.5.1 | ✅ | ✅ | ❌ **قضاوت نادقیق** | هرگز بی‌راستی‌آزمایی دستی گیت نشود |
| mutmut 3.8.1 | ✅ | ❌ | — | CLI عوض شده (`add source_paths`)؛ استفاده نکنید |
| py-spy | ✅ | ✅ | ✅ **بسیار بالا** | ارزشمندترین ابزار این ممیزی؛ به pid واقعیِ پایتون نیاز دارد |
| ESLint 9 | ✅ | ✅ | ✅ بالا | نصب ترکیبی با `ERESOLVE` شکست ⇒ هر بسته جدا با `--legacy-peer-deps` |
| madge | ✅ | ✅ | ✅ | — |
| jscpd | ✅ | ✅ | ✅ | — |
| knip | ✅ | ❌ | — | کرش `oxc-parser` روی Node 22.22.3 |
| vitest / tsc | ✅ | ✅ | ✅ | — |
| schemathesis | ✅ | نصب شد | استفادهٔ کامل نشد | ماتریس اختصاصی دقیق‌تر از fuzz عمومی بود |

### ۸‑۲) موارد BLOCKED — آنچه نتوانستم بسنجم (و نباید «سالم» فرض شود)

| حوزه | دلیل فنی | ریسک باقی‌مانده |
|---|---|---|
| Flutter/Dart: `flutter analyze`, `flutter test`, golden tests, patrol | Flutter SDK در sandbox نیست | کیفیت کلاینت موبایل **سنجیده نشد**؛ فقط ۱ قاعدهٔ semgrep اجرا شد |
| ساخت APK/AAB، R8/ProGuard، `lintVitalRelease`، JADX، apkanalyzer | نبود JDK/Gradle | باگ شناخته‌شدهٔ `android:debuggable="false"` تأیید اجرایی نشد |
| آشوب‌سازی کانتینری (Pumba)، hadolint روی image واقعی، `docker compose up`، Testcontainers | نبود Docker daemon | رفتار در استقرار واقعی (Caddy + Postgres + Valkey) **هرگز اجرا نشد** |
| Postgres واقعی | نصب نیست | سناریوی «SQLite در برابر Postgres» و قفل‌شدن نوشتن‌ها سنجیده نشد |
| Valkey/Redis واقعی | نصب نیست | `memory://` تست شد؛ **اشتراک سبد بین ورکرها در production** تست نشد |
| Prometheus/Grafana واقعی | نصب نیست | درستی rule/alertها سنجیده نشد |
| آزمون UI مرورگری (Playwright، axe، Lighthouse، مرور ۱۰ دکمهٔ بدون onClick) | Chromium بی‌سر در ~۳٫۶ GB RAM ممکن نیست | a11y و جریان‌های کلیک‌شده **تأیید اجرایی نشدند** |
| قواعد آمادهٔ semgrep (`--config auto`, `p/python`) | دسترسی به semgrep.dev مسدود | پوشش قواعد عمومی ناشناخته است |
| آزمون جهش روی کل سوئیت | ۱٬۰۹۵ تست × ۴۶۱ ثانیه بر هر جهش، روی ۲ هسته | امتیاز جهش فقط برای **یک** ماژول پولی اندازه‌گیری شد |
| وضعیت branch protection ‏`main` | GitHub API ⇒ **۴۰۳** | نمی‌توان گفت آیا PR بدون بررسی merge می‌شود |
| مرور دستی ۱۰ دکمهٔ بدون `onClick` | نیاز به مرورگر | ممکن است `type="submit"` سالم باشند یا دکمهٔ مرده |

---

## ۹) ماتریس ردیابی — از یافته تا شاهد تا دستور

| یافته | شدت | تست‌ها | فایل‌های شاهد | خطوط کلیدی منبع | شاهد پذیرشِ رفع |
|---|---|---|---|---|---|
| F‑01 XFF | Critical | T‑36, T‑38, T‑48 | `xff-dockerfile-cmd.json`, `otp-ratelimit-verdicts.json`, `otp-bruteforce.json` | `Dockerfile:27`, `infra/Dockerfile.backend:29`, `app/security/proxy.py:38-58`, `modules/auth/router.py:28-38`, `app/config.py:69` | ۳۰ درخواست با XFF تصادفی ⇒ ≥۲۷ × `429` |
| F‑02 fail-open محیط | Critical | T‑30, T‑35 | `live-security-raw.json`, `metrics-noauth.txt` | `app/config.py:25,127-135`, `modules/auth/service.py:52-53,260-261`, `scripts/deploy_gate.py` | بدون `MP_ENVIRONMENT`: بالا نیاید یا `dev_code` در پاسخ نباشد |
| F‑03 قفل rich | Critical | T‑39, T‑40, T‑41 | `load-plain-dev.json`, `logging-cost.json`, لاگ خام ۱۴۸ MB | `app/main.py:50`, `app/unhandled.py:91`, `app/logging.py` | بار ۸۰ کلاینتی ⇒ لاگ < ۵ MB، `/health` < ۵۰۰ ms، SIGTERM < ۱۰ s |
| F‑04 اشباع pool | High | T‑39, T‑46, T‑40 | `pool-events.jsonl` | `db/base.py`, `app/deps.py:53`, `modules/payments/gateway.py:97,114,164` | `mp_db_pool_checkedout` در `/metrics`؛ بار سنگین ⇒ ۵۰۳ نه ۵۰۰ |
| F‑05 casbin SystemError | High | T‑42, T‑43, T‑44 | `rbac-systemerror-repro.json` | `app/security/rbac.py:230-290,264`, `app/deps.py:135` | ۸۰ نخ × ۴۰۰ فراخوانی ⇒ ۰ خطا؛ میانهٔ `enforce` < ۵۰ µs |
| F‑06 `/metrics` باز | High | T‑30, T‑35 | `metrics-noauth.txt` | `api/v1/monitoring.py:18,24` | بدون توکن ⇒ ۴۰۱/۴۰۳ |
| F‑07 پوشش | High | T‑01 | `backend-coverage.xml` | `PROJECT-HANDOFF.md`, `pyproject.toml` | CI عدد را با دامنهٔ صریح چاپ کند؛ `db ≥ 80`, `modules ≥ 90` |
| F‑08 logout-all | High | T‑35 | `live-security-verdicts.json`, `semgrep-backend.json` | `app/deps.py:60-73,75-95`, `scripts/dast.py:66`, `scripts/seed_s3c_m39.py:28` | پس از `logout-all` هر توکنی ⇒ ۴۰۱ |
| F‑09 مرزهای پولی | High | T‑35 | `live-security-raw.json` | `app/deps.py:36,39`, schemaهای پرداخت | `amount_rial=2^53+1` ⇒ ۴۲۲؛ `"1500000"` ⇒ ۴۲۲ |
| F‑10 نبود lint | High | T‑17 | `eslint-studio.json` | `studio/package.json`, `.github/workflows/*` | `eslint .` ⇒ ۰ error |
| F‑11 جهش ۵۷٫۸٪ | High | T‑21 | `mutmut-verified.json` | `modules/payments/manual_transfer_policy.py:39,49,62` | جهش‌های `#27/#31/#36` ⇒ killed |
| F‑12 اوراکل routes.json | Med‑High | T‑32, T‑45 | `contract-matrix-raw.json`, `contract-diff.json`, `contract-rbac-findings.json` | `api/routes.json`, `tests/integration/test_route_guards.py` | «مشاهده‌شده == اعلام‌شده» برای هر ۱٬۱۴۱ جفت |
| F‑13 گارد تکراری | Medium | T‑32, T‑45 | `contract-diff.json` | `modules/axis_assessment/router.py:17,49` | `guards == ["permission"]` |
| F‑14 gateway-return ۲۰۰ | Medium | T‑34 | `contract-invalid-authed.json` | مسیر `payments/{id}/gateway-return` | ⇒ ۴۰۴ با همان HTML |
| F‑15 پیچیدگی | Medium | T‑07, T‑08, T‑09 | `radon-cc.txt`, `radon-mi.txt`, `lizard*.txt` | `app/config.py:128` (F 47), `engine/axis_prescription.py:43` (F 46) | CC هر تابع < ۱۵؛ ۰ بلوک ≥D |
| F‑16 ایمنی ایستا | Medium | T‑10…T‑13 | `bandit.json`, `detect-secrets.json`, `vulture.txt` | `app/config.py:16` | بدون اقدام فوری |
| F‑17 خطای بی‌صدا | Medium | T‑14 | `semgrep-backend.json` | `api/v1/monitoring.py:18,24`, `scripts/dast.py:79,174,180` | semgrep ⇒ ۰ یافته |
| F‑18 ظرفیت/پیکربندی | Medium | T‑46, T‑48, §۱‑۳ | `pool-events.jsonl`, `contract-invalid-authed.json` | `Dockerfile:27`, `db/base.py`, `app/config.py:65` | جدول حساب ظرفیت در RUNBOOK + گیت |
| F‑19 سه لایهٔ داده | Low‑Med | T‑22 | `studio-ui-wiring.json` | `studio/src/lib/{api,adminApi,session}.ts`, `pages/Shop.tsx:446,459` | grep ⇒ ۰ `await import(` در هندلرها |
| F‑20 export مرده | Low | T‑22 | `studio-ui-wiring.json` | `lib/api.ts:1558` | حذف یا اتصال + تست |
| F‑21 session/وابستگی | Low | T‑14, T‑01 | `semgrep-backend.json` | ۵ اسکریپت، `scripts/dast.py:89` | semgrep ⇒ ۰؛ `dast.py --help` در محیط تمیز |
| F‑22 SQL با f-string | Low | T‑14 | `semgrep-backend.json` | `db/migrations/versions/c3f01ab129e2_…:67,165,169,171` | `op.execute(sa.text(...))` |
| F‑23 دکمه‌های بی‌سیم | Medium | T‑22 | `studio-ui-wiring.json` | ۱۰ محل (§F‑23 گزارش اصلی) | Playwright در CI ⇒ مرور انجام شود |
| F‑24 هشدارهای runtime | Low | T‑39, T‑40 | لاگ خام | ثابت منسوخ ۴۲۲ | اجرای بار بدون `StarletteDeprecationWarning` |
| **F‑25 کفِ گارد شناسه** | **Medium** | **T‑34, T‑23, T‑47** | `contract-invalid-authed.json`, `pathid-scan.json` | `app/id_guard.py:47-52`, `app/deps.py:39` | `unexpected_2xx_on_bad_id == 0` |
| **F‑26 دو شکل پاکت** | **Medium** | **T‑34** | `contract-invalid-authed.json` | هندلرهای `app/unhandled.py`/`app/errors.py` | `fastapi_default_detail == 0` |
| **F‑27 پیش‌نیاز پروندهٔ عضو** | **Medium** | **T‑31, T‑48** | `contract-matrix-raw.json` (pass=seed) | `modules/shop/service.py:293-298` | ⇒ ۴۰۹ با `member_profile_required` |
| **F‑28 «امروز» با UTC در برابر تهران** | **Medium** | **T‑50** | `ruff-recommended-findings.txt` | `modules/axis_assessment/service.py:31`، `modules/nutrition/service.py:124,182` در برابر `modules/shop/service.py:61-62` | `grep -rn "date.today()" modules app engine jobs` ⇒ **۰** مورد |
| **F‑29 لاگ بدون traceback در SMS + noqaهای مرده** | **Low‑Med** | **T‑50** | `ruff-recommended-findings.txt` | `app/sms.py:66,69,72,99,102,105` و `:52,61,94` | `ruff check --select TRY400,S310,RUF100` ⇒ ۰ یافته |

---

## ۱۰) بازتولید کامل — از صفر تا هر عددِ این پرونده

```bash
# ── ۰. پیش‌نیازها ─────────────────────────────────────────────
# پایتون ۳٫۱۱، Node ۲۲، ۲ هسته، ~۴GB RAM، ۲۰GB دیسک
# مخزن MP فقط‌خواندنی بماند؛ همه‌چیز در /tmp/run

# ── ۱. کپی کاری + تضمین دست‌نخورده بودن ─────────────────────
cp -a /tmp/MP /tmp/run/MP
cd /tmp/MP && git status --porcelain | wc -l        # ⇒ 0
git rev-parse --short HEAD                          # ⇒ 662ff88

# ── ۲. دو محیط مجازی (هرگز قاطی نشوند) ───────────────────────
python3 -m venv /tmp/run/venv        && /tmp/run/venv/bin/pip install -U pip
/tmp/run/venv/bin/pip install -e /tmp/run/MP/mp-app/backend
/tmp/run/venv/bin/pip install pytest pytest-cov hypothesis freezegun fakeredis deepdiff jsonschema
/tmp/run/venv/bin/pip check                         # ⇒ No broken requirements found
python3 -m venv /tmp/run/venv-audit
/tmp/run/venv-audit/bin/pip install semgrep "mutmut<3" vulture radon lizard detect-secrets
mkdir -p /tmp/run/npt && cd /tmp/run/npt && npm init -y
for p in eslint typescript-eslint eslint-plugin-react-hooks eslint-plugin-jsx-a11y jscpd knip madge typescript; do
  npm i --no-audit --no-fund --legacy-peer-deps "$p"; done   # نصب جداگانه: ERESOLVE

# ── ۳. DB از صفر + seed ─────────────────────────────────────
mkdir -p /tmp/run/data/receipts
cd /tmp/run/MP/mp-app/backend
MP_DATABASE_URL=sqlite:////tmp/run/data/mp.db /tmp/run/venv/bin/alembic upgrade head
MP_ENVIRONMENT=development MP_DATABASE_URL=sqlite:////tmp/run/data/mp.db \
  PYTHONPATH=/tmp/run/MP/mp-app/backend \
  /tmp/run/venv/bin/python /tmp/run/MP/qa-report/tools/seed_live.py

# ── ۴. بالا آوردن اپ (سه پیکربندی) ─────────────────────────
ENVV='MP_ENVIRONMENT=development MP_DATABASE_URL=sqlite:////tmp/run/data/mp.db \
MP_SECRET_KEY=audit-harness-only-secret-0123456789abcdef MP_SMS_PROVIDER=dev \
MP_PAYMENT_GATEWAY=manual MP_RECEIPTS_DIR=/tmp/run/data/receipts MP_TRUSTED_PROXIES='
# S1 ابزار‌دار (+ shop باز):
env $ENVV MP_SHOP_ONLINE_PURCHASE_ENABLED=true MP_SHOP_OPEN_HOUR=0 MP_SHOP_CLOSE_HOUR=23 \
  /tmp/run/venv/bin/python /home/user/Chat2DB/audit/serve_backend.py
# S2 کنترل خام:   … audit/serve_plain.py
# S3 عینِ Dockerfile (برای F‑01):
env $ENVV /tmp/run/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8010 \
  --workers 2 --proxy-headers --forwarded-allow-ips='*'
curl -s http://127.0.0.1:8010/health          # ⇒ {"status":"ok",…}
curl -s http://127.0.0.1:8010/audit/threads   # ⇒ total_tokens: 40   (فقط S1)

# ── ۵. تست‌های دستهٔ A ──────────────────────────────────────
/tmp/run/venv/bin/python -m pytest -q --cov=. --cov-report=xml:/home/user/Chat2DB/audit/evidence/backend-coverage.xml
cd /tmp/run/MP/mp-app/studio && npm ci && npx tsc --noEmit && npx vitest run

# ── ۶. پراب‌های زنده (دستهٔ C) ─────────────────────────────
cd /home/user/Chat2DB/audit
/tmp/run/venv/bin/python probe_contract.py all        # T‑31 + T‑32 (+T‑33 که نادرست‌نتیجه است)
/tmp/run/venv/bin/python probe_invalid_authed.py      # T‑34 + T‑47 + T‑49 ← معتبر
/tmp/run/venv/bin/python probe_live_security.py       # T‑35
/tmp/run/venv/bin/python probe_otp_limits.py all      # T‑36 (~۵ دقیقه به‌خاطر پنجره‌های نرخ)
/tmp/run/venv/bin/python bench_logging.py             # T‑41
/tmp/run/venv/bin/python repro_rbac_systemerror.py 80 40 400   # T‑42/43/44
/tmp/run/venv/bin/python scan_ui_wiring.py            # T‑22
/tmp/run/venv/bin/python probe_load.py plain-dev 10 40 60 80   # T‑40 (روی S2)

# ── ۷. شاهد حداقلی F‑25 با curl ────────────────────────────
TOK=$(PYTHONPATH=/home/user/Chat2DB/audit /tmp/run/venv/bin/python -c \
  'from harness_common import mint_token; print(mint_token(256,"admin"))')
for id in -1 0 -0 -9223372036854775808 99999999999999999999999 abc 1; do
  printf "%-24s -> %s\n" "$id" "$(curl -s -o /dev/null -w '%{http_code}' \
    -H "Authorization: Bearer $TOK" http://127.0.0.1:8010/api/v1/assessments/member/$id)"
done
# انتظارِ یافت‌شده: 200 200 200 200 422 422 200

# ── ۸. شاهد حداقلی F‑01 با curl (روی S3) ───────────────────
for i in $(seq 1 30); do curl -s -o /dev/null -w "%{http_code} " \
  -H "X-Forwarded-For: 203.0.113.$((RANDOM % 250 + 1))" -H 'content-type: application/json' \
  -d '{"phone":"0913'$RANDOM$RANDOM'"}' http://127.0.0.1:8010/api/v1/auth/otp/request; done; echo
# انتظارِ یافت‌شده: سی بار «200»

# ── ۹. ابزارهای ایستا (دستهٔ B) ────────────────────────────
cd /tmp/run/MP/mp-app/backend && /tmp/run/venv/bin/ruff check . && /tmp/run/venv/bin/ruff format --check .
/tmp/run/venv/bin/radon cc app modules db engine security jobs cache api scripts -s -n C --total-average
/tmp/run/venv/bin/radon mi app modules db engine security jobs cache api scripts
/tmp/run/venv/bin/lizard app modules db engine security jobs cache api --CCN 10 --length 60 -w
/tmp/run/venv-audit/bin/vulture app modules db engine security jobs cache api scripts devtools --min-confidence 80
/tmp/run/venv/bin/bandit -r app modules db engine security jobs cache api scripts -f json -q
/tmp/run/venv/bin/pip-audit -r /tmp/run/mp-deps.txt --no-deps --progress-spinner off
/tmp/run/venv-audit/bin/detect-secrets scan /tmp/run/MP --all-files
/tmp/run/venv-audit/bin/semgrep --config /home/user/Chat2DB/audit/semgrep-mp.yml --metrics=off --json /tmp/run/MP
cd /tmp/run/MP/mp-app/studio && /tmp/run/npt/node_modules/.bin/eslint --config /tmp/run/npt/eslint.mp.config.mjs --format json src
/tmp/run/npt/node_modules/.bin/madge --circular --extensions ts,tsx src
/tmp/run/npt/node_modules/.bin/jscpd --min-tokens 70 --reporters json --output /tmp/out src

# ── ۱۰. آزمون جهش با راستی‌آزمایی دستی (mutmut تنها معتبر نیست)
cd /tmp/run/MP/mp-app/backend
/tmp/run/venv-audit/bin/mutmut run --paths-to-mutate modules/payments/manual_transfer_policy.py \
  --runner "/tmp/run/venv/bin/python -m pytest -x -q tests/regression/test_manual_transfer_policy.py" \
  --no-progress --simple-output
for id in $(seq 1 45); do
  /tmp/run/venv-audit/bin/mutmut apply $id
  /tmp/run/venv/bin/python -m pytest -q tests/regression/test_manual_transfer_policy.py >/dev/null \
    && echo "$id SURVIVED" || echo "$id KILLED"
  git checkout -- modules/payments/manual_transfer_policy.py
done
git status --porcelain | wc -l        # ⇒ 0  (بازگرداندن کامل)
```

---

## ۱۱) امضای پرونده

| مورد | مقدار |
|---|---|
| تعداد اجراهای ثبت‌شده | **۵۰** (T‑01…T‑50 در ۶ دسته) |
| تعداد سلول/درخواست اندازه‌گیری‌شده | ۱٬۱۴۱ (ماتریس مجوز) + ۸۷۲ (ورودی خصمانهٔ معتبر) + ۸۰۴ (پاس نادرست‌نتیجه، بایگانی‌شده) + ۱۶ (seed) + ~۴۴ (XFF/OTP) + ده‌ها هزار درخواست بار |
| تعداد یافته | **۲۹** (F‑01…F‑29) |
| تعداد خاصیتِ سالمِ تأییدشده | ۲۷ |
| تعداد یافتهٔ کاذبِ خودم که رد شد | ۱۲ + ۱ نقص روش‌شناختی (T‑33) |
| حوزه‌های BLOCKED | ۱۱ |
| فایل‌های شاهد commit‌شده | **56** (3,156,857 بایت ≈ 3.01 MB) |
| مخزن `MP` | **بدون هیچ تغییر** — `git status --porcelain` = ۰ در پایان هر مرحله |
| داده‌ها | کاملاً مصنوعی |
| پنجرهٔ اجرا | ۲۰۲۶‑۱۱‑۲۰ ۲۲:۱۰ تا ۲۰۲۶‑۱۱‑۲۱ ۰۴:۴۵ UTC |
| سندِ همراه | `share/MP-FINAL-AUDIT-REPORT-2026-11-20.md` (گزارش یافته‌ها) |
