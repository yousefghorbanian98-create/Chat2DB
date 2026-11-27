#!/usr/bin/env bash
# اجرای پاکت نجات INV-02/INV-03 روی یک SHA مشخص، با چک‌لیست push.
#
# استفاده (از ریشهٔ مخزن MP):
#     bash scripts/run-inv-redo.sh                 # SHA فعلی HEAD
#     bash scripts/run-inv-redo.sh <sha>           # SHA مشخص (پیشنهادی: origin/main)
#
# چه کاری می‌کند:
#   1) SHA را resolve و وضعیت dirty/untracked را چاپ می‌کند (بدون تغییر کار تو).
#   2) دو crosswalk را در evidence/<تاریخ>/INV-02 و INV-03 می‌سازد.
#   3) خروجی را چاپ می‌کند و **هیچ commit/push** انجام نمی‌دهد.
#
# چه کاری نمی‌کند: checkout/reset/clean، تغییر فایل‌های تو، push خودکار.
# اگر worktree dirty باشد، اسکریپت‌ها خودشان هشدار می‌دهند و خروجی به SHA نسبت داده نمی‌شود.

set -euo pipefail

TARGET_SHA="${1:-$(git rev-parse HEAD)}"
DATE_UTC="$(date -u +%F)"
OUT_ROOT="evidence/${DATE_UTC}"
REPO_ROOT="$(git rev-parse --show-toplevel)"
cd "$REPO_ROOT"

echo "== INV-REDO =================================================="
echo "repo      : $REPO_ROOT"
echo "target SHA: $TARGET_SHA"
echo "date(UTC) : $DATE_UTC"
echo "branch    : $(git rev-parse --abbrev-ref HEAD)"
echo "tracked∞  : $(git status --porcelain --untracked-files=no | wc -l) تغییر staged/unstaged"
echo "untracked : $(git status --porcelain | grep -c '^??' || true) فایل"
echo

if [ "$TARGET_SHA" != "$(git rev-parse HEAD)" ]; then
  echo "WARN: SHA هدف با HEAD فعلی یکی نیست."
  echo "      خروجی به کدِ چک‌اوت‌شده تعلق دارد، نه به SHA هدف."
  echo "      برای خروجی معتبر: git worktree add /tmp/inv-redo $TARGET_SHA && cd /tmp/inv-redo"
  echo
fi

for script in scripts/inv02_member_crosswalk.py scripts/inv03_staff_crosswalk.py; do
  if [ ! -f "$script" ]; then
    echo "MISSING: $script — فایل را از پاکت (docs/mp-inv-redo) کپی کن." >&2
    exit 4
  fi
done

python3 scripts/inv02_member_crosswalk.py --repo . --out "${OUT_ROOT}/INV-02"
echo
python3 scripts/inv03_staff_crosswalk.py --repo . --out "${OUT_ROOT}/INV-03"
echo

echo "== خروجی‌ها =================================================="
ls -1 "${OUT_ROOT}/INV-02" "${OUT_ROOT}/INV-03"
echo
echo "== قدم بعدی (دستی) ==========================================="
cat <<'EOF'
1) خروجی را با کد مقایسه کن؛ ردیف‌های GAP را تصمیم بگیر (در scope / defer).
2) فقط همین مسیرها را stage کن (هرگز git add -A):
     git add scripts/inv02_member_crosswalk.py scripts/inv03_staff_crosswalk.py \
             evidence/<تاریخ>/INV-02 evidence/<تاریخ>/INV-03
3) commit:
     git commit -m "INV-02/03: generated crosswalks — evidence: scripts/run-inv-redo.sh"
4) push به شاخهٔ نشست جاری (نه main):
     git push origin HEAD:arena/<session>-mp
5) تأیید وجود شاهد روی ریموت (بدون این، کار تمام نیست):
     git ls-remote origin | grep <session>
     # یا: gh api repos/:owner/:repo/contents/evidence/<تاریخ>/INV-02 --jq '.[].name'
6) در tracker فقط تا PARTIAL ارتقا بده، نه بیشتر.
EOF
