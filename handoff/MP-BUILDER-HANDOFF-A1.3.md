# پیامِ دستی به بیلدر — الحاقیهٔ A1.3 (۲۰۲۶‑۱۱‑۲۱)

> این فایل **همان متنی** است که باید در نشستِ بیلدر / حلقهٔ `FINN-AUDIT-LOOP.md` کپی شود.
> **خودکفاست**: پیکربندی و اسکریپتِ پذیرش هر دو داخلِ خودِ پیام‌اند، پس به هیچ فایلِ
> بیرونی، پیوند یا دسترسیِ شبکه نیاز ندارد.

---

## ─── از اینجا کپی کن ───

# الحاقیهٔ A1.3 — چراغِ سبزِ WP ‏0.9 + پروتکلِ اجرای بی‌ناظر

## ۰ · سه خبر

1. **اختلاف‌ها بسته شد.** هر پنج موردی که گزارش کردی راستی‌آزمایی مستقل شد؛ در دو مورد
   **تو درست می‌گفتی و من غلط** (۱۰۴ قاعدهٔ متمایز، نه ۱۰۸ · `log.error` نه
   `logging.error`)، و در یک مورد **هر سه عدد درست بود** (`RUF100`). جزئیات: §۱.
2. **`WP 0.9` از `BLOCKED` خارج شد.** نقص از سمتِ من بود: متنِ §۲‑الف را *ارجاع* دادم
   و کپی نکردم. اکنون پیکربندیِ کامل داخلِ همین پیام است (§۵).
3. **الحاقیه به A1.3 رفت و «بخش ۹ · پروتکلِ اجرای بی‌ناظر» اضافه شد.** چون کار به
   حلقهٔ خودران منتقل شده، **هیچ عدد، یافته، گیت یا WP‌ای تغییر نکرده** — فقط قواعدِ
   رفتار در نبودِ ناظر صریح شده (§۳). خلاصهٔ اجراییِ §۹ همان §۳ این پیام است.

## ۱ · `RUF100` — اختلاف حل شد: این عدد **تابعِ پیکربندی** است

هر سه اندازه‌گیری روی `662ff88` با ruff ‏۰٫۱۷٫۶ و `--no-cache` تکرار شد:

| پیکربندیِ فعال | `RUF100` | چرا |
|---|---|---|
| `--select RUF100` **تنها** | **۷۲** | هیچ قاعدهٔ دیگری روشن نیست ⇒ ruff هر **۷۲** ‏`# noqa` کدبیس را «بلااثر» می‌شمارد |
| پیکربندیِ فعلیِ پروژه (۸ خانواده) + `--extend-select RUF100` | **۵۹** ← **همان عددی که تو گرفتی و درست بود** | ۱۳ مورد از آن ۷۲ تا برای قواعدی‌اند که در آن ۸ خانواده واقعاً fire می‌شوند ⇒ مؤثر‌اند |
| **پیکربندیِ پیشنهادی (۵۲ قاعده، §۵)** | **۳۹** | با روشن‌شدنِ `S`, `TRY`, `PLW`, `BLE` … بیست `noqa`ی که قبلاً بلااثر بودند **مؤثر** می‌شوند ⇒ ۵۹ − ۲۰ = ۳۹ |

**پیامد برای `BASELINE.md`:** آن «OPEN claim» را ببند و هر سه عدد را **با نامِ
پیکربندی‌شان** بنویس. ستونِ «قبل» برای `WP 0.9` = **۳۹**، و باید **پس از نصبِ
پیکربندی** سنجیده شود (نه پیش از آن).

**علتِ ریشه‌ای:** `RUF100` تنها قاعده‌ای است که مقدارش به `select`ِ فعال وابسته است.
ضمناً `--select` روی خطِ فرمان، `select`ِ پیکربندی را **جایگزین** می‌کند؛ برای افزودن
باید `--extend-select` بزنی. خطای من در نسخهٔ اولِ الحاقیه دقیقاً همین بود.

### ۱‑الف · آن ۲۰ `# noqa` که با پیکربندیِ جدید **مؤثر** می‌شوند — حذفشان ممنوع

