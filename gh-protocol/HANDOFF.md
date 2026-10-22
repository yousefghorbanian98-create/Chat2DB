# Gh Protocol — سند جامع وضعیت و راه‌اندازی (HANDOFF)

**تاریخ:** ۳۰ مهر ۴۰۵ (2026-10-22) · **وضعیت: G0 سبز ✅** — P0 در زیرمجلد `gh-protocol/` همین ریپوی (Chat2DB) build می‌شود و سبز است · **باقی‌مانده:** دسترسی نوشتن GitHub-App به ریپوی جدا `gh-protocol` برای مهاجرت نهایی (کاربر ارور موقتی GitHub در Arena را گزارش داد؛ بعد از رفع، reconnect/افزودن app)

> این سند برای «بقا» نوشته شده: اگر workspace پاک شود و تنها چیزی که مانده باشد همین ریپوی باشد،
> با خواندن این فایل + فایل‌های همین پوشه، کل پروژه به‌طور کامل بازسازی و ادامه می‌شود.

---

## ۱. پروژه چیست

**Gh Protocol** — کلاینت اندروید متن‌باز برای «همیشه متصل ماندن» در شبکه‌های محدود (ایران).
یک تپ، صفر کانفیگ، صفر تله‌متری. هسته: **Xray-core رسمی (XTLS، MPL-2.0)** + کانفیگ رسمی
**Serverless-for-Iran** (subscription: `https://raw.githubusercontent.com/patterniha/Serverless-for-Iran/refs/heads/main/Subscription/Serverless-for-Iran.json#Patterniha-S`)
داخل tunnel بومی `VpnService` (مدار: VpnService → tun2socks → Xray SOCKS5 `:10808`).

**معماری هدف:** Kotlin 2 + Jetpack Compose + Material 3، RTL-first، فونت Vazirmatn،
App ID `com.ghprotocol.app`، minSdk 26 / targetSdk 35، لایسنس MIT (خود اپ).

**پوزیشن‌گذاری صادقانه (قانون غیرقابل‌مذاکره محصول):**
اپ در وضعیت‌های **عادی / محدود / پلکانی** بیشترین احتمال اتصال ممکن را می‌دهد، ولی در **قطع کامل ملی**
(discard در forwarding-plane دروازه) **هیچ نرم‌افزاری** نمی‌تواند اتصال ایجاد کند — اپ این حالت را
تشخیص می‌دهد (F-11) و صادقانه گزارش می‌کند، نه وعده‌ی دروغ.

---

## ۲. وضعیت لحظه‌ای (چک‌لیست)

