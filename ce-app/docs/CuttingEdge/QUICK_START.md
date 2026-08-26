# Quick Reference — نقشه‌ی مهندسی Hybrid

> فایل اصلی: `docs/CuttingEdge/FULL_HYBRID_DESIGN_SYSTEM.md`
> این فایل یک خلاصه‌ی سریع است.

---

## 🎯 تصمیم

**Hybrid Design System** (نه Cyberpunk خالص، نه Minimal خالص):
- **۹۰٪ Minimal Pro** (همیشه، همه‌جا)
- **۹٪ Cyberpunk accent** (فقط ۵ المان)
- **۱٪ Glassmorphism** (فقط المان‌های شناور)

---

## 📁 فایل‌های آماده

### مستندات
- 📄 `FULL_HYBRID_DESIGN_SYSTEM.md` ← **همه چیز اینجاست** (نقشه‌ی کامل)
- 📄 `REVIEW_AND_REDESIGN.md` (آنالیز کد + ۱۲ دیباگ)
- 📄 `REDESIGN_COMPARISON.md` (مقایسه ۷ سبک)
- 📄 `REDESIGN_FINAL_COMPARISON.md` (Minimal vs Hybrid)
- 📄 `REDESIGN_7_HYBRID_EXPLAINED.md` (قوانین Hybrid)

### کد (آماده برای import، هیچ‌کدام فعلاً استفاده نمی‌شود)
- 💻 `frontend/src/styles/design-tokens.css` — CSS variables
- 💻 `frontend/src/editor/Scoreboard.tsx` — Component
- 💻 `frontend/src/lib/format.ts` — Helpers
- 💻 `frontend/src/pages/StyleMatchDemo.tsx` — مثال

### تصاویر (۱۸ عدد)
- 🖼 Launcher (3): Cyberpunk, Hybrid, ...
- 🖼 Studio (2): Cyberpunk, Hybrid
- 🖼 Style Match (7): ۵ سبک مختلف + ۲ Minimal + ۱ Hybrid
- 🖼 Settings (1): Minimal
- 🖼 Export Queue (1): Minimal
- 🖼 Export Complete (1): Hybrid
- 🖼 State Machine (1): Empty/Loading/Error/Success
- 🖼 Architecture (1): لایه‌های Hybrid
- 🖼 Brand Identity (1): wordmark, palette, typography

---

## ⚡ ۵ چیز کلیدی از سند اصلی

### 1️⃣ Design Tokens (فقط variables، بدون logic)
- **Foundation:** `--ce-bg: #0A0A0A`, `--ce-text: #FFFFFF`, `--ce-border: rgba(255,255,255,0.08)`
- **Cyberpunk:** `--ce-neon-pink: #FF2D9C`, `--ce-neon-cyan: #00F0FF`, `--ce-neon-green: #10F0A0`, `--ce-neon-amber: #FFB800`
- **Glass:** `--ce-glass-bg: rgba(255,255,255,0.05)`, `--ce-glass-blur: blur(20px)`
- **Spacing:** 4px grid (4, 8, 12, 16, 24, 32, 48, 64, 96)
- **Motion:** 200ms default, `cubic-bezier(0.22, 0.61, 0.36, 1)`

### 2️⃣ Typography
- **Inter** (sans, body, headings)
- **JetBrains Mono** (تمام اعداد، timecode، score، size)
- **Vazirmatn** (فارسی، خودکار)
- **4 سطح opacity:** 100%, 70%, 50%, 30%

### 3️⃣ فقط ۵ المان Cyberpunk
1. **Playhead** در Timeline (خط صورتی با glow)
2. **Score winner** در Style Match (امتیاز صورتی با ★)
3. **Export button** (border صورتی)
4. **Success moments** (export complete، دایره سبز با glow)
5. **Beat grid** در ruler (خط‌چین زرد)

### 4️⃣ فقط ۳ المان Glass
1. **Task Dock** (پایین)
2. **AI Assistant FAB** (پایین-راست)
3. **Share Card** (در Export Complete)

