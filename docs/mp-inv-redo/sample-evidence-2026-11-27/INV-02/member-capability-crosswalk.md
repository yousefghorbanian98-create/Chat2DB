# INV-02 — crosswalk capability عضو (بازسازیِ قابل‌تکرار)

> **وضعیت سند:** `PARTIAL / NOT_ACCEPTED` — تولیدشده با اسکریپت روی SHA زیر.
> این سند پذیرش محصول، اثبات مجوز یا مجوز انتشار نیست. نسخهٔ ادعاشده در نشست
> پیشین هرگز push نشد؛ تنها راه معتبر، اجرای دوبارهٔ همین اسکریپت روی SHA تازه است.

- SHA: `352781043ad2ba202d8b3b459df1ce7e3d914ef7` · branch: `main` · tracked-dirty: `False` · untracked: `2`
- `backend/api/routes.json` → `7f0333dfb92a5bb56514b7e003cc78370fc7e8fabe3a9a8b5342ccaab9a84cf8`
- `backend/security/rbac.py` → `a8740f75b33e864e1a3990f4d77e2fa781f0c2105c133d9892a41ce63fdf9d2c`
- `studio/src/lib/navigation.ts` → `71fa84e7d3d0ca190e3a79ab91cb43beff7d2b8743ccc71a598b6a3722b73172`
- `studio/src/lib/api.ts` → `f5e977948640587ac5a9c0816c401b63246f4613de77504accfd563b1950af28`
- featureهای Flutter: **17** · مسیرهای API سرور: **141** · مسیرهای صدا‌زده‌شده در Studio: **47**
- شمارش: `GAP=4` · `PARTIAL_REVIEW=13`

**افسانهٔ وضعیت**

| وضعیت | معنا |
|---|---|
| `PARTIAL_REVIEW` | مسیر API + call-site واقعی + اشارهٔ تستی هر سه پیدا شد؛ مجوز/مالکیت اثبات نشده |
| `GAP` | یا call-site نیست، یا هیچ تستی همان مسیر را نام نمی‌برد |
| `BLOCKED` | مسیر API ادعایی در `routes.json` نیست، یا نقشهٔ دامنه تعریف نشده |
| `CURRENT` | **در این نسخه هرگز صادر نمی‌شود** — نیازمند تست منفی + اجرای واقعی |

> ستون «اشارهٔ تستی» یعنی فایل تستی همان مسیر را **نام می‌برد**؛ این شاهد اجرای
> تست یا قبولی آن نیست. ستون نقش‌ها هم از `routes.json` می‌آید، نه از اثبات.

