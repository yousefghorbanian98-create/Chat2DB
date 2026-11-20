#!/usr/bin/env python3
"""آزمون همزمانی/اشباع pool — پیدا کردن ریشهٔ A1 با اندازه‌گیری، نه حدس.

چهار سناریو، هر کدام با نمونه‌برداری زنده از `/audit/pool` (شمارندهٔ checkout/
checkin خودِ SQLAlchemy) تا مشخص شود:
  س۱ «خواندن سنگین»   : ۲۰۰ کلاینت همزمان روی GETهای تحلیلی
  س۲ «نوشتن»           : ۲۰۰ کلاینت همزمان روی POST /expenses (نوشتن SQLite)
  س۳ «ترکیبی»          : خواندن + نوشتن + OTP (هر سه با هم)
  س۴ «بازیابی»         : پس از بار، آیا checkedout به صفر برمی‌گردد؟

معیارهای کلیدی:
  max_pool_checkedout (سقف واقعی = pool_size + max_overflow = ۶۰)
  leak_suspect = checkout − checkin (باید در پایان صفر باشد)
  شمار 5xx و متن خطا (به‌ویژه «database is locked» یا QueuePool timeout)
  p50/p95/p99 تأخیر
  پاسخ /health در حین بار (آیا سرور «قفل» می‌شود یا زنده می‌ماند)

اجرا: /tmp/run/venv/bin/python audit/probe_concurrency.py
"""
from __future__ import annotations

import json
import statistics
import sys
import threading
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from datetime import date
from pathlib import Path

import httpx

sys.path.insert(0, str(Path(__file__).resolve().parent))
from harness_common import BASE, Stats, write_evidence  # noqa: E402

TODAY = date(2026, 11, 20).isoformat()


def pool() -> dict:
    try:
        r = httpx.get(f"{BASE}/audit/pool", timeout=10)
        return r.json()
    except Exception as exc:  # noqa: BLE001
        return {"error": str(exc)}


class Sampler(threading.Thread):
    """نمونه‌برداری ۱۰۰ms از آمار pool در طول بار."""

    def __init__(self) -> None:
        super().__init__(daemon=True)
        self.samples: list[dict] = []
        self.stop_flag = False

    def run(self) -> None:
        while not self.stop_flag:
            snap = pool()
            if "error" not in snap:
                self.samples.append({
                    "t": round(time.time(), 3),
                    "checkedout": snap.get("pool_checkedout"),
                    "overflow": snap.get("pool_overflow"),
                    "checkout": snap.get("checkout"),
                    "checkin": snap.get("checkin"),
                    "connect": snap.get("connect"),
                    "close": snap.get("close"),
                    "leak_suspect": snap.get("leak_suspect"),
                    "max_held_ms": snap.get("max_held_ms"),
                })
            time.sleep(0.1)

    def summary(self) -> dict:
        if not self.samples:
            return {"samples": 0}
        co = [s["checkedout"] for s in self.samples if s["checkedout"] is not None]
        held = [s["max_held_ms"] for s in self.samples if s.get("max_held_ms") is not None]
        return {
            "samples": len(self.samples),
            "max_checkedout": max(co) if co else None,
            "mean_checkedout": round(statistics.mean(co), 2) if co else None,
            "max_overflow_seen": max(s["overflow"] for s in self.samples if s["overflow"] is not None),
            "max_held_ms": max(held) if held else None,
            "final_leak_suspect": self.samples[-1]["leak_suspect"],
            "total_checkout": self.samples[-1]["checkout"],
            "total_checkin": self.samples[-1]["checkin"],
        }


def pct(vals: list[float], p: float) -> float:
    if not vals:
        return 0.0
    s = sorted(vals)
    k = max(0, min(len(s) - 1, int(round(p / 100 * (len(s) - 1)))))
    return round(s[k], 1)


