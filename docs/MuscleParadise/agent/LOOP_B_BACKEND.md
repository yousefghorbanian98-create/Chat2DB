# LOOP B — بک‌اند
## ۲۴ تسک · ~۳ هفته · وابسته به LOOP A

**مرجع:** [`../build/05_BACKEND.md`](../build/05_BACKEND.md) · [`../build/03_API_DESIGN.md`](../build/03_API_DESIGN.md) · [`../build/02_DATABASE_DESIGN.md`](../build/02_DATABASE_DESIGN.md)
**پایه:** ۶٬۳۵۸ خط Python · ۲۷۶ تست · پوشش ۹۰.۹٪ · ۴۹ مسیر

---

# فاز B1 — قرارداد API (تسک ۰۱–۰۸)

## B-01 · صفحه‌بندی مبتنی بر cursor
| **فایل‌ها** | `app/core/pagination.py` (جدید)، `app/repo/members.py`، `app/routers/members.py` |
|---|---|

**مشکل:** `GET /members` **همه** را برمی‌گرداند. با ۲۰۰۰ عضو = چند MB روی گوشی.
**چرا cursor نه offset:** offset با درج مداوم، ردیف جا می‌اندازد.
```http
GET /api/v1/members?limit=50&cursor=eyJpZCI6MTIzfQ
→ { "items": [...], "next_cursor": "...", "has_more": true }
```
**verify:** `pytest tests/test_pagination.py -q` (تست: درج حین صفحه‌بندی، ردیف گم نشود)

## B-02 · صفحه‌بندی روی `/exercises`
با ۸۰۰+ حرکت (LOOP E) این حیاتی می‌شود. + فیلتر `bodyPart`، `equipment`، `search`.

## B-03 · پاکت خطای RFC 9457
| **فایل‌ها** | `app/core/errors.py` (جدید)، `app/main.py` |
|---|---|
```json
{ "type":"...", "title":"...", "status":422, "code":"INJURY_CONTRAINDICATION",
  "detail":"...", "request_id":"...", "fields":{...} }
```
`code` ماشین‌خوان و ثابت · `detail` قابل ترجمه. الان `detail` رشتهٔ آزاد فارسی است و
کلاینت نمی‌تواند رویش منطق بنویسد.

## B-04 · فهرست کدهای خطا
`app/core/error_codes.py` — همهٔ `code`ها در یک جا، با تست که هیچ کد تکراری نیست.

## B-05 · `Idempotency-Key`
| **فایل‌ها** | `app/core/idempotency.py`، `app/migrations/v007_idempotency.py` |
|---|---|
**مشکل:** دوبار زدن «ثبت پرداخت» یا تلاش دوبارهٔ شبکه = **دو پرداخت**.
کلید + پاسخ را ۲۴ ساعت نگه دارید؛ تکرار → همان پاسخ اصلی.
اعمال روی `POST /payments` و `POST /attendance/check-in`.

## B-06 · ETag و `304`
روی `/client/me/*`. Wi-Fi ضعیف باشگاه را به‌شدت سبک می‌کند.

## B-07 · ایندکس‌های ترکیبی
```sql
idx_attendance_gym_day · idx_payments_gym_created · idx_members_gym_code
idx_injuries_member_st · idx_sets_member_logged · idx_<t>_gym_rev (هر جدول)
```
آخری روی **هر** جدول دامنه‌ای — بدون آن sync با رشد داده کند می‌شود.

## B-08 · یکتایی جزئی
```sql
CREATE UNIQUE INDEX uq_members_code ON members(gym_id, membership_code) WHERE deleted_at IS NULL;
```
شرط `WHERE deleted_at IS NULL` مهم است: عضو حذف‌شده نباید کد را برای همیشه قفل کند.

---

# فاز B2 — درستی دامنه (تسک ۰۹–۱۴)

## B-09 · ابطال پرداخت به‌صورت ردیف معکوس
| **فایل‌ها** | `app/migrations/v008_payment_reversal.py`، `app/repo/payments.py` |
|---|---|
**مشکل:** `voided=1` یعنی گزارش «درآمد مرداد» بعد از ابطال در شهریور **عوض می‌شود**.
در حسابداری، ابطال = ردیف جدید با مبلغ منفی + `reverses_payment_id`.
**verify:** تست: درآمد ماه گذشته بعد از ابطال در ماه جاری **تغییر نکند**

## B-10 · `CHECK` روی مبالغ
`CHECK (amount_rial > 0)` و مشابه.

## B-11 · جدول طلایی فیلتر مصدومیت 🔴
| **فایل‌ها** | `tests/test_injury_filter.py` (جدید) |
|---|---|
**فیلتر مصدومیت قلب ایمنی محصول است (C5) و هیچ لنگر معلوم‌الجواب ندارد.**

