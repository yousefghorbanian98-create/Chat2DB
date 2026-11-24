# مثال config — نه گیت فعال یا کامل

- `dependency-cruiser.cjs` از `mp-app/studio/` اجرا می‌شود؛ فقط cycle و browser→Node/Electron نمونه است. ساختار فعلی `src/pages` است؛ feature-directory خیالی نساز. alias/plugin/dynamic imports و testهای مثبت/منفی لازم است تا gate قابل اعتماد شود.
- `knip.example.json` entryهای browser و Electron و testهای موجود را نمونه می‌دهد. URL `$schema` فقط metadata editor است، نه نیاز شبکه‌ای اجرای تحویل؛ در محیط بدون egress schema را دانلود/resolve نکن. auto-delete کد یا تضعیف کارهای native از نتیجهٔ knip مجاز نیست.
- `semgrep-pwa.example.yml` فقط URLهای loopback در browser را مثال می‌زند و هنوز روی MP validate نشده است؛ false-positive و coverage را بسنج. API باید relative و از proxy مجاز برود؛ browser کاربر به localhost sandbox دسترسی ندارد. loopback برای process محلی سرور ممکن است درست باشد؛ scope را با browser code محدود کن.
- Semgrep/rules فعلی MP و GitHub Actions اولویت دارند؛ این فایل‌ها جای گیت موجود یا security review را نمی‌گیرند. هیچ شرط نقش، ownership، پرداخت یا cache امن از این configها ثابت نمی‌شود.
- فایل config را بدون diff/قرارداد/مالکیت به root محصول کپی نکن و در dependency runtime نصب نکن.