```text
api/v1/monitoring.py:24,40,65       cache/store.py:65,74,83,92,103
modules/ai/router.py:28             modules/auth/router.py:56
modules/face_id/deep.py:74          modules/outbox/service.py:115
scripts/dast.py:81,98,115,176,187   scripts/deploy_gate.py:174
tests/integration/test_phase8_reports.py:79
tests/integration/test_qf10_period_report.py:73
```

`diff` دو فهرستِ `file:line` (۵۹ در برابر ۳۹) دقیقاً همین ۲۰ مورد را می‌دهد.
اسکریپتِ §۴ هر ۲۰ را به‌صورت `file:line` وارسی می‌کند و اگر یکی پاک شده باشد
`BLOCKED-NUMERIC` می‌دهد.

## ۲ · اعدادِ موردانتظار در هر مرحله (همه اندازه‌گیری‌شده، نه تخمینی)

| مرحله | کل یافته | قواعدِ متمایز | `RUF100` | `TRY400` | `DTZ011` | `C901` | `format --check` |
|---|---|---|---|---|---|---|---|
| گام ۱ — نصبِ **عیناً** همان پیکربندیِ §۵ | **۴۳۰** | **۵۲** | ۳۹ | ۶ | ۳ | ۱۵ | ۳۷۸ فایل already formatted |
| گام ۲ — افزودنِ `"ERA001",` به `ignore` | **۴۱۹** | **۵۱** | ۳۹ | ۶ | ۳ | ۱۵ | ۳۷۸ فایل |
| پس از `WP 2.6` (F‑29) | ثبتی | ثبتی | **۰** | **۰** | ۳ | ۱۵ | ۳۷۸ فایل |
| پس از `WP 3.6` (F‑28) | ثبتی | ثبتی | **۰** | **۰** | **۰** | ۱۵ | ۳۷۸ فایل |
| پس از `WP 4.5` (F‑22 + حذفِ ۴ `# noqa: S608`) | ثبتی | ثبتی | **۰** | **۰** | **۰** | ۱۵ | ۳۷۸ فایل |

«ثبتی» یعنی عددِ مطلقِ کل یافته در آن مراحل **گیت نیست** (رفعِ هر نقص ممکن است یک
قاعدهٔ تازه را فعال کند) — فقط صفرهای همان ردیف گیت‌اند. در `430` بودنِ عددِ گام ۱
نقشِ `per-file-ignores` تعیین‌کننده است، پس اگر ۴۳۰ نشد اول ببین آن بخش کامل منتقل شده.

**`C901` = ۱۵ با بدترین ۲۸ در `app/config.py:128`** متعلق به `F‑15` است (پرامپتِ اصلی)،
نه این سه WP؛ در اسکریپت `INFO` است نه گیت.

## ۳ · پروتکلِ اجرای بی‌ناظر (خلاصهٔ اجراییِ §۹ الحاقیه)

در حلقهٔ خودران، ابهام به **پرسش** تبدیل نمی‌شود، به **اقدامِ خودسرانه** تبدیل می‌شود؛
و ارزان‌ترین راهِ سبزکردنِ گیتِ ایستا، **ضعیف‌کردنِ خودِ گیت** است. پس:

### ۳‑۱ · سه سطحِ نتیجه

| سطح | یعنی | اقدامِ اجباری |
|---|---|---|
| `MATCH` | عدد = سند | ادامه بده؛ عدد را در `EXECUTION-LOG.md` بنویس |
| `BLOCKED-NUMERIC` | عدد فرق دارد ولی **رفتار** درست است (تست‌ها سبز) | همان WP را متوقف کن؛ بلوکِ §۳‑۵ را کامل بنویس؛ پیکربندی را دستکاری **نکن**؛ به WP مستقلِ بعدی برو (§۳‑۴) |
| `HARD-STOP` | به یکی از مواردِ §۳‑۳ رسیدی | آن کار را انجام **نده**؛ سؤالِ **بسته** را بنویس؛ به WP مستقلِ بعدی برو |

**`BLOCKED-NUMERIC` شکست نیست.** در همین ممیزی، ممیز پنج عددِ اشتباه نوشت و بیلدر با
اندازه‌گیریِ مستقل جلوی آنها ایستاد. اگر عددِ تو با این پیام فرق دارد، **عددِ تو معتبر
است به شرطِ ثبتِ عینیِ فرمان** (فرمانِ کامل + خروجیِ خام + `ruff --version` +
`git rev-parse HEAD`). آنچه هرگز مجاز نیست: تغییرِ پیکربندی یا پاک‌کردنِ `# noqa` برای
اینکه عدد به سند برسد.

