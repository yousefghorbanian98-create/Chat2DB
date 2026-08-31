# 🧠 Nemotron-Brain — انویدیا به‌عنوان مغز متفکر Cutting Edge

> **سند طراحی (تأییدشده توسط یوسف قربانیان، ۲۰۲۶-۰۸-۳۱)** — Nemotron به‌عنوان موتور «قضاوت» برنامه،
> با ورود پلکانی و گیت ارزیابی A/B، اولویت نخست: **Style Match**.
> این سند مرجع فاز ۱۹ لوپ Finn-Loop است (`ce-app/ci/finn-loop.manifest.json` → مراحل `19-*`).

---

## ۰) واقعیت سخت‌افزاری (تصمیم‌ساز)

| منبع | سهم شما | نتیجه |
|---|---|---|
| رم سیستم | **۱۶GB** | اجرای لوکال Nemotron 3 Nano (نیاز ~۲۵GB در Q4) ← **غیرممکن** |
| GPU | **GTX 1650 — 4GB** | فقط برای: رندر NVENC H.264/HEVC (برنامه خودش probe می‌کند)، رابط، مدل‌های سبک بینایی (BlazeFace/MediaPipe) که اکنون هم دارید |
| تصمیم | — | **Nemotron فقط ابری**: دروازهٔ رایگان `build.nvidia.com`؛ آفلاین = رفتار فعلی «پاسخ از اندازه‌گیری‌ها» حفظ می‌شود |

**چرا این ترکیب عالی است:** همهٔ کارهای سنگینِ حس‌گر (رونویسی، VAD، سکانس، چهره، ضرب) لوکال و مجانی
می‌مانند و فقط «قضاوت» — که متنِ سبک است — به API می‌رود. ترافیک خروجی هر قضاوت چند کیلوبایت متن
است، نه ویدیو.

---

## ۱) خانوادهٔ Nemotron و نقش هر عضو در برنامه

| مدل | ابعاد | کانتکست | نقش در CE | مسیر |
|---|---|---|---|---|
| **Nemotron 3 Super 120B (A12B)** | ۱۲B فعال | 1M | **پیش‌فرض مغز**: Style Match، planners، critic، دستیار | API رایگان `integrate.api.nvidia.com/v1` |
| **Nemotron 3 Ultra 550B (A55B)** | ۵۵B فعال | 1M | «حالت استودیو» برای قضاوت‌های سخت (race نهایی، نقد عمیق) — اختیاری | همان API |
| Nemotron 3 Nano 31.6B (A3.6B) | ۳.۶B فعال | 1M | رزرو آیندهٔ لوکال (وقتی سخت‌افزار اجازه دهد) | Ollama/vLLM |
| Nemotron 3 Nano-Omni 30B (A3B) | ۳B فعال | 1M | **فاز آیندهٔ بینایی**: دیدن فریم مرجع برای تایپوگرافی/کالرگرید | API (دارای vision) |

- قرارداد API: **OpenAI-compatible** — یعنی `providers.py` فعلی با یک adapter کوچک ساپورت می‌شود.
- لایسنس: **OpenMDW-1.1 / NVIDIA Open Model License** — تجاری مجاز؛ گیت لایسنس برنامه (قانون ۴) پاس.
- کلید: رایگان از `build.nvidia.com` → متغیر `CE_NVIDIA_API_KEY` (یا Settings → AI).

## ۲) نردبان هوش (جای Nemotron در معماری provider)

```
اولویت قضاوت (هر مرحله از بالا به پایین، اولین زنده):
1. nvidia       → Nemotron 3 Super/Ultra   (API رایگان build.nvidia.com)   ★ جدید
2. OmniRoute    → هر ارائه‌دهندهٔ رایگان/ارزان پشت دروازهٔ localhost:20128
3. ollama       → مدل لوکال کاربر (فقط اگر خودش نصب کرده)
4. offline      → پاسخ صرفاً از اندازه‌گیری‌های محاسبه‌شده (رفتار فعلی؛ هرگز حذف نمی‌شود)
```

قواعد تغییرنکردنی:
1. **LLM فقط قضاوت می‌کند؛ اعداد همیشه از اندازه‌گیری می‌آیند.** خروجی مدل باید در اسکیمای
   وایت‌لیست‌شده (JSON) جا شود وگرنه دور انداخته می‌شود و مسیر offline ادامه می‌دهد.
2. هر پاسخ، نام provider را همراه خودش نشان می‌دهد (`nvidia:nemotron-3-super-120b-a12b`) — هرگز پنهان نیست.
3. کنسنت کاربر: چون رونویسی به سرور NVIDIA می‌رود، در Settings کلید «ارسال رونویسی به سرویس ابری»
   به‌صورت پیش‌فرض خاموش است؛ با روشن‌کردن، فقط رونویسی + اعداد (بدون ویدیو/تصویر) ارسال می‌شود.
4. تایم‌اوت ۳۰s، دو retry، سپس fallback خودکار به سطح بعدی نردبان؛ هیچ diálogoUI بلاک نمی‌شود.

## ۳) Style Match با Nemotron (اولویت نخست)

### ۳.۱ خط تولید فعلی (دست‌نخورده می‌ماند)
ویدیوی مرجع → اندازه‌گیری‌ها (silencedetect، سکانس، tempo، OCR تایپوگرافی، نسبتها) → `.cetemplate` (اعداد) → بازسازی با FFmpeg.

