# 🗺️ نقشه مهندسی کامل Cutting Edge v1.4.0 — بازتولید از صفر تا انتشار EXE + Finn-Loop v3

> **سند مرجع:** این نقشه طوری نوشته شده که فردی با **صفر دانش** دربارهٔ برنامه، بتواند از هیچ،
> کامل‌ترین نسخهٔ برنامه (برابر v1.4.0) را بازتولید کند، آن را به‌صورت نصبی EXE ویندوز منتشر کند،
> و سپس با لوپ خودکار **Finn-Loop v3** (n8n + OmniRoute) توسعه را بدون حضور انسان ادامه دهد.
>
> تاریخ سند: ۲۰۲۶-۰۸-۳۱ · نسخهٔ برنامه: **1.4.0** · نگارنده: ایجنت Arena (جلسهٔ `arena/01a057ca-chat2db`)

---

## بخش ۰ — این برنامه چیست؟ (شناسنامه)

**Cutting Edge (CE)** یک **استودیوی تدوین و برش ویدیو با هوش مصنوعی برای ویندوز** است؛ شعار آن
*«Clip smarter, not harder»*. ویدیوی بلند می‌گیرد (فایل یا یوتیوب)، آن را تحلیل می‌کند
(رونویسی گفتار، سکوت‌ها، سکانس‌ها، چهره، ضرب‌آهنگ)، بهترین لحظه‌ها را برش می‌زند، با
**تایم‌لاین چندلایهٔ حرفه‌ای** قابل ویرایش است (کی‌فریم، ترنزیشن، زیرنویس کی‌راوک فارسی،
کالرگرید، عنوان‌بندی) و خروجی را برای شبکه‌های اجتماعی (9:16 و…) رندر و منتشر می‌کند.

| شناسه | مقدار |
|---|---|
| **آخرین نسخه** | **v1.4.0** (منتشرشده ۲۰۲۶-۰۸-۳۱) |
| **دانلود مستقیم نصبی EXE** | https://github.com/yousefghorbanian98-create/Chat2DB/releases/download/v1.4.0/Cutting-Edge-Setup-1.4.0.exe |
| **فایل آپدیت تفاضلی** | https://github.com/yousefghorbanian98-create/Chat2DB/releases/download/v1.4.0/latest.yml |
| **صفحهٔ ریلیز** | https://github.com/yousefghorbanian98-create/Chat2DB/releases/tag/v1.4.0 |
| **محل توسعهٔ سورس v1.4.0** | https://github.com/yousefghorbanian98-create/Chat2DB/tree/arena/01a032fb-chat2db/ce-app |
| **اسناد مهندسی (۳۳ سند)** | https://github.com/yousefghorbanian98-create/Chat2DB/tree/arena/01a032fb-chat2db/docs/CuttingEdge |
| **آخرین کامیت v1.4.0** | `933b0b3` — big-bang loading + starfield + BlazeFace reframe + caption guards |
| **حجم نصبی** | ۳۵۰٫۲۷۸٫۹۸۰ بایت (≈۳۳۴MB) |
| **منبع حقیقت نسخه** | `ce-app/frontend/package.json → "version"` (قانون ۷ AGENTS.md) |
| **ریپوی مادر (فورک)** | `yousefghorbanian98-create/Chat2DB` |
| **ریپوی تولد پروژه** | `yousefghorbanian98-create/Cutting-Edge-Studio` (نسخهٔ 0.2.0) |

---

## بخش ۱ — شجره‌نامهٔ کامل نسخه‌ها و محل‌ها (نتیجهٔ گشت کامل گیت‌هاب)

| نسخه | محل دقیق | لینک | وضعیت |
|---|---|---|---|
| **0.2.0** (تولد) | ریپوی Cutting-Edge-Studio، برنچ `main` + فایل `CuttingEdge-Studio-v0.2.0.bundle` | https://github.com/yousefghorbanian98-create/Cutting-Edge-Studio | اولین سورس؛ هر دو بیلد CI شکست خورد (مرحلهٔ npm در Actions) |
| 0.2.0 (نسخهٔ دوم) | فورک Chat2DB، برنچ `arena/01a01e05-chat2db` → پوشه‌های `cutting-edge-build/` و `ce-app/` + `CuttingEdge-v0.2.0-full.zip` | https://github.com/yousefghorbanian98-create/Chat2DB/tree/arena/01a01e05-chat2db | نسخهٔ بازسازی‌شده |
| **0.9.6** | فورک Chat2DB، برنچ `main` → `ce-app/` | https://github.com/yousefghorbanian98-create/Chat2DB/tree/main/ce-app | بلوغ معماری: ۲۷ روتر، Brain، ۶۵ تست |
| 0.9.32 → 0.9.51 | ریلیزهای فورک Chat2DB (۲۰+ نصبی) | https://github.com/yousefghorbanian98-create/Chat2DB/releases | خط تولید ریلیز خودکار |
| 1.0.0 → 1.3.0 | ریلیزهای فورک (۴ نصبی + blockmap + latest.yml) | همان صفحهٔ Releases | رسیدن به ۱.۰ |
| **1.4.0 ⭐ آخرین** | برنچ `arena/01a032fb-chat2db` → `ce-app/` | https://github.com/yousefghorbanian98-create/Chat2DB/tree/arena/01a032fb-chat2db/ce-app | **مرجع بازتولید این سند** |
| پروتوتایپ EasyClip | برنچ‌های `Gif`/`Voice`/`Gym-legs`/`main` فورک → `easyclip-desktop/` (Tauri 2 + React 19، نسخهٔ 0.1.0) | https://github.com/yousefghorbanian98-create/Chat2DB/tree/main/easyclip-desktop | آزمایش Tauri؛ وارد محصول نشد |
| وب‌اپ «راهنمای توسعه» | برنچ `Gif` → `video-editing-app-roadmap (1).zip` (اپ Next.js با `roadmap-data.ts` ۱۱۹۹ خطی) | — | نقشهٔ راه ۷ فاز به فارسی؛ منبع ایدهٔ فازها |
| ابزارهای جانبی | برنچ `YouTube` → `youtube-content-repurposing-tool.zip`، `youtube-content-scraper-app.zip` (Next.js) | — | ابزارهای وب جدا از محصول |