### ۳‑۲ · ممنوع: سبزکردنِ گیت با سرکوب

در پیکربندیِ ruff **فقط دو تغییر** مجاز است: (۱) نصبِ **عیناً** همان متنِ §۵،
(۲) افزودنِ **یک** قلم به `ignore`: `"ERA001",`.

| ممنوع | چرا |
|---|---|
| هر `ignore` یا `per-file-ignores` تازه | ۴۳۰ بودنِ این عدد **نتیجهٔ** ignoreهای مستندِ فعلی است |
| کم‌کردنِ هر خانواده از `select` (مثلاً `S` یا `DTZ`) | همان گیتی را می‌کشد که `WP 0.9` برای ساختنش وجود دارد |
| بالا بردنِ `mccabe.max-complexity` از **۱۰** | بدترین تابع امروز ۲۸ است؛ سقف را جابه‌جا نکن، تابع را بشکن (`F‑15`) |
| `ruff check --fix --unsafe-fixes` (۲۱۰ مورد) | در این الحاقیه مجاز نیست؛ فقط **۴۷ رفعِ امن**، در commit جدا |
| غیرمسدودکننده‌کردنِ گیتِ CI برای عبور از آن | معادلِ خاموش‌کردنِ دودزدنِ ساختمان |
| حذف یا `skip` کردنِ تست برای سبزکردنِ suite | خطِ قرمزِ مطلق |

**دو فهرستِ مجازِ حذفِ `# noqa`:** (الف) آن ۳۹ `RUF100`ی که با پیکربندیِ ۵۲قاعده‌ای
بلااثر‌اند — **به‌جز** چهار `# noqa: S608` در
`db/migrations/versions/c3f01ab129e2_*.py:67,165,169,171` که فقط **پس از** رفعِ `F‑22`
پاک می‌شوند. (ب) آن ۲۰ موردِ §۱‑الف: **هرگز**.

### ۳‑۳ · `HARD-STOP` — بدونِ تأییدِ مالک انجام نده

1. هر تغییرِ **schema** یا migration تازه (به‌جز همان `F‑22` که در `WP 4.5` تعریف شده).
2. هر تغییرِ **رفتارِ محصولی**: تنها تصمیم‌های مجاز = پنج تصمیمِ پرامپتِ اصلی + `D‑6`
   و `D‑7`. تصمیمِ هشتم را از خودت نساز.
3. bump نسخهٔ هر وابستگی (**ruff باید روی `0.17.x` بماند** تا این اعداد معتبر باشند).
4. `force-push`، تغییرِ branch protection، یا ادغامِ PR بدونِ چهار رکنِ قانونِ ۳
   (پچ + تستِ رگرسیون + شاهدِ اجراییِ عددیِ قبل/بعد + به‌روزرسانیِ سند).
5. هر کاری که نیاز به **پرسیدن** دارد: سؤالِ بسته را بنویس و رد شو؛ منتظر نمان، حدس نزن.

### ۳‑۴ · وابستگی‌ها — یک بلوک نباید کلِ حلقه را بخواباند

`WP 2.6` و `WP 3.6` به نصبِ پیکربندی **وابسته نیستند**: گیتِ عددیِ هر دو با
`ruff check --no-cache --extend-select TRY400,DTZ011 .` سنجیده می‌شود (این `select`ِ
موجود را **جایگزین نمی‌کند**). پس اگر `WP 0.9` بلوک شد، حلقه را ادامه بده و فقط همان
یک WP را `BLOCKED` نگه دار. تنها وابستگیِ واقعیِ زنجیره‌ای این است:
`رفعِ F‑22` ← `حذفِ ۴×# noqa: S608` ← `روشن‌کردنِ خانوادهٔ S به‌صورت مسدودکننده`.

### ۳‑۵ · قالبِ رکورد در `EXECUTION-LOG.md` (برای هر WP، بدونِ فیلدِ خالی)

