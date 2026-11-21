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
