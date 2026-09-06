# 07 — DevOps، CI/CD و انتشار

---

## 1. وضعیت فعلی

| مورد | وضعیت |
|------|--------|
| CI ساخت نصب‌کننده | ✅ `mp-app/packaging/ci/mp-installers.yml` — ویندوز ۱:۴۲، اندروید ۰:۵۵ |
| نصب‌کنندهٔ ویندوز | ✅ NSIS با پوستهٔ Electron (~۸۴ MB) |
| نصب‌کنندهٔ اندروید | ⚠️ APK دیباگ، پوستهٔ WebView |
| اسکریپت نصب لینوکس/ویندوز | ✅ `install.sh` / `install.ps1` |
| SHA256SUMS | ✅ تولید می‌شود |
| **CI تست (pytest + gate)** | 🔴 **وجود ندارد** |
| اسکن امنیتی | 🔴 وجود ندارد |
| Lighthouse / a11y | 🔴 وجود ندارد |
| تست بار | 🔴 وجود ندارد |

**مهم‌ترین یافته:** CI فقط **می‌سازد**، **نمی‌سنجد**. یعنی یک PR که ۵۰ تست را بشکند،
همچنان نصب‌کنندهٔ سبز تولید می‌کند. این دقیقاً همان چیزی است که باعث شد باگ
تاریخ هارد-کدشدهٔ `useWorkoutLog.test.ts` هفته‌ها ناشناخته بماند.

---

## 2. خط لولهٔ هدف — چهار گردش کار

### 2.1 `ci.yml` — روی هر push و PR (باید < ۸ دقیقه بماند)

```yaml
name: CI
on: [push, pull_request]

jobs:
  backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: '3.11', cache: pip }
      # محیط خالی، فقط requirements.txt — این تنها اثبات درستی آن فایل است
      - run: pip install -r mp-app/backend/requirements.txt
      - run: cd mp-app/backend && pytest --override-ini="addopts=" -q --cov=app --cov-fail-under=85
      - run: cd mp-app/backend && python -m app.export_openapi --yaml > /tmp/o.yaml
      # اسپک نباید از کد عقب بماند
      - run: diff -u mp-app/openapi.yaml /tmp/o.yaml

  frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '22', cache: npm, cache-dependency-path: mp-app/studio/package-lock.json }
      - run: cd mp-app/studio && npm ci
      - run: cd mp-app/studio && npm run gate
      - run: cd mp-app/studio && node scripts/check-bundle-budget.mjs   # سند ۰۴ §۳

  migrations:
    steps:
      # up → down → up روی DB با داده — بدون این، بازگشت نسخه غیرممکن است
      - run: cd mp-app/backend && python -m app.migrations.roundtrip_check

  e2e:
    steps:
      - run: ./scripts/e2e-smoke.sh    # bootstrap → seed → uvicorn → curl → assert
```

`ci.yml` باید **بررسی الزامی (required check)** روی شاخهٔ اصلی باشد. بدون این، بقیه تزئین است.

### 2.2 `security.yml` — روزانه + روی PR

```yaml
- run: pip-audit -r mp-app/backend/requirements.txt --strict
- run: cd mp-app/studio && npm audit --audit-level=high
- run: bandit -q -r mp-app/backend/app
- uses: gitleaks/gitleaks-action@v2
- uses: github/codeql-action/analyze@v3   # python + javascript
```

### 2.3 `quality.yml` — شبانه (کند است، مسدودکنندهٔ PR نباشد)

```yaml
- Lighthouse CI روی build استاتیک   → perf ≥ 90، a11y ≥ 95
- @axe-core/cli روی هر مسیر         → 0 نقض critical
- k6 روی هستهٔ در حال اجرا           → P95 < اهداف سند ۰۱ §۳.۱
```
GitHub Actions مرورگر دارد — این سه مورد که در سندباکس محلی «مسدود» بودند،
در CI کاملاً شدنی‌اند. بهانه‌ای برای نداشتنشان نیست.

### 2.4 `release.yml` — روی تگ `v*`

```
۱. تمام دروازه‌های ci.yml باید سبز باشند (وگرنه توقف)
۲. ساخت ویندوز (NSIS)، اندروید (APK امضاشدهٔ release)، وب (tar.gz)
۳. تولید SHA256SUMS + امضای cosign
۴. تولید SBOM (CycloneDX) برای هر دو اکوسیستم
۵. استخراج بخش نسخه از CHANGELOG.md به‌عنوان یادداشت انتشار
۶. آپلود به GitHub Release
```

