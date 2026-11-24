# ابزارها، منبع رسمی، محل نصب و کاربرد مرحله‌ای

**Arena عامل اصلی کدنویسی است؛ این ابزارها جای Finn یا بازبین مستقل را نمی‌گیرند.** منبع اولیهٔ فرمان‌های محصول، package/workflow/AGENTS همان checkout است. نصب ابزار جدید باید یک نیاز مشخصِ کارت، بررسی هم‌پوشانی و مجوز داشته باشد؛ این سند دستور install-all نیست.

**مرزها:** هیچ ابزار مستندسازی/آزمون این بسته dependency runtime MP نیست. در `mp-app/studio/package.json` یا backend/client ابزار ترسیم نصب نکن. `npm ci` در پوشهٔ ابزار جدا، تنها همان پوشه را تغییر می‌دهد؛ نصب binary/browser/system package به مجوز/محیط خودش نیاز دارد. package lock و metadata، تضمین نبود آسیب‌پذیری یا تأیید حقوقی نیستند.

## ۱. اول کنترل‌های موجود، بعد شکاف

| ابزار/کنترل | منبع رسمی / مجوز | محل و کاربرد در برنامه |
|---|---|---|
| Finn | [finna/Finn-loop](https://github.com/finna/Finn-loop)، metadata MIT؛ پروتکل محلی MP مرجع فعال‌سازی است | spec→build→review→human merge و F/I/N/N؛ خواندن سند مساوی نصب runtime/ساخت issue نیست؛ orchestrator دوم لازم نیست |
| GitHub Actions | [actions](https://github.com/actions)؛ مجوز هر action مستقل | `.github/workflows/ci.yml` و `web.yml` و native jobs حفظ؛ PWA-04/54/55 same-SHA checks، نه CI دوم یا dispatch بدون اذن |
| Semgrep CE | [semgrep/semgrep](https://github.com/semgrep/semgrep)، LGPL-2.1 برای engine؛ rules/Pro/cloud شرایط مستقل | `.semgrep/project-rules.yml` و `mp-harness-rules.yml` فعلی اولویت؛ SAST در G4؛ CLI ایزوله تا dependency backend نشکند |
| Gitleaks CLI | [gitleaks/gitleaks](https://github.com/gitleaks/gitleaks)، MIT؛ نسخهٔ **workflow مقصد** اولویت دارد | history/files با redaction؛ از action با شرط مجوز متفاوت، blind allowlist یا انتشار secret خودداری؛ وجود job≠اجرای scan تازه |
| Ruff / pytest / coverage / Bandit / pip-audit | [Ruff](https://github.com/astral-sh/ruff) MIT؛ [pytest](https://github.com/pytest-dev/pytest) MIT؛ [Bandit](https://github.com/PyCQA/bandit) و [pip-audit](https://github.com/pypa/pip-audit) Apache-2.0 | نسخه‌های constraints backend؛ thresholdهای per-directory جاری حفظ؛ عدد تاریخی coverage جای gate جاری نیست |
| ESLint / Vitest / TypeScript / Vite | منابع و نسخه‌ها در snapshot `mp-app__studio__package.json.source.txt` و lock محصول | lint/test/build Studio موجود؛ بدون ایجاد app دوم یا ارتقای بی‌نیاز library |
| Flutter/Dart/Android | SDK/CI فعلی محصول | PWA-05/55؛ SDK، analyze/format/test و Android debug compile محفوظ؛ نبود SDK در محیط local = NOT_RUN نه حذف gate |

پروژهٔ MP proprietary است؛ source یا prompt/code/data را به هیچ مدل/cloud/report/telemetry بیرونی با اتکا به عمومی‌بودن مخزن نفرست. این handoff مجوز egress یا redistrib جدید ایجاد نمی‌کند. نصب Semgrep CE با cloud/Pro rules یا login یکی نیست؛ rules محلی و metrics خاموش در محدودهٔ مجاز استفاده شوند.

## ۲. ابزارهای مکمل ایزوله و pin‌شدهٔ این ZIP

نسخه‌ها در 2026-11-24 از registry/GitHub metadata بررسی شده‌اند، نه compatibility/security clearance. root مستقیم این ابزارها pin دقیق و lock دارند؛ dependencyهای transitive و optional binary هم بررسی و در محیط مقصد آزموده شوند.

| ابزار / نسخهٔ root | منبع / مجوز metadata | کدام نیاز و کدام گیت |
|---|---|---|
| `dependency-cruiser@18.9.0` | [sverweij/dependency-cruiser](https://github.com/sverweij/dependency-cruiser)، MIT | PWA-10/11؛ browser/Electron boundary و circular import؛ قانون فقط بعد از positive/negative fixture gate است |
| `knip@6.48.0` | [webpro-nl/knip](https://github.com/webpro-nl/knip)، ISC | کشف dead/unreferenced کاندید در Studio؛ نتیجه دستور حذف خودکار فایل/صفحه/native نیست |
| `@playwright/test@1.65.1` | [microsoft/playwright](https://github.com/microsoft/playwright)، Apache-2.0 | PWA-11/20/50/51/53؛ browser/API/E2E و PWA lifecycle؛ browser binary جدا و اجازه‌دار |
| `@axe-core/playwright@4.14.0` | [dequelabs/axe-core](https://github.com/dequelabs/axe-core)، MPL-2.0 برای هسته؛ adapter مجوز خودش | PWA-13/47/52؛ axe بخشی از a11y، نه جای keyboard/focus/device/screen reader review |
| `openapi-typescript@7.13.0` | [openapi-ts/openapi-typescript](https://github.com/openapi-ts/openapi-typescript)، MIT | PWA-01/24؛ type generation فقط از **OpenAPI واقعی و مصوب**؛ routes.json این بسته OpenAPI نیست |
| `typescript@5.6.3` | [microsoft/TypeScript](https://github.com/microsoft/TypeScript)، Apache-2.0 | سازگاری ابزار بررسی؛ compiler محصول از dependency خودش استفاده کند، نه جایگزینی silent |
| `semgrep==1.186.0` | [semgrep/semgrep](https://github.com/semgrep/semgrep)، شرایط بالا | pin محیط اختیاری جدا؛ نسخهٔ فعلی CI را در PWA-04 reconcile کن، نه تحمیل این نسخه به CI |
| `@viz-js/viz@3.31.0` + `sharp@0.35.5` | [viz-js/viz](https://github.com/viz-js/viz) MIT؛ [lovell/sharp](https://github.com/lovell/sharp) Apache-2.0 | **فقط مستندات** DOT→SVG→PNG؛ همان خانواده/نسخهٔ ابزار Graphviz موجود در MP pin مرجع؛ بدون Chromium/Mermaid نصب جدید برای renderer |

محیط ابزار Node این بسته: Node `>=22.19.0 <23`، pin ترجیحی `.node-version` = `22.22.3`؛ `npm@10.9.8`. Node 22.22.3/Python 3.11.2 در ساخت این handoff دیده شده‌اند؛ این عدد انتخاب SDK محصول یا تعهد سازگاری همهٔ toolها نیست.

### نصبِ انتخابی ابزار Node — نه در runtime

فقط اگر کارت واقعاً نیاز داشت و package/lifecycle/lock بازرسی شد:

```bash
# HANDOFF = ریشهٔ ZIP استخراج‌شده؛ آن را به مسیر واقعی تنظیم کن
cd "$HANDOFF/tooling/node"
node --version
npm --version
npm ci --ignore-scripts --no-audit --no-fund
```

root packageها lifecycle تعریف نکرده‌اند؛ `--ignore-scripts` lifecycleهای transitive را هم اجرا نمی‌کند. ابزار دارای native binding ممکن است با این سیاست کار نکند؛ gap محیط را ثبت و binary/lifecycle را بازرسی و جداگانه مجاز کن، نه اینکه blind policy را حذف کنی. **در این تحویل برای این پوشه فقط lock update و `npm ci --dry-run --ignore-scripts --no-audit --no-fund` اجرا شده است؛ dry-run نصب ابزار نیست.**

### کاربرد نمونه پس از تعریف قرارداد و نصبِ مجاز

```bash
TOOLS="$HANDOFF/tooling/node/node_modules/.bin"
cd "$MP_REPO/mp-app/studio"
"$TOOLS/depcruise" --help
"$TOOLS/depcruise" --config "$HANDOFF/config/dependency-cruiser.cjs" src
"$TOOLS/knip" --help
"$TOOLS/knip" --config "$HANDOFF/config/knip.example.json"
"$TOOLS/playwright" --help
```

این مثال‌ها روی MP اجرا نشده‌اند. configها باید با entrypoint/plugin/alias واقعی Studio و مثبت/منفی کنترل شوند؛ خروجی clean از configی که چیزی را scan نمی‌کند gate نیست. testهای Playwright و axe با source/test contract در کارت ساخته/بازاستفاده شوند؛ این ZIP suite E2E محصول را جعل نمی‌کند. `playwright test --list` فقط discovery است؛ browser/SW test باید واقعاً اجرا شود. نصب browser ممکن است CDN و library سیستم بخواهد؛ binary را از منبع تأییدشده و hash معتبر با مجوز محیط آماده کن، نه دانلود مخفی یا `--no-sandbox` به‌عنوان سیاست تولید.

### SAST اختیاری جدا از backend

```bash
python3.11 -m venv "$HANDOFF/.venv-audit"
"$HANDOFF/.venv-audit/bin/python" -m pip install -r "$HANDOFF/tooling/requirements-audit.txt"
cd "$MP_REPO"
SEMGREP_SEND_METRICS=off "$HANDOFF/.venv-audit/bin/semgrep" \
  --metrics=off --config=.semgrep/project-rules.yml --error \
  --exclude=.venv --exclude=node_modules --exclude=__pycache__ mp-app
```

این نصب/scan در تحویل v2 اجرا نشده است. در CI فعلی MP نیز Semgrep venv جدا دارد تا با dependencyهای backend تعارض نکند. `config/semgrep-pwa.example.yml` فقط یک قانون نمونهٔ loopback URL است، نه قواعد کامل امنیت/مجوز/cache؛ قبل از gate شدن تست true/false-positive لازم دارد. هیچ upload/login/remote rules/cloud فعال نکن مگر مجاز.

## ۳. baseline واقعی محصول — دستورهای موجود، نه نتیجهٔ اجرای این تحویل

قبل از اجرای هر script، source و fixture/network/DB هدف را بخوان؛ قرارداد همین کارت باید اجازه دهد. پکیج‌های محصول با lock/constraints خودشان نصب شوند. به‌جای fallback `npm install` که lock را تغییر می‌دهد، شکست `npm ci` را تشخیص بده؛ gate یا lock را بی‌دلیل عوض نکن.

```bash
# Studio: scripts در package.json مرجع وجود دارند
cd "$MP_REPO/mp-app/studio"
npm ci --ignore-scripts --no-audit --no-fund
npm run lint
npm test
npm run build

# backend: فقط در venv/test DB مصنوعی و بعد از خواندن script؛ نسخه‌ها از constraints جاری
cd "$MP_REPO/mp-app/backend"
ruff check --select E,F,W,I,N,UP,B,SIM,DTZ,TRY400,S --ignore E501 .
ruff format --check .
bash scripts/coverage_run.sh

# docs gate محصول، نه gate این ZIP
cd "$MP_REPO"
python3 scripts/docs_gate.py
```

نصب backend طبق CI مرجع از root محصول `pip install -c mp-app/backend/requirements.txt -e "mp-app/backend[dev]"` در venv مجاز است؛ این فایل handoff آن را خودکار اجرا نمی‌کند. runها cwd/SHA/version/exit/count/skips/CI ID می‌خواهند. `ci.yml` بعضی گزارش‌های تشخیصی non-blocking دارد؛ `|| true` یا output قدیمی را به عنوان PASS استفاده نکن. thresholdها/گیت‌ها از workflow و script فعلی استخراج شوند، نه عدد کلی تاریخیِ Finn.

Flutter/Android: از jobهای جاری و SDK pin‌شدهٔ همان workflow استفاده کن؛ در pin مرجع job `Client — pinned SDK · format gate · Android debug compile` و `web.yml` Flutter Web هستند. تکرار فرمان scaffold مربوط به Flutter Web برای ساخت React لازم نیست؛ حذف/تعویض این jobها هم مجاز نیست. local/device/CI شواهد جدا دارند.

## ۴. ترسیم مستندات این بسته — تنها نصب واقعیِ ابزار کمکی در ساخت v2

در MP pin مرجع `tools/graphviz-renderer/package.json` همین نسخه‌های Viz/Sharp را دارد. ابزار موازی heavyweight نصب نمی‌کنیم. برای بازتولید **فقط تصاویر این handoff**:

```bash
cd "$HANDOFF/tooling/diagram"
npm ci --ignore-scripts --no-audit --no-fund
cd "$HANDOFF"
node scripts/render_diagram.mjs diagrams/PWA_Finn_Loop_Flow.fa.dot diagrams/PWA_Finn_Loop_Flow.fa.png 4200
node scripts/render_diagram.mjs diagrams/PWA_50_Microloops.fa.dot diagrams/PWA_50_Microloops.fa.png 5200
```

PNG و SVG تولید می‌شوند. `DejaVu Sans` یا فونت فارسی مجازِ نصب‌شده لازم است؛ font/binary همراه ZIP توزیع نشده. Mermaidهای کنار تصاویر، منبع قابل‌ویرایشِ هم‌معنا هستند؛ PNG/SVG این نسخه از **DOT** ساخته می‌شوند، نه ادعای رندر Mermaid. renderer اجازهٔ خواندن/نوشتن symlink یا overwrite فایل خارج diagrams نمی‌دهد. در این تحویل نصب واقعی ۱۲ package وابستهٔ renderer با lifecycle خاموش و اجرای Viz/Sharp انجام شد؛ ابزارهای پوشهٔ `tooling/node` همچنان نصب/اجرا نشده‌اند.

### بررسی اختیاریِ فقط HTML همین handoff

برای کیفیت خود تحویل، در scratch جدا `playwright-core@1.65.1` و بستهٔ مرورگر `@sparticuz/chromium@153.0.0` از npm با lifecycle خاموش نصب شدند (۲۰ package). منبع wrapper مرورگر [Sparticuz/chromium](https://github.com/Sparticuz/chromium) و metadata مجوزش MIT است؛ Chromium و library/fontهای همراه شرایط مستقل خود را دارند. binaryها، libraryهای استخراج‌شده و node_modules در ZIP/Git نیستند و system/global package نصب نشده است.

[گزارش پالایش‌شده](references/HANDOFF_HTML_SMOKE.json) به hash همین HTML و [recipe متنی اجرا](references/HANDOFF_HTML_SMOKE.recipe.mjs.txt) متصل است. فقط HTML محلی و ساختهٔ خودمان در context آفلاین با HTTP abort و SW مسدود خوانده شد؛ این test محصول MP یا نصب PWA نیست. `--no-sandbox` محدودیت sandbox این smoke است، نه سیاست امنیت محصول و نه مجوز خواندن HTML نامطمئن.

بازتولید اختیاری فقط در محیط Linux مجاز با فونت فارسی و packageهای بررسی‌شده؛ همهٔ مسیرها را به absolute واقعی تنظیم کن:

```bash
SCRATCH="$HANDOFF/.cache/html-smoke"
mkdir -p "$SCRATCH/tmp"
cp "$HANDOFF/references/HANDOFF_HTML_SMOKE.recipe.mjs.txt" "$SCRATCH/smoke.mjs"
npm install --prefix "$SCRATCH" --ignore-scripts --no-audit --no-fund --save-exact \
  @sparticuz/chromium@153.0.0 playwright-core@1.65.1
cd "$SCRATCH"
TMPDIR="$SCRATCH/tmp" DOC_HANDOFF="$HANDOFF" node smoke.mjs
```

recipe فقط فایل محلی تحویل را می‌خواند و گزارش همان تحویل را می‌نویسد؛ از مسیر MP/backend استفاده نکن. library/font/browser استخراج فقط زیر TMPDIR تعیین‌شده است؛ در اجرای واقعی fontconfig به `/etc/fonts` مجاز محلی اشاره کرد. viewportهای 1280×920، 390×844 و 320×780 فقط responsive document smoke هستند؛ **نه دستگاه واقعی، نه accessibility certification، نه review مستقل و نه browser E2E محصول**. نصب binary مرورگر از این مثال پیش‌نیاز هیچ loop محصولی نیست.

## ۵. ابزارهایی که پیش‌فرض نصب نمی‌شوند

| ابزار/خانواده | تصمیم این طرح |
|---|---|
| ECC | در MP از 2026-11-19 حذف شده؛ نصب/فراخوانی تاریخی آن اجرا نشود |
| Spec Kit | فقط pilot مشخص برای کیفیت spec با بررسی overlap Finn؛ install-all لازم نیست؛ [github/spec-kit](https://github.com/github/spec-kit) |
| Container Use | فقط اگر نیاز isolation با ابزار موجود حل نشد و daemon/network/secret scope روشن بود؛ [dagger/container-use](https://github.com/dagger/container-use) |
| AgentLint | هویت/repository/version دقیق در ورودی مشخص نیست؛ انتخاب پروژهٔ هم‌نام یا دستور نصب حدسی ممنوع؛ در صورت نیاز proposal جدا |
| in-toto | فقط برای release attestation نیاز مستقل؛ SHA-bound evidence در Finn حذف نمی‌شود؛ [in-toto/in-toto](https://github.com/in-toto/in-toto) |
| Promptfoo | فقط اگر محصول LLM scope واقعاً داشته باشد و dataset/egress مجاز باشد؛ [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo) |
| Woodpecker / CI دوم | تا توجیه gap در Actions، موازی نصب نشود |
| LangGraph / OpenHands / orchestrator تازه | Finn با آن‌ها جایگزین نشود؛ نصبشان تضمین review یا permission نیست |
| Langfuse / trace ابری | با داده/trace حساس و D-08 باز، پیش‌فرض نیست؛ secret/health/chat/code egress ممنوع |
| vite-plugin-pwa / Workbox | SW موجود اول ممیزی شود؛ افزودن plugin یا auto-cache پیش‌فرض، راه‌حل خودکار PWA-15 نیست |
| k6 / OSV Scanner / Lighthouse CI | فقط اگر کارت نیاز مصوب load/supply-chain/performance داشت، منبع/مجوز/binary/hash/target جدا بررسی؛ نصب/اجرای این تحویل نیست؛ catalog metadata مجوز نیست |

catalogهای [references](references/README.fa.md) منبع و license metadata را نگه می‌دارند؛ برخی نام‌های تاریخی/اختیاری صرفاً برای trace باقی‌اند و برنامهٔ نصب نیستند. نصب binary از release فقط پس از بررسی checksum/signature و معماری؛ فایل checksum از همان منشأ به‌تنهایی تضمین اصالت کامل نیست. هیچ system/global install یا dependency جدید محصول از این متن مجوز نمی‌گیرد.