def run_scenario(name: str, tasks: list[tuple[str, str, dict | None, dict]],
                 workers: int, duration_s: float, stats: Stats) -> dict:
    """tasks: لیست (method, path, body, headers) که گردشی اجرا می‌شوند."""
    results: list[dict] = []
    lock = threading.Lock()
    health: list[tuple[float, int | None]] = []
    deadline = time.time() + duration_s
    counter = Counter()
    err_samples: list[str] = []
    sampler = Sampler()
    sampler.start()

    def one(idx: int) -> None:
        method, path, body, headers = tasks[idx % len(tasks)]
        lat: list[float] = []
        with httpx.Client(base_url=BASE, timeout=30.0) as c:
            while time.time() < deadline:
                t0 = time.perf_counter()
                try:
                    r = c.request(method, path, json=body, headers=headers)
                    status: int | None = r.status_code
                    text = r.text[:220]
                except Exception as exc:  # noqa: BLE001
                    status, text = None, f"{type(exc).__name__}: {exc}"[:220]
                ms = (time.perf_counter() - t0) * 1000
                lat.append(ms)
                with lock:
                    counter[status] += 1
                    if status is None or status >= 500:
                        if len(err_samples) < 25:
                            err_samples.append(f"{method} {path} → {status}: {text}")
                if len(lat) >= 40:
                    break

        with lock:
            results.append({"worker": idx, "requests": len(lat), "latencies_ms": lat})

    def health_probe() -> None:
        while time.time() < deadline:
            t0 = time.perf_counter()
            try:
                r = httpx.get(f"{BASE}/health", timeout=10)
                health.append((round((time.perf_counter() - t0) * 1000, 1), r.status_code))
            except Exception:  # noqa: BLE001
                health.append((round((time.perf_counter() - t0) * 1000, 1), None))
            time.sleep(0.5)

    hp = threading.Thread(target=health_probe, daemon=True)
    hp.start()
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=workers) as ex:
        list(ex.map(one, range(workers)))
    elapsed = time.time() - t0
    sampler.stop_flag = True
    time.sleep(0.4)

    all_lat = [x for r in results for x in r["latencies_ms"]]
    total = sum(r["requests"] for r in results)
    out = {
        "scenario": name,
        "workers": workers,
        "elapsed_s": round(elapsed, 1),
        "requests": total,
        "throughput_rps": round(total / elapsed, 1) if elapsed else 0,
        "status_counts": dict(counter),
        "p50_ms": pct(all_lat, 50), "p95_ms": pct(all_lat, 95),
        "p99_ms": pct(all_lat, 99), "max_ms": round(max(all_lat), 1) if all_lat else None,
        "pool": sampler.summary(),
        "health_during_load": {
            "probes": len(health),
            "failures": sum(1 for _, s in health if s != 200),
            "max_ms": max((h[0] for h in health), default=None),
        },
        "error_samples": err_samples[:10],
    }
    stats.add(pass_="concurrency", **{k: v for k, v in out.items() if k != "scenario"})
    print(json.dumps(out, ensure_ascii=False, indent=1)[:1400])
    return out


def main() -> None:
    from harness_common import Principals

    stats = Stats()
    print("== principals ==")
    pr = Principals()
    H_admin = pr.headers("admin")
    H_super = pr.headers("super_admin")
    H_member = pr.headers("member_pure")
    H_none: dict[str, str] = {}

    print("\n== pool پیش از بار ==")
    before = pool()
    print(" ", json.dumps({k: before.get(k) for k in
                          ("pool_size", "pool_checkedout", "pool_overflow", "checkout", "checkin", "leak_suspect")}))

    read_tasks = [
        ("GET", "/api/v1/admin/analytics/churn-risk", None, H_super),
        ("GET", "/api/v1/admin/analytics/leaderboards", None, H_super),
        ("GET", "/api/v1/members", None, H_admin),
        ("GET", "/api/v1/reports/financial/summary", None, H_super),
        ("GET", "/api/v1/payments", None, H_admin),
        ("GET", "/api/v1/shop/products", None, H_member),
    ]
    write_tasks = [
        ("POST", "/api/v1/expenses",
         {"amount_rial": 1000, "category": "rent", "spent_on": TODAY, "note": "بار harness"}, H_super),
    ]
    otp_tasks = [("POST", "/api/v1/auth/otp/request", {"phone": f"0913{5000000 + i}"}, H_none)
                 for i in range(20)]

    print("\n================ س۱: خواندن سنگین (۲۰۰ همزمان) ================")
    run_scenario("read_heavy_200", read_tasks, 200, 25.0, stats)

    print("\n================ س۲: نوشتن (۲۰۰ همزمان) ================")
    run_scenario("write_heavy_200", write_tasks, 200, 25.0, stats)

    print("\n================ س۳: ترکیبی خواندن+نوشتن+OTP (۲۰۰ همزمان) ================")
    run_scenario("mixed_200", read_tasks + write_tasks + otp_tasks, 200, 25.0, stats)

    print("\n================ س۴: بازیابی پس از بار ================")
    time.sleep(3)
    after = pool()
    print(" ", json.dumps({k: after.get(k) for k in
                          ("pool_checkedout", "pool_overflow", "checkout", "checkin", "leak_suspect",
                           "connect", "close", "max_held_ms", "uptime_s")}))
    r = httpx.get(f"{BASE}/health", timeout=10)
    print("  /health پس از بار →", r.status_code, r.text[:80])
    stats.add(pass_="concurrency", scenario="recovery", pool_after=after, health=r.status_code)

    write_evidence("concurrency-pool.json", {
        "pool_before": before, "pool_after": after,
        "rows": stats.rows,
        "verdict_leak": after.get("leak_suspect"),
    })
    p = stats.dump("concurrency-raw.json")
    print(f"\n→ {p}")


if __name__ == "__main__":
    main()
