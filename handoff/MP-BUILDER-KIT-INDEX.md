# کیتِ کاملِ بیلدر — اول این را بخوان

> بستهٔ خودکفا برای نشستِ بیلدرِ پروژهٔ MP. **هیچ‌چیز بیرونی لازم نیست**: نه پیوند،
> نه دسترسیِ شبکه، نه فایلِ دیگری در مخزن. هر عددی که بیلدر باید بازتولید کند، همراه با
> فرمانِ دقیقِ اندازه‌گیری‌اش داخلِ همین بسته است.
>
> ساخته‌شده در ۲۰۲۶‑۱۱‑۲۱ · base commit 662ff88 · ruff 0.17.6 · 71 ورودی · مهرِ زمانیِ ثابت (بازتولیدپذیر)

---

## ۱ · تنها کاری که باید همین حالا بکنی

`01-paste-into-builder-session/MP-BUILDER-HANDOFF-A1.3.md` را باز کن و متنِ بینِ دو
نشانگرِ **«از اینجا کپی کن»** و **«تا اینجا کپی کن»** را **عیناً** در نشستِ بیلدر
(یا حلقهٔ `FINN-AUDIT-LOOP.md`) کپی کن. بقیهٔ این بسته مرجع است، نه پیام.

چرا کپی و نه پیوند: یک بار به‌جای کپی‌کردنِ متن به آن **ارجاع** داده شد و کلِ `WP 0.9`
یک دورِ کامل بلاک ماند، چون بیلدر فقط چیزی را می‌بیند که در نشستش کپی شده است.

## ۲ · ترتیبِ خواندن

| پوشه | چه دارد | کی لازم می‌شود |
|---|---|---|
| `01-paste-into-builder-session/` | پیامِ آمادهٔ کپی (A1.3): حلِ اختلافِ `RUF100`، اعدادِ هر مرحله، پروتکلِ بی‌ناظر، پیکربندی و اسکریپتِ کامل | **اول** — همین حالا |
| `02-plan/` | پرامپتِ اصلیِ بیلدر (۳۰ WP در ۵ فاز) + الحاقیهٔ A1.3 (`WP 0.9`/`2.6`/`3.6`، تصحیحِ `WP 4.5`، `D‑6`/`D‑7`، §۹) | پیش از شروعِ هر WP |
| `03-findings/` | گزارشِ نهاییِ ۲۹ یافته (`F‑01`…`F‑29`) با زنجیرهٔ `file:line`، ۲۷ ردیفِ سالم، ۱۲+۱ مدعای ردشده، نقشهٔ رفع؛ و صورت‌مسئله‌ها | هنگامِ رفعِ هر یافته |
| `04-evidence/` | پروندهٔ شواهد (§۰–§۱۱ با جدولِ ۲۰ ردیفیِ تصحیحات و manifest) + بریفِ ایجنت + `raw/` = ۴۴ شاهدِ خامِ اندازه‌گیری‌ها | هر وقت عددی را باور نکردی |
| `05-tools/` | پیکربندیِ ruff، اسکریپتِ پذیرش، قواعدِ semgrep، پیکربندیِ ESLint، و `harness/` = ۱۴ اسکریپتِ probe/serve/bench برای **اجرای دوبارهٔ** هر آزمایش | هنگامِ ساختِ گیت و بازتولیدِ شاهد |
| `06-background/` | کاتالوگِ ابزارهای **کاملاً رایگان و اوپن‌سورس** برای هر لایهٔ ممیزی | هنگامِ انتخابِ ابزارِ CI |

⚠ **یک caveat در `06-background/AUDIT_TOOLCHAIN.md`:** بخشِ ۱۲ آن («هستهٔ حداقلی»)
برای استکِ **Java 17 / Spring Boot / React‑TS** نوشته شده و به MP
(**پایتون ۳٫۱۱ / FastAPI / SQLAlchemy**) ربطی ندارد. بخش‌های ۰ تا ۱۱ و ۱۳
(نگاشتِ خواسته ← ابزار، و «از این‌ها استفاده نکنید») قابلِ استفاده‌اند.

## ۳ · دو فرمانِ شروع

```bash
# ۱) پیکربندی را عیناً نصب کن (متنِ کامل در §۵ پیامِ هند‌آف و در 05-tools/)
cp 05-tools/ruff-recommended.toml mp-app/backend/ruff-audit.toml   # یا داخلِ pyproject.toml

# ۲) گیت‌ها را بسنج — باید «گیت‌های نامنطبق: ۰ / PASS» بدهد
cd mp-app/backend
RUFF=/path/to/ruff CFG=../ruff-audit.toml bash ../../05-tools/verify-addendum-gates.sh before
```

مقدارهای موردانتظار: گام ۱ ⇒ **۴۳۰ یافته / ۵۲ قاعدهٔ متمایز**؛ پس از افزودنِ
`"ERA001",` به `ignore` ⇒ **۴۱۹ / ۵۱**. در هر دو حالت `RUF100` = **۳۹**،
`TRY400` = **۶**، `DTZ011` = **۳**، `C901` = **۱۵**، و
`ruff format --check` ⇒ **۳۷۸ فایل already formatted**.

