# ADR پیشنهادی — عنوان تصمیم محدود

- ID تازه مطابق قرارداد ADR مخزن مقصد / تاریخ / وضعیت: PROPOSED
- task/parent: PWA-00 یا کارت مرتبط / D IDs / source pin:
- owner و scope approval: هنوز ثبت نشده

## مسئله و شواهد

رفتار source فعلی، تعارض سند، نیاز کاربر، ریسک و شاهد exact SHA را جدا بنویس. جهت صریح React و حفظ native را از تصمیم‌های باز role/offline/release تفکیک کن.

## گزینه‌ها و انتخاب پیشنهادی

گزینه‌های واقعی، هزینه/مجوز/داده/امنیت/قابل‌بازگشت‌بودن؛ توصیهٔ محدود. ADR مورد قبول قبلی بی‌صدا ویرایش نشود؛ این ADR در صورت تصویب آن را با ارجاع supersede می‌کند.

## مرز انتخاب برای مسیر PWA

- توسعهٔ `mp-app/studio/` برای member+staff؛ نه اپ دوم؛ reuse صفحات staff و UI موجود.
- Flutter/Android، فایل‌ها/اسناد/تست‌ها/CI و Electron حفظ می‌شوند؛ packaging Electron شرط PWA نیست.
- فقط جهت UI: هیچ migration شش نقش/grants/DB/tenant/payment، offline حساس یا مجوز release/deploy/egress از این ADR استنتاج نشود.
- baseline انتشار و device/role/journey/evidence contract با D-01/D-10 جدا ثبت شود.

## اثر و آزمون

مسیرها/API/داده/role/CI متاثر؛ compatibility و native gates؛ security/privacy/finance/legal/product و ۹ حوزهٔ Finn برای همین تغییر؛ آزمون مثبت/منفی و rollback صرفاً طرح، نه اقدام بیرونی.

## تصویب و اجرا

owner / تاریخ / دامنهٔ دقیق / status؛ implementation task IDs؛ head SHA/test/reviewer/merge evidence. تا تصویب، تصمیم پیشنهادی می‌ماند و فقط کار وابسته BLOCKED است.
