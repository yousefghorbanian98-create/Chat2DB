#!/usr/bin/env python3
"""باتری آزمون زندهٔ لایهٔ امنیتی/پولی/مالکیت روی اپِ در حال اجرا.

هر آزمون یک «فرضیهٔ مهندسی» دارد و نتیجهٔ **مشاهده‌شده** را با انتظار مقایسه
می‌کند؛ خروجی هم شاهد JSON است و هم یک جدول قضاوت (PASS/FAIL/NOTE).

  T1  سبد rate-limit: آیا همهٔ کلاینت‌ها پشت یک IP یک سبد مشترک دارند؟
  T2  X-Forwarded-For / X-Real-IP: با MP_TRUSTED_PROXIES="" باید نادیده گرفته شوند
  T3  حدس کد OTP: سقف تلاش و قفل شدن کد
  T4  پول بزرگ: 2^53−1، 2^53+1، منفی، اعشاری، رشته ⇒ چه چیزی برمی‌گردد؟
  T5  idempotency: تکرار کلید یکسان باید یک بار اثر کند
  T6  مالکیت: توکن عضو A روی دادهٔ عضو B
  T7  CORS: Origin مجاز/غیرمجاز در پیکربندی جاری
  T8  نشت اطلاعات در پاسخ خطا و در /metrics بدون احراز هویت
  T9  بازپخش (replay) کد OTP و توکن QR
  T10 هدرهای امنیتی روی پاسخ ۲۰۰ واقعی (نه ۴۰۵)

اجرا: /tmp/run/venv/bin/python audit/probe_live_security.py
"""
from __future__ import annotations

import json
import random
import sys
import time
from pathlib import Path

import httpx

sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness_common import BASE, Stats, write_evidence  # noqa: E402

random.seed(7)
VERDICTS: list[dict] = []


def verdict(tid: str, hypothesis: str, observed: str, status: str, fix: str = "") -> None:
    VERDICTS.append({"id": tid, "hypothesis": hypothesis, "observed": observed,
                     "status": status, "fix": fix})
    print(f"  [{status:<4}] {tid}: {observed[:150]}")


def phone() -> str:
    return f"0913{random.randint(10**6, 10**7 - 1)}"


