# 03 — طراحی API

> منبع حقیقت: `mp-app/openapi.yaml` (تولیدشده از کد با `app/export_openapi.py`).
> **۴۹ مسیر** روی `/api/v1` + `/health`. همهٔ مثال‌های این سند روی نمونهٔ زندهٔ همین بازبینی
> با `curl` اجرا و پاسخشان کپی شده.

---

## 1. اصول قرارداد

| اصل | اجرا |
|-----|------|
| نسخه در مسیر | `/api/v1/...` — شکستن قرارداد یعنی `/v2`، نه تغییر بی‌صدا |
| اسپک تولیدشده از کد | `python -m app.export_openapi --yaml` — اسپک هرگز از کد عقب نمی‌ماند |
| پاکت خطای یکنواخت | `{ "detail": ..., "request_id": ... }` |
| Request ID | هدر `x-request-id` روی هر پاسخ (تولید یا انتشار مجدد) ✅ |
| اعمال مجوز سمت سرور | نقش از توکن، نه از بدنهٔ درخواست ✅ |
| ماسک میدانی | پاسخ‌های `client/*` از `field_mask.py` عبور می‌کنند ✅ |

---

## 2. احراز هویت

دو نقطهٔ ورود، یک قالب توکن:

```http
POST /api/v1/auth/pin           {"username":"owner","pin":"****"}      → کارکنان
POST /api/v1/auth/member-pin    {"membership_code":"MP-DEMO-1","pin":"****"} → ورزشکار
GET  /api/v1/auth/me            Authorization: Bearer <token>
```

**قالب توکن:** `base64(payload).base64(hmac_sha256)` — نه JWT استاندارد، بلکه یک توکن
امضاشدهٔ خانگی با ادعاهای `sub, role, gym, mid, iat, exp, jti`. TTL = ۸ ساعت (یک شیفت).

### ✅ چیزهایی که درست است
- پیام ۴۰۱ برای «کاربر ناشناس»، «غیرفعال» و «PIN غلط» **یکسان** است — بدون شمارش کاربر.
- مقایسهٔ زمان‌ثابت با `hmac.compare_digest`.
- PBKDF2-HMAC-SHA256 با ۲۰۰٬۰۰۰ تکرار.

### 🔴 چیزهایی که کم است
1. **`jti` تولید می‌شود ولی هیچ‌جا ذخیره نمی‌شود** → هیچ راهی برای ابطال توکن نیست.
   اگر گوشی ورزشکار دزدیده شود، توکن تا ۸ ساعت معتبر می‌ماند. **راه‌حل:** جدول
   `revoked_tokens(jti, exp)` + بررسی در `deps.py`.
2. **هیچ محدودیت نرخ (rate limit) روی مسیرهای ورود نیست.** جست‌وجوی کامل یک PIN چهاررقمی
   ۱۰٬۰۰۰ درخواست است — روی LAN یعنی چند ثانیه. **این جدی‌ترین حفرهٔ امنیتی فعلی است.**
   **راه‌حل:** قفل تصاعدی به ازای `(username, ip)` — ۵ خطا → ۳۰ ثانیه، ۱۰ خطا → ۵ دقیقه،
   و ثبت در `audit_log`.
3. توکن رفرش وجود ندارد؛ پس از ۸ ساعت، ورزشکار وسط تمرین بیرون انداخته می‌شود.

---

## 3. نقشهٔ کامل ۴۲ مسیر

### سلامت و زیرساخت
```
GET    /health
GET    /api/v1/health
GET    /api/v1/ai/runtime                     وضعیت مغز AI (و اینکه به قواعد افتاده یا نه)
```

### احراز هویت
```
POST   /api/v1/auth/pin
POST   /api/v1/auth/member-pin
GET    /api/v1/auth/me
```

### اعضا
```
GET    /api/v1/members                        فهرست (TRAINER فقط اعضای خودش)
POST   /api/v1/members
GET    /api/v1/members/{id}
PATCH  /api/v1/members/{id}
POST   /api/v1/members/{id}/pin               تنظیم PIN ورزشکار
GET    /api/v1/members/{id}/qr                QR امضاشده
GET    /api/v1/members/{id}/filters           فیلترهای مؤثر مصدومیت/تجهیزات
```

### مصدومیت
```
GET    /api/v1/members/{id}/injuries
POST   /api/v1/members/{id}/injuries
PATCH  /api/v1/members/{id}/injuries/{injury_id}
GET    /api/v1/client/members/{id}/injuries   نسخهٔ ماسک‌شدهٔ ورزشکار
```

