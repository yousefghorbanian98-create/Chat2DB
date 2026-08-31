#!/usr/bin/env python3
"""Finn-Loop v3 stage dispatcher — Cutting Edge.
Usage:
  python3 run_stage.py <stage-id>   # run one stage (gate enforced)
  python3 run_stage.py --report     # build docs/loop/report.md content to stdout
Reads the manifest at ce-app/ci/finn-loop.manifest.json (single source of truth).
Exit code 0 = stage complete (safe to commit the done marker), non-zero = failed.
"""
from __future__ import annotations
import json, subprocess, sys, datetime, pathlib

ROOT = pathlib.Path(__file__).resolve().parents[3]
MANIFEST = ROOT / "ce-app" / "ci" / "finn-loop.manifest.json"
STAGES_DIR = pathlib.Path(__file__).resolve().parent / "stages"

def load() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))

def run_stage(sid: str) -> int:
    m = load()
    stage = next((s for s in m["stages"] if s["id"] == sid), None)
    if stage is None:
        print(f"[v3] unknown stage {sid}", file=sys.stderr); return 2
    script = STAGES_DIR / f"{sid}.sh"
    if not script.exists():
        print(f"[v3] stage {sid} has no script at {script}", file=sys.stderr); return 2
    print(f"[v3] ▶ {sid}: {stage['title']}  (gate: {stage['gate']})")
    t0 = datetime.datetime.now()
    rc = subprocess.call(["bash", str(script)], cwd=str(ROOT))
    dt = (datetime.datetime.now() - t0).total_seconds()
    print(f"[v3] {'✅ PASS' if rc == 0 else '❌ FAIL'} {sid} in {dt:.1f}s")
    if rc == 0:
        stage["done"] = True
        MANIFEST.write_text(json.dumps(m, ensure_ascii=False, indent=2), encoding="utf-8")
    return rc

def report() -> int:
    m = load()
    done = [s for s in m["stages"] if s["done"]]
    pending = [s for s in m["stages"] if not s["done"]]
    now = datetime.datetime.utcnow().isoformat(timespec="seconds")
    lines = [f"# Finn-Loop v3 report — {now}", "",
             f"- done: **{len(done)}/{len(m['stages'])}**", f"- next: **{pending[0]['id']} — {pending[0]['title']}**" if pending else "- ALL DONE 🎉", "", "| id | stage | gate | status |", "|---|---|---|---|"]
    for s in m["stages"]:
        lines.append(f"| {s['id']} | {s['title']} | {s['gate']} | {'✅' if s['done'] else '⬜'} |")
    print("\n".join(lines)); return 0

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(2)
    sys.exit(report() if sys.argv[1] == "--report" else run_stage(sys.argv[1]))
