# پیش‌نویس خردسازی برنامه با الگوی Finn-loop

> **وضعیت: پیش‌نویس مستقل برای بازبینی مالک.** این فایل نه backlog مصوب است، نه ADR و نه بخشی از Architecture Atlas؛ به index معماری اضافه نشده است. هیچ issueای در Linear/GitHub ساخته نشده و Finn-loop نصب، ادغام یا پیکربندی نشده است. این سند از الگوی `spec → build → review → human merge` استفاده می‌کند.
>
> **مبنای خردسازی:** `system-integrated-flow-v1-2026-11-23.dot/.md` و اسناد جزئی‌ای که همان نمودار به آن‌ها ارجاع می‌دهد؛ `WIRING-LEDGER.md` و `API-ROUTE-CATALOG.md`؛ چرخهٔ ورزشکار/برنامه‌ساز، معماری مسیریابی منابع و پیش‌نویس برنامهٔ تولید. نمودار اصلی ۶۶ گره و ۷۴ یال دارد؛ کاتالوگ API نیز ۱۶۳ operation در ۱۴۱ قالب مسیر را پوشش می‌دهد.
>
> **مرز شواهد:** نمودار، کدخوانی و آزمون گزارش‌شده، معادل اجرای تازهٔ E2E، آزمون دستگاه، production یا تأیید محصول نیستند. برچسب‌های `CURRENT-VERIFY`, `GAP`, `TARGET`, `DECISION` و `CONDITIONAL` در پایین عمداً از هم جدا شده‌اند. این worktree از قبل تغییرات محلی متعددی دارد؛ پیش‌شرط Finn-loop یعنی worktree تمیز در این snapshot برقرار فرض نمی‌شود. هیچ فایل موجودی را stash/reset/overwrite یا پاک نکنید؛ ابتدا باید تغییرات قبلی به‌طور امن از کارهای تازه جدا شوند.

## ۱. قرارداد خردسازی به سبک Finn-loop

### ۱.۱ تعریف واحد کار

یک میکرولوپ پیشنهادی معادل **یک issue با یک نتیجهٔ قابل‌مشاهده و قابل‌آزمون، یک PR، یک بازبینی مستقل و تصمیم انسانی برای merge** است. «کوچک» به معنی چند خط کد نیست: issue باید آن‌قدر محدود باشد که دو مهندس از متن AC/NG به یک رفتار قابل‌مشاهده برسند. راهنمای Finn-loop اندازهٔ حدود یک روز کار عامل یا کمتر را پیشنهاد می‌کند؛ این فقط heuristic اولیه است، نه تخمین زمان مصوب برای Muscle Paradise.

هر کارت باید این فیلدها را داشته باشد:

```text
ID و parent layer / flowchart node
Problem
Acceptance Criteria: AC-1, AC-2, ...
Non-goals: NG-1, NG-2, ...
Dependencies / blocked-by
Relevant nodes, files, API operations and evidence source
Risk class + data class
Test expectations + numbered verification steps
Evidence required for gates 1–9
Budget limits and stop/escalation rule
Owner/spec approval, independent reviewer, human merge
```

اگر یک AC هنوز به تصمیم، قرارداد، منبع داده یا runtime نامعلوم وابسته است، کارت `BLOCKED` می‌ماند؛ عامل نباید آن را با حدس بازنویسی کند. اگر یک کارت از یک PR کوچک‌تر نیست، پیش از `agent-ready` شدن دوباره تقسیم می‌شود.

### ۱.۲ همان زنجیرهٔ ۹حوزه‌ای برای **هر کارت**

این چک‌لیست به همهٔ issueهای پیشنهادی پایین الصاق می‌شود؛ هر issue باید نه نتیجهٔ مستقل ثبت کند. پیکربندی بعضی کنترل‌ها ممکن است در سطح مخزن انجام شود، ولی هر میکرولوپ باید دوباره نشان دهد که کنترل در همان کار رعایت شده است. `UNKNOWN` هرگز `PASS` نیست. فقط در صورت واقعاً نامرتبط‌بودن می‌توان `N/A + دلیل + تأیید انسانی` ثبت کرد؛ حذف بی‌صدای gate مجاز نیست.

| شماره | حوزهٔ اجباری هر issue | خروجی/evidence همان میکرولوپ |
|---:|---|---|
| ۱ | **مشخصات و خردکردن کار** | AC/NG مشاهده‌پذیر، parent layer، dependency و تصمیم‌های حل‌نشده. |
| ۲ | **محیط ایزوله** | worktree/container مجزا، fixture مصنوعی، محدودهٔ دسترسی و وضعیت secret/network. Worktree به‌تنهایی sandbox امنیتی محسوب نمی‌شود. |
| ۳ | **کنترل فرمان‌ها و تغییرات** | command/tool policy، مسیرهای مجاز، خلاصهٔ diff؛ هر تغییر خارج از scope یا عملیات مخرب = توقف. |
| ۴ | **CI، آزمون و امنیت** | آزمون‌های متناسب با AC، scanهای مصوب و نتیجهٔ همان revision؛ تست جاافتاده = `BLOCKED/UNKNOWN`. |
| ۵ | **حفاظت شاخه** | PR، required checks و قواعد branch؛ نبودن یا bypass شدن rule نتیجهٔ قبولی نیست. عامل merge نمی‌کند. |
| ۶ | **ردپا و attestation** | task ID، base/head SHA، نسخهٔ ابزار، CI run، reviewer و evidenceهای پالایش‌شده و متصل به commit دقیق. |
| ۷ | **تأیید انسانی** | تأیید قرارداد پیش از build، escalation موارد مبهم/پرریسک و تصمیم انسانی برای merge. تأیید متن issue با تأیید محصول/ایمنی یکی نیست. |
| ۸ | **سقف زمان، تلاش و هزینه** | سقف عددی پیش از شروع تعیین؛ مصرف در تمام مراحل پایش؛ رسیدن به سقف = توقف و ارجاع، نه retry نامحدود. اعداد هنوز باید مالک تعیین کند. |
| ۹ | **آزمون خصمانهٔ عامل** | ورودی خصمانه/تزریق prompt، تلاش برای عبور از مجوز، افشای داده یا گسترش scope؛ بازبینی مستقل روی head SHA نهایی. |

سقف بودجه در عمل از ابتدا تنظیم می‌شود، هرچند در فهرست مفهومی شما حوزهٔ هشتم است. گیت branch protection هم یک‌بار به‌جای همهٔ issueها PASS نمی‌شود: وضعیت آن برای هر PR جدا بررسی می‌شود.

### ۱.۳ وضعیت کارت‌ها

- `PROPOSED`: خردسازی پیشنهادی؛ نه آمادهٔ اجرا.
- `DECISION`: پاسخ مالک/متخصص لازم است.
- `BLOCKED`: به تصمیم یا dependency پاس‌نشده وابسته است.
- `READY-FOR-OWNER`: AC/NG کامل است و فقط بررسی مالک برای تبدیل‌شدن به کار قابل‌اجرا مانده است.
- `AGENT-READY`: فقط پس از تأیید صریح issue و برقرارشدن هر ۹ حوزه.
- `BUILDING → REVIEW → OWNER-REVIEW → DONE`: وضعیت اجراییِ احتمالی در tracker.

موفقیت یک کارت، نتیجهٔ کارت قبلی را برای کارت بعدی به ارث نمی‌دهد. فقط بعد از تکمیل شواهد، بازبینی، تصمیم انسانی و ادغام در مبنای موردتوافق، وابستگیِ بعدی باز می‌شود. کارهای واقعاً مستقل فقط با dependency صریح و worktreeهای جدا می‌توانند موازی شوند.

## ۲. کارت‌های تصمیم مالک — پیش‌نیازهای باز، نه انتخاب ایجنت

این کارت‌ها چیزی را خودکار تغییر نمی‌دهند. AC هر کدام، ثبت یک تصمیم صریح با دامنه و اثرش است؛ اگر مالک انتخاب نکند، کارهای وابسته `BLOCKED` می‌مانند.

| ID | تصمیم | AC برای بسته‌شدن کارت | NG / وابستگی |
|---|---|---|---|
| D-01 | دامنهٔ client انتشار اول | مالک روشن کند baseline، Android عضو + Studio وب است یا PWA هدف جایگزین می‌شود؛ پلتفرم‌ها و آزمون‌های لازم ثبت شوند. | هیچ فایل Flutter/Android حذف یا مهاجرت نمی‌شود؛ انتخاب PWA از طرح قبلی فرض گرفته نمی‌شود. |
| D-02 | topology و ingress | میزبان، مرز شبکه، HTTPS ingress، مالک عملیات و معیار دسترس‌پذیری روشن شود؛ سرور محلی/Full Cloud بدون تصمیم جایگزین نمی‌شود. | خرید VPS، تونل، دامنه یا deploy انجام نمی‌شود. |
| D-03 | نقش‌ها و grants | حفظ ۶ نقش فعلی یا تعریف target دیگری، ماتریس مجوز و مرجع اعطای grant مشخص شود. | مدل ۳نقشیِ طرح قدیمی به‌عنوان مهاجرت مصوب تلقی نمی‌شود؛ role/DB تغییر نمی‌کند. |
| D-04 | تک‌باشگاه یا multi-tenant | scope نسخهٔ اول و اثر آن بر شناسه، ownership و دادهٔ هر باشگاه تعیین شود. | معماری tenant یا DB مشترک ساخته نمی‌شود. |
| D-05 | سیاست پرداخت و فروشگاه | پرداخت دستی/تطبیق انسانی، دامنهٔ فروشگاه نمایشی و وضعیت checkout/درگاه در scope نسخهٔ اول روشن شود. | اتصال بانکی یا روشن‌کردن خرید آنلاین/auto-settlement انجام نمی‌شود. |
| D-06 | حریم خصوصی و retention | data classes، consent، مدت نگهداری/حذف، backup و scope عکس بدن/دادهٔ سلامت بررسی و تصویب شوند. | دریافت یا استفادهٔ تازه از دادهٔ واقعی/عکس بدن شروع نمی‌شود؛ تا تصمیم، عکس بدن خارج از scope اجرایی است. |
| D-07 | DB و معیار مهاجرت | آستانهٔ بار، همزمانی، restore و RPO/RTO برای ارزیابی SQLite در برابر PostgreSQL تعیین شود. | صرف وجود PostgreSQL در طرح، مجوز migration نیست. |
| D-08 | سیاست مدل و egress عامل | مدل مجاز، محل اجرا، حدود prompt/code/data egress، inference budget و kill switch روشن شود. | API مدل بیرونی یا دسترسی به دادهٔ عضو پیش‌فرض فعال نمی‌شود. |
| D-09 | مالک عملیات، بودجه و پشتیبانی | مسئول staging/backup/restore/alert و حدود هزینه/زمان/پشتیبانی نام‌گذاری شود. | زیرساخت یا ارائه‌دهنده انتخاب/خریداری نمی‌شود. |
| D-10 | تعریف «همهٔ قابلیت‌های اصلی» | فهرست جریان‌های release، نقش‌ها، دستگاه‌ها، RTL و حداقل شواهد پذیرش مالک مشخص شود. | کامل‌بودن را از روی تعداد صفحه/route نتیجه نمی‌گیریم. |
| D-11 | مرز تغذیه، سلامت و منابع | مسئول حرفه‌ای، جمعیت موردپشتیبانی، منبع/مجوز و حد ادعا برای برنامهٔ تمرین، تغذیه و سنجش تعیین شود. | هیچ diagnosis، درمان، وعدهٔ تغذیه یا ادعای اثر تمرینی از سوی عامل/دادهٔ عمومی ساخته نمی‌شود. |

## ۳. بستهٔ baseline و traceability پیش از اصلاح محصول

