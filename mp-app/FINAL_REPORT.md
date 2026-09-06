# Muscle Paradise — FINAL REPORT

**Date:** 2026-08-30 · **Branch:** `arena/01a04e9f-chat2db` · **Loop:** FINN-LOOP v3.0
**Source spec:** `docs/MuscleParadise/ENGINEERING_MAP_FULL_v1.md`

---

## 1. Verdict

**Every engineering-map item that can be built and verified in this sandbox is
built and verified.** Five deliverables are **not** complete; they are blocked by
missing tooling in the environment, listed with evidence in §6. This report does
not count them as done.

Everything claimed below was re-measured in the final pass, after the toolchain
was rebuilt from scratch (§7). No number here is carried over from an earlier
run.

---

## 2. Measured results (final pass)

### Backend — local-first core

| Gate | Result |
|---|---|
| `pytest` (project `pytest.ini`, `--cov-fail-under=80`) | **exit 0** |
| Tests | **234 passed**, 0 failed, 0 skipped |
| Statement coverage | **90.39%** (gate 80%) |
| `-m golden` (known-answer math) | **32 passed** |
| `-m schema` (migrations/schema) | **33 passed** |
| `-m api` (HTTP surface) | **8 passed** |

> The count is read with `--override-ini="addopts="`, because `pytest.ini` puts
> `-q` in `addopts`, which suppresses the summary line. Counting progress dots
> instead is unreliable and produced a wrong figure (233) mid-project; the
> correct baseline was 231, now 234.

### Studio — coach shell + athlete shell

| Gate | Result |
|---|---|
| `npm run gate` (lint + format:check + typecheck + coverage + build) | **exit 0** |
| `eslint . --max-warnings=0` | **0 problems** |
| `prettier --check` | **0 files flagged** |
| `tsc --noEmit` | **exit 0** |
| Vitest | **110 passed** (13 files) |
| Statement coverage | **84.68%** (branch 80.32%, functions 84.72%; gate 80%) |
| Initial bundle | **97.79 kB gzip** JS + 1.39 kB CSS (target < 250 kB) |
| Lazy route chunks | Coach 2.57 kB, Programs 3.44 kB, Operations 4.01 kB, AssessmentJp7 111.10 kB, Sync 2.17 kB (gzip) |

### Codebase

29 commits on the branch · 139 source files · 15,034 lines (`.py`/`.ts`/`.tsx`,
excluding `node_modules`).

---

## 3. Golden fixtures — "every release moves a measured number" (C12)

The JP7 body-composition math is pinned to known-answer fixtures in
`tests/test_jp7.py`, not to vibes:

| sex | age | Σ7 (mm) | body density | %BF (Siri) |
|---|---|---|---|---|
| male | 25 | 60 | 1.080674 | 8.0474 |
| male | 35 | 80 | 1.070632 | 12.3439 |
| female | 25 | 60 | 1.067626 | 13.6453 |
| female | 45 | 120 | 1.042926 | 24.6261 |

**External anchor:** the published fitties.com worked example (male, 35,
Σskin­folds = 107 mm) states body density **1.06166**; the suite asserts
`body_density(...) == approx(1.06166, abs=1e-5)`.

*Recorded discrepancy:* that source's next step is arithmetically wrong —
`495/1.06166 = 466.2492`, i.e. **16.2492 %BF**, not the 466.34 / "16.3" it
prints. The anchor is therefore taken on **body density**, which is the step our
independent Decimal math reproduces exactly.

Nutrition is deterministic too: `BMR = 370 + 21.6·LBM`, activity ×1.2–1.9, goal
×0.85/1.0/1.1, protein 1.8 g/kg LBM. Verified by hand against a live plan:
LBM 50.0857 → BMR **1451.85** (API 1451.9), TDEE ×1.55 = **2250.4**, protein
1.8 × 50.0857 = **90.15** (API 90.2).

Jalali conversion is pinned to nine anchors cross-checked against an independent
implementation (Python `jdatetime`), including Nowruz 1405 = 2026-03-21 and the
leap Esfand 2025-03-20 → 1403-12-30.

---

## 4. Live end-to-end transcript (real HTTP, not TestClient)

Run against a fresh DB with `python -m app.bootstrap` + `python -m app.seed_demo`,
served by uvicorn on :8751:

```
POST /api/v1/nutrition/members/1/plan      (coach token)   -> 201
GET  /api/v1/client/me                     (MP-DEMO-1/1234)-> "نسیم رحیمی", note present? False
GET  /api/v1/client/me/nutrition           (member token)  -> tdee 2250.4, protein 90.2, payload stripped? True
GET  /api/v1/client/me                     (coach token)   -> 403
POST /api/v1/auth/member-pin               (wrong PIN)     -> 401
```

The Studio dev server proxies `/api` to the core; `POST /api/v1/auth/member-pin`
through the Vite proxy on :5173 returns **200**, so the browser path is exercised
end to end, not just the API.

---

## 5. What was built

- **Local-first core (FastAPI + SQLite, WAL):** migrations `0001_core` +
  `0002_member_pin`, gyms/staff/members/assessments/programs/nutrition/
  payments/visits/backups/sync.
- **Deterministic engines:** JP7 + Siri, TDEE/macros, rule-based program planner
  that always competes with the AI path; dry-run before apply; archive with 409
  on re-apply.
- **Auth & isolation:** role tokens (OWNER/TRAINER/RECEPTION/KIOSK/MEMBER),
  PBKDF2 PIN hashing, TRAINER member scoping with 404-on-unassigned, and a
  client surface that is force-scoped to the token's own `member_id`.
