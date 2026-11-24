# مقایسهٔ طرح ارسالی با handoff قبلی و دامنهٔ اصلاح v2

## نتیجه

**طرح ارسالی کاربر مبنای بهتر و منتخب است**؛ چون با کد فعلی هم‌جهت‌تر است، Studio موجود را توسعه می‌دهد، کار عضو و کادر و آزمون‌های PWA واقعی را از هم تفکیک می‌کند و فرض «اپ React دوم» را حذف می‌کند. این پذیرشِ برنامهٔ UI، تصویب بی‌قیدِ role/DB/offline/payment/release نیست.

**شمارش صادقانه:** جدول ارسالی دقیقاً **۵۰ ردیف** دارد: ۶ + ۸ + ۵ + ۱۶ + ۸ + ۷. `PWA-56` آخرین شناسه است، اما gap عددی و شناسه‌های حرفی PWA-3A…3F دارد. شش task اضافی نساخته‌ایم تا متن با ادعای قبلی ۵۶ هم‌شمار شود. هر ۵۰ ID، عنوان و مرز پذیرش در SOURCE_PLAN حفظ و ۱:۱ به artifactهای v2 نگاشت شده‌اند.

## تفاوت‌های مؤثر

| محور | v1 تاریخی | طرح منتخب و اصلاح v2 |
|---|---|---|
| هویت backlog | ۲۸ مورد تازهٔ پیشنهادی بدون نگاشت معتبر به فهرست قبلی؛ اشتباه در ادعای پوشش | ۵۰ parent ارسالی بدون حذف/ادغام/renumber؛ source جدا و traceability و تست literal IDs/AC |
| پایهٔ React | پیشنهاد مسیر جدا از Studio در بخشی از طرح | فقط `mp-app/studio/`؛ member/staff در یک PWA؛ staff موجود adapt شود |
| pin محصول | MP/main در `35d4b35…` | شاخهٔ ارسالی کاربر `arena/5e0f64cf-mp` در `c46e792657e361cd09799c896c47149b4a5c4d86`؛ کد مقصد تازه همچنان باید reconcile شود |
| تصمیم‌های D | اصل متن بازیابی نشده بود؛ reserved و سؤال‌های Q جدا | D-01…11 عین جدول draft در خطوط 68–78 بازیابی؛ Qهای handoff v1 retired، نه جایگزین D یا Qهای سلامت backlog |
| Flutter/Android/Electron | اصل حفاظت وجود داشت اما نقشهٔ اختصاصی/گیت کافی نبود | PWA-05 و PWA-55 صریح؛ web.yml Flutter Web محفوظ؛ Electron جدا و محفوظ |
| صفحات staff | خطر بازسازی/نادیده‌گرفتن صفحات موجود | PWA-40…47 نگاشت و تکمیل؛ Ant Design/توکن/فونت بی‌دلیل تعویض نشود |
| PWA موجود | طرح جدید ممکن بود از صفر تصور شود | manifest/icon/SW/Nginx موجود به‌عنوان CURRENT-VERIFY؛ اصلاح allowlist/method/cache/update و تست browser واقعی |
| هویت/مجوز | خطر یکی‌گرفتن token parsing با مجوز یا target سه‌نقشی با migration | شش نقش جاری محفوظ؛ member در allowlist فعلی AuthContext نیست؛ server identity/ownership، revoke/stale و API منفی جدا |
| رفتار عضو | دسته‌بندی کلی و مرزهای کمتر روشن | شانزده کارت PWA-30…3F؛ IRR/persistence/health/receipt/catalog/chat/inbox و آفلاین شرطی جدا |
| budget | ۳ تلاش/۹۰ دقیقه با ابهام تصویب | سه تلاش کل با G4 متن Finn سازگار ولی runtime enforced نیست؛ ۹۰ دقیقه صریحاً پیشنهاد نیازمند تصویب؛ هزینه/egress مکمل بدون مجوز صفر |
| ابزار | catalog گسترده با خطر برداشت install-all | Finn/Actions/Semgrep/Gitleaks موجود اولویت؛ tools جدا از runtime؛ renderer هم‌خانواده با Graphviz موجود MP؛ ابزارهای موازی deferred |
| تست تحویل | structure/hash خوب، اما تست آن ۲۸ مورد پوشش اصل طرح را ثابت نمی‌کرد | تست source مستقل از plan output، exact titles/AC و مجموعهٔ ۵۰ ID در JSON/Markdown/CSV/roadmap، regression حذف/تغییر و checksum/ZIP |