| ID | میکرولوپ | Acceptance Criteria | Non-goals و وابستگی |
|---|---|---|---|
| B-01 | برچسب‌گذاری وضعیت همهٔ گره‌های نمودار | هر ۶۶ node به `CURRENT-VERIFY/GAP/TARGET/DECISION/CONDITIONAL` و source/evidence مشخص وصل شود؛ خط‌چین هدف با کد جاری یکی نشود. | تغییر نمودار یا ادعای runtime در این کارت انجام نمی‌شود. |
| B-02 | ردگیری کامل کاتالوگ API | هر یک از ۱۶۳ operation به سطح/actor، guard، ownership/scope، service/data و تست/evidence مربوط map یا با `unmapped` ثبت شود. | metadata export جای ممیزی مؤثر RBAC یا اثبات امنیت نیست. |
| B-03 | تکمیل ماتریس ۳۱ سطح UI | ۱۳ سطح Studio و ۱۸ گروه Flutter به intent، component، endpoint و test/evidence وصل شوند؛ سطوح `Members`, `auth`, `intake`, `progress`, `core` برای بررسی انسانی علامت بخورند. | `tests: []` در generator به معنی اثبات نبود همهٔ آزمون‌ها نیست. |
| B-04 | baseline کد، قرارداد و تغییرات محلی | revision/patch موجود، فایل‌های محلی و محیط آزمون بدون پاک‌کردن یا reset ثبت و از branch کاری عامل جدا شوند. | تغییرات موجود نه به عامل نسبت داده می‌شوند و نه مجوز commit/merge می‌گیرند. |
| B-05 | دفتر شکاف‌های جاری | برای هر flow، ادعای کد، گزارش آزمون، گیت پاس/نامعلوم و آزمون بعدی در یک ردیف قابل‌ردگیری بیاید. | آزمون‌های قبلی در این کارت دوباره اجراشده فرض نشوند. |
| B-06 | رفع تعارض اسناد پس از D-01…D-11 | فقط بعد از تصمیم مالک، منبع جاری برای client، role، پرداخت، topology، عکس بدن و DB ثبت شود و اسناد متعارض با ارجاع روشن هم‌راستا شوند. | واردکردن به Atlas/ADR یا رسمی‌کردن نمودار بدون تأیید صریح ممنوع است. |
| B-07 | محیط و دستورهای آزمون مصوب | commandهای واقعی backend/Studio/Flutter، runner، fixture و pre-existing failureها ثبت شوند تا هر issue دستور تست ساختگی نداشته باشد. | secrets، data یا سرویس production به تست وصل نمی‌شوند. |

## ۴. میکرولوپ‌های جریان‌های قابل‌ردیابی فعلی

وضعیت `CURRENT-VERIFY` می‌گوید ابتدا وجود و شواهد همین snapshot را تأیید کن؛ به معنی «پیاده‌سازی جدید لازم است» نیست. AC هر کارت، یک نتیجهٔ رفتاری قابل‌سنجش است؛ اگر ممیزی نشان داد زیرنتیجه‌ها بیش از یک روز/یک PR هستند، آن کارت باید پیش از `AGENT-READY` دوباره شکسته شود.

| ID | میکرولوپ / گره‌های نمودار | AC و شواهد لازم | NG / وابستگی |
|---|---|---|---|
| F-01 | قرارداد مشترک درخواست/پاسخ · `ui_contract`, `response_rules` | نمونهٔ معتبر برای pending/success, 401/403, 422 با حفظ ورودی, 409 reconcile, 429 `Retry-After` و timeoutِ write آزمون شود. | تغییر قرارداد عمومی یا پنهان‌کردن کنترل به‌عنوان مجوز انجام نمی‌شود. |
| F-02 | API client Flutter/Studio · `api_client` | Bearer/refresh، JSON/multipart، لغو/timeout و مدیریت تکرار برای یک flow انتخابی تا UI قابل‌مشاهده تست شود؛ duplication بین clientها ثبت شود. | موفقیت UI بدون response معتبر قبول نیست. |
| F-03 | FastAPI ingress · `ingress` | CORS allowlist، `X-Request-ID`, validation/error handler, rate-limit و ID floor با تست/پیکربندی دقیق بازبینی شوند. | endpoint admin/metrics عمومی نمی‌شود؛ production config فرض نمی‌شود. |
| F-04 | OTP ورود/عضویت · `ux_member_auth`, `svc_identity`, route_identity | درخواست/تأیید OTP به session و member مربوط شود؛ محدودیت تلاش/انقضا/خطا در contract و آزمون معلوم باشد. | SMS provider واقعی بدون D-02/D-08 و credentials مجاز روشن نمی‌شود. |
| F-05 | چرخهٔ session · `session_gate`, `data_identity` | restore, refresh, logout, revoke یک session و revoke-all در API و client تست شوند؛ token منقضی به وضعیت login برگردد. | token به log/telemetry نمی‌رود. |
| F-06 | تغییر شمارهٔ تلفن · `data_identity`, route_identity | درخواست/تأیید تغییر تلفن، اثبات مالکیت شمارهٔ قبلی و وضعیت ناموفق/منقضی با تست سرتاسری پوشش داده شود. | هیچ تغییر مستقیم رکورد بدون challenge معتبر. |
| F-07 | پروفایل و عضویت · `ux_member_auth`, `svc_identity`, `data_identity` | `/members/me`, پروفایل، فهرست/ساخت/تمدید عضویت و invoice در ماتریس مالکیت/نقش map و آزمون شوند. | کاربر به عضو دیگری دسترسی نمی‌گیرد؛ grant تازه ساخته نمی‌شود. |
| F-08 | RBAC/ownership · `authz_gate`, `deny_path`, `role_target` | برای routeهای حساس نقش+permission+record scope در تست مجاز/غیرمجاز اثبات و 401/403 از ورود به service جدا شود. | منوی UI مرز امنیت نیست؛ مهاجرت ۶ نقش به ۳ نقش تا D-03 متوقف است. |
| F-09 | Flutter shell و navigation · `client_app`, `ux_member_*` | مسیرهای OTP/shell/tabs و deep links، loading/error/empty، RTL و reduced-motion روی build واقعی آزموده شوند. | حذف/بازطراحی client تا D-01 مجاز نیست. |
| F-10 | Studio login و shell · `studio_app`, `ux_staff_*` | login/session `checking/unauthenticated/authenticated`، navigation و بازگشت امن از token expiry آزموده شود. | نقش در UI تنها guard امنیتی فرض نمی‌شود. |
| F-11 | ورود اطلاعات و population gate · `ux_member_training`, `route_training`, `svc_training` | body/contract واقعی `POST /population/gate-check`، validation، unknown و پاسخ قابل‌فهم در Client/API با revision مشخص آزمون شود. | گزارش TestClient قبلی به‌جای اجرای مجدد/دستگاه قبول نمی‌شود؛ جمعیت خارج scope خودکار تأیید نمی‌شود. |
| F-12 | توقف fail-closed برنامه‌ساز · `svc_training`, `composer` | برای `blocked`, `needs_review`, unknown یا red flag ــ با vocabulary تأییدشده ــ برنامهٔ اجرایی عضو ساخته/نمایش داده نشود؛ مسیر coach review روشن باشد. | diagnosis، clearance یا rule پزشکی جدید ساخته نمی‌شود؛ این مثال تا D-11 و تأیید متخصص `BLOCKED` است. |
| F-13 | نمایش نام و شناسهٔ حرکت · `data_training`, `route_training` | `exercise_id` به نام canonical/localized و جزئیات مجاز map شود؛ ID خام در UI عضو جای نام حرکت را نگیرد. | merge خودکار رکوردهای کاتالوگ یا ادعای علمی اضافه نمی‌شود. |
| F-14 | کتابخانهٔ جست‌وجوی حرکت · `route_training`, `svc_training`, `ux_member_training` | فهرست/جزئیات exercise با empty/error/media-missing و access صحیح از Client/Studio آزموده شود. | حرکت candidate یا asset بدون مجوز `approved` تلقی نمی‌شود. |
| F-15 | بازبینی، approve/reject برنامه · `ux_staff_program`, `route_training`, `data_training` | coach/نقش مجاز بتواند draft را با دلیل تأیید/رد کند؛ عضو فقط وضعیت مجاز طبق تصمیم محصول ببیند. | `draft` با `approved` یکی نیست؛ `window.prompt` پذیرش نهایی UX محسوب نمی‌شود. |
| F-16 | ثبت اجرای واقعی و feedback · `ux_member_training`, `data_training` | تیک تمرین/ستِ انجام‌شده، effort و دلیل missed با API/DB و version درست ذخیره، retry و reconcile شوند. | state محلی به‌عنوان persistence/تحویل قطعی معرفی نمی‌شود؛ رفتار offline تا D-01/D-06 محدود است. |
| F-17 | اندازه‌گیری خام و JP7 · `ux_member_health`, `svc_assessment`, `data_assessment` | ورودی خام، واحد، site، protocol و assessor به‌طور جدا نگهداری و mismatch `calf`/`midaxillary` با متخصص/مالک حل شود. | معادلهٔ قفل‌شده یا درصد بدنی ادعای معتبر تلقی/فعال نمی‌شود. |
| F-18 | Axis/FieldTest/ارزیابی مربی · `route_assessment`, `data_assessment` | rubric، منبع نمره، نقش reviewer و تاریخ به history متصل شود؛ self-report با coach-assessed تفکیک شود. | ۱۴ مهارت با ۱۳ محور بدون بررسی معنا map نمی‌شوند. |
| F-19 | گزارش‌ها و trend سنجش · `ux_member_health`, `svc_assessment` | JP7/limb/member history با ownership، missing/stale/not comparable و state UI تفکیک شوند. | مقدار ناموجود صفر یا روند مقایسه‌ناپذیر رشد/افت جا زده نمی‌شود. |
| F-20 | هدف تغذیه vs وعده · `route_nutrition`, `svc_nutrition`, `data_nutrition` | `daily_kcal/macros`, `NutritionPlan`, `MealItem` و `FoodLog` در قرارداد و UI جدا دیده شوند؛ `meals: []` به meal plan کامل تعبیر نشود. | وعده یا توصیهٔ پزشکی/تغذیه‌ای بدون D-11/source/approval ساخته نمی‌شود. |
| F-21 | FoodLog، غذا و وزن · `ux_member_health`, `data_nutrition` | ثبت/خواندن food/weight با owner scope، واحد، تاریخ و تفاوت plan/actual آزموده شود. | مصرف واقعی از هدف یا برنامه استنتاج نمی‌شود؛ source ناقص به صفر تبدیل نمی‌شود. |
| F-22 | کلاس و فهرست برنامه · `ux_member_attendance`, `svc_attendance`, `data_attendance` | ساخت/فهرست کلاس و تقویم زمانی/ظرفیت/منطقهٔ زمانی در Studio و Client بررسی شود. | حضور واقعی/دستگاه از فهرست کلاس نتیجه‌گیری نمی‌شود. |
| F-23 | رزرو، waitlist، cancel/rebook · `route_attendance`, `data_attendance` | ظرفیت، ترتیب صف، cancel فرد منتظر و rebook در تست رقابت/تراکنش واقعی هدف‌گذاری‌شده پوشش یابند. | نتیجهٔ SQLite تک‌فرایندی به race production تعمیم داده نمی‌شود. |
| F-24 | QR حضور و رضایت · `kiosk_ui`, `ux_member_attendance`, `svc_attendance` | صدور token کوتاه‌عمر، رضایت، اسکن، scope، expiry/replay و پاسخ duplicate در API و دستگاه پذیرش آزموده شود. | قفل QR محلی جای server validation نیست؛ مسیر `method=face` تا تصمیم مستقل فعال نمی‌شود و fail-closed می‌ماند. |
| F-25 | پرداخت دستی و فیش خصوصی · `ux_member_money`, `ux_staff_finance`, `svc_finance`, `private_store` | شروع پرداخت، بارگذاری/دسترسی/بازبینی فیش و approve/reject در محیط مصنوعی و با audit ثبت شوند. | تصویر فیش proof بانکی یا موفقیت پرداخت نیست؛ receipt شخصی باز/منتشر نمی‌شود؛ gateway زنده فرض نمی‌شود. |
| F-26 | Wallet/Ledger/Coupon · `route_finance`, `data_finance` | charge/pay/balance/transactions/coupon/reverse به ledger و نتیجهٔ idempotent با تست کمبود موجودی و rollback متصل شوند. | اثر مالی واقعی یا race-safe banking از fixture/SQLite تنها ادعا نمی‌شود. |
| F-27 | Refund · `svc_finance`, `data_finance` | `finance.write`, actor, audit, تکرار/refund-state و خطای role در API و Studio پوشش داده شود. | بازپرداخت بانکی live یا اختیار reception بدون تصمیم ایجاد نمی‌شود. |
| F-28 | Expense، رسید و revision · `ux_staff_finance`, `data_finance` | create/update/delete، receipt خصوصی، revision و grants `finance.read/write` در دسترسی/تست map شوند. | حقوقی/مالی یا سند حسابداری رسمی بدون D-05/D-11 صادر نمی‌شود. |
| F-29 | گزارش مالی ناقص/سود نامعلوم · `svc_finance`, `ux_staff_finance` | دورهٔ ناقص/refund بدون تاریخ و تعریف حسابداری، `complete=false` و نمایش unknown را در UI/API حفظ کند. | دادهٔ ناموجود سود صفر/قطعی یا گزارش رسمی جا زده نمی‌شود. |
| F-30 | فروشگاه نمایشی و checkout خاموش · `ux_member_money`, `svc_finance`, `data_finance` | کاتالوگ/قیمت/وضعیت برای عضو خوانا؛ online purchase در config پیش‌فرض fail-closed؛ staff changes با guard آزموده شوند. | checkout، gateway، سفارش‌گیری عضو یا موجودی production بدون D-05 فعال نمی‌شود. |
| F-31 | گفتگو و مالکیت مکالمه · `ux_member_money`, `ux_staff_admin`, `data_comms` | conversation/message/read به actor و owner scope بسته شود؛ دسترسی عضو A به عضو B منفی‌تست شود. | پیام خصوصی به prompt/telemetry بدون سیاست داده ارسال نمی‌شود. |
| F-32 | صندوق اعلان و reminder · `route_comms`, `data_comms` | list/read/reminder به member scope و وضعیت unread درست وصل شود. | اعلان داخلی به push ارسال‌شده یا تحویل background تعبیر نمی‌شود. |
| F-33 | outbox/scheduler/runtime job · `runtime_jobs`, `svc_comms` | startup، تک‌اجرا/lease، idempotency، retry cap، health/heartbeat و توقف worker در failure با runtime evidence آزموده شوند. | وجود class/builder/test به معنی worker فعال نیست؛ production scheduler بی‌اجازه راه نمی‌افتد. |
| F-34 | Dashboard/KPI/عضو انتخابی · `ux_staff_ops`, `route_comms` | KPI/feed و انتخاب عضو به API/filter/date و role مربوط شوند؛ loading/empty/error و unknown گزارش شوند. | mock/visual chart به منبع زنده یا metric معتبر تعبیر نمی‌شود. |
| F-35 | Settings، grants، flags، retention، audit · `ux_staff_admin`, `data_comms` | grant/revoke، flag، نقش، audit و retention routeها در ماتریس مالک/actor و منفی‌تست map شوند. | تغییر grant با UI hide کنترل نمی‌شود؛ `admin` حق super_admin را به ارث نمی‌برد. |
| F-36 | Health/metrics/updates و استقرار · `ingress`, `operations`, `route_comms` | probeهای readiness/liveness، token metrics، CORS/network exposure و update manifest با topology واقعی آزموده شوند. | metrics/admin به اینترنت عمومی باز نمی‌شود؛ وجود endpoint به معنی production monitoring نیست. |
| F-37 | دسترس‌پذیری و Option 03 | RTL، focus/keyboard، reduced motion، contrast، حفظ ورودی، double-submit، toast/inline و empty/error برای هر سطح UI در ماتریس آزمون ثبت شود. | تأیید رسمی سبک Option 03 یا افزودن library تازه از این کارت نتیجه نمی‌شود. |