def main() -> None:
    from harness_common import Principals

    stats = Stats()
    pr = Principals()
    H_super = pr.headers("super_admin")
    H_member = pr.headers("member_pure")
    c = httpx.Client(base_url=BASE, timeout=30.0)

    # ---------------- T1/T2: سبد rate-limit و هدرهای پراکسی ----------------
    print("\n== T1/T2: سبد rate-limit، X-Forwarded-For، X-Real-IP ==")
    # ورودهای Principals هم از همان سبد IP مصرف کرده‌اند ⇒ صبر تا پنجرهٔ تازه
    print("    (۶۵s صبر برای تازه‌شدن پنجرهٔ ۱۰/دقیقه)")
    time.sleep(65)
    results: dict[str, dict] = {}
    for label, extra_headers in (
        ("بدون هدر پراکسی", {}),
        ("با X-Forwarded-For تصادفی", {"X-Forwarded-For": None}),
        ("با X-Real-IP تصادفی", {"X-Real-IP": None}),
    ):
        ok = 0
        limited = 0
        first_429_at = None
        for i in range(14):
            h = dict(extra_headers)
            if h.get("X-Forwarded-For", "x") is None:
                h["X-Forwarded-For"] = f"203.0.113.{random.randint(1, 254)}"
            if h.get("X-Real-IP", "x") is None:
                h["X-Real-IP"] = f"198.51.100.{random.randint(1, 254)}"
            r = c.post("/api/v1/auth/otp/request", json={"phone": phone()}, headers=h)
            if r.status_code == 429:
                limited += 1
                if first_429_at is None:
                    first_429_at = i + 1
            else:
                ok += 1
            stats.add(pass_="ratelimit", label=label, i=i, status=r.status_code, headers=h)
        results[label] = {"accepted": ok, "limited": limited, "first_429_at": first_429_at}
        print(f"    {label}: accepted={ok} limited={limited} first_429_at={first_429_at}")
        time.sleep(63)   # همیشه یک پنجرهٔ کامل صبر کن تا برچسب بعدی آلوده نشود

    shared = results["بدون هدر پراکسی"]["limited"] > 0
    xff_changes = (results["با X-Forwarded-For تصادفی"]["accepted"]
                   != results["بدون هدر پراکسی"]["accepted"])
    verdict("T1", "هر IP یک سبد مستقل ۱۰/دقیقه دارد",
            f"{results['بدون هدر پراکسی']['accepted']} درخواست از ۱۴ پذیرفته شد، "
            f"نخستین ۴۲۹ در درخواست شمارهٔ {results['بدون هدر پراکسی']['first_429_at']}",
            "PASS" if shared else "NOTE")
    verdict("T2", "با MP_TRUSTED_PROXIES='' هدرهای پراکسی نادیده گرفته می‌شوند "
                  "(پس همهٔ کاربران پشت یک پراکسی **یک سبد مشترک** دارند)",
            f"X-Forwarded-For تصادفی نتیجه را {'عوض کرد' if xff_changes else 'عوض نکرد'} "
            f"⇒ accepted={results['با X-Forwarded-For تصادفی']['accepted']} "
            f"(در برابر {results['بدون هدر پراکسی']['accepted']} بدون هدر)",
            "FAIL" if not xff_changes else "PASS",
            "MP_TRUSTED_PROXIES را در production الزامی و اعتبارسنجی کن؛ در OPS-RUNBOOK "
            "مقدار واقعی پراکسی (Caddy) را مستند کن و آزمون بگذار که بدون آن ۴۲۹ نادرست ندهد.")

    # ---------------- T3: حدس کد OTP ----------------
    print("\n== T3: حدس کد OTP (brute force) ==")
    p = phone()
    r = c.post("/api/v1/auth/otp/request", json={"phone": p})
    real_code = r.json().get("dev_code") if r.status_code == 200 else None
    guesses = 0
    accepted_wrong = None
    if real_code:
        for i in range(12):
            wrong = f"{(int(real_code) + i + 1) % 1000000:06d}"
            if wrong == real_code:
                continue
            rr = c.post("/api/v1/auth/otp/verify", json={"phone": p, "code": wrong})
            guesses += 1
            stats.add(pass_="otp_bruteforce", i=i, status=rr.status_code, body=rr.text[:120])
            if rr.status_code == 200:
                accepted_wrong = wrong
                break
        verdict("T3", "کد اشتباه نباید هرگز پذیرفته شود و پس از سقف تلاش، کد باطل شود",
                f"{guesses} حدس اشتباه ⇒ هیچ‌کدام ۲۰۰ نشد" if not accepted_wrong
                else f"خطر: کد اشتباه {accepted_wrong} پذیرفته شد!",
                "FAIL" if accepted_wrong else "PASS")
        # آیا بعد از تلاش‌های ناموفق، کد واقعی هنوز کار می‌کند؟
        rv = c.post("/api/v1/auth/otp/verify", json={"phone": p, "code": real_code})
        verdict("T3b", "پس از N حدس ناموفق، کد واقعی باید قفل شده باشد (otp_max_attempts=5)",
                f"کد واقعی پس از {guesses} حدس ناموفق ⇒ HTTP {rv.status_code}",
                "PASS" if rv.status_code >= 400 else "FAIL",
                "اگر ۲۰۰ است: قفل حدس (attempt counter) روی کد اعمال نمی‌شود؛ "
                "شمارنده را در جدول otp_codes نگه دار و پس از ۵ تلاش کد را باطل کن.")

    # ---------------- T4: پول بزرگ ----------------
    print("\n== T4: مقادیر پولی بزرگ/مرزی ==")
    big = 2 ** 53
    cases = [
        ("2^53-1 (بیشترین عدد امن JSON)", big - 1),
        ("2^53", big),
        ("2^53+1 (ناامن)", big + 1),
        ("10^18", 10 ** 18),
        ("منفی", -5000),
        ("صفر", 0),
        ("اعشاری", 1500.75),
        ("رشته", "1500000"),
    ]
    money_rows = []
    for label, amount in cases:
        body = {"member_id": 1, "amount_rial": amount, "method": "cash",
                "description": f"T4 {label}", "idempotency_key": f"t4-{random.randint(10**9,10**12)}"}
        r = c.post("/api/v1/payments", json=body, headers=H_super)
        try:
            data = r.json()
        except Exception:  # noqa: BLE001
            data = {"raw": r.text[:150]}
        echoed = data.get("amount_rial") if isinstance(data, dict) else None
        money_rows.append({"label": label, "sent": amount, "status": r.status_code,
                           "echoed": echoed, "same": echoed == amount,
                           "body": json.dumps(data, ensure_ascii=False)[:220]})
        stats.add(pass_="money", **money_rows[-1])
        print(f"    {label:<34} sent={amount} → HTTP {r.status_code} echoed={echoed}")
    unsafe = [m for m in money_rows if m["sent"] in (big, big + 1, 10 ** 18) and m["status"] < 300]
    verdict("T4", "مقادیر بزرگ‌تر از 2^53−1 باید رد شوند (422) چون JSON/دارت/TS آن‌ها را دقیق نگه نمی‌دارند",
            f"{len(unsafe)} مورد ناامن با موفقیت پذیرفته شد: "
            f"{[m['label'] for m in unsafe]}" if unsafe else "همهٔ مقادیر ناامن رد شدند",
            "FAIL" if unsafe else "PASS",
            "سقف amount_rial را در schema با le=2**53-1 ببند و آزمون مرزی بگذار.")
    neg = [m for m in money_rows if m["label"] == "منفی" and m["status"] < 300]
    verdict("T4b", "مبلغ منفی/صفر باید رد شود",
            f"منفی ⇒ HTTP {[m['status'] for m in money_rows if m['label']=='منفی'][0]}, "
            f"صفر ⇒ HTTP {[m['status'] for m in money_rows if m['label']=='صفر'][0]}",
            "FAIL" if neg else "PASS")

    # ---------------- T5: idempotency ----------------
    print("\n== T5: idempotency ==")
    key = f"t5-{random.randint(10**9, 10**12)}"
    body = {"member_id": 1, "amount_rial": 120000, "method": "cash",
            "description": "T5", "idempotency_key": key}
    r1 = c.post("/api/v1/payments", json=body, headers=H_super)
    r2 = c.post("/api/v1/payments", json=body, headers=H_super)
    d1, d2 = r1.json(), r2.json()
    same = (d1.get("id") == d2.get("id"))
    stats.add(pass_="idempotency", first=r1.status_code, second=r2.status_code,
              id1=d1.get("id"), id2=d2.get("id"))
    verdict("T5", "دو درخواست با کلید idempotency یکسان باید یک رکورد بسازند",
            f"HTTP {r1.status_code}/{r2.status_code} با id={d1.get('id')} و id={d2.get('id')}"
            + (" ⇒ یکسان" if same else " ⇒ دو رکورد متفاوت ساخته شد"),
            "PASS" if same else "FAIL")

    # ---------------- T6: مالکیت ----------------
    print("\n== T6: مالکیت داده (عضو A روی دادهٔ عضو B) ==")
    others = [2, 3, 4, 5]
    own_rows = []
    for mid in others:
        for path in (f"/api/v1/members/{mid}",
                     f"/api/v1/assessments/member/{mid}",
                     f"/api/v1/nutrition/food-logs/member/{mid}/daily",
                     f"/api/v1/payments/wallet/member/{mid}"):
            r = c.get(path, headers=H_member)
            own_rows.append({"member_id": mid, "path": path, "status": r.status_code,
                             "body": r.text[:150]})
            stats.add(pass_="ownership", **own_rows[-1])
    leaked = [o for o in own_rows if o["status"] == 200]
    verdict("T6", "توکن یک عضو نباید دادهٔ عضو دیگر را بخواند (۴۰۳/۴۰۴ انتظار می‌رود)",
            f"{len(leaked)} پاسخ ۲۰۰ از {len(own_rows)} درخواست بین‌عضوی"
            + (f" ⇒ {[(o['path'], o['status']) for o in leaked][:4]}" if leaked else ""),
            "FAIL" if leaked else "PASS",
            "روی هر مسیر عضو‌محور `ensure_member_scope` بگذار و ماتریس "
            "permission×ownership را در تست بیاور.")

    # ---------------- T7: CORS ----------------
    print("\n== T7: CORS ==")
    cors_rows = []
    for origin in ("https://evil.example.com", "http://127.0.0.1:5173", "null"):
        r = c.options("/api/v1/members", headers={"Origin": origin,
                                                   "Access-Control-Request-Method": "GET"})
        cors_rows.append({"origin": origin, "status": r.status_code,
                          "allow_origin": r.headers.get("access-control-allow-origin"),
                          "allow_creds": r.headers.get("access-control-allow-credentials")})
        stats.add(pass_="cors", **cors_rows[-1])
    bad = [x for x in cors_rows if x["allow_origin"] not in (None, "")]
    verdict("T7", "Origin غیرمجاز نباید بازتاب داده شود (fail-closed)",
            json.dumps(cors_rows, ensure_ascii=False)[:220],
            "FAIL" if bad else "PASS")

    # ---------------- T8: نشت اطلاعات ----------------
    print("\n== T8: نشت اطلاعات ==")
    r = c.get("/api/v1/members/999999", headers=H_super)
    body = r.text
    leak_markers = [m for m in ("Traceback", "/tmp/run", "sqlalchemy", "sqlite", "File \"")
                    if m in body]
    verdict("T8", "پاسخ خطا نباید جزئیات فنی/مسیر فایل نشت دهد",
            f"HTTP {r.status_code} markers={leak_markers} body={body[:120]}",
            "FAIL" if leak_markers else "PASS")
    m = c.get("/api/v1/metrics")
    metric_lines = m.text.splitlines()
    verdict("T8b", "/api/v1/metrics باید پشت احراز هویت/شبکهٔ داخلی باشد",
            f"HTTP {m.status_code} بدون هیچ توکنی؛ {len(metric_lines)} خط، "
            f"{len(set(l.split('{')[0] for l in metric_lines if l.startswith('mp_')))} متریک "
            f"از جمله نام مسیرها و وضعیت outbox",
            "FAIL" if m.status_code == 200 else "PASS",
            "مسیر را با require_permission محافظت کن یا فقط روی پورت/اینترفیس داخلی ببند؛ "
            "در Caddy هم مسیر /metrics را از دسترس عمومی خارج کن.")

    # ---------------- T9: replay ----------------
    print("\n== T9: بازپخش ==")
    p2 = phone()
    r = c.post("/api/v1/auth/otp/request", json={"phone": p2})
    code = r.json().get("dev_code") if r.status_code == 200 else None
    if code:
        v1 = c.post("/api/v1/auth/otp/verify", json={"phone": p2, "code": code})
        v2 = c.post("/api/v1/auth/otp/verify", json={"phone": p2, "code": code})
        stats.add(pass_="replay", first=v1.status_code, second=v2.status_code)
        verdict("T9", "کد OTP باید یک‌بارمصرف باشد",
                f"بار اول HTTP {v1.status_code}، بار دوم HTTP {v2.status_code}",
                "FAIL" if v2.status_code == 200 else "PASS")
    q1 = c.get("/api/v1/face/qr-token", headers=H_member)
    if q1.status_code == 200:
        t = q1.json().get("token") or q1.json().get("qr_token")
        q2 = c.get("/api/v1/face/qr-token", headers=H_member)
        t2 = q2.json().get("token") or q2.json().get("qr_token")
        stats.add(pass_="replay_qr", same=(t == t2))
        verdict("T9b", "توکن QR باید هر بار یکتا باشد (jti مستقل برای replay gate)",
                f"دو فراخوانی ⇒ {'یکسان' if t == t2 else 'مختلف'}",
                "FAIL" if t == t2 else "PASS")

    # ---------------- T10: هدرهای امنیتی روی پاسخ ۲۰۰ ----------------
    print("\n== T10: هدرهای امنیتی روی پاسخ واقعی ==")
    r = c.get("/api/v1/members", headers=H_super)
    want = ["content-security-policy", "x-frame-options", "x-content-type-options",
            "referrer-policy", "permissions-policy", "cross-origin-opener-policy",
            "strict-transport-security"]
    have = {k.lower(): v for k, v in r.headers.items()}
    missing = [w for w in want if w not in have]
    stats.add(pass_="headers", status=r.status_code, missing=missing,
              csp=have.get("content-security-policy"))
    verdict("T10", "همهٔ هدرهای امنیتی روی پاسخ ۲۰۰ حاضر باشند",
            f"HTTP {r.status_code}; حاضر: {[w for w in want if w in have]}; غایب: {missing}",
            "PASS" if not missing else "NOTE",
            "در production باید HSTS هم باشد (فقط وقتی environment=production).")

    c.close()
    write_evidence("live-security-verdicts.json", VERDICTS)
    stats.dump("live-security-raw.json")
    print("\n=== خلاصه ===")
    for v in VERDICTS:
        print(f"  {v['id']:<5} {v['status']:<5} {v['hypothesis'][:70]}")
    print(f"\n→ evidence/live-security-verdicts.json")


if __name__ == "__main__":
    main()
