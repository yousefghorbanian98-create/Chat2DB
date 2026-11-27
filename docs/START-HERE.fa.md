# از اینجا شروع کن — دستور کار بیلدر Muscle Paradise

> این تنها فایلی است که لازم داری. همهٔ فایل‌های دیگر از همین‌جا لینک شده‌اند.
> تاریخ: ۲۰۲۶-۱۱-۲۷ UTC · همهٔ لینک‌ها روی `arena/c1fb460b-chat2db` تست و با
> SHA-256 تأیید شده‌اند (فایل روی گیت‌هاب = فایل محلی).

---

## بخش ۱ — وضعیت واقعی امروز (قبل از هر کاری این را بدان)

| چیز | وضعیت واقعی (بررسی‌شده روی گیت‌هاب) |
|---|---|
| شاخهٔ `arena/5e0f64cf-mp` | **مرده** — PR #29 merge شد و در `main` ادغام شد |
| `main` | `3527810` — commit «PWA: Add shared Studio routing and release hardening (#29)» |
| PR باز | صفر |
| `evidence/` روی `main` | فقط `evidence/m60/` — هیچ `INV-02`/`INV-03` وجود ندارد |
| کار crosswalk نشست قبل | **از بین رفته** — commit نشده بود، در هیچ ریموتی نیست |
| نرخ شکست push/PR بیلدر | بالا — `gh pr create` احتمالاً خطای permission می‌دهد |

**نتیجه:** بیلدر نباید روی `arena/5e0f64cf-mp` کار کند. شاخهٔ کار = شاخهٔ نشست خودش از `origin/main`.

---

## بخش ۲ — سه فایلی که باید دانلود کنی

| # | فایل | برای چه کسی | حجم |
|---|---|---|---|
| ۱ | [MP-BUILDER-PROMPT-COPY.txt](https://github.com/yousefghorbanian98-create/Chat2DB/raw/arena/c1fb460b-chat2db/docs/MP-BUILDER-PROMPT-COPY.txt) | **به بیلدر بده** — پرامپت اصلی حلقهٔ ساخت PWA | ۱۷ KB |
| ۲ | [INV-REDO-PROMPT-COPY.txt](https://github.com/yousefghorbanian98-create/Chat2DB/raw/arena/c1fb460b-chat2db/docs/mp-inv-redo/INV-REDO-PROMPT-COPY.txt) | **به بیلدر بده** — پاکت نجات INV-02/INV-03 | ۹ KB |
| ۳ | [INV-REDO-BOOTSTRAP.fa.md](https://github.com/yousefghorbanian98-create/Chat2DB/raw/arena/c1fb460b-chat2db/docs/mp-inv-redo/INV-REDO-BOOTSTRAP.fa.md) | **برای خودت** — توضیح فارسی چرا و چگونه | ۷ KB |

اگر لینک `raw` در مرورگر باز شد و ذخیره نکرد: راست‌کلیک روی لینک → *Save link as…*
اگر باز هم نشد، صفحهٔ فایل را باز کن و دکمهٔ **Download raw file** را بزن:
- <https://github.com/yousefghorbanian98-create/Chat2DB/blob/arena/c1fb460b-chat2db/docs/MP-BUILDER-PROMPT-COPY.txt>
- <https://github.com/yousefghorbanian98-create/Chat2DB/blob/arena/c1fb460b-chat2db/docs/mp-inv-redo/INV-REDO-PROMPT-COPY.txt>

ابزارهای INV-02/03 (اگر بیلدر خواست خودش دانلود کند):

| فایل | لینک |
|---|---|
| `inv02_member_crosswalk.py` | [دانلود](https://github.com/yousefghorbanian98-create/Chat2DB/raw/arena/c1fb460b-chat2db/docs/mp-inv-redo/inv02_member_crosswalk.py) |
| `inv03_staff_crosswalk.py` | [دانلود](https://github.com/yousefghorbanian98-create/Chat2DB/raw/arena/c1fb460b-chat2db/docs/mp-inv-redo/inv03_staff_crosswalk.py) |
| `run-inv-redo.sh` | [دانلود](https://github.com/yousefghorbanian98-create/Chat2DB/raw/arena/c1fb460b-chat2db/docs/mp-inv-redo/run-inv-redo.sh) |

---

## بخش ۳ — دستور کار: دقیقاً چه بکنی

### قدم ۰ — قبل از هر چیز، بیلدر فعلی را ببند
اگر بیلدر الان وسط کاری است، **اول بگذار STATE را بنویسد و push کند**، بعد پرامپت جدید بده.
اگر کارش گیر کرده یا مرده، اول این را بفرست:

```
اگر کاری نیمه‌تمام داری: STATE را بنویس، commit کن و push کن. بعد بگو تمام شد.
هیچ کار جدیدی شروع نکن تا من پرامپت بعدی را بدهم.
```

### قدم ۱ — پرامپت اصلی را بده
محتوای فایل ۱ (`MP-BUILDER-PROMPT-COPY.txt`) را کامل کپی کن و در چت بیلدر پیست کن.
بالای آن این دو خط را اضافه کن:

```
این یک نشست جدید است. شاخهٔ arena/5e0f64cf-mp مرده (merge شده در PR #29).
شاخهٔ کار خودت را از origin/main بساز و روی آن push کن. روی main commit نکن.
```

### قدم ۲ — منتظر اولین چرخه بمان
بیلدر باید بدون سؤال شروع کند و در پایان چرخهٔ اول گزارش بدهد:
`DONE / DIFF / گیت‌ها / NEXT`. اگر سؤال «ادامه بدهم؟» پرسید، یعنی پرامپت را کامل نخوانده — همان را دوباره بفرست.

### قدم ۳ — پاکت نجات را بده (فقط بعد از اینکه چرخهٔ اول push شد)
فایل ۲ (`INV-REDO-PROMPT-COPY.txt`) را بده. اولش نوشته‌شده که روی کار نیمه‌تمام اجرا نشود.
بالای آن این را اضافه کن:

```
پرامپت قبلی را ادامه بده و STATE را از نو نساز.
این پاکت فقط برای INV-02 و INV-03 است.
```

### قدم ۴ — بعد از هر چرخه فقط یک خط بفرست
```
CONTINUE-LOOP(MP): از STATE ادامه بده. بدون مقدمه، کار بعدی را انتخاب کن و تا شرایط توقف بند ۱۴ پیوسته اجرا کن.
```

### قدم ۵ — تنها دلیلی که خودت باید وارد شوی
| اگر بیلدر گفت | یعنی | کار تو |
|---|---|---|
| «این فقط با تصمیم مالک جلو می‌رود» | یکی از ۶ تصمیم OWNER-DECISIONS | یک تصمیم یک‌خطی بده |
| «صف محلی تمام شد» | همهٔ کارهای قابل ساخت تمام شده | بلاکرها را ببین، تصمیم بگیر |
| «push رد شد» | مشکل دسترسی یا شاخه | بگو شاخهٔ درست چیست |
| هر چیز دیگر | کار عادی | فقط «ادامه» بفرست |

---

## بخش ۴ — چه چیزی را هرگز باور نکن (چک‌لیست خودت)

این‌ها را بیلدر گفته و درست نبود؛ هر بار خودت چک کن:

- [ ] `HEAD=<sha>` گفت → بپرس `git ls-remote origin | head` خروجی‌اش چیست. اگر SHA در ریموت نبود، کارش از بین رفته.
- [ ] «فایل در `evidence/...` هست» → روی گیت‌هاب بگرد. اگر نبود، نیست.
- [ ] «CI سبز است» → بپرس روی کدام SHA. CI روی SHA دیگر شاهد نیست.
- [ ] «۲۱ ردیف crosswalk آماده است» → بپرس `meta.dirty` چه بود. اگر dirty بود، خروجی به کد نسبت داده نمی‌شود.
- [ ] «PASS شد» → بپرس خروجی خام دستور کجاست.

---

## بخش ۵ — چرا این‌ها را ساختم (یک پاراگراف)

پرامپت اول جلوی «بی‌وقفه ادامه بده» را می‌گیرد و از سؤال بی‌مورد جلوگیری می‌کند.
پاکت دوم جلوی «کار از دست رفت» را می‌گیرد: هر شاهد با اسکریپت از روی SHA بازتولید می‌شود، پس اگر نشست مرد، فقط دوباره اجرا می‌شود.
و این فایل جلوی «چه کنم؟» را می‌گیرد.
