# 🔎 SOURCE RESEARCH — ۶ منبع برتر برای موشنهای Master Loop v2.0

> تاریخ: 2026-08-30 · بررسی عمیق ۶ سایت به درخواست کاربر.
> هدف: پیدا کردن چیزی که **بهتر از نمونههای فعلی** باشد و مستقیم قابل واردکردن
> (یا با تغییر کم قابل انطباق) به موشنهای ۴گانه (Loading C · Landing D · Editor G+H · Style Match I+J).
> وضعیت: **فقط تحقیق — هنوز چیزی ساخته/وارد نشده.**

---

## جدول خلاصه

| # | نام | چیست؟ | مستقیم قابل ورود؟ | مجوز/هزینه | بهترین برای |
|---|---|---|---|---|---|
| 1 | **particles.casberry.in** | سیمولاتور ذرات ۳D با WebGL (۲۰٬۰۰۰+ ذره) | ✅ خروجی React/Three.js + نوشتن تابع طبق API عمومیاش | رایگان، بدون ثبتنام | پسزمینهی ذرهای Loading C و Landing D |
| 2 | **originkit.dev** | کتابخانهی ۳۶۳ کامپوننت انیمیشنی (رایگان + Pro) | ⚠️ سورس از طریق MCP با کلید رایگان (۱۰ واکشی/روز)؛ برخی Pro پولی | رایگان/Premium | Star Burst، Scramble Text، Glow Border، Starfield Button، Plasma Ring |
| 3 | **daisyui.com** | کتابخانهی کامپوننت Tailwind با ۳۵ تم و متغیر CSS | ⚠️ مستقیم نیاز به Tailwind v4؛ انطباقی: توکنهای oklch + الگوهای CSS | MIT | سیستم تم (E)، لودینگ/پیشرفت/اسکلتون (C) |
| 4 | **Design Motion Principles** | مهارت (Skill) طراحی موشن برای ایجنتهای AI — ۳ لنز: Kowalski/Krehel/Jhey + حالت Audit | ✅ نصب مستقیم `npx skills add` — همین الان قابل استفاده | MIT (GitHub، ۹۹۹+ ستاره) | ممیزی و ارتقای کیفیت همهی ۴ موشن |
| 5 | **Framer Motion / Motion** | کتابخانهی انیمیشن React (motion.dev) + بخشهای آمادهی Motion UI | ✅ ارتقای مستقیم npm از framer-motion ۱۱ به motion ۱۳؛ +animateView() رایگان | MIT (هسته رایگان)؛ Motion+ پولی | morph تم با View Transition (E)، confetti، coverflow، border-beam، page transitions |
| 6 | **21st.dev** | بزرگترین مارکتپلیس متنباز کامپوننت React (۱۲٬۰۰۰+، shadcn/Tailwind) | ✅ کد داخل خود صفحات نمایش داده میشود — قابل کپی/انطباق | متنباز (بسیاری MIT) | WebGL Shader، Wave Background، Rainbow Borders Button، Heroها |

---

## ۱) particles.casberry.in — AI Particle Simulator (Casberry India)

**چیست:** یک ابزار وب WebGL برای ساخت دستههای عظیم ذرات ۳D (۲۰٬۰۰۰+ واحد در ۶۰fps).
کار با یک تابع جاوااسکریپت انجام میشود که قرارداد API مشخصی دارد:

- متغیرهای ورودی: `i` (شاخص ذره)، `count`، `time`، دسترسی کامل به `THREE`
- خروجی: `target.set(x,y,z)` (موقعیت) و `color.setHSL(...)` (رنگ)
- کمکی: `addControl(id,label,min,max,initial)` برای اسلایدرهای زنده، `setInfo`، `annotate`
- **قوانین سختگیرانهی عملکرد:** صفر GC (نه `new Vector3` در حلقه)، ریاضی بهجای if/else، ممنوعیت document/window/fetch/…
- **خروجیها:** Vanilla JS · React · Three.js · PLY/GLB/OBJ · PNG/JPEG/WebP — بدون نیاز به ثبتنام

**نحوهی ورود به پروژه ما:**
- گزینهی A (مستقیم): در مرورگر خودت خروجی React/Three.js برای مثلاً «سحابی شبکهی عصبی دیتابیس» تولید میکنی و به من میدهی تا وارد کنم.
- گزینهی B (انطباقی — بدون نیاز به خود سایت): من طبق همین قرارداد عمومی API، یک سیستم ذرات ۲۰٬۰۰۰+ برای **Loading C** مینویسم (مثلاً ۵ گره دیتابیس که از ذرات ساخته میشوند یا لوگوی Chat2DB که به ذرات تبدیل میشود).

