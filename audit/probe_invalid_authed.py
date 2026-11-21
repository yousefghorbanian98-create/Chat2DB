#!/usr/bin/env python3
"""پاس ورودی خصمانه — نسخهٔ اصلاح‌شده با احراز هویتِ تأییدشده.

چرا این اسکریپت لازم شد
-----------------------
در اجرای نخست (`probe_contract.py`) پاس سوم با توکنی اجرا شد که در پاس‌های قبل
با `logout-all` باطل شده بود؛ نتیجه ۶۶۴ سلول از ۸۰۴ سلول `401 «نشست معتبر نیست»`
شد و بدنه/شناسهٔ خصمانه هرگز به لایهٔ اعتبارسنجی نرسید ⇒ آن پاس **نادرس‌نتیجه** بود.

این اسکریپت همان ماتریس خصمانه را با توکن **زنده و تأییدشده** اجرا می‌کند:
  ۱. ورود واقعی با OTP برای هر نقش (بدون فراخوانی logout-all در طول اجرا)
  ۲. canary پیش از اجرا و پس از اجرا (اثبات اینکه توکن در تمام مدت معتبر بود)
  ۳. در صورت مشاهدهٔ `401 نشست معتبر نیست` ⇒ ورود دوباره و تکرار همان سلول
     (و ثبت `retried_after_relogin` تا قابل حسابرسی باشد)

خروجی: audit/evidence/contract-invalid-authed.json
"""

from __future__ import annotations

import json
import time
from datetime import datetime, timezone
from typing import Any

import httpx

from harness_common import BASE, Principals, write_evidence
from probe_contract import BAD_IDS, HOSTILE_STRINGS, ROUTES, body_for, classify, load_ids

# مسیرهای دارای پارامتر (همان دامنهٔ پاس نخست)
TEMPLATED = [r for r in ROUTES if "{" in r["path"]]

# مسیرهایی که برای نقش member هم معنادارند (بررسی وابستگی اعتبارسنجی به نقش)
MEMBER_PATHS = [
    "/api/v1/nutrition/food-logs/member/{member_id}/daily",
    "/api/v1/assessments/member/{member_id}",
    "/api/v1/payments/{payment_id}/receipt",
    "/api/v1/shop/products/{product_id}",
    "/api/v1/members/{member_id}",
]

# نشانهٔ توکنِ باطل‌شده (نه خطای مجوز)
REVOKED_MARKERS = ("نشست معتبر نیست", "session_invalid", "invalid_session", "token_revoked")


def canary(pr: Principals, role: str, path: str = "/api/v1/members/me") -> dict[str, Any]:
    """یک درخواست ساده برای اثبات زنده بودن توکن؛ هیچ‌وقت logout صدا نمی‌زند."""
    with httpx.Client(base_url=BASE, timeout=30.0) as c:
        r = c.get(path, headers=pr.headers(role))
        return {"role": role, "path": path, "status": r.status_code,
                "body_head": r.text[:160], "token_is_live": r.status_code != 401}


def is_revoked(status: int | None, body: str) -> bool:
    return status == 401 and any(m in body for m in REVOKED_MARKERS)


