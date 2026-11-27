# INV-03 — crosswalk صفحات کارکنان (بازسازیِ قابل‌تکرار)

> **وضعیت سند:** `PARTIAL / NOT_ACCEPTED` — تولیدشده با اسکریپت روی SHA زیر.
> این سند پذیرش محصول یا اثبات مجوز نیست. ستون نقش، آینهٔ `roleNav.ts` است؛
> اثبات، فقط با اجرای `rbac.py` و تست منفی سمت سرور به دست می‌آید.

- SHA: `352781043ad2ba202d8b3b459df1ce7e3d914ef7` · branch: `main` · tracked-dirty: `False`
- `backend/api/routes.json` → `7f0333dfb92a5bb56514b7e003cc78370fc7e8fabe3a9a8b5342ccaab9a84cf8`
- `studio/src/lib/roleNav.ts` → `650ff74343af6e25010f6a07bab4de477d2ffefcee94be3923a200ed05d53220`
- `studio/src/lib/navigation.ts` → `71fa84e7d3d0ca190e3a79ab91cb43beff7d2b8743ccc71a598b6a3722b73172`
- `studio/src/stores/appStore.ts` → `bb10aa017b194cf1f6367153311b7fb9b2db2997f0b2f2de76182c0ecb663f18`
- صفحه‌های `PAGE_IDS`: **12** · با route: **12** · مسیرهای API سرور: **141**
- قواعد نقش پارس‌شده از `roleNav.ts`: **8**
- شمارش: `GAP=1` · `PARTIAL_REVIEW=11`