| # | feature | Flutter | API مصرف‌شده / کل دامنه | call-site | اشارهٔ تستی | نقش‌های قرارداد | وضعیت | دلیل |
|---|---|---|---|---|---|---|---|---|
| 1 | `assessment14` | 2 فایل | 2 / 7 | `api.ts` | `test_api_contract.py`<br>`test_battle.py`<br>`test_e2e_adaptive_loop.py`<br>`test_e2e_dataflow.py` +5 | admin, coach, manager, member, super_admin | **PARTIAL_REVIEW** | مسیر + مصرف‌کننده + اشارهٔ تستی پیدا شد؛ مجوز/مالکیت با تست منفی اثبات نشده و اجرای تست در این اجرا انجام نشده است |
| 2 | `auth` | 1 فایل | 8 / 10 | `api.ts`<br>`session.ts` | `test_api_contract.py`<br>`test_m67_studio_auth.py`<br>`test_m82_phone_change.py`<br>`test_phase4_identity_session.py` +15 | admin, coach, manager, member, reception, super_admin | **PARTIAL_REVIEW** | مسیر + مصرف‌کننده + اشارهٔ تستی پیدا شد؛ مجوز/مالکیت با تست منفی اثبات نشده و اجرای تست در این اجرا انجام نشده است |
| 3 | `bodycomp` | 1 فایل | 2 / 8 | `api.ts` | `test_api_contract.py`<br>`test_battle.py`<br>`test_e2e_adaptive_loop.py`<br>`test_e2e_dataflow.py` +5 | admin, coach, manager, member, super_admin | **PARTIAL_REVIEW** | مسیر + مصرف‌کننده + اشارهٔ تستی پیدا شد؛ مجوز/مالکیت با تست منفی اثبات نشده و اجرای تست در این اجرا انجام نشده است |
| 4 | `chat` | 2 فایل | 1 / 3 | `api.ts` | `test_e2e_adaptive_loop.py`<br>`test_m51_chat.py`<br>`a11y.test.tsx` | admin, coach, manager, member, super_admin | **PARTIAL_REVIEW** | مسیر + مصرف‌کننده + اشارهٔ تستی پیدا شد؛ مجوز/مالکیت با تست منفی اثبات نشده و اجرای تست در این اجرا انجام نشده است |
| 5 | `checkin` | 2 فایل | 0 / 10 | — | — | — | **GAP** | Flutter 2 فایل دارد اما هیچ call-site در mp-app/studio/src به 10 مسیر این دامنه اشاره نمی‌کند |
| 6 | `classes` | 1 فایل | 1 / 3 | `ScheduleTimeline.tsx` | `test_classes_finance.py`<br>`test_e2e_dataflow.py`<br>`test_m59_shop.py`<br>`test_m74_class_cancel.py` +5 | admin, coach, manager, member, reception, super_admin | **PARTIAL_REVIEW** | مسیر + مصرف‌کننده + اشارهٔ تستی پیدا شد؛ مجوز/مالکیت با تست منفی اثبات نشده و اجرای تست در این اجرا انجام نشده است |
| 7 | `feedback` | 3 فایل | 2 / 10 | `api.ts` | `test_axis_assessment_api.py`<br>`test_battle.py`<br>`test_e2e_adaptive_loop.py`<br>`test_e2e_dataflow.py` +8 | admin, coach, manager, member, reception, super_admin | **PARTIAL_REVIEW** | مسیر + مصرف‌کننده + اشارهٔ تستی پیدا شد؛ مجوز/مالکیت با تست منفی اثبات نشده و اجرای تست در این اجرا انجام نشده است |
| 8 | `home` | 1 فایل | 1 / 11 | `AuthContext.tsx`<br>`api.ts` | `test_e2e_dataflow.py`<br>`test_m46_whoami.py`<br>`test_m67_studio_auth.py`<br>`test_m80_member_checkin_history.py` +12 | admin, coach, manager, member, reception, super_admin | **PARTIAL_REVIEW** | مسیر + مصرف‌کننده + اشارهٔ تستی پیدا شد؛ مجوز/مالکیت با تست منفی اثبات نشده و اجرای تست در این اجرا انجام نشده است |
| 9 | `intake` | 2 فایل | 0 / 3 | — | — | — | **GAP** | Flutter 2 فایل دارد اما هیچ call-site در mp-app/studio/src به 3 مسیر این دامنه اشاره نمی‌کند |
| 10 | `notifications` | 1 فایل | 0 / 4 | — | — | — | **GAP** | Flutter 1 فایل دارد اما هیچ call-site در mp-app/studio/src به 4 مسیر این دامنه اشاره نمی‌کند |
| 11 | `nutrition` | 2 فایل | 3 / 8 | `api.ts` | `test_e2e_adaptive_loop.py`<br>`test_m49_adaptive_nutrition.py`<br>`test_m49_food_logging.py`<br>`test_m78_adaptive_nutrition_client.py` +1 | admin, coach, manager, member, super_admin | **PARTIAL_REVIEW** | مسیر + مصرف‌کننده + اشارهٔ تستی پیدا شد؛ مجوز/مالکیت با تست منفی اثبات نشده و اجرای تست در این اجرا انجام نشده است |
| 12 | `profile` | 2 فایل | 4 / 10 | `AuthContext.tsx`<br>`api.ts`<br>`session.ts` | `test_e2e_dataflow.py`<br>`test_m46_whoami.py`<br>`test_m67_studio_auth.py`<br>`test_m80_member_checkin_history.py` +14 | admin, coach, manager, member, reception, super_admin | **PARTIAL_REVIEW** | مسیر + مصرف‌کننده + اشارهٔ تستی پیدا شد؛ مجوز/مالکیت با تست منفی اثبات نشده و اجرای تست در این اجرا انجام نشده است |
| 13 | `progress` | 1 فایل | 2 / 7 | `api.ts` | `test_api_contract.py`<br>`test_battle.py`<br>`test_e2e_adaptive_loop.py`<br>`test_e2e_dataflow.py` +5 | admin, coach, manager, member, super_admin | **PARTIAL_REVIEW** | مسیر + مصرف‌کننده + اشارهٔ تستی پیدا شد؛ مجوز/مالکیت با تست منفی اثبات نشده و اجرای تست در این اجرا انجام نشده است |
| 14 | `shell` | 1 فایل | 8 / 10 | `api.ts`<br>`session.ts` | `test_api_contract.py`<br>`test_m67_studio_auth.py`<br>`test_m82_phone_change.py`<br>`test_phase4_identity_session.py` +15 | admin, coach, manager, member, reception, super_admin | **PARTIAL_REVIEW** | مسیر + مصرف‌کننده + اشارهٔ تستی پیدا شد؛ مجوز/مالکیت با تست منفی اثبات نشده و اجرای تست در این اجرا انجام نشده است |
| 15 | `shop` | 3 فایل | 8 / 15 | `api.ts` | `test_m59_shop.py`<br>`test_phase2_shop_display.py`<br>`test_phase3_no_online_gateway.py`<br>`test_wp34_member_profile_required.py` +3 | admin, coach, manager, member, reception, super_admin | **PARTIAL_REVIEW** | مسیر + مصرف‌کننده + اشارهٔ تستی پیدا شد؛ مجوز/مالکیت با تست منفی اثبات نشده و اجرای تست در این اجرا انجام نشده است |
| 16 | `today` | 4 فایل | 0 / 4 | — | — | — | **GAP** | Flutter 4 فایل دارد اما هیچ call-site در mp-app/studio/src به 4 مسیر این دامنه اشاره نمی‌کند |
| 17 | `wallet` | 2 فایل | 4 / 25 | `api.ts` | `test_api_contract.py`<br>`test_battle.py`<br>`test_classes_finance.py`<br>`test_e2e_dataflow.py` +18 | admin, manager, member, reception, super_admin | **PARTIAL_REVIEW** | مسیر + مصرف‌کننده + اشارهٔ تستی پیدا شد؛ مجوز/مالکیت با تست منفی اثبات نشده و اجرای تست در این اجرا انجام نشده است |

## مسیرهای Studio (از `navigation.ts`)

```
/
/login
/member
/staff
/staff/${page}
```

## چه چیزی این سند اثبات نمی‌کند

- مجوز سمت سرور: `rbac.py`/`routes.json` شاهد قرارداد است، نه اثبات اجرا.
- مالکیت داده: هیچ تست منفی (عضو A → دادهٔ عضو B) در این اجرا انجام نشده.
- `/member` در `navigation.ts` یک مسیر رزروشدهٔ fail-closed است، نه صفحهٔ ساخته‌شده.
- نصب‌پذیری، offline، مرورگر/دستگاه واقعی و reviewer مستقل: اجرا نشده.

## بازتولید

```bash
git fetch origin && git checkout --detach origin/main   # یا SHA هدف
python3 scripts/inv02_member_crosswalk.py --repo . --out evidence/$(date -u +%F)/INV-02/
```
