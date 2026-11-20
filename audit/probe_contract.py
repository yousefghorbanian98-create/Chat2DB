#!/usr/bin/env python3
"""کاوش قرارداد و سیم‌کشی — هر ۱۶۳ عملیات API، لایه به لایه.

سه پاس:
  پاس ۱ «seed زنده»: موجودیت‌های واقعی (عضو، اشتراک، پرداخت، کوپن، هزینه،
        سبد/سفارش، برنامه، اعلان، چت) از طریق **خودِ API** ساخته می‌شوند تا
        سیم‌کشی نوشتن‌ها اثبات شود و شناسه‌های واقعی برای پاس‌های بعد وجود داشته باشد.
  پاس ۲ «ماتریس مجوز»: هر عملیات × {بدون توکن، member, coach, reception, manager,
        admin, super_admin} ⇒ مقایسهٔ وضعیت واقعی با قراردادِ `api/routes.json`.
        خروجی: دسترسی بیش‌ازحد (خطرناک‌ترین)، انکار نابجا، drift قرارداد، 5xx.
  پاس ۳ «ورودی نامعتبر»: شناسهٔ منفی/صفر/بزرگ/رشته‌ای، رشتهٔ SQL/NoSQL، مسیر
        traversal، بدنهٔ بیش‌ازحد بزرگ ⇒ هیچ 500 یا نشت stack trace مجاز نیست.

اجرا: /tmp/run/venv/bin/python audit/probe_contract.py
"""
from __future__ import annotations

import itertools
import json
import random
import sys
import time
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any

import httpx

sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness_common import (  # noqa: E402
    BACKEND, BASE, ROLES, Stats, load_openapi, load_routes, write_evidence,
)

random.seed(20261120)  # قطعی و بازتولیدپذیر
TODAY = date(2026, 11, 20).isoformat()
# شناسهٔ یکتای هر اجرا (تصادفی قطعی برای *درون* اجرا، ولی یکتا بین اجراها تا
# ۴۰۹ «کد تخفیف قبلاً ثبت شده» مزاحم بازتولید نشود)
RUN = f"{int(time.time()) % 1000000:06d}"
# الگوی واقعی فیلد phone در schema: `^09\d{9}$` (یازده رقم) — Oracle باید به
# `pattern`/`minLength`/`minimum` منتشرشده در OpenAPI احترام بگذارد، وگرنه
# ۴۲۲ِ ساختگی تولید می‌کند و یافتهٔ کاذب می‌سازد.
PH1 = f"0913{RUN[-4:]}001"
PH2 = f"0913{RUN[-4:]}002"
PH3 = f"0913{RUN[-4:]}003"
CODE_PCT, CODE_FIX = f"H{RUN}P", f"H{RUN}F"
NOW_ISO = datetime(2026, 11, 20, 10, 0, tzinfo=timezone.utc).isoformat()

SPEC = load_openapi()
COMPS = SPEC.get("components", {}).get("schemas", {})
ROUTES = load_routes()
OPS_BY_KEY = {(r["method"], r["path"]): r for r in ROUTES}


def resolve(s: Any, depth: int = 0) -> dict:
    if depth > 5 or not isinstance(s, dict):
        return {}
    if "$ref" in s:
        return resolve(COMPS.get(s["$ref"].split("/")[-1], {}), depth + 1)
    out = dict(s)
    if "allOf" in out:
        merged: dict = {}
        for part in out["allOf"]:
            merged.update(resolve(part, depth + 1))
        out = merged
    return out


def op_spec(method: str, path: str) -> dict:
    return SPEC.get("paths", {}).get(path, {}).get(method.lower(), {})


# --------------------------------------------------------------------------
# ارکِل مقدار: نام فیلد → مقدار مصنوعی معتبر (بدون هیچ دادهٔ واقعی)
# --------------------------------------------------------------------------
PHONE_RE = "^09\d{9}$"          # الگوی واقعی phone در OpenAPI
COUPON_RE = "^[A-Z]{3,6}\\d{2,4}$"