```text
WP: 0.9 گام ۱ · برچسب: addendum A1.3
commit: <sha>
فرمان‌ها (verbatim): <هر فرمانی که زدی، عیناً>
اسکریپتِ پذیرش: stage=<...> ⇒ <خروجیِ کاملِ جدول + PASS/ACTION>
عددِ قبل / بعد: 430,52 ⇒ 419,51  (یا هر چه خودت اندازه گرفتی)
نتیجهٔ تست‌ها: <pytest: N passed / M skipped> · <ruff format --check>
انحراف از سند: صفر | یا: <شمارهٔ ردیف + عددِ تو + فرمانت>
HARD-STOPهای برخوردشده: هیچ | یا: <مورد + سؤالِ بسته>
برچسب‌های تازه‌ای که این حلقه ساخت: هیچ | یا: <نامِ تازه> ≡ <نامِ سند>
```

اگر انحرافی نیست بنویس **«انحراف: صفر»** — سکوت مبهم است و در حلقهٔ بی‌ناظر خوانده نمی‌شود.

### ۳‑۶ · نام‌گذاری

هر برچسب یا عبارتِ تازه‌ای که حلقه می‌سازد باید **همان‌جا** با معادلِ سند نگاشته شود —
دقیقاً کاری که با `AD‑1 ≡ D‑6` و `AD‑2 ≡ D‑7` کردی و درست بود. نامِ بی‌نگاشت در
مرورِ بعدی غیرقابلِ ردیابی است.

### ۳‑۷ · پایانِ حلقه

یک گزارشِ نهایی با: (۱) جدولِ **۲۹ یافته × وضعیت** (`FIXED` / `BLOCKED-NUMERIC` /
`HARD-STOP` / `NOT-STARTED`) با commitِ هر `FIXED`؛ (۲) خروجیِ خامِ
`verify-addendum-gates.sh after-wp45` (باید `PASS` باشد)؛ (۳) فهرستِ `HARD-STOP`ها
به‌ترتیبِ اولویت، هرکدام با یک سؤالِ **بسته** (بله/خیر یا دو گزینهٔ مشخص)، نه سؤالِ باز؛
(۴) `sha256` بستهٔ شواهدِ تولیدشدهٔ خودت.

## ۴ · اسکریپتِ پذیرش — این را در `backend/verify-addendum-gates.sh` بگذار

روی `662ff88` با ruff ‏۰٫۱۷٫۶ **آزمون شده**: `before` ⇒ «گیت‌های نامنطبق: ۰ / PASS»
(۴۳۰/۵۲ · `RUF100` ۳۹ · `TRY400` ۶ · `DTZ011` ۳ · `C901` ۱۵ · `S310` در `app/sms.py` ۳
· ۳۷۸ فایل · ۲۰ `noqa` حاضر · ۴ `# noqa: S608` حاضر) و `after-era` ⇒ PASS (۴۱۹/۵۱).
**آزمون‌های منفی** روی درختِ رفع‌نشده: `after-wp26` ⇒ ۲ گیتِ نامنطق، `after-wp36` ⇒ ۴،
`after-wp45` ⇒ ۵، همه با exit=1. بدونِ نصبِ پیکربندی هم `before` ⇒ ۵ گیتِ نامنطبق،
که سیگنالِ «§۵ نصب نشده» است. پس گیت‌ها دندان دارند.

