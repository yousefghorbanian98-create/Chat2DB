# شواهد یک کارت — گزارش پالایش‌شده، متصل به revision

## provenance

- task / parent / AC IDs / قرارداد و spec approval:
- repository / branch مجاز / base SHA / head SHA / patch hash (اگر dirty):
- cwd / sandbox / OS/device/browser/نسخه ابزار / زمان UTC / fixture مصنوعی:
- code pin آزموده‌شده و artifact hash؛ CI run/check/artifact IDs:
- دادهٔ واقعی، token، cookie، receipt، health، chat و secret نباید در خروجی بیایند.

## فرمان‌های واقعاً اجراشده

| # | cwd / exact command | نسخه | start/end UTC / attempt | exit | count/pass/fail/skip | artifact پالایش‌شده + hash | نتیجه |
|---|---|---|---|---:|---|---|---|
| 1 | تکمیل شود؛ این سطر نمونه است | UNKNOWN | NOT_RUN | — | NOT_RUN | NOT_RUN | NOT_RUN |

فرمان اجرا‌نشده را در جدول اجرای واقعی قرار نده؛ در بخش «نشد/چرا/اثر» بیاور. ساخت موفق build لزوماً اجرای تست نیست؛ صفر تست و suite skipped قبولی نیست. mock-only contract با API runtime، emulation با دستگاه و screenshot با persistence یکسان نیستند.

## نتیجهٔ تک‌تک ACها

| AC source → فرزند | رفتار مثبت/منفی | مشاهدهٔ UI و server | reload/version/ownership | evidence exact SHA | نتیجه |
|---|---|---|---|---|---|
| تکمیل شود | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN | NOT_RUN |

## نه حوزهٔ قرارداد — جداگانه

| gate | نتیجه | evidence / finding / owner |
|---|---|---|
| G1-spec | NOT_RUN | |
| G2-isolation | NOT_RUN | |
| G3-tool-scope | NOT_RUN | |
| G4-tests-security | NOT_RUN | |
| G5-branch-protection | NOT_RUN | |
| G6-evidence | NOT_RUN | |
| G7-human-approval | NOT_RUN | |
| G8-budget | NOT_RUN | |
| G9-adversarial-review | NOT_RUN | |

## پنج گیت دامنه‌ای — جداگانه

| domain | نتیجه | evidence / finding / تأیید N/A اگر واقعاً نامرتبط |
|---|---|---|
| security | NOT_RUN | |
| privacy | NOT_RUN | |
| finance | NOT_RUN | |
| legal | NOT_RUN | |
| product | NOT_RUN | |

## budget و توقف

سقف مصوب/منبع: total attempts ≤3 (initial+2 retries)، دقیقهٔ wall-clock مصوب، هزینه/فراخوانی/egress عددی؛ مصرف هر F/I/N/N؛ fingerprint و علت retry؛ stop یا escalation اگر سقف/secret/scope نقض شد. ۹۰ دقیقهٔ پیشنهادی را بدون approval «مصوب» ننویس.

## review و تصمیم انسان

- reviewer واقعاً مستقل / نقش ابزار یا انسان / context / reviewed final head SHA:
- adversarial prompt/scope/role/ownership/egress tests و findings unresolved/resolved:
- self-review یا checklist عامل اصلی جدا نام‌گذاری شود؛ اجرای subagent جعل نشود.
- owner approval با SHA / human merge decision / merge commit / branch protection evidence:
- اگر head تغییر کرد، evidence/check/review اثرگرفته دوباره اجرا/ثبت شوند.
- NOT_RUNها، UNKNOWNها، خطر باقیمانده، D/taskهای BLOCKED و اقدام امن بعدی:
- وضعیت نهایی کارت و بازشدن dependency فقط بعد از merge واقعی در baseline مصوب.

**این فایل در بسته template است؛ همهٔ خانه‌های نمونه NOT_RUN هستند و هیچ تأیید یا QA واقعی را نشان نمی‌دهند.**