**خانوادهٔ محصول در یک نگاه:** ویندوز دسکتاپ (Electron 31 + React 18 + Vite 5) ⇄ بک‌اند محلی
(FastAPI + SQLite روی پورت **8742**) ⇄ موتور رندر (FFmpeg با `filter_complex` واحد، NVENC
در صورت وجود GPU) ⇄ لایهٔ هوش (faster-whisper، silero-vad، MediaPipe/BlazeFace، RapidOCR،
LLM از طریق Ollama/OpenAI/Gemini/Anthropic).

---

## بخش ۲ — معماری کلی

```
┌──────────────────────────── Electron Shell (ویندوز) ───────────────────────────┐
│  Home (لانچر + LiveGlobe + Starfield) │ Studio (ادیتور) │ StyleMatch │ Settings │
│  Doctor │ Dashboard │ Workflows │ Uploads │ NewJob │ JobDetail │ ClipReview     │
│  store/runtime.ts + runtime/RuntimeBridge.tsx  ← کارهای طولانی اینجا (قانون ۶) │
│  preload.ts (contextBridge) → IPC: update:check/download/install               │
│  electron/updater.ts (electron-updater + blockmap = آپدیت تفاضلی)              │
│  electron/main.ts: اسپاون بک‌اند + تزریق CE_FFMPEG_DIR + پنجرهٔ 1440×900       │
└───────────────┬─────────────────────────────────────────────────┬──────────────┘
        HTTP /api/* │                              WebSocket /ws ◄─│ پیشرفت زنده
┌───────────────────▼──────────── FastAPI (:8742) ───────────────▼──────────────┐
│  routers (۲۷): jobs clips ai assistant agent analyze audio board brain        │
│   captions emotion engines extend gpu jobs media motion multicam ocr paths    │
│   projects providers reframe render sounds style system tasks titles          │
│   transcript uploads vad vision workflows (+ health, ws)                      │
│  core/brain: intake→meaning→objective→planners→race→critic→memory  («مغز»)   │
│  core/assistant: chat + planner + providers (ollama/openai/gemini/anthropic)  │
│  core/engine (۴۰+ ماژول): compose(رندر) style(۷۲KB) gpu analyze transcribe    │
│   vad reframe face pose ocr emotion intent multicam rife transnet subtitles   │
│   assfile titles chapters dna proxy proxy sounds persian ...                  │
│  core/mcp_server.py (سرور MCP) · core/tasks.py · core/workflows.py            │
│  services/pipeline.py: ingest→prepare→transcribe→select→reframe→subtitle→export│
│  SQLite (WAL): jobs / clips / stages / settings / uploads  در ~/CuttingEdge   │
└──────────────────────────────┬─────────────────────────────────────────────────┘
                               │ subprocess
                 FFmpeg + ffprobe (باندل‌شده، مسیر: CE_FFMPEG_DIR)
                 مدل‌ها: whisper/vad/ocr/runtime در ~/CuttingEdge/runtime/py
```

**قواعد معماری که خراب‌کردنشان = مرگ محصول:**
1. هر کار طولانی (سوکت/تایمر/آپلود) در فرانت فقط در `store/runtime.ts` + `RuntimeBridge.tsx` — تا عوض‌کردن تب، کار را لغو نکند.
2. نسخه فقط در `ce-app/frontend/package.json`؛ بک‌اند همان را می‌خواند (در بیلد: `CE_VERSION`).
3. زبان مبدأ UI انگلیسی است؛ رشته‌ها همیشه `t('English','فارسی')` از `src/i18n` — هرگز هاردکد.
4. هیچ وابستگی GPL به پروسه لینک نمی‌شود (بخش ۸).
5. ادعا ≠ اثبات: هر قابلیت باید تست مرجع داشته باشد (بخش ۹).

---

## بخش ۳ — پشتهٔ فناوری دقیق