---

## 3. 🔴 APK دیباگ منتشر نکنید

`app-debug.apk` در انتشار v0.20.0 قرار دارد. مشکلات:
- با کلید دیباگ عمومی امضا شده — هرکسی می‌تواند نسخهٔ جعلی بسازد که به‌روزرسانی به نظر برسد؛
- `debuggable=true` یعنی هر کسی با ADB می‌تواند به فرایند وصل شود و توکن را بخواند؛
- قابل انتشار در Play Store نیست.

**اصلاح:** یک keystore بسازید، در GitHub Secrets بگذارید، و `assembleRelease` را
با `minifyEnabled` و امضای واقعی اجرا کنید. تا آن زمان، فایل را
`app-debug-UNSAFE.apk` نام‌گذاری کنید و در یادداشت انتشار هشدار بدهید.

---

## 4. نسخه‌بندی و CHANGELOG

- **SemVer** با معنای صریح برای این محصول:
  - `MAJOR` = شکستن قرارداد API یا مهاجرت غیرقابل‌بازگشت DB؛
  - `MINOR` = قابلیت جدید، سازگار؛
  - `PATCH` = رفع اشکال.
- یک منبع نسخه: `mp-app/studio/package.json` و `app/__init__.py` باید **از یک فایل**
  بخوانند. اکنون دو جا دستی نگهداری می‌شوند = واگرایی حتمی.
- CHANGELOG با **عدد اندازه‌گیری‌شده** در هر ورودی ✅ — این عادت را حفظ کنید.

---

## 5. استقرار

### 5.1 حالت اصلی: نصب روی PC باشگاه
یک فرایند، یک پورت (۸۷۵۱)، `MP_STATIC_DIR` پوستهٔ ساخته‌شده را سرو می‌کند.
در همین بازبینی آزموده شد: `GET /index.html → 200`، `GET /api/v1/... → JSON`. ✅

الزامات باقی‌مانده برای نصب واقعی:
- سرویس ویندوز (NSSM) تا بدون کاربر لاگین‌شده بالا بیاید؛
- قاعدهٔ فایروال فقط برای زیرشبکهٔ محلی؛
- به‌روزرسانی خودکار با **بررسی امضا** (اکنون `updater.py` امضا را verify نمی‌کند —
  یعنی مسیر به‌روزرسانی، مسیر نصب بدافزار است اگر DNS دستکاری شود).

### 5.2 حالت اختیاری: میزبانی متمرکز با Dokploy
برای باشگاه‌های چندشعبه‌ای که آگاهانه ابر می‌خواهند:
```
Traefik (TLS خودکار) → کانتینر MP core → حجم پایدار برای DB و پشتیبان
```
- تصویر چندمرحله‌ای، کاربر غیر-root، `HEALTHCHECK` روی `/api/v1/health`.
- **قانون:** این حالت هرگز پیش‌فرض نشود. C1/C2 (local-first، بدون هزینهٔ اجباری) اصل محصول است.
- اگر متمرکز شد، SQLite دیگر کافی نیست → Postgres (سند ۰۲ §۹).

---

## 6. عملیات روزمره برای مالک باشگاه

مالک باشگاه DevOps نیست. این‌ها باید **دکمه** باشند، نه دستور:

| کار | وضعیت |
|-----|--------|
| پشتیبان‌گیری دستی | ✅ API هست، دکمه لازم است |
| پشتیبان خودکار ساعتی | ❌ |
| بازیابی از فایل | ✅ API |
| دیدن فضای دیسک و سلامت | ❌ |
| به‌روزرسانی با یک کلیک | ⚠️ بدون تأیید امضا |
| صادرات همهٔ داده (CSV/JSON) | ❌ — برای «حق قابلیت انتقال داده» لازم است |

---

## 7. طرح بازگشت (Rollback)

اکنون **وجود ندارد**. اگر v0.21 روی PC مشتری خراب باشد:
1. مهاجرت `down` ندارد؛
2. نصب‌کنندهٔ نسخهٔ قبلی در دسترس است ولی DB جلو رفته؛
3. تنها راه: بازیابی پشتیبان (که خودکار گرفته نمی‌شود).

**الزام قبل از v1.0:** هر انتشار باید قبل از اعمال مهاجرت، **خودکار پشتیبان بگیرد**
و اگر مهاجرت شکست خورد، خودکار برگردد. این ۵۰ خط کد است و از یک فاجعهٔ داده جلوگیری می‌کند.
