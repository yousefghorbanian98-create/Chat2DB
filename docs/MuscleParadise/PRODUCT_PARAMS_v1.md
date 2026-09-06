# 🏋️ MUSCLE PARADISE — پارامترهای محصول جامع v1.2
## دو نسخه · آسیب/محدودیت · شخصی‌سازی · پیشنهادهای تکمیلی · اتوماسیون n8n

> تاریخ: 2026-08-29 (v1.2: پل n8n)  
> وضعیت Cutting Edge: **دست‌نخورده**  
> این سند مکمل `EXECUTIVE_SCHEMATIC_v1.md` و `ENGINEERING_MAP_FULL_v1.md` است.  
> اتوماسیون اختیاری: `N8N_AUTOMATION_BRIDGE.md` · کاتالوگ: https://zie619.github.io/n8n-workflows/

---

# ۱. اصل طلایی محصول (از خواسته تو)

```
هر ورزشکار = یک پروفایل پزشکی-حرکتی زنده
                    ↓
         آسیب‌ها + محدودیت‌ها + اهداف + JP7
                    ↓
     موتور برنامه فقط از فیلتر «ایمن برای این بدن» رد می‌شود
                    ↓
        دو پنجره به همان دیتابیس:

   ┌─────────────────────┐     ┌──────────────────────────┐
   │  MP STUDIO (مال تو) │     │  MP CLIENT (ورزشکار)     │
   │  Admin / Trainer     │     │  Member self-service     │
   │  همه داده‌ها + AI    │     │  فقط دادهٔ خودش          │
   │  مالی + همه اعضا    │     │  یوزر/پسورد یا بیومتریک  │
   └─────────────────────┘     └──────────────────────────┘
```

---

# ۲. دو نسخه رسمی برنامه

| | **MP Studio** (نسخه مربی/صاحب) | **MP Client** (نسخه ورزشکار) |
|--|-------------------------------|------------------------------|
| مخاطب | تو، مربی کمکی، پذیرش | فقط عضو باشگاه |
| ورود | PIN + اثرانگشت + نقش | یوزرنیم/پسورد یا کد عضویت + OTP اختیاری + بیومتریک دستگاه |
| داده可见 | **همه** اعضا، مالی، AI، تنظیمات، سینک | **فقط** پروفایل خودش |
| ماژول‌ها | کامل (۱۲+ ماژول) | زیرمجموعه محدود |
| نصب | PC باشگاه + تبلت مربی + کیوسک | موبایل Android (+ PWA) |
| AI | ساخت/تأیید/ویرایش برنامه برای هر کس | فقط **مشاهده** و بازخورد اجرا (نه تولید برای دیگران) |
| مالی | ثبت پرداخت، بدهی، گزارش | وضعیت عضویت خودش + تاریخچه پرداخت خودش |
| خروج داده | Export کامل باشگاه | Export فقط پرونده خودش (PDF/QR) |

## ۲.۱ نقش‌ها داخل Studio (نه فقط دو باینری)

| نقش | دسترسی |
|-----|--------|
| **OWNER** | همه‌چیز + حذف باشگاه + بکاپ + لایسنس |
| **ADMIN** | اعضا، مالی، گزارش، تنظیمات (بدون حذف مالک) |
| **TRAINER** | اعضا اختصاص‌یافته، JP7، برنامه، تغذیه، یادداشت — **بدون** گزارش مالی کل |
| **RECEPTION** | check-in، تمدید ساده، ثبت نقدی — بدون AI سنگین و بدون ویرایش پزشکی |
| **KIOSK** | فقط اسکن QR ورود/خروج (صفحه قفل‌شده) |
| **MEMBER** | فقط Client app |

> یک کدبیس، چند **flavor / role shell**. نه دو پروژه جدا که دوباره‌کاری شود.

## ۲.۲ قانون حریم خصوصی (غیرقابل مذاکره)

- Client **هرگز** API لیست اعضا را نمی‌بیند (حتی اگر URL را حدس بزند).
- فیلتر اجباری سمت سرور: `WHERE member_id = auth.uid` برای نقش MEMBER.
- فیلدهای حساس (کد ملی، یادداشت پزشکی مربی، مبلغ بدهی دیگران) در response نقش MEMBER حذف می‌شوند (**field masking**).
- لاگ دسترسی: چه کسی پرونده پزشکی چه کسی را دید.

---

# ۳. پروفایل شخصی — آسیب و محدودیت (هسته شخصی‌سازی)