### ۴.۱ نگاشت کارت‌های UI به گره‌های نمودار

- Flutter: `client_app`, `ux_member_auth` → F-04…F-09؛ `ux_member_training` → F-11…F-16؛ `ux_member_health` → F-17…F-21 و TARGET-Q/C؛ `ux_member_attendance` → F-22…F-24؛ `ux_member_money` → F-25…F-32.
- Studio: `studio_app`, `ux_staff_ops` → F-10, F-34, F-35؛ `ux_staff_program` → F-15, F-18, F-20؛ `ux_staff_finance` → F-25…F-29؛ `ux_staff_admin` → F-24, F-31…F-36.
- پذیرش: `kiosk_operator`, `kiosk_ui` → F-22…F-24؛ آزمون سخت‌افزار/شبکه یک evidence جدا دارد.

## ۵. میکرولوپ‌های طراحی آیندهٔ فرم ورزشکار و مربی

همهٔ این کارت‌ها `TARGET` هستند. اجرای هرکدام به D-01/D-06/D-11، قرارداد داده و بررسی privacy/role مربوط وابسته است. هیچ‌کدام از وجود فرم یا نمودار به‌تنهایی قابلیت جاری نتیجه نمی‌شوند. هر ردیف یک issue جداست و همان ۹ حوزه را می‌گذراند.

### ۵.۱ فرم ورزشکار Q01–Q11

| ID | مسئله/AC قابل‌مشاهده | NG / وابستگی |
|---|---|---|
| Q-01 | پروفایل/اندازهٔ پایه با واحد، source، زمان و وضعیت self-report/coach-measured جدا در snapshot ثبت شود. | PII/health به prompt یا خروجی عمومی نمی‌رود؛ D-06/D-11. |
| Q-02 | هدف اصلی، اولویت مرتب، افق و معیار موفقیت به‌صورت قابل‌توضیح ثبت شود. | نتیجهٔ تمرین/زمان‌بندی تضمین نمی‌شود؛ D-11. |
| Q-03 | سابقه، وقفه و حرکت/لود اخیر با source/confidence به history وصل شود. | خوداظهاری با log اجراشده یکی نمی‌شود. |
| Q-04 | سلامت/درد/عمل جراحی فقط به حداقل لازم، با unknown و مسیر stop/review ثبت شود. | تشخیص یا auto-clear ساخته نمی‌شود؛ owner/specialist review اجباری. |
| Q-05 | زمان، روز، مدت جلسه، محل و سفر به availability نسخه‌دار تبدیل شود. | عدم پاسخ مساوی availability نیست. |
| Q-06 | تجهیزات واقعی با taxonomy، محل و availability به hard constraint وصل شود. | free text/unknown به «موجود» map نمی‌شود. |
| Q-07 | آلرژی/ترجیح غذایی و آمادگی، با رضایت و جداسازی از planner تمرین ثبت شود. | مکمل یا meal prescription بدون منبع/صلاحیت تولید نمی‌شود. |
| Q-08 | خواب، recovery، استرس، هوازی و خستگی با self-report/source/تاریخ نگه‌داری شوند. | self-report تشخیص یا score پزشکی نیست. |
| Q-09 | علاقه/عدم‌علاقه به‌عنوان preference نرم از درد/restriction سخت جدا شود. | dislike به contraindication تبدیل نمی‌شود؛ درد به نادیده‌گرفتن safety نمی‌انجامد. |
| Q-10 | self-assessment مهارت با تعریف rubric، مقیاس، زمان و `unknown` واقعی ثبت شود. | خودارزیابی معادل تست/مشاهدهٔ مربی نیست. |
| Q-11 | تعهد، مانع، روز قابل‌پایبندی و متن اختیاری با پالایش دادهٔ حساس ثبت شود. | متن آزاد به‌صورت خام در log/PDF/مدل کپی نمی‌شود. |

### ۵.۲ فرم مربی C01–C11

| ID | مسئله/AC قابل‌مشاهده | NG / وابستگی |
|---|---|---|
| C-01 | مربی snapshot ورزشکار را تأیید/اصلاح کند؛ actor، دلیل و زمان append-only ثبت شوند. | history overwrite نمی‌شود؛ دسترسی role محدود. |
| C-02 | دادهٔ خام JP7، site، واحد، ابزار، protocol، assessor و کیفیت از derived metric جدا ثبت شود. | تا حل `calf`/`midaxillary` و تصویب معادله/جمعیت، درصد فعال/ادعا نمی‌شود. |
| C-03 | اندازه‌های بدنی/عکس در site، واحد، protocol، رضایت و retention روشن تفکیک شوند. | عکس بدن در release scope فعلی وارد نمی‌شود؛ D-06. |
| C-04 | rubric مهارت ۱۴گانه با نقش ارزیاب و روش test نسخه‌دار شود. | نگاشت به ۱۳ محور موجود تا بازبینی معنایی انجام نمی‌شود. |
| C-05 | red flag و نتیجهٔ بررسی به stop/review/referral قابل‌مشاهده ختم شود. | هیچ «ایمن از نظر پزشکی» یا auto-clear. |
| C-06 | injury restriction با منبع، سمت/ناحیه، دامنه، تاریخ/انقضا و reviewer ثبت شود. | فاز توان‌بخشی/تشخیص ایجاد نمی‌شود. |
| C-07 | referral، مسئول پیگیری و وضعیت unresolved ثبت شود؛ unresolved مانع مسیر وابسته بماند. | ارجاع به‌عنوان clear تلقی نمی‌شود. |
| C-08 | performance test با protocol، واحد، شرایط، assessor و مقایسه‌پذیری ثبت شود. | آزمون بی‌روش score تصمیم‌ساز نمی‌شود. |
| C-09 | اولویت هدف، rule/metric، بازهٔ بازآزمایی و rationale نسخه‌دار شود. | آستانهٔ علمی از repo یا مدل حدس زده نمی‌شود. |
| C-10 | override حرکت/دوز/ترتیب و دلیل مربی در نسخهٔ draft ثبت و قابل‌مقایسه شود. | override خاموش/بدون actor قابل‌انتشار نیست. |
| C-11 | approve/reject/review مربی، actor، زمان و نسخهٔ دقیق را ثبت کند. | approve draft شناسهٔ ProgramVersion immutable می‌سازد؛ merge نرم‌افزاری جای امضای مربی نیست. |

## ۶. میکرولوپ‌های Source Registry و Exercise Catalog

### ۶.۱ خود رجیستری

| ID | میکرولوپ | AC | NG / dependency |
|---|---|---|---|
| SRC-00 | schema و قرارداد رجیستری منبع | هر منبع `source_id`, نوع (dataset/library/API/knowledge/renderer), connector, version/commit/snapshot, SHA-256, schema, acquired_at, license evidence, attribution, quality, retention و review status داشته باشد. | هیچ منبعی صرفاً به‌دلیل public بودن مجاز یا ingest نمی‌شود. |
| SRC-01 | adapter/sandbox قرارداد | connectorهای موردتصویب در sandbox، با ورودی/خروجی نسخه‌دار، timeout، egress و خطای safe آزموده شوند. | سرویس external به production data وصل نمی‌شود؛ import خودکار قبل از license gate مجاز نیست. |
| SRC-02 | canonical mapping حرکات | alias و external ID به canonical ID با provenance و review state map شوند؛ اختلاف منابع قابل‌ردگیری بماند. | نام مشابه، permission to merge یا contraindication محسوب نمی‌شود. |
| SRC-03 | lifecycle وضعیت catalog/asset | `candidate → review → approved → deprecated` و حق جداگانهٔ text/image/GIF روشن و test شود. | asset دارای حق نامشخص به UI/PDF نمی‌رود. |

### ۶.۲ یک issue مستقل برای هر `source_id`

هر `SRC-<ID>` پایین باید **issue جدا** باشد، نه یک ticket بزرگ برای ingest کل اینترنت. AC مشترک: نوع واقعی منبع تأیید شود؛ code/data/media license مستقل بررسی شود؛ نسخه یا snapshot و hash pin شود؛ schema/کیفیت/محدودیت جمعیت ثبت شود؛ owner/مجوز/privacy review انجام شود؛ disposition یکی از `approved-for-evaluation / hold / reject` باشد. NG مشترک: **هیچ download، ingest، runtime call یا انتشار asset پیش از تصمیم/مجوز صریح نیست.**

