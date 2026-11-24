# قرارداد microtask — قبل از کدنویسی تکمیل شود

> قالب خالی است؛ هیچ فیلد زیر شاهد اجرا یا پذیرش نیست. مقدار نامعلوم را `UNKNOWN` بنویس، نه حدس.

- ID: `PWA-xx.n`
- وضعیت: `PROPOSED`
- هدف واحد و رفتار قبل/بعد:
- repository / شاخهٔ مجاز / base SHA / dirty state:
- تصمیم‌های لازم با namespace و منبع:
- وابستگی واقعی و وضعیت merge/پذیرش آن:
- in-scope (مسیر و رفتار دقیق):
- out-of-scope (از جمله Flutter/Android، grants و دادهٔ واقعی):
- فایل‌های مجاز موجود و خروجی پیشنهادیِ صریحاً ناموجود:
- ورودی و fixture مصنوعی:
- خروجی مورد انتظار و مدل/API/مالک داده:
- معیارهای Given/When/Then، با تست مثبت، منفی، empty، error، offline و ownership:
- فرمان هر تست، cwd، نسخه، timeout و شمار تست مورد انتظارِ غیرصفر:
- معیار lint/type، graph، dead-code، SAST و supply-chain مرتبط:
- بازبین واقعاً مستقل و روش بازتولید:

## پنج گیت دامنه‌ای — برای هر زیرکار الزامی است

| گیت | اثر/ریسک | تست/شاهد لازم | مسئول تأیید | نتیجه |
|---|---|---|---|---|
| امنیت | UNKNOWN | NOT_RUN | UNASSIGNED | UNKNOWN |
| حریم | UNKNOWN | NOT_RUN | UNASSIGNED | UNKNOWN |
| مالی | UNKNOWN | NOT_RUN | UNASSIGNED | UNKNOWN |
| حقوقی | UNKNOWN | NOT_RUN | UNASSIGNED | UNKNOWN |
| محصول | UNKNOWN | NOT_RUN | UNASSIGNED | UNKNOWN |

N/A فقط با دلیل محدود و تأیید مالک ریسک؛ نبود ابزار/مدل/دستگاه دلیل N/A نیست.

## بودجه و بازگشت

- سقف: **۳ تلاش کل، ۲ retry، ۹۰ دقیقه**؛ هر کدام زودتر تمام شد، `BLOCKED`.
- سقف پیشنهادی اندازه: ۸ فایل دست‌نویس/۴۰۰ خط؛ بزرگ‌تر را پیش از اجرا خرد کن.
- rollback محدود/غیرمخرب؛ برای DB فقط طرح مجاز و fixture:
- اثر خارجی مجاز در همین کار (پیش‌فرض هیچ):
- در نتیجهٔ مبهم push/upload/payment ابتدا remote state خوانده شود؛ retry کور ممنوع.
- شرط stop و سؤال بستهٔ مالک:
- کار مستقل بعدی در صورت BLOCKED:

## چرخه

scope → Arena → کنترل قطعی → بازبین مستقل → گیت → evidence → تأیید/merge لازم.
`AGENT-READY` فقط مجوز شروع در همین دامنه است؛ `VERIFIED` نیازمند اجرا و شاهد واقعی است.
