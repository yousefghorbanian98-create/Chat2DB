# بستهٔ واحد تصمیم‌های مالک — فقط ابهام‌های مؤثر را متوقف کن

**اصل:** قبل از سؤال، تصمیم‌های معتبرِ checkout جاری (`AGENTS`، ADR، `OWNER-DECISIONS`، صف/هندآف) بررسی شوند. این جدول درخواست پاسخ دوباره به همهٔ گذشته نیست. D-01…D-11 از draft اصلی MP بازیابی شده‌اند؛ متن دقیق و URL/line/pin در [DECISION_REGISTER](templates/DECISION_REGISTER.json) است. وضعیت `DECISION` در رجیستر یعنی input لازم است، نه پاسخ مصوب. نسخهٔ draft منبع، خود backlog اجرایی یا ADR مصوب نیست.

## زمینهٔ قطعی این مأموریت

کاربر مسیر UI جدید را **React PWA با گسترش Studio موجود و حفظ Flutter/Android** خواسته است. این جهت برای آماده‌سازی PWA-00 معلوم است؛ release baseline، شش‌نقش/سه‌نقش، storage، offline و staging خودکار مصوب نیستند. نقش‌های backend فعلی `member / coach / reception / manager / admin / super_admin` بمانند تا ADR مستقل. فروشگاه نمایشی، رسید خصوصی/بازبینی انسانی، نبود عکس بدن و نبود ادعای پزشکی محدودیت‌های این طرح‌اند؛ افزایش scope به‌بهانهٔ برابری Flutter ممنوع است.

## چهار پاسخ فوری را یک‌جا آماده کن

| موضوع | پاسخ لازم از مالک | پیشنهاد محدود و برگشت‌پذیر | تا زمان پاسخ چه می‌شود؟ |
|---|---|---|---|
| D-01 + D-10: release baseline | نقش PWA در انتشار اول، وضعیت پشتیبانی Android/Flutter Web، فهرست پنج سفر/دستگاه و حداقل evidence | ثبت جهت React/Studio در ADR؛ native و همهٔ CI فعلی حفظ؛ معیار پذیرش جدا | ممیزی/قرارداد/پروتکل و protection inventory ادامه؛ ادعای جایگزینی native یا Go متوقف |
| D-03: نقش و grants | حفظ شش نقش یا target دیگر؟ چه کسی grant می‌دهد/لغو می‌کند؟ permission matrix هر operation و ownership چیست؟ | حفظ شش نقش فعلی؛ UI گروه‌بندی member/staff بدون migration؛ server enforcement مرجع | UI prototype غیرحساس و source crosswalk ادامه؛ تغییر role/grant/DB و feature وابسته BLOCKED |
| D-06 + جزئیات PWA-03: session/offline | ریسک token در localStorage، refresh/revoke/expiry و دادهٔ مجازِ ماندگار/retention؛ آیا feedback offline واقعاً لازم است؟ | online-first؛ فقط static shell؛ هیچ API/PII/receipt/health/chat/session cache و هیچ offline write حساس | مستندسازی و تست منفی source ادامه؛ cache حساس/PWA-3F و storage migration تأییدنشده BLOCKED |
| D-02/D-09/D-10: staging/release | میزبان/HTTPS/ingress، مسئول عملیات، بودجه و مجوز محدود staging با دادهٔ مصنوعی و SHA | config/tests محلی اول؛ staging جدا از production و فقط بعد از scope/authorization | build/مرور config مجازِ قرارداد ادامه؛ deploy/workflow dispatch/release/rollback بیرونی متوقف |

**نکتهٔ session:** این بسته گزینهٔ cookie یا localStorage را به‌جای مالک «تصویب» نمی‌کند؛ threat model، CORS/CSRF/CSP، XSS و قرارداد backend باید با هم بررسی شوند. حذف token از localStorage بدون هم‌راستایی refresh/revoke سرور و Electron، اصلاح اثبات‌شده نیست.

## پوشش کامل یازده D، بدون بازتعریف آن‌ها