## ۴ · سه قاعدهٔ کلیِ این بسته

1. **عددها به نسخه گره خورده‌اند.** همهٔ اعداد با **ruff ‏۰٫۱۷٫۶** روی **۳۷۶ فایل** در
   commit **`662ff88`** و با `--no-cache` گرفته شده‌اند. با نسخهٔ دیگر، عددِ مطلق عوض می‌شود.
2. **زمان‌ها نسبت‌اند، نه مطلق.** میلی‌ثانیه‌ها ماشین‌وابسته‌اند (۲ vCPU). نسبتِ
   «گیتِ lint در برابر pytest» (~۰٫۰۲٪) معتبر است، عددِ خام نه.
3. **اگر عددِ تو فرق داشت، عددِ تو معتبر است** — به شرطِ ثبتِ عینیِ فرمان. آنچه مجاز
   نیست: دستکاریِ پیکربندی یا پاک‌کردنِ `# noqa` برای رسیدن به عددِ سند
   (پیامِ هند‌آف §۳‑۲: ممنوعیتِ «سبزکردنِ گیت با سرکوب»).

## ۵ · وارسیِ سلامتِ بسته

```bash
sha256sum -c MANIFEST.sha256 --quiet && echo "همهٔ اعضا سالم‌اند"
```

`MANIFEST.sha256` hashِ **همهٔ اعضا جز خودش** را دارد. hashِ خودِ ZIP داخلِ خودش نیست
(دورِ باطل است)؛ در `handoff/README.md` و در پیامِ commitِ مخزن ثبت شده است.

## ۶ · اعضای بسته

(بدونِ خودِ این فایل و بدونِ `MANIFEST.sha256` — هیچ‌کدام نمی‌توانند hashِ خودشان را داشته باشند)

