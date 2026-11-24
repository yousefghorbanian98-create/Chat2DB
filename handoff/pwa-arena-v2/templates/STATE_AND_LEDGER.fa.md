# قالب اتصال به state/ledger موجود — فایل قبلی را بازنویسی نکن

در MP، مکان واقعی و صف فعال را از AGENTS/هندآف همان checkout پیدا کن. نام‌های تاریخی `.finn/state/STATE.md`، `LEDGER.md`، `DECISIONS.md` و `REGRESSIONS.md` راهنما هستند، نه دستور ایجاد/overwrite یک سیستم موازی. یادداشت‌های جدید افزایشی و بدون دادهٔ حساس باشند.

## state

task/parent/AC، status، base/head/patch hash، dependency/D blockers، F/I/N/N جاری، آخرین gate دارای شاهد، attempt/fingerprint، wall-clock و هزینهٔ مصوب/مصرف، reviewer و human approval/merge، اقدام بعدی دقیق.

## ledger — append only

تاریخ / task / خطا یا درس / منبع شاهد / علت / آزمون رگرسیون / قاعدهٔ عدم تکرار. در آغاز loop بعدی ledger مرتبط طبق قرارداد موجود خوانده شود؛ نام task تازه budget خطای قبلی را پاک نمی‌کند.

## decisions

تصمیم برگشت‌پذیر درون‌دامنه‌ای عامل با دلیل؛ تصمیم owner با ID/D/ADR و سند approval جدا؛ وضعیت DECISION/BLOCKED تا پاسخ واقعی. هیچ تصمیم امنیت/حقوقی/مالی/سلامت یا اذن بیرونی با حدس پر نشود.

## regressions

bug fingerprint / parent/child / failing test قبل / passing test بعد / exact SHA / negative cases / CI evidence. skipped یا mock-only را به‌جای persistence/server-security نگذار.

## checkpoint و handoff

مسیرهای تغییرکرده، command/exit/count واقعی، review/check‌های همان head، effectهای بیرونی attempted با نتیجهٔ معلوم/نامعلوم و ID، داده/فایل‌های دیگران untouched، unresolved risk و کار مستقل بعدی. UNKNOWN/NOT_RUN و no-Go صریح بمانند.
