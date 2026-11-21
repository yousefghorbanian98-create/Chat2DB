#!/usr/bin/env python3
"""build_builder_kit.py — ساختِ «کیتِ کاملِ بیلدر» به‌صورتِ قطعی و بازتولیدپذیر.

    python3 audit/build_builder_kit.py          # از ریشهٔ مخزن اجرا شود

خروجی:
  handoff/MP-BUILDER-KIT-2026-11-21.zip   بستهٔ نهایی (با MANIFEST.sha256 درونش)
  handoff/MP-BUILDER-KIT-INDEX.md         همان «00-READ-ME-FIRST.md» درونِ بسته

چرا مولد و نه ZIPِ دستی: تا هر کس بتواند با اجرای همین فایل، بسته‌ای
**بایت‌به‌بایت یکسان** بسازد. به همین دلیل مهرِ زمانیِ همهٔ ورودی‌ها ثابت است
(BUILD_STAMP) و هیچ‌جا از ساعتِ دیوار استفاده نمی‌شود ⇒ دو اجرای متوالی،
sha256 یکسان می‌دهند.

چرا hashِ خودِ بسته داخلِ بسته نیست: یک بسته نمی‌تواند hashِ خودش را درونِ خودش
داشته باشد (دورِ باطل). sha256ِ خودِ ZIP در handoff/README.md و در پیامِ commit
ثبت می‌شود. MANIFEST.sha256ِ درونِ بسته، hashِ همهٔ اعضا **جز خودش** را دارد.
"""
from __future__ import annotations

import hashlib
import pathlib
import subprocess
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT_ZIP = ROOT / "handoff" / "MP-BUILDER-KIT-2026-11-21.zip"
OUT_INDEX = ROOT / "handoff" / "MP-BUILDER-KIT-INDEX.md"
KIT_ROOT = "MP-BUILDER-KIT-2026-11-21"
BUILD_STAMP = (2026, 11, 21, 13, 45, 0)          # ثابت ⇒ بازتولیدِ بایت‌به‌بایت
BUILD_LABEL = "۲۰۲۶‑۱۱‑۲۱ · base commit 662ff88 · ruff 0.17.6"

# ── چیدمانِ بسته بر پایهٔ «کاربرد»، نه بر پایهٔ «محلِ ذخیره» ────────────────
# (dest داخل بسته, src در مخزن)
DOCS = [
    ("01-paste-into-builder-session/MP-BUILDER-HANDOFF-A1.3.md", "handoff/MP-BUILDER-HANDOFF-A1.3.md"),
    ("02-plan/MP-BUILDER-PROMPT-2026-11-21.md", "share/MP-BUILDER-PROMPT-2026-11-21.md"),
    ("02-plan/MP-BUILDER-ADDENDUM-2026-11-21.md", "share/MP-BUILDER-ADDENDUM-2026-11-21.md"),
    ("03-findings/MP-FINAL-AUDIT-REPORT-2026-11-20.md", "share/MP-FINAL-AUDIT-REPORT-2026-11-20.md"),
    ("03-findings/MP-PROBLEMS-2026-11-20.md", "share/MP-PROBLEMS-2026-11-20.md"),
    ("04-evidence/MP-EVIDENCE-DOSSIER-2026-11-20.md", "share/MP-EVIDENCE-DOSSIER-2026-11-20.md"),
    ("04-evidence/MP-AGENT-BRIEF.md", "share/MP-AGENT-BRIEF.md"),
    ("05-tools/ruff-recommended.toml", "audit/ruff-recommended.toml"),
    ("05-tools/verify-addendum-gates.sh", "audit/verify-addendum-gates.sh"),
    ("06-background/AUDIT_TOOLCHAIN.md", "docs/AUDIT_TOOLCHAIN.md"),
]

