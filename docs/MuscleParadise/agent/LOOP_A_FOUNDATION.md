# LOOP A — پایه و امنیت
## ۱۹ تسک · ~۲ هفته · **مسدودکننده: هیچ لوپ دیگری قبل از اتمام این شروع نمی‌شود**

> **چرا این لوپ اول است؟**
> پروژه یک PIN چهاررقمی **بدون هیچ محدودیت نرخی** دارد. ۱۰٬۰۰۰ حالت، روی LAN چند ثانیه.
> ساختن رابط کاربری زیبا روی سیستمی که در چند ثانیه شکسته می‌شود، بی‌معناست.

**مرجع:** [`../build/06_SECURITY_PRIVACY.md`](../build/06_SECURITY_PRIVACY.md) · [`../build/02_DATABASE_DESIGN.md`](../build/02_DATABASE_DESIGN.md)

---

## A-01 · محدودیت نرخ: هستهٔ شمارنده

| | |
|---|---|
| **هدف** | یک شمارندهٔ تلاش ناموفق با پنجرهٔ زمانی، مستقل از HTTP |
| **فایل‌ها** | `mp-app/backend/app/core/ratelimit.py` (جدید)، `tests/test_ratelimit.py` (جدید) |
| **مرجع** | build/06 §3 P0-1 |

**کار:**
ماژول خالص (بدون FastAPI — قانون C13) با این رابط:
```python
class AttemptLimiter:
    def check(self, key: str) -> None:      # اگر قفل است، RateLimitedError با seconds_left
    def record_failure(self, key: str) -> None
    def record_success(self, key: str) -> None   # صفر کردن شمارنده
```
سیاست تصاعدی: **۵ خطا → ۳۰ ثانیه · ۱۰ → ۵ دقیقه · ۲۰ → قفل تا باز کردن دستی**

**تست‌ها (قبل از کد بنویسید):**
- ۴ خطا → هنوز مجاز
- ۵ خطا → `RateLimitedError` با `seconds_left ≈ 30`
- بعد از انقضای پنجره → دوباره مجاز
- موفقیت → شمارنده صفر
- کلیدهای متفاوت مستقل‌اند
- ⚠️ **ساعت را فریز کنید** (`freezegun` یا تزریق `now`) — قانون T1

**verify:** `pytest tests/test_ratelimit.py -q` → exit 0

---

## A-02 · محدودیت نرخ: دوام در SQLite

| **فایل‌ها** | `app/migrations/v004_ratelimit.py`، `app/repo/ratelimit.py`، تست |
|---|---|

**کار:** جدول `auth_attempts(key, failures, locked_until, updated_at)`.
چرا دوام لازم است: ری‌استارت سرور نباید قفل را پاک کند، وگرنه مهاجم فقط منتظر ری‌استارت می‌ماند.

**verify:** `pytest tests/test_ratelimit.py tests/test_migrations.py -q`

---

## A-03 · اتصال محدودیت نرخ به مسیرهای ورود

| **فایل‌ها** | `app/routers/auth.py`، `tests/test_security.py` |
|---|---|

**کار:** در `/auth/pin` و `/auth/member-pin`:
- کلید = `(gym_id, username|membership_code, client_ip)`
- قبل از بررسی رمز → `check()`؛ اگر قفل → **۴۲۹** با هدر `Retry-After`
- شکست → `record_failure()` · موفقیت → `record_success()`

⚠️ **دقت:** پیام ۴۲۹ نباید فاش کند که کاربر وجود دارد یا نه. برای کاربر ناموجود هم همان رفتار.

**تست:** ۶ تلاش ناموفق → ششمی ۴۲۹ · هدر `Retry-After` موجود · کاربر دیگر تأثیر نمی‌گیرد

**verify:** `pytest tests/test_security.py -q && python -m app.export_openapi --yaml > ../openapi.yaml`

---

## A-04 · سیاست حداقلی PIN

| **فایل‌ها** | `app/core/security.py`، `app/schemas.py`، تست |
|---|---|

**کار:** تابع `validate_pin_strength(pin) -> None`. رد کردن:
- تکراری: `1111`, `0000`
- متوالی: `1234`, `4321`, `0123`
- ۲۰ PIN رایج (فهرست را در کد بنویسید با کامنت منبع)
- طول < ۴

اعمال در `/members/{id}/pin` و ساخت کارکنان. پیام خطای فارسی و قابل‌فهم.

**verify:** `pytest tests/test_security.py -q`

---

## A-05 · اجبار تغییر رمز مالک در اولین اجرا

| **فایل‌ها** | `app/bootstrap.py`، `app/routers/auth.py`، `app/migrations/v005_must_change_pin.py` |
|---|---|

