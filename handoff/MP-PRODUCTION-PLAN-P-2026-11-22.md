# پلن تولید فاز P — «هارنسِ agent-محور و گیت‌های خود-پلیس»

نسخهٔ ۱ · ۲۰۲۶‑۱۱‑۲۲ · تهیه‌کننده: ممیز (شاخهٔ `arena/2cde32d6-chat2db` در Chat2DB) · مجری: بیلدر (شاخهٔ کاریِ MP)
منبعِ الگوها: ‏`expo/exact` (MIT) — فقط **الگو** وام گرفته می‌شود، نه وابستگی. `morluto/rea` و `expo/exact` **نصب نمی‌شوند**.
وضعیتِ شروع: **پس از checkpoint 1 و merge توسط مالک** — مگر مالک صریحاً زودتر بگوید (توصیهٔ ممیز: نگویید، تا لوپِ ممیزی کش نیاید).

---

## ۰) چرا این فازها (همه با سنجه، نه حدس)

| سنجهٔ ممیز | نتیجه |
|---|---|
| هارنسِ UI-راندنی در استودیو | **نیست** — در `mp-app/studio/package.json` و `tests/` اثری از playwright/puppeteer/cypress نیست |
| devDependencies موجودِ استودیو | `@testing-library/react ^16.0.1` · `@testing-library/user-event ^14.6.10` · `jsdom ^25.0.1` · `vitest ^3.2.7` · `environment: "jsdom"` در `vitest.config.ts:15` ⇒ **پلن بدونِ وابستگیِ تازه ممکن است** |
| زمان در استودیو | `new Date(` در **۱۱ فایل** · `src/lib/clock.ts` **وجود ندارد** · `Date.now()` = ۰ |
| زمان در بک‌اند | **بسته شده**: `app/clock.py` (تنها نقطهٔ `_now_utc()` + `today_in_shop_zone()`، منطقهٔ `settings.shop_timezone`) با `tests/regression/test_wp36_shop_today.py` ⇒ نیمهٔ استودیوییِ F‑28 باز است |
| گاردریلِ لایهٔ داده | فقط یک تستِ رگرسیون (`test_b2_wp23_wp43_wp44.py::test_no_dynamic_import_in_studio_handlers`)؛ در `eslint.config.mjs` هیچ `no-restricted-syntax`/`no-restricted-imports` نیست ⇒ قاعدهٔ دائمی وجود ندارد |
| فرمتِ تشخیصِ گیت‌ها | `scripts/docs_gate.py` (۲۱۲ خط) دسته‌ای چاپ می‌کند ولی **شناسهٔ پایدار و پیشنهاد ندارد** (خط‌های ۱۱۱/۱۱۳/۱۱۹/۱۶۶/۱۷۶/۱۸۳ همه `path:line: متنِ آزاد`)؛ `scripts/interaction_map.py` (۴۰۵ خط، `problems` در ۳۶۷–۳۸۰) هم بدونِ شناسه |
| jobهای CI | دقیقاً ۸: `secret-scan`(۱۵) · `docs`(۹۴) · `backend`(۱۱۴) · `studio`(۱۹۶) · `client-flutter`(۲۲۲) · `live-contract`(۳۸۱) · `e2e-api`(۴۳۳) · `client-pinned`(۴۵۵) |
| job `docs` | هم‌اکنون `tools/mermaid-check` (خطِ ۱۱۰) و `python3 scripts/repo_hygiene_gate.py` (خطِ ۱۱۲) را صدا می‌زند ⇒ میزبانِ طبیعیِ گیت‌های تازهٔ هارنس |
| job `studio` | ‏`npm ci || npm install`(۲۰۵) · `npm run lint`(۲۰۶–۲۰۸) · `npm test`(۲۱۱) · `vite build`(۲۱۲–۲۱۳) ⇒ تست‌های تازه **خودکار** در CI می‌روند |
| آرتیفکتِ Android | ساخته نمی‌شود: `apk.yml` با AD‑21 حذف شد؛ `client-pinned` فقط «Android debug compile» (کامنتِ `ci.yml:450` همین را می‌گوید) |