| لایه | فناوری | نسخه | نقش |
|---|---|---|---|
| شل | Electron | 31 | پنجره، آپدیت، اسپاون بک‌اند، native save dialog |
| UI | React | 18.3 | همهٔ صفحات |
| بیلد UI | Vite | 5 | dev server 5173 + build |
| زبان | TypeScript | 5.5+ | strict |
| استایل | CSS خالص + توکن‌ها | `design-tokens.css` + `global.css` (~۱۰۴KB) | سیستم طراحی Hybrid |
| انیمیشن | CSS + rAF + three.js | LiveGlobe/Starfield | موشن برنامه |
| فونت | @fontsource/vazirmatn | آفلاین | فارسی/RTL |
| API کلاینت | axios + fetch(NDJSON) | — | REST + استریم |
| state | zustand | — | store/runtime |
| بک‌اند | Python | 3.11 (embeddable در نصبی) | — |
| فریم‌ورک | FastAPI + uvicorn | — | REST + WS |
| دیتابیس | SQLite (WAL) | — | jobs/clips/stages/settings/uploads |
| رونویسی | faster-whisper | — | word-timestamps |
| VAD | FFmpeg silencedetect + silero-vad (ONNX 2.2MB) | opt-in از Settings | نقشهٔ گفتار |
| بینایی | opencv-python + mediapipe (+ BlazeFace برای reframe) | — | چهره/پوز/حرکت |
| OCR | RapidOCR 1.4.4 (مدل داخل wheel) | --no-deps در runtime/py | متن روی تصویر |
| AI | ollama / openai / gemini / anthropic SDKs | انتخاب کاربر | قضاوت/دستیار |
| رندر | FFmpeg (gyan full build) + NVENC/libx264 | — | compose تک‌فیلتر |
| زیرنویس | libass (ASS) | — | فارسی صحیح + کی‌راوک |
| آپدیت | electron-updater + blockmap | — | پچ تفاضلی |
| لاگ | electron-log → `%APPDATA%\Cutting Edge\logs` | — | تشخیص |
| CI | GitHub Actions (windows-latest) + uv + کش Electron | — | بیلد/ریلیز |

---

## بخش ۴ — راه‌اندازی از صفر (محیط توسعه) — گام‌به‌گام

> تمام این بخش روی هر ویندوز ۱۰/۱۱ یا حتی لینوکس (برای همهٔ کارها به‌جز بسته‌بندی) کار می‌کند.

**پیش‌نیازها:** Git، Python 3.11، Node.js 20، [اختیاری] FFmpeg محلی، [اختیاری برای سرعت] uv.

```bash
# ۱) دریافت سورس v1.4.0
git clone https://github.com/yousefghorbanian98-create/Chat2DB
cd Chat2DB && git checkout arena/01a032fb-chat2db

# ۲) اسکریپت یک‌کلیکهٔ محیط (venv + ffmpeg استاتیک + npm install)
bash ce-app/scripts/dev-setup.sh
#   ← اگر اینترنت فیلتر است و npm در نصب Electron باینری مرد:
npm config set electron_skip_binary_download=1 && npm install  # تست‌ها به باینری نیاز ندارند

# ۳) بک‌اند (ترمینال ۱)
export CE_FFMPEG_DIR=<repo>/ce-app/.ffmpeg
<repo>/ce-app/.venv/bin/python ce-app/backend/run_backend.py   # :8742

# ۴) فرانت (ترمینال ۲)
cd ce-app/frontend && npm run dev    # vite:5173 + electron

# ۵) اجرای کل تست‌ها (بدون ویندوز هم کار می‌کند)
cd ce-app/backend  && python -m pytest          # ~۲۰۰ تست
cd ce-app/frontend && npm run test:ui           # ui-audit + bridge contract
```

**مسیرهای داده در سیستم کاربر:** ریشهٔ همه‌چیز `~/CuttingEdge/` شامل `work/` (فایل‌های کاری jobها)،
`exports/`، `data/cuttingedge.db`، `projects/*.ceproj`، `config.json`، `runtime/py` (مدل‌ها)،
`motion/` (پک‌های موشن JSON)، `%APPDATA%\Cutting Edge\logs`.

---

## بخش ۵ — بک‌اند، خط‌به‌خط

### ۵.۱ روترها (۲۷ فایل در `backend/app/routers/`)
| روتر | حجم | مسئولیت |
|---|---|---|
| `ai.py` | 20KB | مدیریت ارائه‌دهنده‌ها (ollama/openai/gemini/anthropic)، انتخاب مدل |
| `style.py` | 16KB | Style Match: قالب `.cetemplate` از ویدیوی مرجع |
| `media.py` | 9.4KB | کتابخانه رسانه، پروکسی ۷۲۰p |
| `render.py` | 6.4KB | رندر/اکسپورت (compose) با پیشرفت WS |
| `assistant.py` | 6.3KB | چت دستیار + استریم NDJSON `/api/assistant/chat/stream` |
| `agent.py` | 5.6KB | عامل خودکار روی پروژه |
| `engines.py` | 6.4KB | نصب/وضعیت موتورهای runtime (vad/ocr/...) |
| `captions.py` | 7.2KB | تولید/ویرایش زیرنویس خودکار (شکست خط واقف‌آگاه) |
| `board.py` | 3.9KB | برد کلیپ‌ها |
| `gpu.py` | 2KB | درخواست فعال‌سازی GPU از ویندوز |
| `emotion.py`, `vision.py`, `ocr.py`, `pose.py`-مرتبط | — | تحلیل احساس/تصویر/متن/پوز |
| `multicam.py`, `reframe.py`, `motion.py` | — | چنددوربینه، ری‌فریم ۹:۱۶ هوشمند، موشن |
| `vad.py`, `transcript.py`, `audio.py` | — | VAD/رونویسی/صوت |
| `projects.py`, `paths.py`, `providers.py`, `system.py`, `tasks.py`, `workflows.py`, `titles.py`, `sounds.py`, `extend.py`, `uploads.py`, `clips.py`, `jobs.py`, `analyze.py` | — | CRUD پروژه/کار، مسیرها، اکشن‌های صفحه |

