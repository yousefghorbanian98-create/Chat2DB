#!/usr/bin/env python3
"""INV-03 crosswalk generator — صفحات کارکنان در همان Studio (PWA-40).

چرا این فایل وجود دارد
----------------------
INV-03 در tracker فقط «شروع‌شده و PARTIAL/NOT_ACCEPTED» است. مثل INV-02، هر خروجی
دست‌نویس که push نشود با بسته‌شدن نشست از بین می‌رود. این اسکریپت نقشهٔ
صفحه → route / نقش / API / تست را از خود کد می‌سازد تا قابل تکرار باشد.

قواعد سخت
---------
1. فقط‌خواندنی؛ تنها دو فایل خروجی خودش را می‌نویسد.
2. نقش‌ها از `mp-app/studio/src/lib/roleNav.ts` خوانده می‌شوند (آینهٔ rbac سرور)، نه از حافظه.
3. هر صفحه باید در `PAGE_IDS` (appStore) باشد؛ صفحهٔ بی‌route در `routes.json` → وضعیت مشخص.
4. هرگز `CURRENT` صادر نمی‌شود؛ سقف `PARTIAL_REVIEW` است.
5. اگر صفحه‌ای فایل نداشته باشد یا route نباشد → `BLOCKED`، نه حدس.

اجرا (از ریشهٔ مخزن MP، روی SHA تازه):
    python3 scripts/inv03_staff_crosswalk.py --repo . --out evidence/$(date -u +%F)/INV-03/
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

# ── نقشهٔ دامنهٔ هر صفحهٔ کارکنان → پیشوندهای مسیر API سرور ──
# دستی و قابل‌بازبینی. اگر پیشوندی در routes.json نبود، صفحه BLOCKED می‌شود.
PAGE_TO_API: dict[str, tuple[str, ...]] = {
    "dashboard": ("/api/v1/admin/kpis", "/api/v1/admin/members-summary",
                  "/api/v1/admin/attendance", "/api/v1/health/"),
    "members": ("/api/v1/members/", "/api/v1/admin/members-summary"),
    "programs": ("/api/v1/programs/",),
    "nutrition": ("/api/v1/nutrition/", "/api/v1/ai/nutrition/"),
    "assessment": ("/api/v1/assessments/", "/api/v1/ai/suggest-weight"),
    "chat": ("/api/v1/chat/",),
    "checkin": ("/api/v1/face/", "/api/v1/admin/checkins"),
    "finance": ("/api/v1/payments/",),
    "expenses": ("/api/v1/expenses/",),
    "analytics": ("/api/v1/admin/analytics/", "/api/v1/admin/retention"),
    "settings": ("/api/v1/admin/", "/api/v1/updates/"),
    "shop": ("/api/v1/shop/",),
}

# سه شکل واقعیِ صدا زدن API در Studio:
#   1) `${API_BASE}/admin/kpis`            (api.ts)
#   2) getJson<X>("/admin/members-summary") — API_BASE داخل helper اضافه می‌شود
#   3) "/api/v1/..."                        (literal کامل، مثلاً در تست/driver)
CONSUMER_PATTERNS = (
    re.compile(r"""\$\{API_BASE\}(/[^"'`$\s]*)"""),
    re.compile(r"""(?:getJson|postJson|putJson|patchJson|deleteJson|sessionFetch|request)"""
               r"""\s*(?:<[^>()]*>)?\(\s*[`"'](/[^`"'$\s]*)"""),
    re.compile(r"""["'`](/api/v1/[^"'`\s]*)["'`]"""),
)
PLACEHOLDER = re.compile(r"\{[^}]*\}|\$\{[^}]*\}")


def sh(*args: str, cwd: Path) -> str:
    try:
        return subprocess.run(args, cwd=cwd, capture_output=True, text=True).stdout.strip()
    except OSError:
        return ""


def sha256(path: Path) -> str | None:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None


def canon(path: str) -> str:
    return PLACEHOLDER.sub("*", path.split("?")[0].rstrip("/"))


