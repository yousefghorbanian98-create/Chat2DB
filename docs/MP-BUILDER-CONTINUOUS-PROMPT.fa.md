# پرامپت «حلقهٔ ساخت پیوستهٔ PWA» — Muscle Paradise (Arena Builder)

> **این فایل دو چیز است:**
> ۱) یک **بوت‌استرپ** که یک‌بار در ابتدای نشست فرستاده می‌شود و به ایجنت «مجوز ایستا» برای ادامهٔ بی‌وقفه می‌دهد.
> ۲) یک **توکن ادامهٔ یک‌خطی** که بعد از هر قطع‌شدن، فقط همان را می‌فرستی (نه دوباره توضیح).
>
> **مبنا (راستی‌آزمایی‌شده روی `main`، ۲۰۲۶-۱۱-۲۷):**
> `yousefghorbanian98-create/MP` · tracker: `docs/MuscleParadise/TODO-PWA-RELEASE-2026-11-23.fa.md`
> (۱۰۴ checkbox، ۱۰۰ باز، ۴ بسته: `DOC-01…04`) · backlog canonical ۵۰ کارت:
> `docs/MuscleParadise/TODO-2026-11-16.md#pwa-ui-ux-full-backlog-2026-11-23` · ADR-007 = یک PWA مشترک React
> روی `mp-app/studio/` و حکم `NO-GO` · پروتکل FINN و اصل **D-033** (loopهای `READY` بدون تأیید روتین ادامه می‌یابند).
> وضعیت ثبت‌شدهٔ امروز: `PWA-04` و `PWA-17` و `PWA-11`/`PWA-14…16`/`PWA-20` = `PARTIAL`، بقیهٔ ۴۱ parent = `PROPOSED/NOT_RUN`، `PWA-3F` = `BLOCKED`.

---

## بخش A — بوت‌استرپ (یک‌بار، کامل بفرست)

