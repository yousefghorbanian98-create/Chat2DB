#!/usr/bin/env python3
"""INV crosswalk v2 — رفع سه false-negative که بیلدر در review.md ثبت کرد.

چرا این فایل وجود دارد
----------------------
اسکریپت v1 فقط این سه الگو را می‌دید:
    ${API_BASE}/x    ·    getJson("/x")    ·    "/api/v1/x"
و همین باعث شد سه چیز از چشم بیفتد (بیلدر درست تشخیص داد):

  1. `adminApi.ts`: مسیرها با پارامتر پیش‌فرض `base = "/api/v1"` ساخته می‌شوند:
         sessionFetch(`${base}/admin/analytics/churn-risk`, …)
     → v1 هیچ call-site در Analytics پیدا نکرد (false-negative).

  2. `roleNav.ts`: ردیف‌هایی مثل `dashboard: { roles: ALL_STAFF }` از constant
     استفاده می‌کنند؛ پارسر v1 فقط `roles: [...]` لفظی را می‌خواند و alias را
     باز نمی‌کرد (ستون نقش خالی می‌شد).

  3. `api.ts`: بعضی مسیرها پویا هستند:
         `${API_BASE}/members/${id}/checkins`
     → v1 یا نمی‌دید یا به مسیر اشتباه نگاشت می‌کرد.

راه‌حل: یک اسکنر واحد و مشترک که هر سه را می‌بیند، به‌علاوهٔ ثبت صریح
«dynamic» در خروجی تا دیگر به‌عنوان GAP گزارش نشود.

قواعد سخت (بدون تغییر نسبت به v1)
---------------------------------
- فقط‌خواندنی؛ تنها فایل خروجی خودش را می‌نویسد.
- هیچ‌وقت CURRENT صادر نمی‌کند؛ سقف PARTIAL_REVIEW است.
- dynamic-call به‌عنوان «پوشش داده‌نشده» علامت می‌خورد، نه GAP و نه PASS.

اجرا (از ریشهٔ مخزن MP):
    python3 scripts/crosswalk_v2.py --repo . --out evidence/$(date -u +%F)/INV-02 --kind member
    python3 scripts/crosswalk_v2.py --repo . --out evidence/$(date -u +%F)/INV-03 --kind staff
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

PLACEHOLDER = re.compile(r"\{[^}]*\}|\$\{[^}]*\}")

# ── الگوهای call-site؛ هر کدام در کد واقعی دیده و تست شده‌اند ──
# 1) ${API_BASE}/x   یا   ${base}/x   (adminApi با پارامتر پیش‌فرض base)
# 2) getJson("/x") و خانواده‌اش
# 3) "/api/v1/x" لفظی
CALL_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("template-base", re.compile(r"""\$\{(?:API_BASE|base)\}(/[^"'`$\s]*)""")),
    ("helper", re.compile(
        r"""(?:getJson|postJson|putJson|patchJson|deleteJson|sessionFetch|request)"""
        r"""\s*(?:<[^>()]*>)?\(\s*[`"'](/[^`"'$\s]*)""")),
    ("literal", re.compile(r"""["'`](/api/v1/[^"'`\s]*)["'`]""")),
)

MEMBER_DOMAINS: dict[str, tuple[str, ...]] = {
    "auth": ("/api/v1/auth/",),
    "shell": ("/api/v1/auth/",),
    "home": ("/api/v1/members/me", "/api/v1/programs/member/", "/api/v1/notifications/member/"),
    "today": ("/api/v1/programs/member/", "/api/v1/workouts/", "/api/v1/nutrition/member/"),
    "profile": ("/api/v1/members/me", "/api/v1/auth/phone-change/"),
    "progress": ("/api/v1/assessments/",),
    "assessment14": ("/api/v1/assessments/",),
    "bodycomp": ("/api/v1/assessments/", "/api/v1/nutrition/member/"),
    "nutrition": ("/api/v1/nutrition/", "/api/v1/foods/"),
    "classes": ("/api/v1/classes/",),
    "checkin": ("/api/v1/face/", "/api/v1/checkins/", "/api/v1/members/me/checkins",
                "/api/v1/admin/checkins"),
    "feedback": ("/api/v1/feedback/", "/api/v1/programs/"),
    "chat": ("/api/v1/chat/",),
    "notifications": ("/api/v1/notifications/",),
    "wallet": ("/api/v1/payments/", "/api/v1/members/memberships"),
    "shop": ("/api/v1/shop/",),
    "intake": ("/api/v1/population/", "/api/v1/assessments/intake"),
}