def path_match(a: str, b: str) -> bool:
    pa, pb = canon(a).split("/"), canon(b).split("/")
    if len(pa) != len(pb):
        return False
    return all(x == "*" or y == "*" or x == y for x, y in zip(pa, pb))


def under_prefix(path: str, prefix: str) -> bool:
    return canon(path).startswith(canon(prefix))


@dataclass
class Row:
    page: str
    component: str | None
    route: str | None
    roles: list[str]
    apis_total: int = 0
    apis_used: int = 0
    consumers: list[str] | None = None
    tests: list[str] | None = None
    status: str = "UNKNOWN"
    reason: str = ""


def load_routes(repo: Path) -> set[str]:
    data = json.loads((repo / "mp-app/backend/api/routes.json").read_text(encoding="utf-8"))
    return {op["path"] for op in data.get("operations", [])}


def page_rules(repo: Path) -> dict[str, list[str]]:
    """roleNav.ts → {page: [roles]}. الگوی ساده؛ اگر پارس نشد، لیست خالی و هشدار."""
    path = repo / "mp-app/studio/src/lib/roleNav.ts"
    if not path.is_file():
        return {}
    text = path.read_text(encoding="utf-8")
    rules: dict[str, list[str]] = {}
    for match in re.finditer(r"(\w+):\s*\{[^}]*?roles:\s*\[([^\]]*)\]", text, re.S):
        rules[match.group(1)] = [r.strip().strip('"\'') for r in match.group(2).split(",") if r.strip()]
    return rules


def page_ids(repo: Path) -> list[str]:
    path = repo / "mp-app/studio/src/stores/appStore.ts"
    if not path.is_file():
        return []
    text = path.read_text(encoding="utf-8")
    block = re.search(r"PAGE_IDS\s*=\s*\[(.*?)\]\s*as const", text, re.S)
    return re.findall(r'"([a-z_]+)"', block.group(1)) if block else []


def navigation_pages(repo: Path) -> set[str]:
    """صفحه‌هایی که navigation.ts واقعاً route می‌دهد.

    الگوی واقعی: `path.match(/^\/staff\/([a-z]+)$/)` + `STAFF_PAGES.includes(...)`.
    اگر این مسیر عمومی وجود داشته باشد، همهٔ PAGE_IDS مسیر دارند.
    """
    path = repo / "mp-app/studio/src/lib/navigation.ts"
    if not path.is_file():
        return set()
    text = path.read_text(encoding="utf-8")
    generic = bool(re.search(r"/\^\\?/staff\\?/\(\[a-z\]\+\)", text)) or (
        "/staff/" in text and "STAFF_PAGES" in text)
    if generic:
        return set(page_ids(repo))
    return set(re.findall(r'path === "/staff/([a-z]+)"', text))


def call_sites(repo: Path) -> dict[str, set[str]]:
    studio = repo / "mp-app/studio/src"
    hits: dict[str, set[str]] = {}
    if not studio.is_dir():
        return {}
    for ts in studio.rglob("*.ts*"):
        text = ts.read_text(encoding="utf-8", errors="ignore")
        for pattern in CONSUMER_PATTERNS:
            for match in pattern.finditer(text):
                raw = match.group(1)
                full = raw if raw.startswith("/api/") else "/api/v1" + raw
                hits.setdefault(canon(full), set()).add(str(ts.relative_to(repo)))
    return hits


def test_mentions(repo: Path) -> dict[str, set[str]]:
    hits: dict[str, set[str]] = {}
    for root in (repo / "mp-app/studio/tests", repo / "mp-app/backend/tests"):
        if not root.is_dir():
            continue
        for path in root.rglob("*"):
            if path.suffix not in {".ts", ".tsx", ".py"} or not path.is_file():
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for m in re.finditer(r"/api/v1/[A-Za-z0-9_/{}\-]+", text):
                hits.setdefault(canon(m.group(0)), set()).add(str(path.relative_to(repo)))
    return hits


