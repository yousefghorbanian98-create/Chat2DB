# قرارداد میکرولوپ / فرزند — پیش از AGENT-READY تکمیل شود

## هویت و دامنه

- task ID / parent از ۵۰ ردیف / source AC mapping:
- عنوان اصلی parent (بدون تغییر) / outcome کوچک این issue:
- repository / شاخهٔ مجاز جاری / base SHA / dirty patch hash:
- مشکل قابل‌مشاهده / class ریسک / class داده:
- مسیرهای allowlist موجود/جدید / مسیرهای محفوظ Flutter/Android/Electron:
- API operation دقیق (method + path از قرارداد جاری) / ownership/roles/grants:
- dependencies / D IDs مؤثر / تصمیم معتبر قبلی + منبع:
- وضعیت: PROPOSED | DECISION | BLOCKED | READY-FOR-OWNER | AGENT-READY

## AC و NG قابل‌آزمون

- AC-1 (Given/When/Then، شامل خروجی server و UI):
- AC-2 (دسترسی/مالکیت منفی):
- AC-3 (reload/persistence/version یا N/A مستدل):
- همهٔ ACهای parent که این فرزند پوشش می‌دهد؛ ACهای باقی‌مانده و ID فرزند دیگر:
- NG-1: اپ React دوم، حذف/خاموشی Flutter/Android/Electron، migration نقش/DB/tenant ضمنی ممنوع.
- NG-2: no API/PII/session/receipt/health offline cache/write مگر تصمیم جدا؛ PWA-3F پیش‌فرض BLOCKED.
- NG-3: no live money/checkout/medical claim/LLM numeric planning/production/egress بدون مجوز.

## کنترل آغاز نه حوزهٔ Finn — برای همین issue

| gate | قرارداد پیش از اجرا | شاهد پایان / نتیجه (ابتدا NOT_RUN) |
|---|---|---|
| G1-spec | AC/NG خرد و parent mapping، spec owner | NOT_RUN |
| G2-isolation | cwd/sandbox، fixture مصنوعی، secret/network policy | NOT_RUN |
| G3-tool-scope | فرمان/مسیر مجاز؛ اثرهای بیرونی ممنوع/صریح | NOT_RUN |
| G4-tests-security | test IDs/commands/cwd/count/threshold و baseline | NOT_RUN |
| G5-branch-protection | PR target، required checks/rules، no bypass | NOT_RUN |
| G6-evidence | base/head/patch SHA، CI/artifact/version/redaction | NOT_RUN |
| G7-human-approval | spec approved by/date؛ merger تعیین‌شده | NOT_RUN |
| G8-budget | تلاش/زمان/هزینه/egress عددی و stop rule | NOT_RUN |
| G9-adversarial-review | reviewer مستقل واقعی و prompt/ownership/scope attack cases | NOT_RUN |

## پنج gate دامنه‌ای — هرکدام مستقل

| domain | ریسک/آزمون/تصمیم مرتبط | نتیجه و evidence |
|---|---|---|
| security | server authorization/ownership، OTP/session/QR، SW method/origin | NOT_RUN |
| privacy | receipt/chat/health/token، cache/log/trace، A/B و logout | NOT_RUN |
| finance | canonical IRR، unknown≠zero، manual review، no checkout/live money | NOT_RUN |
| legal | license کد/tool/rules/font/model/data و egress/consent | NOT_RUN |
| product | crosswalk رفتار/منبع، RTL/a11y، حفظ native و معیار مالک | NOT_RUN |

N/A فقط با دلیل واقعی و نام/تأیید انسان؛ نبود ابزار/reviewer/دستگاه یا UNKNOWN دلیل N/A نیست.

## آزمون و budget پیش از شروع

- فرمان‌ها: cwd + exact argv + نسخه + دادهٔ مصنوعی + minimum test count + expected exit. script موجود را قبل از اجرا بخوان؛ command حدسی نساز.
- positive / negative ownership-role / stale-revoked / error-timeout / reload / regression / prompt-injection cases:
- baseline failureها با evidence جدا؛ هیچ skip/ignore/threshold reduction برای سبزشدن.
- max_total_attempts: **3**؛ max_retries: **2**؛ fingerprint خطا/راهبرد حفظ شود.
- wall_clock_minutes: **پیشنهاد 90؛ تا عدد و تصویب مالک ثبت نشده AGENT-READY نیست**.
- paid_external_calls/cost_without_approval: **0**؛ egress خارجی پیش‌فرض ممنوع؛ سقف استثنای مصوب:
- مصرف attempt/زمان/هزینه در F/I/N/N؛ سقف پر شد یا secret/out-of-scope دیدی ⇒ توقف و BLOCKED/FAIL.
- اثر بیرونیِ مبهم blind retry نشود؛ remote/server state اول خوانده شود.

## تأیید، review و closure

- spec/owner approval واقعی + تاریخ/دامنه؛ ابزارهای آغاز برقرار؛ readiness reviewer:
- Forge → Inspect → Normalize → Next؛ نتیجه هر AC و گیت با evidence SHA-bound.
- independent reviewer / ابزار یا انسان / context مستقل / reviewed head SHA / یافته‌ها و رفع آن‌ها:
- human approval / approved head / CI runs / human merger / merge commit در baseline مصوب:
- پس از تغییر head، review/checkهای اثرگرفته دوباره لازم‌اند. عامل از این template مجوز push/merge ندارد.
- ledger/state/decisions/regressions/parity update؛ unresolved risks؛ اقدام امن بعدی:
- final status: DONE فقط پس از gates + review + approval + merge واقعی؛ UNKNOWN/NOT_RUN/DEFERRED ≠ PASS.
