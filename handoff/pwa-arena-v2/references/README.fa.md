# منشأ منابع، pin و مرز شواهد

## مرجع محصول و شرایط استفاده

- repository: [yousefghorbanian98-create/MP](https://github.com/yousefghorbanian98-create/MP)
- شاخهٔ ارسالی کاربر: `arena/5e0f64cf-mp`؛ pin بررسی‌شده: [`c46e792657e361cd09799c896c47149b4a5c4d86`](https://github.com/yousefghorbanian98-create/MP/commit/c46e792657e361cd09799c896c47149b4a5c4d86)، زمان `2026-11-24T08:58:07Z`.
- فایل‌های منتخب با GitHub API/tree/blob به‌صورت خواندنی گرفته شده‌اند؛ tree غیرtruncated بود. فایل‌ها source هستند و در این تحویل اجرا نشده‌اند. remote/local source جدیدتر در مقصد باید reconcile شود؛ pin دستور reset/checkout نیست.
- `LICENSE.source.txt` (نام واقعی snapshot در SOURCE_MANIFEST) شرایط **Proprietary** MP را ثبت می‌کند؛ مجوز بازتوزیع عمومی یا egress از عمومی‌بودن GitHub نتیجه نمی‌شود. بسته با درخواست مالک برای handoff آماده شده و حقوق/محدودیت کد و وابستگان را تغییر نمی‌دهد. این منابع برای گیرندهٔ مجازند، نه مجوز مستقلِ reuse/hosting/مدل ابری.
- نام snapshotها با `__` و `.source.txt` عمداً از فایل اجرایی/AGENTS حاکم جداست. هیچ script یا snippet تاریخی داخل آن‌ها دستور خودکار نیست. دستورهای ECC در FINN تاریخی‌اند و طبق AGENTS/ECC-removal اجرا نشوند.

## محتوا

| فایل | کاربرد / چیزی که اثبات نمی‌کند |
|---|---|
| `SOURCE_MANIFEST.json` | ۲۷ snapshot منتخب با repository/path/commit/URL/SHA-256؛ فقط byte provenance، نه اجرای تست |
| `MP_SOURCE_COMMIT.json` | metadata پالایش‌شدهٔ commit/branch/date و nontruncated tree؛ نه دستور checkout |
| `HANDOFF_HTML_SMOKE.json` / `HANDOFF_HTML_SMOKE.recipe.mjs.txt` | بررسی فقط HTML خود تحویل در browser محلی/آفلاین، متصل به hash HTML و recipe؛ نه محصول، دستگاه واقعی یا review مستقل |
| `MP_SOURCE_INVENTORY.json` | مسیرهای ۱۷ feature عضو، صفحه‌ها/testها و ۸۰ مسیر مرجع کارت‌ها که در tree pin وجود داشتند؛ نه ادعای نبود هر فایل جدید یا parity کامل |
| `mp-api-routes.snapshot.json` | ۱۴۱ مسیر و ۱۶۳ operation export‌شده؛ metadata guards/roles/scope، نه enforce شدن واقعی RBAC |
| `MP_API_OPERATIONS.csv` | نمای قابل‌جست‌وجوی همان operations برای crosswalk؛ endpoint جدید یا قرارداد OpenAPI نیست |
| `github-tool-catalog.json` | metadata منابع رسمی و مجوز/commit در 2026-11-24، از بررسی v1 حفظ‌شده؛ حضور ابزارهای اختیاری/تاریخی یعنی install plan نیست |
| `npm-tool-catalog.json` | root versions/engines/license/integrity برای ابزارهای منتخب و renderer؛ lock integrity با بررسی امنیت/مجوز کامل برابر نیست |
| `python-tool-catalog.json` | metadata اختیاری ابزار Python از بررسی هم‌تاریخ قبلی؛ اجرا/نصب این تحویل نیست |
| `binary-releases.json` | نام/version/URL release assets، نه binary همراه بسته یا hash تأییدشدهٔ دانلود؛ بخش OpenHands و k6/OSV صرفاً تاریخی/اختیاری |

نام snapshot مجوز: [LICENSE](LICENSE.source.txt). بقیه از `SOURCE_MANIFEST.json` به نام دقیق و لینک pin قابل پیگیری‌اند.

## یافته‌های کلیدی و منبعشان

- D-01…D-11: `docs/MuscleParadise/architecture/finn-loop-microtask-backlog-draft-v1-2026-11-23.md` **خطوط 68–78**؛ تعریف ۹ حوزه/وضعیت‌ها در ابتدای همان draft است. بازیابی متن به معنی تصویب پیش‌نویس یا پاسخ مالک نیست.
- Finn: `docs/MuscleParadise/FINN_LOOP.md` قانون G4 سقف ۳ تلاش برای همان خطا دارد؛ AGENTS فعلی، تاریخی‌بودن بخش‌های ECC و ممنوعیت roleplay/subagent جعلی را روشن می‌کند. ۹۰ دقیقه در این بسته پیشنهاد است، نه numeric runtime contractِ منبع.
- React foundation: `mp-app/studio/package.json`، `src/App.tsx` و `src/lib/roleNav.ts`؛ member در `STUDIO_ROLES` داخل `src/auth/AuthContext.tsx` نیست.
- session: `src/lib/session.ts` tokenها را در localStorage می‌گذارد و مرز XSS را تصریح می‌کند؛ این مشاهده مجوز ذخیرهٔ امن یا مهاجرت خودکار نیست.
- PWA: `public/manifest.webmanifest`، `public/sw.js`، `tests/pwa.test.ts`؛ نصب/update/cache واقعی با browser در این کار آزموده نشده‌اند. منبع SW نشان‌دهندهٔ gap method/cache-ownership است، نه گزارش exploit اجراشده.
- deployment config: `nginx.conf` / `Dockerfile` / `vite.config.ts`؛ SPA fallback و API proxy وجود دارند؛ staging اجرا نشده است.
- API/roles: `backend/security/rbac.py`، `app/security/route_policy.py` و export کاتالوگ؛ همچنان شش نقش جاری، نه target سه‌نقشی مصوب.
- پرداخت: `PLAN-MANUAL-TRANSFER.md` و سایر قراردادهای جاری باید با `OWNER-DECISIONS` مقصد reconcile شوند؛ submit≠بانک و تطبیق انسانی مستقل، private receipt و display-only shop از مرزهای این طرح‌اند.
- CI: `.github/workflows/ci.yml` و `web.yml`؛ Studio/backend/security/native jobs و Flutter Web وجود دارند. بعضی مراحل diagnostics non-blocking هستند؛ موفقیت واقعی فقط از exit/count و required checks همان SHA نتیجه می‌شود.
- `tools/graphviz-renderer/package.json`: ابزار doc موجود MP با Viz 3.31.0/Sharp 0.35.5؛ renderer این handoff هم‌خانواده است و dependency محصول نیست.

## source plan و source code دو مرجع متفاوت‌اند

[SOURCE_PLAN.fa.md](../SOURCE_PLAN.fa.md) رونویسی جدول‌های پیام کاربر، مرجع **خواسته و مرز پذیرش ۵۰ کارت** است؛ snapshotهای MP مرجع **مشاهدهٔ static کد** هستند. اگر رفتار Flutter فعلی checkout سفارش دارد ولی طرح جدید shop را نمایش‌محور محدود کرده، parity به معنی روشن‌کردن checkout نیست؛ تفاوت باید به‌عنوان تصمیم/scope ثبت شود. هیچ جدول/نمودار به‌تنهایی proof of readiness نیست.
