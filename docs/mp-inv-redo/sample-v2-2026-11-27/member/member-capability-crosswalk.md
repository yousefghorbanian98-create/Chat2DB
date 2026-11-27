# INV-02 — crosswalk عضو (v2)

> **وضعیت:** `PARTIAL / NOT_ACCEPTED`. این نسخه سه false-negative نسخهٔ اول را
> رفع می‌کند (تمپلیت `${base}`, alias نقش‌ها, مسیرهای پویا) — طبق یافته‌های
> `review.md` خودِ اجرای قبلی. هیچ ردیفی CURRENT نمی‌شود.

- SHA: `352781043ad2ba202d8b3b459df1ce7e3d914ef7` · branch: `main` · tracked-dirty: `False` · untracked: `1`
- `backend/api/routes.json` → `7f0333dfb92a5bb56514b7e003cc78370fc7e8fabe3a9a8b5342ccaab9a84cf8`
- `backend/security/rbac.py` → `a8740f75b33e864e1a3990f4d77e2fa781f0c2105c133d9892a41ce63fdf9d2c`
- `studio/src/lib/roleNav.ts` → `650ff74343af6e25010f6a07bab4de477d2ffefcee94be3923a200ed05d53220`
- `studio/src/lib/api.ts` → `f5e977948640587ac5a9c0816c401b63246f4613de77504accfd563b1950af28`
- `studio/src/lib/adminApi.ts` → `612cbd1e89a78301545f67c88264519a7c492d148ef44779050f50cc1327f2ce`
- `studio/src/lib/navigation.ts` → `71fa84e7d3d0ca190e3a79ab91cb43beff7d2b8743ccc71a598b6a3722b73172`
- call-site: `{'template-base': 28, 'helper': 57, 'literal': 0}` · پویا: **0**
- شمارش: `GAP=3` · `PARTIAL_REVIEW=14`

| وضعیت | معنا |
|---|---|
| `PARTIAL_REVIEW` | route/نقش + call-site + اشارهٔ تستی؛ مجوز اثبات نشده |
| `GAP` | call-site یا تست همان مسیر نیست |
| `DYNAMIC_UNCOVERED` | فقط call پویا؛ اسکنر استاتیک نمی‌تواند نگاشت کند — بررسی دستی |
| `BLOCKED` | مسیر/نقشهٔ دامنه وجود ندارد |
| `CURRENT` | **هرگز در این نسخه صادر نمی‌شود** |

