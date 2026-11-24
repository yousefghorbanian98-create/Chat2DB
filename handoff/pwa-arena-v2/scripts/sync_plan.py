#!/usr/bin/env python3
"""Synchronize the exact user inventory and additive execution metadata.

No installs/network/application execution. --check is read-only. The literal
expected IDs below intentionally do not come from generated PWA_PLAN.json.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_IDS = (
    "PWA-00", "PWA-01", "PWA-02", "PWA-03", "PWA-04", "PWA-05",
    "PWA-10", "PWA-11", "PWA-12", "PWA-13", "PWA-14", "PWA-15", "PWA-16", "PWA-17",
    "PWA-20", "PWA-21", "PWA-22", "PWA-23", "PWA-24",
    "PWA-30", "PWA-31", "PWA-32", "PWA-33", "PWA-34", "PWA-35", "PWA-36", "PWA-37",
    "PWA-38", "PWA-39", "PWA-3A", "PWA-3B", "PWA-3C", "PWA-3D", "PWA-3E", "PWA-3F",
    "PWA-40", "PWA-41", "PWA-42", "PWA-43", "PWA-44", "PWA-45", "PWA-46", "PWA-47",
    "PWA-50", "PWA-51", "PWA-52", "PWA-53", "PWA-54", "PWA-55", "PWA-56",
)
PHASE_TITLES = (
    "تثبیت تصمیم و خط مبنا", "تبدیل Studio به پوستهٔ PWA مشترک", "هویت، نشست و امنیت دسترسی",
    "انتقال تجربه‌های عضو از Flutter به React", "تجربهٔ کارکنان در همان PWA", "آزمون یکپارچه و انتشار محدود",
)


def read_source(root: Path = ROOT) -> list[dict]:
    rows: list[dict] = []
    phase = None
    for line in (root / "SOURCE_PLAN.fa.md").read_text(encoding="utf-8").splitlines():
        heading = re.match(r"## فاز ([۰-۵]) — ", line)
        if heading:
            phase = "۰۱۲۳۴۵".index(heading[1])
        if re.match(r"^\| PWA-[0-9A-F]{2} \|", line):
            columns = [value.strip() for value in line.split("|")[1:-1]]
            if len(columns) != 3 or phase is None:
                raise ValueError("Unexpected source inventory row")
            rows.append({"id": columns[0], "phase": phase, "title_fa": columns[1], "source_acceptance_fa": columns[2]})
    if tuple(row["id"] for row in rows) != EXPECTED_IDS:
        raise ValueError("Source inventory differs from the 50 user-supplied IDs; do not silently renumber or consolidate")
    if [sum(row["phase"] == phase for row in rows) for phase in range(6)] != [6, 8, 5, 16, 8, 7]:
        raise ValueError("Unexpected source phase counts")
    return rows


def generated(root: Path = ROOT) -> dict[str, str]:
    rows = read_source(root)
    details = json.loads((root / "PLAN_DETAILS.json").read_text(encoding="utf-8"))
    if set(details["tasks"]) != set(EXPECTED_IDS):
        raise ValueError("Execution metadata must cover each original ID exactly once")
    by_id = {row["id"]: row for row in rows}
    # A true DAG check: dependencies need not be adjacent or artificially serialized.
    visiting, visited = set(), set()
    def visit(task_id: str) -> None:
        if task_id in visiting:
            raise ValueError("Dependency cycle: " + task_id)
        if task_id in visited:
            return
        visiting.add(task_id)
        for dependency in details["tasks"][task_id]["depends_on"]:
            if dependency not in by_id:
                raise ValueError("Unknown dependency: " + dependency)
            visit(dependency)
        visiting.remove(task_id)
        visited.add(task_id)
    for task_id in by_id:
        visit(task_id)
    tasks = []
    for row in rows:
        record = {**row, **details["tasks"][row["id"]]}
        record.update({
            "acceptance_fa": [row["source_acceptance_fa"]],
            "required_finn_gates": details["gates_per_task"]["finn"],
            "required_domain_gates": details["gates_per_task"]["domain"],
            "budget": details["budget"],
            "completion_claim": False,
            "task_card": "templates/MICROTASK_TEMPLATE.fa.md",
            "evidence_template": "templates/EVIDENCE_TEMPLATE.fa.md",
            "human_contract_approval": "NOT_GRANTED_BY_HANDOFF",
            "independent_review": "NOT_RUN",
            "human_merge": "REQUIRED_NOT_AUTHORIZED_BY_HANDOFF",
        })
        tasks.append(record)
    plan = {
        "schema_version": 2, "version": "2.0.0", "date_utc": "2026-11-24",
        "kind": "USER_PLAN_PRESERVED_WITH_PROPOSED_EXECUTION_METADATA_NOT_PRODUCT_EVIDENCE",
        "task_count": len(tasks), "phase_counts": [6, 8, 5, 16, 8, 7],
        "source": "SOURCE_PLAN.fa.md", "identity": "PLAN_IDENTITY.json",
        "source_snapshot": details["source_snapshot"],
        "product_root": details["product_root"],
        "forbidden_second_product_root": details["forbidden_second_product_root"],
        "conditional_completion": details["conditional_completion"],
        "default_budget": details["budget"],
        "conditional_decision_dependencies": details.get("conditional_decision_dependencies", []),
        "plan": tasks,
    }
    content = ["# فهرست اجرایی کامل — هر ۵۰ میکرولوپ", "",
        "> تولیدشده از SOURCE_PLAN.fa.md + PLAN_DETAILS.json؛ متن مرز پذیرش از جدول کاربر حفظ شده است. وابستگی و تست تمرکزی افزوده، پیشنهادی‌اند. این فایل شاهد اجرای محصول نیست.", "",
        "هر کارت فقط با ۹ حوزهٔ Finn و ۵ گیت دامنه‌ای مستقل، قرارداد مصوب، بودجهٔ عددی و review/merge انسانی می‌تواند بسته شود. توضیح کامل در [Finn نهایی](FINN_LOOP_FINAL.fa.md) و [راهنمای اصلی](HANDOFF.fa.md).", ""]
    for phase in range(6):
        content += [f"## فاز {phase} — {PHASE_TITLES[phase]}", ""]
        for row in [r for r in tasks if r["phase"] == phase]:
            content += [f"### {row['id']} — {row['title_fa']}", "",
                "**مرز پذیرش ارسالی کاربر (بدون جایگزینی):**", "", row["source_acceptance_fa"], "",
                "**تکمیل اجرایی پیشنهادی:** " + row["verification_focus_fa"], "",
                "- وابستگی کارت: " + ("، ".join(row["depends_on"]) or "ندارد؛ آماده‌بودن محیط/قرارداد همچنان لازم است."),
                "- تصمیم مرتبط: " + ("، ".join(row["owner_decisions"]) or "فقط تصمیم‌های واقعاً مؤثر؛ پیش‌فرضِ حل‌شده فرض نشود."),
                "- مسیرهای موجودِ بررسی‌شده در tree مرجع: " + "، ".join("`" + s + "`" for s in row["source_paths"]),
                f"- وضعیت ابتدایی: `{row['status']}`؛ شاهد: `NOT_RUN`؛ review مستقل: `NOT_RUN`؛ هیچ ادعای تکمیل ندارد.",
                "- قرارداد: ۹ حوزهٔ G1…G9 و security/privacy/finance/legal/product برای **همین کارت**؛ budget: حداکثر ۳ تلاش کل، ۲ retry؛ ۹۰ دقیقه پیشنهادِ نیازمند تصویب؛ صفر تماس پولی بدون مجوز.",
                "- اگر این ردیف بزرگ است: زیرکارت‌های `" + row['id'] + ".1`، `.2`… با AC/NG مستقل؛ parent و همهٔ مرزهای بالا حفظ شوند و parent تا بسته‌شدن همهٔ فرزندان DONE نیست.", ""]
    content += ["## نکتهٔ شرطی PWA-3F", "", "PWA-3F حذف نشده و جزء ۵۰ ردیف است. در حالت پیش‌فرض BLOCKED است؛ release بدون آفلاین فقط با defer صریح مالک، ثبت دامنهٔ خارج‌شده و اثبات عدم ذخیره/ارسال آفلاین حساس قابل بررسی است. BLOCKED یا DEFERRED به معنی PASS نیست.", ""]
    return {"PWA_PLAN.json": json.dumps(plan, ensure_ascii=False, indent=2) + "\n", "MICROLOOPS.fa.md": "\n".join(content)}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="Compare without writing")
    args = parser.parse_args()
    differences = []
    for name, content in generated().items():
        file = ROOT / name
        if args.check:
            if not file.exists() or file.read_text(encoding="utf-8") != content:
                differences.append(name)
        else:
            file.write_text(content, encoding="utf-8")
    if differences:
        print("OUT_OF_SYNC: " + ", ".join(differences))
        return 1
    print("50 original IDs / 6 phases / exact source titles and boundaries: synchronized (not product QA)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