### ۵.۲ «مغز» (`backend/core/brain/`) — سیگنال می‌سنجد، Whisper رونویسی می‌کند، LLM قضاوت می‌کند، حسابِ خالص تصمیم می‌گیرد
| فایل | حجم | نقش |
|---|---|---|
| `intake.py` | 15KB | پرسش‌های مفهومی (نوع/هدف/ریتم/عبارات/طول هدف) |
| `meaning.py` | 6.6KB | معناشناسی رونویسی |
| `objective.py` | 13.8KB | هدف‌گذاری عددی از ورودی کاربر |
| `planners.py` | 16.3KB | برنامهٔ برش (کاندیدها با نمرهٔ بازهٔ کامل ۰..۱) |
| `race.py` | 7.2KB | مسابقهٔ برنامه‌ها و انتخاب برترین |
| `critic.py` | 3.3KB | نقد برنامهٔ برنده |
| `memory.py` | 3KB | حافظهٔ تصمیم‌ها بین جلسات |
| `editor_brain.py` | 17.2KB | مغز ویرایش (توصیهٔ در لحظهٔ ادیتور) |

### ۵.۳ موتورها (`backend/core/engine/` — ۴۰+ ماژول)
مهم‌ترین‌ها: **`compose.py` (۳۷KB) — کل مدل ادیت به یک `filter_complex` FFmpeg**؛
`style.py` (۷۲KB — Style Match و کالرگرید)؛ `gpu.py` (۲۸KB)؛ `analyze.py` (سکوت+سکانس)؛
`transcribe.py`؛ `vad.py`؛ `reframe.py` (+BlazeFace)؛ `face.py`/`pose.py`؛ `ocr.py`؛
`emotion.py`؛ `intent.py`؛ `multicam.py`؛ `rife.py`/`transnet.py` (اینترپول/کات صحنه)؛
`subtitles.py`/`assfile.py` (ASS/کی‌راوک)؛ `titles.py` (۱۵ پریست، فقط ۵ کانال مجاز x,y,scale,rotate,volume؛ `titles.validate()` رد می‌کند)؛
`chapters.py`؛ `audio.py` (نویزگیری + زنجیرهٔ voice-enhance تا ‎-16 LUFS)؛ `persian.py`؛
`proxy.py` (پروکسی ۷۲۰p)؛ `engines.py` (+`_pypi.py` نصب on-demand در `~/CuttingEdge/runtime/py`)؛
`clips_board.py`؛ `export_pack.py`؛ `interchange.py` (OTIO)؛ `dna.py`؛ `attribution.py`؛ `fillers.py`؛ `sounds.py`؛ `whisperx_align.py`؛ `cancellation.py`؛ `features.py`؛ `arc_hook.py`؛ `captions_llm.py`؛ `text_polish.py`؛ `audio_extract.py`؛ `transcript_edit.py`؛ `ingest.py`/`export.py` (yt-dlp/خروجی).

### ۵.۴ زیرساخت
- `services/pipeline.py`: ارکستراتور job — `ingest→prepare→transcribe→select→reframe→subtitle→export` با رکورد `stages` و پیشرفت.
- `websocket/job_events.py`: broadcast پیشرفت زنده به همهٔ کلاینت‌ها.
- `database.py`: SQLite با WAL؛ جدول‌ها: `jobs`، `clips`، `stages`، `settings`، `uploads`.
- `config.py`: pydantic-settings؛ ریشهٔ داده `~/CuttingEdge`؛ خواندن `config.json` کاربر.
- `core/mcp_server.py`: سرور MCP برای اتصال ابزارهای بیرونی.
- `core/tasks.py` + `routers/tasks.py`: مدیریت کارهای پس‌زمینهٔ طولانی (Running Tasks در UI).
- `core/workflows.py`: گردش‌کارهای قابل ثبت.
- ۶۵ فایل تست در `backend/tests/` — هر قابلیت یک تست مرجع (بخش ۹).

---

## بخش ۶ — فرانت‌اند، خط‌به‌خط

### ۶.۱ صفحات (`src/pages/`)
| صفحه | حجم | نقش |
|---|---|---|
| `Home.tsx` | 11.4KB | لانچر: کارت آپدیت، شروع جدید، پروژه‌های اخیر + LiveGlobe + Starfield |
| `Studio.tsx` | 41KB | ادیتور کامل (تایم‌لاین + مانیتور + ابزارها) |
| `StyleMatch.tsx` | 52KB | بازسازی ویدیو در قالب مرجع (`.cetemplate`) |
| `Settings.tsx` | 49KB | همهٔ تنظیمات + موتورها + GPU + موشن‌پک + زبان |
| `Workflows.tsx`, `Doctor.tsx`, `Dashboard.tsx`, `NewJob.tsx`, `JobDetail.tsx`, `ClipReview.tsx`, `Uploads.tsx`, `Attribution.tsx` | — | بقیهٔ صفحات |