INDEX_TEMPLATE = """# کیتِ کاملِ بیلدر — اول این را بخوان

> بستهٔ خودکفا برای نشستِ بیلدرِ پروژهٔ MP. **هیچ‌چیز بیرونی لازم نیست**: نه پیوند،
> نه دسترسیِ شبکه، نه فایلِ دیگری در مخزن. هر عددی که بیلدر باید بازتولید کند، همراه با
> فرمانِ دقیقِ اندازه‌گیری‌اش داخلِ همین بسته است.
>
> ساخته‌شده در {build_label} · {entries} ورودی · مهرِ زمانیِ ثابت (بازتولیدپذیر)

---

## ۱ · تنها کاری که باید همین حالا بکنی

`01-paste-into-builder-session/MP-BUILDER-HANDOFF-A1.3.md` را باز کن و متنِ بینِ دو
نشانگرِ **«از اینجا کپی کن»** و **«تا اینجا کپی کن»** را **عیناً** در نشستِ بیلدر
(یا حلقهٔ `FINN-AUDIT-LOOP.md`) کپی کن. بقیهٔ این بسته مرجع است، نه پیام.

چرا کپی و نه پیوند: یک بار به‌جای کپی‌کردنِ متن به آن **ارجاع** داده شد و کلِ `WP 0.9`
یک دورِ کامل بلاک ماند، چون بیلدر فقط چیزی را می‌بیند که در نشستش کپی شده است.

## ۲ · ترتیبِ خواندن

| پوشه | چه دارد | کی لازم می‌شود |
|---|---|---|
| `01-paste-into-builder-session/` | پیامِ آمادهٔ کپی (A1.3): حلِ اختلافِ `RUF100`، اعدادِ هر مرحله، پروتکلِ بی‌ناظر، پیکربندی و اسکریپتِ کامل | **اول** — همین حالا |
| `02-plan/` | پرامپتِ اصلیِ بیلدر (۳۰ WP در ۵ فاز) + الحاقیهٔ A1.3 (`WP 0.9`/`2.6`/`3.6`، تصحیحِ `WP 4.5`، `D‑6`/`D‑7`، §۹) | پیش از شروعِ هر WP |
| `03-findings/` | گزارشِ نهاییِ ۲۹ یافته (`F‑01`…`F‑29`) با زنجیرهٔ `file:line`، ۲۷ ردیفِ سالم، ۱۲+۱ مدعای ردشده، نقشهٔ رفع؛ و صورت‌مسئله‌ها | هنگامِ رفعِ هر یافته |
| `04-evidence/` | پروندهٔ شواهد (§۰–§۱۱ با جدولِ ۲۰ ردیفیِ تصحیحات و manifest) + بریفِ ایجنت + `raw/` = ۴۴ شاهدِ خامِ اندازه‌گیری‌ها | هر وقت عددی را باور نکردی |
| `05-tools/` | پیکربندیِ ruff، اسکریپتِ پذیرش، قواعدِ semgrep، پیکربندیِ ESLint، و `harness/` = ۱۴ اسکریپتِ probe/serve/bench برای **اجرای دوبارهٔ** هر آزمایش | هنگامِ ساختِ گیت و بازتولیدِ شاهد |
| `06-background/` | کاتالوگِ ابزارهای **کاملاً رایگان و اوپن‌سورس** برای هر لایهٔ ممیزی | هنگامِ انتخابِ ابزارِ CI |

⚠ **یک caveat در `06-background/AUDIT_TOOLCHAIN.md`:** بخشِ ۱۲ آن («هستهٔ حداقلی»)
برای استکِ **Java 17 / Spring Boot / React‑TS** نوشته شده و به MP
(**پایتون ۳٫۱۱ / FastAPI / SQLAlchemy**) ربطی ندارد. بخش‌های ۰ تا ۱۱ و ۱۳
(نگاشتِ خواسته ← ابزار، و «از این‌ها استفاده نکنید») قابلِ استفاده‌اند.

## ۳ · دو فرمانِ شروع

```bash
# ۱) پیکربندی را عیناً نصب کن (متنِ کامل در §۵ پیامِ هند‌آف و در 05-tools/)
cp 05-tools/ruff-recommended.toml mp-app/backend/ruff-audit.toml   # یا داخلِ pyproject.toml

# ۲) گیت‌ها را بسنج — باید «گیت‌های نامنطبق: ۰ / PASS» بدهد
cd mp-app/backend
RUFF=/path/to/ruff CFG=../ruff-audit.toml bash ../../05-tools/verify-addendum-gates.sh before
```

مقدارهای موردانتظار: گام ۱ ⇒ **۴۳۰ یافته / ۵۲ قاعدهٔ متمایز**؛ پس از افزودنِ
`"ERA001",` به `ignore` ⇒ **۴۱۹ / ۵۱**. در هر دو حالت `RUF100` = **۳۹**،
`TRY400` = **۶**، `DTZ011` = **۳**، `C901` = **۱۵**، و
`ruff format --check` ⇒ **۳۷۸ فایل already formatted**.

## ۴ · سه قاعدهٔ کلیِ این بسته

1. **عددها به نسخه گره خورده‌اند.** همهٔ اعداد با **ruff ‏۰٫۱۷٫۶** روی **۳۷۶ فایل** در
   commit **`662ff88`** و با `--no-cache` گرفته شده‌اند. با نسخهٔ دیگر، عددِ مطلق عوض می‌شود.
2. **زمان‌ها نسبت‌اند، نه مطلق.** میلی‌ثانیه‌ها ماشین‌وابسته‌اند (۲ vCPU). نسبتِ
   «گیتِ lint در برابر pytest» (~۰٫۰۲٪) معتبر است، عددِ خام نه.
3. **اگر عددِ تو فرق داشت، عددِ تو معتبر است** — به شرطِ ثبتِ عینیِ فرمان. آنچه مجاز
   نیست: دستکاریِ پیکربندی یا پاک‌کردنِ `# noqa` برای رسیدن به عددِ سند
   (پیامِ هند‌آف §۳‑۲: ممنوعیتِ «سبزکردنِ گیت با سرکوب»).

## ۵ · وارسیِ سلامتِ بسته

```bash
sha256sum -c MANIFEST.sha256 --quiet && echo "همهٔ اعضا سالم‌اند"
```

`MANIFEST.sha256` hashِ **همهٔ اعضا جز خودش** را دارد. hashِ خودِ ZIP داخلِ خودش نیست
(دورِ باطل است)؛ در `handoff/README.md` و در پیامِ commitِ مخزن ثبت شده است.

## ۶ · اعضای بسته

{member_table}

---

*این فایل توسط `audit/build_builder_kit.py` ساخته شده و بازتولیدپذیر است: دو اجرای
متوالی، بسته‌ای با sha256ِ یکسان می‌دهند (مهرِ زمانیِ ثابت، بدونِ ساعتِ دیوار).*
"""


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def human(n: int) -> str:
    return f"{n:,}"