| # | کلید | فایل | route | نقش‌ها (alias حل‌شده) | API مصرف‌شده/کل | call-site | پویای پوشش‌داده‌نشده | اشارهٔ تستی | وضعیت |
|---|---|---|---|---|---|---|---|---|---|
| 1 | `assessment14` | 2 فایل | — | — | 2 / 7 | `api.ts` | — | `apiCoverage.test.ts`<br>`test_api_contract.py`<br>`test_battle.py`<br>`test_e2e_adaptive_loop.py` | **PARTIAL_REVIEW** |
| 2 | `auth` | 1 فایل | — | — | 8 / 10 | `api.ts`<br>`session.ts` | — | `a11y.test.tsx`<br>`apiCoverage.test.ts`<br>`authFlow.test.tsx`<br>`deviceSessions.test.tsx` | **PARTIAL_REVIEW** |
| 3 | `bodycomp` | 1 فایل | — | — | 2 / 8 | `api.ts` | — | `apiCoverage.test.ts`<br>`test_api_contract.py`<br>`test_battle.py`<br>`test_e2e_adaptive_loop.py` | **PARTIAL_REVIEW** |
| 4 | `chat` | 2 فایل | — | super_admin, admin, manager, coach, reception, member | 1 / 3 | `api.ts` | — | `a11y.test.tsx`<br>`test_e2e_adaptive_loop.py`<br>`test_m51_chat.py` | **PARTIAL_REVIEW** |
| 5 | `checkin` | 2 فایل | — | super_admin, admin, manager, coach, reception, member | 1 / 12 | `api.ts` | — | `a11y.test.tsx`<br>`locustfile_full.py`<br>`test_m45_checkin_feed.py`<br>`test_m46_security_matrix.py` | **PARTIAL_REVIEW** |
| 6 | `classes` | 1 فایل | — | — | 1 / 3 | `ScheduleTimeline.tsx` | — | `a11y.test.tsx`<br>`authFlow.test.tsx`<br>`test_classes_finance.py`<br>`test_e2e_dataflow.py` | **PARTIAL_REVIEW** |
| 7 | `feedback` | 3 فایل | — | — | 2 / 10 | `api.ts` | — | `apiCoverage.test.ts`<br>`locustfile_full.py`<br>`test_axis_assessment_api.py`<br>`test_battle.py` | **PARTIAL_REVIEW** |
| 8 | `home` | 1 فایل | — | — | 1 / 11 | `AuthContext.tsx`<br>`api.ts` | — | `a11y.test.tsx`<br>`authFlow.test.tsx`<br>`locustfile_full.py`<br>`pwa.test.ts` | **PARTIAL_REVIEW** |
| 9 | `intake` | 2 فایل | — | — | 0 / 3 | — | — | — | **GAP** |
|  |  |  |  |  |  |  |  |  | ↳ هیچ call-site استاتیکی برای مسیرهای این دامنه نیست |
| 10 | `notifications` | 1 فایل | — | — | 0 / 4 | — | — | — | **GAP** |
|  |  |  |  |  |  |  |  |  | ↳ هیچ call-site استاتیکی برای مسیرهای این دامنه نیست |
| 11 | `nutrition` | 2 فایل | — | super_admin, admin, manager, coach, member | 3 / 8 | `api.ts` | — | `test_e2e_adaptive_loop.py`<br>`test_m49_adaptive_nutrition.py`<br>`test_m49_food_logging.py`<br>`test_m78_adaptive_nutrition_client.py` | **PARTIAL_REVIEW** |
| 12 | `profile` | 2 فایل | — | — | 4 / 10 | `AuthContext.tsx`<br>`api.ts`<br>`session.ts` | — | `a11y.test.tsx`<br>`authFlow.test.tsx`<br>`locustfile_full.py`<br>`phoneChange.test.tsx` | **PARTIAL_REVIEW** |
| 13 | `progress` | 1 فایل | — | — | 2 / 7 | `api.ts` | — | `apiCoverage.test.ts`<br>`test_api_contract.py`<br>`test_battle.py`<br>`test_e2e_adaptive_loop.py` | **PARTIAL_REVIEW** |
| 14 | `shell` | 1 فایل | — | — | 8 / 10 | `api.ts`<br>`session.ts` | — | `a11y.test.tsx`<br>`apiCoverage.test.ts`<br>`authFlow.test.tsx`<br>`deviceSessions.test.tsx` | **PARTIAL_REVIEW** |
| 15 | `shop` | 3 فایل | — | super_admin, admin, manager, coach, reception, member | 8 / 15 | `api.ts` | — | `apiCoverage.test.ts`<br>`test_m59_shop.py`<br>`test_phase2_shop_display.py`<br>`test_phase3_no_online_gateway.py` | **PARTIAL_REVIEW** |
| 16 | `today` | 4 فایل | — | — | 0 / 4 | — | — | — | **GAP** |
|  |  |  |  |  |  |  |  |  | ↳ هیچ call-site استاتیکی برای مسیرهای این دامنه نیست |
| 17 | `wallet` | 2 فایل | — | — | 4 / 25 | `api.ts` | — | `locustfile_full.py`<br>`paymentPanel.test.tsx`<br>`receiptQueue.test.tsx`<br>`test_api_contract.py` | **PARTIAL_REVIEW** |

## چه چیزی این نسخه هنوز اثبات نمی‌کند

- مجوز سمت سرور؛ `routes.json`/`rbac.py` شاهد قرارداد است، نه اجرا.
- مالکیت: تست منفی (عضو A → دادهٔ عضو B) در همین اجرا اجرا نشده.
- تمایز «مصرف‌کنندهٔ صفحهٔ عضو» از «پنل کارکنان»: فایل مشترک است (`api.ts`,
  `adminApi.ts`)؛ تفکیک کامپوننتی نیاز به مرور دستی دارد.
- مرورگر/دستگاه/نصب‌پذیری و reviewer مستقل.

## بازتولید

```bash
python3 scripts/crosswalk_v2.py --repo . --out evidence/$(date -u +%F)/INV-02 --kind member
```