def main() -> None:
    started = datetime.now(timezone.utc).isoformat(timespec="seconds")
    t0 = time.time()
    pr = Principals()
    ids = load_ids()

    canary_before = [canary(pr, "admin"), canary(pr, "member")]
    assert all(c["token_is_live"] for c in canary_before), \
        f"توکن زنده نیست — اجرا متوقف شد: {canary_before}"

    relogins = 0
    cells: list[dict[str, Any]] = []
    findings: dict[str, list] = {
        "server_errors_5xx": [], "leaked_stacktrace": [], "unexpected_2xx_on_bad_id": [],
        "bad_error_envelope": [], "revoked_token_cells": [], "id_guard_rejections": [],
    }

    def request(method: str, url: str, body: Any, role: str, kind: str, injected: str,
                path_tmpl: str) -> None:
        nonlocal relogins
        with httpx.Client(base_url=BASE, timeout=60.0) as c:
            r = c.request(method, url, json=body, headers=pr.headers(role))
            status, text = r.status_code, r.text
        retried = False
        if is_revoked(status, text):                       # توکن در حین اجرا باطل شد
            findings["revoked_token_cells"].append({"role": role, "path": path_tmpl,
                                                    "injected": injected, "status": status})
            relogins += 1
            fresh = Principals()                           # ورود کامل دوباره
            pr.tokens[role] = fresh.tokens[role]
            with httpx.Client(base_url=BASE, timeout=60.0) as c:
                r = c.request(method, url, json=body, headers=pr.headers(role))
                status, text = r.status_code, r.text
            retried = True
        cls = classify(status)
        cells.append({"pass_": "invalid_authed", "kind": kind, "role": role, "method": method,
                      "path": path_tmpl, "url": url, "injected": injected, "status": status,
                      "classification": cls, "retried_after_relogin": retried,
                      "body_head": (text[:200] if isinstance(text, str) else None)})
        if cls == "server_error_5xx":
            findings["server_errors_5xx"].append({"role": role, "method": method, "path": path_tmpl,
                                                  "injected": injected, "status": status,
                                                  "body_head": text[:200]})
        if "Traceback" in (text or "") or "File \"/" in (text or ""):
            findings["leaked_stacktrace"].append({"role": role, "path": path_tmpl,
                                                  "injected": injected, "body_head": text[:200]})
        if cls == "allowed_2xx" and kind == "bad_path_id":
            findings["unexpected_2xx_on_bad_id"].append({"role": role, "method": method,
                                                         "path": path_tmpl, "injected": injected,
                                                         "status": status})
        if cls == "reached_4xx" and "invalid_id" in (text or ""):
            findings["id_guard_rejections"].append({"role": role, "path": path_tmpl,
                                                    "injected": injected})
        if status is not None and status >= 400:
            try:
                env = json.loads(text)
                ok = isinstance(env, dict) and ({"error", "detail", "code", "message"} & set(env))
                if not ok:
                    findings["bad_error_envelope"].append({"path": path_tmpl, "status": status,
                                                           "keys": list(env)[:6]})
            except Exception:                              # noqa: BLE001
                if not (text or "").lstrip().startswith("<!doctype"):   # صفحهٔ HTML درگاه عمدی است
                    findings["bad_error_envelope"].append({"path": path_tmpl, "status": status,
                                                           "non_json": (text or "")[:80]})

    # --- ۱) شناسه‌های نامعتبر روی همهٔ مسیرهای پارامتردار، با نقش admin ---
    import re

    for r in TEMPLATED:
        tokens = re.findall(r"\{(\w+)\}", r["path"])
        for bad in BAD_IDS:
            url = r["path"]
            for tk in tokens:
                url = url.replace("{" + tk + "}", bad)
            request(r["method"], url, body_for(r["method"], r["path"], ids), "admin",
                    "bad_path_id", bad, r["path"])

    # --- ۲) همان شناسه‌ها با نقش member روی مسیرهای عضو (وابستگی به نقش) ---
    for tmpl in MEMBER_PATHS:
        spec = next((x for x in ROUTES if x["path"] == tmpl), None)
        if spec is None:
            continue
        tokens = re.findall(r"\{(\w+)\}", tmpl)
        for bad in BAD_IDS:
            url = tmpl
            for tk in tokens:
                url = url.replace("{" + tk + "}", bad)
            request(spec["method"], url, body_for(spec["method"], tmpl, ids), "member",
                    "bad_path_id_member", bad, tmpl)

    # --- ۳) رشته‌های خصمانه در بدنه، با احراز هویت واقعی ---
    for hostile in HOSTILE_STRINGS:
        for role, path, body in (
            ("admin", "/api/v1/members", {"phone": hostile, "full_name": hostile, "gender": "male"}),
            ("admin", "/api/v1/expenses", {"amount_rial": 1000, "category": "rent",
                                           "spent_on": "2026-11-20", "note": hostile}),
            ("admin", "/api/v1/payments/coupons", {"code": hostile, "kind": "percent", "value": 5}),
            ("member", "/api/v1/nutrition/weight-logs", {"weight_kg": 80.5,
                                                         "logged_for_date": "2026-11-20",
                                                         "note": hostile}),
        ):
            request("POST", path, body, role, "hostile_body", hostile[:40], path)

    canary_after = [canary(pr, "admin"), canary(pr, "member")]

    hist: dict[str, int] = {}
    for c in cells:
        hist[str(c["status"])] = hist.get(str(c["status"]), 0) + 1
    by_kind: dict[str, dict[str, int]] = {}
    for c in cells:
        d = by_kind.setdefault(c["kind"], {})
        d[str(c["status"])] = d.get(str(c["status"]), 0) + 1

    payload = {
        "generated_at": started,
        "elapsed_s": round(time.time() - t0, 1),
        "why": ("پاس سومِ اجرای نخست با توکن باطل‌شده اجرا شد (۶۶۴ سلول ۴۰۱ «نشست معتبر نیست»)؛"
                " این اجرا همان ماتریس را با توکن زنده و canary تأییدشده تکرار می‌کند"),
        "base": BASE,
        "cells_total": len(cells),
        "status_histogram": dict(sorted(hist.items(), key=lambda x: -x[1])),
        "by_kind": by_kind,
        "relogins": relogins,
        "revoked_token_cells": len(findings["revoked_token_cells"]),
        "canary_before": canary_before,
        "canary_after": canary_after,
        "tokens_live_throughout": all(c["token_is_live"] for c in canary_before + canary_after),
        "findings": {k: v for k, v in findings.items()},
        "finding_counts": {k: len(v) for k, v in findings.items()},
        "cells": cells,
    }
    p = write_evidence("contract-invalid-authed.json", payload)
    print(f"cells={len(cells)} elapsed={payload['elapsed_s']}s relogins={relogins} "
          f"tokens_live={payload['tokens_live_throughout']}")
    print("status:", payload["status_histogram"])
    print("finding_counts:", payload["finding_counts"])
    for f in ("server_errors_5xx", "leaked_stacktrace", "unexpected_2xx_on_bad_id"):
        for item in findings[f][:12]:
            print(f"  {f}: {json.dumps(item, ensure_ascii=False)[:220]}")
    print("canary_after:", json.dumps(canary_after, ensure_ascii=False)[:300])
    print("wrote", p)


if __name__ == "__main__":
    main()
