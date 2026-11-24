# چک‌لیست انتشار (M31) — Release Checklist

## الف) کیفیت (همه سبز = شرط انتشار)
- [x] pytest: ۱۸۲+ تست سبز (`mp-app/backend`)
- [x] ruff: صفر خطا
- [x] semgrep: صفر یافته (قوانین python)
- [x] Locust: بدون 5xx در دود بار (آخرین: M30 ۵۰ کاربر)
- [x] مانور بکاپ/بازیابی سبز (`test_backup_drill.py`)
- [x] مهاجرت‌ها: `alembic upgrade head` روی DB تمیز (M23/M27 تأییدشده)

## الف-۱) قفل استقرار production — این موارد پیش از ورود دادهٔ واقعی باید سبز شوند
- [ ] کلید signing افشاشده rotate/revoke و مسیر به‌روزرسانی کاربران تأیید شد؛ حذف فایل از HEAD کافی نیست.
- [ ] Gitleaks MIT CLI روی کل history اجرا شد؛ findings قرمز و بدون baseline/allowlist پنهان شدند.
- [ ] `.env` production با کلید JWT و کلید بیومتریک مجزای ۳۲ بایتی، CORS/TLS و secret manager آماده است.
- [ ] SMS provider واقعی/HTTPS و live payment merchant/sandbox policy عملیاتی تأیید شدند؛ OTP توسعه و gateway mock در production ممنوع‌اند.
- [ ] Valkey production سالم، `/api/v1/health/ready` سبز و rate-limit storage مشترک بین workerها تأیید شد.
- [ ] migration `alembic upgrade head` روی دیتابیس scratch از صفر و روی clone امنِ backup اجرا شد؛ duplicate gateway authorityها پیش از upgrade بررسی شدند.
- [ ] backup صحیح از `/data/mp.db` ساخته، restore drill انجام و نسخهٔ رمزگذاری‌شده خارج از همان میزبان نگهداری شد.
- [ ] Prometheus/exporter/alert rules دیده شدند و Alertmanager/receiver با test notification تنظیم شد.
- [ ] Registry push/Dokploy deploy/rollback روی staging واقعاً تمرین و نتیجه ثبت شد؛ هیچ deploy خودکار از این شاخه انجام نشده است.

> موارد بالا وضعیت عملیاتی‌اند؛ Compose/API تغییرکرده به‌تنهایی معادل secret، merchant، DNS/TLS، host inventory، backup offsite یا staging verification نیست.

## الف-۲) بازبینی REA پیش از هر تگ (M45 — از ۲۰۲۶-۱۱-۱۵ اجباری)
- [ ] `rea identify-flutter-build <apk>` — هش Dart snapshot + نسخهٔ engine ثبت شد
- [ ] `rea inspect-apk-signature <apk>` — طرح‌های v1/v2/v3 و اثر انگشت گواهی ثبت شد
- [ ] `rea audit-release-exposure <apk>` — هیچ source map / debug symbol / credential marker افشا نشد
- [ ] `versionName` در APK با تگ ریلیز هم‌خوان است (خواندن مانیفست دودویی)
- [ ] `INTERNET` و `networkSecurityConfig` در مانیفست **release** موجودند (نه فقط debug)
- [ ] `android:debuggable="false"` صریحاً در مانیفست است (observation، نه inference)
- [ ] `ApiClient` فقط loopback/RFC1918 را با HTTP می‌پذیرد (تست‌های `api_client_test.dart` سبز)
- [ ] گزارش تأیید در `finn/reports/rea/<date>-REA-GAP-CLOSURE.md` نوشته شد

## الف-۳) وضعیت شاخه‌ها در زمان ارائه
- [ ] `git ls-remote --heads origin` فقط `main` را نشان می‌دهد (به‌جز شاخهٔ فعالِ همان لحظه، اگر نشستی در جریان است).
- [ ] هر شاخهٔ مرج‌شده از `origin` حذف شده است؛ برای محتوای مرجع فقط تگ `archive/*` مانده.
- [ ] `main` آخرین merge را با CI سبز روی همان SHA دارد و worktree محلی تمیز است.
- [ ] روی GitHub گزینهٔ «Automatically delete head branches» روشن است (فقط مالک می‌تواند).

## ب) انطباق
- [x] E07: هیچ معادلهٔ بدون منبع اجرا نمی‌شود (`equations.py` — قفل فعال)
- [x] E10: نگهداری/حذف مستند (DATA-RETENTION.md)
- [x] حریم خصوصی بیومتریک نسخه‌دار + API (faceid-privacy-1.0)
- [x] گزارش محرمانه: نام واقعی فقط نسخهٔ داخلی، هویت مستعار در REA
- [x] دادهٔ واقعی در Git/dev/test/logs نیست

## ج) محصول
- [x] هر دکمه/خروجی → خروجی واقعی (OUTPUT-AUDIT-2026-11-14.md)
- [x] مسیرهای گیت‌شده (population) با خطای صریح متوقف می‌شوند
- [x] خروجی گزارش: HTML چاپی + JSON (D-020)
- [x] RTL/فارسی + جزئیات میکرو (DESIGN.md)
- [x] APK اندروید: ساخت debug در CI با جاب `client-pinned` (`ci.yml`) (**توجه:** `apk.yml` با AD‑21 در ۲۰۲۶‑۱۱‑۲۲ حذف شد؛ گیت Android اکنون جاب `client-pinned` در `ci.yml` است) — ساخت امضاشدهٔ release دیگر workflow جداگانه ندارد

## د) عملیات
- [x] ران‌بوک عملیات (OPS-RUNBOOK.md)
- [x] دلتا-انتشار مستند (بدون حذف‌نصب)
- [x] فهرست تحویل + SHA256 (handoff zip در Git)

## هشدارهای پابرجا (نه مانع انتشار)
- محدودیت‌های سندباکس (D-002/003/004/007/008/013/015): ماتریس وضعیت در HANDOFF-ANALYSIS-2026-11-14.md
- کلاس خصوصی پیشرفته (B-11): طراحی‌شده، پیاده‌سازی به‌ازای دادهٔ واقعی مشتری
- Face-ID عمیق (ArcFace): پشت قفل مدل تا تأمین وزن/اجازه