```bash
RUFF=/path/to/ruff ./verify-addendum-gates.sh before      # ⇒ 430/52
RUFF=/path/to/ruff ./verify-addendum-gates.sh after-era   # ⇒ 419/51
RUFF=/path/to/ruff ./verify-addendum-gates.sh after-wp26  # ⇒ TRY400=0, RUF100=0
RUFF=/path/to/ruff ./verify-addendum-gates.sh after-wp36  # ⇒ DTZ011=0, date.today()=0
RUFF=/path/to/ruff ./verify-addendum-gates.sh after-wp45  # ⇒ 4×`# noqa: S608`=0
```

`CFG=` را خالی بگذار اگر پیکربندی را داخلِ `backend/pyproject.toml` نصب کرده‌ای
(حالتِ درستِ نهایی). خروجیِ خامِ هر اجرا را **کامل** در `EXECUTION-LOG.md` بچسبان.

```bash
#!/usr/bin/env bash
# verify-addendum-gates.sh — گیت‌های عددیِ الحاقیهٔ A1.3 برای اجرای بی‌ناظر (حلقهٔ خودران)
#
# کاربرد:   RUFF=/path/to/ruff ./verify-addendum-gates.sh [before|after-era|after-wp26|after-wp36|after-wp45]
# محلِ اجرا: mp-app/backend   ·   نیازمندی: ruff 0.17.x (با نسخهٔ دیگر اعداد فرق می‌کنند)
# خروجی:     یک جدول + «PASS» یا «ACTION» + exit code (0 = همهٔ گیت‌ها منطبق)
#
# هر «موردانتظار» در این فایل روی commit 662ff88 با ruff 0.17.6 اندازه‌گیری شده است
# (۳۷۶ فایل، --no-cache). CFG را خالی بگذار اگر پیکربندی را در pyproject.toml نصب کرده‌ای؛
# در غیر این صورت CFG=/path/to/ruff-recommended.toml بده.
set -u
STAGE="${1:-before}"
RUFF="${RUFF:-ruff}"
CFG="${CFG:-}"
command -v "$RUFF" >/dev/null 2>&1 || { echo "FATAL: ruff پیدا نشد ⇒ RUFF=/path/to/ruff"; exit 2; }
CARG=(); [ -n "$CFG" ] && CARG=(--config "$CFG")
OUT="$(mktemp)"; trap 'rm -f "$OUT"' EXIT
$RUFF check --no-cache "${CARG[@]}" --output-format concise . >"$OUT" 2>&1

# ۲۰ `# noqa`ی که با پیکربندیِ جدید «مؤثر» می‌شوند و حذفشان ممنوع است (§۲‑الف)
KEEP20="api/v1/monitoring.py:24 api/v1/monitoring.py:40 api/v1/monitoring.py:65
cache/store.py:65 cache/store.py:74 cache/store.py:83 cache/store.py:92 cache/store.py:103
modules/ai/router.py:28 modules/auth/router.py:56 modules/face_id/deep.py:74
modules/outbox/service.py:115 scripts/dast.py:81 scripts/dast.py:98 scripts/dast.py:115
scripts/dast.py:176 scripts/dast.py:187 scripts/deploy_gate.py:174
tests/integration/test_phase8_reports.py:79 tests/integration/test_qf10_period_report.py:73"
# چهار `# noqa: S608` روی خطوطِ F‑22 — تا پیش از رفعِ F‑22 باید بمانند (§۵)
S608="db/migrations/versions/c3f01ab129e2_downstream_indexes.py:67"

fail=0
row() { # <نام> <موردانتظار> <واقعی> <gate|info>
  local n="$1" e="$2" a="$3" lvl="${4:-gate}" v="INFO"
  if [ "$lvl" = gate ]; then
    if [ "$e" = "$a" ]; then v="MATCH"; else v="BLOCKED-NUMERIC"; fail=$((fail+1)); fi
  fi
  printf '| %-32s | %10s | %10s | %s |\n' "$n" "$e" "$a" "$v"
}
cnt() { grep -c "$1" "$OUT"; }
present() { local f="${1%%:*}" l="${1##*:}"; [ -f "$f" ] && sed -n "${l}p" "$f" | grep -q '# noqa' && echo yes || echo no; }

echo "== stage=$STAGE  cwd=$(pwd)  head=$(git rev-parse --short HEAD 2>/dev/null || echo n/a)  ruff=$($RUFF --version | awk '{print $2}')"
echo "== cfg=${CFG:-<pyproject.toml نصب‌شده>}"
case "$STAGE" in before|after-era|after-wp26|after-wp36|after-wp45) ;; *) echo "FATAL: stage نامعتبر"; exit 2;; esac
echo "| گیت | موردانتظار | واقعی | نتیجه |"; echo "|---|---|---|---|"
RV="$($RUFF --version | awk '{print $2}')"
row "ruff نسخه (0.17 لازم است)" "0.17" "$(echo "$RV" | cut -d. -f1-2)" gate

case "$STAGE" in
  before)    exp_err=430; exp_rules=52 ;;
  after-era) exp_err=419; exp_rules=51 ;;
  *)         exp_err=""; exp_rules="" ;;