---

## ۱) قواعدِ تغییرناپذیر

1. **وابستگیِ تازه ممنوع** (npm و pip، حتی devDependency). همهٔ فازها با devDependencies موجودِ جدولِ بالا ساخته می‌شوند. نیازِ واقعی ⇒ توقفِ سخت و سؤال.
2. **job تازهٔ CI ممنوع؛ ویرایشِ ruleset ممنوع.** ruleset ‏`27826883` دقیقاً همان ۸ check بالا را لازم می‌داند (`strict: true`). هر گیتِ تازه باید **داخلِ یکی از همان ۸ job** اجرا شود: گیت‌های هارنس/اسناد ⇒ `docs`؛ تست‌های استودیو ⇒ `studio` (از مسیرِ `npm test` موجود).
3. **red-first**: پیش از هر پیاده‌سازی، تستِ شکست‌خور بنویس و خروجیِ قرمزش را در `EXECUTION-LOG.md` بگذار.
4. **هیچ گیتی ضعیف نشود**: کاهشِ آستانه، حذف/skip تست، افزودنِ استثنا به `ROUTE_EXCEPTIONS`، widening احراز هویت، تغییرِ نسخهٔ وابستگی، force-push/بازنویسیِ تاریخ ⇒ توقفِ سخت.
5. هر عددِ گزارش‌شده باید **فرمان و خروجیِ خامش** در `EXECUTION-LOG.md` باشد. گزارشِ نوبت ≤۶ bullet.
6. هر فاز **≤۲ کامیت + یک بخشِ LOG + یک push**. `merge` ممنوع. فقط روی شاخهٔ کاریِ مجازِ خودت push کن.
7. ‏`share/` و فایل‌های untracked (مثل `mp-app/backend/var/receipts/*.png`) و هر باینری/تصویری commit نشود.
8. ابهام ⇒ انتخابِ محافظه‌کارانه طبقِ AD‑21…AD‑24، ثبت به‌صورت `D-n` با دلیل و راهِ برگرداندن، بعد ادامه.

---

## ۲) جدولِ فازها

| فاز | عنوان | اولویت | تلاش | ریسک | پیش‌نیاز |
|---|---|---|---|---|---|
| **P‑1** | ساعتِ یکتای استودیو + منعِ `new Date()` مستقیم (نیمهٔ بازِ F‑28) | بالا | S | کم | — |
| **P‑2** | درایورِ قطعیِ UI استودیو: ‏`render/tap/type/clock/state/snapshot` | بالا | M | کم (jsdom موجود) | P‑1 |
| **P‑3** | تشخیص‌های دسته‌ای با **شناسهٔ پایدار + پیشنهادِ اصلاح** در `docs_gate.py` و `interaction_map.py` | بالا | M | متوسط (گیت‌های لازم‌الاجرا) | — |
| **P‑4** | گاردریلِ لایهٔ داده به‌صورت قاعدهٔ دائمیِ ESLint (تثبیتِ F‑19/WP 4.3) | متوسط | S | کم | — |
| **P‑5** | گیتِ «buildِ کهنه ممنوع» + چاپِ فرمانِ بازسازی | متوسط | S | کم | — |
| **P‑6** | یادداشتِ اصطکاک با یک فرمان (`friction note`) | پایین | S | کم | P‑3 |
| **P‑7** | بودجهٔ اندازهٔ bundle استودیو | **اختیاری — فقط با تأییدِ مالک** | S | آستانهٔ تازه | — |
| **P‑8** | ممیزیِ آرتیفکتِ release با REA/Ghidra | **مشروط به تصمیمِ مالک** | — | — | ساختِ دوبارهٔ APK |

---

## ۳) مشخصاتِ فازها

### P‑1 · ساعتِ یکتای استودیو (نیمهٔ بازِ F‑28)