## ۳.۱ بلوک‌های پروفایل کامل

```
MEMBER PROFILE
├── هویت (نام، کد عضویت، تماس، عکس، QR)
├── دموگرافیک (سن، جنس، قد، وزن)
├── اهداف (چربی‌سوزی / حجم / قدرت / توان / rehabiliation / عمومی)
├── سبک زندگی (خواب، شغل نشسته/ایستاده، سطح استرس — اختیاری)
├── 🩺 MEDICAL & INJURY DOSSIER   ← جدید و اجباری برای AI
├── 🚫 MOVEMENT LIMITATIONS      ← جدید
├── 🏋️ Experience & preferences
├── 🥗 Nutrition constraints
├── 📅 Availability (روز/ساعت تمرین)
└── 📎 Attachments (عکس MRI/نسخه — رمزنگاری‌شده، فقط Studio)
```

## ۳.۲ ساختار آسیب (Injury Record)

هر آسیب یک رکورد جدا با تاریخچه است (نه یک text box ساده):

| فیلد | مثال | چرا |
|------|------|-----|
| `body_region` | knee_r, lumbar, shoulder_l, wrist_r, neck… | فیلتر حرکت |
| `side` | left / right / bilateral / n/a | |
| `diagnosis_label` | ACL sprain G2, impingement, disc bulge | متن مربی |
| `status` | active / recovering / cleared / chronic | |
| `pain_scale_0_10` | 0–10 | شدت |
| `onset_date` / `cleared_date` | | |
| `aggravators` | deep flexion, overhead press, running | |
| `easers` | ice, band work | |
| `contraindicated_patterns` | axial loading, end-range rotation… | **قانون AI** |
| `allowed_modifications` | goblet squat instead of back squat | |
| `clinician_note` | فقط Studio | |
| `member_visible_note` | متن امن برای Client | |
| `requires_medical_clearance` | bool | اگر true → AI برنامه قدرت سنگین نسازد |

### نواحی استاندارد بدن (enum)
```
neck, cervical, thoracic, lumbar, sacroiliac,
shoulder, scapula, elbow, wrist, hand,
hip, groin, knee, ankle, foot,
chest, abdomen, cardiovascular, respiratory, neurological, other
```

## ۳.۳ محدودیت حرکتی (Movement Limitation) — جدا از آسیب

گاهی آسیب «تمام‌شده» است ولی الگو مانده:

| نوع | مثال |
|-----|------|
| ROM محدود | shoulder flexion < 150° |
| الگوی ممنوع | overhead bar، behind-neck، plyometric |
| تجهیز ممنوع | treadmill (zish زانو)، barbell back squat |
| محیط | آسم → HIIT طولانی ممنوع |
| عصبی-عضلانی | تعادل ضعیف → single-leg advanced بعداً |
| زنان/بارداری/پس از زایمان | پروتکل جدا (guardrail) |
| زیر ۱۸ | رضایت ولی + بار کمتر |

## ۳.۴ پرچم‌های ایمنی سراسری (Red Flags)

اگر هر کدام فعال باشد، AI و Rule engine **مسیر توانبخشی/ارجاع** می‌گیرند نه bulk سنگین:

- درد قفسه سینه / تنگی نفس فعالیتی  
- سرگیجه شدید  
- جراحی < ۱۲ هفته بدون clearance  
- شکستگی التیام‌نیافته  
- دستور پزشک «no load bearing»

→ در UI: بنر قرمز + الزام تأیید مربی برای هر برنامه.

## ۳.۵ ارتباط آسیب → موتور برنامه (قانون شخصی‌سازی)

```
Candidate exercise
   → blocked by active injury region?        DROP
   → blocked by contraindicated_pattern?     DROP or SWAP
   → equipment missing in gym?               DROP
   → conflicts nutrition/time?               adjust
   → matches goal + JP7 classification?      score↑
   → novelty vs last mesocycle?              score↑
   → passes dry-run + trainer confirm?       APPLY
```

**هیچ برنامه‌ای بدون عبور از فیلتر Injury/Limitation ذخیره فعال نمی‌شود** (مگر OWNER صریحاً override با دلیل لاگ‌شده).

---

# ۴. آنچه در هر نسخه دیده می‌شود

## ۴.۱ MP Studio — صفحه پروفایل عضو (کامل)