### 5️⃣ هر صفحه دقیقاً طراحی شده
- Launcher: minimal + ۲ cyberpunk dots + ۱ glass AI
- Studio: minimal + cyberpunk playhead + glass task dock
- Style Match: minimal + cyberpunk winner score + glass trace
- Settings: ۱۰۰٪ minimal
- Export Queue: minimal + cyberpunk progress bars
- Export Complete: minimal + cyberpunk success + glass share

---

## 🐛 ۱۲ دیباگ (از ابتدای جلسه)

| # | اولویت | مشکل | فایل |
|---|--------|------|------|
| A1 | P0 🔴 | WebSocket race + task leak | `backend/app/websocket/job_events.py` |
| A2 | P0 🔴 | pip install بدون timeout | `backend/core/runtime_packages.py` |
| A3 | P0 🔴 | SQLite thread-unsafe | `backend/app/database.py` |
| A4 | P0 🔴 | Path validation ندارد | ۱۲ router |
| A5 | P1 🟠 | Ollama warmup | `backend/core/brain/planners.py` |
| A6 | P1 🟠 | Timeline listener re-create | `frontend/src/editor/Timeline.tsx` |
| A7 | P1 🟠 | RAF در background tab | `frontend/src/editor/PreviewMonitor.tsx` |
| A8 | P1 🟠 | WS reconnect ساده | `frontend/src/api/websocket.ts` |
| A9 | P2 🟡 | Zustand selectors نادقیق | `frontend/src/editor/model.ts` |
| A10 | P2 🟡 | Logging ساخت‌یافته ندارد | همه‌جا |
| A11 | P2 🟡 | axios بدون interceptor | `frontend/src/api/client.ts` |
| A12 | P3 🟢 | Code smell جزئی | `Timeline.tsx:116` |

---

## 💡 ۱۰ ایده (از ابتدای جلسه)

| # | ایده | زمان | چرا خفن |
|---|------|------|---------|
| B1 | Director Mode (voice) | ۱ هفته | ترکیب ۲ feature موجود = ۱ جدید |
| B2 | Cut on Emotion (vit-fer) | ۲ هفته | on-device emotion detection |
| B3 | Multi-Cam Switcher | ۳ هفته | AI auto-cut |
| B4 | Beat-Synced Text Animations | ۱ هفته | TikTok-style captions |
| B5 | Export Recipe Marketplace | ۲ هفته | اکوسیستم می‌سازد |
| B6 | GPU Direct Path (NVENC) | ۱ روز | ۵-۱۰× سریع‌تر export |
| B7 | Smart Thumbnail Generator | ۱ هفته | YouTube Summary-like |
| B8 | Plugin System (VSCode-style) | ۳ هفته | نگهداری ۱۰× ساده‌تر |
| B9 | Performance HUD (F3) | ۲ روز | شفافیت برای کاربر حرفه‌ای |
| B10 | Director's Cut Review | ۱ هفته | implicit training data |

---

## 🗓️ نقشه‌ی راه

**فاز ۱ (1.0):** ۸ هفته
- A1-A4 (دیباگ بحرانی)
- Migration به Hybrid (C13)
- A5-A8 + B6

**فاز ۲ (1.1-1.5):** ۱۲ هفته
- B1, B4, B5, B7, B9, B10
- Multi-platform installers

**فاز ۳ (2.0):** ۲۴ هفته
- B2, B3, B8
- Collaboration features
- Mobile companion

---

## ❓ سؤال کلیدی

**قدم بعدی چیست؟**
1. شروع Migration به Hybrid (C13) — ۶ هفته
2. فقط Critical Bug Fixes (A1-A4) — ۲ هفته
3. صبر تا 1.0 و بعد
4. اول یک prototype کوچک (مثلاً فقط Scoreboard cyberpunk variant) — ۱ هفته

---

**فایل کامل:** `docs/CuttingEdge/FULL_HYBRID_DESIGN_SYSTEM.md`
**تاریخ:** 2026-08-27
**شاخه:** `arena/01a04055-chat2db`
**وضعیت:** هیچ تغییری در کد فعلی