| # | صفحه | کامپوننت | route | نقش‌های UI | API مصرف‌شده/کل | call-site | اشارهٔ تستی | وضعیت | دلیل |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `dashboard` | `Dashboard.tsx` | `/staff/dashboard` | — | 3 / 4 | `api.ts` | `a11y.test.tsx`<br>`api.test.ts`<br>`authFlow.test.tsx`<br>`liveContract.test.ts`<br>`locustfile_full.py` | **PARTIAL_REVIEW** | route + نقش + call-site + اشارهٔ تستی پیدا شد؛ اثر نهایی/مجوز و مرور صفحه با data واقعیِ ساختگی انجام نشده |
| 2 | `members` | `Members.tsx` | `/staff/members` | admin, coach, manager, reception, super_admin | 3 / 11 | `AuthContext.tsx`<br>`api.ts` | `a11y.test.tsx`<br>`apiCoverage.test.ts`<br>`authFlow.test.tsx`<br>`locustfile_full.py`<br>`pwa.test.ts` | **PARTIAL_REVIEW** | route + نقش + call-site + اشارهٔ تستی پیدا شد؛ اثر نهایی/مجوز و مرور صفحه با data واقعیِ ساختگی انجام نشده |
| 3 | `programs` | `Programs.tsx` | `/staff/programs` | admin, coach, manager, member, super_admin | 2 / 10 | `api.ts` | `apiCoverage.test.ts`<br>`locustfile_full.py`<br>`test_axis_assessment_api.py`<br>`test_battle.py`<br>`test_e2e_adaptive_loop.py` | **PARTIAL_REVIEW** | route + نقش + call-site + اشارهٔ تستی پیدا شد؛ اثر نهایی/مجوز و مرور صفحه با data واقعیِ ساختگی انجام نشده |
| 4 | `nutrition` | `Nutrition.tsx` | `/staff/nutrition` | admin, coach, manager, member, super_admin | 3 / 9 | `api.ts` | `test_e2e_adaptive_loop.py`<br>`test_m49_adaptive_nutrition.py`<br>`test_m49_food_logging.py`<br>`test_m78_adaptive_nutrition_client.py`<br>`test_rbac.py` | **PARTIAL_REVIEW** | route + نقش + call-site + اشارهٔ تستی پیدا شد؛ اثر نهایی/مجوز و مرور صفحه با data واقعیِ ساختگی انجام نشده |
| 5 | `assessment` | `Assessment.tsx` | `/staff/assessment` | admin, coach, manager, member, super_admin | 3 / 8 | `api.ts` | `apiCoverage.test.ts`<br>`test_ai_kpis.py`<br>`test_api_contract.py`<br>`test_battle.py`<br>`test_e2e_adaptive_loop.py` | **PARTIAL_REVIEW** | route + نقش + call-site + اشارهٔ تستی پیدا شد؛ اثر نهایی/مجوز و مرور صفحه با data واقعیِ ساختگی انجام نشده |
| 6 | `chat` | `Chat.tsx` | `/staff/chat` | — | 1 / 3 | `api.ts` | `a11y.test.tsx`<br>`test_e2e_adaptive_loop.py`<br>`test_m51_chat.py` | **PARTIAL_REVIEW** | route + نقش + call-site + اشارهٔ تستی پیدا شد؛ اثر نهایی/مجوز و مرور صفحه با data واقعیِ ساختگی انجام نشده |
| 7 | `checkin` | `CheckIn.tsx` | `/staff/checkin` | — | 1 / 11 | `api.ts` | `a11y.test.tsx`<br>`locustfile_full.py`<br>`test_m45_checkin_feed.py`<br>`test_m46_security_matrix.py`<br>`test_m80_member_checkin_history.py` | **PARTIAL_REVIEW** | route + نقش + call-site + اشارهٔ تستی پیدا شد؛ اثر نهایی/مجوز و مرور صفحه با data واقعیِ ساختگی انجام نشده |
| 8 | `finance` | `Finance.tsx` | `/staff/finance` | admin, manager, super_admin | 4 / 21 | `api.ts` | `locustfile_full.py`<br>`paymentPanel.test.tsx`<br>`receiptQueue.test.tsx`<br>`test_api_contract.py`<br>`test_battle.py` | **PARTIAL_REVIEW** | route + نقش + call-site + اشارهٔ تستی پیدا شد؛ اثر نهایی/مجوز و مرور صفحه با data واقعیِ ساختگی انجام نشده |
| 9 | `expenses` | `Expenses.tsx` | `/staff/expenses` | admin, manager, super_admin | 1 / 3 | `api.ts` | `test_phase6c_expenses.py`<br>`test_phase8_release_sweep.py`<br>`test_qf06_expense_receipt.py`<br>`test_routes_effective_guards.py`<br>`test_wp24_rbac_decision_cache.py` | **PARTIAL_REVIEW** | route + نقش + call-site + اشارهٔ تستی پیدا شد؛ اثر نهایی/مجوز و مرور صفحه با data واقعیِ ساختگی انجام نشده |
| 10 | `analytics` | `Analytics.tsx` | `/staff/analytics` | admin, coach, manager, super_admin | 0 / 4 | — | — | **GAP** | هیچ call-site در Studio به 4 مسیر این دامنه اشاره نمی‌کند |
| 11 | `settings` | `Settings.tsx` | `/staff/settings` | admin, super_admin | 5 / 17 | `api.ts` | `a11y.test.tsx`<br>`api.test.ts`<br>`authFlow.test.tsx`<br>`liveContract.test.ts`<br>`locustfile_full.py` | **PARTIAL_REVIEW** | route + نقش + call-site + اشارهٔ تستی پیدا شد؛ اثر نهایی/مجوز و مرور صفحه با data واقعیِ ساختگی انجام نشده |
| 12 | `shop` | `Shop.tsx` | `/staff/shop` | — | 8 / 15 | `api.ts` | `apiCoverage.test.ts`<br>`test_m59_shop.py`<br>`test_phase2_shop_display.py`<br>`test_phase3_no_online_gateway.py`<br>`test_role_nav_parity.py` | **PARTIAL_REVIEW** | route + نقش + call-site + اشارهٔ تستی پیدا شد؛ اثر نهایی/مجوز و مرور صفحه با data واقعیِ ساختگی انجام نشده |

## چه چیزی این سند اثبات نمی‌کند

- نمایش درست صفحه با دادهٔ واقعی (fixture ساختگی) اجرا نشده است.
- مجوز سرور: نقش‌ها از `roleNav.ts` آمده‌اند؛ `rbac.py` اجرا و تست منفی نشده.
- تفکیک «مصرف‌کنندهٔ صفحهٔ کارکنان» از «مصرف‌کنندهٔ صفحهٔ عضو» در سطح فایل انجام
  شده، نه در سطح کامپوننت؛ برخی call-siteها مشترک‌اند.
- browser/device، screen reader و reviewer مستقل: اجرا نشده.

## بازتولید

```bash
git fetch origin && git checkout --detach origin/main
python3 scripts/inv03_staff_crosswalk.py --repo . --out evidence/$(date -u +%F)/INV-03/
```
