# نمونه‌های پیکربندی — هنوز فعال یا کامل نیستند

این نمونه‌ها **گیت اجراشده یا تأیید امنیت نیستند**. در PWA-01/02 باید مطابق مسیر مصوب، alias، entrypoint، generator و قواعد backend تنظیم و با fixture مثبت/منفی واقعاً تست شوند. آن‌ها را برای رسیدن به عدد سبز ضعیف نکن.

- `dependency-cruiser.cjs.example`: نمونهٔ بدون چرخه، بدون core module نود در browser و مرز featureها. پس از پذیرش مسیر در ریشهٔ PWA با نام `.dependency-cruiser.cjs` تنظیم شود. entrypoint/tsconfig واقعی باید موجود باشد. import مشترک را از shared/services انجام بده، نه با کپی‌کردن featureها.
- `semgrep-pwa.example.yml`: فقط یک policy آغازین برای URL loopback در source مرورگر؛ هیچ ادعایی دربارهٔ پوشش کامل SAST، XSS، مجوز یا پول ندارد. در source comments/fixture ممکن است نیاز به triage محدود داشته باشد؛ blanket ignore نکن.
- `puppeteer.example.json`: مسیر browser را محلی تنظیم کن. پیش‌فرض sandbox فعال می‌ماند؛ افزودن `--no-sandbox` فقط در محیط ایزوله با تصمیم ریسک، نه در production و نه به عنوان راه‌حل عمومی.

Knip باید entrypointهای HTML/Vite/SW و فایل تولیدی را بشناسد؛ Playwright باید `baseURL` واقعی staging/preview و account fixture مصنوعی داشته باشد. عمداً configی با `tests: []` یا ignore همهٔ src نساخته‌ایم تا صفر تست/صفر یافته به اسم PASS تحویل نشود.

این فایل‌ها اصل تازهٔ RBAC، schema، retention، مبلغ یا اختیار owner ایجاد نمی‌کنند.
