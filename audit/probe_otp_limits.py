#!/usr/bin/env python3
"""آزمون‌های دقیق OTP و دورزدن rate-limit — با پنجره‌های زمانی جدا.

چرا لازم شد؟ در باتری نخست، چند آزمون **نامعتبر** ماندند چون سبد ۱۰/دقیقهٔ
همان IP پیش‌تر مصرف شده بود و پاسخ‌ها ۴۲۹ شدند (نه نتیجهٔ منطق برنامه).
اینجا هر آزمون پنجرهٔ تازهٔ خودش را دارد:

  A  سقف حدس کد: ۴ حدس غلط ⇒ کد واقعی هنوز کار کند؛ بار دوم همان کد ⇒ باطل
  B  پس از ۶ حدس غلط ⇒ کد واقعی باید قفل شده باشد (otp_max_attempts=5)
  C  دورزدن سبد با X-Forwarded-For تصادفی (۳۰ درخواست پشت‌سرهم)
  D  همان آزمون C ولی با پراکسی‌هدرهای خاموش در سرور (کنترل)
  E  مصرف‌کنندهٔ واقعی کلید: چه چیزی در `request.client.host` می‌نشیند؟

اجرا: /tmp/run/venv/bin/python audit/probe_otp_limits.py [A|B|C|all]
"""
from __future__ import annotations

import json
import random
import sys
import time
from pathlib import Path

import httpx

sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness_common import BASE, write_evidence  # noqa: E402

random.seed(11)
OUT: list[dict] = []


def phone() -> str:
    return f"0913{random.randint(10**6, 10**7 - 1)}"


def record(**kw) -> None:
    OUT.append(kw)
    print("   ", json.dumps({k: v for k, v in kw.items() if k != "raw"}, ensure_ascii=False)[:230])


def wait_fresh_window(seconds: int = 65) -> None:
    print(f"    … {seconds}s صبر برای پنجرهٔ تازهٔ rate-limit")
    time.sleep(seconds)


def test_A(c: httpx.Client) -> None:
    print("\n== A) سقف حدس + یک‌بارمصرف بودن کد ==")
    wait_fresh_window()
    p = phone()
    r = c.post("/api/v1/auth/otp/request", json={"phone": p})
    assert r.status_code == 200, f"otp/request failed: {r.status_code} {r.text[:120]}"
    code = r.json()["dev_code"]
    wrong_statuses = []
    for i in range(4):
        w = f"{(int(code) + i + 1) % 1000000:06d}"
        if w == code:
            continue
        rr = c.post("/api/v1/auth/otp/verify", json={"phone": p, "code": w})
        wrong_statuses.append(rr.status_code)
    ok = c.post("/api/v1/auth/otp/verify", json={"phone": p, "code": code})
    again = c.post("/api/v1/auth/otp/verify", json={"phone": p, "code": code})
    record(test="A", phone=p, wrong_guesses=wrong_statuses,
           real_code_after_4_wrong=ok.status_code,
           real_code_replay=again.status_code,
           replay_body=again.text[:160],
           verdict_one_time=("PASS" if again.status_code >= 400 else "FAIL"),
           verdict_under_limit=("PASS" if ok.status_code == 200 else "NOTE"))


def test_B(c: httpx.Client) -> None:
    print("\n== B) قفل شدن کد پس از عبور از سقف تلاش ==")
    wait_fresh_window()
    p = phone()
    r = c.post("/api/v1/auth/otp/request", json={"phone": p})
    assert r.status_code == 200, f"otp/request failed: {r.status_code}"
    code = r.json()["dev_code"]
    wrong = []
    for i in range(8):
        w = f"{(int(code) + i + 1) % 1000000:06d}"
        if w == code:
            continue
        rr = c.post("/api/v1/auth/otp/verify", json={"phone": p, "code": w})
        wrong.append(rr.status_code)
        if rr.status_code == 429:
            break
    real = c.post("/api/v1/auth/otp/verify", json={"phone": p, "code": code})
    record(test="B", wrong_guess_statuses=wrong, real_code_after=real.status_code,
           real_body=real.text[:160],
           verdict=("PASS" if real.status_code >= 400 else "FAIL"),
           note="429 یعنی سبد rate-limit؛ 4xx دیگر یعنی قفلِ شمارندهٔ تلاش")


def test_C(c: httpx.Client, label: str, n: int = 30) -> None:
    print(f"\n== C) دورزدن سبد با X-Forwarded-For تصادفی ({label}) ==")
    wait_fresh_window()
    accepted = 0
    limited = 0
    statuses = []
    for i in range(n):
        h = {"X-Forwarded-For": f"203.0.113.{random.randint(1, 254)}"}
        r = c.post("/api/v1/auth/otp/request", json={"phone": phone()}, headers=h)
        statuses.append(r.status_code)
        if r.status_code == 429:
            limited += 1
        else:
            accepted += 1
    record(test="C", label=label, requests=n, accepted=accepted, limited=limited,
           statuses=statuses[:12],
           verdict=("FAIL" if accepted >= n * 0.9 else "PASS"),
           note="اگر تقریباً همه پذیرفته شوند ⇒ کلید سبد از هدرِ کنترل‌شدهٔ کلاینت می‌آید")


def test_D(c: httpx.Client) -> None:
    print("\n== D) baseline بدون هدر پراکسی (همان پنجرهٔ C ادامه ندارد) ==")
    wait_fresh_window()
    accepted = 0
    statuses = []
    for i in range(14):
        r = c.post("/api/v1/auth/otp/request", json={"phone": phone()})
        statuses.append(r.status_code)
        accepted += 1 if r.status_code != 429 else 0
    record(test="D", requests=14, accepted=accepted, statuses=statuses,
           note="سقف انتظار: ۱۰ در دقیقه (otp_rate_limit) + ۳ در ثانیه (burst)")


def test_E(c: httpx.Client) -> None:
    print("\n== E) چه IP‌ای در لاگ/متریک ثبت می‌شود؟ ==")
    h = {"X-Forwarded-For": "203.0.113.77"}
    r = c.get("/api/v1/metrics", headers=h)
    lines = [ln for ln in r.text.splitlines() if ln.startswith("mp_http_requests_total")]
    record(test="E", metrics_lines=len(lines), sample=lines[:3],
           note="متریک برچسب IP ندارد ⇒ نمی‌توان کلاینت متخلف را از متریک پیدا کرد")


def main() -> None:
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    c = httpx.Client(base_url=BASE, timeout=30.0)
    if which in ("all", "A"):
        test_A(c)
    if which in ("all", "B"):
        test_B(c)
    if which in ("all", "C"):
        test_C(c, "سرور جاری")
    if which in ("all", "D"):
        test_D(c)
    if which in ("all", "E"):
        test_E(c)
    c.close()
    p = write_evidence("otp-ratelimit-verdicts.json", OUT)
    print(f"\n→ {p}")


if __name__ == "__main__":
    main()