### ۶.۲ اجزای ادیتور (`src/editor/`)
`Timeline.tsx` (۲۵KB — چندلایه، فیلم‌استریپ، وِیوفرم، زوم Ctrl+چرخ‌موش، snap، ripple/roll/slip) ·
`EditorToolbar.tsx` (۶۸KB — ریل ابزار: ۱۸ ابزار کلیپ + پنل‌های تودرتو) ·
`PreviewMonitor.tsx` (۲۰KB — پخش واقعی با صدا + اعمال زندهٔ افکت‌ها به‌صورت CSS + کراس‌فید دو لایه) ·
`MediaBin.tsx` · `model.ts` (۳۸KB — مدل سند ادیت: کلیپ‌ها/کی‌فریم‌ها/افکت‌ها) ·
`applyPlan.ts` (اعمال برنامهٔ مغز روی سند) · `transitions.ts` (۲۸ نوع xfade) ·
`CommandPalette.tsx` (Cmd+K) · `AssistantButton.tsx` + `BrainBar.tsx` + `TierPanel.tsx` + `Scoreboard.tsx` ·
`ProjectBar.tsx` + `ProjectAutosave.tsx` (ذخیرهٔ ۲۰ثانیه‌ای `.ceproj` + بازیابی) · `RecorderModal.tsx`.

### ۶.۳ زیرساخت UI
- `components/`: `LoadingScreen` (big-bang)، `LiveGlobe` (سه‌بعدی three.js)، `Starfield`، `GpuCard`، `AiRuntimeCard`، `UpdateCard`، `BackendBanner`، `RunningStrip`، `Page` (پوستهٔ مشترک)، `FullscreenButton` (F11)، `BrandMark`، `Layout`.
- `store/runtime.ts` + `runtime/RuntimeBridge.tsx`: تک‌محل کارهای طولانی (قانون ۶).
- `i18n/index.ts`: `t('English','فارسی')` + RTL/LTR فوری.
- `api/*`: ۲۳ فایل تایپ‌دار — قرارداد کامل با بک‌اند؛ `scripts/check-bridge.mjs` قرارداد را تست می‌کند.
- `styles/design-tokens.css` + `global.css`: سیستم طراحی Hybrid (بخش ۷).

---

## بخش ۷ — سیستم طراحی Hybrid + موشن

- **توکن‌ها:** همهٔ رنگ/شعاع/سایه/زمان در `design-tokens.css`؛ هیچ هگز خام در کامپوننت‌ها.
- **زبان موشن به‌صورت داده:** چهار پک داخلی `cinematic` / `energetic` / `calm` / `celebration` + دراپ‌این JSON از `~/CuttingEdge/motion`. API: `/api/motion/list|params|set|recommend`. چهار پارامتر واقعی: `duration→--m-speed`، `stagger→--m-stagger`، `ease→--m-ease`، `particles→میدان ذرهٔ LiveGlobe`. تست `test_motion.py` روی «متغیری که نوشته می‌شود ولی هیچ CSS نمی‌خواند» مردود می‌کند. (سند: `MOTION_PACKAGES.md`)
- **صحنه‌های امضادار:** LiveGlobe (کرهٔ سه‌بعدی اتصالات با پالس روی کمان‌ها؛ reduced-motion = یک فریم ثابت)، Starfield، LoadingScreen big-bang، playhead با دنباله، waveform beat-glow، zoom-punch.
- **دوگانهٔ زبان:** پیش‌فرض انگلیسی + فارسی، فلیپ LTR/RTL فوری و ماندگار.
- **گیت‌های کیفیت:** Visual (SSIM)، Animation (۱۸ چک)، Taste، a11y (بخش ۹ و لوپ).

---

## بخش ۸ — ۷ قانون غیرقابل‌مذاکره (از `ce-app/AGENTS.md` — عیناً)

1. **قبل از انتشار راستی‌آزمایی:** `python -m pytest` و `npm run test:ui` هر دو باید سبز باشند؛ تغییر بسته‌بندی باید `scripts/smoke-test.ps1` را در CI پاس کند.
2. **«کامپایل شد» ≠ «کار می‌کند»** — دو باگی که به کاربر رسید (بک‌اند خالی، پنجرهٔ سیاه) هر دو بدون خطا کامپایل می‌شدند.
3. باگ‌های تعمیرشدهٔ بخش ۴ `STATE.md` نباید برگردند.
4. **لایسنس مقدس است:** هیچ وابستگی GPL به پروسه لینک نمی‌شود؛ ریپوی بدون فایل لایسنس اصلاً قابل‌کپی نیست.
5. **انگلیسی مبدأ است:** `t('English','فارسی')`؛ هرگز یک زبان هاردکد نشود.
6. کارهای طولانی فقط در `runtime.ts`/`RuntimeBridge`.
7. نسخه فقط در `frontend/package.json`؛ bump نسخه = تریگر ریلیز.

---

## بخش ۹ — تست، گیت‌ها و تضمین کیفیت