esac
act_err="$(grep -oE 'Found [0-9]+ error' "$OUT" | grep -oE '[0-9]+' | head -1)"
act_rules="$($RUFF check --no-cache "${CARG[@]}" --statistics . 2>/dev/null | awk '$2 ~ /^[A-Z]+[0-9]+$/{n++} END{print n+0}')"
if [ -n "$exp_err" ]; then row "کل یافته" "$exp_err" "${act_err:-0}" gate; row "قواعدِ متمایز" "$exp_rules" "$act_rules" gate
else row "کل یافته (ثبتی)" "-" "${act_err:-0}" info; row "قواعدِ متمایز (ثبتی)" "-" "$act_rules" info; fi

case "$STAGE" in after-wp26|after-wp36|after-wp45) exp_try=0 ;; *) exp_try=6 ;; esac
case "$STAGE" in after-wp36|after-wp45) exp_dtz=0 ;; *) exp_dtz=3 ;; esac
case "$STAGE" in before|after-era) exp_ruf=39 ;; *) exp_ruf=0 ;; esac
row "RUF100 (noqa بلااثر)" "$exp_ruf" "$(cnt RUF100)" gate
row "TRY400" "$exp_try" "$(cnt TRY400)" gate
row "DTZ011" "$exp_dtz" "$(cnt DTZ011)" gate
row "C901 (پیچیدگی)" "-" "$(cnt C901)" info
row "S310 در app/sms.py" "-" "$(grep -c 'app/sms.py.*S310' "$OUT")" info
row "format --check" "378 files" "$($RUFF format --no-cache "${CARG[@]}" --check . 2>&1 | grep -oE '[0-9]+ files already formatted' | head -1)" info

k=0; for pair in $KEEP20; do [ "$(present "$pair")" = yes ] && k=$((k+1)); done
row "۲۰ noqa ممنوع‌الحذف" "20" "$k" gate
s=0; for f in $(ls db/migrations/versions/c3f01ab129e2_*.py 2>/dev/null); do
  s=$((s + $(grep -c '# noqa: S608' "$f"))); done
case "$STAGE" in after-wp45) row "۴ noqa: S608 (پس از F‑22)" "0" "$s" gate ;;
             *)              row "۴ noqa: S608 (تا پیش از F‑22)" "4" "$s" gate ;; esac
if [ "$STAGE" = "after-wp36" ] || [ "$STAGE" = "after-wp45" ]; then
  row "date.today() در ۴ دایرکتوری" "0" "$(grep -rn 'date\.today()' modules app engine jobs 2>/dev/null | wc -l | tr -d ' ')" gate
  row "ENV TZ در infra" "-" "$(grep -rl 'TZ=' ../infra 2>/dev/null | wc -l | tr -d ' ')" info
fi
echo "== گیت‌های نامنطبق: $fail"
if [ "$fail" -eq 0 ]; then echo "PASS"
else echo "ACTION (§۹‑۱): همین WP را متوقف کن · بلوکِ §۹‑۶ را در EXECUTION-LOG.md بنویس · پیکربندی را دستکاری نکن · به WP مستقلِ بعدی برو."
fi
exit $((fail > 0))
```

## ۵ · پیکربندی — اگر §۲‑الف به دستت نرسیده بود، **همین** است

`sha256 = 6bafdba17d60db628197cf89aa4c65477025e0207bc3e1612612f2c2cdf72e5a` · ۴٬۹۷۳ بایت · ۷۱ خط.
این نسخه یک **کامنتِ اصلاح‌شده** دارد: کامنتِ قبلیِ `FBT` ادعا می‌کرد
`bank_verified: bool = False` را می‌گیرد، که غلط بود — آن آرگومان پشتِ `*` است
(keyword-only) در `modules/payments/manual_transfer_policy.py:52` ⇒ `FBT` آن را
**نمی‌گیرد** و آن هسته پیشاپیس درست طراحی شده. ۲۱ موردِ واقعیِ `FBT` و سه موردِ
مسیرِ پول/سبد خرید در همان کامنت نام برده شده‌اند.

```toml
# پیکربندی پیشنهادی ruff برای mp-app/backend
# مبنا: پیکربندی فعلی پروژه (۸ خانواده) + خانواده‌های باگ‌یاب که امروز خاموش‌اند.
# هر ignore دلیلِ مستند دارد. اندازه‌گیری‌شده با ruff 0.17.6 روی ۳۷۶ فایل.