**چرا بهتر از فعلی:** نمونهی فعلی ~۱۰ گره و ۸ لبه دارد؛ این یکی افکت ذرهای سینمایی با عمق و «واو» واقعی میسازد — مخصوصاً برای اسپلشاسکرین.

---

## ۲) originkit.dev — Free Animated Component Library

**چیست:** کتابخانهی کامپوننتهای انیمیشنی — سایت الان **۳۶۳ کامپوننت** دارد (پلاگین MCP میگوید ۵۰ تا، ولی سایت خیلی بیشتر است). دستهها:

| دسته | کامپوننتهای شاخص |
|---|---|
| Interactive Elements | Black Hole ⚫، Fluid Trail، SVG Particles، Kinetic Grid، Harmonic Shell، Structure Flow، Warp Field، Fluid Field، Arch Corridor |
| Image Gallery | **Coverflow Carousel (۲۱٫۲k بازدید)**، Rotunda Carousel، Spiral Images، Swipe Stack، Infinity Canvas |
| Text | **Scramble Text**، Text Morph، Smoky Text، Weight Hover |
| Animation | **Pixel Reveal**، **Star Burst**، **Particle Tunnel**، Glitter Wrap، Plasma Ring، Light Bloom |
| Background | Snow Fall، Blinking Squares، Character Waves، Scroll Wave Field، Elemental Water |
| Button | **Starfield Button** (سند API کاملش را خواندم)، Emoji Burst، Link Preview، Glow Border، Pulsating Border، Flare Arc، Fibre Arc، Keycap Button، Rubber Spheres |

**نحوهی ورود:** سورس کد از طریق MCP سرور (`mcp.originkit.dev`) با **کلید API رایگان** (originkit.dev → Settings → API Integration) و سقف ۱۰ واکشی در روز. خروجی در React/Next/Vite/Framer و CSS/Tailwind/CSS Modules. بعضی کامپوننتها Pro (پولی) هستند — «Starfield Button» رایگان بود و داکیومنت فنی عالی دارد (مسیر نورها با طول کمان، ماسک border-box، هش ساین برای تعییننشدنی، تیکر framer-motion).

**بهترین کاربردها برای ما:**
- **Star Burst / Pixel Reveal** → لحظهی burst در Loading C
- **Scramble Text** → تایپرایتر ادیتر (D-2) — افکت قویتر از reveal ساده
- **Starfield Button** → دکمهی Run در ادیتر (D)
- **Glow Border / Pulsating Border** → پنلهای Style Match (E)
- **Plasma Ring / Light Bloom** → حلقهی پیشرفت و لوگو (B-4, B-5)

---

## ۳) daisyUI — Tailwind CSS Component Library

**چیست:** معروفترین کتابخانهی کامپوننت Tailwind (MIT). ۳۵ تم آماده با نامهای light/dark/cupcake/synthwave/night/coffee/… — همه بر پایهی **متغیرهای CSS به فرمت oklch** و attribute ی `data-theme` (با قابلیت تودرتو). کتابخانهی `theme-change` هم برای ذخیرهی انتخاب تم در localStorage دارد.

**نحوهی ورود:**
- مستقیم: نیازمند Tailwind v4 در پروژه (در دموی ما نیست؛ میشود اضافه کرد ولی سنگین است)
- **انطباقی (پیشنهادی):** فقط «سیستم توکن» را برمیداریم — نامگذاری `--color-base-100/200/300`, `--color-primary`, `--radius-box`, `--depth`, `--noise` و ساختار `data-theme` را به CSS خالص خودمان منتقل میکنیم؛ کامپوننتهای `loading spinner`, `progress`, `skeleton`, `steps`, `countdown`, `stat` را با CSS خودمان پیاده میکنیم.

**بهترین کاربردها:** سیستم تم Style Match (E-1) — دموی فعلی ۳ تم دارد، با توکنهای daisyUI میتوان ۱۲+ تم واقعی با فرمت استاندارد ارائه کرد؛ و اسکلتون/استپس برای مراحل پایپلاین Loading C.

---

## ۴) Design Motion Principles (kylezantos/design-motion-principles)

