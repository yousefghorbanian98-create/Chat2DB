# توضیح بازطراحی ترکیبی (Hybrid) — Cutting Edge v0.9.34

> تصویر: `REDESIGN_7_HYBRID_STUDIO.png`
> تاریخ: 2026-08-27
> فلسفه: ۹۰٪ Minimal Pro + ۹٪ Cyberpunk + ۱٪ Glassmorphism

---

## چرا ترکیب، نه یک سبک واحد؟

اگر همه چیز Cyberpunk باشد → خسته‌کننده برای استفاده طولانی، چشم خسته می‌شود.
اگر همه چیز Minimal باشد → هیچ شخصیتی، مثل ۱۰۰ SaaS دیگر.
اگر همه چیز Glass باشد → سنگین، کُند، شلوغ.

**جواب:** هر سبک را در جایی که بهترین است، استفاده کن.

---

## قانون توزیع (۹۰-۹-۱)

### ۹۰٪ — Minimal Pro (پایه، همه‌جا)
- پس‌زمینه، سایدبارها، timeline، toolbar
- رنگ: مشکی خالص + متن سفید در opacity‌های مختلف
- هیچ glow، هیچ gradient
- **وظیفه:** خوانایی، حرفه‌ای بودن، استفاده طولانی بدون خستگی

**المان‌های Minimal Pro در تصویر:**
- کل صفحه (پس‌زمینه `#0A0A0F`)
- تایم‌لاین (۳ لاین، کلیپ‌ها)
- Toolbar
- Sidebar چپ و راست
- فرم‌ها در Inspector

### ۹٪ — Cyberpunk (لحظات ویژه)
- فقط جایی که «جادو» یا «action» در جریان است
- **وظیفه:** شخصیت، هیجان، نشان دادن AI/playhead

**المان‌های Cyberpunk در تصویر:**

| المان | چرا Cyberpunk؟ |
|-------|---------------|
| **Playhead** (خط عمودی صورتی با glow) | مهم‌ترین المان تایم‌لاین — باید دیده شود |
| **Scoreboard "0.83 → USED"** (با ★ و رنگ صورتی) | لحظه‌ی تصمیم AI = جادو |
| **Progress bars** در task dock (نئونی) | نشان‌دهنده‌ی progress فعال |
| **Export button** (با border صورتی نئونی) | CTA اصلی، باید متمایز باشد |
| **REC ● dot** (در monitor) | فقط این یک نقطه قرمز، نه کل UI |
| **Beat grid** (خط‌چین نئونی زرد) | دیتای تکنیکال، باید دیده شود |

**نکته کلیدی:** همه‌ی این‌ها accent هستند، نه پایه. هر کدام **یک رنگ** دارند، نه چند رنگ.

### ۱٪ — Glassmorphism (المان‌های شناور)
- فقط المان‌هایی که **روی محتوای دیگر شناورند**
- **وظیفه:** عمق، جداسازی بصری، حس «این یک لایه‌ی دیگر است»

**المان‌های Glass در تصویر:**

| المان | چرا Glass؟ |
|-------|-----------|
| **Task dock** (پایین، ۶۰px ارتفاع) | روی timeline شناور است، باید جدا به نظر برسد |
| **AI Assistant FAB** (پایین-راست، دایره) | entry point، نیاز به عمق |
| **⌘K command hint** (نبود، حذف شد) | — |

**نکته کلیدی:** Glass **هرگز** container اصلی نمی‌شود. فقط overlay/floating.

---

## قوانین طلایی (که باید رعایت شود)

### قانون ۱: «Accent نباید گریه کند»
اگر یک المان Cyberpunk است، باید **کاملاً** Cyberpunk باشد. نیمه‌نیمه = هرج‌ومرج.
- ❌ Border نئونی ۵۰٪ opacity + بدون glow
- ✅ Border نئونی ۱۰۰٪ + glow ۴px