def main() -> int:
    members: dict[str, bytes] = {}
    for dest, src in DOCS:
        p = ROOT / src
        if not p.is_file():
            raise SystemExit(f"FATAL: منبع پیدا نشد: {src}")
        members[dest] = p.read_bytes()
    for p in sorted((ROOT / "audit" / "evidence").rglob("*")):
        if p.is_file() and "__pycache__" not in str(p):
            members[f"04-evidence/raw/{p.relative_to(ROOT / 'audit' / 'evidence').as_posix()}"] = p.read_bytes()
    # ابزارهای 05-tools/ از پیش در DOCS آمده‌اند؛ این مولد هم عمداً داخلِ بسته نمی‌رود
    # (به مسیرهای مخزن وابسته است و از درونِ بسته اجراشدنی نیست).
    SKIP = {"build_builder_kit.py", "ruff-recommended.toml", "verify-addendum-gates.sh"}
    for p in sorted((ROOT / "audit").iterdir()):
        if not p.is_file() or p.name in SKIP:
            continue
        members[f"05-tools/harness/{p.name}"] = p.read_bytes()

    # MANIFEST: همهٔ اعضا جز خودش (و جز ایندکس که هنوز ساخته نشده)
    staged = dict(members)
    index_body = INDEX_TEMPLATE.format(
        build_label=BUILD_LABEL,
        entries=f"{len(staged) + 2}",           # + ایندکس + MANIFEST
        member_table="\n".join(
            f"| `{d}` | {human(len(b))} | `{sha256(b)[:16]}…` |"
            for d, b in sorted(staged.items())
        ),
    )
    # سرستونِ جدولِ اعضا
    index_body = index_body.replace(
        "## ۶ · اعضای بسته\n\n|",
        "## ۶ · اعضای بسته\n\n(بدونِ خودِ این فایل و بدونِ `MANIFEST.sha256` — هیچ‌کدام نمی‌توانند hashِ خودشان را داشته باشند)\n\n| عضو | اندازه (بایت) | SHA‑256 (۱۶ رقم نخست) |\n|---|---|---|\n|",
        1,
    )
    staged["00-READ-ME-FIRST.md"] = index_body.encode("utf-8")
    manifest = "".join(f"{sha256(b)}  {d}\n" for d, b in sorted(staged.items()))
    staged["MANIFEST.sha256"] = manifest.encode("utf-8")

    OUT_INDEX.write_bytes(staged["00-READ-ME-FIRST.md"])
    with zipfile.ZipFile(OUT_ZIP, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for dest in sorted(staged):
            zi = zipfile.ZipInfo(f"{KIT_ROOT}/{dest}", date_time=BUILD_STAMP)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, staged[dest])
        assert z.testzip() is None
    blob = OUT_ZIP.read_bytes()
    print(f"بسته: {OUT_ZIP.relative_to(ROOT)}")
    print(f"  ورودی‌ها : {len(staged)}")
    print(f"  اندازه   : {human(len(blob))} بایت")
    print(f"  sha256   : {sha256(blob)}")
    print(f"  index    : {OUT_INDEX.relative_to(ROOT)} ({human(OUT_INDEX.stat().st_size)} بایت)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