| ID / عنوان اصلی | حداقل خروجی تصمیم | اثر روی برنامه و کار مستقل |
|---|---|---|
| D-01 — دامنهٔ client انتشار اول | baseline و platform/test مصوب؛ React UI فقط بخشی از پاسخ است | PWA-00/10/54/55/56؛ ممیزی مستقل ادامه |
| D-02 — topology و ingress | میزبان، شبکه، HTTPS، مسئول و دسترس‌پذیری | PWA-17/54؛ config خواندنی/محلی مجاز، نه خرید یا deploy |
| D-03 — نقش‌ها و grants | شش نقش یا target مصوب، ماتریس مجوز و مرجع grant | PWA-02 و auth/staff/security وابسته؛ server gate تضعیف نشود |
| D-04 — تک‌باشگاه یا multi-tenant | scope باشگاه و اثر شناسه/ownership | crosswalk PWA-01 و API منفی PWA-24/53؛ tenant migration فقط اگر دامنه عوض شود، نه پیش‌شرط ساخت UI بی‌خطر |
| D-05 — سیاست پرداخت و فروشگاه | manual transfer/human reconciliation، catalog و checkout state | PWA-3A/3B/3C/44/45/56؛ فعلاً checkout خاموش و no live money |
| D-06 — حریم خصوصی و retention | classes/consent/retention/delete/backup و scope سلامت/عکس | session/cache/3F/receipt/chat/health و PWA-51/53؛ عکس بدن خارج scope |
| D-07 — DB و معیار مهاجرت | بار/همزمانی/restore/RPO/RTO برای ارزیابی SQLite/Postgres | فقط اگر GAP backend واقعاً به DB مربوط شد؛ React مجوز migration نیست، UI مستقل بلوکه نشود |
| D-08 — سیاست مدل و egress عامل | مدل/محل اجرا/کد و دادهٔ مجاز، budget و kill switch | تمام ابزارهای مکمل/مدل/telemetry و آفلاین مرتبط؛ هیچ API ابری یا egress پیش‌فرض |
| D-09 — مالک عملیات، بودجه و پشتیبانی | مسئول staging/backup/restore/alert و سقف هزینه/زمان | PWA-54/56 و budget هر کارت؛ ابزار محلی بی‌هزینه جای انتخاب provider نیست |
| D-10 — تعریف «همهٔ قابلیت‌های اصلی» | سفر، role، دستگاه، RTL و حداقل شاهد مالک | PWA-00/39/50…56؛ تعداد page/route معیار کامل‌بودن نیست |
| D-11 — مرز تغذیه، سلامت و منابع | مسئول حرفه‌ای، جمعیت هدف، مرجع/مجوز و حد ادعا | PWA-33/35/36/37/42/56؛ LLM اعداد/تشخیص/تغذیه نمی‌سازد |

## فرم پاسخ یک‌جای مالک

برای هر D مؤثر، این فیلدها تکمیل و با ADR/تصمیم جاری لینک شوند؛ کارت را صرفاً با نوشتن «تصمیم شد» نبندید:

- ID و پرسش با دامنهٔ دقیق؛ منبع تصمیم قبلی اگر هست؛ conflict با طرح تازه.
- گزینهٔ منتخب، دلیل و non-goals؛ نقش پاسخ‌دهنده و تاریخ.
- paths/roles/data/محیط‌های شامل و مستثنا؛ اذن اثر بیرونی **اگر وجود دارد** جداگانه و محدود.
- عدد budget زمان/هزینه/تلاش و stop rule؛ ۳ تلاش کل سقف پیشنهادی/سازگار با متن Finn، ۹۰ دقیقه نیازمند تصویب صریح.
- evidence/آزمون لازم برای enforce کردن تصمیم؛ owner/spec approval با product/medical/legal approval یکی نیست.
- taskهای بازشونده، taskهای همچنان BLOCKED و کار مستقل بعدی.

پاسخ برگشت‌ناپذیر یا پرریسک را حدس نزنید. اگر پاسخ نیامد، `BLOCKED + دلیل` برای وابسته و ادامهٔ مستقل با قرارداد معتبر، نه توقف کل صف و نه PASS ساختگی.
