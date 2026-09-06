# 02 — طراحی پایگاه داده

> منبع حقیقت: `mp-app/backend/app/migrations/`.
> این سند از **DB زندهٔ ساخته‌شده در همین بازبینی** استخراج شده (`PRAGMA table_info` روی هر جدول)،
> نه از حافظه.

---

## 1. انتخاب موتور و دلیلش

**SQLite در حالت WAL**، تک‌فایل، روی PC باشگاه.

| چرا | جزئیات |
|-----|---------|
| Local-first (C1) | بدون سرور، بدون شبکه، بدون هزینهٔ ماهانه |
| پشتیبان‌گیری بی‌دردسر | یک فایل + WAL؛ کپی اتمی با `VACUUM INTO` |
| کارایی کافی | ۵۰ req/s با WAL روی SSD به‌راحتی |
| ریسک | نوشتن هم‌زمان تک‌نویسنده است — برای یک باشگاه مسئله نیست |

**پیکربندی الزامی روی هر اتصال** (پیاده‌شده در `app/db.py`):
```sql
PRAGMA foreign_keys = ON;   -- پیش‌فرض SQLite خاموش است؛ بدون این، ردیف یتیم می‌ماند
PRAGMA journal_mode = WAL;
```

### 🔴 سه PRAGMA که کم است — باید اضافه شود

```sql
PRAGMA busy_timeout = 5000;   -- بدون این، دو نوشتن هم‌زمان = SQLITE_BUSY فوری در پیک کیوسک
PRAGMA synchronous = NORMAL;  -- با WAL امن است و نوشتن را چند برابر سریع می‌کند
PRAGMA wal_autocheckpoint = 1000;
```
`busy_timeout` جدی‌ترین آن‌هاست: در پیک ساعت ۱۹، اسکن کیوسک و ثبت پرداخت پذیرش هم‌زمان
می‌شوند و بدون این تنظیم، یکی از آن‌ها ۵۰۰ می‌گیرد.

---

## 2. الگوی مشترک هر جدول

هر جدول دامنه‌ای این ستون‌های حسابرسی را **در ابتدا** دارد:

| ستون | نوع | نقش |
|------|-----|-----|
| `id` | INTEGER PK | کلید محلی |
| `gym_id` | INTEGER NOT NULL | مرزِ چنداجاره‌ای (multi-tenant) — هر کوئری باید فیلتر کند |
| `created_at` / `updated_at` | TEXT (ISO-8601 UTC) | زمان‌مهر |
| `deleted_at` | TEXT NULL | **حذف نرم** — پایهٔ tombstone برای sync |
| `rev` | INTEGER | شمارندهٔ نسخه — پایهٔ delta sync |

این پنج ستون همان چیزی است که sync، حسابرسی و بازیابی را ممکن می‌کند. **حذف سخت ممنوع است**
مگر در ابزار پاک‌سازی صریح مالک.

---

## 3. ۲۶ جدول — گروه‌بندی دامنه‌ای

### 3.1 هویت و سازمان
| جدول | ستون‌های کلیدی |
|------|------------------|
| `gyms` | `name`, `secret_key` |
| `staff` | `username`, `pin_hash`, `password_hash`, `role`, `full_name`, `active` |
| `members` | `membership_code`, `first_name`, `last_name`, `sex`, `birth_date`, `phone`, `photo_path`, `membership_exp`, `guardian_consent`, `pin_hash` |
| `member_trainer` | `member_id`, `trainer_id`, `primary_flag` |
| `devices` | `device_id`, `kind`, `label`, `last_seen`, `public_key` |

### 3.2 سلامت و محدودیت (قلب ایمنی محصول)
| جدول | ستون‌های کلیدی |
|------|------------------|
| `member_injuries` | `body_region`, `side`, `label`, `status`, `pain_0_10`, `onset`, `cleared`, `clinician_note`, `member_visible_note`, `requires_clearance` |
| `member_limitations` | `contraindicated_pattern`, `allowed_modification`, `note` |
| `exercise_contraindications` | `exercise_id`, `body_region`, `pattern`, `severity` |
| `consents` | `kind`, `version`, `signed_at`, `signature` |

**نکتهٔ طراحی مهم و درست:** `clinician_note` و `member_visible_note` جدا هستند.
یعنی مربی می‌تواند یادداشت بالینی بنویسد که ورزشکار هرگز نبیند — و ماسک سمت سرور
(`app/core/field_mask.py`) این را اعمال می‌کند. این تصمیم درستی است و باید حفظ شود.