### ۳.۲ افزودهٔ Nemotron — «چراییِ سبک»
رونویسی + نقشهٔ اندازه‌گیری‌ها به‌صورت متن فشرده به Super می‌رود و مدل این‌ها را برمی‌گرداند
(همه در قالب JSON وایت‌لیست):

```json
{
  "narrative_rhythm": "hook in first 2.5s, question → payoff loop every ~18s",
  "hook_pattern":     "cold-open on peak motion, then context line",
  "caption_tone":     "short, imperative, 2-4 words per line, karaoke highlight",
  "pacing_verdict":   "cut density follows beat grid at 0.9x energy",
  "keep_phrases":     ["..."], "drop_phrases": ["..."],
  "style_summary_fa": "…", "style_summary_en": "…"
}
```

این فیلدها در **`.cetemplate` نسخهٔ ۲** ذخیره می‌شوند (`nemotron` بخش جدید + `provider` + `model` +
`measured_hash` برای اطمینان از اینکه قضاوت روی همین اندازه‌گیری‌هاست). بازسازی همچنان فقط از
اعداد استفاده می‌کند؛ متن‌های «چرایی» در UI کارت Style Match و برای intake بهتر نمایش داده می‌شوند.

### ۳.۳ گیت ارزیابی A/B (شرط ورود به پیش‌فرض)
روی ۳ ویدیوی fixture (درس/ورزشی/ویلاگ):
| متریک | قدیم (فقط اعداد) | Nemotron | شرط قبولی |
|---|---|---|---|
| پوشش منابع استفاده‌شده (% footage used) | مبنا | مقایسه | ≥ مبنا − ۵٪ |
| تطابق طول هدف | مبنا | مقایسه | بهتر یا مساوی |
| قلاب در ۳ ثانیه اول (تشخیص از رونویسی) | ندارد | دارد | ≥ ۲ از ۳ fixture |
| نرخ undo کاربر در تست دستی | مبنا | مقایسه | کمتر یا مساوی |
گیت: **report تولید شود + هیچ متریک کلیدی بیش از ۱۰٪ بدتر نشود**؛ در غیر این صورت مرحله
Self-Healing می‌گیرد (پرامپت اصلاح می‌شود، نه اعداد).

## ۴) فایل‌های تغییر (فاز ۱۹)

| فایل | تغییر |
|---|---|
| `backend/core/assistant/providers.py` | افزودن سطح `nvidia` به نردبان (OpenAI-compat، `enable_thinking`، استریم) |
| `backend/core/brain/nemotron.py` | **جدید** — adapter قضاوت: build prompt از اندازه‌گیری‌ها → validate JSON → خروجی typed |
| `backend/core/engine/style.py` | تولید بخش `nemotron` در `.cetemplate` v2 + خواندن آن در بازسازی |
| `backend/app/routers/ai.py` و `providers.py` | provider جدید + تست سلامت + نمایش در UI |
| `backend/app/routers/style.py` | endpoint `/api/style/ab` برای گیت A/B |
| `frontend/src/pages/Settings.tsx` | کلید API، کنسنت ارسال رونویسی، انتخاب مدل (Super/Ultra) |
| `frontend/src/pages/StyleMatch.tsx` | کارت «چرایی سبک» + نشان provider |
| `tests/test_providers_nvidia.py`, `test_style_template_v2.py`, `test_ab_harness.py` | **جدید** — همه با mock (بدون نیاز به کلید در CI) |
| `docs/CuttingEdge/PROVIDERS.md`, `STATE.md` | ثبت تصمیم و وضعیت |

## ۵) مراحل فاز ۱۹ در Finn-Loop (id → gate)

| id | مرحله | gate |
|---|---|---|
| `19-0` | سند + کلید/کنسنت در Settings + اسکیمای template v2 | tests + i18n pass |
| `19-1` | NemotronProvider در نردبان (تایم‌اوت/retry/fallback) | `pytest -k providers` |
| `19-2` | `brain/nemotron.py` + بخش nemotron در Style Match v2 | `pytest -k style` |
| `19-3` | هارنس A/B سه fixture + گزارش متریک‌ها | ab report + قاعدهٔ −۱۰٪ |
| `19-4` | پیش‌فرض‌شدن Style Match وقتی کلید+کنسنت هست؛ حفظ offline | `pytest -k brain` |
| `19-5` | گسترش به editor_brain/critic با همان adapter | `pytest -k brain` |
| `19-6` | مستندات (این سند در STATE/PROVIDERS) + changelog | docs |

**بدون کلید چه می‌شود؟** اسکریپت‌های `19-*` اگر `CE_NVIDIA_API_KEY` نبینند، مرحله را
`pending-needs-key` گزارش می‌کنند و لوپ به مرحلهٔ بعدیِ قابل‌انجام می‌رود — گیر نمی‌کند.
دریافت کلید رایگان: https://build.nvidia.com

## ۶) پرامپت ایجنت (ضمیمهٔ مستر-پرامپت بخش ۱۴ نقشهٔ مهندسی)

```text
وقتی روی فاز ۱۹ کار می‌کنی: LLM فقط قضاوت؛ خروجی فقط JSON در اسکیمای وایت‌لیست؛
اعداد همیشه از اندازه‌گیری. provider همیشه در پاسخ نام‌برده می‌شود. بدون کلید:
pending-needs-key، نه شکست. کنسنت ارسال رونویسی خاموشِ پیش‌فرض می‌ماند.
مدل پیش‌فرض: nvidia/nemotron-3-super-120b-a12b (Ultra فقط «حالت استودیو»).
```