| گیت | فرمان | محافظت |
|---|---|---|
| تست بک‌اند | `cd ce-app/backend && python -m pytest` | ~۲۰۰ تست روی ۶۵ فایل (brain/style/compose/gpu/…) |
| تست UI | `cd ce-app/frontend && npm run test:ui` | ui-audit (۸ صفحه) + قرارداد bridge |
| پخش/تایم‌لاین | `node scripts/playback-test.mjs` | صحت پخش/ترنسپورت |
| دودِ بسته‌بندی | `ce-app/scripts/smoke-test.ps1` | نصب واقعی ویندوز |
| آدیت UI بسته‌شده | `scripts/packaged-ui-audit.mjs` | رگرسیون نصبی |
| امنیت | ۱۰ چک (path gate, licence gate, …) | فاز ۶ لوپ |
| کارایی | ۴۰۰+ متریک + CWV + قفل ۶۰fps | فاز ۷ لوپ |
| بصری | اسکرین‌شات vs مرجع (SSIM) | فاز ۹ لوپ |
| انیمیشن | ۱۸ چک‌پوینت | فاز ۱۰ لوپ |
| سلیقه | Taste Skill gate | فاز ۱۱ لوپ |

**محیط تمیز بعد از wipe:** همیشه `bash ce-app/scripts/dev-setup.sh` → دو ترمینال بخش ۴.

---

## بخش ۱۰ — بسته‌بندی، انتشار EXE و آپدیت خودکار (صفر تا دانلود)

1. **ورک‌فلوی ریلیز:** `ce-app/ci/ce-workflow.yml` — روی هر push به هر برنچی که `ce-app/**` را تغییر دهد اجرا می‌شود؛ با job «decide» نسخهٔ `frontend/package.json` را می‌خواند و **فقط اگر ریلیز `v<نسخه>` وجود نداشته باشد** بیلد می‌کند (بدون ریلیز تکراری).
2. **بیلد (windows-latest):** FFmpeg full از gyan → venv با **uv** (سریع‌ترین نصب wheelهای سنگین mediapipe/opencv/ctranslate2) → کپی `app,core,uploaders,run_backend.py` به `build/backend` → `vite build` → کش Electron → `electron-builder --win nsis`.
3. **بستهٔ NSIS:** CPython 3.11 embeddable + باندل FFmpeg/ffprobe + آیکون‌های `build-assets/` + `scripts/before-pack.js` (آماده‌سازی) → خروجی `frontend/release/*.exe`.
4. **انتشار:** `gh release create v<نسخه>` با سه فایل: `Cutting-Edge-Setup-<v>.exe` + `.exe.blockmap` + `latest.yml`.
5. **آپدیت خودکار:** برنامهٔ نصب‌شده در استارتاپ چک ساکت می‌کند + دکمهٔ «بررسی و نصب به‌روزرسانی» → دانلود **تفاضلی فقط blockmap-diff** (چند MB) → نصب بدون حذف.
6. **بیلد دستی محلی:** `powershell -ExecutionPolicy Bypass -File ce-app/scripts/build-installer-local.ps1`.
7. **بیلد سرانگشتی (بدون CI):** در اکشن صفحهٔ ریپو → «🎬 Build Cutting Edge» → Run workflow (`ce-app/.github/workflows/build.yml`) → دانلود Artifact.

---

## بخش ۱۱ — Finn-Loop v3: لوپ خودکار توسعه (n8n + OmniRoute) — بدون حضور انسان

### ۱۱.۱ معماری
```
GitHub (منبع حقیقت) ◄──── کامیت هر مرحله ──────┐
   ▲                                           │
   │ readWriteFile(manifest)                   │ github.createFile(docs/loop/done/<id>.done)
   │                                           │
┌──┴────────────────── n8n (ارکستراتور) ───────┴──────────────────┐
│ Read Manifest → [run-<id> (executeCommand) → mark-<id> (github)]×63 │
│ + Schedule Trigger (هر ساعت؛ ادامه از اولین done-نشده)             │
│ + نود گزارش: docs/loop/report.md (done/pending)                    │
└──────────────────────┬────────────────────────────────────────────┘
                       │ هر ایجنتِ LLM-نیازمند فقط از دروازه:
                       ▼
        OmniRoute (http://localhost:20128/v1) — router مدل‌ها
        (نردبان gateway→ollama→ارزان‌ترین ارائه‌دهندهٔ زنده)
```

### ۱۱.۲ تضمین‌های «هیچ مرحله‌ای گم و فراموش نمی‌شود» (میراث v2 + تقویت v3)
1. **لوپ داده‌است نه حافظه:** فهرست مراحل در `ce-app/ci/finn-loop.manifest.json` داخل مخزن است.
2. **ادامه از اولین done-نشده:** هر اجرا اولین مرحلهٔ بدون `docs/loop/done/<id>.done` را برمی‌دارد؛ پس از wipe یا قطع جلسه از همان‌جا ادامه می‌یابد.
3. **هر مرحله = gate + کامیت:** مرحله فقط با پاس‌شدن gate و رسیدن کامیتِ `*.done` به گیت‌هاب «تمام» می‌شود.
4. **n8n همان manifest را اجرا می‌کند** — ترتیب در ورک‌فلو سخت‌کدشده است؛ پرش ممکن نیست.
5. **گزارش پایانی بعد از هر دور** به `docs/loop/report.md` کامیت می‌شود.
6. **(جدید v3) Watchdog:** اگر ۲ اجرای متوالی یک مرحله شکست بخورد، Self-Healing با پرامپت OmniRoute بازنویسیِ اسکریپتِ همان مرحله را انجام می‌دهد (max ۳ تلاش؛ بعد برچسب `blocked` در گزارش).