| خانوادهٔ کارت‌ها | source_idهای مستقل که باید جداگانه بررسی شوند |
|---|---|
| کاتالوگ/نمایش حرکت | `EX01`, `EX02`, `EX03`, `EX04`, `EX05`, `WGER-EX`, `WGER-APP`, `EX09`, `EX10`, `AN01`, `VIS01`, `VIS02` |
| بیومکانیک/توان‌بخشی | `BIO01`, `BIO02`, `BIO03`, `BIO04`, `BIO05`, `BIO06-CODE`, `BIO06-DATA`, `BIO07`, `BIO08`, `BIO09-A`, `BIO09-B`, `BIO10`, `BIO11` |
| بار/عملکرد | `TL01`, `TL02-GC`, `TL02-SWEAT`, `TL02-OPEN`, `TL03-WHIPPR`, `TL03-LACTATER`, `TL04`, `TL05`, `TL06`, `TL07-COMP`, `TL07-TRAINCALC`, `TL07-OFFICIAL`, `TL08-GH`, `TL08-GL` |
| دانش/آموزش | `EDU01`, `EDU02`, `EDU03-PHYS`, `EDU03-REHAB`, `EDU03-SPORTS` |
| تغذیه و نشر | `NUT01`, `NUT-GAP`, `PDF01-GH`, `PDF01-PYPI`, `PDF02` |

این فهرست در مجموع ۴۹ source record/issue slot دارد. `NUT-GAP` یک کار «انتخاب یا ثبت منبع تغذیهٔ ناموجود» است، نه مجوز fallback به MET یا منبع نامرتبط. دو آیتم از یک پروژه با license متفاوت همچنان issue/record مستقل‌اند. پس از تصمیم، connector یا importer جدا و کوچک می‌شود.

## ۷. زنجیرهٔ آیندهٔ ProgramComposer → ProgramVersion → PDF/QR → چرخهٔ بعد

تمام کارت‌های این بخش `TARGET` هستند و به تصمیم مالک، منبع مجاز، قرارداد داده و safety review وابسته‌اند. وابستگی ترتیبی، عمداً اجازه نمی‌دهد QR/PDF پیش از canonical version ساخته شود.

| ID | میکرولوپ | AC | NG / وابستگی |
|---|---|---|---|
| P-01 | `AnswerEnvelope` و snapshot نسخه‌دار | پاسخ به `question_id/source_id/source_version/record/schema/time/transform/confidence/license/evidence` متصل شود؛ unknown/stale/conflict جدا بماند. | مقدار پیش‌فرض یا دادهٔ عمومی جای پاسخ فردی را نمی‌گیرد. |
| P-02 | Question Router | هر Q/C به منبع مجاز و دامنهٔ داده map شود؛ missing/unauthorized source به hold ختم شود. | sourceهای مختلف کورکورانه join یا merge نمی‌شوند. |
| P-03 | ورودی‌های موردنیاز ProgramComposer | snapshot رضایت‌مند/تأییدشده، goal، availability، logs، equipment، safety و source version با completeness check خوانده شود. | Agent یا model data شخصی را برای planning code نخواند. |
| P-04 | hard constraints و safety gate پیش از انتخاب | population/red flag/unknown/restriction/equipment-invalid قبل از ranker اعمال و نتیجهٔ stop/review قابل‌آزمون باشد. | hard constraint با score نرم جبران نمی‌شود؛ تشخیص/clearance تولید نمی‌شود. |
| P-05 | soft goals و ترجیحات | goal، اولویت، علاقه، تنوع و زمان فقط بین candidateهای hard-valid وزن‌دهی و reason ثبت شود. | preference نرم موجب نقض قید سخت نیست. |
| P-06 | deterministic rule-set | الگوریتم/فرمول، input, population, limits و rule version تست و pin شوند. | LLM عدد لود، دوز، منع یا threshold را اختراع نمی‌کند؛ rule علمی بدون متخصص فعال نمی‌شود. |
| P-07 | ساختار block/week/session | خروجی به ساختار canonical و معیارهای زمان، روز، recovery، duplicates و volume که owner/domain expert تصویب کرده وصل شود. | عددهای تمرینی/پیشرفت عمومی بدون scope/evidence وارد نمی‌شوند. |
| P-08 | selection/omission rationale | هر حرکت انتخاب/حذف‌شده، alternative و دلیل، source/catalog ID و rule trace داشته باشد. | score بی‌توضیح یا catalog ID خام به برنامهٔ نهایی نمی‌رود. |
| P-09 | اعتبارسنجی نهایی draft | سازگاری تعداد روز، مدت، equipment، skill، استراحت، قید و completeness با testهای ثابت بررسی شود؛ هیچ candidate معتبر → stop/review. | fallback ثابت برای همه و تبدیل `unknown` به safe ممنوع. |
| P-10 | coach review/override | Studio پیش‌نویس، assumption، evidence و تغییرات را نشان دهد؛ override دلیل و actor داشته باشد. | ساخت draft مجوز نمایش/اجرا برای ورزشکار نیست. |
| P-11 | lifecycle و approval | `draft → coach_review → approved → published → superseded/archived` با state transition و نقش معتبر آزموده شود. | transition یا publish با UI-only gate انجام نمی‌شود. |
| P-12 | immutable ProgramVersion | snapshot, rules/catalog version, member/cycle scope, JSON schema و content hash در نسخهٔ تغییرناپذیر pin شوند. | plan قبلی overwrite نمی‌شود؛ hash جای permission نیست. |
| P-13 | API و صفحهٔ مصرف‌کنندهٔ نسخه | اپ و Studio همان version ID را نمایش/خواندن کنند؛ وضعیت، نام حرکت و دسترسی owner آزموده شود. | یک برنامهٔ جدا در client/PDF دوباره محاسبه نمی‌شود. |
| P-14 | PDF از canonical version | renderer/template/font version و content hash ثبت شود؛ فارسی/RTL، صفحه‌بندی، چاپ و visual regression آزموده شود. | OCR روی PDF داخلی، دادهٔ جدید یا rule اجرای برنامه تولید نمی‌کند. |
| P-15 | حریم و دسترسی PDF | فایل private، owner/scope-checked، retention/deletion/auditدار و با اطلاعات حداقلی باشد. | URL عمومی یا PII/health غیرضروری چاپ نمی‌شود؛ D-06 لازم است. |
| P-16 | QR نسخهٔ برنامه | QR فقط opaque, revocable reference باشد؛ پس از login/owner check دقیقاً version/PDF pin‌شده resolve شود. expiry, revoke, replay و دسترسی غیرمجاز تست شوند. | QR برنامه با QR حضور باشگاه یکی نیست؛ دادهٔ حساس داخل QR نیست. |
| P-17 | import برنامهٔ بیرونی | فایل اصلی hash شود؛ extraction/OCR فقط candidate با page/bbox/confidence بسازد؛ مربی/عضو تأیید کند. | PDF بیرونی دستور قابل‌اجرا یا source-of-truth نیست؛ set/load/progression حدس نمی‌زنیم. |
| P-18 | planned vs performed | ست/تکرار/effort/missed reason به version/session مشخص متصل و persistence/retry بررسی شود. | برنامهٔ برنامه‌ریزی‌شده با اجرای واقعی یکی نمی‌شود. |
| P-19 | مقایسه و scorecard هر جزء | فقط سنجهٔ معتبر و قابل‌مقایسه با protocol/version/تاریخ trend بسازد؛ عدم مقایسه‌پذیری صریح بماند. | همبستگی/score به علت تمرین یا رشد موضعی تعمیم داده نمی‌شود. |
| P-20 | چرخهٔ بعدی و version n+1 | دادهٔ جدید و log واقعی برای draft بعدی استفاده شود؛ مربی تغییر/حفظ حرکت و ساختار را بررسی کند. | نسخهٔ قبلی تغییر نمی‌کند و بازتولید خودکارِ برنامه بدون approval نداریم. |
| P-21 | ماژول جداگانهٔ تغذیه/MealItem | در صورت منبع/مجوز/کیفیت/صلاحیت کافی، target، MealItem و FoodLog جدا به نسخه وصل شوند؛ نبود منبع `not configured` بماند. | exercise planner به‌تنهایی meal plan/medical nutrition ایجاد نمی‌کند. |

## ۸. میکرولوپ‌های AI factory، CI و عملیات انتشار

این‌ها اجرای ابزار Finn-loop نیستند؛ قطعات زیرساخت/سیاستی هستند که لازم‌اند تا ۹ گیت برای هر microtask قابل‌اعتماد شود. پذیرش هر مورد به تصمیم‌ها و baseline مربوط وابسته است.

| ID | میکرولوپ | AC و evidence خروج | NG / وابستگی |
|---|---|---|---|
| A-01 | انتخاب queue و منبع حقیقت task | tracker، statusها، blocked-by، claim و owner مشخص شوند؛ Linear فقط در صورت تصمیم/اتصال مصوب. | issue واقعی در tracker ساخته نمی‌شود تا مالک workflow را تأیید کند. |
| A-02 | sandbox عامل | اجرای rootless/least-privilege، scratch repo/worktree، no production secret، egress policy و cleanup امن در POC تست شود. | worktree به‌تنهایی sandbox یا مجوز shell نیست. |
| A-03 | command/path policy | read/write path، command class، destructive operation، dependency install و prompt injection با allow/deny و audit آزموده شوند. | agent policy متن prompt تنها کنترل امنیتی نماند. |
| A-04 | branch protection و checkهای اجباری | default branch، PR requirement، reviewer, required tests و bypass policy با config خوانده و در PR آزمایشی verify شوند. | Finn یا agent مجاز به تغییر rules/merge نیست. |
| A-05 | CI واقعی پروژه | backend, Studio, Flutter, docs, security, dependency/image checks با commandهای تأییدشده روی همان SHA اجرا شوند؛ required status mapping روشن شود. | workflow خود Finn یا check یک لایه به‌جای تست target app پذیرفته نمی‌شود. |
| A-06 | evidence bundle و provenance | issue, patch/SHA, tool/model version, command result, scan, reviewer و attestation policy با redaction ثبت شوند. | ادعای in-toto/signed provenance بدون تولید/verify امضا نمی‌شود. |
| A-07 | سقف budget و kill switch | wall-clock, retries, model calls/tokens/cost, command count و stop action از config قابل‌ممیزی اعمال شوند. | retry limit فعلی در اسناد فقط پیشنهاد است؛ رقم/مرز جدید بدون مالک فرض نمی‌شود. |
| A-08 | red-team هارنس عامل | fixtureهای prompt injection, hostile issue/comment, secret request, scope escalation, egress attempt و bypass testing به نتیجهٔ قابل‌تکرار متصل شوند. | مرور عادیِ builder جای ارزیابی خصمانهٔ مستقل نیست. |
| A-09 | reviewer مستقل و convergence | reviewer با context مستقل head دقیق را ببیند؛ fix/review فقط تا سقف retry مصوب؛ پس از سقف `needs-human` شود. | self-review یا retry نامحدود نداریم؛ قابلیت‌های roadmap Finn موجود فرض نمی‌شوند. |
| O-01 | DB و transaction baseline | SQLite concurrency/locking, migration trigger, idempotency و backup نیازسنجی و در scratch تست شود؛ معیار SQLite/PG به مالک ارائه شود. | migration یا انتخاب PG صرفاً از پیش‌نویس انجام نمی‌شود. |
| O-02 | فایل خصوصی و retention | مسیر storage، auth/scope، upload limits, malware/content handling, backup/delete/retention و آزمون منفی مستند شود. | فایل private یا دادهٔ کاربر به static/public دسترسی نمی‌گیرد. |
| O-03 | scheduler/outbox runtime | startup, single-active worker/lease, retry cap, idempotency, dead-letter, health/alert و recovery در محیط غیرتولیدی اثبات شود. | تعریف class/job در source به runtime فعال تعبیر نمی‌شود. |
| O-04 | topology، TLS و proxy | بعد از D-02، Compose source-of-truth, ingress, CORS, DNS/TLS, health path و secret delivery در staging verify شود. | هیچ host/cloud/tunnel یا production deploy بی‌اجازه ساخته نمی‌شود. |
| O-05 | backup و restore | backup خارج میزبان، retention/encryption، restore روی میزبان جدا، زمان/دادهٔ بازیابی و هشدار با evidence ثبت شود. | وجود scheduler/Restic config به معنی backup/restore واقعی نیست. |
| O-06 | سرویس پیامک/notification خارجی | provider، secrets، cost/rate limit, delivery retry و privacy با fixture و opt-in staging تست شود. | SMS `dev` به ارسال واقعی تعبیر نمی‌شود؛ push خارجی خودکار فعال نیست. |
| O-07 | source بانکی و تطبیق | فقط پس از D-05 مشخص شود دستی می‌ماند یا integration لازم است؛ verification/settlement, fraud/replay و audit تعریف شود. | کارت‌به‌کارت/فیش را به gateway live تبدیل نمی‌کند. |
| O-08 | observability و incident | metrics/alerts از host مستقل، redaction، owner، runbook، kill switch و incident response تست شوند. | health endpoint تنها probe مستقل یا SLO نیست. |
| O-09 | supply chain/artifact | pinning, dependency/image scan, SBOM, digest, signing/verification و promotion مسیر مصوب در CI/staging اجرا شود. | tag تنها immutable provenance نیست؛ Trivy/Syft/Cosign تا بررسی مجوز/نسخه نصب نمی‌شوند. |
| O-10 | device/browser/E2E | Android/Flutter، Studio browser، QR hardware, RTL, network interruption و roles در staging با دادهٔ مصنوعی آزموده شوند. | TestClient یا visual mock جای دستگاه/شبکه را نمی‌گیرد. |
| O-11 | Go/No-Go و release | وضعیت هر جریان، unresolved `UNKNOWN`, severity/exception owner, backup/rollback, digest, support و امضای تصمیم release در checklist جمع شود. | گیت باز `NO-GO` است؛ این سند مجوز release نیست. |
| O-12 | post-release learning | defect/reopen/revert, test gaps, retry/cost و service outcome به پیشنهاد rule نسخه‌دار تبدیل و فقط با merge انسانی policy شود. | عامل policy/instructions خودش را بی‌صدا تغییر نمی‌دهد. |

