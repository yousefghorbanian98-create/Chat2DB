# LOOP C — فرانت‌اند
## ۲۸ تسک · ~۳ هفته · وابسته به LOOP A

> این لوپ عمداً ریزترین تسک‌ها را دارد، چون شما مشخصاً خواستید توسعهٔ فرانت به
> میکروتسک‌های بسیار دقیق تقسیم شود.

**مرجع:** [`../build/04_FRONTEND.md`](../build/04_FRONTEND.md) · [`../build/09_DESIGN_SYSTEM_UIUX.md`](../build/09_DESIGN_SYSTEM_UIUX.md)
**پایهٔ موجود:** ۸٬۹۰۴ خط TS/TSX · ۱۵۳ تست سبز · باندل ورودی ۶.۲۴ kB gzip

---

# فاز C1 — بهداشت و زیرساخت (تسک ۰۱–۰۷)

## C-01 · شکستن چانک JP7 — جداسازی نمودار
| | |
|---|---|
| **مشکل** | `AssessmentJp7` = **۱۱۱ kB gzip** — تقریباً به‌اندازهٔ کل بقیهٔ برنامه |
| **علت** | Recharts در همان چانک فرم است |
| **فایل‌ها** | `src/pages/AssessmentJp7.tsx`، `src/components/BodyFatChart.tsx` |

**کار:** نمودار را با `React.lazy()` جدا کنید. فرم ورود ۷ پوست‌چین **فوراً** بیاید؛
نمودار تاریخچه بعد از تعامل بارگذاری شود. `<Suspense>` با skeleton.

**verify:**
```bash
npm run build && node -e "
const fs=require('fs');const f=fs.readdirSync('dist/assets').find(x=>x.includes('AssessmentJp7'));
const kb=fs.statSync('dist/assets/'+f).size/1024;console.log(f,kb);process.exit(kb<120?0:1)"
```
**هدف:** چانک اصلی JP7 < ۳۰ kB gzip

---

## C-02 · تعریف `manualChunks` صریح
| **فایل‌ها** | `vite.config.ts` |
|---|---|

**مشکل:** چانک vendor نامش `tokens-BR8iTfOk.js` است (گمراه‌کننده) و به‌روزرسانی یک صفحه،
کش React کاربر را باطل می‌کند.

```ts
build: { rollupOptions: { output: { manualChunks: {
  react: ['react', 'react-dom'],
  motion: ['framer-motion'],
}}}}
```

**verify:** `npm run build` → فایل‌های `react-*.js` و `motion-*.js` جدا موجود باشند

---

## C-03 · اسکریپت بودجهٔ باندل
| **فایل‌ها** | `scripts/check-bundle-budget.mjs` (جدید)، `package.json` |
|---|---|

```
ورودی (entry)      ≤ 40 kB gzip
هر چانک مسیر       ≤ 60 kB gzip
کل CSS             ≤ 20 kB gzip
```
اگر رد شد → `exit 1` با پیام روشن. سپس به `npm run gate` و CI اضافه کنید.

> **بودجه‌ای که CI نمی‌سنجد، بودجه نیست.**

**verify:** `node scripts/check-bundle-budget.mjs` → exit 0

---

## C-04 · قاعدهٔ ESLint: فقط `api/client.ts` حق `fetch` دارد
| **فایل‌ها** | `eslint.config.js` |
|---|---|

**کار:** `no-restricted-globals: fetch` با استثنا برای `src/api/client.ts`.
الان این قانون نانوشته است و دیر یا زود نقض می‌شود.

**verify:** `npm run lint` → exit 0 (و افزودن `fetch` در یک کامپوننت باید قرمز شود)

---

## C-05 · قاعدهٔ ویژگی‌های منطقی CSS (RTL)
| **فایل‌ها** | `.stylelintrc.json` (جدید)، `package.json` |
|---|---|

```
❌ margin-left     →  ✅ margin-inline-start
❌ padding-right   →  ✅ padding-inline-end
❌ text-align:left →  ✅ text-align:start
❌ left/right      →  ✅ inset-inline-start/end
```
بدون این، افزودن انگلیسی در آینده = بازنویسی کل CSS.