- **چرا:** بک‌اند با `app/clock.py` بسته شده؛ استودیو هنوز ۱۱ مصرفِ مستقیمِ `new Date(` دارد و ماژولِ ساعت ندارد ⇒ «امروز» در UI می‌تواند با «امروز» در بک‌اند تفاوت کند (مرزِ ۰۰:۰۰–۰۳:۳۰ تهران).
- **دامنه:** `mp-app/studio/src/lib/clock.ts` (جدید) · ۱۱ فایلِ مصرف‌کننده · `mp-app/studio/eslint.config.mjs` · `mp-app/studio/tests/clock.test.ts` (جدید) · به‌روزرسانیِ ردیفِ F‑28 در `docs/MuscleParadise/audit/CHECKLIST.md`.
- **معیارهای پذیرش:**
  - **C1** ‏`src/lib/clock.ts` سه API دارد: `now(): Date` · `today(): string` (ISO در منطقهٔ فروشگاه) · `setClock(iso | null)` (فقط تست/درایور).
  - **C2** منطقهٔ زمانی از همان قراردادِ بک‌اند خوانده شود (‏`Asia/Tehran` پیش‌فرض، از تنظیمات/API — نه hardcode در ۱۱ جا).
  - **C3** ‏`grep -rE "new Date\(|Date\.now\(" mp-app/studio/src | wc -l` ⇒ فقط داخلِ `src/lib/clock.ts` (خارجِ آن **۰**).
  - **C4** قاعدهٔ `no-restricted-syntax` در ESLint همان را دائمی کند؛ `npm run lint` ⇒ **۰ خطا، ۰ هشدار**.
  - **C5** تستِ red-first مرزِ نیمه‌شب: با ساعتِ ثابت `2026-03-20T20:30:00Z` ⇒ «امروز» در تهران `2026-03-21` باشد (و برعکس).
  - **C6** هیچ رفتارِ محصولی عوض نشود: فقط منبعِ زمان جابه‌جا شود.
- **CI:** از `npm run lint`(۲۰۶) و `npm test`(۲۱۱) موجود — بدونِ job تازه.
- **خارج از دامنه:** تغییرِ منطقهٔ زمانیِ بک‌اند، timezone picker، تغییرِ منطقِ تاریخِ شمسی.
- **Rollback:** ‏`git revert` همان کامیت.

### P‑2 · درایورِ قطعیِ UI (الگوی `agent.mjs` در Exact)

- **چرا:** استودیو هیچ راهِ «راندنِ UI» ندارد؛ ممیز و بیلدر مجبورند رگرسیونِ UI را با خواندنِ کد حدس بزنند. الگو: ‏`bun scripts/agent.mjs web tree "tap X" "type Y" "clock +60000" state "screenshot out.png"`.
- **دامنه:** `mp-app/studio/scripts/agent_drive.mjs` (جدید) · `mp-app/studio/tests/driver/*.test.tsx` (جدید) · یک خطِ script در `package.json` (`"drive": "node scripts/agent_drive.mjs"`) · یک بخشِ runbook در `docs/MuscleParadise/runbooks/`.
- **معیارهای پذیرش:**
  - **C1** یک فرمانِ واحد با افعالِ به‌ترتیب: `render <Page>` · `tap "<label|selector>"` · `type "<selector>" "<text>"` · `clock <ISO8601|+Nms>` · `state [jsonPath]` · `snapshot <file>` (اجرا روی vitest + `@testing-library/react` + `user-event` — بدونِ مرورگرِ واقعی).
  - **C2** **قطعیّت:** دو اجرای پشتِ‌سرِهم با ورودیِ یکسان ⇒ خروجیِ بایت‌به‌بایت یکسان (‏`sha256sum` هر دو در LOG، `diff` خالی). هیچ timestamp/ترتیبِ تصادفی/`Math.random` در خروجی نباشد.
  - **C3** ‏`clock` از مسیرِ `src/lib/clock.ts` (فاز P‑1) عبور کند، نه mock سراسریِ jsdom؛ نمونه: `clock 2026-03-20T20:30:00Z` ⇒ در state مقدارِ «امروز» `2026-03-21`.
  - **C4** ‏`state` خروجیِ JSON با کلیدهای **مرتب** می‌دهد؛ `snapshot` **متنِ DOM** می‌نویسد (نه PNG) تا در diffِ git خوانا باشد. نوشتنِ باینری/تصویر ⇒ توقفِ سخت.
  - **C5** هر خطای درایور: شناسهٔ پایدارِ `DRV-###` + مسیر/خط + پیشنهادِ اصلاح (هم‌راستا با P‑3).
  - **C6** زمانِ یک درایویِ نمونه در CI **≤ ۳۰ ثانیه** (`time` در LOG).
  - **C7** ‏`git diff mp-app/studio/package.json` ⇒ **فقط یک script تازه**؛ هیچ وابستگیِ تازه‌ای نباشد.
  - **C8** حداقل دو صفحهٔ واقعی (یکی فرم‌دار مثل `Shop`، یکی جدول‌دار) با درایور پوشش داده شوند تا الگو اثبات شود، نه toy.