| آیتم | وضعیت |
|---|---|
| پلن تولید (v1.3) | ✅ کامل — `PRODUCTION_PLAN.md` در همین پوشه + نسخه‌ی زنده در workspace: `/home/user/serverless-android/PRODUCTION_PLAN.md` |
| اپ HTML یک‌کلیک (deliverable اول) | ✅ `/home/user/serverless-iran/index.html` (53,204 B) + `lib/qrcode.js` — سرویس پیش‌نمایش: `python3 -m http.server 8321 --bind 0.0.0.0` در cwd آن پوشه |
| اسکلت P0 (32 فایل) | ✅ کامل در workspace: `/home/user/gh-protocol` (git commit محلی `72ba997` روی بوش `main`) + **کپی این پوشه** |
| Keystore release | ✅ تولیدشده (EC P-256، 25 ساله، alias `ghprotocol`) — فایل‌ها: `/home/user/.ghprotocol-keystore.b64` و `/home/user/.ghprotocol-keystore-pass` (⚠️ خارج از Git — اگر پاک شدند، بخش ۷ روش بازسازی را اجرا کنید؛ چون هنوز release‌ای امضا نشده، بازسازی **بدون هیچ هزینه‌ای** است) |
| ریپوی `gh-protocol` (جدا) | ✅ ساخته‌شده توسط کاربر (public، خالی) — منتظر مهاجرت |
| Push به `gh-protocol` (جدا) | ❌ مسدود — app فقط read دارد (403). بعد از reconnect/افزودن app با write، مهاجرت = یک commit |
| **build واقعی (P0)** | ✅ **در `Chat2DB/gh-protocol/`** — workflow ریشه: `.github/workflows/gh-protocol.yml` (paths-filtered) · run سبز: [39834413232](https://github.com/yousefghorbanian98-create/Chat2DB/actions/runs/39834413232) (4m22s) |
| **Release** | ✅ [`gh-protocol-P0-test`](https://github.com/yousefghorbanian98-create/Chat2DB/releases/tag/gh-protocol-P0-test) با artifact `apk-p0` (15.5 MB: دو APK + SHA256SUMS) |
| امضای release در CI | ⚠️ **ephemeral keystore به‌ازای هر run** (app دسترسی secrets هم ندارد — 403)؛ به‌محض set شدن `KEYSTORE_PKCS12`+`KEYSTORE_PASS` در Secrets، خودکار به کلید دائمی سوییچ می‌کند |
| لاگ‌های CI از داخل sandbox | ⚠️ results-receiver و blob.core.windows.net در allowlist شبکه‌ی sandbox نیستند → لاگ از طریق بوش خودکار `ci-diag` (step شکست، tail لاگ gradle را آنجا commit می‌کند) |

**تک‌گلوئی فعلی:** فقط «دسترسی نوشتن+secrets به ریپوی جدا gh-protocol» — و این فقط برای **مهاجرت نهایی و کلید دائمی** است؛ ساخت و تست هر روز از همین‌جا خودکار ادامه دارد (بخش ۶).

---

## ۳. محتوای این پوشه (بازسازی کامل)

```
gh-protocol-skeleton/
├── HANDOFF.md                ← این سند
├── PRODUCTION_PLAN.md        ← پلن تولید v1.3 (منبع حقiquel؛ فارسی)
├── DESIGN.md                 ← توکن‌های طراحی v0.1 (M3)
├── LICENSE                   ← MIT (+ قید MPL-2.0 برای Xray-core)
├── README.md                 ← README ریپوی (با بخش Honest positioning)
├── settings.gradle.kts / build.gradle.kts / gradle.properties
├── gradlew, gradlew.bat, gradle/wrapper/*   ← Gradle 8.10.2 wrapper کامل (jar + properties)
├── .github/workflows/build.yml              ← CI: build+test+sign+SHA256+artifact
└── app/                      ← ماژول اندروید
    ├── build.gradle.kts      ← AGP 8.7.3, Kotlin 2.0.21, Compose BOM 2024.12.01
    ├── src/main/AndroidManifest.xml          ← permissionهای نهایی + GhVpnService placeholder
    ├── src/main/java/com/ghprotocol/app/     ← MainActivity, ui/(HomeScreen+theme), service/
    ├── src/main/res/                               ← strings (en/fa), themes, adaptive icon, Vazirmatn (3 وزن)
    └── src/test/java/.../SkeletonTest.kt         ← smoke test
```

**نکته‌های فنی اسکلت:**
- امضای release: `build/keystore/release.keystore` در CI از Secrets decode می‌شود (اکشن `timheuer/base64-to-file`)؛ اگر secret نباشد، release روی signing debug می‌نشیند تا build سبز بماند.
- `.gitignore` پوشش می‌دهد: `build/keystore/` هرگز commit نمی‌شود.
- `GhVpnService` در P0 no-op است (سطح permission از روز اول قفل شده؛ پیاده‌سازی واقعی در P2/F-3).
- نسخه: `versionName "0.1.0-p0"`.

---

## ۴. پلن تولید (خلاصه‌ی قابل‌اجرا — مرجع کامل: PRODUCTION_PLAN.md)

### ۴.۱ قابلیت‌ها (F)

| # | قابلیت | فاز |
|---|---|---|
| F-1 | اتصال یک‌تپ (auto از subscription رسمی) | P1 |
| F-2 | بوت‌استرپ Xray-core (چک نسخه ≥ 26.6.27، arm64-v8a ≈20MB + SHA-256) | P2 |
| F-3 | VpnService یک‌تپ (mixed `:10808`) | P2 |
| F-4 | قطع/اتصال < ۳ ثانیه + آیکون status bar درست | P1 |
| F-5 | آفلاین اولیه + پیام فارسی + تلاش مجدد | P1 |
| F-6 | به‌روزرسانی خودکار کانفیگ (WorkManager ۱۲h) + **mirror لینک subscription در GitHub (failover)** | P2 |
| F-7 | QR + Share subscription | P1 |
| F-8 | راهنمای فارسی (پورت ۱۰۰۸، جئو، IPv6، Private DNS) | P1 |
| F-9 | RTL کامل + Material 3 + Vazirmatn + WCAG AA | P1 |
| F-10 | حریم خصوصی: صفر تله‌متری؛ فقط `INTERNET`+`VPN` | P1 |
| F-11 | **تشخیص قطعی + وضعیت صادقانه** (probe هر ۱۵ دقیقه، ping در سطح Xray-core؛ ۳ حالت) | P1 |
| F-12 | **بقای آفلاین** + auto-sync کانفیگ در چند ثانیه پس از بازگشت | P1 |
| F-13 | «آماده‌سازی برای قطعی» (کش کانفیگ/هسته + پیش‌دانلود محتوا) | P2 |
| F-14 | راهنمای اتصال جایگزین (اطلاعاتی): اینترنت‌پرو، سیم/رومینگ، ماهواره+ریسک، ابزارهای مکمل | P1 |
| F-15 | تجویز پروتکل (UDP-drop → TCP-first، مثل اکتبر ۲۰۲۶) | P2 |
| F-16 | امبر هر کانفیگ معتبر دلخواه (URL/QR/متن/فایل؛ + لینک‌های خام vless:// و trojan:// با تبدیل خودکار + fragment + address override — الگوی Simorgh) | P2 |
| F-17 | **اسکنر IP تمیز** (dirty-IP recovery: پینگ واقعی Xray روی IPهای Cloudflare per-ISP؛ فقط آدرس عوض، SNI/Host/Path دست‌نخورده) | P2 |
| F-18 | **بالانسر هوشمند** (انتخاب خودکار کم‌latency + rotate خودکار در مرگ route) | P2 |

**Non-goals:** iOS/دسکتوپ (NG-1) · اکانت/کلود (NG-2) · Google Play (NG-3) · **MitM/Domain Fronting** (NG-4) · تغییر پورت ۱۰۸۰۸ (NG-5) · تبلیغ/پرداخت/ردیابی (NG-6).

### ۴.۲ کیفیت

- **DoD (14 مورد):** ACs سبز در CI · ktlint/Detekt/Lint صفر · پوشش ≥70٪ · golden 12 صفحه×2تم (Roborazzi) · Strix صفر High/Critical + mobsfscan · امضای release v1+v2 + zipalign · حجم arm64 ≤25MB · چرخه‌ی نصب→اتصال ویدیوگرفته · Release با SHA-256+راهنمای فارسی+نسخه هسته · decision log · dependency freeze · گزارش نهایی · بلک‌اوت‌رزیستنس (F-11/12/15) · F-17/18 + crash guard raceها.
- **حلقه‌ی Finn-loop:** finn-spec → finn-build (1 issue/PR، ≤1 agent-day) → finn-review؛ ۲ شکست = خُردکردن issue؛ A-1..A-4 (merge خودکار فقط با سبز بودن PR، rollback خودکار).
- **گیت‌ها:** G0 (اسکلت سبز) → G1 (P1 همراه) → G2 (P2 هسته) → G3 (P3 پرداخت/موشن) → G4 (P4 امنیت: Strix+MobSF+MASVS) → G5 (Release با DoD کامل).
- **فازها:** P0: 2 issue/8 چرخه · P1: 9/28 · P2: 12/48 · P3: 4/15 · P4: 2/8 · P5: 2/2 → **جمع 31 issue ≈ 118 چرخه**.

### ۴.۳ تصمیمات کلیدی (D)

D-1 ریپوی `gh-protocol` (public، جدا از Chat2DB) · D-4 v1 بدون بک‌اند (DockPloy برای v1.1) · D-6 لایسنس MIT · D-7 **نام Gh Protocol / App ID `com.ghprotocol.app`** (تأیید کاربر) · D-8 F-Droid در v1.1 · D-9 **bootstrap خودکار keystore در GitHub Secrets** (رمزنگاری با public-key ریپوی؛ کلید هرگز خارج از GitHub).

### ۴.۴ ریسک‌های اصلی

R-11 (GPL بودن v2rayNG → فقط مرجع معماری؛ مرجع کدی MIT: LionRayVPN + hev-socks5-tunnel) · R-12 (قطع کامل شبکه — احتمال بالا؛ اپ تضمین نمی‌کند، صادق می‌گوید: F-11..F-15 + F-14) · R-10 (اعتماد به APK sideload → checksum + امضا + صفحه‌ی امنیت + F-Droid).

### ۴.۵ منابع رایگان هر فاز (خلاصه)

Actions public = رایگان/نامحدود (4c/16GB) · gradle/actions (caching) · ReactiveCircus/android-emulator-runner · Roborazzi · Vazirmatn (OFL) · XTLS/Xray-core releases رسمی (SHA-256) · MobSF/mobsfscan · Context7 (1k call/ماه) · fastlane (MIT).

---

## ۵. یافته‌های پژوهشی (مبانی تصمیمات — همه راستی‌آزموده)

### ۵.۱ بلک‌اوت ۲۰۲۶

- **دو موج:** ۸–۲۸ ژانویه (اعتراضات) + ۲۸ فوریه – ۲۶ مه (جنگ) = **88 روز / 2093 ساعت** (رکورد تاریخ)؛ ترافیک به ۱–۴٪ عادی.
- **مکانیسم (هوشمندانه‌ترین قطعی تاریخ):** NOT BGP-withdrawal — 80–88٪ پیشفیکس‌ها announce ماندند؛ **packet discard در forwarding-plane دروازه ملی** + برداشتن 98.5٪ مسیرهای IPv6 + DNS poisoning + allowlist پروتکل. → در لایه IP «وصل» به نظر می‌رسید ولی هیچ بسته‌ای عبور نمی‌کرد.
- **نتیجه:** در قطع کامل **هیچ client-side** (VPN/Serverless/Tor) کار نکرد (NYT: «VPNs stopped working»).
- **تنها ابزار مؤثر (ناقص):** Starlink (~50k ترمینال، رایگان) با GPS-jamming 30–80٪ + مصادره 40k+ ایستگاه + مجرمانه‌سازی (6 ماه–5 سال؛ با جاسوسی تا اعدام).
- **حالت «VPNهای گران‌قیمت» انتهای قطعی:** کریدورهای **egress مجازرسانی‌شده توسط دولت** (اینترنت‌پرو/سیم‌سفید) که واسطه‌ها 10–50x گران‌تر می‌فروختند (گزارشات 300 هزار تا 7 میلیون تومان/GB) — هیچ ترفند فنی نبود.
- **وضعیت 22 اکتبر ۲۰۲:** اینترنت باز ولی عمداً افت‌خورده: throttle + **drop UDP** (از 9 اکتبر) + قطعی‌های چنداستانی (16 اکتبر) + تهدید سپاه به قطع 7 کابل زیردریایی هرمز (19–20 اکتبر) + ادامه‌ی جنگ (روز 231) + ترافیک ≈75٪ زیر سطح قبل‌ازجنگ.

### ۵.۲ حکم «تضمین» (صادقانه)

| وضعیت | اپ | دلیل |
|---|---|---|
| عادی (DPI/whitelist) | ✅ target طراحی | خردشدن TCP/TLS + دورزدن fingerprint |
| افت‌خورده (وضعیت فعلی) | ✅ با F-15/F-17/F-18 | تا یک مسیر بین‌المللی باز باشد |
| قطع کامل | ❌ هیچ نرم‌افزاری نمی‌تواند | بسته از کشور خارج نمی‌شود؛ فقط سخت‌افزار |

### ۵.۳ مسیرهای بسته‌شده (چک فنی انجام‌شده — دوباره باز نکنید)

- **«فریب با .ir به‌جای دامنه‌های خارجی»:** routing بر پایه‌ی prefix مقصد IP است نه نام دامنه؛ TLD `.ir` خود زیر کنترل دولت است (nic.ir + DNS ملی)؛ SNI=.ir روی IP خارجی = ناسازگاری گواهی + heuristic DPI؛ تنها شکل ممکن mirror داخلی = فقط محتوای کش‌شده (همان F-12). **تحت هیچ شرایطی برای سرویس زنده شدنی نیست.**
- **Sوار مخفیانه‌ی کریدورهای اینترنت‌پرو:** metered + identity-linked؛ خارج از چارچوب = کشف‌پذیر + جریمه (جرایم سایبری) → خارج از scope.
- **Domain fronting کلاسیک:** مرده (Google 2018، AWS، Azure ژانویه 2024) → NG-4 تایید.
- **ECH:** در ایران default مرده — ایران DNS رمزنگاری‌شده‌ی bootstrap آن را سانسور می‌کند (PETS 2025)؛ 99.99٪ deployments = Cloudflare.

### ۵.۴ تکنیک‌های زنده ۲۰۲۶ (مورث fronting — پذیرفته شد)

**Clean-IP recovery + SNI-keep + fragmentation + route-balancing.** دو پروژه‌ی مستقل روی آن هم‌گرایی کرده‌اند:
- **Nova Radar** (IRNova/Nova-Proxy): اسکن سریع‌ترین IPهای تمیز Cloudflare per-ISP + اعمال per-user؛ mirror subscription در GitHub؛ لینک مختلط VLESS+Trojan. (لایسنس از 4.3.0: PolyForm Noncommercial — فقط مرجع معماری.)
- **Simorgh** (rezakhosh78/SIMORGH، Xray 26.6.27 = target ما، همین subscription Patterniha را می‌خواند): balancer با ping واقعی Xray (3x) + rotate خودکار؛ Fragment (vless/trojan → JSON + fragment + address override)؛ MSP (route روی IP تمیز در شرایط degraded/outage)؛ crash guard raceها؛ حذف اپ از tunnel خودش.
- **Mahsa NG** (GFW-knocker/MahsaNG، GPL — فقط مرجع): rotating configs، per-subnet feedback، ضد-بازفروش کانفیگ، Mahsa-Core (Noise/WARP/Youtube-Direct).
- **Defyx VPN** (UnboundTechCo، Flutter/MT + DXcore بسته): failover خودکار چندموتوره (Warp/Psiphon/Xray/Outline) + Deep Scan؛ در بلک‌اوت روی Psiphon/Conduit P2P سوئیچ کرد؛ الگوی v1.1 ما. آنتی‌الگو: هسته‌ی بسته.

### ۵.۵ منابع اصلی

Wikipedia: 2026_Internet_blackout_in_Iran · arXiv 2603.28753 و 2605.00187 (مکانیسم) · PETS 2025 (ECH) · NetBlocks/IODA/Kentik · NYT 2026-03-18 · Reuters 2026-04-28 · Al Jazeera 2026-05-14 · Bloomberg (iran-internet) · GitHub: GFW-knocker/MahsaNG، IRNova/Nova-Proxy، UnboundTechCo/defyxVPN، rezakhosh78/SIMORGH.

---

## ۶. راهنمای اجرا (دقیق، قدم‌به‌قدم)

**وضعیت کنونی (بعد از G0):** build روزمره در `Chat2DB/gh-protocol/` است و سبز؛ دو کاربرد برای ریپوی جدا `gh-protocol` باقی است: (الف) کلید دائمی (secrets) و (ب) هویت مستقل محصول. هر دو بعد از برقراری دسترسی نوشتن+secrets انجام می‌شود:

**پیش‌نیاز:** کاربر اتصال GitHub در Arena را reconnect کرده (یا app را روی `gh-protocol` با دسترسی نوشتن نصب کرده). تست سریع:
```bash
cd /home/user/gh-protocol   # یا کپی این پوشه
gh api /repos/yousefghorbanian98-create/gh-protocol/contents/.probe -X PUT -f message=p -f content=$(echo -n x|base64) -f branch=main
# موفق = path برمی‌گردد؛ شکست = 403 «Resource not accessible by integration»
```

### قدم ۱ — push
```bash
cd /home/user/gh-protocol
git remote set-url origin https://x-access-token:$(gh auth token)@github.com/yousefghorbanian98-create/gh-protocol.git
git push -u origin main
```
(اگر `/home/user/gh-protocol` پاک شده بود: `cp -r /home/user/Chat2DB/gh-protocol-skeleton /home/user/gh-protocol && cd /home/user/gh-protocol && rm PRODUCTION_PLAN.md && git init -b main && git add -A && git commit -m "P0: Gh Protocol skeleton"`)

### قدم ۲ — Secrets (bootstrap keystore — D-9)
نام‌های secret (دقیقاً همین): `KEYSTORE_PKCS12` (محتوای base64 از `/home/user/.ghprotocol-keystore.b64`) و `KEYSTORE_PASS` (محتوای `/home/user/.ghprotocol-keystore-pass`).
```bash
# با /tmp/genv/bin/python (cryptography+PyNaCl) — اگر گنو پاک شده:
#   python3 -m venv /tmp/genv && /tmp/genv/bin/pip install cryptography pynacl
/tmp/genv/bin/python - <<'PY'
import base64, nacl.secret
key = base64.b64decode("$(gh api /repos/yousefghorbanian98-create/gh-protocol/actions/secrets/public-key --jq .key)")
box = nacl.secret.SecretBox(nacl.public.Key(base64.b64decode("$(gh api /repos/yousefghorbanian98-create/gh-protocol/actions/secrets/public-key --jq .key)")))
for name, path in (("KEYSTORE_PKCS12","/home/user/.ghprotocol-keystore.b64"), ("KEYSTORE_PASS","/home/user/.ghprotocol-keystore-pass")):
    val = open(path).read().strip()
    enc = box.encrypt(val.encode()).decode()
    open(f"/tmp/secret_{name}.json","w").write(f'{{"encrypted_value":"{enc}","key_id":"$(gh api /repos/yousefghorbanian98-create/gh-protocol/actions/secrets/public-key --jq .key_id)"}}')
    print(name, "ready")
PY
gh api /repos/yousefghorbanian98-create/gh-protocol/actions/secrets/KEYSTORE_PKCS12 -X PUT --input /tmp/secret_KEYSTORE_PKCS12.json
gh api /repos/yousefghorbanian98-create/gh-protocol/actions/secrets/KEYSTORE_PASS -X PUT --input /tmp/secret_KEYSTORE_PASS.json
```
(نکته: متن بالا الگوست — مقادیر `$(...)` را قبل از اجرا resolve کنید یا یک اسکریپت یک‌پارچه بنویسید؛ من در زمان اجرا اسکریپت تمیز می‌نویسم.)

### قدم ۳ — CI
```bash
gh run list -R yousefghorbanian98-create/gh-protocol -L3
gh run watch <run-id> -R yousefghorbanian98-create/gh-protocol   # یا poll هر ۳۰ ثانیه
# اگر شکست: gh run view --log-failed؛ debug و fix و push دوباره (حلقه‌ی خودکار — معمولاً 1-2 دور)
```

### قدم ۴ — بستن G0
- [ ] workflow سبز (build debug+release + test)
- [ ] artifact `apk-p0` موجود: `gh run download <id> -R ... -n apk-p0 -o /tmp/apk`
- [ ] Release-test: `gh release create P0-test ... --notes "G0: signed skeleton APK"` + `SHA256SUMS`
- [ ] گزارش به کاربر

### مسیر جایگزین (اگر دسترسی نوشتن برنگشت)
اجرا داخل Chat2DB: ریپوی `gh-protocol` را ignore کنید؛ اسکلت را در `/home/user/Chat2DB/gh-protocol/` بریزید (همین کپی)، workflow با `paths: ['gh-protocol/**']` فیلتر شود، و push روی `arena/7324330b-chat2db`. (انحراف از D-1 — فقط اگر app تا چند روز دسترسی نگرفت.)

---

## ۷. Keystore (اگر پاک شد — بازسازی بدون هزینه)

چون هنوز هیچ release‌ای امضا نشده، بازسازی کلید جدید **هیچ مشکلی** ایجاد نمی‌کند:
```bash
python3 -m venv /tmp/genv && /tmp/genv/bin/pip install cryptography
/tmp/genv/bin/python - <<'PY'
import datetime, base64
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import pkcs12, BestAvailableEncryption
from cryptography import x509
from cryptography.x509.oid import NameOID
key = ec.generate_private_key(ec.SECP256R1())
name = x509.Name([x509.NameAttribute(NameOID.COUNTRY_NAME,"IR"),
  x509.NameAttribute(NameOID.ORGANIZATION_NAME,"Gh Protocol"),
  x509.NameAttribute(NameOID.COMMON_NAME,"Gh Protocol Release Key")])
now = datetime.datetime.now(datetime.timezone.utc)
cert = (x509.CertificateBuilder().subject_name(name).issuer_name(name)
  .public_key(key.public_key()).serial_number(x509.random_serial_number())
  .not_valid_before(now - datetime.timedelta(days=1))
  .not_valid_after(now + datetime.timedelta(days=365*25))
  .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
  .add_extension(x509.KeyUsage(digital_signature=True, content_commitment=False, key_encipherment=False,
    data_encipherment=False, key_agreement=False, key_cert_sign=False, crl_sign=False,
    encipher_only=False, decipher_only=False), critical=True)
  .sign(key, hashes.SHA256()))
pw = "ghprotocol-2026-release"   # یا یک گذرواژه‌ی دلخواه (در secret KEYSTORE_PASS می‌رود)
blob = pkcs12.serialize_key_and_certificates(b"ghprotocol", key, cert, None, BestAvailableEncryption(pw.encode()))
open("/home/user/.ghprotocol-keystore.b64","w").write(base64.b64encode(blob).decode())
open("/home/user/.ghprotocol-keystore-pass","w").write(pw)
print("keystore rebuilt OK")
PY
```
**امنیت:** محتوای keystore هرگز در هیچ ریپوی (حتی خصوصی) commit نشود — فقط در GitHub Actions Secrets. (دلیل: ریپوی Chat2DB public است.)

---

## ۸. نقشه‌ی راه بعد از G0

P1 (همراه): F-1,5,7,8,9,11,12,14 + golden (Roborazzi) + web-preview → G1
P2 (هسته): F-2,3,4,6,13,15,16,17,18 (اتصال واقعی روی emulator + تله‌متری شبکه) → G2
P3 (پرداخت): motion + onboarding + dependency freeze → G3
P4 (امنیت): Strix full + mobsfscan/MobSF + MASVS → G4
P5 (ریلیز): DoD 14/14 + Release + GitHub Pages + گزارش + ویدیو → G5
v1.1 (اختیاری): F-Droid + DockPloy backend + failover چندموتوره (الگوی Defyx)

**حالت اجرا:** Finn-loop Auto — حلقه‌ی خودکار spec→build→review؛ حاشیه‌ی خطا با خُردکردن issue و rollback خودکار؛ ورودی انسانی: صفر.

---

## ۹. منابع زنده در workspace (بهتر از هر سندی — اگر زنده‌اند)

- `/home/user/serverless-android/PRODUCTION_PLAN.md` — پلن v1.3 (منبع حقیقت پلن)
- `/home/user/serverless-iran/index.html` + `lib/qrcode.js` — اپ HTML یک‌کلیک
- `/home/user/gh-protocol/` — اسکلت با git محلی (commit `72ba997`)
- `/home/user/.ghprotocol-keystore.b64` + `/home/user/.ghprotocol-keystore-pass`
- **اگر reset خورده بود:** این پوشه (`Chat2DB/gh-protocol-skeleton/`) تنها منبع باقی‌مانده است؛ همه‌چیز از بخش‌های ۶ و ۷ بازسازی می‌شود.
