# LOOP D — پوستهٔ Tauri (چهار نسخه)
## ۲۲ تسک · ~۳ هفته · وابسته به LOOP A

**هدف:** از Electron ۸۴MB به چهار باینری Tauri (~۱۰MB هرکدام) از **یک** کدپایه.

---

## ⚠️ دو واقعیت که باید قبل از شروع بدانید

**۱. پلاگین‌های `barcode-scanner` و `biometric` فقط Android/iOS هستند — روی دسکتاپ وجود ندارند.**
کیوسک شما دسکتاپ است. پس اسکن QR روی دسکتاپ باید با `getUserMedia` در خود WebView
انجام شود، یا با **اسکنر سخت‌افزاری USB** (که برای کیوسک واقعی بهتر و سریع‌تر است).

**۲. ساخت Rust کندتر از باندل JS است.** انتظار CI را تنظیم کنید (~۴ دقیقه به‌جای ~۲).

---

# فاز D0 — نمونهٔ آزمایشی (تسک ۰۱–۰۳) 🔬

> **این فاز قبل از هر تعهدی انجام می‌شود.** اگر شکست خورد، Electron می‌ماند و
> تصمیم دوباره بررسی می‌شود. ریسک را زود کشف کنید، نه بعد از دو هفته.

## D-01 · نصب زنجیرهٔ ابزار
Rust · `tauri-cli` · Android SDK/NDK · `cargo-ndk`.
**verify:** `cargo tauri --version && rustc --version` → exit 0

## D-02 · اسکلت Tauri با UI موجود
`mp-app/shell/` — `npm run build` فعلی را به‌عنوان `frontendDist` بدهید.
هیچ تغییری در `src/` ندهید.
**verify:** `cargo tauri build --debug` → باینری اجرا می‌شود و UI فعلی را نشان می‌دهد

## D-03 · اثبات ساخت اندروید
**verify:** `cargo tauri android build --debug` → APK تولید شود
> اگر D-01…D-03 شکست خورد → **توقف**، ثبت در `ERRORS.log`، مشورت با کاربر.

---

# فاز D1 — پیکربندی چهار هدف (تسک ۰۴–۰۹)

## D-04 · چهار پیکربندی Tauri
```
shell/tauri.admin.desktop.conf.json    → index.html  + sidecar هسته
shell/tauri.admin.android.conf.json    → index.html  (کلاینت نازک)
shell/tauri.client.desktop.conf.json   → client.html
shell/tauri.client.android.conf.json   → client.html
```
شناسه‌های جدا: `app.muscleparadise.admin` / `.client`

## D-05 · قابلیت‌های حداقلی (least privilege)
`shell/capabilities/` — **مهم‌ترین مزیت امنیتی Tauri v2**.
- ادمین دسکتاپ: fs (محدود به پوشهٔ داده) · shell (فقط sidecar) · updater
- کلاینت: **بدون fs** · بدون shell · فقط http به LAN + barcode-scanner (اندروید)

⚠️ اپ کلاینت نباید هیچ دسترسی فایل‌سیستمی داشته باشد. اگر دارد، اشتباه است.

## D-06 · هسته به‌عنوان sidecar (فقط ادمین دسکتاپ)
Python + هسته را با PyInstaller بسته‌بندی و به‌عنوان sidecar اجرا کنید.
مدیریت چرخهٔ عمر: بالا آمدن، سلامت، **توقف مؤدبانه** (checkpoint شدن WAL).

## D-07 · کشف سرور روی LAN (سه اپ دیگر)
اولین اجرا: ورود دستی آدرس **یا** کشف mDNS.
⚠️ **اعتبارسنجی ورودی:** فقط `http(s)` + host. (همان اشتباهی که در وب‌هوک بود.)

## D-08 · CSP سخت در Tauri
`connect-src` فقط به هستهٔ پیکربندی‌شده.

## D-09 · به‌روزرسان امضاشدهٔ Tauri
`tauri-plugin-updater` با کلید عمومی. **بدون تأیید امضا فعال نشود** (B-21).

---

# فاز D2 — قابلیت‌های بومی (تسک ۱۰–۱۵)

## D-10 · اسکن QR روی اندروید
`tauri-plugin-barcode-scanner`.

## D-11 · اسکن QR روی دسکتاپ
`getUserMedia` + `BarcodeDetector` با fallback به `jsQR`.
**دلیل:** پلاگین روی دسکتاپ وجود ندارد.

## D-12 · Face ID / اثر انگشت برای قفل‌گشایی اپ 🆕
`tauri-plugin-biometric` (فقط اندروید).
⚠️ **این با تشخیص چهرهٔ کیوسک فرق دارد.** اینجا گوشیِ خودِ ورزشکار او را تأیید می‌کند؛
داده هرگز از Secure Enclave خارج نمی‌شود؛ **صفر ریسک GDPR**.
همیشه fallback به PIN داشته باشید.

## D-13 · ذخیرهٔ امن توکن
`tauri-plugin-stronghold` یا keychain سیستم — نه `localStorage`.

## D-14 · اعلان‌های محلی
یادآوری انقضای عضویت (بدون PHI در متن اعلان).

## D-15 · تفکیک ادمین/کلاینت در زمان ساخت
`import.meta.env.VITE_MP_EDITION` = `admin` | `client`.
کد ادمین **نباید** در باندل کلاینت باشد (tree-shake).
**verify:** `! grep -r "adminOnlySecret" dist-client/`

---

# فاز D3 — ساخت و بسته‌بندی (تسک ۱۶–۲۲)

## D-16 · نصب‌کنندهٔ ویندوز ادمین (NSIS/MSI)
**هدف: < ۱۵ MB** (اکنون ۸۴ MB با Electron)

## D-17 · نصب‌کنندهٔ ویندوز کلاینت

## D-18 · APK **release امضاشده** ادمین
🔴 انتشار فعلی `app-debug.apk` است: کلید عمومی دیباگ + `debuggable=true`
(هرکسی با ADB می‌تواند توکن بخواند).
keystore در GitHub Secrets · `minifyEnabled` · امضای واقعی.

## D-19 · APK release امضاشده کلاینت

## D-20 · `network_security_config.xml`
cleartext فقط برای `192.168.0.0/16` و `10.0.0.0/8` — نه همه‌جا.
روی Wi-Fi عمومی، توکن ورزشکار نباید متن ساده برود.

## D-21 · سرویس ویندوز برای هسته
NSSM یا Task Scheduler — بدون پنجرهٔ CMD باز · شروع خودکار · چرخش لاگ.

## D-22 · گردش‌کار CI ساخت
`.github/workflows/mp-tauri-build.yml` — چهار هدف + SHA256SUMS.

---

# معیار خروج LOOP D
```
□ ۲۲ تسک DONE
□ چهار نصب‌کننده ساخته می‌شوند
□ نصب‌کنندهٔ ویندوز < ۱۵ MB
□ APKها release و امضاشده (نه debug)
□ اپ کلاینت هیچ دسترسی fs ندارد
□ اسکن QR روی اندروید و دسکتاپ کار می‌کند
□ به‌روزرسان امضا را تأیید می‌کند
□ cleartext فقط روی بازهٔ خصوصی
□ ادمین دسکتاپ بدون سرور جداگانه بالا می‌آید (sidecar)
```
**عدد:** `نصب‌کننده: ۸۴ MB → < ۱۵ MB` · `نسخه‌ها: ۱ → ۴`
