#!/usr/bin/env python3
"""لایهٔ مشترک harness — احراز هویت واقعی، کلاینت HTTP، و نویسندهٔ شاهد.

هیچ فایلی در مخزن `MP` تغییر نمی‌کند: این کد فقط **از بیرون** به اپِ در حال
اجرا (پورت ۸۰۱۰) و به DB محلی harness وصل می‌شود. کاربران نقش‌دار همگی
**مصنوعی** و با شماره‌های الگوی seed خودِ پروژه (`0912…`) ساخته می‌شوند.
"""
from __future__ import annotations

import json
import os
import sqlite3
import sys
import time
from pathlib import Path
from typing import Any

import httpx

BASE = os.environ.get("MP_BASE_URL", "http://127.0.0.1:8010")
BACKEND = "/tmp/run/MP/mp-app/backend"
DB = "/tmp/run/data/mp.db"
EVIDENCE = Path(os.environ.get("AUDIT_EVIDENCE", "/home/user/Chat2DB/audit/evidence"))
EVIDENCE.mkdir(parents=True, exist_ok=True)

# همان متغیرهای محیطیِ پروسهٔ سرور (تا امضای JWT یکی باشد)
os.environ.setdefault("MP_ENVIRONMENT", "development")
os.environ.setdefault("MP_DATABASE_URL", "sqlite:////tmp/run/data/mp.db")
os.environ.setdefault("MP_SECRET_KEY", "audit-harness-only-secret-0123456789abcdef")
os.environ.setdefault("MP_SMS_PROVIDER", "dev")
sys.path.insert(0, BACKEND)


ROLES = ["member", "coach", "reception", "manager", "admin", "super_admin"]
# شماره‌های مصنوعی — همان الگوی seed پروژه (هیچ دادهٔ واقعی نیست)
ROLE_PHONES = {
    "member": "09120000001",       # از seed_live (نقش: admin) → در harness عضو می‌شود
    "coach": "09120000901",
    "reception": "09120000902",
    "manager": "09120000903",
    "admin": "09120000904",
    "super_admin": "09120000905",
    "member_pure": "09130000001",  # عضو ساده از seed_live (۲۵۰ عضو)
}


def _db() -> sqlite3.Connection:
    c = sqlite3.connect(DB, timeout=30)
    c.execute("PRAGMA busy_timeout=30000")
    return c


def ensure_role_users() -> dict[str, int]:
    """کاربر نقش‌دار مصنوعی بساز/به‌روز کن (بدون دست‌زدن به مخزن)."""
    c = _db()
    ids: dict[str, int] = {}
    for role, phone in ROLE_PHONES.items():
        row = c.execute("select id from users where phone=?", (phone,)).fetchone()
        if row is None:
            cur = c.execute(
                "insert into users (phone, full_name, role, is_active, created_at, updated_at) "
                "values (?, ?, ?, 1, datetime('now'), datetime('now'))",
                (phone, f"کاربر مصنوعی {role}", "member" if role == "member_pure" else role),
            )
            uid = cur.lastrowid
        else:
            uid = row[0]
            want = "member" if role == "member_pure" else role
            c.execute("update users set role=? where id=?", (want, uid))
        ids[role] = uid
    # grantهای مالی برای admin (مطابق KNOWN_PERMISSIONS)
    admin_id = ids["admin"]
    for perm in ("finance.read", "finance.write", "reports.confidential", "roles.manage", "flags.write"):
        ex = c.execute(
            "select 1 from admin_permissions where user_id=? and permission=? and revoked_at is null",
            (admin_id, perm),
        ).fetchone()
        if ex is None:
            c.execute(
                "insert into admin_permissions (user_id, permission, note, created_at) "
                "values (?, ?, 'harness', datetime('now'))",
                (admin_id, perm),
            )
    c.commit()
    c.close()
    return ids