- همه بلوک‌های §۳  
- تاریخچه JP7 + نمودار  
- برنامه‌های فعال/آرشیو + نسخه AI و ویرایش مربی  
- تغذیه  
- حضور  
- مالی و بدهی  
- یادداشت خصوصی مربی‌ها (thread)  
- آسیب‌ها timeline  
- Progressive overload / PR  
- Progress photos  
- فایل‌های ضمیمه  
- دکمه «تولید برنامه با AI» + dry-run  

## ۴.۲ MP Client — خانه ورزشکار (فقط خود)

```
خانه
├── وضعیت عضویت (روز مانده / انقضا)
├── چک‌این امروز (QR من)
├── برنامه تمرین این هفته + تیک ست‌ها
├── برنامه غذای امروز + آب
├── آخرین %چربی و روند ساده
├── آسیب‌های «قابل نمایش به من» (نه یادداشت خصوصی مربی)
├── پیام/یادداشت مربی برای من
├── نوبت پیکرسنجی بعدی (فقط مشاهده)
├── تاریخچه پرداخت خودم + دانلود رسید
└── تنظیمات: رمز، اثرانگشت، زبان، خروج
```

**ندارد:** لیست اعضا، مالی باشگاه، AI برای دیگران، ویرایش JP7 دیگران، تنظیمات سرور، سینک ادمین.

### ۴.۳ چه چیزهایی Client می‌تواند «بنویسد»؟

| مجاز | غیرمجاز |
|------|---------|
| لاگ ست (وزن/تکرار/RPE) که مربی فعال کرده | تغییر تشخیص آسیب بدون تأیید |
| تیک درد جلسه (traffic light) | حذف پرداخت |
| درخواست تمدید / پیام به مربی | دیدن پرونده دیگران |
| به‌روزرسانی عکس پروفایل و وزن روزانه | override برنامه قفل‌شده مربی |
| بازخورد «این حرکت درد دارد» → فلگ برای Studio | |

---

# ۵. چیزهای دیگری که باید از الان به برنامه اضافه شوند
### (پیشنهادهای محصولی فراتر از حرف تو — اولویت‌بندی‌شده)

## ۵.۱ P0 — بدون این‌ها محصول حرفه‌ای/ایمن نیست

| # | قابلیت | دلیل |
|---|--------|------|
| P0-1 | **دو پوسته Studio / Client + RBAC** | خواسته اصلی تو |
| P0-2 | **Injury & Limitation dossier** ساختاریافته | شخصی‌سازی واقعی |
| P0-3 | **Exercise contraindication graph** | اتصال آسیب↔حرکت |
| P0-4 | **Override با audit log** | مربی مسئول است |
| P0-5 | **Consent + Medical disclaimer** امضای دیجیتال | پایان‌نامه + قانونی |
| P0-6 | **JP7 با تاریخ + روند** | هسته تو |
| P0-7 | **Filter AI بر اساس equipment باشگاه** | |
| P0-8 | **QR check-in امضادار + وضعیت عضویت** | |
| P0-9 | **پرداخت/انقضا + رسید** | |
| P0-10 | **Backup رمزدار + restore تست‌شده** | |
| P0-11 | **Field masking API** | امنیت Client |
| P0-12 | **نسخه‌بندی program_json** | |
| P0-13 | **Dry-run AI قبل از apply** | الگوی CE |
| P0-14 | **حالت Kiosk** | درب باشگاه |
| P0-15 | **Youth / pregnancy guardrails** | |

## ۵.۲ P1 — تفاوت «باشگاهOrdinary» با «Muscle Paradise»