- **CI:** ‏`npm test` موجود در job `studio`.
- **خارج از دامنه:** Playwright/مرورگرِ واقعی/Electron، E2E شبکه‌ای، screenshot باینری، تستِ بار.
- **Rollback:** حذفِ دو مسیرِ تازه + بازگرداندنِ یک خطِ script (بدونِ اثر بر کدِ محصول).

### P‑3 · تشخیص‌های دسته‌ای با شناسهٔ پایدار (الگوی «کامپایلری که درس می‌دهد»)

- **چرا:** Exact در یک اجرا تا ۲۰ خطای مستقل با شناسهٔ پایدار و پیشنهادِ دقیق می‌دهد (`[type-assign]`، `[lower-unknown-attr]`). گیت‌های ما دسته‌ای‌اند ولی شناسه/پیشنهاد ندارند ⇒ هر خطا یک رفت‌وبرگشتِ اضافه برای agent می‌سازد.
- **دامنه:** `scripts/docs_gate.py` · `scripts/interaction_map.py` · `docs/MuscleParadise/audit/GATE-CODES.md` (جدید، جدولِ مرجعِ کدها) · تست‌های همان اسکریپت‌ها.
- **معیارهای پذیرش:**
  - **C1** هر تشخیص شناسهٔ پایدارِ نسخه‌دار بگیرد: `DOC-###` · `MAP-###` · بعداً `STALE-###` · `DRV-###`.
  - **C2** فرمتِ خروجیِ واحد: ‏`CODE path:line: پیام ← پیشنهاد`.
  - **C3** دسته‌بندیِ کامل (نه fail-fast) با **سقفِ ۲۰ تشخیص در هر دسته** و سپس `+N موردِ دیگر` (دقیقاً الگوی Exact) تا خروجی منفجر نشود.
  - **C4** **معنی عوض نشود:** مجموعهٔ تشخیص‌ها پیش و پس از تغییر یکسان بماند. سنجهٔ الزامی در LOG: خروجیِ هر دو گیت روی tipِ فعلی، **پیش از** تغییر و **پس از** آن، با `sort` و `diff` ⇒ فقط تفاوتِ «افزودنِ کد و پیشنهاد»، بدونِ تشخیصِ تازه یا گم‌شده.
  - **C5** ‏**exit codeها دقیقاً همان بمانند** (`docs_gate.py` دو مسیرِ exit دارد، `interaction_map.py` یکی) تا jobهای CI نشکنند.
  - **C6** پرچمِ `--json` با کلیدهای `code/path/line/message/suggestion` (برای مصرفِ ماشینیِ ممیز).
  - **C7** ‏`GATE-CODES.md` معنی و راهِ حلِ هر کدِ **فعال** را داشته باشد و `docs_gate` لینک‌هایش را بسنجد (خودِ گیت روی خودش).
  - **C8** تستِ red-first برای کدگذاری (یک سندِ خرابِ نمونه ⇒ انتظارِ `DOC-###` مشخص).