## چه چیز از طرح ارسالی با قید روشن پذیرفته شد؟

- «هر سطر یک میکرولوپ» parent planning unit است؛ بعضی سطرها برای یک PR بیش از حد بزرگ‌اند. خردسازی به فرزند با AC mapping **قبل از AGENT-READY** لازم است؛ parent اصلی حذف نمی‌شود.
- «حداکثر سه تلاش» در source Finn هم آمده؛ این سازگاری متنی است نه اثبات نصب Finn runtime. budget زمان/هزینهٔ عددی هر کارت هنوز قبل از اجرا تصویب می‌شود.
- «PWA مشترک/نقش‌های ساده‌تر» فقط بخش اول، جهت صریح UI کاربر است؛ کاهش شش نقش backend به سه یا ایجاد grant implicit مجاز نیست.
- «online-first» پیشنهاد امن آغاز است. PWA-3F پیش‌فرض BLOCKED؛ defer برای release بدون offline، پاسخ صریح مالک و ثبت scope می‌خواهد؛ BLOCKED و DEFERRED گواه PASS نیستند.
- «staging» به قرارداد مقصد/مجوز نیاز دارد؛ این بسته هیچ deploy/workflow dispatch/production/rollback/live payment را خودکار نمی‌کند.
- تعداد سابق ۵۶ یا گزارش builder با ۲۶ مورد، از این جدول قابل اثبات نیست. v1 از Git حذف نمی‌شود و برای تاریخچه دست‌نخورده می‌ماند.

## همهٔ بخش‌هایی که بازبینی می‌شوند

1. راهنمای اصلی، HTML آفلاین، README شروع/دانلود و prompt انتقال؛ هویت مخزن و شروع PWA-00.
2. source inventory ثابت، plan ماشین‌خوان ۵۰موردی، متن کامل کارت‌ها، DAG پیشنهادی، نگاشت ۱:۱ و ماتریس parity/interaction.
3. Finn نهایی، template قرارداد/ADR/evidence/state و ۹ حوزه + پنج گیت در هر کارت؛ review مستقل و merge انسانی.
4. رجیستر D واقعی و decision package با دامنهٔ پاسخ‌های قبلی و سؤال‌های باز؛ هیچ owner approval جعل نشده است.
5. نمودار چرخه و roadmap تمام ۵۰ کارت با DOT/Mermaid/PNG/SVG؛ copies فعلی docs از v2 و نسخهٔ قدیم داخل v1 تاریخی محفوظ.
6. پیش‌پرواز/validator خواندنی، مثال‌های config متناسب با Studio و نصب ابزار ایزوله/اختیاری، catalog/provenance و lock جدید renderer.
7. builder نسخه‌پذیر، تست پوشش source و regression، manifests، گزارش صادقانهٔ verification و ZIP نسخهٔ جدا.

## چیزهایی که این اصلاح انجام نمی‌دهد

هیچ کد محصول MP تغییر/اجرا نشده؛ feature parity، API enforcement، امنیت، نصب واقعی PWA، CI محصول، دستگاه، بازبینی مستقل، مجوز حقوقی بازتوزیع عمومی یا Go محصول از ساخت این اسناد نتیجه نمی‌شود. مجوز کاربر برای انتشار handoff در Chat2DB، مجوز push/merge/deploy محصول MP یا افشای داده/کد به سرویس مکمل نیست.

این صفحه changelogِ اصلاح بسته است؛ نتایج **واقعاً اجراشدهٔ بسته** و محدودیت‌های آن فقط در [VERIFICATION.fa.md](VERIFICATION.fa.md) ثبت می‌شوند.
