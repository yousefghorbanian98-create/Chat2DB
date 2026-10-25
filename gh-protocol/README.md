# Gh Protocol — v1.0.0

**همیشه متصل. — Stay connected.**

[![Release v1.0.0](https://img.shields.io/badge/release-v1.0.0-34d399)](https://github.com/yousefghorbanian98-create/Chat2DB/releases/tag/gh-protocol-v1.0.0)
[![Xray-core v26.10.21](https://img.shields.io/badge/Xray--core-v26.10.21-22d3ee)](https://github.com/XTLS/Xray-core/releases/tag/v26.10.21)
[![Finn-Loop Gates](https://img.shields.io/badge/Finn--Loop-G0..G5%20PASSED-818cf8)](./QUALITY_GATES.md)

**Gh Protocol** یک کلاینت اندروید متن‌باز، بدون نیاز به سرور شخصی و بدون تله‌متری برای حفظ ارتباط در شبکه‌های محدود است. این برنامه اشتراک رسمی **Serverless-for-Iran** (و لینک‌های `vless://` / `trojan://`) را همراه با فرگمنت TLS و اسکنر IP تمیز روی هستهٔ رسمی **Xray-core v26.10.21** در قالب یک تونل بومی `VpnService` با یک تپ اجرا می‌کند.

---

## دانلود و نصب در ۳ گام (۳-Step Quick Start)

1. **دانلود و نصب APK:**
   - **[دانلود مستقیم `GhProtocol-v1.0.0-arm64-v8a.apk` (~۲۲ مگابایت — پیشنهادی برای تمام گوشی‌های اندروید)](https://github.com/yousefghorbanian98-create/Chat2DB/releases/download/gh-protocol-v1.0.0/GhProtocol-v1.0.0-arm64-v8a.apk)**
   - **[دانلود مستقیم `GhProtocol-v1.0.0-universal.apk` (نسخهٔ جامع arm64 + x86_64)](https://github.com/yousefghorbanian98-create/Chat2DB/releases/download/gh-protocol-v1.0.0/GhProtocol-v1.0.0-universal.apk)**
   - **[فایل هش `SHA256SUMS`](https://github.com/yousefghorbanian98-create/Chat2DB/releases/download/gh-protocol-v1.0.0/SHA256SUMS)** | **[گزارش جامع `FINAL_REPORT.html`](./FINAL_REPORT.html)**
2. **اتصال با یک کلیک:** برنامه را باز کنید و روی دکمهٔ بزرگ **«اتصال»** بزنید؛ در اولین اجرا مجوز سیستمی VPN اندروید را تایید کنید.
3. **ابزارهای بازیابی در زمان اختلال شدید:**
   - **اسکنر IP تمیز (F-17):** یافتن سریع‌ترین IP کلودفلر با هندشیک واقعی TLS 1.2 روی اپراتور فعلی شما.
   - **وارد کردن کانفیگ دلخواه (F-16):** پشتیبانی از لینک‌های `vless://`، `trojan://` و JSON با تزریق خودکار TLS Fragmentation.
   - **آماده‌سازی برای قطعی (F-13):** ذخیرهٔ آفلاین آخرین اشتراک سالم و بررسی سلامت هسته.

---

> ## مرزهای صادقانهٔ عملکرد (Honest Positioning)
> **Gh Protocol** شانس اتصال شما را در شرایط عادی، اختلال شدید DPI، مسدودسازی SNI و محدودیت UDP به حداکثر می‌رساند. اما در صورت **قطع کامل ارتباط بین‌المللی در دروازهٔ ملی (National Gateway Forwarding-Plane Cutoff)**، هیچ نرم‌افزار سمت کلاینتی قادر به ایجاد اتصال بین‌المللی نیست. برنامه این وضعیت را از طریق کاوشگر شبکه تشخیص داده و صادقانه نمایش می‌دهد.

---

## معماری فنی (v1.0.0)

```
User Tap ──> Compose UI (RTL / Vazirmatn / MotionSpec <=300ms)
         ──> HomeViewModel + SubscriptionRepository (Primary + Mirror + Embedded Fallback)
         ──> ConfigPatcher (vless/trojan/JSON + TLS Fragment + Clean IP + Single Outbound)
         ──> VpnTunnelService (TUN 10.8.0.2/24 + IPv6 fd00:1::1/128 Leak Guard)
              ├─> UDP :53 ──> Dokodemo-door :15353 ──> Xray dns-out (Cloudflare DoH)
              └─> TCP SYN/Data (RFC 793) ──> SOCKS5 :10808 ──> Xray-core v26.10.21
```

## وضعیت قابلیت‌ها (F-1 تا F-18)

| کد | قابلیت | وضعیت |
|----|--------|-------|
| F-1..F-10 | اتصال یک‌کلیکی، Xray-core 26.10.21، تونل VPN، پینگ واقعی، آپدیت خودکار، QR، لاگ ماسک‌شده، تم تیره/روشن، فارسی/انگلیسی | ✅ v1.0.0 |
| F-11..F-15 | تشخیص صادقانهٔ قطعی، بقای آفلاین، آماده‌سازی پیش از قطعی، راهنمای اتصال جایگزین، تطبیق خودکار پروتکل (TCP-first) | ✅ v1.0.0 |
| F-16..F-18 | مبدل هوشمند `vless://` و `trojan://` با فرگمنت، اسکنر IP تمیز با هندشیک TLS، بالانسر هوشمند با چرخش خودکار | ✅ v1.0.0 |

## بررسی اصالت فایل (SHA-256 & Signature)

```bash
sha256sum -c SHA256SUMS
apksigner verify --verbose --print-certs GhProtocol-v1.0.0-arm64-v8a.apk
```

## مجوز (License)

MIT (کد کلاینت Gh Protocol) + MPL-2.0 (باینری رسمی Xray-core از پروژهٔ XTLS).