- **ریسک و دستورِ خاص:** این دو گیت امروز **سبز** و در CI لازم‌الاجرا هستند. اگر کدگذاری باعثِ قرمزیِ job `docs` شد ⇒ همان کامیت را `revert` کن و گزارش بده؛ خودسرانه آستانه را شل نکن.
- **Rollback:** ‏`git revert` (فرمت به حالتِ آزاد برمی‌گردد؛ منطقِ تشخیص دست‌نخورده بود).

### P‑4 · گاردریلِ لایهٔ داده به‌صورت قاعدهٔ دائمیِ ESLint

- **چرا:** F‑19 («۳ لایهٔ جداگانهٔ دسترسی به داده + `await import()` پویا در هندلر») با WP 4.3 بسته شد ولی فقط با یک تستِ رگرسیون؛ قاعدهٔ lint نیست، پس می‌تواند برگردد.
- **دامنه:** `mp-app/studio/eslint.config.mjs` · (در صورتِ نیاز) یک تستِ رگرسیونِ تکمیلی.
- **معیارهای پذیرش:**
  - **C1** ‏`await import(` از `src/lib/api` در `src/pages/**` و `src/components/**` ⇒ خطای lint.
  - **C2** ‏`fetch(`/`axios`/`XMLHttpRequest` بیرون از `src/lib/api.ts` ⇒ خطای lint (تثبیتِ «یک لایهٔ داده»).
  - **C3** ‏`npm run lint` ⇒ **۰ خطا، ۰ هشدار** (گیتِ موجود در `ci.yml:206`).
  - **C4** تستِ رگرسیونِ قبلی (`test_no_dynamic_import_in_studio_handlers`) **حذف نشود** — کمربند و بند.
  - **C5** اگر نقضِ مشروعی پیدا شد (مثلاً code-splitting واقعیِ یک صفحهٔ سنگین) ⇒ **توقفِ سخت و سؤال**؛ استثناگذاریِ خودسرانه ممنوع.
- **Rollback:** ‏`git revert` یک کامیت.

### P‑5 · گیتِ «buildِ کهنه ممنوع»

- **چرا:** driverِ Exact از راندنِ buildِ قدیمی‌تر از source سرباز می‌زند و فرمانِ بازسازی را چاپ می‌کند. درسِ معادلِ ما: نتیجهٔ سبز از باندل/شاخهٔ کهنه (همان کلاسِ خطایی که ممیز با short-sha و موجِ دومِ CI تجربه کرد).
- **دامنه:** `scripts/staleness_gate.py` (جدید) · یک step در job `docs` کنارِ `scripts/repo_hygiene_gate.py` (`ci.yml:112`) · استفادهٔ اختیاری در `agent_drive.mjs`.
- **معیارهای پذیرش:**
  - **C1** مقایسهٔ زمان/هَشِ source با artifact (‏`mp-app/studio/dist` اگر موجود باشد).
  - **C2** در CI که artifact در workspace نیست ⇒ **skip مستند با دلیل**، نه شکست (job `docs` باید سبز بماند).
  - **C3** پیامِ شکست شاملِ **فرمانِ دقیقِ بازسازی** باشد (`cd mp-app/studio && npm run build`).
  - **C4** exit code فقط ۰ یا ۱؛ یک تستِ pytest برای خودِ گیت (red-first) در مسیرِ موجودِ تست‌های `scripts/`.
  - **C5** job تازه اضافه نشود (قاعدهٔ ۲).
  - **C6** صداقت در LOG: بنویس که در CI عملاً no-op است و ارزشش برای اجرای محلیِ بیلدر/ممیز است.
- **Rollback:** حذفِ step + حذفِ اسکریپت.

### P‑6 · یادداشتِ اصطکاک با یک فرمان

