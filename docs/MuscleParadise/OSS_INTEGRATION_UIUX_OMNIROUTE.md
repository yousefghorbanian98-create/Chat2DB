# یکپارچه‌سازی UI/UX Pro Max + OmniRoute در Muscle Paradise

**تاریخ:** 2026-08-28  
**Cutting Edge (`ce-app/`, `docs/CuttingEdge/`):** بدون تغییر ✅  
**لایسنس‌ها:** هر دو پروژه هدف **MIT** اعلام شده‌اند (قبل از ship تجاری attribution را دوباره verify کن).

---

## خلاصه اجرایی

| ابزار | GitHub | چیست؟ | وارد MP می‌شود؟ | چطور؟ |
|-------|--------|--------|-----------------|-------|
| **UI/UX Pro Max Skill** | [nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | پایگاه دانش طراحی برای AI (استایل، رنگ، فونت، UX، stack) | ✅ **بله — الان نصب شد** | skill + design system generator |
| **OmniRoute** | [diegosouzapw/OmniRoute] | Gateway محلی صدها مدل AI روی `localhost:20128/v1` | ⚠️ **بله به‌عنوان لایه توسعه/اختیاری — نه هسته runtime اجباری محصول** | sidecar اختیاری کنار Ollama |

---

# ۱) UI/UX Pro Max — وضعیت نصب در این ریپو

## چه کار می‌کند؟
- skill برای دستیار کدنویس (Claude/Cursor/…)  
- دیتابیس: ده‌ها UI style، palette، typography، chart، UX guideline، راهنمای React/Flutter/…  
- دستور `--design-system` → فایل MASTER برای پروژه

## کجا نصب شد؟ (خارج از Cutting Edge)

```
docs/MuscleParadise/tools/ui-ux-pro-max/     # موتور search + data + LICENSE
.agents/skills/ui-ux-pro-max/                # SKILL.md برای agent
docs/MuscleParadise/design-system/
  └── muscle-paradise/
        MASTER.md                            # DS قفل‌شده برند MP (emerald/gold)
        pages/                               # override صفحات
```

## چطور دوباره جستجو کنی؟

```bash
cd docs/MuscleParadise

# سیستم طراحی کامل
python3 tools/ui-ux-pro-max/scripts/search.py \
  "gym fitness trainer dashboard" --design-system -p "Muscle Paradise" -f markdown

# دامنه خاص
python3 tools/ui-ux-pro-max/scripts/search.py "glassmorphism dark" --domain style
python3 tools/ui-ux-pro-max/scripts/search.py "form validation" --domain ux
python3 tools/ui-ux-pro-max/scripts/search.py "line chart progress" --domain chart

# stack
python3 tools/ui-ux-pro-max/scripts/search.py "touch target navigation" --stack flutter
python3 tools/ui-ux-pro-max/scripts/search.py "accessible form" --stack react
```

## خروجی اصلی برای MP
فایل قفل‌شده برند:

**`design-system/muscle-paradise/MASTER.md`**

نکته مهم: خروجی خام Pro Max برای «fitness» گاهی palette **نارنجی energy** می‌دهد.  
ما آن را با برند واقعی MP (**زمرد `#00B86A` + طلا `#FFD700` + glass dark**) override کردیم — mockupها منبع حقیقت رنگ هستند.

## کاربرد روزمره در توسعه UI
1. قبل از ساخت هر صفحه Studio/Client → بخوان `MASTER.md`  
2. اگر صفحه خاص است → `pages/<name>.md` بساز (override)  
3. چک‌لیست Pre-Delivery را قبل از merge UI تیک بزن  
4. آیکون = Lucide (نه emoji) — قانون Pro Max + CE  

## چه چیزی نیست؟
- **کامپوننت React آماده ship نیست**؛ intelligence برای طراحی است  
- جایگزین Ant Design/Flutter widgets نمی‌شود؛ روی آن‌ها سوار می‌شود  

---

# ۲) OmniRoute — آیا و چگونه؟

## چه کار می‌کند؟
- یک **AI Gateway محلی** (MIT): یک endpoint سازگار OpenAI  
- ده‌ها/صدها provider، fallback خودکار، فشرده‌سازی توکن، dashboard  
- نصب رایج: `npm i -g omniroute` → `http://localhost:20128/v1`  
- مناسب Claude Code / Cursor / ابزارهای توسعه و همچنین appهایی که OpenAI SDK می‌زنند

## تطبیق با معماری MP

```
                    ┌─────────────────────────────┐
  توسعه‌دهنده ──►  │ OmniRoute :20128 (اختیاری)  │──► cloud models / free tiers
                    └──────────────┬──────────────┘
                                   │ فقط اگر OWNER روشن کند
┌──────────────┐                   ▼
│ MP Studio UI │────────► MP Core FastAPI :8751
└──────────────┘                   │
                                   ├─► 1) Rule planner (همیشه، آفلاین)
                                   ├─► 2) Ollama local (پیشنهاد پیش‌فرض محصول)
                                   └─► 3) OpenAI-compatible URL  ← می‌تواند OmniRoute یا Ollama باشد
```

### ✅ جاهایی که OmniRoute ارزش دارد
| سناریو | فایده |
|--------|--------|
| **محیط توسعه / Agent Mode** | مدل‌های قوی‌تر برای نوشتن کد و پرامپت‌تست |
| **باشگاه با اینترنت + OWNER opt-in** | fallback وقتی Ollama ضعیف/خراب است |
| **یک baseURL برای Provider abstraction** | مثل CE: plain HTTP به هر OpenAI-compatible |
| **فشرده‌سازی context برنامه ورزشی طولانی** | RTK/Caveman اگر context KB بزرگ شد |

### ⚠️ جاهایی که نباید هسته اجباری شود
| دلیل | توضیح |
|------|--------|
| قول محصول | Local-first؛ بدون سرور ابری اجباری |
| داده پزشکی/آسیب | پروفایل injury نباید بی‌جهت به API ابری برود |
| کیوسک/باشگاه بدون نت | OmniRoute بدون upstream = خالی؛ Ollama+Rule باید کافی باشند |
| پیچیدگی نصب برای مربی | `npm i -g omniroute` برای end-user سنگین است |
| حجم/سطح حمله | سرویس اضافه روی PC باشگاه |

### قانون محصول پیشنهادی (قفل‌شده)

```
اولویت موتور تولید برنامه:
  1. Rule engine (deterministic)           — همیشه
  2. Ollama local                          — پیش‌فرض AI
  3. Custom OpenAI-compatible endpoint     — اختیاری (OmniRoute / LM Studio / vLLM)
  4. هرگز cloud اجباری؛ هرگز بدون consent برای PII
```

در Settings → **AI Runtime** (الگوی CE AiRuntimeCard):
- [ ] Ollama status  
- [ ] Optional: «Gateway URL» = `http://127.0.0.1:20128/v1`  
- [ ] Toggle: «ارسال داده عضو به gateway» پیش‌فرض **OFF**؛ اگر ON فقط با redact (بدون کدملی/نام کامل در صورت امکان)  
- [ ] Race/Judge مثل CE: اگر gateway بد جواب داد، rule برنده می‌ماند  

## نصب اختیاری (توسعه‌دهنده — نه داخل ce-app)

```bash
# روی ماشین dev — خارج از bundle محصول
npm install -g omniroute
omniroute
# API: http://localhost:20128/v1
# Dashboard: http://localhost:20128
```

در کد MP (آینده `mp-app/backend`):

```python
# pseudocode — provider like CE plain requests
OPENAI_BASE = settings.ai_base_url  # default http://127.0.0.1:11434 (ollama) or :20128
# POST {OPENAI_BASE}/chat/completions
```

**کد OmniRoute را fork داخل باینری MP نکن** مگر نیاز به patch؛ به‌عنوان dependency runtime جدا / documented sidecar نگه دار (لایسنس MIT + attribution).

---

# ۳) نقشه استفاده ترکیبی

| لایه | ابزار | نقش |
|------|-------|-----|
| زیبایی و UX | **UI/UX Pro Max** + MASTER.md | تصمیم استایل، a11y، chart، Flutter/React guidelines |
| پوسته دسکتاپ | الگوی **Cutting Edge** (خواندنی) | Electron, Ant, Update, i18n |
| AI آفلاین | **Ollama** + Rule + RAG | هسته محصول |
| AI چند-provider اختیاری | **OmniRoute** | sidecar dev / advanced owner |
| دامنه باشگاه | schema + injury + Studio/Client | PRODUCT_PARAMS |

---

# ۴) کارهایی که الان انجام شده

- [x] Clone و کپی UI/UX Pro Max به `docs/MuscleParadise/tools/ui-ux-pro-max`  
- [x] Skill در `.agents/skills/ui-ux-pro-max`  
- [x] تولید + **brand-lock** `design-system/muscle-paradise/MASTER.md`  
- [x] سند یکپارچه‌سازی (همین فایل)  
- [ ] صفحه-overrideها (studio-home, jp7, client, kiosk) — در صورت نیاز مرحله بعد  
- [ ] mp-app theme tokens از MASTER  
- [ ] OmniRoute: فقط مستند؛ نصب global روی sandbox اختیاری (نیاز Node≥۲۲)

---

# ۵) Attribution (باید در About اپ بیاید)

```
UI/UX Pro Max Skill — © Next Level Builder — MIT
https://github.com/nextlevelbuilder/ui-ux-pro-max-skill

OmniRoute — © Diego Rodrigues & contributors — MIT
https://github.com/diegosouzapw/OmniRoute
(optional sidecar; not required for core offline operation)
```

---

# ۶) پاسخ کوتاه به سؤال تو

> **می‌تونی وارد کنی و استفاده کنی؟**

| | |
|--|--|
| **UI/UX Pro Max** | ✅ وارد شد و **همین الان** برای DS و قوانین UI استفاده می‌شود. |
| **OmniRoute** | ✅ از نظر لایسنس/فنی قابل استفاده است؛ در MP به‌صورت **gateway اختیاری / dev** طراحی می‌شود، نه جایگزین Ollama اجباری، تا قول offline-first و حریم داده آسیب‌دیدگی نقض نشود. |

اگر بگویی «OmniRoute را روی همین ماشین هم بالا بیاور»، در نوبت بعد فقط به‌عنوان process جدا (نه داخل CE) امتحان می‌کنیم.