line-length = 100
extend-exclude = [".venv"]
target-version = "py311"

[lint]
select = [
  # ── آنچه امروز روشن است و درست کار می‌کند ──────────────────────
  "E", "W", "F", "I", "N", "UP", "B", "SIM",

  # ── باگ‌یاب‌های واقعی که امروز خاموش‌اند ────────────────────────
  "DTZ",    # datetime بدون timezone ← ۳ باگ واقعی (تهران در برابر UTC)
  "ASYNC",  # فراخوانی مسدودکننده داخل تابع async
  "S",      # flake8-bandit داخل ruff (S105/S110/S112/S310/S603/S607/S608/S311)
  "BLE",    # except کور
  "TRY",    # tryceratops (TRY400 = از دست رفتن traceback)
  "LOG", "G",  # خطاهای لاگ‌کردن و قالب لاگ
  "C90",    # پیچیدگی mccabe ← جایگزین radon/lizard در گیتِ CI
  "FAST",   # قوانین اختصاصی FastAPI (FAST002 = وابستگی بدون Annotated)
  "SLF",    # دسترسی به عضو خصوصی (limiter._storage)
  "FBT",    # تلهٔ بولی در امضا — ۲۱ مورد، سه‌تایش در مسیرِ پول/سبد خرید:
           # modules/payments/router.py:329,362,364,366 · modules/payments/service.py:254
           # · modules/shop/router.py:126. توجه: bank_verified در
           # modules/payments/manual_transfer_policy.py:52 پشتِ * است (keyword-only)
           # ⇒ FBT آن را نمی‌گیرد و آن هسته پیشاپیس درست طراحی شده است.
  "ERA",    # کد کامنت‌شده (مرده) — ولی ۱۱/۱۱ یافته‌اش روی این کدبیس کاذب است:
           # security/rbac.py:146,161 و modules/population/gates.py:11 کامنتِ فارسی‌اند،
           # db/models/content.py:73 و modules/assessment/equations.py:14-19 مستندِ شکلِ داده.
           # در WP 0.9 این خانواده را به ignore منتقل کن ⇒ ۴۳۰ به ۴۱۹ می‌رسد.
  "T20",    # print
  "A",      # سایه‌زدن builtin
  "PERF", "PIE", "RET", "RSE", "FURB", "PTH", "SLOT",
  "PLC", "PLE", "PLW",   # pylint (عمداً بدون PLR2004 = magic-value)
  "TC", "ARG", "Q", "ISC", "EXE", "PGH", "YTT", "T10", "FIX", "TD",
  "RUF",    # شامل RUF100 = noqa‌های بلااثر

  # ── عمداً روشن نشدند (فاز ۲، اگر خواستی) ──────────────────────
  # "D"    → ۱٬۴۹۹ یافتهٔ docstring؛ ارزش دارد ولی یک پروژهٔ جداست
  # "ANN"  → ۱٬۲۵۹ یافتهٔ type-hint؛ mypy/pyright بهتر این کار را می‌کند
  # "PLR"  → ۹۴۴ مورد PLR2004 (magic value) بیشترش در تست‌ها
  # "COM"  → با `ruff format` تضاد دارد
  # "CPY"  → کپی‌رایت؛ بی‌ربط
  # "D"/"DOC" → مستندسازی؛ اختیاری
]
ignore = [
  "E501",                    # طول خط را formatter مدیریت می‌کند (همان تصمیم فعلی پروژه)
  "COM812", "ISC001",        # با `ruff format` تضاد رسمی دارند — هرگز همزمان روشن نشوند
  "RUF001", "RUF002", "RUF003",  # «ambiguous unicode»: ۱٬۴۹۵ یافتهٔ کاذب از متن فارسیِ پروژه
  "TRY003", "EM101", "EM102",    # پیامِ خطای فارسیِ inline الگوی عمدی پروژه است (۳۶۰+۳۰۹+۵۱ = ۷۲۰ یافتهٔ نویز)
  "PLC0415",                     # import تنبل؛ ۹۸۸ مورد، الگوی رایج و بی‌ضرر در این کدبیس
  "D203", "D213",                  # (اگر روزی "D" روشن شد) تضادهای شناخته‌شده
]