**چیست:** یک **مهارت (Skill) برای ایجنتهای AI** — ۹۹۹+ ستاره، MIT. سه لنز طراحی که بر اساس نوع پروژه وزن میگیرند:
- **Emil Kowalski** (Linear): «اصلاً باید انیمیت بشه؟» — سرعت و خویشتنداری (برای ابزارهای بهرهوری)
- **Jakub Krehel**: «آیا بهاندازهی کافی ظریف است؟» — پولیش تولید
- **Jhey Tompkins**: «چه میتوانست بشود؟» — آزمایش خلاقانه

**امکانات کلیدی:**
- دو حالت: **Create** (ساخت کامپوننت با موشن درست) و **Audit** (ممیزی موشنهای موجود + گزارش HTML با دموهای لوپشونده)
- **Frequency Gate:** هرچقدر انیمیشن بیشتر تکرار شود باید کوتاهتر/حذف شود
- دستورالعملهای مدتزمان، **کتاب پخت (cookbook)** شامل transitions/springs/FLIP/scroll-driven
- **چکلیست ضد-AI-slop:** تشخیص الگوهای موشن AI-زده (پالس بیهدف، hover-scale روی همهچیز، stagger اسپم)
- prefers-reduced-motion **الزامی** (نه اختیاری)

**نحوهی ورود:** `npx skills add kylezantos/design-motion-principles` — مستقیم توسط من بهعنوان ایجنت قابل استفاده است.

**بهترین کاربرد:** اجرای **Audit** روی هر ۴ موشن فعلی و اعمال نسخههای اصلاحشده — یعنی موشنها را نه فقط زیباتر، بلکه **حرفهایتر** میکنیم (ضد slop). مخصوصاً برای یک ابزار بهرهوری (که Chat2DB هست) لنز Emil حیاتی است: لودینگ باید زیر ~۲ ثانیه باشد نه ۳٫۵.

---

## ۵) Framer Motion / Motion (motion.dev)

**چیست:** کتابخانهی انیمیشن React — MIT، رایگان، همان چیزی که الان `framer-motion@11` در دمو داریم. نسخهی جدید (`motion@13`) با امکانات تازه:

- **`animateView()`** — پیادهسازی آسان View Transition API (توی هستهی رایگان!) — **دقیقاً همان چیزی که Section E-4 نقشه میخواهد**
- **Motion UI** — بخشهای آماده با درجهی عملکرد MotionScore: Heroها (editorial stagger)، Pricing (price morph)، Testimonials (logo ticker, coverflow)، Bento grids، Stats counters، Navigation، **Page Transitions (curtains)**، FAQ، Overlays (sheet, toasts)، Buttons (rolling text, hold-to-confirm)، **Loaders (skeleton handoff)**، Accordion، **Border Beam**، Confetti، Command palette، Coverflow، Add-to-basket
- ۴۳۰+ مثال آماده + **AI Kit** برای ایجنتها
- Springs واقعی، layout animation، stagger، gestureهای hover/press/drag، RTL-ready

**نحوهی ورود:** `npm i motion` (جایگزین framer-motion — API سازگار) + `@motion/ui-*` برای سکشنهای رایگان. بخشی از Motion UI در بستهی پولی Motion+ است ($399 یکبار / $249 سالانه هر صندلی) — بخش رایگان برای ما کافی است.

**بهترین کاربردها برای ما:**
- `animateView()` برای **مورف تم Style Match** (جایگزین rAF-lerp فعلی — smoother و native)
- **Page Transitions** بین Loading → Landing (پردهای)
- **Border Beam / Confetti** → بوردر درخشان پنلها + انفجار موفقیت در Run
- **Coverflow** → گالری تمها در Style Match
- **Loaders (skeleton)** → وضعیتهای لودینگ

---

## ۶) 21st.dev — 12,000+ Crafted UI Components

**چیست:** بزرگترین مارکتپلیس متنباز کامپوننت React (shadcn/ui + Tailwind + Radix) با ۱٫۴ میلیون توسعهدهنده. ۱۲٬۰۰۰+ کامپوننت، ۲٬۰۰۰+ بلاک مارکتینگ (Hero، شیدر، پسزمینه، گرادیان…)، ۲٬۱۰۰+ کامپوننت UI (دکمه، AI chat، کارت، گالری 3D، ناوبری). نصب با `npx shadcn@latest add …` یا **کپی مستقیم کد از خود صفحه** (تبهای Preview/Code — در بررسی من، کد WebGL Shader مستقیم نمایش داده شد).