| # | قابلیت | توضیح |
|---|--------|-------|
| P1-1 | **Pain check-in قبل از هر جلسه** (سبز/زرد/قرمز) | اگر قرمز → پیشنهاد deload خودکار |
| P1-2 | **Readiness score** ساده (خواب+کوفتگی+استرس ۱–۵) | تنظیم حجم همان روز |
| P1-3 | **Movement screen سبک** (overhead squat view، shoulder reach…) | ورودی اصلاحی |
| P1-4 | **Corrective block اجباری** وقتی limitation فعال است | ۱۰–۱۵ دقیقه اول |
| P1-5 | **Swap exercise هوشمند** داخل Client با حفظ الگو | اگر دستگاه اشغال/درد |
| P1-6 | **Trainer assignment** (هر عضو → مربی مسئول) | TRAINER فقط clients خودش |
| P1-7 | **PT pack** (بسته ۸ جلسه خصوصی + مصرف جلسه) | درآمد مربی |
| P1-8 | **Progress photo** با راهنمای پوز و نور | |
| P1-9 | **پیام درون‌برنامه‌ای مربی↔عضو** | بدون وابستگی واتساپ |
| P1-10 | **هشدار عدم حضور N روز** | retention |
| P1-11 | **لیست انتظار کلاس گروهی** | اگر کلاس دارید |
| P1-12 | **واحد پول ریال + تقویم شمسی همه‌جا** | |
| P1-13 | **چاپ حرارتی رسید** (اختیاری) | |
| P1-14 | **دو امضا روی برنامه:** AI draft → Trainer approved → Client acknowledged | |
| P1-15 | **Export ورزشکار بدون داده مالی دیگران** | QR/PDF امن |
| P1-16 | **حالت مهمان/آزمایشی ۷ روز** | جذب |
| P1-17 | **مقایسه before/after JP7 یک‌کلیکی برای فروش تمدید** | |
| P1-18 | **پل اتوماسیون n8n (اختیاری)** — یادآوری انقضا، رسید، غیبت، بکاپ | کاتالوگ: https://zie619.github.io/n8n-workflows/ · جزئیات: `N8N_AUTOMATION_BRIDGE.md` |
| P1-19 | **کانال اطلاع‌رسانی** Telegram / WhatsApp / SMS ایرانی روی webhookهای MP | هسته بدون n8n هم کار کند |

## ۵.۳ P2 — درجه یک / رقابتی

| # | قابلیت |
|---|--------|
| P2-1 | گیمیفیکیشن: streak، badge «۴ هفته بدون غیبت» |
| P2-2 | جدول لیدر بورد **اختیاری و opt-in** (حریم خصوصی) |
| P2-3 | snoreregister تجهیزات + تعمیرات |
| P2-4 | شیفت کارکنان + پورسانت فروش |
| P2-5 | بارکد مواد غذایی OFF برای لاگ وعده |
| P2-6 | ویدیو فرم کوتاه آفلاین per exercise |
| P2-7 | همگام‌سازی چند شعبه (همان gym_id hierarchy) |
| P2-8 | Voice note مربی روی حرکت (مثل واک) |
| P2-9 | تست‌های آمادگی: cooper، plank time، max pushup |
| P2-10 | گزارش ماهانه خودکار PDF برای عضو (ایمیل/اشتراک فایل) |
| P2-11 | تم باشگاه (رنگ/لوگوی تو روی Client) white-label سبک |
| P2-12 | حالت مسابقه/چالش ۳۰ روزه داخل باشگاه |
| P2-13 | اتصال ترازوی بلوتوثی (اختیاری) |
| P2-14 | NFC کارت عضویت علاوه بر QR |
| P2-15 | آنالیز «کیفیت اجرا» بعداً با ویدیو (فاز دور — از CE الهام) |

## ۵.۴ P3 — آینده / پایان‌نامه فاز ۲

- نسخه iOS Client  
- ویزارد «باشگاه من از صفر» برای فروش به باشگاه‌های دیگر  
- Marketplace قالب برنامه (بدون ابر اجباری: pack فایل)  
- Tele-rehab سبک  
- انگلیسی کامل برای عضو خارجی  

---

# ۶. پارامترهای ورودی شخصی‌سازی برنامه (چک‌لیست موتور)

قبل از ساخت برنامه، سیستم باید این‌ها را داشته باشد یا صریحاً «نامشخص» بگذارد:

### هویت تمرینی
- [ ] هدف اصلی + افق زمانی (۴/۸/۱۲ هفته)  
- [ ] سطح (مبتدی / متوسط / پیشرفته)  
- [ ] سابقه پیوسته تمرین (ماه)  
- [ ] روزهای در دسترس در هفته + مدت هر جلسه  
- [ ] ترجیح split یا «خود سیستم تصمیم بگیرد»  

### بدن
- [ ] JP7 آخرین + delta نسبت به قبل  
- [ ] وزن، قد، دور کمر/لگن اختیاری  
- [ ] کلاس BF (athletic…obese)  

### ایمنی
- [ ] آسیب‌های active  
- [ ] محدودیت‌های حرکتی  
- [ ] red flags  
- [ ] دارو/شرایط (دیابت، فشار — فقط پرچم، نه تجویز)  

### امکانات
- [ ] inventory باشگاه  
- [ ] دمبل تا چند کیلو، rack، کابل، cardio…  

