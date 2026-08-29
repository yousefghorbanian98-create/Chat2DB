# 🏋️ MUSCLE PARADISE (MP) — شماتیک اجرایی v1.0
## Executive Schematic · Gap Analysis · CE Pattern Map · OSS Import List

> **قانون طلایی:** هیچ فایلی داخل `ce-app/` یا `docs/CuttingEdge/` تغییر نمی‌کند.  
> فقط **الگوبرداری مفهومی + کپی ایده‌ها در مسیر جدا** `docs/MuscleParadise/` و بعداً `mp-app/`.

**تاریخ:** 2026-08-28  
**برند:** Muscle Paradise · مخفف لوگو: **MP**  
**مرجع نقشه مهندسی:** Engineering Map v1.0 (ارسالی کاربر)  
**مرجع الگو:** Cutting Edge v0.9.x (`ce-app/`) — فقط خواندنی

---

# فهرست
1. [شماتیک اجرایی یک‌صفحه‌ای](#1)
2. [تصحیح معماری نسبت به نقشه v1.0](#2)
3. [آنچه نقشه فعلی کم دارد (Gap Analysis)](#3)
4. [چه چیزهایی از Cutting Edge الگوبرداری می‌شود](#4)
5. [کاتالوگ اوپن‌سورس واقعی برای import](#5)
6. [نقشه وابستگی ماژول‌ها (ترتیب ساخت)](#6)
7. [قرارداد داده مشترک (Shared Contracts)](#7)
8. [چک‌لیست روز صفر اجرایی](#8)

---

<a id="1"></a>
# ۱. شماتیک اجرایی یک‌صفحه‌ای

```
╔══════════════════════════════════════════════════════════════════════════════╗
║                         MUSCLE PARADISE  ·  MP                               ║
║              Local-First  ·  Optional Deep-Net Knowledge  ·  No Cloud Bill    ║
╚══════════════════════════════════════════════════════════════════════════════╝

┌──────────────┐  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐
│  Android App │  │  Desktop PC  │  │  Web PWA     │  │  Kiosk / درب باشگاه  │
│  (Flutter)   │  │  Electron+   │  │  (React)     │  │  QR scanner station  │
│  Member+Staff│  │  React (CE)  │  │  same UI kit │  │  (tablet / phone)    │
└──────┬───────┘  └──────┬───────┘  └──────┬───────┘  └──────────┬───────────┘
       │                 │                 │                     │
       └─────────────────┴────────┬────────┴─────────────────────┘
                                  │  HTTPS local / LAN / loopback
                                  ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                     MP CORE  (الگوی Cutting Edge)                           │
│  FastAPI · SQLite · Job Queue · WebSocket progress · Local REST             │
│  Port پیشنهادی: 8751   (CE از 8742 استفاده می‌کند — تداخل نداشته باشد)      │
├──────────────────────┬──────────────────────┬───────────────────────────────┤
│  Domain Services     │  AI Brain (local)    │  Sync Fabric (P2P)            │
│  · members           │  · Rule planner      │  · QR payload (signed JWT)    │
│  · jp7 assessment    │  · Ollama planner    │  · Bluetooth / Wi-Fi Direct   │
│  · training builder  │  · RAG (Chroma/lancedb)│ · Delta log + CRDT merge   │
│  · nutrition         │  · Scientific KB     │  · encrypted backup pack      │
│  · attendance        │  · Judge/score       │  · LAN multi-device discovery │
│  · payments/billing  │  · Prompt templates  │                               │
│  · reports/PDF       │                      │                               │
└──────────────────────┴──────────────────────┴───────────────────────────────┘
                                  │
          ┌───────────────────────┼───────────────────────┐
          ▼                       ▼                       ▼
   ┌─────────────┐        ┌──────────────┐        ┌────────────────┐
   │ SQLite MP   │        │ Knowledge    │        │ Optional Net   │
   │ + FTS5      │        │ Pack (local) │        │ Deep Search    │
   │ members…    │        │ exercises    │        │ (only when     │
   │ assessments │        │ papers/RAG   │        │  user allows)  │
   │ programs    │        │ foods IR+USDA│        │ · refresh KB   │
   │ payments    │        │ corrective   │        │ · model update │
   │ sync_log    │        │ protocols    │        │ · delta app    │
   └─────────────┘        └──────────────┘        └────────────────┘
```

### جریان اصلی کسب‌وکار (Happy Path مربی)

```
[عضو جدید]
   → ثبت پروفایل + QR + اثرانگشت (اختیاری)
   → پیکرسنجی JP7
   → محاسبه Density / %BF / LBM / FM
   → ذخیره assessment با تاریخ شمسی+میلادی
        │
        ▼
[دکمه «برنامه بساز»]
   → Rule Engine (همیشه)  +  Ollama (اگر نصب)  +  RAG از KB
   → Race/Judge مثل CE: بدترین حالت = خروجی rule، نه hallucination
   → برنامه تمرینی JSON + برنامه غذایی JSON
   → PDF قابل چاپ + آرشیو در پروفایل
        │
        ▼
[روزهای عادی باشگاه]
   → Check-in QR/Fingerprint
   → لاگ حضور
   → پرداخت/تمدید شهریه
   → هشدار انقضا
        │
        ▼
[بین دستگاه‌ها]
   → Delta Sync (QR chunk / BT / Wi-Fi Direct / USB backup)
```

### اصل هوش مصنوعی (مستقیم از فلسفه CE / BRAIN_DESIGN)

| کار | کی انجام می‌دهد | چرا |
|-----|----------------|-----|
| محاسبه JP7، TDEE، ماکرو | **کد قطعی** (فرمول) | قابل اندازه‌گیری؛ LLM حق اختراع عدد ندارد |
| انتخاب پروتکل تمرینی پایه | **Rule planner** | همیشه آفلاین کار کند |
| شخصی‌سازی، تنوع، اصلاحی، متن برنامه | **Ollama + RAG** | قضاوت متنی |
| «آیا برنامه خوب است؟» | **Judge عددی** (نه حس) | سقف ست، تعادل push/pull، محدودیت پزشکی، کالری ±۵٪ هدف |
| اندازه‌گیری واقعیت بدن | **کالiper + مربی** | مدل عکس‌بین فقط کمکی است، نه جایگزین JP7 |

> قانون CE: **LLM هرگز اندازه نمی‌گیرد؛ اندازه‌گیری هرگز بحث نمی‌کند.**

---

<a id="2"></a>
# ۲. تصحیح معماری نسبت به نقشه v1.0

نقشه v1.0 عالی است، ولی چند نقطه برای **اجرا بدون دوباره‌کاری** باید اصلاح شود:

| مورد در v1.0 | واقعیت / توصیه اجرایی |
|--------------|----------------------|
| Flutter برای Mobile+Desktop + Next جدا | **دوباره‌کاری UI.** CE همین الان Electron+React+Ant+Zustand دارد. پیشنهاد: **PC/Web = همان استک CE**؛ **Android = Flutter یا PWA نصب‌شونده** |
| «کاملاً بدون اینترنت» + «سرچ عمیق اینترنت» | تناقض. مدل درست: **Local-First + Optional Online Enrichment** (KB قابل دانلود، deep search فقط با اجازه) |
| ChromaDB روی موبایل | سنگین. **LanceDB / sqlite-vss / embeddings در SQLite** برای موبایل؛ Chroma فقط روی PC |
| LLaMA 3.1 8B روی همه Android | غیرواقعی برای خیلی از گوشی‌ها. PC = 8B؛ موبایل = Phi-3 / Gemma 2B یا **فقط فراخوانی به PC باشگاه روی LAN** |
| nearby_connections | خوب برای Android؛ روی Windows Electron باید **LAN HTTP + QR + WebRTC/Bluetooth alternate** |
| wger به‌عنوان هسته | **AGPL-3** — اگر کد wger را داخل باینری MP بگذاری، ممکن است کل MP را AGPL کند. **داده/ایده OK؛ fork کد فقط با آگاهی لایسنس** |
| یک کدبیس Dart+TS Shared | در عمل دو runtime. بهتر: **Shared OpenAPI schema + JSON contracts** بین Flutter و FastAPI |

### استک پیشنهادی نهایی (اجرایی)

| لایه | انتخاب | الگو از |
|------|--------|---------|
| Desktop | Electron 31 + React 18 + Vite + Ant Design + Zustand | **Cutting Edge** |
| Backend local | FastAPI + SQLite + WebSocket jobs | **Cutting Edge** |
| Android | Flutter 3.x (member app + trainer field) | جدید |
| Web | همان frontend CE به‌صورت PWA (vite-plugin-pwa) | CE + PWA |
| AI | Ollama local + rule planner + RAG | CE Brain |
| Update | electron-updater (GitHub Releases) | CE UpdateCard |
| i18n | fa + en (Vazirmatn) | CE i18n |
| Charts | Recharts / Ant Charts روی PC؛ fl_chart روی Flutter | — |

---

<a id="3"></a>
# ۳. آنچه نقشه فعلی کم دارد (Gap Analysis)

## ۳.۱ شکاف‌های محصولی (باید به نقشه اضافه شوند)

| # | قابلیت گم‌شده | چرا حیاتی است | اولویت |
|---|---------------|---------------|--------|
| G01 | **حالت‌های استقرار (Deployment Modes)** | باشگاه تک‌دستگاه / چندتبلت LAN / مربی سیار | P0 |
| G02 | **نقش Kiosk ورود** (صفحه قفل‌شده فقط QR) | درب باشگاه نباید به کل دیتابیس دسترسی داشته باشد | P0 |
| G03 | **Consent & Medical disclaimer** | AI پزشکی/تغذیه نیست؛ امضای رضایت ورزشکار | P0 |
| G04 | **Versioned Program Schema** (`program_json` v1/v2) | بدون version مهاجرت می‌شکند | P0 |
| G05 | **Idempotent payments + audit trail** | جلوگیری از ثبت دوبل شهریه | P0 |
| G06 | **Soft-delete + tombstone برای sync** | CRDT/دلتا بدون tombstone خراب می‌شود | P0 |
| G07 | **Device identity + pairing** | کدام تبلت «منبع حقیقت» است | P0 |
| G08 | **Conflict UI** (نه فقط merge خودکار) | دو مربی همزمان وزن را عوض کنند | P1 |
| G09 | **Calibration کالپر / Intra-tester error** | JP7 بدون پروتکل اندازه‌گیری بی‌ارزش است | P1 |
| G10 | **JP3 / JP4 / Durnin-Womersley / Navy** به‌عنوان fallback | بعضی روزها ۷ نقطه ممکن نیست | P1 |
| G11 | **RPE/RIR log واقعی جلسه** | progressive overload بدون لاگ ست، شعار است | P1 |
| G12 | **Equipment inventory باشگاه** | AI نباید Hack Squat بدهد اگر دستگاه ندارید | P1 |
| G13 | **Corrective screen (FMS-like سبک)** | فقط %چربی برای اصلاحی کافی نیست | P1 |
| G14 | **Periodization cycles** (mesocycle 4–12 w) | برنامه یک‌برگی ≠ برنامه‌نویسی علمی | P1 |
| G15 | **Deload & injury flag workflow** | توقف خودکار progressive overload | P1 |
| G16 | **Persian food DB + واحد خانگی** (قاشق، لیوان) | USDA alone برای ایران کافی نیست | P0 |
| G17 | **آلرژی / مذهب / گیاه‌خواری / بودجه** در nutrition | وگرنه برنامه کلیشه‌ای می‌شود | P0 |
| G18 | **SMS ایرانی به‌صورت adapter** (اختیاری، نه ابری اجباری) | کاوه‌نگار / IPPanel / ... | P2 |
| G19 | **چاپ حرارتی رسید** (ESC/POS) | باشگاه واقعی رسید می‌خواهد | P2 |
| G20 | **Backup رمزنگاری‌شده با عبارت عبور** + تست restore | بدون restore تست‌شده = بکاپ جعلی | P0 |
| G21 | **Telemetry محلی اختیاری** (crash log روی دیسک) | مثل CE؛ بدون ارسال ابری | P2 |
| G22 | **Multi-gym / multi-branch** later | schema از روز اول `gym_id` داشته باشد | P1 |
| G23 | **Staff shift & commission** | اگر چند مربی فروش دارند | P2 |
| G24 | **Locker / کارت قفسه** | عملیاتی باشگاه | P3 |
| G25 | **Class/Group schedule** (کراس‌فیت، یوگا) | خیلی باشگاه‌ها فقط بدنسازی نیستند | P2 |
| G26 | **PT session packing** (بسته ۸ جلسه خصوصی) | مدل درآمد مربی | P1 |
| G27 | **Photo progress با pose guide** | before/after علمی‌تر | P1 |
| G28 | **Export برای ورزشکار (QR برنامه بدون داده مالی)** | حریم خصوصی | P0 |
| G29 | **Role-based field masking** | عضو مبلغ بقیه را نبیند | P0 |
| G30 | **Knowledge Pack versioning** (`kb-2026.08.pack`) | آپدیت علمی جدا از آپدیت UI | P0 |
| G31 | **Air-gapped mode** صریح | باشگاه بدون نت | P0 |
| G32 | **Hardware profile wizard** (RAM/GPU → کدام مدل AI) | مثل AiRuntimeCard در CE | P0 |
| G33 | **Dry-run قبل از اعمال برنامه AI** | مثل Assistant CE: نشان بده → تأیید | P0 |
| G34 | **Undo برای عملیات مخرب** (حذف عضو، تغییر مالی) | اعتماد مربی | P1 |
| G35 | **Seed demo data فارسی** | ارائه به سرمایه‌گذار/استاد | P1 |
| G36 | **Test fixtures با جواب معلوم** برای JP7 و Judge | فلسفه CE: measured not asserted | P0 |
| G37 | **لیسانس و attribution screen** | OSS اجباری است | P1 |
| G38 | **Gender-inclusive + youth guardrails** | زیر ۱۸ با رضایت ولیی | P0 |
| G39 | **Waist-hip, neck, blood pressure optional** | مکمل JP7 | P2 |
| G40 | **Offline map of «why this exercise»** citations | اعتماد علمی | P1 |

## ۳.۲ شکاف‌های مهندسی

| # | مورد | توضیح |
|---|------|-------|
| E01 | **OpenAPI-first** | یک `openapi.yaml` منبع حقیقت برای Flutter و React |
| E02 | **Migration runner** (Alembic یا equivalent) | schema.sql خام کافی نیست |
| E03 | **Job system** برای AI طولانی | مثل CE tasks + WS progress + Cancel |
| E04 | **Client timeout budget** | CE با ۳۰s timeout سوخت؛ MP همان درس را از روز اول بگیرد |
| E05 | **Deterministic PDF** | همان داده → همان هش PDF در تست |
| E06 | **Content Security برای Electron** | preload bridge مثل CE |
| E07 | **Signed QR payloads** (HMAC/Ed25519) | QR جعلی = ورود رایگان |
| E08 | **Rate limit محلی روی check-in** | ضد اسپم اسکن |
| E09 | **PII encryption at rest** (SQLCipher یا field-level) | کد ملی، اثرانگشت hash |
| E10 | **Fingerprint فقط template/hash** نه تصویر خام | الزام حریم خصوصی |
| E11 | **Separate processes**: UI / API / AI worker | کرش Ollama کل UI را نکشد |
| E12 | **Feature flags فایل محلی** | rollout تدریجی |
| E13 | **msix/nsis + Android APK pipeline** | الگوی GitHub Actions CE |
| E14 | **Differential update فقط برای app**؛ KB جدا | وگرنه پچ ۵۰۰MB می‌شود |
| E15 | **Clock skew handling** | تاریخ شمسی/میلادی روی دستگاه‌های اشتباه |

## ۳.۳ شکاف‌های دانش علمی (برای «کلیشه‌ای نبودن»)

نقشه گفته «دیتابیس علمی وسیع» ولی منبع داده را مشخص نکرده:

| بسته دانش | محتوا | منبع پیشنهادی |
|-----------|-------|----------------|
| KB-EX | حرکات + عضله + تجهیز + منع | free-exercise-db (MIT) + ترجمه فارسی |
| KB-CORR | حرکات اصلاحی / upper-cross / knee valgus | پروتکل‌های متنی curate + RAG |
| KB-PROG | مدل‌های برنامه‌نویسی (PPL, UL, Full, Block) | rule templates نسخه‌دار |
| KB-NUT-IR | غذای ایرانی + واحد خانگی | curate دستی + OFF subset |
| KB-NUT-US | USDA SR legacy subset | public domain |
| KB-PAPERS | چکیده مقالات (نه PDF کامل لزوماً) | متون مجاز / خلاصه خودی |
| KB-SAFE | red-flag پزشکی | لیست قاعده‌ای (chest pain, …) → ارجاع پزشک |

---

<a id="4"></a>
# ۴. چه چیزهایی از Cutting Edge الگوبرداری می‌شود

> **روش:** ایده و ساختار را در `mp-app/` پیاده می‌کنیم.  
> **ممنوع:** edit مستقیم `ce-app/**` و `docs/CuttingEdge/**`.

## ۴.۱ ماتریس الگوبرداری

| جزء CE (مسیر خواندنی) | patttern برای MP | سطح reuse |
|----------------------|------------------|------------|
| `ce-app/` monorepo: backend + frontend + scripts + Actions | همان اسکلت `mp-app/` | ⭐⭐⭐⭐⭐ ساختار |
| FastAPI + SQLite + port محلی | MP Core API | ⭐⭐⭐⭐⭐ |
| `core/brain/*` : objective, planners, race, meaning | Sports Brain: rule vs Ollama vs score | ⭐⭐⭐⭐⭐ **مهم‌ترین** |
| `core/assistant/planner.py` whitelist ops + validate + dry-run | AI برنامه فقط از ops مجاز (addExercise, setSets, …) | ⭐⭐⭐⭐⭐ |
| Job/task + WebSocket progress + Cancel | تولید برنامه AI / import KB / backup | ⭐⭐⭐⭐⭐ |
| `AiRuntimeCard` + Ollama optional | کارت «موتور هوش مصنوعی باشگاه» | ⭐⭐⭐⭐⭐ |
| `UpdateCard` + `electron-updater` + GitHub Releases | Delta/in-app update MP | ⭐⭐⭐⭐⭐ |
| `GpuCard` / one-button GPU | اجرای مدل روی GPU ویندوز | ⭐⭐⭐⭐ |
| i18n fa/en + Vazirmatn | UI دو زبانه باشگاه | ⭐⭐⭐⭐⭐ |
| Ant Design + Page shell + launcher home | Super-app launcher: اعضا / پیکرسنجی / AI / مالی | ⭐⭐⭐⭐ |
| Zustand store + React Query | state کلاینت | ⭐⭐⭐⭐ |
| preload bridge امن Electron | API محلی بدون nodeIntegration | ⭐⭐⭐⭐⭐ |
| `tests/*` با جواب معلوم + browser checks | JP7 fixtures + attendance tests | ⭐⭐⭐⭐⭐ فلسفه |
| ROADMAP «هر ریلیز یک عدد» | ROADMAP_MP با metric | ⭐⭐⭐⭐⭐ |
| OSS licence hygiene (رد GPL داخل پروسس) | همان برای MP | ⭐⭐⭐⭐⭐ |
| Offline-first، بدون cloud processing | اصل محصول | ⭐⭐⭐⭐⭐ |
| Installer slim + on-demand heavy engines | Whisper-like: مدل‌های بزرگ on-demand | ⭐⭐⭐⭐ |
| STATE.md به‌عنوان حافظه پروژه | `docs/MuscleParadise/STATE.md` | ⭐⭐⭐⭐ |

## ۴.۲ چیزهایی که از CE **برنمی‌داریم** (دامنه اشتباه)

| CE | چرا به MP نمی‌آید |
|----|-------------------|
| FFmpeg timeline / NLE | دامنه ویدیو است |
| Whisper / scene detect / Demucs | مگر بعداً برای «ویدیو فرم حرکت» فاز دور |
| Style Match templates | — |
| MovieLite / MLT | — |
| YouTube uploader | مگر مارکتینگ جدا |

## ۴.۳ الگوی Brain که عیناً به MP ترجمه می‌شود

```
measurements (JP7 numbers, history delta, goals, limits, equipment)
        │
prompt/goal ──►  planners: Rules · Ollama(+RAG) · (model2)
        │
        ▼
 validator (whitelist program ops + clamps: sets 1–10, rest 30–300, …)
        │
        ▼
 judge score (when target exists):
   · calorie error        ×3
   · muscle balance       ×2
   · respects limitations ×3
   · equipment available  ×3
   · novelty vs last plan ×1
   · progressive overload ×2
        │
        ▼
 dry-run UI → user confirm → one undoable apply
```

## ۴.۴ الگوی UI/Launcher پیشنهادی MP (از CE super-app)

```
خانه MP
├── 👥 اعضا
├── 📏 پیکرسنجی
├── 🤖 مربی هوشمند (AI)
├── 🏋️ برنامه تمرینی
├── 🥗 تغذیه
├── 🚪 ورود/خروج
├── 💰 مالی
├── 📊 گزارش‌ها
├── 🔄 همگام‌سازی
├── 🧠 موتور AI (وضعیت Ollama/مدل/KB)
├── ⬆️ به‌روزرسانی
└── ⚙️ تنظیمات باشگاه
```

---

<a id="5"></a>
# ۵. کاتالوگ اوپن‌سورس واقعی برای import

> فقط مواردی که **وجودشان و لایسنس‌شان** برای استفاده عملی معنی‌دار است.  
> قبل از کپی کد: `LICENSE` فایل را در attribution بیاور.

## ۵.۱ هسته اپ و زیرساخت (الگوی CE + مکمل)

| نیاز | پروژه | لایسنس | نحوه استفاده در MP |
|------|-------|--------|-------------------|
| Desktop shell | Electron + electron-builder | MIT | مثل CE |
| Auto update | `electron-updater` | MIT | مثل CE UpdateCard |
| UI | Ant Design 5 + lucide-react | MIT | مثل CE |
| Local API | FastAPI + Uvicorn | MIT | مثل CE |
| DB | SQLite + SQLAlchemy یا stdlib sqlite3 | Public | CE بعداً SQLAlchemy را حذف کرد؛ MP می‌تواند stdlib+migrations |
| State | Zustand / TanStack Query | MIT | مثل CE |
| Charts | Recharts یا @ant-design/charts | MIT | پیشرفت BF% |
| PDF | reportlab (Py) یا @react-pdf/renderer | MIT/الکی | فاکتور + برنامه |
| i18n font | Vazirmatn (`rastikerdar/vazirmatn`) | OFL | مثل CE |
| Jalali | `moment-jalaali` یا `dayjs` + jalali plugin | MIT | تاریخ شمسی |
| QR | `qrcode` + `html5-qrcode` / `zxing` | MIT/Apache | check-in + sync |
| CRDT delta | **Yjs** یا **Automerge** | MIT | sync چنددستگاه |
| Embeddings RAG | `chromadb` (PC) یا **lancedb** / sqlite-vss | Apache/MIT | KB |
| Local LLM | **Ollama** | MIT | AI |
| Vector small | `sentence-transformers` on-demand | Apache | embedding فارسی با مدل مناسب |

## ۵.۲ فیتنس / حرکت / تغذیه (دامنه MP)

| نیاز | پروژه | لایسنس | هشدار | استفاده |
|------|-------|--------|-------|---------|
| دیتابیس حرکات JSON ~800 | [`yuhonas/free-exercise-db`](https://github.com/yuhonas/free-exercise-db) | **MIT** | — | **seed اصلی exercises** |
| حرکات + ویدیو دمو | [`amiinwani/free-exercise-db-with-videos`](https://github.com/amiinwani/free-exercise-db-with-videos) / zenithfits | **MIT** (متادیتا) | ویدیو را جدا بررسی حق نشر | assets آفلاین اختیاری |
| workout manager کامل | [`wger-project/wger`](https://github.com/wger-project/wger) | **AGPL-3** | ❌ کد را داخل MP قاطی نکن مگر کل MP را AGPL کنی | ایده UX + API shape؛ داده CC جدا |
| gym management + QR attendance | [`RJGATON007/gyms`](https://github.com/RJGATON007/gyms) | بررسی LICENSE | کد Tkinter قدیمی | ایده QR expire-on-membership |
| QR attendance LAN | [`AzeemIdrisi/QR-Attendance-System`](https://github.com/AzeemIdrisi/QR-Attendance-System) | بررسی | Django | ایده نمایش QR روی مانیتور |
| GYM One | [`mayerbalintdev/GYM-One`](https://github.com/mayerbalintdev/GYM-One) | OSS | PHP stack | ایده ماژول‌های باشگاه |
| Laravel gymie | [`lubusIN/laravel-gymie`](https://github.com/lubusIN/laravel-gymie) | OSS | PHP | ایده CRM عضو |
| self-host tracker | openGym (GitLab mirrors) | بررسی | — | heatmap فعالیت، passkey ایده |
| Android fitness log | [`brodeurlv/fastnfitness`](https://github.com/brodeurlv/fastnfitness) | OSS | Java | ایده UX لاگ ست |
| غذا جهانی | [Open Food Facts](https://world.openfoodfacts.org/data) | ODbL | share-alike برای DB | subset آفلاین ایران+جهان |
| غذا علمی US | [USDA FoodData Central](https://fdc.nal.usda.gov/) | Public domain | — | macros پایه |
| comprehensive food DB | [`lxaw/ComprehensiveFoodDatabase`](https://github.com/lxaw/ComprehensiveFoodDatabase) | بررسی | — | research seed |

## ۵.۳ فرمول و ابزار پیکرسنجی

| مورد | منبع | یادداشت |
|------|------|---------|
| JP7 / JP3 equations | Jackson & Pollock 1978/1985 (literature) | در کد خودت پیاده کن؛ تست واحد با اعداد طلایی |
| Siri / Brozek | literature | هر دو را در assessment نگه دار |
| ماشین‌حساب مرجع برای QA | topendsports / super-calculator صفحات JP | فقط برای **verify** نه کپی UI |
| اپ کلینیکال skinfold | Plixi (proprietary) | فقط benchmark UX — کد نگیر |

## ۵.۴ موبایل / بیومتریک / P2P

| نیاز | پروژه/پکیج | لایسنس | استفاده |
|------|------------|--------|---------|
| Fingerprint/Face | `local_auth` (Flutter) | BSD | ورود مربی/عضو |
| QR Flutter | `qr_flutter` + `mobile_scanner` | MIT/Apache | |
| BT/WiFi Direct | `nearby_connections` | Apache | sync Android↔Android |
| Secure storage | `flutter_secure_storage` | BSD | PIN/token |
| Local DB | `sqflite` / `drift` | MIT | |
| Charts | `fl_chart` | MIT | |
| PDF | `pdf` + `printing` | Apache | |

## ۵.۵ چیزهایی که **عمداً وارد نمی‌کنیم**

| مورد | دلیل |
|------|------|
| هر SaaS ابری اجباری | خلاف خواسته |
| GPL/AGPL داخل پروسس اصلی (RMBG, برخی TTS, wger core) | آلودگی لایسنس — درس CE |
| مدل‌های غیرتجاری / research-only | نصب‌کننده عمومی |
| اسکراپر bodybuilding.com | ToS و شکنندگی |
| اثرانگشت خام ابری | حریم خصوصی |

## ۵.۶ بستهٔ «Knowledge Pack» قابل دانلود (طراحی MP)

```
mp-kb-YYYY.MM/
├── manifest.json          # version, hash, locale
├── exercises.sqlite       # from free-exercise-db + FA translation
├── foods_ir.sqlite        # Iranian foods curated
├── foods_usda_subset.sqlite
├── corrective_rules.json
├── program_templates.json # PPL/UL/FB versioned
├── rag/
│   ├── embeddings.lance
│   └── chunks.jsonl
└── LICENSE-ATTRIBUTION.md
```

آپدیت تفاضلی: `manifest` + binary diff فقط روی بخش‌های عوض‌شده (نه کل اپ).

---

<a id="6"></a>
# ۶. نقشه وابستگی ماژول‌ها (ترتیب ساخت بدون دوباره‌کاری)

```
                    [0] Contracts + Schema + Design tokens
                                    │
                    [1] MP Core API (FastAPI+SQLite+auth PIN)
                                    │
              ┌─────────────────────┼─────────────────────┐
              ▼                     ▼                     ▼
        [2] Members           [3] JP7 Engine        [4] Desktop shell
        CRUD+QR               formulas+tests         (CE pattern UI)
              │                     │                     │
              └──────────┬──────────┘                     │
                         ▼                                │
                  [5] Assessment history + charts  ←───────┘
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
   [6] Attendance   [7] Payments   [8] Equipment inventory
          │              │              │
          └──────────────┼──────────────┘
                         ▼
              [9] Rule-based program builder  (بدون AI)
                         │
                         ▼
              [10] AI Brain race + dry-run + RAG KB
                         │
          ┌──────────────┼──────────────┐
          ▼              ▼              ▼
   [11] Nutrition   [12] PDF/Export  [13] Flutter member app
                         │
                         ▼
              [14] Sync fabric (QR→BT→WiFi→file)
                         │
                         ▼
              [15] Updater + KB packs + installer
                         │
                         ▼
              [16] Hardening, audit, demo, docs, thesis packaging
```

### قانون وابستگی
- **AI بعد از Rule builder** می‌آید (مثل CE: rule همیشه در race).
- **Sync بعد از tombstone/audit fields** در schema.
- **Flutter بعد از پایدار شدن OpenAPI** (یک‌بار codegen).
- **Nutrition بعد از JP7** چون Katch-McArdle به LBM نیاز دارد.

---

<a id="7"></a>
# ۷. قرارداد داده مشترک (Shared Contracts) — حداقل‌ها

## ۷.۱ شناسه‌ها
- `gym_id`, `device_id`, `member_id` → UUID یا ULID
- همه جداول: `created_at`, `updated_at`, `deleted_at`, `rev` (monotonic)

## ۷.۲ QR Member payload (مثال)
```json
{
  "v": 1,
  "typ": "mp.member.checkin",
  "gym": "ulid…",
  "mid": "ulid…",
  "exp": 1893456000,
  "sig": "base64…"
}
```

## ۷.۳ Program JSON v1 (whitelist)
```json
{
  "schema": "mp.program/v1",
  "meta": {"goal": "cut", "weeks": 8, "split": "PPL"},
  "days": [
    {
      "name": "Push A",
      "items": [
        {
          "op": "addExercise",
          "exercise_id": "ex_bench_press",
          "sets": 4,
          "reps": "6-8",
          "rir": 2,
          "rest_s": 180,
          "notes_fa": "کتف‌ها جمع"
        }
      ]
    }
  ],
  "citations": ["kb:prog:ppl-block-v3"]
}
```

هر `op` خارج از whitelist → drop (الگوی CE).

## ۷.۴ Assessment result
```json
{
  "schema": "mp.assessment/v1",
  "protocol": "JP7",
  "sites_mm": {"chest": 12, "midax": 10, "tri": 14, "subsc": 15, "abd": 22, "supra": 18, "thigh": 20},
  "age": 28,
  "sex": "M",
  "weight_kg": 82.4,
  "bd": 1.0712,
  "bf_siri": 12.1,
  "bf_brozek": 11.8,
  "fm_kg": 9.97,
  "lbm_kg": 72.43,
  "class": "athletic"
}
```

---

<a id="8"></a>
# ۸. چک‌لیست روز صفر اجرایی

```text
□ پوشه mp-app/ جدید (نه داخل ce-app)
□ docs/MuscleParadise/STATE.md + ROADMAP_MP.md
□ openapi.yaml خالی با /health
□ schema.sql + migrations + gym_id از روز اول
□ پیاده‌سازی jp7.py با ۱۰ fixture طلایی (مرد/زن، چند سن)
□ Electron hello + FastAPI 8751 + UpdateCard کپی‌الگویی
□ Seed exercises از free-exercise-db (MIT) + ۳۰ حرکت ترجمه‌شده فارسی
□ AiRuntimeCard: detect Ollama, pull list, timeout, cancel
□ هیچ commitای روی docs/CuttingEdge و ce-app
```

### متریک‌های «انجام شد» (فلسفه CE)

| قابلیت | عدد موفقیت |
|--------|------------|
| JP7 | خطا نسبت به fixture طلایی < 0.05 %BF |
| Check-in QR | < 800 ms از اسکن تا OK روی LAN |
| AI program | بدون Ollama هم 100% برنامه rule برمی‌گردد |
| AI program با Ollama | score ≥ rule روی fixture؛ هرگز پایین‌تر اگر model بد حرف بزند |
| Backup restore | restore روی DB خالی → row count یکسان |
| Update | پچ اپ < 50 MB برای تغییرات UI معمول |
| KB pack | نصب آفلاین از USB بدون اینترنت |

---

# ۹. جمع‌بندی خلاقانه — MP در یک جمله معماری

> **Muscle Paradise = Cutting Edge Brain pattern × Gym OS domain × Local Knowledge Packs**  
> یعنی: همان نظم «اندازه‌گیری قطعی + planner رقابتی + dry-run + آپدیت تفاضلی + بدون ابر اجباری»،  
> اما به‌جای تایم‌لاین ویدیو: **عضو، کالپر، برنامه، غذا، درب باشگاه، پول.**

### اولویت ساخت این ماه (اگر فقط یک مسیر)

1. **JP7 + Members + PDF report** (هسته پایان‌نامه و باشگاه تو)  
2. **Rule program builder + equipment filter**  
3. **Ollama race + dry-run** (الگوی CE)  
4. **QR check-in + payments ساده**  
5. **KB pack v0 از free-exercise-db**  
6. بعد Flutter member  

---

# ۱۰. ارجاعات سریع OSS

- free-exercise-db: https://github.com/yuhonas/free-exercise-db  
- free-exercise-db-with-videos: https://github.com/amiinwani/free-exercise-db-with-videos  
- wger (ایده/AGPL): https://github.com/wger-project/wger  
- gyms QR: https://github.com/RJGATON007/gyms  
- QR attendance: https://github.com/AzeemIdrisi/QR-Attendance-System  
- GYM One: https://github.com/mayerbalintdev/GYM-One  
- gymie: https://github.com/lubusIN/laravel-gymie  
- Yjs: https://github.com/yjs/yjs  
- Automerge: https://github.com/automerge/automerge  
- Ollama: https://github.com/ollama/ollama  
- Open Food Facts data: https://world.openfoodfacts.org/data  
- USDA FDC: https://fdc.nal.usda.gov/  
- Vazirmatn: https://github.com/rastikerdar/vazirmatn  
- Cutting Edge (الگوی داخلی، بدون تغییر): `ce-app/`, `docs/CuttingEdge/`

---

**پایان شماتیک اجرایی v1.0**  
مسیر فایل: `docs/MuscleParadise/EXECUTIVE_SCHEMATIC_v1.md`  
وضعیت Cutting Edge: **دست‌نخورده ✅**
