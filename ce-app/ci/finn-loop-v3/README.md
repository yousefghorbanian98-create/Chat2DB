# Finn-Loop v3 runtime (Cutting Edge)
- `run_stage.py <id>` یک مرحله را از روی `ce-app/ci/finn-loop.manifest.json` اجرا و gate را اعمال می‌کند.
- `stages/<id>.sh` منطق واقعی هر مرحلهٔ فازهای ۱۵–۱۸ است.
- ورک‌فلوی n8n: `ce-app/ci/finn-loop.n8n.json` (Import در n8n؛ branch هدف: arena/01a032fb-chat2db).
- گزارش: `python3 run_stage.py --report`