def otp_login(client: httpx.Client, phone: str, max_wait: float = 150.0) -> dict[str, Any]:
    """ورود واقعی با OTP — با احترام به rate-limit خودِ اپ (۴۲۹ ⇒ صبر و تلاش دوباره).

    نکتهٔ ممیزی: چون `otp_rate_limit=10/minute` و `otp_burst_limit=3/second` است و
    کلیدِ سبد در development «IP همتا» است، هفت هویت پشت یک IP عملاً **یک سبد
    مشترک** دارند — همان سازوکاری که در production پشت پراکسی بدون
    `MP_TRUSTED_PROXIES` برای کل باشگاه رخ می‌دهد (یافتهٔ A3).
    """
    deadline = time.time() + max_wait
    attempt = 0
    while True:
        attempt += 1
        r = client.post("/api/v1/auth/otp/request", json={"phone": phone})
        if r.status_code == 429 and time.time() < deadline:
            time.sleep(15.0)
            continue
        r.raise_for_status()
        code = r.json().get("dev_code")
        assert code, f"dev_code missing for {phone}: {r.text[:200]}"
        v = client.post("/api/v1/auth/otp/verify", json={"phone": phone, "code": code})
        if v.status_code == 429 and time.time() < deadline:
            time.sleep(15.0)
            continue
        v.raise_for_status()
        return v.json()


def mint_token(user_id: int, role: str) -> str:
    """مسیر جایگزین: ساخت توکن با همان ماژول JWT خودِ پروژه (بدون OTP).

    `auth_version` از DB خوانده می‌شود، چون `app/deps.py:64-67` توکنِ بدون
    `ver` را تنها در صورتی می‌پذیرد که `user.auth_version == 0` باشد.
    """
    from app.security.jwt import create_access_token

    c = _db()
    row = c.execute("select auth_version from users where id=?", (user_id,)).fetchone()
    c.close()
    ver = int(row[0]) if row else 0
    return create_access_token(user_id, role, auth_version=ver)


class Principals:
    """توکن هر نقش + توکن نامعتبر + بدون توکن."""

    def __init__(self, base: str = BASE):
        self.base = base
        self.user_ids = ensure_role_users()
        self.tokens: dict[str, str] = {}
        self.raw: dict[str, dict] = {}
        with httpx.Client(base_url=base, timeout=60.0) as c:
            for role, phone in ROLE_PHONES.items():
                try:
                    data = otp_login(c, phone)
                    tok = data.get("access_token") or data.get("token")
                    assert tok, f"no access_token for {role}: {list(data)}"
                    self.raw[role] = {**data, "auth_path": "otp_live"}
                except Exception as exc:  # noqa: BLE001 — مسیر جایگزین
                    uid = self.user_ids[role]
                    real_role = "member" if role == "member_pure" else role
                    tok = mint_token(uid, real_role)
                    self.raw[role] = {"auth_path": "minted_fallback", "reason": str(exc)[:160]}
                self.tokens[role] = tok
                time.sleep(7.0)  # زیر سقف 10/minute بمان

    def headers(self, role: str | None) -> dict[str, str]:
        if role is None:
            return {}
        return {"Authorization": f"Bearer {self.tokens[role]}"}


def write_evidence(name: str, payload: Any) -> Path:
    p = EVIDENCE / name
    p.write_text(json.dumps(payload, ensure_ascii=False, indent=1, default=str), encoding="utf-8")
    return p


def load_routes() -> list[dict]:
    return json.loads(Path(f"{BACKEND}/api/routes.json").read_text(encoding="utf-8"))["operations"]


def load_openapi() -> dict:
    return json.loads((EVIDENCE / "openapi-live.json").read_text(encoding="utf-8"))


class Stats:
    def __init__(self) -> None:
        self.t0 = time.time()
        self.rows: list[dict] = []

    def add(self, **kw: Any) -> None:
        self.rows.append(kw)

    def dump(self, name: str) -> Path:
        summary = {
            "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "elapsed_s": round(time.time() - self.t0, 1),
            "records": len(self.rows),
            "rows": self.rows,
        }
        return write_evidence(name, summary)
