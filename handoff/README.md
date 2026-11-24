# بستهٔ تحویل اصلاح‌شدهٔ Arena — React PWA برای Muscle Paradise

برای بیلدر بدون سابقهٔ گفتگو: **نقشه و قرارداد اجراست، نه پیاده‌سازی یا گواه PASS محصول.**

## دانلود نسخهٔ منتخب v2.0.0

**[دانلود مستقیم MP-PWA-Arena-Handoff-v2.0.0.zip](https://github.com/yousefghorbanian98-create/Chat2DB/raw/refs/heads/arena/d885a3c9-chat2db/handoff/releases/MP-PWA-Arena-Handoff-v2.0.0.zip)**

[SHA-256 خود ZIP](releases/MP-PWA-Arena-Handoff-v2.0.0.zip.sha256) · [راهنمای اصلی](pwa-arena-v2/HANDOFF.fa.md) · [HTML کامل آفلاین](pwa-arena-v2/HANDOFF.fa.html) · [متن کامل ۵۰ کارت](pwa-arena-v2/MICROLOOPS.fa.md) · [JSON](pwa-arena-v2/PWA_PLAN.json)

ZIP را استخراج و `README_FIRST.fa.txt` را بخوانید؛ `HANDOFF.fa.html` راهنما، تمام ۵۰ کارت، Finn، تصمیم‌ها، ابزارها و دو تصویر را در یک HTML بدون JS/شبکه دارد. **کل بسته** و `templates/RESUME_PROMPT.fa.txt` را به بیلدر بدهید تا از PWA-00 آغاز کند.

## چه چیز اصلاح شد؟

- مبنای منتخب **همان طرح ارسالی کاربر با ۵۰ ID/عنوان/مرز پذیرش** است؛ ۶/۸/۵/۱۶/۸/۷ ردیف در شش فاز. PWA-56 شمارهٔ آخر است و count نیست؛ PWA-3A…3F حفظ شده‌اند. حذف/ادغام/renumber یا شش کارت ساختگی نداریم.
- `mp-app/studio/` موجود به یک PWA مشترک member/staff گسترش می‌یابد؛ نه اپ React دوم، نه مهاجرت به Flutter Web. صفحات staff و UI موجود بازاستفاده شوند.
- Flutter/Android، مستندات/تست/CI و Flutter Web job فعلی و Electron محفوظ؛ packaging Electron پیش‌شرط PWA نیست.
- D-01…D-11 از منبع واقعی MP در `c46e792657e361cd09799c896c47149b4a5c4d86` بازیابی شده‌اند؛ نه reserved/unmapped. تصمیم React، مدل نقش/DB/session/offline/payment/release را ضمنی حل نمی‌کند.
- Finn نهایی: ۹ حوزه + پنج گیت مستقل در **هر کارت/فرزند**، شاهد همان SHA، budget/stop صریح، reviewer مستقل و human approval/merge؛ UNKNOWN قبولی نیست.
- دو نمودار جدید: چرخهٔ هر کارت و نقشهٔ تک‌تک ۵۰ parent؛ PNG/SVG/DOT/Mermaid داخل ZIP و [docs](../docs/PWA_Finn_Loop_Flow.fa.md).
- source inventory مستقل، traceability، templateها، ابزار/lock/config ایزوله، preflight/validator خواندنی، builder نسخه‌پذیر و تست‌های ضدحذف/تغییر AC بازبینی شده‌اند.

[مقایسه و changelog کامل](pwa-arena-v2/COMPARISON_AND_CHANGELOG.fa.md) · [Finn نهایی](pwa-arena-v2/FINN_LOOP_FINAL.fa.md) · [منبع جدول کاربر](pwa-arena-v2/SOURCE_PLAN.fa.md) · [گزارش اعتبارسنجی](pwa-arena-v2/VERIFICATION.fa.md)

## شروع و مرز مجوز

محصول در `yousefghorbanian98-create/MP` است؛ این مخزن Chat2DB فقط تحویل را میزبانی می‌کند و `mp-app/` ندارد. pin منبع دستور checkout/reset/switch شاخه نیست. در محیط مقصد repo/شاخه/AGENTS/صف جاری و authority خود آن محیط را بررسی کنید. کار بدون قرارداد AGENT-READY نشود.

پیشنهاد آغاز online-first/static shell، بدون API/PII/session/receipt/health cache یا offline write حساس است؛ PWA-3F پیش‌فرض BLOCKED. سه تلاش **کل** و دو retry؛ ۹۰ دقیقه پیشنهاد نیازمند تصویب مالک است. هیچ MP push/PR/merge، deploy/release/rollback، پرداخت واقعی، DB یا egress/مدل مکمل از handoff مجوز نمی‌گیرد.

## کنترل بسته پس از استخراج — بدون نصب

از ریشهٔ ZIP استخراج‌شده، Python 3.11+:

```bash
sha256sum -c MANIFEST.sha256
python3 scripts/sync_plan.py --check
python3 scripts/make_roadmap.py --check
python3 scripts/validate_package.py
```

این‌ها فقط تمامیت بسته و حفظ source plan را می‌سنجند؛ `PACKAGE_OK_NOT_QA` و `INVENTORY_OK_NOT_QA` شاهد محصول یا approval نیستند. snapshotهای محصول فقط متن با pin/hash هستند؛ کد کامل runtime، SDK/browser binary، DB، `.env` یا دادهٔ عضو داخل ZIP نیست.

## بازتولید در همین مخزن تحویل

```bash
# فقط dependency مستندسازی در venv جدا؛ نه dependency محصول
python3.11 -m venv handoff/.venv-docs
handoff/.venv-docs/bin/python -m pip install -r handoff/requirements-docs.txt
python3 handoff/pwa-arena-v2/scripts/sync_plan.py --check
python3 handoff/pwa-arena-v2/scripts/make_roadmap.py --check
handoff/.venv-docs/bin/python handoff/build_pwa_handoff.py --version 2.0.0
handoff/.venv-docs/bin/python -m unittest discover -s handoff/tests -v
(cd handoff/pwa-arena-v2 && sha256sum -c MANIFEST.sha256)
(cd handoff/releases && sha256sum -c MP-PWA-Arena-Handoff-v2.0.0.zip.sha256)
```

اگر متن source/metadata تغییر کرد، ابتدا sync بدون `--check` و سپس تست بازبینیِ exact inventory اجرا شود؛ تغییر ۵۰ ID/AC نیاز به تصمیم صریح دارد و نباید با بازتولید output پنهان شود. تصاویر از DOT با ابزار جدا مطابق [TOOLCHAIN](pwa-arena-v2/TOOLCHAIN.fa.md) رندر می‌شوند؛ builder خودش tool/browser نصب نمی‌کند. timestamp/order/permission ZIP ثابت و hash ZIP بیرون خودش است؛ manifest داخلی self-hash ندارد.

## تاریخچه — v1 را برای اجرای این طرح استفاده نکنید

[v1.0.0 تاریخی](releases/MP-PWA-Arena-Handoff-v1.0.0.zip) و payload آن بدون تغییر نگه داشته شده‌اند. این نسخه **۲۸ مورد تازهٔ پیشنهادی** بود و هیچ نگاشت تأییدشده‌ای به ۵۶ مورد قبلی یا ۵۰ ردیف فعلی نداشت؛ تست‌های قبلی صرفاً ساختار همان پیشنهاد را می‌سنجیدند. تعداد ۲۶ گزارش‌شدهٔ builder هنوز علت اثبات‌شده ندارد. هیچ استناد v1 برای تکمیل دامنهٔ v2 کافی نیست.

`build_pwa_handoff.py --version 1.0.0` فقط فایل‌های frozen v1 را با همان bytes بازبسته‌بندی می‌کند و HTML/manifest تاریخی را regenerate نمی‌کند. تست‌های v1 همچنان از artifact تاریخی خودشان می‌سنجند؛ تست‌های مستقل v2 تطبیق طرح ارسالی را کنترل می‌کنند.

فقط اسناد/نمودارها/بستهٔ تحویل در این شاخه منتشر می‌شوند. هیچ PR، merge، tag، GitHub Release، workflow dispatch یا deploy محصول برای این تحویل انجام نمی‌شود.