- **چرا:** Exact به agent می‌گوید اصطکاک‌ها را با `feedback note "<what happened>"` ثبت کند. ما `EXECUTION-LOG.md` داریم ولی ورودیِ دستی‌اش چندخطی است و گاه فراموش می‌شود.
- **دامنه:** `scripts/friction_note.py` (جدید) · `docs/MuscleParadise/audit/FRICTION.md` (جدید) · یک خط در `AGENTS.md`/handoff.
- **معیارهای پذیرش:**
  - **C1** ‏`python3 scripts/friction_note.py "متن"` ⇒ یک ردیفِ استاندارد: timestamp UTC · sha شاخه · شناسهٔ `FR-###` · متن.
  - **C2** **بدونِ secret:** پیش از نوشتن، الگوهای کلید/توکن را رد کن؛ در صورتِ شک **ننویس** و هشدار بده (exit ≠ ۰).
  - **C3** ‏`docs_gate` لینکِ `FRICTION.md` را بشناسد و trailing-whitespace/لینکِ خراب نگیرد.
  - **C4** تستِ red-first (شاملِ حالتِ «متنِ مشکوک به secret» ⇒ باید رد شود).
- **Rollback:** حذفِ دو فایل.

### P‑7 · بودجهٔ اندازهٔ bundle (**اختیاری — فقط با تأییدِ صریحِ مالک**)

- **چرا مشروط:** این یک **آستانهٔ تازه** است و طبقِ قواعد، افزودنِ آستانه بدونِ تأییدِ مالک ممنوع است.
- **معیارها (در صورتِ تأیید):** C1 baseline از **عددِ واقعیِ امروزِ** `vite build` (کل + بزرگ‌ترین chunk، به کیلوبایت) در یک فایلِ baseline · C2 گیت داخلِ job `studio` **پس از** stepِ build(۲۱۲) · C3 آستانه = baseline + ۵٪ (نه عددِ حدسی) · C4 کاهش/افزایشِ آستانه بدونِ تأیید ممنوع · C5 پیامِ شکست: عددِ امروز، baseline، و بزرگ‌ترین chunk‌های مقصر.

### P‑8 · ممیزیِ آرتیفکتِ release با REA/Ghidra (**مشروط به تصمیمِ مالک**)

- **چرا مشروط:** امروز هیچ APK/AAB در خطِ لوله ساخته نمی‌شود (`apk.yml` با AD‑21 حذف شد؛ `client-pinned` فقط debug compile می‌کند) ⇒ چیزی برای تحلیل وجود ندارد.
- **در صورتِ تصمیمِ مالک به ساختِ دوبارهٔ release:** ممیزیِ **یک‌بارهٔ** آرتیفکت با **Ghidra (رایگان)** — **نه Hopper** (لایسنسِ تجاری/ demo prompt). اجرا **بیرون از پوشهٔ مخزن** (توصیهٔ خودِ README ‏`rea`). خروجی‌ها پیش از هر commit از secret-scan بگذرند.
- **شاهدهای لازم:** فهرستِ permissionها · `android:debuggable=false` · نبودِ endpoint/secretِ پخته‌شده در باینری · اثباتِ اعمالِ R8/minify · اندازهٔ AAB نسبت به بودجهٔ WP 0.6.
- **در سندباکسِ ممیز BLOCKED-ENV است** (java/flutter/gradle/docker ندارد) ⇒ فقط روی ماشینِ مالک یا محیطِ دارای Java.

---

## ۴) گروه‌بندیِ کامیت‌ها و ترتیب

| بسته | محتوا | کامیت | push |
|---|---|---|---|
| **P‑A** | P‑1 (ساعت) | ۱ | ۱ |
| **P‑B** | P‑2 (درایور) | ≤۲ | ۱ |
| **P‑C** | P‑3 (کدگذاریِ گیت‌ها) | ≤۲ | ۱ |
| **P‑D** | P‑4 (ESLint) + P‑5 (staleness) | ≤۲ | ۱ |
| **P‑E** | P‑6 (friction note) | ۱ | ۱ |
| **P‑F** | P‑7 **فقط** با تأییدِ مالک | ≤۱ | ≤۱ |

- پیش از هر push: ‏`lint`/`format` + تستِ همان حوزه.
- اجرای **کاملِ** تست‌ها (backend + studio) فقط یک بار، پس از P‑E؛ سپس جدولِ SUMMARY و توقف برای داوری.
- P‑8 هیچ‌وقت خودکار شروع نشود.

---

## ۵) پروتکلِ داوریِ ممیز — این خروجی‌ها را در `EXECUTION-LOG.md` بگذار