| مصدومیت | حرکت | انتظار |
|---|---|---|
| زانوی راست حاد | اسکات با هالتر | مسدود |
| زانوی راست حاد | پرس سینه | مجاز |
| شانهٔ چپ مزمن | پرس سرشانه | مسدود |
| شانهٔ چپ برطرف‌شده | پرس سرشانه | مجاز |
| کمر + بدون رک | ددلیفت | مسدود (دوگانه) |
| زانو + نیاز به تأییدیه | هر حرکت پا | مسدود تا `cleared` |

هر ردیف یک تست. اگر روزی کسی منطق را «بهینه» کرد، این جدول جلویش را می‌گیرد.

## B-12 · اجبار رضایت‌نامه
بدون رضایت امضاشده → `POST /assessments` = **۴۲۲**.
زیر ۱۸ سال → `guardian_consent` اجباری.
**این ریسک حقوقی واقعی است** (آنالیز بدنی روی نوجوان بدون رضایت ولی).

## B-13 · تست ویژگی‌محور JP7
`hypothesis`: برای هر ورودی معتبر → `0 < %BF < 75` و `fat_mass + lean_mass == weight`.

## B-14 · تست همزمانی
۲۰ نخ هم‌زمان check-in و پرداخت → بدون `SQLITE_BUSY`، بدون داده مفقود.

---

# فاز B3 — قابلیت‌های ناقص (تسک ۱۵–۲۰)

## B-15 · API کتابخانهٔ حرکات با ویدیو
| **فایل‌ها** | `app/migrations/v009_exercise_media.py`، `app/routers/exercises.py` |
|---|---|
ستون‌های `video_male_path`, `video_female_path`, `thumbnail_path`,
`instructions`, `form_cues`, `common_mistakes`.
سرو ویدیو از Knowledge Pack با `Range` request (پخش تدریجی).

## B-16 · نصب‌کنندهٔ Knowledge Pack
| **فایل‌ها** | `app/core/knowledge_pack.py` (جدید)، `app/routers/packs.py` |
|---|---|
جدول `knowledge_packs_meta` از قبل هست ولی **هرگز استفاده نشده**.
نصب از zip محلی · **تأیید checksum** · نسخه‌بندی · حذف.
⚠️ همان محافظت path-traversal که در `updater.py` اعمال شد، اینجا هم لازم است.

## B-17 · گزارش‌های دوره‌ای
درآمد ماهانه/سالانه · نرخ ریزش · روند حضور · اعضای در معرض انقضا.

## B-18 · صادرات کامل داده
CSV و JSON — برای «حق قابلیت انتقال داده» (GDPR).

## B-19 · واردات CSV اعضا
معیار خروج v1.0 می‌گوید مربی باید ۵۰ عضو را از CSV وارد کند.
پیش‌نمایش قبل از درج + گزارش خطای سطر به سطر.

## B-20 · پیام‌رسانی مربی↔عضو
جدول `messages` هست، API نیست.

---

# فاز B4 — سخت‌سازی (تسک ۲۱–۲۴)

## B-21 · تأیید امضای به‌روزرسان
| **فایل‌ها** | `app/updater.py` |
|---|---|
🔴 اکنون بسته را **بدون تأیید امضا** اعمال می‌کند. با DNS دستکاری‌شده،
مسیر به‌روزرسانی = مسیر نصب بدافزار.

## B-22 · تست فهرست سفید n8n
```python
assert set(body) <= {"v","event","gym_id","member_id","days_left","at","sig","privacy"}
```
جلوگیری از اینکه روزی کسی «برای راحتی» نام عضو را اضافه کند.

## B-23 · تست یکپارچگی Ollama
مسیر AI فقط با mock تست شده. یک تست با مدل کوچک (`qwen2.5:0.5b`) در CI +
تست تزریق پرامپت (خروجی مخرب باید رد شود) + سقف زمان و توکن.

## B-24 · تست معماری
```python
def test_core_has_no_web_dependency():
    for f in Path("app/core").rglob("*.py"):
        assert "fastapi" not in f.read_text()
def test_routers_have_no_sql():
    for f in Path("app/routers").rglob("*.py"):
        assert "sqlalchemy" not in f.read_text()
```

---

# معیار خروج LOOP B
```
□ ۲۴ تسک DONE
□ /members با ۲۰۰۰ عضو → پاسخ < ۵۰ kB
□ دو بار POST با همان Idempotency-Key → یک ردیف
□ جدول طلایی مصدومیت: ۶/۶ سبز
□ درآمد ماه گذشته بعد از ابطال تغییر نکند
□ آنالیز بدون رضایت → ۴۲۲
□ ۲۰ نخ همزمان → بدون SQLITE_BUSY
□ openapi.yaml همگام
□ پوشش ≥ ۸۵٪
```
**عدد:** `مسیرها: ۴۹ → ~۶۵` · `ماژول کامل: ۹ → ۱۴`