## ۹. Traceability کامل از گره‌های فلوچارت به کارت‌ها

این جدول تضمین می‌کند هیچ بخش عملکردی از نمودار اصلی هنگام تبدیل به issue ناپدید نشده باشد. nodeهای legend خودشان قابلیت محصول نیستند؛ زبان وضعیت evidence را تعریف می‌کنند.

| cluster نمودار | node IDهای منبع | کارت‌های مرتبط |
|---|---|---|
| بازیگران | `member`, `staff`, `kiosk_operator` | D-01/D-03/D-10؛ F-04…F-10؛ F-22…F-24 |
| کلاینت‌ها | `client_app`, `studio_app`, `kiosk_ui` | D-01؛ F-09/F-10؛ F-24؛ O-10 |
| UI عضو | `ux_member_auth`, `ux_member_training`, `ux_member_health`, `ux_member_attendance`, `ux_member_money` | F-04…F-09, F-11…F-32؛ Q-01…Q-11 |
| UI کارکنان | `ux_staff_ops`, `ux_staff_program`, `ux_staff_finance`, `ux_staff_admin` | F-10, F-15, F-18, F-20, F-24…F-37 |
| تعامل مشترک | `ui_contract`, `api_client`, `ingress`, `session_gate`, `authz_gate`, `deny_path`, `response_rules` | F-01…F-08؛ A-04/A-05 |
| خانوادهٔ route | `route_identity`, `route_training`, `route_assessment`, `route_attendance`, `route_nutrition`, `route_finance`, `route_comms` | B-02/B-03؛ F-04…F-36 و trace mapping کاتالوگ |
| service | `svc_identity`, `svc_training`, `svc_assessment`, `svc_attendance`, `svc_nutrition`, `svc_finance`, `svc_comms` | F-04…F-36؛ TARGET-P-01…P-21 |
| مدل داده | `data_identity`, `data_training`, `data_assessment`, `data_attendance`, `data_nutrition`, `data_finance`, `data_comms` | F-04…F-35؛ Q/Cها؛ P-01…P-21 |
| storage/runtime | `sqlite_store`, `private_store`, `runtime_jobs` | F-25/F-28/F-33؛ O-01/O-02/O-03/O-05 |
| integrations/ops | `sms`, `bank`, `ai_optional`, `operations` | D-02/D-05/D-08؛ O-04/O-06/O-07/O-08؛ A-02/A-07 |
| تصمیم‌های باز | `confirmed_platform`, `pwa_target`, `role_target`, `privacy_decision` | D-01…D-10؛ B-06 |
| زنجیرهٔ آیندهٔ برنامه | `q_forms`, `source_gate`, `composer`, `versioned_program`, `private_pdf_qr`, `cycle_metrics` | Q-01…Q-11؛ C-01…C-11؛ SRC-*؛ P-01…P-21 |
| راهنمای شواهد | `legend_current`, `legend_conditional`, `legend_gap`, `legend_target` | B-01/B-05؛ واژگان وضعیت این سند؛ issue تولیدی مستقل نیستند. |
| پیوندهای شواهد | `route_catalog`, `references` | B-02/B-03؛ مسیر/فایل‌های مرجع زیر. |

### ۹.۱ پوشش API — تمام ۱۶۳ operation در scope traceability

کاتالوگ operation به‌عنوان مرجع ردیف‌به‌ردیف در B-02 استفاده می‌شود. این‌ها تعداد operation هر حوزه در snapshot منبع‌اند؛ **به معنی ۱۶۳ پیاده‌سازی تازه یا ۱۶۳ PR نیستند**. اگر ممیزی یک defect مستقل پیدا کند، برای آن micro-fix جدا می‌سازیم.

| حوزهٔ کاتالوگ | شمارش | issue-family که باید هر operation را trace کند |
|---|---:|---|
| هویت، پروفایل، عضویت | 23 | F-04…F-08 + B-02 |
| Intake، برنامه، تمرین، کتابخانه | 15 | F-11…F-16 + B-02 |
| ارزیابی و سنجش | 10 | F-17…F-19 + B-02 |
| کلاس، QR و حضور | 12 | F-22…F-24 + B-02 |
| تغذیه، غذا و وزن | 9 | F-20/F-21 + TARGET Q/C/P + B-02 |
| مالی، پرداخت، هزینه، فروشگاه | 52 | F-25…F-30 + B-02 |
| گفت‌وگو، اعلان، مدیریت و عملیات | 42 | F-31…F-36 + O-03/O-08 + B-02 |

هر mapping حداقل `method + path template + operationId + actor + guards/scopes + consumer + test/evidence + status` دارد. guardهای metadata به‌تنهایی مجوز مؤثر تلقی نمی‌شوند؛ service ownership و تست منفی هم لازم است.

### ۹.۲ پوشش اسناد جزئی

- API: `session-decisions-2026-11-23/API-ROUTE-CATALOG.md` و `mp-app/backend/api/routes.json`.
- UI/Studio/Flutter: `WIRING-LEDGER.md`, `interaction-map.json`, `frontend-ui-ux-*-option-03-*` و فایل‌های مسیر اپ.
- پرداخت/کلاس/refund: `transaction-findings-flow-v1-2026-11-23.dot` و بخش‌های finance/class در WIRING-LEDGER.
- Intake/حرکت/برنامه: `training-intake-decision-tree-2026-11-23.md`, `training-program-builder-design-2026-11-23.md`.
- lifecycle، ارزیابی، PDF و QR: `athlete-program-lifecycle-v2-2026-11-23.md`, `athlete-jp7-program-qr-v6-2026-11-23.md` و flowهای v2/v3/v6.
- منابع مجاز: `open-source-question-routing-and-layered-data-architecture-v1-2026-11-23.md`.
- تولید و عملیات: `ai-autonomous-production-plan-v1-2026-11-23.md`؛ G0–G10 در آن phaseهای macro هستند، نه issueهای آماده.

## ۱۰. ترتیب پیشنهادی، blockers و اولین پایلوت

1. **تصمیم/آمادگی، نه کدنویسی:** D-01…D-11 و B-01…B-07؛ اگر scope یا evidence مبهم است، کارت بعدی `BLOCKED` بماند.
2. **امنیت ابزار ساخت:** A-01…A-08 و branch/CI/provenance/budget، ابتدا روی fixture مصنوعی و فقط در صورت تصمیم به استفاده از عامل.
3. **اولین Finn-style pilot:** یک کار کم‌ریسک مستنداتی/تستی، یک issue و یک PR؛ تمام ۹ حوزه با evidence ثبت شود. فعلاً خود L10 safety، پرداخت، permission migration، migration DB، انتشار و دادهٔ سلامت پایلوت مناسب نیستند.
4. **جریان‌های فعلی:** F-01…F-37 را بر اساس dependency و risk به vertical sliceهای کوچک اجرا کن؛ نتیجهٔ کدخوانی/آزمون قدیمی به‌جای evidence revision جدید قبول نشود.
5. **طرح آیندهٔ ورزشکار/برنامه:** Q/C و SRC فقط پس از تصمیم privacy/domain/license؛ سپس P-01 به‌ترتیب تا P-21.
6. **staging/release:** O-01…O-11 پس از تصمیم توپولوژی، وجود مسئول، backup/restore و required checks. release فقط با همهٔ گیت‌ها PASS و تأیید مالک.
7. **چرخهٔ یادگیری:** O-12 پس از چند issue ادغام‌شده و شواهد واقعی review؛ پیشنهاد policy فقط PR برای تأیید انسانی.

### وابستگی‌های اصلی

```text
D-01…D-11
  → B-01…B-07
  → A-01…A-09 / CI & branch policy
  → F-01…F-37 current flows
  → Q-01…Q-11 + C-01…C-11 (پس از data/privacy/clinical approval)
  → SRC-00…SRC-<49 IDs> (هر source جدا؛ فقط منابع تصویب‌شده)
  → P-01…P-21 program lifecycle
  → O-01…O-11 staging/recovery/release
  → O-12 learning loop
```

این ترتیب جای dependency ریز هر issue را نمی‌گیرد؛ مثلاً QR نسخهٔ برنامه تا `P-12` ProgramVersion و `P-15` access/privacy تکمیل نشده، `BLOCKED` است. PWA تا D-01، نقش target تا D-03، online payment تا D-05، تصویر بدن تا D-06، Postgres تا D-07 و external inference تا D-08 اجرا نمی‌شود.

## ۱۱. Issue نمونهٔ Finn-loop برای نشان‌دادن اندازه

**نمونهٔ نمایشی؛ `AGENT-READY` نیست:**

```text
ID: F-12 (بعد از baseline و تأیید دامنه)
Problem: وضعیت حل‌نشدهٔ safety ممکن است به draft قابل‌مشاهده برای عضو برسد.
AC-1: با fixture وضعیت blocked/needs_review/unknown طبق enum تأییدشده، API هیچ برنامهٔ اجرایی عضو برنگرداند/منتشر نکند.
AC-2: پاسخ صریحِ review-required در UI/API قابل‌فهم باشد و مسیر مربی قابل‌ردگیری بماند.
AC-3: مسیر مجاز، roleهای نامجاز و حالت عدم‌دسترسی در تست service/API/UI پوشش داده شود.
AC-4: evidence به head SHA، آزمون‌ها و نقش‌های استفاده‌شده متصل باشد.
NG-1: هیچ diagnosis، clearance یا contraindication جدیدی ساخته نشود.
NG-2: هیچ health data واقعی، migration، PDF انتشار، external model یا live service وارد نشود.
Dependencies: D-03, D-06, D-11, B-01, B-02, B-07.
Tests: unit + API/permission regression + existing relevant CI; device E2E در کارت جدا.
Human: owner contract approval + qualified domain review + human merge.
Gates: هر ۹ حوزه از Section 1.2 با PASS/BLOCKED و evidence مجزا ثبت شوند.
```

این نمونه ادعای وضعیت production نیست. WIRING-LEDGER گپ را در snapshot فعلی گزارش کرده، اما مسئلهٔ اجرایی تا بازبینی source/contract و آزمون همان revision، آمادهٔ عامل نیست.

## ۱۲. شرط ورود به Linear/Finn-loop واقعی

Finn-loop پروژهٔ اصلی، مهارت‌های Claude Code را با Linear و GitHub CLI به کار می‌گیرد؛ اجرای واقعی به نسخهٔ سازگار Claude Code، connector Linear، team/labels/states و `gh` احرازشده نیاز دارد و CI هدف را خودش نمی‌سازد. بنابراین این فایل را می‌توان بعداً به issueها تبدیل کرد، اما فعلاً هیچ issue خارجی ایجاد نشده است. برای هر کارت تنها پس از owner approval، tracker setup و پاک‌سازی امن مرز worktree، یک متن Finn-style شامل AC/NG/verification و ۹ حوزه ساخته می‌شود.