**کامپوننتهای شاخصی که دیدم/شناسایی کردم:**
- **WebGL Shader** (Ali Imam — ۲٫۰k): موج رنگی تمامصفحه با three.js
- **Vercel Hero** · **Liquid Metal Hero** (۷۶۱) · **Waitlist Hero** (۱٫۳k) · **Gradient Bar Hero** · **Hero Section 5** · **Hero ASCII** (۹۶۷)
- **Wave Background** · **Animated Gradient Background** (۱٫۴k) · **Vapour Text Effect** (۱٫۶k) · **Hover Preview** (۳۶۳) · **Hover Footer** (۷۴۴)
- دکمهها: **Rainbow Borders Button** (۳۷۴) · **Star Button** (۴۴۱) · **Hover Button** · **Gradient Button** · **Button Colorful** (۵۶۴)
- دستههای بزرگ: **WebGL (۳۹۷)** · **Hero section (۷۴۸)** · **Wave (۱۱۰)** · **Glassmorphism (۲۴۰)** · **Liquid Glass (۲۶)**
- (گلوب ۳D محبوب با three.js هم در این دستهها هست — الگوی arcs/points که در Landing D استفاده میکنیم)

**نحوهی ورود:** کدها React + Tailwind هستند؛ در دموی ما (CSS خالص) **انطباقی** وارد میشوند — کلاسهای Tailwind به CSS معادل تبدیل میشوند (برای من معمول است). برای نصب shadcn در پروژهی واقعی هم مسیر رسمی وجود دارد.

**بهترین کاربردها برای ما:**
- **WebGL Shader / Wave Background** → پسزمینهی Landing D (قویتر از کرهی سیمی ساده)
- **Rainbow Borders / Star Button** → دکمهی Run ادیتر
- **Liquid Metal / Vapour Text** → تایپوگرافی لوگو و عنوان
- **Animated Gradient Background** → پشت پنلهای Style Match

---

## 🏆 پیشنهاد ترکیبی من (بهترینِ بهترینها)

| موشن | الان | جایگزین پیشنهادی | منبع |
|---|---|---|---|
| **C · Loading** | گره+لبه+پالس | صحنهی ذرهای ۲۰٬۰۰۰+ (لوگو→ذرات) + Star Burst پایان | Casberry + Originkit |
| **D · Landing** | کرهی سیمی | کرهی سیمی + **WebGL Shader پسزمینه** + Wave | 21st.dev |
| **G+H · Editor** | تایپرایتر ساده | **Scramble Text** + دکمهی **Starfield/Rainbow** + Border Beam روی پنل AI | Originkit + 21st.dev |
| **I+J · Style Match** | lerp دستی | **animateView()** (View Transition واقعی) + ۳۵ تم oklch + Coverflow | Motion + daisyUI |
| **همه** | — | اجرای **Audit ضد-slop** و اصلاح مدتزمانها | Design Motion Principles |

---

## ⚠️ محدودیتهای صادقانه

- **Casberry:** ابزارش تعاملی است و من از سندباکس نمیتوانم داخلش کلیک کنم؛ یا تو در مرورگرت خروجی بگیری، یا من طبق قرارداد عمومی API خودم مینویسم (نتیجه یکسان از نظر کیفیت قابل کنترل است).
- **Originkit:** برای واکشی سورس، کلید API رایگان لازم است (originkit.dev → Settings → API Integration) — اگر بدهی، مستقیم میآورم؛ بدون کلید، از روی داکیومنت و توضیحات عمومی انطباق میدهم.
- **21st.dev:** کد صفحهها را میتوانم همین الان کپی کنم (نیاز به اکانت ندارد برای مشاهده) — فقط تبدیل Tailwind→CSS زمان میبرد.
- **Motion UI:** برخی سکشنها در Motion+ پولی هستند؛ انتخابهای من از بخش رایگاناند.

---

## 📋 فهرست اسامی (برای انتخاب تو)

1. **particles.casberry.in** — ذرات ۳D سینمایی (سیمولاتور AI)
2. **originkit.dev** — ۳۶۳ کامپوننت انیمیشنی (رایگان+Pro)
3. **daisyui.com** — ۳۵ تم + کامپوننتهای Tailwind (MIT)
4. **design-motion-principles** (Skill) — ممیزی و استاندارد حرفهای موشن
5. **Framer Motion / motion.dev** — ارتقای هسته + animateView + Motion UI
6. **21st.dev** — ۱۲٬۰۰۰+ کامپوننت (شیدرها، Heroها، دکمهها)
