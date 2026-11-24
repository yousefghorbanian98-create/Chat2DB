# بستهٔ تحویل Arena — مسیر React PWA برای Muscle Paradise

این بسته برای بیلدری نوشته شده که سابقهٔ گفتگو را ندارد. **مستندات و نقشهٔ شروع است، نه پیاده‌سازی PWA یا انتشار محصول.**

## دانلود

**[دانلود مستقیم MP-PWA-Arena-Handoff-v1.0.0.zip](https://github.com/yousefghorbanian98-create/Chat2DB/raw/refs/heads/arena/d885a3c9-chat2db/handoff/releases/MP-PWA-Arena-Handoff-v1.0.0.zip)**

[SHA-256 فایل ZIP](releases/MP-PWA-Arena-Handoff-v1.0.0.zip.sha256) · [فایل اصلی handoff](pwa-arena-v1/HANDOFF.fa.md) · [HTML آفلاین](pwa-arena-v1/HANDOFF.fa.html) · [طرح ماشین‌خوان](pwa-arena-v1/PWA_PLAN.json)

برای شروع، ZIP را باز کنید و `README_FIRST.fa.txt`، سپس `HANDOFF.fa.html` یا `HANDOFF.fa.md` را بخوانید. **کل بسته** را به محیط بیلدر برسانید و پیام آمادهٔ بخش ۱ handoff را کپی کنید.

## چه چیزهایی دارد؟

- خواستهٔ محصول، هویت دو مخزن و مسیرهای واقعی کد؛ source محصول در `yousefghorbanian98-create/MP` است.
- تقسیم‌بندی **پیشنهادی PWA-00 تا PWA-27**، شامل هر **۱۷ حوزه**ٔ client، وابستگی و معیار پذیرش.
- نقش Arena به عنوان کدنویس اصلی؛ ابزارهای قطعی، بازبین مستقل واقعی، گیت‌های امنیت/حریم/مالی/حقوقی/محصول و سقف ۳ تلاش کل/۹۰ دقیقه.
- ابزارهای OSS، نسخه/مجوز/منبع، محل نصب جدا از runtime و فرمان‌های مرحله‌ای.
- همان فلوچارت PNG/SVG و منبع Mermaid؛ تصویر در HTML هم embed شده است.
- قالب microtask، ADR، شواهد، ماتریس interaction و برابری حوزه‌ها؛ رجیستر تصمیم‌ها.
- preflight خواندنی، lock ابزارهای Node و اسکریپت ترسیم؛ بدون source کامل MP، binary، SDK، secret، DB یا دادهٔ عضو.

## مرزهای مهم

Flutter/Android **حفظ می‌شود**؛ تعارض baseline انتشار PWA/Android فقط با تصمیم مالک و ADR بسته می‌شود. هیچ role/grant/retention/پرداخت واقعی/merge/deploy از این بسته مجوز نمی‌گیرد. `UNKNOWN` و تست اجرا نشده PASS نیست.

متن کامل و نگاشت تاریخی D-01..D-11 تأیید نشد؛ IDها رزرو هستند و جعل/بازتعریف نشده‌اند. Q-01..Q-11 سؤال‌های جدید همین تحویل‌اند، نه جایگزین تصمیم‌های قبلی. PWA-00 فقط از بررسی خواندنی و کار مستقل شروع می‌شود.

## بازتولید بسته و تست

از ریشهٔ همین مخزن، فقط ابزار ساخت مستندات را در محیط جدا نصب کنید:

```bash
python3.11 -m venv handoff/.venv-docs
handoff/.venv-docs/bin/python -m pip install -r handoff/requirements-docs.txt
handoff/.venv-docs/bin/python handoff/build_pwa_handoff.py
handoff/.venv-docs/bin/python -m unittest discover -s handoff/tests -v
(cd handoff/pwa-arena-v1 && sha256sum -c MANIFEST.sha256)
(cd handoff/releases && sha256sum -c MP-PWA-Arena-Handoff-v1.0.0.zip.sha256)
```

خروجی ZIP با timestamp و ترتیب ثابت ساخته می‌شود. hash خود ZIP بیرون آن است؛ manifest داخلی self-hash ندارد. [گزارش اعتبارسنجی](pwa-arena-v1/VERIFICATION.fa.md) مرز تست بسته و تست محصول را روشن می‌کند. تست‌های ساختاری و preflight روی fixture مصنوعی هستند، نه شاهد اجرای MP.

فقط source این بسته، خروجی ZIP درخواستی و نمودارها در این شاخه تحویل می‌شوند؛ هیچ PR، merge، tag، GitHub Release یا deploy محصول برای این تحویل لازم نیست.