قانون merge این طرح در تمام مراحل **human merge** است. هیچ کارت اجازهٔ خودکار برای تغییر Branch Protection، merge، release، deploy، دسترسی به secret، inference بیرونی یا استفاده از دادهٔ واقعی صادر نمی‌کند.


## ۱۳. خردکردن مسیرهای پرحجم و نگاشت ردیف‌به‌ردیف API

برای اینکه issueهای بزرگِ حوزهٔ مالی/عضویت به یک PR چنددامنه‌ای تبدیل نشوند، کارت‌های parent زیر به برش‌های اجرایی کوچک‌تر تقسیم می‌شوند. parent فقط برای grouping است؛ **برش‌های پسونددار** واحدهای پیشنهادی issue/PR هستند و هرکدام هر ۹ gate را جدا می‌گذراند.

| کارت parent | برش‌های microtask | شرط کوچک‌بودن/وابستگی |
|---|---|---|
| F-07 | `F-07A` پروفایل self و تاریخچه؛ `F-07B` directory/create/update عضو و scope؛ `F-07C` plan/membership/invoice | تست owner-scope و نقش برای هر برش جدا؛ role decision D-03 blocker است. |
| F-25 | `F-25A` payment list/create/start/invoice؛ `F-25B` upload/read فیش خصوصی؛ `F-25C` approve/reject/verify/fail/callback/return و state transition | gateway path فقط با D-05؛ کارت receipt با data/privacy gate جدا. |
| F-26 | `F-26A` wallet balance/transactions/charge/pay؛ `F-26B` coupon و ledger/reverse | هر write با transaction/idempotency/audit خودش؛ تست concurrency جدا. |
| F-28 | `F-28A` expense CRUD/revision/grant؛ `F-28B` upload/read رسید خصوصی | receipt/data-retention و finance grants، دو شاهد جدا. |
| F-30 | `F-30A` product/category/price/status read؛ `F-30B` cart/order/checkout fail-closed؛ `F-30C` staff product/price/gateway/change-request | عضو checkout تا D-05 خاموش؛ super_admin review با D-03. |
| F-34 | `F-34A` analytics/KPI/member summary؛ `F-34B` attendance/check-in ops view؛ `F-34C` confidential report access | confidential grant و leakage test از chart presentation جدا. |
| F-35 | `F-35A` permission/user/role grants؛ `F-35B` feature flags؛ `F-35C` retention؛ `F-35D` audit | هیچ تغییر grant/retention بدون D-03/D-06 و تأیید مالک اجرا نمی‌شود. |

جدول زیر از همان snapshot `routes.json` ساخته شده است. برای **هر operation** یک issue-family مشخص شده تا چیزی از flowchart/route catalog جا نماند؛ این mapping به معنی اصلاح، پوشش تست یا قبولی دسترسی نیست. source of truth برای guard/role/operation ID، API-ROUTE-CATALOG و `routes.json` است.