**کار:** ستون `staff.must_change_pin`. اگر `1`:
- توکن صادر می‌شود ولی **فقط** مسیر تغییر رمز را باز می‌کند؛ بقیه ۴۰۳ با کد `MUST_CHANGE_PIN`
- بعد از تغییر موفق → `0`

**چرا:** رمز `1111` در متن عمومی منتشر شده است.

**verify:** `pytest tests/test_security.py tests/test_phase1_api.py -q`

---

## A-06 · دکوراتور `@audited`

| **فایل‌ها** | `app/core/audit.py` (جدید)، `app/repo/audit.py`، تست |
|---|---|

**کار:** `audit_log` ساخته شده ولی **صفر بار نوشته می‌شود** (بررسی شد).
```python
@audited(action="payment.create", entity="payments")
def create_payment(engine, *, actor, ...): ...
```
ثبت: `actor_staff_id`, `action`, `entity`, `entity_id`, `detail` (JSON، **بدون PHI**).

⚠️ نوشتن حسابرسی نباید عملیات اصلی را بشکند — اگر ثبت شکست خورد، لاگ کنید ولی تراکنش اصلی ادامه یابد.

**verify:** `pytest tests/test_audit.py -q`

---

## A-07 · اعمال حسابرسی روی رویدادهای حساس

| **فایل‌ها** | `app/repo/{payments,members,injuries,programs}.py`، `app/routers/{auth,backup}.py` |
|---|---|

**حداقل رویدادها:** ورود موفق/ناموفق · ایجاد و ابطال پرداخت · تغییر مصدومیت ·
اعمال برنامه · بازیابی پشتیبان · تغییر نقش · تغییر PIN

**تست:** برای هر رویداد، یک تست که یک ردیف در `audit_log` می‌سازد.

**verify:** `pytest -q --cov=app --cov-fail-under=85`

---

## A-08 · ابطال توکن

| **فایل‌ها** | `app/migrations/v006_revoked_tokens.py`، `app/auth/deps.py`، `app/routers/auth.py` |
|---|---|

**کار:** `jti` تولید می‌شود ولی ذخیره نمی‌شود → هیچ راه ابطالی نیست.
- جدول `revoked_tokens(jti, exp, revoked_at)`
- بررسی در `deps.py`
- `POST /auth/logout` (این توکن) و `POST /auth/logout-all` (همهٔ توکن‌های این کاربر)
- پاک‌سازی خودکار ردیف‌های منقضی

**verify:** `pytest tests/test_security.py -q` + توکن ابطال‌شده → ۴۰۱

---

## A-09 · هدرهای امنیتی HTTP

| **فایل‌ها** | `app/main.py`، `tests/test_security_headers.py` |
|---|---|

```
Content-Security-Policy: default-src 'self'; script-src 'self'; object-src 'none';
                         frame-ancestors 'none'; base-uri 'self'
X-Content-Type-Options: nosniff
Referrer-Policy: no-referrer
Permissions-Policy: camera=(self), microphone=(), geolocation=()
```
⚠️ `camera=(self)` لازم است — اسکن QR دوربین می‌خواهد.

**verify:** `pytest tests/test_security_headers.py -q`

---

## A-10 · رد کردن `*` در CORS تولید

| **فایل‌ها** | `app/config.py`، تست |
|---|---|

**کار:** اگر `MP_ENV=production` و `MP_CORS_ORIGINS='*'` → **خطای راه‌اندازی**، نه هشدار.

**verify:** `pytest tests/test_config.py -q`

---

## A-11 · محدودیت اندازهٔ بدنه

| **فایل‌ها** | `app/main.py`، تست |
|---|---|

**کار:** میان‌افزار: بدنهٔ > ۲ MB → **۴۱۳**. (عکس پیشرفت بعداً مسیر جدا با سقف خودش دارد.)

**verify:** `pytest tests/test_limits.py -q`

---

## A-12 · لاگ ساخت‌یافتهٔ JSON

| **فایل‌ها** | `app/core/logging.py` (جدید)، `app/main.py` |
|---|---|

```json
{"ts":"...","level":"ERROR","request_id":"...","route":"/api/v1/payments","code":"...","msg":"..."}
```
+ `RotatingFileHandler` ۱۰MB × ۵ (دیسک PC باشگاه پر می‌شود).
⚠️ **هرگز PIN، توکن یا PHI در لاگ ننویسید.** یک تست این را بسنجد.

**verify:** `pytest tests/test_logging.py -q`

---

## A-13 · مسیر `/ready`

| **فایل‌ها** | `app/routers/health.py`، تست |
|---|---|