def synth_for_pattern(pat: str) -> Any:
    """مقدار مصنوعی منطبق بر الگوهای regex منتشرشده در OpenAPI.

    نکتهٔ روش‌شناختی: ارکِل ممیز **باید** به `pattern`/`minLength`/`minimum`
    منتشرشده احترام بگذارد؛ وگرنه ۴۲۲ِ ساختگی تولید می‌کند و «یافتهٔ کاذب»
    می‌سازد. اینجا فقط الگوهای واقعاً موجود در پروژه پوشش داده شده‌اند.
    """
    if pat == PHONE_RE:
        return f"09{random.randint(10**8, 10**9 - 1)}"
    if pat == COUPON_RE:
        return f"HRNS{random.randint(10, 99)}"
    if pat.startswith("^") and "\d" in pat:
        digits = int(re.search(r"\{(\d+)\}", pat).group(1)) if re.search(r"\{(\d+)\}", pat) else 8
        return str(random.randint(10 ** (digits - 1), 10 ** digits - 1))
    return None



def value_for(name: str, sch: dict, ids: dict[str, Any], depth: int = 0) -> Any:
    sch = resolve(sch)
    if "enum" in sch and sch["enum"]:
        return sch["enum"][0]
    if "default" in sch and sch["default"] is not None:
        return sch["default"]
    ty = sch.get("type")
    n = name.lower()
    pat = sch.get("pattern")
    if pat:
        v = synth_for_pattern(pat)
        if v is not None:
            return v
    for key_name, mn, mx in (("amount_rial", 1, None), ("price_rial", 1, None), ("value", 1, 100)):
        pass  # سقف/کف در ادامه با minimum/maximum اعمال می‌شود
    if sch.get("minimum") is not None or sch.get("maximum") is not None:
        lo = sch.get("minimum", 1)
        hi = sch.get("maximum", lo + 100)
        return int((lo + hi) // 2)

    # شناسه‌های واقعی از seed
    for key, idname in (
        ("member_id", "member_id"), ("user_id", "user_id"), ("payment_id", "payment_id"),
        ("expense_id", "expense_id"), ("order_id", "order_id"), ("product_id", "product_id"),
        ("coupon", "coupon_id"), ("conversation_id", "conversation_id"),
        ("notification_id", "notification_id"), ("program_id", "program_id"),
        ("assessment_id", "assessment_id"), ("class_id", "class_id"), ("plan_id", "plan_id"),
        ("entry_id", "entry_id"), ("gateway_id", "gateway_id"), ("item_id", "item_id"),
        ("checkin_id", "checkin_id"), ("session_id", "session_id"), ("grant_id", "grant_id"),
        ("request_id", "change_request_id"), ("exercise_id", "exercise_id"),
    ):
        if n == key and idname in ids:
            return ids[idname]

    if n in ("phone", "member_phone"):
        return f"0913{random.randint(1000000, 9999999)}"
    if n.endswith("_rial") or n in ("amount", "amount_rial", "price_rial", "value"):
        return 50000
    if n in ("spent_on", "run_date", "date", "on_date", "day"):
        return TODAY
    if n.endswith("_at") or n in ("expires_at", "starts_at", "valid_until"):
        return (datetime(2026, 12, 20, 10, 0, tzinfo=timezone.utc)).isoformat()
    if n in ("height_cm",):
        return 178
    if n in ("weight_kg",):
        return 78.5
    if n in ("duration_days",):
        return 30
    if n in ("qty", "sets", "reps", "count"):
        return 3
    if n in ("idempotency_key",):
        return f"harness-{random.randint(10**9, 10**10)}"
    if n in ("code",):
        return f"HRNS{random.randint(1000, 9999)}"
    if ty == "array":
        item = resolve(sch.get("items", {}))
        if not item:
            return []
        if item.get("type") == "object" or "properties" in item:
            return [build_object(item, ids, depth + 1)]
        return [value_for("item", item, ids, depth + 1)]
    if ty == "object":
        return build_object(sch, ids, depth + 1)
    if ty == "integer":
        return 1
    if ty == "number":
        return 1.0
    if ty == "boolean":
        return False
    return f"harness-{n}"[:60]


def build_object(sch: dict, ids: dict[str, Any], depth: int = 0) -> dict:
    sch = resolve(sch)
    props = sch.get("properties", {})
    required = set(sch.get("required", []))
    out: dict[str, Any] = {}
    if depth > 3:
        return out
    for name, sub in props.items():
        if name in required or depth == 0:
            out[name] = value_for(name, sub, ids, depth + 1)
    return out


def body_for(method: str, path: str, ids: dict[str, Any]) -> Any | None:
    rb = op_spec(method, path).get("requestBody")
    if not rb:
        return None
    content = rb.get("content", {})
    js = content.get("application/json", {}).get("schema")
    if js is not None:
        sch = resolve(js)
        if sch.get("type") == "array" or "properties" in sch:
            return build_object(sch, ids) if "properties" in sch else [build_object(sch, ids)]
        return None
    return None


def fill_path(path: str, ids: dict[str, Any]) -> str:
    import re

    out = path
    for token in re.findall(r"\{(\w+)\}", path):
        n = token.lower()
        val: Any = ids.get(n)
        if val is None:
            if n.endswith("_id"):
                val = ids.get(n[:-3] + "_id", 1)
            elif n in ("key",):
                val = "harness.key"
            elif n in ("job_key",):
                val = "finance.daily"
            elif n in ("run_date", "date"):
                val = TODAY
            else:
                val = 1
        out = out.replace("{" + token + "}", str(val))
    return out


# --------------------------------------------------------------------------
# پاس ۱ — seed زنده با خودِ API
# --------------------------------------------------------------------------
SEED_STEPS: list[tuple[str, str, str, dict, str | None]] = [
    # (label, method, path, body, id_key_to_capture)
    ("member.create", "POST", "/api/v1/members",
     {"phone": PH1, "full_name": "عضو مصنوعی ۱", "gender": "male", "height_cm": 178}, "member_id"),
    ("member.create2", "POST", "/api/v1/members",
     {"phone": PH2, "full_name": "عضو مصنوعی ۲", "gender": "female", "height_cm": 165}, "member_id2"),
    ("membership.create", "POST", "/api/v1/members/memberships",
     {"member_id": "@member_id", "plan_name": "یک ماهه", "duration_days": 30, "price_rial": 1500000}, "membership_id"),
    ("coupon.percent", "POST", "/api/v1/payments/coupons",
     {"code": CODE_PCT, "kind": "percent", "value": 10, "max_uses": 2,
      "expires_at": "2026-12-30T10:00:00+00:00"}, "coupon_id"),
    ("coupon.fixed", "POST", "/api/v1/payments/coupons",
     {"code": CODE_FIX, "kind": "fixed", "value": 50000, "max_uses": 1}, None),
    ("payment.cash", "POST", "/api/v1/payments",
     {"member_id": "@member_id", "amount_rial": 1500000, "method": "cash",
      "description": "پرداخت مصنوعی harness", "idempotency_key": f"harness-pay-{RUN}"}, "payment_id"),
    ("payment.with_coupon", "POST", "/api/v1/payments",
     {"member_id": "@member_id", "amount_rial": 1500000, "method": "cash",
      "coupon_code": CODE_PCT, "idempotency_key": f"harness-pay2-{RUN}"}, "payment_id2"),
    ("wallet.charge", "POST", "/api/v1/payments/wallet/charge",
     {"member_id": "@member_id", "amount_rial": 500000, "description": "شارژ مصنوعی",
      "idempotency_key": f"harness-wallet-{RUN}"}, None),
    ("expense.create", "POST", "/api/v1/expenses",
     {"amount_rial": 250000, "category": "rent", "spent_on": TODAY, "payee": "مالک ساختمان",
      "note": "هزینهٔ مصنوعی harness"}, "expense_id"),
    ("shop.cart_add", "POST", "/api/v1/shop/cart", {"product_id": "@product_id", "qty": 2}, "cart_item_id"),
    ("shop.checkout", "POST", "/api/v1/shop/checkout", {"method": "wallet", "note": "harness"}, "order_id"),
    ("nutrition.weight", "POST", "/api/v1/nutrition/weight-logs",
     {"member_id": "@member_id", "entries": [{"weight_kg": 78.5, "logged_for_date": TODAY}]}, None),
    ("notification.create", "POST", "/api/v1/notifications",
     {"member_id": "@member_id", "title": "اعلان مصنوعی", "body": "harness", "kind": "general"}, "notification_id"),
    ("chat.conversation", "POST", "/api/v1/chat/conversations",
     {"member_id": "@member_id", "subject": "گفت‌وگوی مصنوعی"}, "conversation_id"),
    ("class.create", "POST", "/api/v1/classes",
     {"name": "کلاس مصنوعی", "capacity": 10, "starts_at": "2026-12-01T17:00:00+00:00"}, "class_id"),
    ("member.create3_for_shop", "POST", "/api/v1/members",
     {"phone": PH3, "full_name": "عضو مصنوعی ۳", "gender": "male", "height_cm": 180}, "member_id3"),
]


def run_seed(pr: Any, stats: Stats) -> dict[str, Any]:
    ids: dict[str, Any] = {}
    with httpx.Client(base_url=BASE, timeout=60.0) as c:
        # شناسه‌های پایه از DB
        import sqlite3

        from harness_common import DB

        db = sqlite3.connect(DB)
        for tbl, key in (("products", "product_id"), ("users", "user_id"),
                         ("product_categories", "category_id")):
            row = db.execute(f"select id from {tbl} order by id limit 1").fetchone()
            if row:
                ids[key] = row[0]
        db.close()

        for label, method, path, body, capture in SEED_STEPS:
            payload = json.loads(json.dumps(body))

            def sub(o: Any) -> Any:
                if isinstance(o, dict):
                    return {k: sub(v) for k, v in o.items()}
                if isinstance(o, list):
                    return [sub(v) for v in o]
                if isinstance(o, str) and o.startswith("@"):
                    return ids.get(o[1:], o)
                return o

            payload = sub(payload)
            role = "admin"
            t0 = time.perf_counter()
            try:
                r = c.request(method, path, json=payload, headers=pr.headers(role))
                ms = round((time.perf_counter() - t0) * 1000, 1)
                try:
                    data = r.json()
                except Exception:
                    data = {"raw": r.text[:200]}
                ok = r.status_code < 400
                if ok and capture:
                    for cand in ("id", f"{capture.replace('_id', '')}_id", "member_id", "payment_id"):
                        if isinstance(data, dict) and cand in data:
                            ids[capture] = data[cand]
                            break
                    else:
                        if isinstance(data, dict):
                            for k, v in data.items():
                                if k.endswith("_id") or k == "id":
                                    ids.setdefault(capture, v)
                stats.add(pass_="seed", label=label, method=method, path=path,
                          status=r.status_code, ok=ok, ms=ms,
                          response_keys=list(data)[:8] if isinstance(data, dict) else None,
                          error=None if ok else json.dumps(
                              data.get("error", data), ensure_ascii=False)[:400])
                print(f"  [{'OK ' if ok else 'FAIL'}] {label:<22} {r.status_code} {ms:>7}ms "
                      f"{'' if ok else str(data)[:110]}")
            except Exception as exc:  # noqa: BLE001
                stats.add(pass_="seed", label=label, method=method, path=path,
                          status=None, ok=False, ms=None, error=f"{type(exc).__name__}: {exc}")
                print(f"  [ERR ] {label:<22} {type(exc).__name__}: {exc}")
    return ids


# --------------------------------------------------------------------------
# پاس ۲ — ماتریس مجوز روی هر ۱۶۳ عملیات
# --------------------------------------------------------------------------
def classify(status: int | None) -> str:
    if status is None:
        return "transport_error"
    if status in (401, 403):
        return "denied"
    if 200 <= status < 300:
        return "allowed_2xx"
    if 400 <= status < 500:
        return "reached_4xx"      # authorization passed, business/validation rejected
    if status >= 500:
        return "server_error_5xx"
    return f"other_{status}"


def run_matrix(pr: Any, ids: dict[str, Any], stats: Stats) -> dict[str, Any]:
    principals: list[str | None] = [None, *ROLES]
    findings: dict[str, list] = {"unauth_allowed": [], "over_permissive": [],
                                 "contract_drift_denied": [], "server_errors": [],
                                 "leaked_stacktrace": [], "slow_ops": []}
    summary: dict[str, int] = {}
    with httpx.Client(base_url=BASE, timeout=60.0) as c:
        for r in ROUTES:
            method, path = r["method"], r["path"]
            allowed_roles = set(r.get("roles") or [])
            guards = r.get("guards") or []
            url = fill_path(path, ids)
            body = body_for(method, path, ids)
            for role in principals:
                t0 = time.perf_counter()
                try:
                    resp = c.request(method, url, json=body, headers=pr.headers(role))
                    status: int | None = resp.status_code
                    text = resp.text
                except Exception as exc:  # noqa: BLE001
                    status, text = None, f"{type(exc).__name__}: {exc}"
                ms = round((time.perf_counter() - t0) * 1000, 1)
                cls = classify(status)
                summary[cls] = summary.get(cls, 0) + 1
                expected_allowed = (role is None and not guards) or (role in allowed_roles)
                leaked = isinstance(text, str) and ("Traceback (most recent call last)" in text
                                                     or 'File "' in text and "line " in text)
                row = dict(pass_="rbac", method=method, path=path, url=url, role=role,
                           guards=guards, contract_roles=sorted(allowed_roles), status=status,
                           classification=cls, expected_allowed=expected_allowed, ms=ms,
                           body_head=(text[:160] if isinstance(text, str) else None))
                stats.add(**row)
                if role is None and cls == "allowed_2xx":
                    findings["unauth_allowed"].append({"method": method, "path": path, "status": status})
                if role is not None and role not in allowed_roles and guards and cls in (
                        "allowed_2xx", "reached_4xx"):
                    findings["over_permissive"].append(
                        {"method": method, "path": path, "role": role, "status": status,
                         "contract_roles": sorted(allowed_roles)})
                if role in allowed_roles and cls == "denied":
                    findings["contract_drift_denied"].append(
                        {"method": method, "path": path, "role": role, "status": status})
                if cls == "server_error_5xx":
                    findings["server_errors"].append(
                        {"method": method, "path": path, "role": role, "status": status,
                         "body_head": row["body_head"]})
                if leaked:
                    findings["leaked_stacktrace"].append({"method": method, "path": path, "role": role})
                if ms > 1500:
                    findings["slow_ops"].append({"method": method, "path": path, "role": role, "ms": ms})
    return {"summary": summary, "findings": findings}


# --------------------------------------------------------------------------
# پاس ۳ — ورودی نامعتبر / خصمانه
# --------------------------------------------------------------------------
BAD_IDS = ["-1", "0", "-9223372036854775808", "99999999999999999999999",
           "1e5", "abc", "1%20OR%201=1", "1;DROP%20TABLE%20users",
           "%2e%2e%2f%2e%2e%2fetc%2fpasswd", "null", "1.5", "-0"]
HOSTILE_STRINGS = ["' OR 1=1 --", "\"; DROP TABLE users; --", "<script>alert(1)</script>",
                   "../../etc/passwd", "%00", "ا" * 5000, "\r\nInjected: header", "{{7*7}}"]


def run_invalid(pr: Any, ids: dict[str, Any], stats: Stats) -> dict[str, Any]:
    findings: dict[str, list] = {"server_errors": [], "leaked_stacktrace": [],
                                 "unexpected_2xx": [], "bad_error_envelope": []}
    targets = [p for p in ROUTES if "{" in p["path"]]
    with httpx.Client(base_url=BASE, timeout=60.0) as c:
        for r in targets:
            import re

            tokens = re.findall(r"\{(\w+)\}", r["path"])
            for bad in BAD_IDS:
                url = r["path"]
                for tk in tokens:
                    url = url.replace("{" + tk + "}", bad)
                body = body_for(r["method"], r["path"], ids)
                try:
                    resp = c.request(r["method"], url, json=body, headers=pr.headers("admin"))
                    status, text = resp.status_code, resp.text
                except Exception as exc:  # noqa: BLE001
                    status, text = None, str(exc)
                cls = classify(status)
                stats.add(pass_="invalid", kind="bad_path_id", method=r["method"], path=r["path"],
                          injected=bad, status=status, classification=cls,
                          body_head=text[:200] if isinstance(text, str) else None)
                if cls == "server_error_5xx":
                    findings["server_errors"].append({"method": r["method"], "path": r["path"],
                                                      "injected": bad, "status": status,
                                                      "body_head": text[:200]})
                if "Traceback" in (text or ""):
                    findings["leaked_stacktrace"].append({"path": r["path"], "injected": bad})
                if cls == "allowed_2xx" and bad in ("-1", "abc", "null", "1e5"):
                    findings["unexpected_2xx"].append({"method": r["method"], "path": r["path"],
                                                       "injected": bad, "status": status})
                if status is not None and status >= 400:
                    try:
                        env = json.loads(text)
                        if not isinstance(env, dict) or not (
                                {"detail"} & set(env) or {"error"} & set(env)
                                or {"code"} & set(env) or {"message"} & set(env)):
                            findings["bad_error_envelope"].append(
                                {"path": r["path"], "status": status, "keys": list(env)[:6]})
                    except Exception:
                        findings["bad_error_envelope"].append(
                            {"path": r["path"], "status": status, "non_json": text[:80]})
        # رشته‌های خصمانه در بدنه
        for hostile in HOSTILE_STRINGS:
            for path, body in (("/api/v1/members", {"phone": hostile, "full_name": hostile,
                                                     "gender": "male"}),
                               ("/api/v1/expenses", {"amount_rial": 1000, "category": "rent",
                                                     "spent_on": TODAY, "note": hostile}),
                               ("/api/v1/payments/coupons", {"code": hostile, "kind": "percent",
                                                             "value": 5})):
                try:
                    resp = c.post(path, json=body, headers=pr.headers("admin"))
                    status, text = resp.status_code, resp.text
                except Exception as exc:  # noqa: BLE001
                    status, text = None, str(exc)
                cls = classify(status)
                stats.add(pass_="invalid", kind="hostile_body", path=path, injected=hostile[:40],
                          status=status, classification=cls, body_head=text[:200] if isinstance(text, str) else None)
                if cls == "server_error_5xx":
                    findings["server_errors"].append({"path": path, "hostile": hostile[:40],
                                                      "status": status, "body_head": text[:200]})
                if "Traceback" in (text or ""):
                    findings["leaked_stacktrace"].append({"path": path, "hostile": hostile[:40]})
    return findings


def load_ids() -> dict[str, Any]:
    prev = Path(__file__).resolve().parent / "evidence" / "contract-rbac-findings.json"
    if prev.exists():
        return json.loads(prev.read_text(encoding="utf-8")).get("ids", {})
    return {}


def main() -> None:
    from harness_common import Principals

    stats = Stats()
    print("== principals (OTP login for 7 identities) ==")
    pr = Principals()
    for role in ROLES:
        print(f"  token[{role}] len={len(pr.tokens[role])} user_id={pr.user_ids.get(role)}")

    which = sys.argv[1] if len(sys.argv) > 1 else "all"

    print("\n== pass 1: live seed through the API ==")
    ids = run_seed(pr, stats) if which in ("all", "seed") else load_ids()
    print("  captured ids:", json.dumps({k: v for k, v in ids.items()}, ensure_ascii=False)[:400])

    if which not in ("all", "matrix", "invalid"):
        stats.dump("contract-matrix-raw.json")
        return
    print(f"\n== pass 2: authorization matrix ({len(ROUTES)} ops × {len(ROLES)+1} principals) ==")
    t0 = time.time()
    matrix = run_matrix(pr, ids, stats)
    print(f"  done in {time.time()-t0:.0f}s | classification summary: {json.dumps(matrix['summary'])}")
    for k, v in matrix["findings"].items():
        print(f"  {k}: {len(v)}")
    write_evidence("contract-rbac-findings.json", {"ids": ids, **matrix})

    if which not in ("all", "invalid"):
        return
    print("\n== pass 3: invalid / hostile inputs ==")
    t0 = time.time()
    inv = run_invalid(pr, ids, stats)
    print(f"  done in {time.time()-t0:.0f}s")
    for k, v in inv.items():
        print(f"  {k}: {len(v)}")
    write_evidence("contract-invalid-findings.json", inv)

    p = stats.dump("contract-matrix-raw.json")
    print(f"\nraw rows → {p} ({len(stats.rows)} records)")


if __name__ == "__main__":
    main()