def build(repo: Path) -> tuple[list[Row], dict]:
    routes = load_routes(repo)
    rules = page_rules(repo)
    ids = page_ids(repo)
    nav = navigation_pages(repo)
    calls = call_sites(repo)
    tests = test_mentions(repo)
    pages_dir = repo / "mp-app/studio/src/pages"

    rows: list[Row] = []
    for page in ids:
        # نام فایل ممکن است CamelCase با حرف بزرگ دوم باشد (CheckIn.tsx)؛
        # تطبیق case-insensitive انجام می‌شود تا صفحهٔ موجود BLOCKED نشود.
        candidates = [p for p in pages_dir.glob("*.tsx") if p.stem.lower() == page.lower()]
        component = candidates[0] if candidates else None
        comp = str(component.relative_to(repo)) if component else None
        prefixes = PAGE_TO_API.get(page)
        row = Row(page=page, component=comp, route=f"/staff/{page}" if page in nav else None,
                  roles=sorted(rules.get(page, [])), consumers=[], tests=[])

        if prefixes is None:
            row.status, row.reason = "BLOCKED", "نقشهٔ دامنهٔ API برای این صفحه تعریف نشده"
        elif comp is None:
            row.status, row.reason = "BLOCKED", "فایل صفحه در src/pages پیدا نشد"
        else:
            apis = sorted(p for p in routes if any(under_prefix(p, pre) for pre in prefixes))
            used = [a for a in apis if any(path_match(a, c) for c in calls)]
            row.apis_total, row.apis_used = len(apis), len(used)
            row.consumers = sorted({Path(f).name for c, fs in calls.items()
                                    if any(path_match(a, c) for a in used) for f in fs})[:5]
            row.tests = sorted({Path(f).name for a in used for c, fs in tests.items()
                                if path_match(a, c) for f in fs})[:5]
            if not used:
                row.status = "GAP"
                row.reason = f"هیچ call-site در Studio به {len(apis)} مسیر این دامنه اشاره نمی‌کند"
            elif not row.tests:
                row.status, row.reason = "GAP", "call-site هست ولی هیچ تستی همان مسیر را نام نمی‌برد"
            else:
                row.status = "PARTIAL_REVIEW"
                row.reason = ("route + نقش + call-site + اشارهٔ تستی پیدا شد؛ "
                              "اثر نهایی/مجوز و مرور صفحه با data واقعیِ ساختگی انجام نشده")
        rows.append(row)

    counts: dict[str, int] = {}
    for r in rows:
        counts[r.status] = counts.get(r.status, 0) + 1

    meta = {
        "sha": sh("git", "rev-parse", "HEAD", cwd=repo),
        "branch": sh("git", "rev-parse", "--abbrev-ref", "HEAD", cwd=repo),
        "dirty": bool(sh("git", "status", "--porcelain", "--untracked-files=no", cwd=repo)),
        "sources": {
            "backend/api/routes.json": sha256(repo / "mp-app/backend/api/routes.json"),
            "studio/src/lib/roleNav.ts": sha256(repo / "mp-app/studio/src/lib/roleNav.ts"),
            "studio/src/lib/navigation.ts": sha256(repo / "mp-app/studio/src/lib/navigation.ts"),
            "studio/src/stores/appStore.ts": sha256(repo / "mp-app/studio/src/stores/appStore.ts"),
        },
        "counts": {"pages": len(ids), "routed_pages": len([r for r in rows if r.route]),
                   "server_routes": len(routes)},
        "status_counts": counts,
        "role_rules_parsed": len(rules),
        "generated_by": "scripts/inv03_staff_crosswalk.py",
    }
    return rows, meta