### 3.3 سنجش و برنامه
| جدول | ستون‌های کلیدی |
|------|------------------|
| `body_assessments` | `protocol`, `equation`, `weight_kg`, `height_cm`, `age_years`, `sites_mm`, `sum_mm`, `body_density`, `body_fat_pct`, `fat_mass_kg`, `lean_mass_kg`, `classification`, `measured_by`, `payload` |
| `exercises` | `key`, `name_en`, `name_fa`, `category`, `equipment`, `pattern`, `primary_muscles`, `source`, `source_license` |
| `gym_equipment` | `name`, `category`, `count`, `available` |
| `training_programs` | `title`, `status`, `source`, `payload`, `judge_score`, `generated_by`, `approved_by`, `applied_at` |
| `nutrition_plans` | `bmr_kcal`, `tdee_kcal`, `protein_g`, `carbs_g`, `fat_g`, `payload` |

`exercises.source_license` یک ستون هوشمندانه است: هر حرکت مجوز مبدأش را حمل می‌کند،
پس ممیزی لایسنس (C9) با یک `SELECT DISTINCT` قابل انجام است، نه با حدس.

### 3.4 عملیات روزانه
| جدول | ستون‌های کلیدی |
|------|------------------|
| `attendance` | `member_id`, `checked_in`, `checked_out`, `method`, `qr_sig`, `staff_id` |
| `packages` | `name`, `duration_days`, `price_rial`, `active` |
| `payments` | `member_id`, `package_id`, `amount_rial`, `method`, `receipt_no`, `voided`, `staff_id` |
| `session_sets` | `exercise_key`, `set_index`, `weight_kg`, `reps`, `rir`, `logged_at` |
| `session_feedback` | `exercise_key`, `pain_flag`, `pain_0_10`, `note` |
| `workout_logs` | `session_date`, `payload`, `athlete_note` |
| `messages` | `from_staff_id`, `to_member_id`, `body`, `read_at` |
| `progress_photos` | `path`, `shot_kind`, `taken_at` |

### 3.5 زیرساخت
| جدول | نقش |
|------|------|
| `sync_log` | `device_id`, `direction`, `rev_from`, `rev_to`, `row_count`, `ok`, `detail` |
| `knowledge_packs_meta` | `pack_id`, `version`, `installed_at`, `checksum` |
| `audit_log` | `actor_staff_id`, `action`, `entity`, `entity_id`, `detail` |
| `schema_migrations` | `version`, `label`, `checksum`, `applied_at` |

---

## 4. 🔴 پول به‌صورت INTEGER — درست است، ولی نیمه‌کاره

`payments.amount_rial` عدد صحیح است (ریال، بدون اعشار) — **این تصمیم کاملاً درست است**؛
هرگز پول را float نکنید.

اما دو شکاف:
1. هیچ `CHECK (amount_rial > 0)` وجود ندارد.
2. `voided` بولین است، ولی **هیچ ردیف معکوس (reversal) ثبت نمی‌شود**. در حسابداری واقعی،
   ابطال باید یک ردیف جدید با مبلغ منفی و ارجاع به اصل باشد، نه تغییر ردیف قدیمی.
   وگرنه گزارش «درآمد ماه» بعد از ابطال، تاریخچه را بازنویسی می‌کند.

**اصلاح پیشنهادی (مهاجرت v004):**
```sql
ALTER TABLE payments ADD COLUMN reverses_payment_id INTEGER
  REFERENCES payments(id);
-- و در کد: ابطال = درج ردیف منفی، نه UPDATE voided=1
```

---

## 5. 🔴 `audit_log` ساخته شده ولی هرگز نوشته نمی‌شود

بررسی شد: `audit_log` فقط در فایل مهاجرت ظاهر می‌شود و **در هیچ repository نوشته نمی‌شود**.
یعنی جدول حسابرسی خالی است. برای محصولی که دادهٔ سلامتی و پول نگه می‌دارد، این نقص جدی است.

**اصلاح:** یک دکوراتور در لایهٔ repo:
```python
@audited(action="payment.create", entity="payments")
def create_payment(...): ...
```
حداقل این رویدادها باید ثبت شوند: ورود/خروج، ایجاد و ابطال پرداخت، تغییر مصدومیت،
اعمال برنامه، بازیابی پشتیبان، تغییر نقش کاربر.