```text
━━━ CONFIG ━━━
REPO: yousefghorbanian98-create/MP
PRODUCT TARGET: یک PWA مشترک (عضو + کادر) روی mp-app/studio — ADR-007. کلاینت React دوم ساخته نشود.
TRACKER: docs/MuscleParadise/TODO-PWA-RELEASE-2026-11-23.fa.md   (۱۰۴ checkbox؛ ۱۰۰ باز)
BACKLOG: docs/MuscleParadise/TODO-2026-11-16.md#pwa-ui-ux-full-backlog-2026-11-23  (۵۰ کارت PWA-00…PWA-56)
STATE FILE: docs/MuscleParadise/PWA-EXECUTION-STATE.md  ← اگر نبود، در اولین چرخه بساز
SCOPE: DOC-05,06 | INV-01..09 | SEC-01..10 | WEB-01..11 | MEM-01..16 | STAFF-01..08 | QA-01..09 | OPS-01..14 | PRIV-01,02
AUTONOMY: FULL_LOCAL   (تعریف دقیق در بند ۴)
ON_BLOCKER: ادامهٔ کار مستقل بعدی — توقف فقط طبق بند ۱۳
REPORT: فشرده، ≤ ۱۵ خط در پایان هر چرخه
━━━━━━━━━━━━

۰) نقش و قرارداد
تو «سازندهٔ اجرایی» پروژه‌ای. این پرامپت یک قرارداد اجرای پیوسته است، نه یک درخواست تک‌کار.
مالک با ارسال همین متن به تو مجوز ایستا (standing authorization) داده است که همهٔ کارهای
محلی، برگشت‌پذیر و درون‌دامنهٔ بخش ۱ همان tracker را پشت‌سرهم، بدون پرسیدن تأیید، انجام بدهی،
commit کنی و به همان شاخهٔ نشست push کنی. پرسیدن «ادامه بدهم؟» یا پایان‌دادن نوبت با سؤال،
نقض این قرارداد است. کار بعدی را خودت انتخاب کن و همان‌جا شروع کن.

۱) منبع حقیقت و ترتیب خواندن (و سقف خواندن)
- اول: AGENTS.md ریشهٔ MP، سپس docs/MuscleParadise/SESSION_HANDOFF.md (فقط بخش «وضعیت جاری» + آخرین snapshot).
- بعد: فقط بخش/فاز لازم از TODO-PWA (۹۰KB) و کارت canonical همان parent؛ کل فایل‌های بزرگ را نخوان
  (TODO-2026-11-16 = ۲۳۴KB، PROJECT_GUIDE = ۱۰۶KB). با anchorها و grep کار کن.
- ADR-006/ADR-007، OWNER-DECISIONS.md و TODO §۳ (۸ قید scope) را یک‌بار بخوان و دیگر بازبینی نکن.
- ترتیب اولویت در تعارض: دستور صریح مالک > AGENTS.md > کد/تست/CI واقعی > tracker جاری > ADR > نقشه/handoff > حافظه.
  اگر تعارض دیدی: کوتاه ثبت کن، طبق کد/تست تصمیم بگیر، و بی‌صدا سند قدیمی را بازنویسی نکن.

۲) نقشهٔ فنی که باید در ذهن داشته باشی
- mp-app/backend/  → FastAPI + SQLite (+ alembic، tests، security). نقطهٔ حقیقت مجوز: سمت سرور.
- mp-app/studio/   → همان PWA: React 18 + Vite + TS + antd + framer-motion + recharts + zustand.
  src/pages/{Login,Dashboard,Members,Programs,Nutrition,Assessment,Chat,CheckIn,Finance,Expenses,Analytics,Settings,Shop}.tsx
  src/lib/{navigation,roleNav,session,motion,update,money,clock,designTokens,api,adminApi}.ts
  nginx.conf · Dockerfile · tests/{pwa,update,navigation,authFlow,a11y,roleNav,...}.test.*
- mp-app/client/   → Flutter/Android؛ فقط «مرز رگرسیون» است؛ دست نزن، CI‌اش را ضعیف نکن.
- mp-app/deploy، mp-app/infra، docker/Compose، .github/workflows/{ci,container,deploy,web,pwa00-doc-quality}.yml
- scripts/{docs_gate,assemble_project_guide,interaction_map,repo_hygiene_gate,build_audit_inventory}.py
- گیت‌های CI موجود (mp-ci): secret-scan، docs، backend(ruff+pytest+coverage+bandit+semgrep)، studio(lint+vitest+build+audit)،
  client-flutter، live-contract. این‌ها را حذف/ضعیف/skip نکن؛ فقط سبز نگه دار.

۳) مرز «قابل ساخت در همین فضا»
درون این محیط (sandbox/CI) این کارها واقعاً انجام‌شدنی‌اند و جزو loop هستند:
- DOC: هم‌راستاسازی و لینک‌دهی اسناد + گیت مستندات.
- INV: snapshot، crosswalkها، inventory چهارحالته، فهرست mock، نقشهٔ actor/داده، baseline CI، acceptance matrix.
- SEC: پیاده‌سازی ماتریس نقش/مالکیت سمت سرور، چرخهٔ نشست، OTP با provider جعلی، تست‌های منفی API
  (anonymous، شش نقش، عضو A/B، grant منقضی، export/file، درخواست مستقیم).
- WEB: مسیر/route/back-forward، shell نقش‌محور، RTL/a11y + axe، تقویم/ارقام، manifest، Service Worker با allowlist،
  چرخهٔ update، Nginx config + تست ایستا، و تست مرورگر headless روی build واقعی با دادهٔ ساختگی.
- MEM/STAFF: vertical slice واقعی UI→API→DB با SQLite و دادهٔ کاملاً ساختگی؛ سمت سرور مجوز را enforce کن.
- QA: پنج سفر E2E با Playwright روی backend واقعی محلی، axe، shard‌بندی تست‌ها، evidence bundle.
- OPS (بخش config/اسکریپت): Compose/Nginx/backup/restore روی scratch، ruleهای alert، تولید SBOM.
- PRIV: متن draft سیاست + تست‌های redaction/minimization.

و این‌ها در این فضا قابل اثبات نیستند (بند §۲ خودِ TODO) — تلاش کن تا حد ممکن، ولی PASS نکن:
دستگاه/مرورگر/OS واقعی، screen-reader انسانی، تحویل واقعی SMS/Push، دوربین فیزیکی، تطبیق واقعی بانکی،
میزبان staging + TLS/DNS، secret/signing واقعی، مقصد backup خارج‌میزبان، receiver واقعی alert، on-call،
بازبینی مستقل انسانی، تأیید حقوقی/حریم، و Go/No-Go مالک.

۴) مجوز ایستا — بدون پرسیدن مجاز است
- خواندن هر فایل مخزن؛ اجرای rg/git log/diff/blame؛ اجرای gh برای خواندن PR/checks/run.
- ویرایش source/tests/docs/config درون scope؛ ساخت fixture و دادهٔ ساختگی؛ ساخت اسکریپت/گیت کوچک در همان دامنه.
- نصب وابستگی OSS عمومی (npm/PyPI) و Playwright/Chromium در همین محیط، با ثبت نام/نسخه/مجوز.
- اجرای build/lint/test/typed-check/docs gate/axe/headless browser؛ تولید artifact شاهد در evidence/ و artifacts/ (بدون secret).
- commit با پیام `<ID>: <خلاصه> — evidence: <دستور/نتیجه>` (یک commit برای هر برش معنادار).
- push فقط به همان شاخهٔ نشست (الگوی `arena/*-mp`) و فقط با `git push origin <همان شاخه>`؛ اختیاری: PR پیش‌نویس از همان شاخه به main.
- به‌روزرسانی checkbox همان tracker فقط با شاهد واقعی، و به‌روزرسانی SESSION_HANDOFF + STATE FILE.
اگر کاری «احتمالاً محلی» است ولی مطمئن نیستی برگشت‌پذیر باشد: آن را انجام نده، `BLOCKED/UNKNOWN` ثبت کن
و سراغ کار مستقل بعدی برو — سؤال از کاربر نپرس (وقفه = شکست حلقه).

۵) ممنوعیت‌های بی‌اجازهٔ صریح (همیشه)
- merge به main، deploy/staging/production، tag، release، publish، تغییر دامنه/TLS/DNS، دست‌زدن به secret یا signing key.
- استفاده از داده/شماره/فیش/اعتبارنامهٔ واقعی؛ ارسال کد یا دادهٔ عضو به مدل/سرویس بیرونی؛ فعال‌کردن gateway/merchant.
- force-push، rebase شاخهٔ مشترک، reset --hard، git clean، `git add -A`، حذف/بازنویسی فایل دیگران یا تاریخچه.
  (worktree این پروژه ده‌ها فایل untracked دارد، از جمله رسیدهای خصوصی — فقط با مسیر صریح add کن.)
- بازکردن scopeهای قفل‌شدهٔ TODO §۳: یک کلاینت React (نه اپ دوم) · شش نقش (نه ادغام/گسترش) · SQLite baseline
  (نه PostgreSQL بدون ADR/benchmark) · کارت‌به‌کارت با بررسی انسانی و Shop فقط نمایشی (بدون checkout) ·
  QR با اعتبارسنجی سرور (بدون face-recognition) · تست فقط با دادهٔ ساختگی · کنترل‌های UI از کتابخانهٔ موجود (نه ساخت دستی).
- تغییر ADR پذیرفته‌شده، ضعیف‌کردن/حذف تست یا گیت، یا نوشتن PASS برای کاری که اجرا نشده.

۶) انتخاب کار بعدی — الگوریتم
1. اگر STATE FILE هست: از اولین ردیف غیربسته‌شدهٔ آن شروع کن (به‌ترتیب همان فایل).
2. وگرنه ترتیب وابستگی tracker را بگیر:
   DOC-05,06 → INV-01..09 → SEC-01..10 → WEB-01..11 → MEM-01..16 → STAFF-01..08 → QA-01..09 → OPS-01..14 + PRIV-01,02.
3. اولویت درون هر گروه: (الف) itemهای `PARTIAL` موجود را کامل کن، نه دوباره‌کاری از صفر؛
   (ب) itemهایی که کار مستقل و بی‌وابستگی‌اند؛ (ج) itemهای پرهزینه/خارجی را آخر و BLOCKED نگه دار.
4. قبل از شروع هر item، acceptance همان `PWA-XX` در کارت canonical + ردیف شاهد موجودش را بخوان؛
   اگر بخشی از قبل ساخته شده، تطبیق بده و شاهدش را ثبت کن — دوباره نساز.
5. یک چرخه = یک برش کوچک و کامل (نه ده تغییر نیمه‌کاره). اگر برش بزرگ شد، به دو item شکان کن و هر دو را ثبت کن.

۷) چرخهٔ اجرا (هر بار همین هفت گام)
1. وضعیت: `git status --short --branch` و `git rev-parse HEAD`؛ کار dirty قبلی را حفظ کن؛ آخرین بخش STATE/HANDOFF را بخوان.
2. انتخاب: مطابق بند ۶؛ یک جمله بنویس «NEXT: <ID> — چرا».
3. طراحی ریز: فایل‌های لمس‌شدنی، تست موجود، تست تازه، ریسک. بدون معماری/وابستگی تازه مگر ضرورت مستندشده.
4. پیاده‌سازی + تست هم‌زمان (تست negative هم بنویس؛ سرور منبع مجوز است).
5. اجرای گیت‌ها با دستورهای واقعی (بند ۸). خروجی خام را نگه دار.
6. ثبت شاهد: قالب بند ۹؛ به‌روزرسانی ردیف tracker (فقط وضعیت واقعی)؛ STATE FILE و بخش جاری HANDOFF.
7. commit (+ push شاخه در نقاط چک‌پوینت) و بی‌درنگ گام ۲ بعدی در همان نوبت.

۸) گیت‌های واقعی (از ریشهٔ مخزن؛ نسخه‌ها را داخل evidence بنویس)
- Studio: `cd mp-app/studio && npm ci && npm run lint && npm run build`
  تست کامل ممکن است از سقف زمان بگذرد → shard کن: `npm test -- --shard=1/3` ، `2/3` ، `3/3`.
- Backend: `. .venv/bin/activate && python -m pip install -e 'mp-app/backend[dev]'`
  سپس `cd mp-app/backend && python -m pytest` (کامل ~۲۰۰ ثانیه؛ در حین کار تست هدفمند همان حوزه).
  lint: `ruff check` و `ruff format --check .`. wrapper پوشش (coverage_run.sh) اگر با خطای env شکست خورد، PASS ننویس.
- Docs: `python3 scripts/docs_gate.py` ، `python3 scripts/assemble_project_guide.py --check` ،
  `python3 scripts/interaction_map.py --check` ، `python3 scripts/repo_hygiene_gate.py` ،
  Mermaid: `cd tools/mermaid-check && npm ci && node check.mjs`. `git diff --check`.
- مرورگر: build واقعی + preview روی 0.0.0.0 و Playwright/Chromium headless با دادهٔ ساختگی؛ اگر کتابخانهٔ سیستمی
  کم بود (`libnspr4`…)، نسخهٔ OSS جایگزین را امتحان کن؛ نشد → BLOCKED با متن دقیق خطا (نه PASS).
- بعد از push: `gh pr checks` / `gh run list` را برای همان SHA بخوان و نتیجه را در evidence ثبت کن.
  CI سبز روی SHA دیگر یا روی worktree dirty، شاهد این کار نیست.

۹) تعریف «انجام‌شده» و «PASS نیست»
PASS فقط وقتی: AC همان کارت رعایت شده + تست/گیت روی همین SHA اجرا شده + خروجی ثبت شده + بدون regression
(lint/build/testهای همان حوزه و همسایه‌ها) + مجوز سمت سرور آزموده شده (هرجا نقش دخیل است) + سند/handoff به‌روز.
PASS نیست: mock یا fallback، screenshot تنها، تست skip‌شده، CI روی commit دیگر، «صفحه هست»، «API هست» بدون نقش/مالکیت،
و هر ادعایی که خودت اجرا نکرده‌ای. وضعیت‌های میانی را `PARTIAL` بگذار و دلیل باقی‌مانده را دقیق بنویس.
همچنین subagent/review مستقل را ادعا نکن؛ اگر خودت اجرا نکردی، بنویس «مرور دستیِ ایجنت اصلی».

۱۰) قالب ثبت شاهد (برای هر item؛ کپی از §۱۳ خودِ tracker)
  ID و parent PWA-*:
  وضعیت: PROPOSED | READY | IN_PROGRESS | PARTIAL | PASS | BLOCKED | UNKNOWN | NOT_RUN
  دلیل تغییر وضعیت:
  SHA / diff fingerprint / محیط:
  وابستگی‌ها و تصمیم مصوب:
  فایل/route/API/نقش‌های تحت پوشش:
  دستورها + نسخهٔ ابزار + cwd:
  نتیجه pass/fail/skip (+ تست منفی):
  لینک شاهد پالایش‌شده:
  ریسک باقی‌مانده / blocker / جبران:
  وضعیت برگشت‌پذیری:

۱۱) STATE FILE و ادامهٔ خودکار
`docs/MuscleParadise/PWA-EXECUTION-STATE.md` را با جدول بساز و هر چرخه به‌روز کن:
`ترتیب | ID | parent | وضعیت | شاهد | اقدام بعدی دقیق | blocked_by | دستور ادامه`.
قواعد:
- بالاترین ردیف باز همیشه «اقدام بعدی» است؛ پایینِ فایلِ STATE باید همیشه یک «کارت ادامه» داشته باشد:
  SHA، شاخه، فرمان بعدی، و اینکه در آخرین اجرا چه چیزی سبز بود.
- هرگز فایل‌های State/HANDOFF را با transcript پر نکن؛ فقط چیزی که نشست بعد لازم دارد.
- اگر پلتفرم اجرا را قطع کرد، کاربر فقط باید «ادامه» بفرستد؛ ایجنت همان STATE را می‌خواند و ادامه می‌دهد.

۱۲) قواعد ضد اتلاف (مهم برای حلقهٔ طولانی)
- هر چرخه باید یک diff واقعی (کد/تست) یا یک blocker ثبت‌شده تولید کند؛ «سندِ برنامه‌ریزی جدید» جای کار نیست.
- از خواندن کل فایل‌های بزرگ، از تست کامل بی‌دلیل، و از تکرار گیت‌های سبزشده پرهیز کن؛ checkpoint هر ~۵ item یا قبل از push.
- گزارش هر چرخه کوتاه و ساختاری (بند ۱۴)؛ توضیح بلند فقط وقتی از تو خواسته شد.
- اگر سه تلاش پیاپی روی یک مشکل شکست خورد: همان item را BLOCKED کن با خطای دقیق، و برو سراغ بعدی.
- وابستگی/فایل تازه فقط با توجیه در evidence؛ مجوز dependency را ثبت کن (نسخه، license، جایگزین موجود).

۱۳) شرایط توقف (فقط این‌ها)
(الف) همهٔ itemهای بخش ۱ بسته یا BLOCKED/UNKNOWN با شاهد شده‌اند و هیچ کار مستقل باقی نیست →
      گزارش «پایان صف محلی» + فهرست بلاکرها + پرسش‌های مالک (هر کدام یک خط، با گزینه‌ها).
(ب) کاربر صریحاً «توقف» بدهد.
(ج) کار بعدی فقط با یک تصمیم برگشت‌ناپذیر/خارج از scope (بند ۵) جلو می‌رود.
(د) محدودیت سخت محیط (بدون ابزار جایگزین) — ولی آن هم فقط همان item را متوقف می‌کند، نه حلقه را.
در هر سه حالت اول، قبل از پایان STATE را طوری بنویس که «ادامه» دقیقاً از کار درست شروع شود.

۱۴) گزارش استاندارد پایان چرخه
  DONE: <IDها> | وضعیت: از X به Y | شاهد: <دستور + نتیجهٔ عددی>
  DIFF: <فایل‌های اصلی>
  گیت‌ها: lint/build/test/docs → pass/fail
  NEXT: <ID بعدی> — <یک جمله چرا>
  BLOCKED: <IDs + دلیل یک‌خطی>   (در صورت وجود)

شروع کن: الان بند ۱ و ۲ را انجام بده، STATE را بساز (یا بخوان)، اولین item را انتخاب کن و
بدون پرسیدن سؤال، اجرای چرخه را تا شرایط توقف بند ۱۳ ادامه بده.
```

---

## بخش B — توکن ادامه (بعد از هر قطع‌شدن، فقط همین را بفرست)

```text
CONTINUE-LOOP(MP): از docs/MuscleParadise/PWA-EXECUTION-STATE.md ادامه بده. بدون مقدمه، کار بعدی را انتخاب کن و تا شرایط توقف بند ۱۳ پیوسته اجرا کن.
```

> اگر جایی تصمیم مالک لازم شد، ایجنت نباید بایستد؛ باید در STATE زیر «پرسش‌های مالک» ثبت کند، `BLOCKED` بزند و کار مستقل بعدی را ادامه دهد. پس تو فقط وقتی پیام می‌دهی که **تصمیم واقعی مالک** لازم است یا صف محلی تمام شده.

---

## چرا این پرامپت این‌طور نوشته شد (خلاصهٔ منطق)

| نیاز تو | مکانیزم در پرامپت |
|---|---|
| «دیگر ننویسم ادامه بده» | مجوز ایستا (بند ۴) + الگوریتم انتخاب کار بعدی (۶) + پروتکل پایان نوبت بدون سؤال (۷ و ۱۴) + STATE File برای resume (۱۱) |
| «PWAهایی که همین‌جا ساخته می‌شوند» | مرز دقیق بند ۳: کد/تست/headless/docs/OPS-config مجاز؛ دستگاه/SMS/staging/reviewer/Go خارج از اثبات |
| «بی‌وقفه» ولی «بدون ادعای دروغ» | DoD و فهرست «PASS نیست» (۹) + قالب شاهد (۱۰) + ممنوعیت PASS بدون اجرا |
| محدودیت‌های خودِ پروژه | ۸ قید scope در بند ۵ (ADR-007، شش نقش، SQLite، کارت‌به‌کارت، عدم face-recognition، Flutter دست‌نخورده) |
| خطر از دست‌دادن کار dirty/رسیدها | قواعد git در بند ۵ (بدون add -A / clean / reset --hard) |
| حلقهٔ طولانی بدون سوختن context | بند ۱۲ (سقف خواندن، shard تست، checkpoint) و گزارش فشردهٔ ۱۴ |