**verify:** `npx stylelint "src/**/*.css"` → exit 0

---

## C-06 · نصب و اتصال `vitest-axe`
| **فایل‌ها** | `package.json`، `vitest.setup.ts` |
|---|---|

```bash
npm i -D vitest-axe
```
یک helper: `expectNoA11yViolations(container)`.

**verify:** `npm test` → exit 0

---

## C-07 · ممیزی کنتراست توکن‌ها
| **فایل‌ها** | `src/styles/tokens.css`، `../build/09_DESIGN_SYSTEM_UIUX.md` §2 |
|---|---|

**کار:** هر جفت رنگ متن/پس‌زمینه را بسنجید. پالت تیره (`#0B0F14`) اغلب یعنی
«متن خاکستری کم‌کنتراست». جدول را در سند ۰۹ پر کنید. هر مورد < ۴.۵:۱ را اصلاح کنید
(حلقهٔ فوکوس ≥ ۳.۰:۱).

**verify:** یک تست که نسبت کنتراست توکن‌های اصلی را محاسبه و assert می‌کند

---

# فاز C2 — i18n و فارسی (تسک ۰۸–۱۲)

## C-08 · زیرساخت i18n سبک
| **فایل‌ها** | `src/i18n/index.ts`، `src/i18n/fa.json`، `src/i18n/en.json` |
|---|---|

**کار:** یک `t()` ساده با JSON. **i18next نصب نکنید** — سنگین است و نیاز ندارید.
```ts
export function t(key: string, vars?: Record<string,string|number>): string
```
fallback: اگر کلید نبود، خودِ کلید برگردد (تا در UI فوراً دیده شود).

**verify:** `npm test -- src/i18n` → exit 0

---

## C-09 · استخراج رشته‌ها — صفحات ادمین
| **فایل‌ها** | `src/pages/{Coach,Programs,Operations,Sync,AssessmentJp7}.tsx` |
|---|---|

رشتهٔ فارسی هارد-کد → `t('key')` + ورودی در `fa.json` و `en.json`.
کلیدها سلسله‌مراتبی: `coach.title`, `programs.empty`, …

**verify:**
```bash
! grep -rPn '>[^<>{}]*[\x{0600}-\x{06FF}]' src/pages/Coach.tsx src/pages/Programs.tsx \
    src/pages/Operations.tsx src/pages/Sync.tsx src/pages/AssessmentJp7.tsx
npm run gate
```

---

## C-10 · استخراج رشته‌ها — صفحات کلاینت
| **فایل‌ها** | `src/pages/{ClientShell,Login,Landing}.tsx`، `src/pages/client/*.tsx` |
|---|---|

**verify:**
```bash
! grep -rPn '>[^<>{}]*[\x{0600}-\x{06FF}]' src/pages/ClientShell.tsx src/pages/Login.tsx \
    src/pages/Landing.tsx src/pages/client/
npm run gate
```

---

## C-11 · استخراج رشته‌ها — کامپوننت‌ها و پیام‌های خطا
| **فایل‌ها** | `src/components/**`، `src/api/client.ts`، `src/ops/opsValidation.ts` |
|---|---|

⚠️ پیام‌های خطای اعتبارسنجی هم شامل می‌شوند — اینها اغلب فراموش می‌شوند.

**verify:**
```bash
! grep -rPn '>[^<>{}]*[\x{0600}-\x{06FF}]' src/components/ --include=*.tsx
npm run gate
```

---

## C-12 · نمایش ارقام و پول فارسی
| **فایل‌ها** | `src/core/format.ts` (جدید)، تست |
|---|---|

```ts
toFaDigits(n)      // ۱۲۳۴  — فقط نمایش
formatRial(n)      // ۱٬۵۰۰٬۰۰۰ ریال
formatRelativeJalali(d)  // «۳ روز دیگر منقضی می‌شود»
```
⚠️ **قانون آهنین:** ارقام فارسی **فقط در لایهٔ نمایش**. ورودی و ذخیره لاتین بماند.
یک تست این را اثبات کند.

**verify:** `npm test -- src/core/format` → exit 0