- **Field masking (C9/C11):** `mask_member_row`, `mask_assessment_row`,
  `mask_nutrition_row` strip clinician notes and the internal `payload` envelope
  from every member-facing row; `pin_hash` is excluded from all read columns.
- **Persian-first surfaces:** Jalali dates, Persian assessment PDF and cash/card
  receipt (in-house MIT RTL reorderer + arabic-reshaper — `python-bidi` was
  rejected as LGPL-3.0, see `NOTICES.md`), idempotent Persian demo seed
  (`MP-DEMO-1` / PIN 1234).
- **Dual shells:** Studio (coach) and `ClientShell` (athlete) with server-side
  isolation proven by the 403 above; dual-mode login (staff PIN / membership
  code + PIN).
- **Docs kept honest:** `LOOP_STATE.md`, `ERRORS.log` (58 lines),
  `DESIGN_SYSTEM.md`, `NOTICES.md`, `CHANGELOG.md` (0.14.0 → 0.19.0, each entry
  carrying a measured delta).

**Design conflict, resolved and documented** (`DESIGN_SYSTEM.md`): FINN-LOOP asks
for cinematic motion; the product spec `MASTER.md` sets the motion dial to
**4/10** for dense dashboards. MASTER.md governs data-dense Studio/Client
surfaces (200 ms fades, no `back.out` on tables, never scale rows); the loop's
springs apply to launcher entrance, modals, toasts and celebrations.
`prefers-reduced-motion` is honoured throughout.

---

## 6. NOT complete — blocked by the environment

Re-verified in the final pass with `command -v`; all ten absent:
`flutter`, `dart`, `electron`, `ollama`, `lighthouse`, `chromium`,
`chromium-browser`, `google-chrome`, `firefox`, `puppeteer`. No
`node_modules/electron/dist` exists either.

| Item | Why blocked | What was done instead |
|---|---|---|
| Core Web Vitals (FCP/LCP/CLS/FID) | no browser, no lighthouse | route code-splitting + 97.79 kB gzip initial bundle, measured from `vite build` |
| Electron desktop binary | `ELECTRON_SKIP_BINARY_DOWNLOAD=1`, no dist | web shells only |
| Native Flutter athlete client | no `flutter`/`dart` SDK | the athlete contract it would consume (`/api/v1/client/*`) is built and tested |
| Ollama live inference | no `ollama` binary | AI brain degrades to the deterministic rule engine and reports its state honestly via `/ai/runtime` |
| Runnable Kiosk | needs a browser target | signed-QR check-in path is unit-tested; no runnable kiosk |

These are recorded in `LOOP_STATE.md` as BLOCKED with reasons, not hidden.

---

## 7. Two environment resets, and a real bug they exposed

The sandbox was reset to the base commit `763a0de` twice mid-project. Each time
the working tree survived but the git HEAD, the Python venv and `node_modules`
were gone, while `origin/arena/01a04e9f-chat2db` still held the pushed work.
Recovery each time: `git fetch` + `git reset --hard FETCH_HEAD`, then
`diff -rq` against a pre-reset backup — **empty**, i.e. nothing was lost.

The rebuild exposed a genuine defect: `requirements.txt` was missing
`cryptography` (a fresh install could not even import the app, because
`app/core/backup.py` needs Fernet) and `PyMuPDF` (whose absence made a PDF
text-extraction test **skip silently**). Both are now pinned, and the final pass
installed cleanly from `requirements.txt` alone — which is the proof the fix
holds.

The project gate also caught that five files added in 0.18/0.19 had never been
through Prettier (`npm run gate` exited 1 on formatting alone). Fixed in
`a4b83f4`; the gate now exits 0 including the production build.

---

## 8. How to run

```bash
# core
python3 -m venv .venv-mp && .venv-mp/bin/pip install -r mp-app/backend/requirements.txt
cd mp-app/backend
MP_OWNER_PIN=<pin> MP_DB_PATH=/tmp/mp.db ../../.venv-mp/bin/python -m app.bootstrap
MP_DB_PATH=/tmp/mp.db ../../.venv-mp/bin/python -m app.seed_demo      # demo athlete
MP_DB_PATH=/tmp/mp.db ./run.sh                                        # uvicorn :8751
# run.sh lives in mp-app/backend/, defaults to 127.0.0.1 and MP_VENV=../../.venv-mp.
# For the sandbox preview pass MP_HOST=0.0.0.0. It execs:
#   uvicorn app.main:create_app_from_env --factory --port 8751

# studio
cd mp-app/studio && npm install && npm run dev                        # :5173
```

Sign in as staff (`owner` / your PIN) or switch to **ورزشکار** and use
`MP-DEMO-1` / `1234`.

```bash
.venv-mp/bin/python -m pytest                      # 234 passed, gate exit 0
cd mp-app/studio && npm run gate                   # exit 0
```

---

## 9. Honest remaining gaps (not blocked, just not done)

- No page render tests for **Operations** or **OpsKpis**. Login *is* covered
  (3 tests, added with the dual-mode sign-in), as are Coach, Programs, Sync,
  AssessmentJp7, ClientShell, the ops panels and the motion presets.
- The RAG/FA food database is not populated; nutrition computes from LBM only.
- `NOTICES.md` is still a seed list and must grow with every new dependency.
- Visual/animation quality gates were scored by checklist against MASTER.md, not
  by a browser-based measurement — see §6.