### سنجش JP7
```
POST   /api/v1/assessments/calculate          محاسبهٔ بدون ذخیره (پیش‌نمایش)
GET    /api/v1/members/{id}/assessments
POST   /api/v1/members/{id}/assessments
GET    /api/v1/members/{id}/assessments/{aid}/pdf   PDF فارسی
```

### حرکات و تجهیزات
```
GET    /api/v1/exercises
GET    /api/v1/exercises/{key}/contraindications
GET    /api/v1/equipment
POST   /api/v1/equipment
PATCH  /api/v1/equipment/{id}
```

### برنامهٔ تمرینی (الگوی dry-run → apply)
```
GET    /api/v1/members/{id}/programs
POST   /api/v1/members/{id}/programs
POST   /api/v1/members/{id}/programs/generate   قواعد ⟷ AI مسابقه می‌دهند
POST   /api/v1/programs/{pid}/dry-run           پیش‌نمایش بدون اثر
POST   /api/v1/programs/{pid}/apply             ۴۰۹ اگر قبلاً اعمال شده
POST   /api/v1/programs/{pid}/archive
```
این الگو (**dry-run اجباری قبل از apply، و apply یک‌بارمصرف با ۴۰۹**) بهترین تصمیم
معماری کل پروژه است. آن را در هر عملیات مخرب آینده هم تکرار کنید.

### تغذیه، حضور، مالی، گزارش
```
POST   /api/v1/nutrition/members/{id}/plan
POST   /api/v1/attendance/check-in
POST   /api/v1/attendance/check-out/{member_id}
GET    /api/v1/attendance/today
GET    /api/v1/packages
POST   /api/v1/payments
POST   /api/v1/payments/{id}/void
GET    /api/v1/payments/{id}/receipt            رسید PDF
GET    /api/v1/reports/dashboard
```

### سطح ورزشکار (کاملاً محدود به خود)
```
GET    /api/v1/client/me
GET    /api/v1/client/me/assessments
GET    /api/v1/client/me/nutrition
GET    /api/v1/client/me/programs
```

### مدیریت
```
POST   /api/v1/admin/backup
POST   /api/v1/admin/backup/restore
GET    /api/v1/sync/delta
```

### مسیرهای تازه‌کشف‌شده (در اسپک منتشرشده نبودند)

اسپک `openapi.yaml` مخزن **کهنه بود** و ۷ مسیر را نداشت. با بازتولید از کد، شمار واقعی
از ۴۲ به **۴۹** رسید:

```
GET  /api/v1/client/me/checkin-qr
GET  /api/v1/client/me/injuries
GET  /api/v1/client/me/payments
GET  /api/v1/client/me/workouts
GET  /api/v1/reports/expiring
GET  /api/v1/reports/inactive-members
PUT  /api/v1/automation/config
```

این دقیقاً دلیل وجود دروازهٔ «اسپک باید با کد یکی باشد» در CI است (سند ۰۷ §۲.۱):
سندی که دستی نگهداری شود، بی‌صدا از کد جدا می‌شود.

---

## 4. اثبات زندهٔ ایزولاسیون

اجرا شده در همین بازبینی روی نمونهٔ در حال اجرا:

```bash
$ curl -s /api/v1/reports/dashboard -H "authorization: Bearer $OWNER"
{"date":"2026-09-06","members_total":1,"members_active":1,
 "members_with_active_injury":0,"check_ins_today":1,"revenue_rial_this_month":1500000}

$ curl -s /api/v1/client/me -H "authorization: Bearer $MEMBER"
{"id":1,"membership_code":"MP-DEMO-1","first_name":"نسیم","last_name":"رحیمی",...}

$ curl -o /dev/null -w "%{http_code}" /api/v1/members -H "authorization: Bearer $MEMBER"
403
```
یعنی ادعای C4 (ورزشکار فقط خودش را می‌بیند) **واقعاً سمت سرور اعمال می‌شود**، نه فقط در UI.

---

## 5. 🔴 شکاف‌های قرارداد که باید بسته شود

### 5.1 صفحه‌بندی وجود ندارد
`GET /members` و `GET /exercises` **همه‌چیز را برمی‌گردانند**. با ۲۰۰۰ عضو و ۸۰۰ حرکت،
این یک پاسخ چندمگابایتی روی گوشی ورزشکار است.