---

# فاز C3 — آفلاین و دوام داده (تسک ۱۳–۱۷)

## C-13 · لایهٔ IndexedDB
| **فایل‌ها** | `src/offline/db.ts` (جدید)، تست |
|---|---|

**کار:** یک wrapper نازک روی IndexedDB (**بدون کتابخانه** — ~۸۰ خط کافی است).
دو store: `queue` (نوشتن‌های معلق) و `cache` (آخرین پاسخ‌های خوانده‌شده).

**verify:** `npm test -- src/offline` → exit 0

---

## C-14 · صف آفلاین ثبت تمرین
| **فایل‌ها** | `src/offline/queue.ts`، `src/hooks/useWorkoutLog.ts`، تست |
|---|---|

**مشکل:** ورزشکار در زیرزمین باشگاه بدون Wi-Fi ست ثبت می‌کند → رفرش صفحه = داده رفت.
ادعای local-first برای ورزشکار **توخالی** است.

**کار:** شکست شبکه → درج در صف + پیام «ذخیره شد، هنگام اتصال ارسال می‌شود».
هنگام آنلاین شدن → پخش با ترتیب.
⚠️ **از `Idempotency-Key` استفاده کنید** (LOOP B) تا تلاش دوباره پرداخت/ثبت دوتایی نسازد.

**verify:** `npm test -- src/offline src/hooks/useWorkoutLog` → exit 0

---

## C-15 · نشانگر وضعیت اتصال
| **فایل‌ها** | `src/components/ConnectionBadge.tsx`، تست |
|---|---|

سه حالت: آنلاین · آفلاین (n مورد در صف) · در حال همگام‌سازی.
باید در دسترس باشد (نه فقط رنگ — متن هم داشته باشد).

---

## C-16 · نسخه‌بندی و پاک‌سازی کش Service Worker
| **فایل‌ها** | `public/sw.js`، `src/pwa.test.tsx` |
|---|---|

**مشکل کلاسیک PWA:** بعد از به‌روزرسانی، کاربر نسخهٔ کهنه می‌بیند.
**کار:** نام کش `mp-v<version>` + در `activate` کش‌های قدیمی پاک شوند.
استراتژی مستند: پوسته = cache-first · API = network-first با fallback.

**verify:** `npm test -- src/pwa` → exit 0

---

## C-17 · ذخیرهٔ خودکار پیش‌نویس تمرین
| **فایل‌ها** | `src/client/workoutDraft.ts`، `src/hooks/useWorkoutLog.ts` |
|---|---|

پیش‌نویس هر ۲ ثانیه در IndexedDB. بازگشت به صفحه → بازیابی.

---

# فاز C4 — بخش آموزش ویدیویی (تسک ۱۸–۲۲) 🆕

> **ویژگی درخواستی شما:** ورزشکار ویدیوی کوتاه یک تکرار از هر حرکت را ببیند،
> تا نیاز نباشد حرکات ابتدایی را از صفر به همه آموزش دهید.

## C-18 · کامپوننت پخش‌کنندهٔ ویدیو
| **فایل‌ها** | `src/components/exercise/ExerciseVideo.tsx`، تست |
|---|---|

**کار:** `<video>` بومی — **هیچ کتابخانهٔ پخش‌کننده نصب نکنید**.
- `loop` + `muted` + `playsInline` (یک تکرار، تکرارشونده)
- `poster` از thumbnail
- بارگذاری تنبل (`loading="lazy"` روی poster، ویدیو فقط با تعامل)
- کنترل بزرگ و لمسی
- fallback: اگر ویدیو نبود، تصویر + متن دستورالعمل

**verify:** `npm test -- src/components/exercise` → exit 0

---

## C-19 · کارت حرکت
| **فایل‌ها** | `src/components/exercise/ExerciseCard.tsx`، تست |
|---|---|

نام فارسی + انگلیسی · عضلهٔ هدف · تجهیزات · ویدیو · نکات فرم · اشتباهات رایج.
⚠️ اگر حرکت با مصدومیت ورزشکار مغایر است → **بنر هشدار** و پیشنهاد جایگزین.

