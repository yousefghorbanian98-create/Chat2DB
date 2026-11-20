#!/usr/bin/env python3
"""اسکن دقیق «دکمه → هندلر → فراخوانی API» در studio (لایهٔ سیم‌کشی UI).

چرا این اسکریپت؟ نسخهٔ نخستِ ممیزی با regex سادهٔ `<button([^>]*)>` نوشته شده
بود و چون در JSX خصوصیت‌ها چندخطی‌اند، `onClick` خطِ بعد را نمی‌دید ⇒ ۷۵ دکمهٔ
سالم را «بی‌سیم» گزارش کرد (یافتهٔ کاذب). بررسی دستی ردش کرد. این نسخه
**tag-aware** است: عمق `{}` و quote را دنبال می‌کند تا پایان واقعی تگ.

خروجی‌ها:
  ۱. شمار دکمه‌ها و تفکیک: onClick دارد / ندارد / هندلر تهی
  ۲. برای هر دکمهٔ دارای onClick: آیا زنجیرهٔ هندلر به یک تابع API می‌رسد؟
  ۳. توابع export شدهٔ `lib/api.ts` که هیچ‌جا import نشده‌اند (سیم‌کشی مرده)
  ۴. فایل‌های صفحه که هیچ تابع API‌ای import نکرده‌اند (صفحهٔ نمایشی/مرده)

اجرا: /tmp/run/venv/bin/python audit/scan_ui_wiring.py
"""
from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

SRC = Path("/tmp/run/MP/mp-app/studio/src")
EVIDENCE = Path("/home/user/Chat2DB/audit/evidence")
TAG_RE = re.compile(r"<(button|Button|IconButton)\b", re.IGNORECASE)
IMPORT_RE = re.compile(r"import\s+(?:type\s+)?\{([^}]+)\}\s+from\s+['\"]([^'\"]*api)['\"]", re.S)


def read_tag(txt: str, start: int) -> tuple[str, int]:
    """از `<button` تا `>` بسته‌شده (با رعایت عمق {} و quote) — نه اولین `>`."""
    i = start
    depth = 0
    quote = ""
    while i < len(txt):
        ch = txt[i]
        if quote:
            if ch == quote:
                quote = ""
        elif ch in "\"'`":
            quote = ch
        elif ch == "{":
            depth += 1
        elif ch == "}":
            depth -= 1
        elif ch == ">" and depth <= 0:
            return txt[start:i + 1], i + 1
        i += 1
    return txt[start:start + 400], len(txt)


def exported_api_functions(api_file: Path) -> set[str]:
    txt = api_file.read_text(encoding="utf-8")
    names = set(re.findall(r"export\s+async\s+function\s+(\w+)", txt))
    names |= set(re.findall(r"export\s+function\s+(\w+)", txt))
    names |= set(re.findall(r"export\s+const\s+(\w+)\s*=\s*async", txt))
    names |= set(re.findall(r"export\s+const\s+(\w+)\s*=\s*\(", txt))
    return names


def handler_chain(file_txt: str, handler_body: str, api_names: set[str], depth: int = 0) -> bool:
    """آیا بدنهٔ هندلر (مستقیم یا از طریق توابع محلی) به API می‌رسد؟"""
    if depth > 3:
        return False
    if any(re.search(rf"\b{re.escape(n)}\s*\(", handler_body) for n in api_names):
        return True
    if re.search(r"\b(fetch|axios)\s*\(", handler_body):
        return True
    # توابع محلی صدا زده‌شده را دنبال کن
    for callee in set(re.findall(r"\b(?:void\s+)?([a-zA-Z_]\w*)\s*\(", handler_body)):
        m = re.search(rf"(?:const|function)\s+{re.escape(callee)}\b[^{{]*{{", file_txt)
        if not m:
            continue
        # بدنهٔ تقریبی همان تابع
        sub, _ = read_tag(file_txt, m.end() - 1)
        if handler_chain(file_txt, sub, api_names, depth + 1):
            return True
    return False


def main() -> None:
    files = [f for f in SRC.rglob("*.tsx") if ".test." not in f.name]
    api_file = SRC / "lib" / "api.ts"
    api_names = exported_api_functions(api_file)

    total = 0
    with_click = 0
    no_click: list[str] = []
    empty_click: list[str] = []
    click_without_api: list[str] = []
    imports_per_file: dict[str, set[str]] = {}
    used_api: Counter = Counter()

    for f in files:
        txt = f.read_text(encoding="utf-8")
        rel = str(f.relative_to(SRC))
        imported: set[str] = set()
        for m in IMPORT_RE.finditer(txt):
            for part in m.group(1).split(","):
                name = part.strip().split(" as ")[-1].strip()
                if name:
                    imported.add(name)
        imports_per_file[rel] = imported & api_names
        used_api.update(imported & api_names)

        for m in TAG_RE.finditer(txt):
            tag, _ = read_tag(txt, m.start())
            total += 1
            line = txt[:m.start()].count("\n") + 1
            oc = re.search(r"onClick\s*=\s*\{(.*?)\}\s*(?=\w+=|/?>)", tag, re.S)
            if not oc:
                # حالت چندخطی/بدون فاصله: جست‌وجوی ساده‌تر در کل تگ
                if "onClick" in tag:
                    oc2 = re.search(r"onClick\s*=\s*\{(.*)", tag, re.S)
                    body = oc2.group(1).rstrip("} \n") if oc2 else ""
                else:
                    no_click.append(f"{rel}:{line}")
                    continue
            else:
                body = oc.group(1)
            with_click += 1
            stripped = body.strip()
            if stripped in ("", "undefined", "null") or re.fullmatch(
                    r"\(\)\s*=>\s*\{\s*\}", stripped) or re.fullmatch(r"\(\)\s*=>\s*\{\}", stripped):
                empty_click.append(f"{rel}:{line} → onClick={stripped[:40]}")
                continue
            if not handler_chain(txt, stripped, api_names | imported):
                click_without_api.append(f"{rel}:{line} → {stripped[:60]}")

    never_imported = sorted(api_names - set(used_api))
    pages_no_api = sorted(rel for rel, imps in imports_per_file.items()
                          if rel.startswith("pages/") and not imps)

    out = {
        "buttons_total": total,
        "buttons_with_onClick": with_click,
        "buttons_without_onClick": len(no_click),
        "buttons_without_onClick_list": no_click[:40],
        "buttons_empty_onClick": empty_click,
        "buttons_onClick_without_api_call": click_without_api[:40],
        "api_functions_exported": len(api_names),
        "api_functions_never_imported": never_imported,
        "pages_without_any_api_import": pages_no_api,
    }
    EVIDENCE.mkdir(parents=True, exist_ok=True)
    (EVIDENCE / "studio-ui-wiring.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"دکمه‌ها: {total} | با onClick: {with_click} | بدون onClick: {len(no_click)} "
          f"| onClick تهی: {len(empty_click)}")
    print(f"onClick بدون رسیدن به API: {len(click_without_api)}")
    for x in click_without_api[:12]:
        print("   -", x)
    print(f"توابع API export شده: {len(api_names)} | هرگز import نشده: {len(never_imported)}")
    for x in never_imported[:14]:
        print("   -", x)
    print(f"صفحه‌های بدون هیچ import از api.ts: {len(pages_no_api)} → {pages_no_api[:8]}")
    print("→ evidence/studio-ui-wiring.json")


if __name__ == "__main__":
    sys.exit(main())