### قانون ۲: «Glass فقط شناور»
اگر یک المان Glass است، باید **روی چیز دیگری** باشد. اگر container اصلی Glass شود، همه چیز «روی چیزی شناور» به نظر می‌رسد و حس hierarchy از بین می‌رود.
- ❌ Sidebar = Glass
- ✅ Sidebar = Solid `#0F0F14` + Task dock = Glass

### قانون ۳: «Minimal یعنی هوا»
اگر یک المان Minimal است، باید **حداکثر ۱۰٪ المان‌های صفحه** را اشغال کند. تراکم در Minimal = شلوغی.
- ❌ ۲۰ المان در یک sidebar
- ✅ ۵ المان، با ۲۴px gap بینشان

### قانون ۴: «هر رنگ یک وظیفه»
| رنگ | وظیفه | کجا |
|-----|-------|-----|
| سفید (کامل) | متن اصلی | همه‌جا |
| سفید (۷۰٪) | متن ثانویه | labels، توضیحات |
| سفید (۴۰٪) | متن سوم | metadata |
| سفید (۲۰٪) | جداکننده | borders، disabled |
| `#FF2D9C` صورتی | action، primary accent | playhead، export، AI |
| `#00F0FF` فیروزه‌ای | info، data | scoreboard، progress |
| `#10F0A0` سبز | success، online | checkmarks، status |
| `#FFB800` زرد | warning، grid | beat grid، pending |

**هیچ‌وقت** دو المان هم‌جنس هم‌رنگ نباشند مگر در یک گروه معنایی.

### قانون ۵: «Typography می‌گوید چه چیزی مهم است»
- **Mono (JetBrains Mono):** هر عدد، هر timecode، هر ID، هر size
- **Inter Medium:** هر عنوان، هر button
- **Inter Regular:** هر توضیح، هر label

اگر عددی با Inter نشان داده شود، کاربر آن را «متن» می‌بیند نه «داده».

---

## فایل‌های مرتبط

| فایل | توضیح |
|------|------|
| `REDESIGN_7_HYBRID_STUDIO.png` | تصویر اصلی ترکیب (Studio page) |
| `REDESIGN_LAUNCHER_CYBERPUNK.png` | Launcher ۱۰۰٪ Cyberpunk |
| `REDESIGN_2_STYLEMATCH_GLASSMORPHISM.png` | Style Match ۱۰۰٪ Glass |
| `REDESIGN_6_STYLEMATCH_MINIMAL.png` | Style Match ۱۰۰٪ Minimal |
| `REDESIGN_COMPARISON.md` | مقایسه‌ی ۶ سبک جدا |
| `REVIEW_AND_REDESIGN.md` | بررسی کد + ایده + تم‌ها |

---

## پیشنهاد اجرا (اگر می‌خواهی شروع کنی)

### مرحله ۱: تم Minimal Pro (۳ روز)
- همه‌ی CSS variables را تعریف کن
- ۹۰٪ UI بدون تغییر باقی می‌ماند
- چیز جدید: opacity‌های متن استاندارد، hairline borders، Inter Medium

### مرحله ۲: اضافه کردن Cyberpunk accent (۲ روز)
- فقط ۵ المان بالا را عوض کن (playhead, scoreboard, progress, export, REC)
- CSS variables جدید: `--neon-pink`, `--neon-cyan`, `--neon-green`, `--neon-amber`
- box-shadow با alpha کم

### مرحله ۳: Glass task dock (۱ روز)
- فقط `.ce-running` (که الان در CSS هست) را به `rgba(255,255,255,0.06) + backdrop-filter: blur(20px)` تبدیل کن
- AI Assistant FAB نیز Glass

**جمع: ۶ روز کار، صفر خط JS، ~۳۰۰ خط CSS.**

---

**ساخته شده توسط Arena Agent** — بررسی مستقیم کد در `/home/user/Chat2DB/ce-app/`.