---

## C-20 · صفحهٔ کتابخانهٔ حرکات
| **فایل‌ها** | `src/pages/client/ExerciseLibrary.tsx`، تست |
|---|---|

جست‌وجو (فارسی و انگلیسی) · فیلتر عضله/تجهیزات · **مجازی‌سازی فهرست**
(۳۱۷ حرکت — بدون مجازی‌سازی روی موبایل کند می‌شود).
با `React.lazy()` — نباید باندل اصلی را سنگین کند.

**verify:** `npm test && node scripts/check-bundle-budget.mjs`

---

## C-21 · ویدیو داخل صفحهٔ برنامهٔ تمرینی
| **فایل‌ها** | `src/pages/client/WorkoutLogCard.tsx` |
|---|---|

کنار هر حرکت در برنامهٔ امروز، دکمهٔ «▶ نمایش» → ویدیو در مودال.
**همین ویژگی است که مربی را از تکرار آموزش‌های ابتدایی خلاص می‌کند.**

---

## C-22 · کش آفلاین ویدیو
| **فایل‌ها** | `src/offline/videoCache.ts`، `public/sw.js` |
|---|---|

ویدیوهای دیده‌شده کش شوند (سقف ~۲۰۰MB، حذف LRU).
**verify:** تست که سقف رعایت می‌شود و قدیمی‌ترین حذف می‌شود

---

# فاز C5 — کیفیت صفحات (تسک ۲۳–۲۸)

## C-23 · صفحه‌بندی در UI
| **فایل‌ها** | `src/hooks/useMembers.ts`، `src/pages/Coach.tsx` |
|---|---|
مصرف cursor از LOOP B + بارگذاری تدریجی (infinite scroll یا دکمهٔ «بیشتر»).

## C-24 · حالت‌های loading / خالی / خطا
| **فایل‌ها** | همهٔ صفحات |
|---|---|
skeleton (نه اسپینر) · حالت خالی با اقدام پیشنهادی · خطای فارسی + دکمهٔ تلاش دوباره.

## C-25 · تست a11y روی همهٔ صفحات
| **فایل‌ها** | همهٔ `*.test.tsx` |
|---|---|
`expectNoA11yViolations(container)` در هر تست صفحه.
**verify:** `npm test` → exit 0

## C-26 · ناوبری کامل با کیبورد
فوکوس مرئی · ترتیب منطقی · بدون تله فوکوس در مودال · `Esc` می‌بندد.

## C-27 · تست رندر Operations و OpsKpis
شکاف شناخته‌شده: این دو صفحه تست رندر ندارند.

## C-28 · ممیزی حرکت
| **فایل‌ها** | `src/motion/presets.ts` |
|---|---|
هیچ عدد جادویی انیمیشن در کامپوننت‌ها — همه از `presets.ts`.
دیال ۴/۱۰ برای داشبورد و جدول · ۸/۱۰ برای فرود، مودال، توست.
`prefers-reduced-motion` همه‌جا محترم.

**verify:** `! grep -rn "transition:\s*{" src/pages src/components --include=*.tsx`

---

# معیار خروج LOOP C

```
□ ۲۸ تسک DONE
□ هیچ چانک > ۶۰ kB gzip (JP7 از ۱۱۱ → < ۳۰)
□ node scripts/check-bundle-budget.mjs → exit 0
□ صفر رشتهٔ فارسی هارد-کد در JSX
□ صفر نقض a11y در همهٔ تست‌های صفحه
□ npx stylelint → exit 0 (بدون ویژگی جهت‌محور)
□ ثبت تمرین در حالت آفلاین کار می‌کند و بعداً همگام می‌شود
□ ویدیوی حرکت در اپ کلاینت پخش می‌شود
□ npm run gate → exit 0
□ تست‌ها در TZ=Pacific/Kiritimati هم سبز
```

**عددی که این لوپ جابه‌جا می‌کند:**
`بزرگ‌ترین چانک: ۱۱۱ kB → < ۶۰ kB` · `نقض a11y: نامعلوم → ۰` · `تست فرانت: ۱۵۳ → ~۲۴۰`
