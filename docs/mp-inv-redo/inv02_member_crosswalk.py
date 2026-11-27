#!/usr/bin/env python3
"""INV-02 crosswalk generator — Muscle Paradise (PWA merged client).

چرا این فایل وجود دارد
----------------------
crosswalk عضو که نشست پیشین در `evidence/2026-11-23/INV-02/member-capability-crosswalk.md`
ادعا کرد، هرگز روی ریموت ظاهر نشد (نه commit، نه push) و با بسته‌شدن نشست از بین رفت.
این اسکریپت همان crosswalk را **از روی کد همان SHA** بازتولید می‌کند تا اعداد
قابل‌تکرار و قابل‌راستی‌آزمایی باشند، نه نقل‌قول از حافظه.

قواعدی که این اسکریپت رعایت می‌کند
----------------------------------
1. فقط‌خواندنی است؛ جز دو فایل خروجی خودش چیزی نمی‌نویسد.
2. هر «مصرف‌کنندهٔ React» با تطبیق واقعیِ مسیر در `mp-app/studio/src` پیدا می‌شود
   (الگوی `${API_BASE}/x` و literal `"/api/v1/x"`)، نه با جست‌وجوی نام feature.
3. ستون تست فقط وقتی پر می‌شود که فایل تستی **همان مسیر API** را نام ببرد؛
   اشارهٔ متنی به نام feature شاهد محسوب نمی‌شود (منبع مثبت کاذب در نسخهٔ v1 بود).
4. هیچ ردیفی `CURRENT` نمی‌شود. سقف ممکن `PARTIAL_REVIEW` است، چون مجوز سمت سرور
   با تست منفی (عضو A → دادهٔ عضو B) اثبات نشده است.
5. اگر مسیر API ادعایی در `routes.json` نباشد، ردیف `BLOCKED` می‌شود، نه GAP.

اجرا (از ریشهٔ مخزن MP، روی همان SHA تازهٔ ریموت)
------------------------------------------------
    python3 scripts/inv02_member_crosswalk.py --repo . --out evidence/$(date -u +%F)/INV-02/

خروجی: `member-capability-crosswalk.md` و `.json`.
بدون commit و push، خروجی «شاهد رسمی» نیست.
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

# ── نقشهٔ دامنه: پوشهٔ feature در Flutter → پیشوندهای مسیر API در endpoint واقعی ──
# این نقشه دستی است و باید با `mp-app/backend/api/routes.json` تطبیق داده شود.
# اگر پیشوندی در routes.json نبود، ردیف BLOCKED می‌شود — حدس زده نمی‌شود.
FEATURE_TO_API: dict[str, tuple[str, ...]] = {
    "auth": ("/api/v1/auth/",),
    "shell": ("/api/v1/auth/",),
    "home": ("/api/v1/members/me", "/api/v1/programs/member/", "/api/v1/notifications/member/"),
    "today": ("/api/v1/programs/member/", "/api/v1/workouts/", "/api/v1/nutrition/member/"),
    "profile": ("/api/v1/members/me", "/api/v1/auth/phone-change/"),
    "progress": ("/api/v1/assessments/", "/api/v1/members/{member_id}/weight"),
    "assessment14": ("/api/v1/assessments/",),
    "bodycomp": ("/api/v1/assessments/", "/api/v1/nutrition/member/"),
    "nutrition": ("/api/v1/nutrition/", "/api/v1/foods/"),
    "classes": ("/api/v1/classes/",),
    "checkin": ("/api/v1/face/", "/api/v1/checkins/", "/api/v1/attendance/"),
    "feedback": ("/api/v1/feedback/", "/api/v1/programs/"),
    "chat": ("/api/v1/chat/",),
    "notifications": ("/api/v1/notifications/",),
    "wallet": ("/api/v1/payments/", "/api/v1/members/memberships"),
    "shop": ("/api/v1/shop/",),
    "intake": ("/api/v1/population/", "/api/v1/assessments/intake"),
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


# ─────────────────────────── کمکی‌ها ───────────────────────────
def sh(*args: str, cwd: Path) -> str:
    try:
        return subprocess.run(args, cwd=cwd, capture_output=True, text=True).stdout.strip()
    except OSError:
        return ""


def sha256(path: Path) -> str | None:
    return hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None


def canon(path: str) -> str:
    """پارامتر مسیر را یکسان می‌کند و اسلش انتهایی و query را می‌ریزد."""
    return PLACEHOLDER.sub("*", path.split("?")[0].rstrip("/"))


def path_match(a: str, b: str) -> bool:
    """تطبیق segment-wise با احترام به وایلدکارد؛ `/a/{id}` با `/a/5` نمی‌خواند."""
    pa, pb = canon(a).split("/"), canon(b).split("/")
    if len(pa) != len(pb):
        return False
    return all(x == "*" or y == "*" or x == y for x, y in zip(pa, pb))


def under_prefix(path: str, prefix: str) -> bool:
    return canon(path).startswith(canon(prefix))


# ─────────────────────────── منابع ───────────────────────────
def load_routes(repo: Path) -> dict[str, set[str]]:
    """routes.json → {path: roles}. منبع مجوز همان چیزی است که سرور می‌سازد."""
    data = json.loads((repo / "mp-app/backend/api/routes.json").read_text(encoding="utf-8"))
    routes: dict[str, set[str]] = {}
    for op in data.get("operations", []):
        routes.setdefault(op["path"], set()).update(op.get("roles") or [])
    return routes


def flutter_features(repo: Path) -> dict[str, list[str]]:
    base = repo / "mp-app/client/lib/features"
    if not base.is_dir():
        return {}
    return {
        d.name: [str(p.relative_to(repo)) for p in sorted(d.rglob("*.dart"))]
        for d in sorted(p for p in base.iterdir() if p.is_dir())
    }


def react_call_sites(repo: Path) -> dict[str, set[str]]:
    """مسیر API (canonical) → فایل‌های Studio که آن را صدا می‌زنند."""
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


def api_test_sites(repo: Path) -> dict[str, set[str]]:
    """مسیر API → فایل‌های تستی که همان مسیر را نام می‌برند (شاهد متنی، نه اجرا)."""
    hits: dict[str, set[str]] = {}
    for root in (repo / "mp-app/studio/tests", repo / "mp-app/backend/tests"):
        if not root.is_dir():
            continue
        for path in root.rglob("*"):
            if not path.is_file() or path.suffix not in {".ts", ".tsx", ".py"}:
                continue
            text = path.read_text(encoding="utf-8", errors="ignore")
            for match in re.finditer(r"/api/v1/[A-Za-z0-9_/{}\-]+", text):
                hits.setdefault(canon(match.group(0)), set()).add(
                    str(path.relative_to(repo)))
    return hits


def studio_routes(repo: Path) -> list[str]:
    nav = repo / "mp-app/studio/src/lib/navigation.ts"
    if not nav.is_file():
        return []
    text = nav.read_text(encoding="utf-8")
    routes = set(re.findall(r'path === "(/[^"]*)"', text))
    routes.update(re.findall(r"`(/staff/[^`]*)`", text))
    return sorted(routes)


# ─────────────────────────── مدل ───────────────────────────
@dataclass
class Row:
    feature: str
    flutter: list[str]
    apis: list[str] = field(default_factory=list)
    consumed: list[str] = field(default_factory=list)
    consumers: list[str] = field(default_factory=list)
    tests: list[str] = field(default_factory=list)
    roles: list[str] = field(default_factory=list)
    status: str = "UNKNOWN"
    reason: str = ""


def classify(row: Row) -> None:
    if not row.apis:
        row.status = "BLOCKED"
        row.reason = ("هیچ مسیر API برای این دامنه در routes.json پیدا نشد؛ "
                      "نقشهٔ FEATURE_TO_API باید با تصمیم بازبینی شود")
        return
    if not row.consumed:
        row.status = "GAP"
        row.reason = (f"Flutter {len(row.flutter)} فایل دارد اما هیچ call-site در "
                      f"mp-app/studio/src به {len(row.apis)} مسیر این دامنه اشاره نمی‌کند")
        return
    if not row.tests:
        row.status = "GAP"
        row.reason = ("مصرف‌کنندهٔ React هست، ولی هیچ تستی همان مسیرهای مصرف‌شده را "
                      "نام نمی‌برد")
        return
    row.status = "PARTIAL_REVIEW"
    row.reason = ("مسیر + مصرف‌کننده + اشارهٔ تستی پیدا شد؛ مجوز/مالکیت با تست منفی "
                  "اثبات نشده و اجرای تست در این اجرا انجام نشده است")


def build(repo: Path) -> tuple[list[Row], dict]:
    routes = load_routes(repo)
    features = flutter_features(repo)
    calls = react_call_sites(repo)
    tests = api_test_sites(repo)

    rows: list[Row] = []
    for feature, files in features.items():
        prefixes = FEATURE_TO_API.get(feature)
        if prefixes is None:
            rows.append(Row(feature, files, status="BLOCKED",
                            reason="نقشهٔ دامنه برای این feature تعریف نشده — نیاز به تصمیم"))
            continue
        apis = sorted(p for p in routes if any(under_prefix(p, pref) for pref in prefixes))
        consumed = [a for a in apis if any(path_match(a, c) for c in calls)]
        consumers = sorted({f for c, files_ in calls.items() if any(path_match(a, c) for a in consumed)
                            for f in files_})
        testable = sorted({f for a in consumed for c, files_ in tests.items()
                           if path_match(a, c) for f in files_})
        row = Row(
            feature=feature,
            flutter=files,
            apis=apis,
            consumed=consumed,
            consumers=consumers,
            tests=testable,
            roles=sorted({r for a in consumed for r in routes[a]}),
        )
        classify(row)
        rows.append(row)

    counts: dict[str, int] = {}
    for row in rows:
        counts[row.status] = counts.get(row.status, 0) + 1

    meta = {
        "sha": sh("git", "rev-parse", "HEAD", cwd=repo),
        "branch": sh("git", "rev-parse", "--abbrev-ref", "HEAD", cwd=repo),
        "dirty": bool(sh("git", "status", "--porcelain", "--untracked-files=no", cwd=repo)),
        "untracked": len([ln for ln in sh("git", "status", "--porcelain", cwd=repo).splitlines()
                          if ln.startswith("??")]),
        "sources": {
            "backend/api/routes.json": sha256(repo / "mp-app/backend/api/routes.json"),
            "backend/security/rbac.py": sha256(repo / "mp-app/backend/security/rbac.py"),
            "studio/src/lib/navigation.ts": sha256(repo / "mp-app/studio/src/lib/navigation.ts"),
            "studio/src/lib/api.ts": sha256(repo / "mp-app/studio/src/lib/api.ts"),
        },
        "counts": {
            "flutter_features": len(rows),
            "server_routes": len(routes),
            "studio_call_paths": len(calls),
        },
        "status_counts": counts,
        "studio_routes": studio_routes(repo),
        "generated_by": "scripts/inv02_member_crosswalk.py",
    }
    return rows, meta


# ─────────────────────────── خروجی ───────────────────────────
def render_markdown(rows: list[Row], meta: dict) -> str:
    def cell_list(items: list[str], limit: int = 4, name: bool = True) -> str:
        if not items:
            return "—"
        shown = [Path(i).name if name else i for i in items[:limit]]
        more = f" +{len(items) - limit}" if len(items) > limit else ""
        return "<br>".join(f"`{s}`" for s in shown) + more

    head = [
        "# INV-02 — crosswalk capability عضو (بازسازیِ قابل‌تکرار)",
        "",
        "> **وضعیت سند:** `PARTIAL / NOT_ACCEPTED` — تولیدشده با اسکریپت روی SHA زیر.",
        "> این سند پذیرش محصول، اثبات مجوز یا مجوز انتشار نیست. نسخهٔ ادعاشده در نشست",
        "> پیشین هرگز push نشد؛ تنها راه معتبر، اجرای دوبارهٔ همین اسکریپت روی SHA تازه است.",
        "",
        f"- SHA: `{meta['sha']}` · branch: `{meta['branch']}` · "
        f"tracked-dirty: `{meta['dirty']}` · untracked: `{meta['untracked']}`",
    ]
    for name, digest in meta["sources"].items():
        head.append(f"- `{name}` → `{digest or 'MISSING'}`")
    head += [
        f"- featureهای Flutter: **{meta['counts']['flutter_features']}** · "
        f"مسیرهای API سرور: **{meta['counts']['server_routes']}** · "
        f"مسیرهای صدا‌زده‌شده در Studio: **{meta['counts']['studio_call_paths']}**",
        "- شمارش: " + " · ".join(f"`{k}={v}`" for k, v in sorted(meta["status_counts"].items())),
        "",
        "**افسانهٔ وضعیت**",
        "",
        "| وضعیت | معنا |",
        "|---|---|",
        "| `PARTIAL_REVIEW` | مسیر API + call-site واقعی + اشارهٔ تستی هر سه پیدا شد؛ مجوز/مالکیت اثبات نشده |",
        "| `GAP` | یا call-site نیست، یا هیچ تستی همان مسیر را نام نمی‌برد |",
        "| `BLOCKED` | مسیر API ادعایی در `routes.json` نیست، یا نقشهٔ دامنه تعریف نشده |",
        "| `CURRENT` | **در این نسخه هرگز صادر نمی‌شود** — نیازمند تست منفی + اجرای واقعی |",
        "",
        "> ستون «اشارهٔ تستی» یعنی فایل تستی همان مسیر را **نام می‌برد**؛ این شاهد اجرای",
        "> تست یا قبولی آن نیست. ستون نقش‌ها هم از `routes.json` می‌آید، نه از اثبات.",
        "",
        "| # | feature | Flutter | API مصرف‌شده / کل دامنه | call-site | اشارهٔ تستی | نقش‌های قرارداد | وضعیت | دلیل |",
        "|---|---|---|---|---|---|---|---|---|",
    ]
    def esc(text: str) -> str:
        """فقط محتوای سلول فرار داده می‌شود؛ جداکنندهٔ ستون‌ها دست‌نخورده می‌ماند."""
        return text.replace("|", "\\|").replace("\n", " ")

    body = []
    for i, row in enumerate(rows, 1):
        api_cell = f"{len(row.consumed)} / {len(row.apis)}" if row.apis else "0 / 0"
        cells = [
            str(i),
            f"`{row.feature}`",
            f"{len(row.flutter)} فایل",
            api_cell,
            cell_list(row.consumers),
            cell_list(row.tests),
            ", ".join(row.roles) or "—",
            f"**{row.status}**",
            row.reason,
        ]
        body.append("| " + " | ".join(esc(c) for c in cells) + " |")

    tail = [
        "",
        "## مسیرهای Studio (از `navigation.ts`)",
        "",
        "```",
        *(meta["studio_routes"] or ["(navigation.ts خوانده نشد)"]),
        "```",
        "",
        "## چه چیزی این سند اثبات نمی‌کند",
        "",
        "- مجوز سمت سرور: `rbac.py`/`routes.json` شاهد قرارداد است، نه اثبات اجرا.",
        "- مالکیت داده: هیچ تست منفی (عضو A → دادهٔ عضو B) در این اجرا انجام نشده.",
        "- `/member` در `navigation.ts` یک مسیر رزروشدهٔ fail-closed است، نه صفحهٔ ساخته‌شده.",
        "- نصب‌پذیری، offline، مرورگر/دستگاه واقعی و reviewer مستقل: اجرا نشده.",
        "",
        "## بازتولید",
        "",
        "```bash",
        "git fetch origin && git checkout --detach origin/main   # یا SHA هدف",
        "python3 scripts/inv02_member_crosswalk.py --repo . --out evidence/$(date -u +%F)/INV-02/",
        "```",
        "",
    ]
    return "\n".join(head + body + tail)


def main() -> int:
    ap = argparse.ArgumentParser(description="INV-02 member capability crosswalk generator")
    ap.add_argument("--repo", default=".")
    ap.add_argument("--out", required=True, help="پوشهٔ خروجی، مثلاً evidence/2026-11-27/INV-02")
    args = ap.parse_args()

    repo = Path(args.repo).resolve()
    out = Path(args.out)
    out = out if out.is_absolute() else repo / out

    required = repo / "mp-app/backend/api/routes.json"
    if not required.is_file():
        print(f"FATAL: {required} پیدا نشد. اسکریپت باید از ریشهٔ مخزن MP اجرا شود.", file=sys.stderr)
        return 2

    rows, meta = build(repo)
    out.mkdir(parents=True, exist_ok=True)
    (out / "member-capability-crosswalk.md").write_text(render_markdown(rows, meta), encoding="utf-8")
    (out / "member-capability-crosswalk.json").write_text(
        json.dumps({"meta": meta, "rows": [r.__dict__ for r in rows]},
                   ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(f"OK  sha={meta['sha'][:12] or '?'}  features={meta['counts']['flutter_features']}  "
          f"routes={meta['counts']['server_routes']}  {meta['status_counts']}")
    print(f"OUT {out / 'member-capability-crosswalk.md'}")
    if meta["dirty"]:
        print("WARN: worktree dirty است — خروجی به SHA تمیز نسبت داده نمی‌شود.", file=sys.stderr)
    print("یادآوری: تا commit+push نشود، این خروجی شاهد رسمی نیست.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