| عضو | اندازه (بایت) | SHA‑256 (۱۶ رقم نخست) |
|---|---|---|
| `01-paste-into-builder-session/MP-BUILDER-HANDOFF-A1.3.md` | 27,908 | `3a0f9582b179651c…` |
| `02-plan/MP-BUILDER-ADDENDUM-2026-11-21.md` | 67,827 | `eb2a37d227703452…` |
| `02-plan/MP-BUILDER-PROMPT-2026-11-21.md` | 40,447 | `9ffc5853019026d2…` |
| `03-findings/MP-FINAL-AUDIT-REPORT-2026-11-20.md` | 114,784 | `65cb5aaf07cfc503…` |
| `03-findings/MP-PROBLEMS-2026-11-20.md` | 40,422 | `a2e7910817bac975…` |
| `04-evidence/MP-AGENT-BRIEF.md` | 140,046 | `af8ef690c394ad92…` |
| `04-evidence/MP-EVIDENCE-DOSSIER-2026-11-20.md` | 163,567 | `3a4841f23aa5629b…` |
| `04-evidence/raw/backend-coverage.xml` | 426,890 | `4bee93f485ddd96c…` |
| `04-evidence/raw/bandit.json` | 88,436 | `e8873e4e62be0a0f…` |
| `04-evidence/raw/contract-diff.json` | 661 | `007efc700ea858a2…` |
| `04-evidence/raw/contract-invalid-authed.json` | 477,652 | `83f99bcd8cd7608b…` |
| `04-evidence/raw/contract-invalid-findings.json` | 227 | `8ec588731b3e813e…` |
| `04-evidence/raw/contract-matrix-raw.json` | 850,104 | `3d58413631bd741f…` |
| `04-evidence/raw/contract-rbac-findings.json` | 73,763 | `7a1615c7a80490bc…` |
| `04-evidence/raw/detect-secrets.err` | 0 | `e3b0c44298fc1c14…` |
| `04-evidence/raw/detect-secrets.json` | 51,599 | `c81a5c71ed768029…` |
| `04-evidence/raw/eslint-stderr.txt` | 0 | `e3b0c44298fc1c14…` |
| `04-evidence/raw/eslint-studio.json` | 227,239 | `f4bc1e42425fae5c…` |
| `04-evidence/raw/jscpd-out/jscpd-report.json` | 13,131 | `b24d9fafa1c9a5f8…` |
| `04-evidence/raw/knip-err.txt` | 1,132 | `39bd484355b70f7d…` |
| `04-evidence/raw/knip-studio.json` | 0 | `e3b0c44298fc1c14…` |
| `04-evidence/raw/live-security-raw.json` | 17,051 | `5fee5dc9e6712414…` |
| `04-evidence/raw/live-security-verdicts.json` | 4,678 | `e469e8204e6943ab…` |
| `04-evidence/raw/lizard-warnings.txt` | 6,316 | `60a06161a1227e87…` |
| `04-evidence/raw/lizard.txt` | 85,468 | `ea8036705318f2bc…` |
| `04-evidence/raw/load-plain-dev.json` | 2,196 | `8cfe7d99c701c551…` |
| `04-evidence/raw/logging-cost.json` | 1,933 | `5aa00c80012a0554…` |
| `04-evidence/raw/metrics-noauth.txt` | 6,529 | `5e91cabc0603eb7f…` |
| `04-evidence/raw/mutmut-manual-transfer-policy.json` | 4,444 | `8e342556a3dc07ef…` |
| `04-evidence/raw/mutmut-verified.json` | 9,751 | `f2efa6755909765f…` |
| `04-evidence/raw/openapi-live.json` | 171,395 | `b6154d165d910be0…` |
| `04-evidence/raw/otp-bruteforce.json` | 213 | `4578fbefd881fe19…` |
| `04-evidence/raw/otp-ratelimit-verdicts.json` | 1,960 | `bb4367a3ce256c36…` |
| `04-evidence/raw/pathid-scan.json` | 6,485 | `786af49a7e77d4e6…` |
| `04-evidence/raw/pool-events.jsonl` | 23,476 | `f6ddcb801ee235d5…` |
| `04-evidence/raw/radon-cc.txt` | 2,283 | `40dd187d192ab682…` |
| `04-evidence/raw/radon-mi.txt` | 8,513 | `a7b72e7fd226eeb8…` |
| `04-evidence/raw/rbac-systemerror-repro.json` | 3,240 | `4fd047831fcce31b…` |
| `04-evidence/raw/ruff-all-families.txt` | 501 | `76f308417919b4bc…` |
| `04-evidence/raw/ruff-all-rules.txt` | 4,857 | `cf6019cda5a780d0…` |
| `04-evidence/raw/ruff-recommended-findings.txt` | 42,414 | `693ab7332acb8ac6…` |
| `04-evidence/raw/ruff-recommended-stats.txt` | 2,153 | `2e3ee2e813ba0c55…` |
| `04-evidence/raw/semgrep-backend.json` | 18,984 | `9dbfae3187f91bb1…` |
| `04-evidence/raw/semgrep-client.json` | 3,428 | `f01227ccc53d73a9…` |
| `04-evidence/raw/semgrep-studio.json` | 6,573 | `453fe65667f5e7b6…` |
| `04-evidence/raw/semgrep-summary.txt` | 2,891 | `0256bb78099c0ffa…` |
| `04-evidence/raw/studio-buttons-wiring.json` | 4,120 | `2a2471ca2049a7a1…` |
| `04-evidence/raw/studio-dead-exports.json` | 351 | `10d3269172162426…` |
| `04-evidence/raw/studio-ui-wiring.json` | 3,349 | `83098cbeef9940da…` |
| `04-evidence/raw/vulture.txt` | 74 | `e2ad653f7ae18595…` |
| `04-evidence/raw/xff-dockerfile-cmd.json` | 462 | `20220d5e4f5eba62…` |
| `05-tools/harness/.gitignore` | 19 | `862263fa1f46c20f…` |
| `05-tools/harness/bench_logging.py` | 3,951 | `3eaec1b8b785987a…` |
| `05-tools/harness/eslint-studio.flat.mjs` | 633 | `613bd388f35229e6…` |
| `05-tools/harness/harness_common.py` | 7,825 | `9204e48d0a8e168d…` |
| `05-tools/harness/probe_concurrency.py` | 9,709 | `26762cc833f5008a…` |
| `05-tools/harness/probe_contract.py` | 25,534 | `b93b37548097d46d…` |
| `05-tools/harness/probe_invalid_authed.py` | 10,772 | `edd3c25cd06a53d8…` |
| `05-tools/harness/probe_live_security.py` | 16,650 | `0b7326b2b10aacf7…` |
| `05-tools/harness/probe_load.py` | 7,721 | `940089b867e6446e…` |
| `05-tools/harness/probe_otp_limits.py` | 6,356 | `662906b965d4801e…` |
| `05-tools/harness/repro_rbac_systemerror.py` | 4,829 | `4d0cfbe573652b38…` |
| `05-tools/harness/scan_ui_wiring.py` | 7,088 | `64e64c20bfe2b1f5…` |
| `05-tools/harness/semgrep-mp.yml` | 7,002 | `d58146b4f372ca82…` |
| `05-tools/harness/serve_backend.py` | 10,139 | `fc1f4e3644718f19…` |
| `05-tools/harness/serve_plain.py` | 2,073 | `fe6a735f3ce45fb5…` |
| `05-tools/ruff-recommended.toml` | 4,973 | `6bafdba17d60db62…` |
| `05-tools/verify-addendum-gates.sh` | 5,409 | `7abab6c3f868697d…` |
| `06-background/AUDIT_TOOLCHAIN.md` | 31,161 | `9a8d52c21087f9b0…` |

---

*این فایل توسط `audit/build_builder_kit.py` ساخته شده و بازتولیدپذیر است: دو اجرای
متوالی، بسته‌ای با sha256ِ یکسان می‌دهند (مهرِ زمانیِ ثابت، بدونِ ساعتِ دیوار).*