### ۱۱.۳ فازهای تکمیل‌شدهٔ v2 (۴۴ مرحله — مرجع تاریخچه)
فاز ۰ ممیزی خط‌به‌خط (۴ مرحله) · ۱ موشن لندینگ (۵) · ۲ موشن StyleMatch (۵) · ۳ موشن ادیتور (۶) ·
۴ یکپارچگی/سرعت (۵) · ۵ دیباگ خودکار (۳) · ۶ امنیت · ۷ کارایی · ۸ دکمه‌به‌دکمه (۳) ·
۹ بصری SSIM · ۱۰ انیمیشن (۱۸ چک) · ۱۱ Taste · ۱۲ Self-Healing · ۱۳ قرارداد/snapshot/feature-flag/i18n/a11y/bundle/افزایشی/changelog (۸) · ۱۴ پابلیش پچ تفاضلی.

### ۱۱.۴ فازهای جدید v3 — «قدرت ادیتور + AI عمیق + موشن کلاس جهانی» (۱۹ مرحلهٔ جدید)

| فاز | شناسه | مرحله | gate | ابزارها |
|---|---|---|---|---|
| **۱۵ ادیتور حرفه‌ای** | 15-0 | Bootstrap: کپی رانتایم v3 روی برنچ هدف از این سند | فایل‌ها موجود | gh api |
| | 15-1 | Keyframe Engine v2: منحنی بزیه/velocity در ادیتور+اکسپورت | `pytest -k keyframes` | bezierjs |
| | 15-2 | ماسک و Blend Modes در compose | parity تست رندر | FFmpeg maskedmerge |
| | 15-3 | Motion Tracking v2: چسباندن متن/شیء به حرکت | دقت روی نمونهٔ تست | mediapipe/pose |
| | 15-4 | پک افکت: blur/depth/glow/shake/preset‌ها | SSIM بصری | FFmpeg gblur/unsharp |
| | 15-5 | Multicam Pro: سوییچ زاویه با کلید + سینک صوتی | e2e | playback-test |
| **۱۶ هوش عمیق** | 16-1 | ارتقای Brain: planner↔critic با حافظهٔ بلندمدت | `pytest -k brain` | — |
| | 16-2 | Assistant v2: استریم + tool-calling whitelist | `pytest -k assistant` | OmniRoute |
| | 16-3 | Auto-Diagnose: خطا→ریشه→پچ پیشنهادی | self-debug سبز | OmniRoute |
| | 16-4 | E2E دکمه‌به‌دکمهٔ عمیق همهٔ صفحات/حالت‌ها | e2e پاس | ui-audit گسترش |
| **۱۷ موشن کلاس جهانی** | 17-1 | Motion Token v2: کتابخانهٔ spring/easing/stagger | anim gate | framer-motion اصول، Design Motion Principles |
| | 17-2 | لندینگ سینمایی: aurora gradient-mesh + cursor spotlight + میدان ذره | visual+taste | particles (سبک casberry) |
| | 17-3 | پالیش میکرواینترکشن دکمه/کارت/تب | anim ۱۸چک | Originkit، 21st.dev |
| | 17-4 | پالیش ادیتور: playhead trail، clip spring، ripple v2 | anim gate | — |
| | 17-5 | گیت کامل Taste + پادِ anti-slop | taste pass | taste-skill |
| | 17-6 | a11y + reduced-motion parity کامل | a11y pass | — |
| **۱۸ انتشار 1.5.0** | 18-1 | گیت حجم bundle+نصبی (بودجه ≤۳۳۶MB) | size | — |
| | 18-2 | Changelog + مستندات + اسکرین‌شات‌های جدید | docs | — |
| | 18-3 | bump به 1.5.0 → ریلیز CI → تأیید آپدیت تفاضلی روی v1.4.0 | release زنده | ce-workflow |

### ۱۱.۵ فایل‌های اجرایی v3 (در همین برنچ، کنار این سند)
- `ce-app/ci/finn-loop.manifest.json` — **نسخهٔ ۳** (۶۳ مرحله؛ ۴۴ انجام‌شدهٔ v2 + ۱۹ جدید)
- `ce-app/ci/finn-loop.n8n.json` — ورک‌فلوی n8n با ۱۲۷ node (آمادهٔ import)
- `ce-app/ci/finn-loop-v3/run_stage.py` — دیسپچر مراحل (خواندن manifest، اجرای gate، گزارش)
- `ce-app/ci/finn-loop-v3/stages/<id>.sh` — اسکریپت واقعی هر مرحلهٔ جدید
- `ce-app/ci/finn-loop-v3/README.md` — راهنمای کوتاه اجرا

---

## بخش ۱۲ — نقشهٔ ابزارها (هر ابزار ← دقیقاً کجا)