| Method | Path template | operationId | Issue-family |
|---|---|---|---|
| GET | `/api/v1/admin/analytics/churn-risk` | `_churn_risk_api_v1_admin_analytics_churn_risk_get` | `F-34A` |
| GET | `/api/v1/admin/analytics/leaderboards` | `_leaderboards_api_v1_admin_analytics_leaderboards_get` | `F-34A` |
| GET | `/api/v1/admin/attendance` | `attendance_api_v1_admin_attendance_get` | `F-34B` |
| GET | `/api/v1/admin/audit` | `list_audit_api_v1_admin_audit_get` | `F-35D` |
| GET | `/api/v1/admin/checkins` | `checkins_api_v1_admin_checkins_get` | `F-34B` |
| GET | `/api/v1/admin/flags` | `list_flags_api_v1_admin_flags_get` | `F-35B` |
| PUT | `/api/v1/admin/flags` | `set_flag_api_v1_admin_flags_put` | `F-35B` |
| GET | `/api/v1/admin/flags/{key}` | `get_flag_api_v1_admin_flags__key__get` | `F-35B` |
| GET | `/api/v1/admin/kpis` | `_kpis_api_v1_admin_kpis_get` | `F-34A` |
| GET | `/api/v1/admin/members-summary` | `members_summary_api_v1_admin_members_summary_get` | `F-34A` |
| GET | `/api/v1/admin/permissions` | `permissions_list_api_v1_admin_permissions_get` | `F-35A` |
| POST | `/api/v1/admin/permissions` | `permissions_grant_api_v1_admin_permissions_post` | `F-35A` |
| GET | `/api/v1/admin/permissions/known` | `permissions_known_api_v1_admin_permissions_known_get` | `F-35A` |
| DELETE | `/api/v1/admin/permissions/{grant_id}` | `permissions_revoke_api_v1_admin_permissions__grant_id__delete` | `F-35A` |
| GET | `/api/v1/admin/retention` | `preview_api_v1_admin_retention_get` | `F-35C` |
| POST | `/api/v1/admin/retention/run` | `run_api_v1_admin_retention_run_post` | `F-35C` |
| GET | `/api/v1/admin/users` | `users_list_api_v1_admin_users_get` | `F-35A` |
| DELETE | `/api/v1/admin/users/{user_id}/role` | `revoke_role_api_v1_admin_users__user_id__role_delete` | `F-35A` |
| POST | `/api/v1/admin/users/{user_id}/role` | `grant_role_api_v1_admin_users__user_id__role_post` | `F-35A` |
| POST | `/api/v1/ai/nutrition/generate` | `generate_nutrition_api_v1_ai_nutrition_generate_post` | `F-20` |
| POST | `/api/v1/ai/program/generate` | `generate_program_api_v1_ai_program_generate_post` | `F-12` |
| POST | `/api/v1/ai/suggest-weight` | `suggest_weight_api_v1_ai_suggest_weight_post` | `F-18` |
| POST | `/api/v1/assessments` | `create_assessment_api_v1_assessments_post` | `F-18` |
| POST | `/api/v1/assessments/jp7` | `record_jp7_api_v1_assessments_jp7_post` | `F-17` |
| GET | `/api/v1/assessments/jp7/member/{member_id}/trend` | `jp7_trend_api_v1_assessments_jp7_member__member_id__trend_get` | `F-17` |
| POST | `/api/v1/assessments/limb` | `record_limb_api_v1_assessments_limb_post` | `F-19` |
| GET | `/api/v1/assessments/limb/member/{member_id}/report` | `segmental_report_api_v1_assessments_limb_member__member_id__report_get` | `F-19` |
| GET | `/api/v1/assessments/member/{member_id}` | `list_member_assessments_api_v1_assessments_member__member_id__get` | `F-18` |
| GET | `/api/v1/assessments/{assessment_id}` | `get_assessment_api_v1_assessments__assessment_id__get` | `F-18` |
| POST | `/api/v1/auth/logout` | `logout_api_v1_auth_logout_post` | `F-05` |
| POST | `/api/v1/auth/logout-all` | `logout_all_api_v1_auth_logout_all_post` | `F-05` |
| POST | `/api/v1/auth/otp/request` | `otp_request_api_v1_auth_otp_request_post` | `F-04` |
| POST | `/api/v1/auth/otp/verify` | `otp_verify_api_v1_auth_otp_verify_post` | `F-04` |
| POST | `/api/v1/auth/phone-change/confirm` | `phone_change_confirm_api_v1_auth_phone_change_confirm_post` | `F-06` |
| POST | `/api/v1/auth/phone-change/request` | `phone_change_request_api_v1_auth_phone_change_request_post` | `F-06` |
| POST | `/api/v1/auth/phone-change/verify-old` | `phone_change_verify_old_api_v1_auth_phone_change_verify_old_post` | `F-06` |
| POST | `/api/v1/auth/refresh` | `refresh_api_v1_auth_refresh_post` | `F-05` |
| GET | `/api/v1/auth/sessions` | `sessions_api_v1_auth_sessions_get` | `F-05` |
| DELETE | `/api/v1/auth/sessions/{session_id}` | `revoke_session_api_v1_auth_sessions__session_id__delete` | `F-05` |
| POST | `/api/v1/axis-assessments` | `create_assessment_api_v1_axis_assessments_post` | `F-18` |
| GET | `/api/v1/axis-assessments/member/{member_id}` | `list_member_history_api_v1_axis_assessments_member__member_id__get` | `F-18` |
| GET | `/api/v1/axis-assessments/{assessment_id}/matrix` | `get_matrix_api_v1_axis_assessments__assessment_id__matrix_get` | `F-18` |
| POST | `/api/v1/axis-assessments/{assessment_id}/review` | `review_assessment_api_v1_axis_assessments__assessment_id__review_post` | `F-18` |
| GET | `/api/v1/chat/conversations` | `list_conversations_api_v1_chat_conversations_get` | `F-31` |
| POST | `/api/v1/chat/conversations` | `open_conversation_api_v1_chat_conversations_post` | `F-31` |
| GET | `/api/v1/chat/conversations/{conversation_id}/messages` | `list_messages_api_v1_chat_conversations__conversation_id__messages_get` | `F-31` |
| POST | `/api/v1/chat/conversations/{conversation_id}/messages` | `send_message_api_v1_chat_conversations__conversation_id__messages_post` | `F-31` |
| POST | `/api/v1/chat/conversations/{conversation_id}/read` | `mark_read_api_v1_chat_conversations__conversation_id__read_post` | `F-31` |
| GET | `/api/v1/classes` | `list_classes_api_v1_classes_get` | `F-22` |
| POST | `/api/v1/classes` | `create_class_api_v1_classes_post` | `F-22` |
| POST | `/api/v1/classes/book` | `book_api_v1_classes_book_post` | `F-23` |
| POST | `/api/v1/classes/cancel` | `cancel_api_v1_classes_cancel_post` | `F-23` |
| GET | `/api/v1/expenses` | `list_expenses_api_v1_expenses_get` | `F-28A` |
| POST | `/api/v1/expenses` | `create_expense_api_v1_expenses_post` | `F-28A` |
| DELETE | `/api/v1/expenses/{expense_id}` | `delete_expense_api_v1_expenses__expense_id__delete` | `F-28A` |
| PATCH | `/api/v1/expenses/{expense_id}` | `update_expense_api_v1_expenses__expense_id__patch` | `F-28A` |
| GET | `/api/v1/expenses/{expense_id}/receipt` | `read_expense_receipt_api_v1_expenses__expense_id__receipt_get` | `F-28B` |
| POST | `/api/v1/expenses/{expense_id}/receipt` | `upload_expense_receipt_api_v1_expenses__expense_id__receipt_post` | `F-28B` |
| POST | `/api/v1/face/checkin` | `check_in_api_v1_face_checkin_post` | `F-24` |
| POST | `/api/v1/face/checkin-qr` | `checkin_qr_api_v1_face_checkin_qr_post` | `F-24` |
| POST | `/api/v1/face/checkins/{checkin_id}/exit` | `checkin_exit_api_v1_face_checkins__checkin_id__exit_post` | `F-24` |
| POST | `/api/v1/face/consent` | `grant_consent_api_v1_face_consent_post` | `F-24` |
| POST | `/api/v1/face/consent/revoke` | `revoke_consent_api_v1_face_consent_revoke_post` | `F-24` |
| GET | `/api/v1/face/deep-status` | `deep_status_api_v1_face_deep_status_get` | `F-24` |
| POST | `/api/v1/face/enroll` | `enroll_api_v1_face_enroll_post` | `F-24` |
| DELETE | `/api/v1/face/enroll/{member_id}` | `delete_face_api_v1_face_enroll__member_id__delete` | `F-24` |
| GET | `/api/v1/face/privacy-notice` | `privacy_notice_api_v1_face_privacy_notice_get` | `F-24` |
| GET | `/api/v1/face/qr-token` | `qr_token_api_v1_face_qr_token_get` | `F-24` |
| GET | `/api/v1/finance/reports/daily/{run_date}` | `daily_api_v1_finance_reports_daily__run_date__get` | `F-29` |
| GET | `/api/v1/finance/reports/period` | `period_api_v1_finance_reports_period_get` | `F-29` |
| GET | `/api/v1/finance/reports/schedule` | `schedule_status_api_v1_finance_reports_schedule_get` | `F-29` |
| POST | `/api/v1/finance/reports/schedule/{job_key}/run` | `run_job_api_v1_finance_reports_schedule__job_key__run_post` | `F-29` |
| GET | `/api/v1/health/ready` | `ready_api_v1_health_ready_get` | `F-36` |
| GET | `/api/v1/library/exercises` | `list_exercises_api_v1_library_exercises_get` | `F-14` |
| GET | `/api/v1/library/exercises/{exercise_id}` | `get_exercise_api_v1_library_exercises__exercise_id__get` | `F-14` |
| GET | `/api/v1/members` | `list_members_api_v1_members_get` | `F-07B` |
| POST | `/api/v1/members` | `create_member_api_v1_members_post` | `F-07B` |
| GET | `/api/v1/members/me` | `get_me_api_v1_members_me_get` | `F-07A` |
| PUT | `/api/v1/members/me` | `update_me_api_v1_members_me_put` | `F-07A` |
| GET | `/api/v1/members/me/checkins` | `my_checkins_api_v1_members_me_checkins_get` | `F-24` |
| GET | `/api/v1/members/me/face-consent` | `my_face_consent_api_v1_members_me_face_consent_get` | `F-24` |
| POST | `/api/v1/members/memberships` | `create_membership_api_v1_members_memberships_post` | `F-07C` |
| POST | `/api/v1/members/memberships/from-plan` | `create_from_plan_api_v1_members_memberships_from_plan_post` | `F-07C` |
| GET | `/api/v1/members/memberships/plans` | `list_plans_api_v1_members_memberships_plans_get` | `F-07C` |
| GET | `/api/v1/members/memberships/{membership_id}/invoice` | `get_invoice_api_v1_members_memberships__membership_id__invoice_get` | `F-07C` |
| GET | `/api/v1/members/{member_id}` | `get_member_api_v1_members__member_id__get` | `F-07B` |
| PATCH | `/api/v1/members/{member_id}` | `update_member_api_v1_members__member_id__patch` | `F-07B` |
| GET | `/api/v1/members/{member_id}/memberships` | `member_memberships_api_v1_members__member_id__memberships_get` | `F-07C` |
| GET | `/api/v1/metrics` | `prometheus_metrics_api_v1_metrics_get` | `F-36` |
| POST | `/api/v1/notifications` | `send_api_v1_notifications_post` | `F-32` |
| GET | `/api/v1/notifications/member/{member_id}` | `list_notifications_api_v1_notifications_member__member_id__get` | `F-32` |
| GET | `/api/v1/notifications/reminders/member/{member_id}` | `member_reminders_api_v1_notifications_reminders_member__member_id__get` | `F-32` |
| POST | `/api/v1/notifications/{notification_id}/read` | `mark_read_api_v1_notifications__notification_id__read_post` | `F-32` |
| POST | `/api/v1/nutrition/food-logs` | `log_food_api_v1_nutrition_food_logs_post` | `F-21` |
| GET | `/api/v1/nutrition/food-logs/member/{member_id}/daily` | `daily_summary_api_v1_nutrition_food_logs_member__member_id__daily_get` | `F-21` |
| GET | `/api/v1/nutrition/foods` | `search_foods_api_v1_nutrition_foods_get` | `F-21` |
| GET | `/api/v1/nutrition/member/{member_id}/adaptive` | `adaptive_report_api_v1_nutrition_member__member_id__adaptive_get` | `F-21` |
| POST | `/api/v1/nutrition/plans` | `create_plan_api_v1_nutrition_plans_post` | `F-20` |
| GET | `/api/v1/nutrition/plans/member/{member_id}` | `list_member_plans_api_v1_nutrition_plans_member__member_id__get` | `F-20` |
| POST | `/api/v1/nutrition/plans/{plan_id}/approve` | `approve_plan_api_v1_nutrition_plans__plan_id__approve_post` | `F-20` |
| POST | `/api/v1/nutrition/weight-logs` | `log_weight_api_v1_nutrition_weight_logs_post` | `F-21` |
| GET | `/api/v1/payments` | `list_payments_api_v1_payments_get` | `F-25A` |
| POST | `/api/v1/payments` | `create_payment_api_v1_payments_post` | `F-25A` |
| GET | `/api/v1/payments/coupons` | `list_coupons_api_v1_payments_coupons_get` | `F-26B` |
| POST | `/api/v1/payments/coupons` | `create_coupon_api_v1_payments_coupons_post` | `F-26B` |
| POST | `/api/v1/payments/finance/commission` | `_commission_api_v1_payments_finance_commission_post` | `F-29` |
| GET | `/api/v1/payments/finance/export.csv` | `_finance_csv_api_v1_payments_finance_export_csv_get` | `F-29` |
| GET | `/api/v1/payments/finance/summary` | `_finance_summary_api_v1_payments_finance_summary_get` | `F-29` |
| GET | `/api/v1/payments/invoice/{member_id}` | `invoice_api_v1_payments_invoice__member_id__get` | `F-25A` |
| POST | `/api/v1/payments/ledger/{entry_id}/reverse` | `ledger_reverse_api_v1_payments_ledger__entry_id__reverse_post` | `F-26B` |
| GET | `/api/v1/payments/ledger/{member_id}` | `ledger_list_api_v1_payments_ledger__member_id__get` | `F-26B` |
| POST | `/api/v1/payments/wallet/charge` | `wallet_charge_api_v1_payments_wallet_charge_post` | `F-26A` |
| POST | `/api/v1/payments/wallet/pay` | `wallet_pay_api_v1_payments_wallet_pay_post` | `F-26A` |
| GET | `/api/v1/payments/wallet/{member_id}` | `wallet_balance_api_v1_payments_wallet__member_id__get` | `F-26A` |
| GET | `/api/v1/payments/wallet/{member_id}/transactions` | `wallet_transactions_api_v1_payments_wallet__member_id__transactions_get` | `F-26A` |
| POST | `/api/v1/payments/{payment_id}/approve` | `approve_receipt_api_v1_payments__payment_id__approve_post` | `F-25C` |
| POST | `/api/v1/payments/{payment_id}/callback` | `gateway_callback_api_v1_payments__payment_id__callback_post` | `F-25C` |
| POST | `/api/v1/payments/{payment_id}/fail` | `fail_payment_api_v1_payments__payment_id__fail_post` | `F-25C` |
| GET | `/api/v1/payments/{payment_id}/gateway-return` | `gateway_return_api_v1_payments__payment_id__gateway_return_get` | `F-25C` |
| GET | `/api/v1/payments/{payment_id}/receipt` | `receipt_api_v1_payments__payment_id__receipt_get` | `F-25B` |
| POST | `/api/v1/payments/{payment_id}/receipt` | `upload_receipt_api_v1_payments__payment_id__receipt_post` | `F-25B` |
| POST | `/api/v1/payments/{payment_id}/refund` | `refund_payment_endpoint_api_v1_payments__payment_id__refund_post` | `F-27` |
| POST | `/api/v1/payments/{payment_id}/reject` | `reject_receipt_api_v1_payments__payment_id__reject_post` | `F-25C` |
| POST | `/api/v1/payments/{payment_id}/start` | `start_payment_api_v1_payments__payment_id__start_post` | `F-25A` |
| POST | `/api/v1/payments/{payment_id}/verify` | `verify_payment_api_v1_payments__payment_id__verify_post` | `F-25C` |
| POST | `/api/v1/population/gate-check` | `gate_check_api_v1_population_gate_check_post` | `F-11` |
| POST | `/api/v1/population/intake/next` | `intake_next_api_v1_population_intake_next_post` | `F-11` |
| GET | `/api/v1/population/paths` | `paths_api_v1_population_paths_get` | `F-11` |
| GET | `/api/v1/programs` | `list_programs_api_v1_programs_get` | `F-15` |
| POST | `/api/v1/programs/from-engine` | `create_from_engine_api_v1_programs_from_engine_post` | `F-15` |
| GET | `/api/v1/programs/member/{member_id}` | `list_member_programs_api_v1_programs_member__member_id__get` | `F-15` |
| GET | `/api/v1/programs/member/{member_id}/readiness` | `member_readiness_api_v1_programs_member__member_id__readiness_get` | `F-15` |
| GET | `/api/v1/programs/member/{member_id}/volume` | `member_volume_api_v1_programs_member__member_id__volume_get` | `F-15` |
| POST | `/api/v1/programs/set-feedback` | `set_feedback_api_v1_programs_set_feedback_post` | `F-16` |
| POST | `/api/v1/programs/sync/set-feedback` | `sync_set_feedback_api_v1_programs_sync_set_feedback_post` | `F-16` |
| GET | `/api/v1/programs/{program_id}` | `get_program_api_v1_programs__program_id__get` | `F-15` |
| POST | `/api/v1/programs/{program_id}/approve` | `approve_program_api_v1_programs__program_id__approve_post` | `F-15` |
| POST | `/api/v1/programs/{program_id}/reject` | `reject_program_api_v1_programs__program_id__reject_post` | `F-15` |
| GET | `/api/v1/reports/confidential/{member_id}` | `confidential_report_api_v1_reports_confidential__member_id__get` | `F-34C` |
| GET | `/api/v1/shop/cart` | `cart_api_v1_shop_cart_get` | `F-30B` |
| POST | `/api/v1/shop/cart` | `cart_add_api_v1_shop_cart_post` | `F-30B` |
| DELETE | `/api/v1/shop/cart/{item_id}` | `cart_remove_api_v1_shop_cart__item_id__delete` | `F-30B` |
| PATCH | `/api/v1/shop/cart/{item_id}` | `cart_update_api_v1_shop_cart__item_id__patch` | `F-30B` |
| GET | `/api/v1/shop/categories` | `categories_api_v1_shop_categories_get` | `F-30A` |
| GET | `/api/v1/shop/change-requests` | `change_requests_api_v1_shop_change_requests_get` | `F-30C` |
| POST | `/api/v1/shop/change-requests` | `change_request_create_api_v1_shop_change_requests_post` | `F-30C` |
| POST | `/api/v1/shop/change-requests/{request_id}/review` | `change_request_review_api_v1_shop_change_requests__request_id__review_post` | `F-30C` |
| POST | `/api/v1/shop/checkout` | `checkout_api_v1_shop_checkout_post` | `F-30B` |
| GET | `/api/v1/shop/gateways` | `gateways_api_v1_shop_gateways_get` | `F-30C` |
| POST | `/api/v1/shop/gateways` | `gateway_create_api_v1_shop_gateways_post` | `F-30C` |
| PUT | `/api/v1/shop/gateways/{gateway_id}` | `gateway_update_api_v1_shop_gateways__gateway_id__put` | `F-30C` |
| GET | `/api/v1/shop/orders` | `orders_api_v1_shop_orders_get` | `F-30B` |
| PATCH | `/api/v1/shop/orders/{order_id}` | `order_status_api_v1_shop_orders__order_id__patch` | `F-30B` |
| GET | `/api/v1/shop/orders/{order_id}/receipt` | `order_receipt_api_v1_shop_orders__order_id__receipt_get` | `F-30B` |
| GET | `/api/v1/shop/prices` | `prices_api_v1_shop_prices_get` | `F-30A` |
| POST | `/api/v1/shop/prices` | `price_upsert_api_v1_shop_prices_post` | `F-30C` |
| GET | `/api/v1/shop/products` | `products_api_v1_shop_products_get` | `F-30A` |
| POST | `/api/v1/shop/products` | `create_product_api_v1_shop_products_post` | `F-30C` |
| GET | `/api/v1/shop/products/{product_id}` | `product_detail_api_v1_shop_products__product_id__get` | `F-30A` |
| PATCH | `/api/v1/shop/products/{product_id}` | `update_product_api_v1_shop_products__product_id__patch` | `F-30C` |
| GET | `/api/v1/shop/status` | `status_api_v1_shop_status_get` | `F-30A` |
| GET | `/api/v1/updates/manifest` | `manifest_api_v1_updates_manifest_get` | `F-36` |
| GET | `/health` | `health_health_get` | `F-36` |


**تفسیر:** این‌ها trace links بین operation و microtask هستند، نه ۱۶۳ issue مستقل. هر issue باید AC را برای operationهای حوزه‌اش محدود و آزمون‌پذیر کند؛ هر operation بدون تست/evidence به‌صورت `BLOCKED/UNKNOWN` باقی می‌ماند. اگر پیاده‌سازی آن بخش نیاز به چند PR داشت، issue-family دوباره به issueهای کوچک‌تر شکسته می‌شود و dependency ثبت می‌گردد.