**استاندارد لازم — مبتنی بر مکان‌نما (cursor)، نه offset:**
```http
GET /api/v1/members?limit=50&cursor=eyJpZCI6MTIzfQ
→ { "items": [...], "next_cursor": "eyJpZCI6MTczfQ", "has_more": true }
```
offset با داده‌ای که مدام درج می‌شود ردیف را جا می‌اندازد؛ cursor نه.

### 5.2 بدون ETag / کش شرطی
ورزشکار هر بار باز کردن اپ، کل برنامه‌اش را دوباره می‌گیرد.
`ETag` + `If-None-Match` → `304` روی `/client/me/*` بار را روی Wi-Fi ضعیف باشگاه به‌شدت کم می‌کند.

### 5.3 بدون کلید یکتاسازی (Idempotency-Key) روی POSTها
اگر ورزشکار دوبار روی «ثبت پرداخت» بزند یا شبکه قطع و دوباره تلاش شود، **دو پرداخت** ثبت می‌شود.
```http
POST /api/v1/payments
Idempotency-Key: 8f14e45f-...
```
سرور کلید و پاسخ را ۲۴ ساعت نگه دارد و تکرار را با همان پاسخ اصلی جواب دهد.
برای `attendance/check-in` هم لازم است (اسکن دوباره در ۳۰ ثانیه).

### 5.4 پاکت خطا استاندارد نیست
اکنون `detail` یک رشتهٔ آزاد فارسی است. کلاینت نمی‌تواند روی آن منطق بنویسد.
**قالب پیشنهادی (RFC 9457 Problem Details):**
```json
{
  "type": "https://mp.local/errors/injury-blocks-program",
  "title": "برنامه با مصدومیت فعال مغایر است",
  "status": 422,
  "code": "INJURY_CONTRAINDICATION",
  "detail": "حرکت «اسکات» با مصدومیت زانوی راست مغایرت دارد",
  "request_id": "01H...",
  "fields": { "exercises[3].key": "back-squat" }
}
```
`code` ماشین‌خوان است و ثابت می‌ماند؛ `detail` قابل ترجمه است.

### 5.5 بدون سیاست منسوخ‌سازی
قبل از v1.0 اضافه کنید: هدر `Deprecation` و `Sunset` روی مسیرهای در حال حذف، حداقل
دو نسخه فاصله.

---

## 6. کدهای وضعیت — قرارداد

| کد | معنی در MP |
|----|-------------|
| 200 / 201 | موفق |
| 304 | بدون تغییر (پس از افزودن ETag) |
| 400 | JSON بدشکل |
| 401 | توکن نبود/منقضی/جعلی |
| 403 | نقش اجازه ندارد (نمونه: MEMBER روی `/members`) |
| 404 | یافت نشد — **و همچنین برای TRAINER روی عضو تخصیص‌نیافته** (نه ۴۰۳، تا وجود عضو فاش نشود) ✅ |
| 409 | تعارض حالت (اعمال دوبارهٔ برنامه) ✅ |
| 422 | اعتبارسنجی — شامل رد شدن به‌خاطر مصدومیت |
| 429 | محدودیت نرخ — **هنوز پیاده نشده** |
| 500 | خطای داخلی؛ بدنه هرگز استک نشان نمی‌دهد، فقط `request_id` |

انتخاب ۴۰۴ به‌جای ۴۰۳ برای مربی غیرمجاز، تصمیم امنیتی هوشمندانه‌ای است که باید مستند بماند.

---

## 7. 🔴 CORS در حالت تولید

`config.py` پیش‌فرض امنی دارد (`localhost:5173`, `app://mp`) ✅.
اما `MP_CORS_ORIGINS='*'` پذیرفته می‌شود. باید:
- در حالت تولید، `*` **رد شود** (خطای راه‌اندازی)، نه فقط ناخوشایند باشد؛
- فهرست مجاز، آدرس LAN باشگاه را صریح داشته باشد.

---

## 8. پل اتوماسیون (n8n)

قرارداد: فقط رویداد و شناسه، **هیچ PHI**.
```json
POST <n8n webhook>
{ "event": "membership.expiring", "gym_id": 1, "member_id": 42,
  "days_left": 3, "ts": "2026-09-06T06:00:00Z", "sig": "hmac..." }
```
هیچ نام، تلفن، وزن یا مصدومیتی عبور نمی‌کند. این قرارداد باید یک **تست** داشته باشد که
بدنهٔ خروجی را در برابر فهرست سفید کلیدها بسنجد — تا کسی روزی «برای راحتی» نام را اضافه نکند.