def render(rows: list[Row], meta: dict) -> str:
    def esc(t: str) -> str:
        return str(t).replace("|", "\\|").replace("\n", " ")

    lines = [
        "# INV-03 — crosswalk صفحات کارکنان (بازسازیِ قابل‌تکرار)",
        "",
        "> **وضعیت سند:** `PARTIAL / NOT_ACCEPTED` — تولیدشده با اسکریپت روی SHA زیر.",
        "> این سند پذیرش محصول یا اثبات مجوز نیست. ستون نقش، آینهٔ `roleNav.ts` است؛",
        "> اثبات، فقط با اجرای `rbac.py` و تست منفی سمت سرور به دست می‌آید.",
        "",
        f"- SHA: `{meta['sha']}` · branch: `{meta['branch']}` · tracked-dirty: `{meta['dirty']}`",
    ]
    for name, digest in meta["sources"].items():
        lines.append(f"- `{name}` → `{digest or 'MISSING'}`")
    lines += [
        f"- صفحه‌های `PAGE_IDS`: **{meta['counts']['pages']}** · با route: "
        f"**{meta['counts']['routed_pages']}** · مسیرهای API سرور: **{meta['counts']['server_routes']}**",
        f"- قواعد نقش پارس‌شده از `roleNav.ts`: **{meta['role_rules_parsed']}**",
        "- شمارش: " + " · ".join(f"`{k}={v}`" for k, v in sorted(meta["status_counts"].items())),
        "",
        "| # | صفحه | کامپوننت | route | نقش‌های UI | API مصرف‌شده/کل | call-site | اشارهٔ تستی | وضعیت | دلیل |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for i, r in enumerate(rows, 1):
        cells = [
            str(i), f"`{r.page}`", f"`{Path(r.component).name}`" if r.component else "—",
            f"`{r.route}`" if r.route else "—",
            ", ".join(r.roles) or "—",
            f"{r.apis_used} / {r.apis_total}",
            "<br>".join(f"`{c}`" for c in (r.consumers or [])) or "—",
            "<br>".join(f"`{t}`" for t in (r.tests or [])) or "—",
            f"**{r.status}**", r.reason,
        ]
        lines.append("| " + " | ".join(esc(c) for c in cells) + " |")

    lines += [
        "",
        "## چه چیزی این سند اثبات نمی‌کند",
        "",
        "- نمایش درست صفحه با دادهٔ واقعی (fixture ساختگی) اجرا نشده است.",
        "- مجوز سرور: نقش‌ها از `roleNav.ts` آمده‌اند؛ `rbac.py` اجرا و تست منفی نشده.",
        "- تفکیک «مصرف‌کنندهٔ صفحهٔ کارکنان» از «مصرف‌کنندهٔ صفحهٔ عضو» در سطح فایل انجام",
        "  شده، نه در سطح کامپوننت؛ برخی call-siteها مشترک‌اند.",
        "- browser/device، screen reader و reviewer مستقل: اجرا نشده.",
        "",
        "## بازتولید",
        "",
        "```bash",
        "git fetch origin && git checkout --detach origin/main",
        "python3 scripts/inv03_staff_crosswalk.py --repo . --out evidence/$(date -u +%F)/INV-03/",
        "```",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(description="INV-03 staff page crosswalk generator")
    ap.add_argument("--repo", default=".")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    repo = Path(args.repo).resolve()
    out = Path(args.out)
    out = out if out.is_absolute() else repo / out

    if not (repo / "mp-app/backend/api/routes.json").is_file():
        print("FATAL: از ریشهٔ مخزن MP اجرا کن (mp-app/backend/api/routes.json پیدا نشد).",
              file=sys.stderr)
        return 2
    if not page_ids(repo):
        print("FATAL: PAGE_IDS در mp-app/studio/src/stores/appStore.ts خوانده نشد؛ "
              "الگوی پارس عوض شده — اول اسکریپت را اصلاح کن، خروجی خالی نده.", file=sys.stderr)
        return 3

    rows, meta = build(repo)
    out.mkdir(parents=True, exist_ok=True)
    (out / "staff-page-crosswalk.md").write_text(render(rows, meta), encoding="utf-8")
    (out / "staff-page-crosswalk.json").write_text(
        json.dumps({"meta": meta, "rows": [r.__dict__ for r in rows]},
                   ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(f"OK  sha={meta['sha'][:12] or '?'}  pages={meta['counts']['pages']}  "
          f"routed={meta['counts']['routed_pages']}  {meta['status_counts']}")
    print(f"OUT {out / 'staff-page-crosswalk.md'}")
    print("یادآوری: PARTIAL است؛ بدون commit+push شاهد رسمی نیست.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