STAFF_DOMAINS: dict[str, tuple[str, ...]] = {
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


# ─────────────────────── استخراج نقش‌ها با alias ───────────────────────
def role_constants(text: str) -> dict[str, list[str]]:
    """`const ALL_STAFF: readonly Role[] = ["a","b"]` → {"ALL_STAFF": ["a","b"]}."""
    out: dict[str, list[str]] = {}
    for m in re.finditer(r"const\s+([A-Z_][A-Z0-9_]*)\s*(?::[^=]+)?=\s*\[([^\]]*)\]", text):
        out[m.group(1)] = [v.strip().strip("\"'") for v in m.group(2).split(",") if v.strip()]
    return out


def role_rules(repo: Path) -> dict[str, list[str]]:
    path = repo / "mp-app/studio/src/lib/roleNav.ts"
    if not path.is_file():
        return {}
    text = path.read_text(encoding="utf-8")
    consts = role_constants(text)
    rules: dict[str, list[str]] = {}
    for m in re.finditer(r"(\w+):\s*\{[^}]*?roles:\s*(\[[^\]]*\]|[A-Z_][A-Z0-9_]*)", text, re.S):
        page, raw = m.group(1), m.group(2).strip()
        if raw.startswith("["):
            rules[page] = [v.strip().strip("\"'") for v in raw.strip("[]").split(",") if v.strip()]
        else:
            rules[page] = list(consts.get(raw, []))
    return rules


# ─────────────────────── استخراج call-site ───────────────────────
@dataclass
class CallSite:
    path: str          # canonical، مثلاً /api/v1/members/*/checkins
    raw: str           # همان چیزی که در کد بود
    file: str
    kind: str          # template-base | helper | literal
    dynamic: bool      # آیا متغیر غیرقابل‌حل داشته؟


def call_sites(repo: Path) -> list[CallSite]:
    studio = repo / "mp-app/studio/src"
    if not studio.is_dir():
        return []
    sites: list[CallSite] = []
    for ts in studio.rglob("*.ts*"):
        text = ts.read_text(encoding="utf-8", errors="ignore")
        for kind, pattern in CALL_PATTERNS:
            for m in pattern.finditer(text):
                raw = m.group(1)
                full = raw if raw.startswith("/api/") else "/api/v1" + raw
                dynamic = "$" in raw.replace("${", "")
                sites.append(CallSite(canon(full), raw, str(ts.relative_to(repo)), kind, dynamic))
    return sites


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


def server_routes(repo: Path) -> dict[str, set[str]]:
    data = json.loads((repo / "mp-app/backend/api/routes.json").read_text(encoding="utf-8"))
    routes: dict[str, set[str]] = {}
    for op in data.get("operations", []):
        routes.setdefault(op["path"], set()).update(op.get("roles") or [])
    return routes


@dataclass
class Row:
    key: str
    files: list[str]
    route: str | None = None
    roles: list[str] | None = None
    apis_used: list[str] = field(default_factory=list)
    apis_total: int = 0
    consumers: list[str] = field(default_factory=list)
    tests: list[str] = field(default_factory=list)
    uncovered_dynamic: list[str] = field(default_factory=list)
    status: str = "UNKNOWN"
    reason: str = ""


def classify(row: Row) -> None:
    if row.apis_total == 0:
        row.status, row.reason = "BLOCKED", "هیچ مسیر API در routes.json برای این دامنه نیست"
        return
    if row.uncovered_dynamic and not row.apis_used:
        row.status = "DYNAMIC_UNCOVERED"
        row.reason = ("فقط call-site پویا پیدا شد که با اسکنر استاتیک به مسیر مشخص "
                      "نگاشت نمی‌شود — نیاز به بررسی دستی، نه GAP")
        return
    if not row.apis_used:
        row.status, row.reason = "GAP", "هیچ call-site استاتیکی برای مسیرهای این دامنه نیست"
        return
    if not row.tests:
        row.status, row.reason = "GAP", "call-site هست ولی هیچ تستی همان مسیر را نام نمی‌برد"
        return
    row.status = "PARTIAL_REVIEW"
    row.reason = ("route/نقش + call-site + اشارهٔ تستی پیدا شد؛ مجوز با تست منفی "
                  "اثبات نشده و اجرای تست در این اجرا انجام نشده")


def build(repo: Path, kind: str) -> tuple[list[Row], dict]:
    domains = MEMBER_DOMAINS if kind == "member" else STAFF_DOMAINS
    routes = server_routes(repo)
    sites = call_sites(repo)
    tests = test_mentions(repo)
    rules = role_rules(repo)
    rows: list[Row] = []

    if kind == "member":
        base = repo / "mp-app/client/lib/features"
        entries = {d.name: [str(p.relative_to(repo)) for p in sorted(d.rglob("*.dart"))]
                   for d in sorted(p for p in base.iterdir() if p.is_dir())} if base.is_dir() else {}
    else:
        pages = repo / "mp-app/studio/src/pages"
        ids = []
        store = repo / "mp-app/studio/src/stores/appStore.ts"
        if store.is_file():
            m = re.search(r"PAGE_IDS\s*=\s*\[(.*?)\]\s*as const", store.read_text(encoding="utf-8"), re.S)
            ids = re.findall(r'"([a-z_]+)"', m.group(1)) if m else []
        entries = {}
        for page in ids:
            hits = [p for p in pages.glob("*.tsx") if p.stem.lower() == page.lower()]
            entries[page] = [str(hits[0].relative_to(repo))] if hits else []

    for key, files in entries.items():
        prefixes = domains.get(key)
        row = Row(key=key, files=files,
                  route=(f"/staff/{key}" if kind == "staff" else None),
                  roles=rules.get(key))
        if prefixes is None:
            row.status, row.reason = "BLOCKED", "نقشهٔ دامنه برای این مورد تعریف نشده"
            rows.append(row)
            continue
        apis = sorted(p for p in routes if any(under_prefix(p, pre) for pre in prefixes))
        used = [a for a in apis if any(path_match(a, s.path) for s in sites)]
        dyn = sorted({s.raw for s in sites if s.dynamic
                      and any(s.path.startswith(canon(pre).split("*")[0]) or
                              under_prefix(s.path, pre) for pre in prefixes)})
        row.apis_total, row.apis_used = len(apis), used
        row.consumers = sorted({Path(s.file).name for s in sites
                                if any(path_match(a, s.path) for a in used)})
        row.tests = sorted({Path(f).name for a in used for c, fs in tests.items()
                            if path_match(a, c) for f in fs})[:6]
        row.uncovered_dynamic = dyn[:5]
        classify(row)
        rows.append(row)

    counts: dict[str, int] = {}
    for r in rows:
        counts[r.status] = counts.get(r.status, 0) + 1

    meta = {
        "kind": kind,
        "sha": sh("git", "rev-parse", "HEAD", cwd=repo),
        "branch": sh("git", "rev-parse", "--abbrev-ref", "HEAD", cwd=repo),
        "tracked_dirty": bool(sh("git", "status", "--porcelain", "--untracked-files=no", cwd=repo)),
        "untracked": len([ln for ln in sh("git", "status", "--porcelain", cwd=repo).splitlines()
                          if ln.startswith("??")]),
        "sources": {
            "backend/api/routes.json": sha256(repo / "mp-app/backend/api/routes.json"),
            "backend/security/rbac.py": sha256(repo / "mp-app/backend/security/rbac.py"),
            "studio/src/lib/roleNav.ts": sha256(repo / "mp-app/studio/src/lib/roleNav.ts"),
            "studio/src/lib/api.ts": sha256(repo / "mp-app/studio/src/lib/api.ts"),
            "studio/src/lib/adminApi.ts": sha256(repo / "mp-app/studio/src/lib/adminApi.ts"),
            "studio/src/lib/navigation.ts": sha256(repo / "mp-app/studio/src/lib/navigation.ts"),
        },
        "site_kinds": {k: len([s for s in sites if s.kind == k]) for k, _ in CALL_PATTERNS},
        "dynamic_sites": len([s for s in sites if s.dynamic]),
        "status_counts": counts,
        "role_aliases_resolved": {k: v for k, v in rules.items() if v},
        "generated_by": "scripts/crosswalk_v2.py",
    }
    return rows, meta


def render(rows: list[Row], meta: dict) -> str:
    def esc(t) -> str:
        return str(t).replace("|", "\\|").replace("\n", " ")

    title = ("INV-02 — crosswalk عضو (v2)" if meta["kind"] == "member"
             else "INV-03 — crosswalk صفحات کارکنان (v2)")
    lines = [
        f"# {title}",
        "",
        "> **وضعیت:** `PARTIAL / NOT_ACCEPTED`. این نسخه سه false-negative نسخهٔ اول را",
        "> رفع می‌کند (تمپلیت `${base}`, alias نقش‌ها, مسیرهای پویا) — طبق یافته‌های",
        "> `review.md` خودِ اجرای قبلی. هیچ ردیفی CURRENT نمی‌شود.",
        "",
        f"- SHA: `{meta['sha']}` · branch: `{meta['branch']}` · "
        f"tracked-dirty: `{meta['tracked_dirty']}` · untracked: `{meta['untracked']}`",
    ]
    for name, digest in meta["sources"].items():
        lines.append(f"- `{name}` → `{digest or 'MISSING'}`")
    lines += [
        f"- call-site: `{meta['site_kinds']}` · پویا: **{meta['dynamic_sites']}**",
        "- شمارش: " + " · ".join(f"`{k}={v}`" for k, v in sorted(meta["status_counts"].items())),
        "",
        "| وضعیت | معنا |",
        "|---|---|",
        "| `PARTIAL_REVIEW` | route/نقش + call-site + اشارهٔ تستی؛ مجوز اثبات نشده |",
        "| `GAP` | call-site یا تست همان مسیر نیست |",
        "| `DYNAMIC_UNCOVERED` | فقط call پویا؛ اسکنر استاتیک نمی‌تواند نگاشت کند — بررسی دستی |",
        "| `BLOCKED` | مسیر/نقشهٔ دامنه وجود ندارد |",
        "| `CURRENT` | **هرگز در این نسخه صادر نمی‌شود** |",
        "",
        "| # | کلید | فایل | route | نقش‌ها (alias حل‌شده) | API مصرف‌شده/کل | call-site | پویای پوشش‌داده‌نشده | اشارهٔ تستی | وضعیت |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for i, r in enumerate(rows, 1):
        lines.append("| " + " | ".join(esc(c) for c in [
            str(i), f"`{r.key}`", f"{len(r.files)} فایل", f"`{r.route}`" if r.route else "—",
            ", ".join(r.roles or []) or "—",
            f"{len(r.apis_used)} / {r.apis_total}",
            "<br>".join(f"`{c}`" for c in r.consumers[:4]) or "—",
            "<br>".join(f"`{d}`" for d in r.uncovered_dynamic[:3]) or "—",
            "<br>".join(f"`{t}`" for t in r.tests[:4]) or "—",
            f"**{r.status}**",
        ]) + " |")
        if r.status != "PARTIAL_REVIEW":
            lines.append("| " + " | ".join(["", "", "", "", "", "", "", "", "", f"↳ {esc(r.reason)}"]) + " |")

    lines += [
        "",
        "## چه چیزی این نسخه هنوز اثبات نمی‌کند",
        "",
        "- مجوز سمت سرور؛ `routes.json`/`rbac.py` شاهد قرارداد است، نه اجرا.",
        "- مالکیت: تست منفی (عضو A → دادهٔ عضو B) در همین اجرا اجرا نشده.",
        "- تمایز «مصرف‌کنندهٔ صفحهٔ عضو» از «پنل کارکنان»: فایل مشترک است (`api.ts`,",
        "  `adminApi.ts`)؛ تفکیک کامپوننتی نیاز به مرور دستی دارد.",
        "- مرورگر/دستگاه/نصب‌پذیری و reviewer مستقل.",
        "",
        "## بازتولید",
        "",
        "```bash",
        f"python3 scripts/crosswalk_v2.py --repo . --kind {meta['kind']} --out evidence/<DATE>/INV-0{'2' if meta['kind'] == 'member' else '3'}",
        "```",
        "",
    ]
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".")
    ap.add_argument("--out", required=True)
    ap.add_argument("--kind", choices=("member", "staff"), required=True)
    args = ap.parse_args()

    repo = Path(args.repo).resolve()
    out = Path(args.out)
    out = out if out.is_absolute() else repo / out
    if not (repo / "mp-app/backend/api/routes.json").is_file():
        print("FATAL: از ریشهٔ مخزن MP اجرا کن.", file=sys.stderr)
        return 2

    rows, meta = build(repo, args.kind)
    if not rows:
        print("FATAL: هیچ ردیفی ساخته نشد — الگوی ورودی (features/ یا PAGE_IDS) شکسته است.",
              file=sys.stderr)
        return 3

    out.mkdir(parents=True, exist_ok=True)
    name = "member-capability-crosswalk" if args.kind == "member" else "staff-page-crosswalk"
    (out / f"{name}.md").write_text(render(rows, meta), encoding="utf-8")
    (out / f"{name}.json").write_text(
        json.dumps({"meta": meta, "rows": [r.__dict__ for r in rows]},
                   ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"OK  kind={args.kind}  sha={meta['sha'][:12] or '?'}  {meta['status_counts']}")
    print(f"OUT {out / (name + '.md')}")
    print("یادآوری: PARTIAL است؛ بدون commit+push شاهد رسمی نیست.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