| ابزار (از درخواست شما) | مخزن/لینک | جای دقیق در پروژه/لوپ |
|---|---|---|
| Finn-loop | github.com/finna/Finn-loop | اسکلت ۳مهارتی spec→build→review؛ v2/v3 ما بر پایهٔ آن + کامیت هر مرحله |
| n8n-workflows | n8n.io | ارکستراتور ۱۲۷-node (`ce-app/ci/finn-loop.n8n.json`) |
| OmniRoute | github.com/BunsDev/omniroute | دروازهٔ مدل‌ها `localhost:20128/v1`؛ روتینگ ارزان‌ترین ارائه‌دهنده |
| UI/UX Pro Max Skill | github.com/nextlevelbuilder/ui-ux-pro-max-skill | مرجع استایل/پالت/قواعد UX در مراحل Design (فاز ۱۷) |
| Taste Skill | github.com/senlindesign/taste-skill | گیت ۱۷-۵ (anti-slop + quality gate سلیقه) |
| Awesome Claude Design | github.com/rohitg00/awesome-claude-design | مرجع DESIGN.md و زیبایی‌شناسی در مرحلهٔ Design |
| Design-MD (TypeUI) | typeui.sh/design-md | استخراج DESIGN.md از رفرنس‌های بصری برای فاز ۱۷ |
| Find Skills | github.com/travisvn/awesome-claude-skills | کشف اسکیل‌های کمکی در مرحلهٔ Plan |
| Particles (casberry) | particles.casberry.in | مرجع بصری میدان ذرهٔ لندینگ (۱۷-۲) |
| Originkit | github.com/vellum-ai/originkit | ایمپورت کامپوننت‌های انیمیشنی (۱۷-۳) |
| 21st.dev | 21st.dev | ایمپورت کامپوننت‌های پریمیوم (۱۷-۳) |
| Framer Motion / Design Motion Principles | motion.dev | اصول فیزیک فنر/easing در Motion Token v2 (۱۷-۱) |
| DaisyUI | daisyui.com | مرجع نام‌گذاری توکن/کامپوننت (اختیاری؛ سیستم فعلی CSS توکن‌محور است) |

---

## بخش ۱۳ — Runbook: اجرای لوپ از صفر (۱۰ دقیقه، بدون سیستم شما)

1. **OmniRoute:** `docker run -p 20128:20128 bunsdev/omniroute` → کلید ارائه‌دهنده‌ها را در پنل `http://localhost:20128` ثبت کنید.
2. **n8n:** `docker run -p 5678:5678 n8nio/n8n` → Import ← فایل `ce-app/ci/finn-loop.n8n.json` (لینک دانلود در ریلیز همین سند).
3. در nodeهای `mark-*` فقط یک‌بار توکن GitHub (دسترسی content) را در Credentials متصل کنید؛ پارامتر `branch` روی `arena/01a032fb-chat2db` است (خانهٔ v1.4.0).
4. **Activate** ورک‌فلو. Schedule هر ساعت: ادامه از اولین `done-نشده`.
5. انتشار خودکار: مرحلهٔ ۱۸-۳ نسخه را `1.5.0` می‌کند؛ `ce-workflow.yml` خودش می‌سازد و ریلیز می‌دهد؛ نصبی‌های موجود از طریق blockmap آپدیت می‌شوند.
6. پایش بدون حضور: `docs/loop/report.md` و تب Actions ریپو.

---

## بخش ۱۴ — مستر-پرامپت ایجنت‌ها (کپی-پیست برای هر LLM لوپ)

```text
تو ایجنت ساختاریِ Cutting Edge هستی (ریپو: yousefghorbanian98-create/Chat2DB، برنچ arena/01a032fb-chat2db، ریشه: ce-app/).
قوانین:
1) قبل از هر تغییر: ce-app/AGENTS.md و docs/CuttingEdge/STATE.md را بخوان؛ بخش ۴ STATE.md (باگ‌های تعمیرشده) را دوباره نشکن.
2) هر تغییر با scope بسته: فقط فایل‌های مرحلهٔ جاری از ce-app/ci/finn-loop.manifest.json.
3) سبز اجباری: cd ce-app/backend && python -m pytest  و  cd ce-app/frontend && npm run test:ui.
4) نسخه فقط در ce-app/frontend/package.json؛ زبان UI فقط t('English','فارسی').
5) لایسنس: بدون GPL؛ ریپوی بدون لایسنس ممنوع.
6) کار طولانی فقط در store/runtime.ts + RuntimeBridge.
7) مرحله فقط با gate سبز + کامیت docs/loop/done/<id>.done تمام می‌شود؛ در شکست: تشخیص→اصلاح→تلاش مجدد (حداکثر ۳)؛ در بن‌بست: گزارش در docs/loop/report.md.
8) مدل‌های LLM فقط از دروازهٔ OmniRoute (CE_OMNIROUTE_URL).
```

---

## پیوست — فایل‌های همراه این سند (دانلود مستقیم در ریلیز)

| فایل | نقش |
|---|---|
| `ENGINEERING_MAP_V1.4.md` | همین سند |
| `ce-app/ci/finn-loop.manifest.json` (v3) | ۶۳ مرحله با gate/done — منبع حقیقت لوپ |
| `ce-app/ci/finn-loop.n8n.json` (v3) | ورک‌فلوی n8n قابل-import |
| `ce-app/ci/finn-loop-v3/run_stage.py` | دیسپچر اجرای مرحله |
| `ce-app/ci/finn-loop-v3/stages/*.sh` | منطق هر مرحلهٔ جدید |