[lint.mccabe]
max-complexity = 10     # امروز ۱۵ تابع بالای این سقف‌اند؛ بدترین ۲۸

[lint.per-file-ignores]
"tests/**"          = ["S101", "SLF001", "ARG001", "ARG002", "FBT001", "S311", "PLR2004", "TD", "FIX"]
"scripts/**"        = ["T201", "S603", "S607", "S310", "FIX", "TD"]
"db/migrations/**"  = ["ERA001", "E402", "S608"]   # S608 باید با تصمیمِ F‑22 حذف شود، نه ignore
"eval/**"           = ["T201", "S310", "S603"]
"devtools/**"       = ["T201", "S310", "FAST002"]
"tests/load/**"     = ["S311", "T201", "PLR2004"]

[lint.isort]
# همان تصمیم درستِ فعلی پروژه (باگ CI ۲۰۲۶‑۱۱‑۱۵): صریح بماند تا نتیجه مستقل از محیط باشد
known-first-party = ["app", "api", "db", "engine", "modules", "security", "cache", "jobs", "eval"]
```

## ۶ · ترتیبِ اجباری و دو «دست نزن»

1. پیکربندیِ §۵ را **عیناً** بنویس (commit جدا) ⇒ اسکریپت با `stage=before` ⇒ `430/52` PASS.
2. `"ERA001",` را به `ignore` اضافه کن ⇒ `stage=after-era` ⇒ `419/51` PASS.
   (هر ۱۱ موردِ `ERA001` روی این کدبیس کامنتِ فارسیِ مستندساز است، نه کدِ کامنت‌شده؛
   تک‌تک با `sed -n` دیده شده‌اند: `security/rbac.py:146,161` ·
   `modules/population/gates.py:11` · `db/models/content.py:73` ·
   `modules/assessment/equations.py:14-19`.)
3. **`ruff check --fix` را هنوز نزن.** آن ۳۹ `RUF100` شاملِ چهار `# noqa: S608` روی
   خطوطِ `F‑22` هم می‌شود؛ حذفِ زودهنگامشان آخرین نشانهٔ آن نقص را پاک می‌کند.
4. `WP 2.6` (F‑29): `log.error` → `log.exception` فقط در `app/sms.py:66,69,72,99,102,105`.
   **دست نزن ۱:** `:58` و `:91` **بیرون از** `except`‌اند و `TRY400` روی آنها fire نمی‌شود؛
   تبدیلشان کنی ۲ لاگِ درست را خراب کرده‌ای. (نامِ درست `log.error` است، چون
   `app/sms.py:14` → `log = logging.getLogger("mp.sms")`؛ پیامِ عمومیِ ruff
   `logging.error` می‌گوید ولی کد `log.error` است.)
5. `WP 3.6` (F‑28): `today_in_shop_zone()` در `modules/axis_assessment/service.py:31` و
   `modules/nutrition/service.py:124,182` + `ENV TZ` در ایمیج (لایهٔ دوم) + تستِ مرزیِ
   ۰۰:۰۰–۰۳:۳۰. مرجعِ «امروز» = `settings.shop_timezone` (`D‑6`).
6. **۴۷ رفعِ امن** در commit جدا («chore(ruff): 47 safe autofixes»). **۲۱۰ unsafe را
   یکجا نزن.**
7. `WP 4.5` (F‑22) را طبقِ بخشِ ۵ الحاقیه رفع کن، **بعد** آن چهار `# noqa: S608` را پاک
   کن، و در `EXECUTION-LOG.md` بنویس که ruff `S608` این مورد را **نمی‌گیرد** (حتی با
   `--ignore-noqa`) ⇒ **semgrep تنها گیت است**.
8. گیتِ CI: `ruff check` + `ruff format --check`، هر دو SHA‑پین. مسدودکننده فقط برای
   `DTZ, TRY, ASYNC, S, BLE, LOG, C90, SLF001, PLW`؛ بقیه ابتدا non‑blocking.
   **دست نزن ۲:** تا `F‑22` رفع نشده، `S` را مسدودکننده نکن.

**چراغِ سبز:** `WP 0.9` را شروع کن. هر سه WP را می‌توانی در همین حلقه تا پایان ببری،
به شرطِ رعایتِ §۳.

## ─── تا اینجا کپی کن ───