### تغذیه
- [ ] هدف کالری (cut/bulk/maintain)  
- [ ] آلرژی، مذهب، گیاه‌خواری، بودجه، تعداد وعده  
- [ ] ترجیح غذای ایرانی  

### رفتار
- [ ] نرخ حضور ۸ هفته اخیر  
- [ ] پایبندی لاگ ست  
- [ ] دردهای تکرارشونده روی حرکت X  

---

# ۷. جریان تأیید برنامه (سه امضا)

```
[1] AI یا Rule  →  status: draft
[2] مربی در Studio بازبینی/ویرایش  →  status: trainer_approved
[3] عضو در Client «دریافت کردم / سؤالی دارم»  →  status: client_ack
        │
        └─ اگر client گزارش درد بدهد → status: needs_review
```

برنامه `trainer_approved`نشده در Client به‌عنوان «نهایی» نشان داده نمی‌شود (مگر OWNER اجازه «auto-publish» بدهد برای باشگاه شلوغ).

---

# ۸. مدل داده — جداول جدید (خلاصه)

```sql
-- آسیب‌ها
member_injuries (
  id, member_id, body_region, side, label, status,
  pain_0_10, onset_date, cleared_date,
  aggravators_json, contraindicated_patterns_json,
  allowed_mods_json, clinician_note, member_note,
  requires_clearance, created_by, rev, deleted_at
);

-- محدودیت‌های ماندگار
member_limitations (
  id, member_id, type, pattern_or_equipment, severity,
  notes, active, rev, deleted_at
);

-- گراف منع حرکت (دانش)
exercise_contraindications (
  exercise_id, pattern, region, severity  -- hard_block | modify | caution
);

-- تخصیص مربی
member_trainer (
  member_id, trainer_staff_id, is_primary
);

-- بازخورد درد جلسه از Client
session_feedback (
  id, member_id, session_date, readiness_1_5,
  pain_flag, pain_region, notes, seen_by_trainer
);

-- رضایت‌نامه
consents (
  member_id, type, version, signed_at, signature_meta
);
```

---

# ۹. UI پیشنهادی — کارت «ایمنی بدن» در Studio

```
┌─ 🩺 وضعیت ایمنی: ALI REZAEE ─────────────────────┐
│  🔴 Knee R — ACL sprain (active, pain 4/10)       │
│      ممنوع: deep knee flexion load, jumping        │
│      مجاز: leg press partial, bike                 │
│  🟡 Lumbar — chronic, pain 2/10                    │
│      ممنوع: behind-neck, max load good morning     │
│  ✅ Clearance پزشکی: دارد (تا 2026-12)             │
│  [ویرایش آسیب‌ها]  [ساخت برنامه با فیلتر ایمنی]   │
└────────────────────────────────────────────────────┘
```

در Client همان کارت **بدون clinician_note** و با زبان ساده‌تر.

---

# ۱۰. تصمیم‌های باز برای تو (وقتی خواستی جواب بده)

این‌ها را عمداً قفل نکردم تا با سلیقه باشگاهت تنظیم شود:

1. **Client برنامه را می‌تواند جزئیات ست عوض کند یا فقط لاگ بزند؟**  
2. **آیا عضو JP7 خودش را می‌بیند یا فقط بعد از تأیید مربی؟**  
3. **چند شعبه / یک باشگاه؟**  
4. **کلاس گروهی دارید یا فقط بدنسازی + PT؟**  
5. **پرداخت فقط نقد/کارت در باشگاه یا بعداً درگاه؟** (درگاه = خلاف «بدون ابر» مگر اختیاری)  
6. **زبان پیش‌فرض Client: فقط فارسی یا fa/en؟**  
7. **حداقل سن عضویت و سیاست نوجوان؟**  
8. **آیا مربی کمکی مالی را ببیند؟** (پیشنهاد پیش‌فرض: نه)

---

# ۱۱. جمع‌بندی یک‌خطی

> **MP Studio** مغز و صندوق و پرونده پزشکی باشگاه است؛  
> **MP Client** آینهٔ شخصی همان پرونده برای خود ورزشکار است؛  
> **آسیب + محدودیت** فیلتر اجباری قبل از هر برنامه است؛  
> باقی ویژگی‌ها (readiness، corrective، PT pack، گیمیفیکیشن…) دور همین هسته چیده می‌شوند.

---

**فایل:** `docs/MuscleParadise/PRODUCT_PARAMS_v1.md`  
**CE:** بدون تغییر ✅