1. ‏`git diff --stat` هر کامیت + فهرستِ فایل‌ها از `gh api repos/…/commits/<sha>`.
2. ‏`npm test` در `mp-app/studio` ⇒ شمارِ pass/fail/skip + زمانِ کل.
3. ‏`npm run lint` ⇒ `۰ خطا، ۰ هشدار` (خروجیِ خام).
4. ‏`python3 scripts/docs_gate.py; echo EXIT=$?` و `python3 scripts/interaction_map.py --check; echo EXIT=$?` — **پیش و پس از P‑3** + `diff` دو خروجی (برای C4/C5).
5. دو اجرای پشتِ‌سرِهمِ درایور + `sha256sum` هر دو (C2ِ P‑2).
6. ‏`grep -rE "new Date\(|Date\.now\(" mp-app/studio/src | grep -v lib/clock.ts | wc -l` ⇒ `۰` (C3ِ P‑1).
7. ‏`python3 scripts/staleness_gate.py; echo EXIT=$?` در دو حالتِ «artifact نیست» و «artifact کهنه» (C2/C3ِ P‑5).
8. نتیجهٔ CI: ‏`run id` + وضعیتِ **هر ۸ job**.
9. برای P‑3: خروجیِ `--json` روی یک نمونهٔ خراب (C6).
10. هر ادعای «بدونِ وابستگیِ تازه»: ‏`git diff --stat -- '*package.json' '*package-lock.json' '*requirements.txt'` ⇒ خالی یا فقط script.

---

## ۶) توقفِ سخت (سؤال از مالک/ممیز — بقیهٔ موارد را خودت با `D-n` حل کن)

- نیاز به **هر** وابستگیِ تازه (npm/pip، حتی dev).
- نیاز به **job تازهٔ CI** یا هر ویرایشی در ruleset ‏`27826883`.
- هر تغییرِ تضعیف‌کننده: کاهشِ آستانه، حذف/skip تست، افزودنِ استثنا به `ROUTE_EXCEPTIONS`، شل‌کردنِ احراز هویت.
- نوشتنِ باینری/تصویر/PNG در مخزن.
- نقضِ **مشروعِ** قاعدهٔ lint در P‑4 (مثلاً code-splitting واقعی).
- یافتهٔ secret-scan بیرون از سه مسیرِ مجازِ AD‑23.
- شروعِ P‑7 یا P‑8 بدونِ تأییدِ صریحِ مالک.
- قرمزیِ CI که علتش خارج از بستهٔ خودت است.

---

## ۷) تعریفِ DONE برای کلِ فاز P

- همهٔ `C-n` های P‑1…P‑6 سبز، با سنجهٔ خامِ هر کدام در `EXECUTION-LOG.md`.
- ‏`npm run lint` ⇒ ۰/۰ · `npm test` بدونِ شکست · هر **۸ job** سبز روی tip.
- ‏`docs_gate` و `interaction_map` با **معنیِ یکسان** و فرمتِ کددار؛ `GATE-CODES.md` کامل و لینک‌سنجی‌شده.
- ردیف‌های متأثر در `docs/MuscleParadise/audit/CHECKLIST.md` (F‑28 نیمهٔ استودیو، F‑19 تثبیت) به‌روز با sha و ستونِ شاهدِ پُر.
- جدولِ **SUMMARY**: فاز · کامیت · معیارها · سنجه · وضعیت.
- توقف برای داوریِ عددیِ ممیز. ‏**merge فقط توسط مالک.**

---

### بازیابیِ این فایل اگر سندباکس reset شد

```bash
curl -fsS -H "Accept: application/vnd.github.raw" \
  "https://api.github.com/repos/yousefghorbanian98-create/Chat2DB/contents/handoff/MP-PRODUCTION-PLAN-P-2026-11-22.md?ref=arena/2cde32d6-chat2db" \
  -o /tmp/PLAN-P.md
sha256sum /tmp/PLAN-P.md   # باید با hash ثبت‌شده در handoff/README.md برابر باشد
```