**کار:** `/health` = زنده است. `/ready` = واقعاً کار می‌کند:
DB قابل نوشتن · مهاجرت‌ها به‌روز · فضای دیسک > ۵۰۰MB → وگرنه **۵۰۳** با دلیل.

**verify:** `pytest tests/test_health.py -q`

---

## A-14 · مهاجرت `down()`

| **فایل‌ها** | `app/migrations/base.py` + همهٔ فایل‌های مهاجرت |
|---|---|

**کار:** هر مهاجرت `down()` بگیرد. بدون این، بازگشت نسخه غیرممکن است.

**verify:** `pytest tests/test_migrations.py -q`

---

## A-15 · تست رفت‌وبرگشت مهاجرت

| **فایل‌ها** | `app/migrations/roundtrip_check.py` (جدید)، `tests/test_migrations.py` |
|---|---|

```python
db = seed_realistic_gym(members=50, payments=200)
before = checksum_all_tables(db)
migrate_up(db); migrate_down(db); migrate_up(db)
assert checksum_all_tables(db) == before
```
سپس به `.github/workflows/mp-ci.yml` اضافه کنید (job `migrations`).

**verify:** `python -m app.migrations.roundtrip_check` → exit 0

---

## A-16 · پشتیبان اتمی با `VACUUM INTO`

| **فایل‌ها** | `app/core/backup.py`، تست |
|---|---|

**کار:** کپی فایل SQLite حین نوشتن = پشتیبان خراب. از `VACUUM INTO` استفاده کنید.

**verify:** `pytest tests/test_backup.py -q`

---

## A-17 · پشتیبان خودکار ساعتی + چرخش

| **فایل‌ها** | `app/core/scheduler.py` (جدید)، `app/main.py`، تست |
|---|---|

**کار:** `asyncio` task هر ساعت → پشتیبان رمزشده → نگه‌داشتن ۳۰ نسخهٔ آخر.
RPO یک‌ساعتهٔ سند ۰۱ اکنون **تضمین نشده** است.

**verify:** `pytest tests/test_scheduler.py -q`

---

## A-18 · تست بازیابی خودکار

| **فایل‌ها** | `tests/test_backup.py` |
|---|---|

```python
# داده بریز → پشتیبان بگیر → DB را نابود کن → بازیابی → checksum مقایسه کن
```
**پشتیبانی که بازیابی‌اش آزموده نشده، پشتیبان نیست.**

**verify:** `pytest tests/test_backup.py -q`

---

## A-19 · رفع نقض لایه‌بندی در `health.py` 🔴

| | |
|---|---|
| **هدف** | دروازهٔ G5 را از قرمز به سبز ببرید |
| **فایل‌ها** | `app/routers/health.py`، `app/repo/health.py` (جدید)، تست |
| **مرجع** | قانون C13 |

**مشکل (تأییدشده با اجرا):**
```bash
$ grep -rl "^from sqlalchemy" mp-app/backend/app/routers/
mp-app/backend/app/routers/health.py     # ← نقض C13
```
`health.py` مستقیماً `from sqlalchemy import text` و `Engine` را import می‌کند.
روتر نباید SQL بنویسد — این کار `repo/` است.

**کار:** منطق کوئری را به `app/repo/health.py` منتقل کنید؛ روتر فقط آن را صدا بزند.
این تسک با A-13 (`/ready`) هم‌راستاست — می‌توانید هر دو را با هم انجام دهید.

**verify:**
```bash
! grep -rl "^from sqlalchemy\|^import sqlalchemy" mp-app/backend/app/routers/
pytest tests/test_health.py -q
```

> **توجه برای عامل:** تا وقتی A-19 تمام نشده، دروازهٔ **G5 قرمز است**.
> این یک بدهی شناخته‌شده از قبل است، نه چیزی که شما شکستید. آن را زود رفع کنید.

---

# معیار خروج LOOP A

```
□ ۱۹ تسک DONE (یا BLOCKED با دلیل مکتوب)
□ ۶ تلاش ناموفق ورود → ۴۲۹ (اثبات با curl زنده)
□ audit_log بعد از یک پرداخت آزمایشی، ردیف دارد
□ توکن ابطال‌شده → ۴۰۱
□ python -m app.migrations.roundtrip_check → exit 0
□ چرخهٔ پشتیبان→بازیابی در تست، بدون از دست رفتن داده
□ هر ۵ دروازه سبز
□ پوشش بک‌اند ≥ ۸۵٪ (اکنون ۹۰.۹٪ — نباید افت کند)
```

**عددی که این لوپ جابه‌جا می‌کند:**
`بدهی‌های امنیتی P0: ۳ → ۰` و `دروازه‌های CI: ۵ → ۷`