---

## 6. ایندکس‌ها — چه هست و چه کم است

مهاجرت v001 با `_index()` ایندکس می‌سازد. برای بار هدف، این ایندکس‌های ترکیبی **الزامی** هستند:

```sql
CREATE INDEX idx_attendance_gym_day   ON attendance(gym_id, checked_in);
CREATE INDEX idx_payments_gym_created ON payments(gym_id, created_at);
CREATE INDEX idx_members_gym_code     ON members(gym_id, membership_code);
CREATE INDEX idx_injuries_member_st   ON member_injuries(member_id, status);
CREATE INDEX idx_sets_member_logged   ON session_sets(member_id, logged_at);
-- ایندکس sync: بدون این، delta sync کل جدول را می‌خواند
CREATE INDEX idx_<t>_gym_rev          ON <table>(gym_id, rev);
```
آخری باید روی **هر** جدول دامنه‌ای وجود داشته باشد، وگرنه sync با رشد داده کند می‌شود.

**یکتایی‌های الزامی:**
```sql
CREATE UNIQUE INDEX uq_members_code   ON members(gym_id, membership_code) WHERE deleted_at IS NULL;
CREATE UNIQUE INDEX uq_staff_user     ON staff(gym_id, username)         WHERE deleted_at IS NULL;
CREATE UNIQUE INDEX uq_payment_receipt ON payments(gym_id, receipt_no)   WHERE deleted_at IS NULL;
```
شرط `WHERE deleted_at IS NULL` مهم است: عضو حذف‌شده نباید کد عضویت را برای همیشه قفل کند.

---

## 7. مهاجرت‌ها

سه مهاجرت موجود: `v001_core`، `v002_member_pin`، `v003_workout_logs`.
جدول `schema_migrations` **checksum** دارد — طراحی خوبی است، چون تغییر بی‌سروصدای یک
مهاجرت اعمال‌شده را می‌گیرد.

### 🔴 شکاف: هیچ مهاجرتِ برگشتی (down) وجود ندارد
اگر نسخهٔ ۰.۲۱ روی DB مشتری اعمال شود و باگ داشته باشد، راه برگشتی جز بازیابی پشتیبان نیست.

**قانون از این پس:** هر مهاجرت باید `up()` و `down()` داشته باشد، و CI باید
`up → down → up` را روی یک DB با داده اجرا کند (سند ۰۸ §۴).

---

## 8. مدل همگام‌سازی (Sync)

مبنا: `rev` صعودی + tombstone (`deleted_at`).
```
Device A  ──GET /sync/delta?since=rev──▶  Core
          ◀── ردیف‌های rev > since (شامل حذف‌شده‌ها) ──
```
**حل تعارض:** اکنون «آخرین نوشتن برنده است» (LWW). برای دادهٔ سلامتی خطرناک است:
اگر مربی مصدومیت را «فعال» کند و دستگاه قدیمی‌تر «برطرف‌شده» بفرستد، فیلتر ایمنی از بین می‌رود.

**قانون پیشنهادی:** برای `member_injuries` و `training_programs`، تعارض = **merge محافظه‌کارانه**
(محدودکننده‌ترین حالت برنده است) + پرچم برای بازبینی انسانی. برای بقیه LWW کافی است.

---

## 9. معیار مهاجرت به PostgreSQL

SQLite تا این آستانه‌ها می‌ماند. عبور از **هر دو** یعنی وقت Postgres است:

| سنجه | آستانه |
|------|---------|
| باشگاه‌های همزمان روی یک نصب | > ۱ (چند شعبه با یک هسته) |
| نویسندهٔ هم‌زمان | > ۵ |
| حجم DB | > ۵ GB |
| نیاز به دسترسی از راه دور | خارج از LAN |

چون لایهٔ repo از SQLAlchemy Core استفاده می‌کند، مهاجرت عمدتاً مسئلهٔ
`AUTOINCREMENT`، `TEXT` تاریخ‌ها و PRAGMAهاست. **از امروز**: به‌جای `TEXT` برای تاریخ‌ها،
همه‌جا ISO-8601 UTC بنویسید (که اکنون درست انجام می‌شود ✅) تا مهاجرت بی‌درد باشد.