## ۱۴. نگاشت ردیف‌به‌ردیف سطح‌های UI

این crosswalk از `interaction-map.json` snapshot خوانده شده است. تعداد endpoint فقط تعداد ثبت‌شده در آن artifact است؛ آن را با تعداد control، تست E2E یا سطح پذیرش محصول اشتباه نگیرید. هر surface به issue-family می‌رود؛ نقص واقعی در آن surface به micro-fix جدا تقسیم می‌شود.

| Surface | Kind | File/feature root | Endpoint records | Issue-family |
|---|---|---|---:|---|
| `Analytics` | `studio-page` | `mp-app/studio/src/pages/Analytics.tsx` | 2 | `F-34A` |
| `Assessment` | `studio-page` | `mp-app/studio/src/pages/Assessment.tsx` | 4 | `F-17/F-18/F-19/F-32` |
| `Chat` | `studio-page` | `mp-app/studio/src/pages/Chat.tsx` | 5 | `F-31` |
| `CheckIn` | `studio-page` | `mp-app/studio/src/pages/CheckIn.tsx` | 1 | `F-24/F-34B` |
| `Dashboard` | `studio-page` | `mp-app/studio/src/pages/Dashboard.tsx` | 3 | `F-34A` |
| `Expenses` | `studio-page` | `mp-app/studio/src/pages/Expenses.tsx` | 4 | `F-28A/F-28B/F-29` |
| `Finance` | `studio-page` | `mp-app/studio/src/pages/Finance.tsx` | 14 | `F-25A/F-25B/F-25C/F-26A/F-26B/F-27/F-29` |
| `Login` | `studio-page` | `mp-app/studio/src/pages/Login.tsx` | 0 | `F-04/F-05/F-10` |
| `Members` | `studio-page` | `mp-app/studio/src/pages/Members.tsx` | 4 | `F-07A/F-07B/F-07C` |
| `Nutrition` | `studio-page` | `mp-app/studio/src/pages/Nutrition.tsx` | 5 | `F-20/F-21` |
| `Programs` | `studio-page` | `mp-app/studio/src/pages/Programs.tsx` | 7 | `F-11/F-12/F-15/F-16` |
| `Settings` | `studio-page` | `mp-app/studio/src/pages/Settings.tsx` | 11 | `F-05/F-08/F-35A/F-35B/F-35C/F-35D/F-36` |
| `Shop` | `studio-page` | `mp-app/studio/src/pages/Shop.tsx` | 0 | `F-30A/F-30B/F-30C` |
| `assessment14` | `client-feature` | `mp-app/client/lib/features/assessment14` | 3 | `F-18` |
| `auth` | `client-feature` | `mp-app/client/lib/features/auth` | 1 | `F-04/F-05/F-06` |
| `bodycomp` | `client-feature` | `mp-app/client/lib/features/bodycomp` | 1 | `F-17/F-19` |
| `chat` | `client-feature` | `mp-app/client/lib/features/chat` | 4 | `F-31` |
| `checkin` | `client-feature` | `mp-app/client/lib/features/checkin` | 5 | `F-24` |
| `classes` | `client-feature` | `mp-app/client/lib/features/classes` | 0 | `F-22/F-23` |
| `feedback` | `client-feature` | `mp-app/client/lib/features/feedback` | 1 | `F-16` |
| `home` | `client-feature` | `mp-app/client/lib/features/home` | 0 | `F-09` |
| `intake` | `client-feature` | `mp-app/client/lib/features/intake` | 5 | `F-11/F-12` |
| `notifications` | `client-feature` | `mp-app/client/lib/features/notifications` | 0 | `F-32` |
| `nutrition` | `client-feature` | `mp-app/client/lib/features/nutrition` | 0 | `F-20/F-21` |
| `profile` | `client-feature` | `mp-app/client/lib/features/profile` | 5 | `F-05/F-06/F-07A/F-07C` |
| `progress` | `client-feature` | `mp-app/client/lib/features/progress` | 1 | `F-16/F-17/F-18/F-19` |
| `shell` | `client-feature` | `mp-app/client/lib/features/shell` | 0 | `F-09` |
| `shop` | `client-feature` | `mp-app/client/lib/features/shop` | 3 | `F-30A/F-30B` |
| `today` | `client-feature` | `mp-app/client/lib/features/today` | 0 | `F-09/F-16` |
| `wallet` | `client-feature` | `mp-app/client/lib/features/wallet` | 1 | `F-25A/F-25B/F-26A` |
| `core` | `client-feature` | `mp-app/client/lib/core` | 19 | `F-01/F-02/F-03/F-05/F-08` |


`Members`, `auth`, `intake`, `progress` و `core` در artifact فعلی نیازمند بازبینی انسانیِ test mapping هستند؛ `tests: []` یا endpoint بدون test در map یک سرنخ برای B-03 است، نه اثبات نبود هر نوع تست دیگر.


## ۱۵. مرزبندی وضعیت جاری، گپ، وابستگی و هدف آینده

این برچسب‌ها برای جلوگیری از تبدیل نمودار هدف به ادعای قابلیت جاری‌اند. وضعیت هر feature باید روی revision جدید دوباره بررسی شود؛ «current» فقط می‌گوید code/contract در snapshot پیدا شده، نه اینکه کل سفر کاربر pass یا production-ready است.

| وضعیت | کارت‌ها/واقعیت ثبت‌شده | رفتار در backlog |
|---|---|---|
| `CURRENT-CONTRACT / CURRENT-VERIFY` | خانواده‌های route و مدل‌های دامنه در API catalog/source؛ clientهای Flutter/Studio؛ نقش‌های فعلی شش‌گانه؛ برخی سفرهای گزارش‌شده در TestClient | اول trace و آزمون revision دقیق؛ تا PASSِ هر نه حوزه، کار بعدی آزاد نمی‌شود. |
| `GAP` | F-12: `blocked/needs_review` ممکن است draft/نمایش عضو شود؛ F-16: تیک اجرای روزانه در مسیر مرورشده persistence کامل ندارد؛ F-17: JP7 معادله قفل است و ورودی `calf`/`midaxillary` ناهمخوان گزارش شده؛ F-20: generation فعلی meal plan کامل نیست و `meals: []` گزارش شده؛ F-15: UI رد برنامه `window.prompt` است؛ F-29: گزارش مالی ناقص/تعریف سود باز است. | میکرولوپ اصلاحی فقط پس از baseline, owner contract و آزمون‌ها؛ عبارت «حل شد» بدون evidence همان SHA پذیرفته نیست. |
| `CURRENT-VERIFY + OPEN` | F-11: body JSON gate در گزارش قبلی TestClient موفق بوده، اما این نشست آن را دوباره اجرا نکرد؛ F-23: رفتار queue/rebook در TestClient/SQLite گزارش شده، race واقعی نامعلوم؛ F-24: مسیر QR گزارش شده، دستگاه و replay عملی نامعلوم؛ F-33: تعریف scheduler/outbox هست، runtime فعال در startup اثبات نشده؛ F-36/O-* استقرار/restore/device عملی در این کار آزموده نشده. | evidence سطح API/SQLite را به device/network/production تعمیم نده؛ آزمون missing صریحاً `UNKNOWN` است. |
| `CONDITIONAL` | SMS با provider `dev`؛ bank/gateway؛ Ollama/AI optional؛ Valkey، worker، host/HTTPS، backup خارجی و اتصال سرویس‌ها به config/runtime وابسته‌اند. | قبل از provider/secrets/network، D-02/D-05/D-08/D-09، قرارداد، مالک و تست staging لازم است؛ هیچ‌کدام را فعال فرض نکن. |
| `DECISION` | D-01…D-11، از جمله Android+Studio/PWA، role target، topology، مالی، عکس بدن، DB و مدل | مالک تصمیم می‌گیرد؛ issueهای وابسته `BLOCKED` می‌مانند؛ عامل حق انتخاب پیش‌فرض ندارد. |
| `TARGET` | Q-01…Q-11، C-01…C-11، SRC-*، P-01…P-21، ProgramVersion/PDF/QR و scorecard چرخه | design/future؛ فقط بعد از تأیید scope، privacy، domain expert، منبع و license به build-ready تبدیل می‌شود. |

این تفکیک با توضیح master flow سازگار است: خط پیوسته/سبز، خط‌چین کهربایی، گپ قرمز و مسیر وابسته به config معانی جدا دارند؛ رنگ/نمودار به‌تنهایی آزمون E2E نیست.

## ۱۶. برش‌های نهایی قبل از صدور issueهای leaf

نگاشت ۱۶۳ operation در بخش ۱۳ به issue-family اشاره می‌کند. هر family دارای child در این جدول باید در tracker **با child leaf** ثبت شود؛ parent صرفاً grouping است. همهٔ leafها همچنان هر ۹ حوزه را از نو می‌گذرانند.

| Parent | Leaf issueهای پیشنهادی | مرز AC هر leaf |
|---|---|---|
| F-02 | `F-02A` Flutter API client؛ `F-02B` Studio `sessionFetch` | token/refresh و request/error state هر client جدا؛ shared contract از F-01. |
| F-07 | `F-07A` self profile؛ `F-07B` member directory/create/update/scope؛ `F-07C` memberships/plans/invoices | هر leaf یک سفر/مجموعه endpoint هم‌رفتار و تست owner-scope. |
| F-18 | `F-18A` assessment/FieldTest records؛ `F-18B` Axis create/history/matrix/review؛ `F-18C` suggest-weight | هرکدام source/rubric/reviewer جدا؛ F-18C تا D-11 و rule owner `BLOCKED`. |
| F-24 | `F-24A` consent/privacy notice/QR-token؛ `F-24B` QR scan/check-in/exit/replay؛ `F-24C` face method/enrollment/deep-status fail-closed | QR مسیر حضور است؛ face recognition روشن نمی‌شود مگر تصمیم/privacy مستقل. device test برای F-24B در O-10 evidence جداست. |
| F-25 | `F-25A` payment list/create/start/invoice؛ `F-25B` private receipt upload/read؛ `F-25C` staff review/verify/fail/callback/return | actor/state/receipt هرکدام مستقل؛ gateway live فقط با D-05. |
| F-26 | `F-26A` wallet balance/charge/pay/transactions؛ `F-26B` coupon/ledger/reverse | transaction/idempotency و مجوز write هر leaf جدا. |
| F-28 | `F-28A` expense CRUD/revision/grant؛ `F-28B` receipt upload/read | دسترسی فایل و finance scope در leaf receipt جدا تست می‌شود. |
| F-30 | `F-30A` public/member catalog read؛ `F-30B` cart/orders/checkout fail-closed؛ `F-30C` staff catalog/price/gateway/change request | checkout عضو تا D-05 خاموش؛ staff mutation و `super_admin` review تا D-03. |
| F-33 | `F-33A` scheduler startup/lease/heartbeat؛ `F-33B` outbox notification delivery/retry؛ `F-33C` finance report schedule/manual run | worker active بودن، idempotency و schedule هرکدام runtime evidence خود را دارند. |
| F-34 | `F-34A` analytics/KPI/member summary؛ `F-34B` staff attendance/check-in view؛ `F-34C` confidential report access | grant محرمانه جدا از KPI و نمودار آزمون می‌شود. |
| F-35 | `F-35A` permissions/users/roles؛ `F-35B` flags؛ `F-35C` retention preview/run؛ `F-35D` audit | تغییر permission/retention فقط با owner decision و audit evidence. |
| F-37 | `F-37A` inventoryِ tokens/reduced motion/a11y baseline؛ `F-37B…F-37AF` هر اصلاح واقعی، یک surface/یک رفتار در هر issue | ۳۱ سطح UI در Section 14؛ bulk restyle یا اصلاح چندصفحه‌ای issue واحد نمی‌شود. |
| P-14 | `P-14A` renderer/template/font/license؛ `P-14B` RTL/print visual regression | PDF از version ID ثابت؛ هر تغییر font/layout شواهد render دقیق می‌خواهد. |

`F-37B…F-37AF` فقط pattern نام‌گذاری leafهاست؛ تعداد و عنوان واقعی پس از B-03 و defectهای قابل‌مشاهده تعیین می‌شود، نه از پیش حدس زده. هیچ leaf پیشنهادی به‌تنهایی اجازهٔ نصب Finn-loop یا ایجاد issue خارجی نیست.
