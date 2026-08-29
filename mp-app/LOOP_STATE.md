# MP LOOP_STATE.md — FINN-LOOP v3.0 execution record

```
Current Iteration: 16
Current Phase: Phase 3 — Quality gates (FINN-LOOP §3: ESLint 0 / Prettier / tsc / coverage >=80%)
Current Task: Studio quality gate CLOSED — ESLint 0 warnings, Prettier clean, 90 tests, 82.24% statements, `npm run gate` exit 0. Next = Core Web Vitals in a real browser, Vazirmatn TTF for Persian PDF, then client-side deliverables (Flutter, Kiosk flavour, Electron, Persian demo seed)
Status: STUDIO_QUALITY_GATE_GREEN
Design Quality Score: 7/10
Animation Quality Score: 8/10
Code Quality Score: 10/10
Completed Tasks: [see checklist below]
Failed Tasks: [] (13 defects found + fixed, all logged in ERRORS.log)
Last Updated: 2026-08-30 (Asia/Tehran)
```

## Routing decisions (Phase 1.1 — OmniRoute pattern)

| Task | Complexity | Route taken |
|------|-----------|-------------|
| `mp-app/` monorepo scaffold | medium | Plan → Implement → Test |
| SQLite schema (24 tables) + migration runner | complex | Plan → Decompose (base/runner/v001) → Implement → Integration test |
| JP7 deterministic core | **critical** | Plan → Implement → Unit (12 golden) → Integration → external-anchor test |
| `/health` probe | medium | Plan → Implement → Test |
| Studio tokens + motion system | medium | Plan → Implement → Test |
| Studio launcher shell | simple | Direct implementation |
| PIN hashing / tokens / signed QR | **critical** | Plan → Implement → Unit (24) → tamper + replay + expiry tests |
| RBAC dependencies | **critical** | Plan → Implement → per-role matrix tests |
| Members CRUD + QR | complex | Plan → Implement → Unit + integration + tombstone test |
| Assessments API (compute + history) | **critical** | Plan → Implement → Unit → golden-math assertion on the stored row |
| Injuries + field masking | complex | Plan → Implement → masking + filter tests |

## Phase 0 checklist (map §14) — DONE

- [x] Create `mp-app/` monorepo (backend + studio + openapi.yaml)
- [x] FastAPI `/health` on **8751** — verified live
- [x] SQLite schema + migrations + `gym_id` — 24 tables, checksum drift detection
- [x] openapi.yaml — regenerated from the real app: **13 paths / 13 schemas**
- [x] Studio Electron hello + theme tokens from MASTER.md
- [x] STATE.md + map linked — this file
- [x] License attribution stub — `mp-app/NOTICES.md`
- [ ] **Dev tooling:** ChunkHound / open-codebase-index not installed in this sandbox

## Phase 1 checklist (map §14)

- [x] Staff auth PIN — PBKDF2-HMAC-SHA256 200k iters, constant-time compare,
      no user enumeration; machine-local HMAC session tokens (8h TTL)
- [x] Members CRUD + QR id — create/read/patch/tombstone, signed 60s QR
      (`{v,typ,gym,mid,exp,sig}`), `bootstrap.py` seeds gym + OWNER
- [x] `jp7.py` + 10 golden tests — **12 fixtures**, external anchor included
- [x] Assessment UI (mockup 07) + history chart  ✅ RTL, 3-col, silhouette markers, live preview (client jp7 mirror, unit-tested), injury banner, BF% trend (Recharts), lazy-split
- [ ] PDF assessment report — needs `reportlab`, not installed yet
- [x] Injury/limitation CRUD + safety card data — dossier, contraindication
      patterns, `GET /members/{id}/filters`, and the Studio-vs-member field mask

## Phase 2 checklist (map §14)

- [x] Attendance QR signed check-in — 60s HMAC QR verify; expired membership 402; double check-in 409; check-out; today count
- [x] Packages + payments + receipt PDF — integer rials; RECEPTION cash entry; finance-only void (tombstoned)
- [x] Dashboard KPIs — finance-gated
- [x] Equipment inventory — OWNER/ADMIN manage
- [x] Seed exercises + 30 FA — idempotent loader (30 then 0)

## Phase 3 checklist (map §14)

- [x] Rule templates PPL/UL/FB/corrective — pure builder, unit-tested
- [x] Contraindication graph filter — hard_block DROP → SWAP → equipment DROP → corrective
- [x] Program JSON v1 + apply/archive — whitelist ops; lifecycle state machine; C8 re-check

## Phase 4 checklist (map §14)

- [x] Ollama detect + AiRuntime — GET /ai/runtime, injectable probe, never required
- [ ] RAG over KB pack — deferred (needs vector store + embeddings; no Ollama here)
- [x] Race rule vs Ollama + judge — rules win ties/absent/unsafe (C7)
- [ ] Dry-run UI (mockup 08) — backend dry-run exists (Phase 3); AI UI deferred
- [x] Nutrition Katch-McArdle from LBM — golden-tested; FA foods subset deferred

## Verified evidence (commands actually run)

| Check | Command | Result |
|-------|---------|--------|
| Backend suite | `pytest` (mp-app/backend) | **219 passed**, 2 warnings |
| JP7 golden | `pytest -m golden` | 32 tests; 12 fixtures within ±0.05 %BF |
| Schema | `pytest -m schema` | 33 tests; audit columns on all 24 tables |
| Security | `pytest tests/test_security.py` | 24 tests (tamper/replay/expiry/algo) |
| Phase 1 API | `pytest tests/test_phase1_api.py` | 40 tests incl. full RBAC matrix |
| Live E2E | `uvicorn :8752` + curl chain | login → member → JP7 (BD 1.050006 / BF 21.4259) → injury → filters → masked view → signed QR → injury badge = 1 |
| OpenAPI | `python -m app.export_openapi` | 13 paths, 13 schemas, 1179-line YAML |
| Studio gate | `npm run gate` | tsc clean, **45 tests**, initial **93.97 kB gzip** (recharts lazy-split: +111 kB on assessment route) |

### Live E2E transcript (real HTTP, not TestClient)

```
POST /api/v1/auth/pin                    -> token (role OWNER, 8h)
POST /api/v1/members                     -> member id 1 (Sara Azad, female)
POST /api/v1/members/1/assessments       -> body_density 1.050006, body_fat_pct
                                            21.4259, FM 13.3912, LBM 49.1088,
                                            classification "fit"
POST /api/v1/members/1/injuries          -> injury 1, patterns ['spinal_flexion']
GET  /api/v1/members/1/filters           -> blocked ['spinal_flexion'],
                                            allowed ['trap_bar_deadlift']
GET  /api/v1/client/members/1/injuries   -> keys [body_region,id,label,
                                            member_visible_note,status]
                                            clinician_note leaked? False
GET  /api/v1/members/1/qr                -> {v:1,typ:member,gym:1,mid:1,exp,sig}
GET  /api/v1/members                     -> Sara Azad | active_injuries: 1
```

## RBAC matrix (locked by tests)

| Endpoint group | OWNER | ADMIN | TRAINER | RECEPTION | KIOSK | MEMBER |
|----------------|-------|-------|---------|-----------|-------|--------|
| read members | ✅ all | ✅ all | ⚠️ assigned only | ✅ all | ❌ 403 | ❌ 403 |
| write members | ✅ | ✅ | ❌ 403 | ✅ | ❌ 403 | ❌ 403 |
| JP7 assessments | ✅ | ✅ | ⚠️ assigned only | ❌ 403 | ❌ 403 | ❌ 403 |
| injuries / filters | ✅ | ✅ | ✅ | ❌ 403 | ❌ 403 | ❌ 403 |
| `/auth/me` | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `POST /assessments/calculate` (pure math) | open — no PII, no persistence |

## Taste score breakdown (Phase 3.5)

| Axis | Score | Why |
|------|-------|-----|
| Visual Polish | 7 | Assessment page now matches mockup 07 layout; Lucide still not wired; no PDF yet |
| Animation Quality | 8 | Presets unit-tested, reduced-motion honoured, dashboard/cinematic split enforced |
| Interaction Design | 7 | Spring press/hover, labelled skeletons; no command palette yet |
| Readability | 9 | Docstrings, typed, ≤300-line files, no `any` |
| Consistency | 9 | One token source, one motion source, one error envelope |
| Performance | 8 | 91.73 kB gzip; `x-response-ms` 2.9 on /health; browser metrics unmeasured |
| Security | 9 | PBKDF2 200k, constant-time compare, HMAC tokens + QR, RBAC matrix, CORS allowlist, Electron isolation, FK enforcement |
| Accessibility | 8 | roles/aria-busy/44px targets/reduced motion; no screen-reader pass |
| Responsiveness | 7 | CSS grid auto-fill; untested at 375px/2560px |
| Delight Factor | 4 | Deferred by design (MASTER.md motion dial 4/10) |
| **Average** | **7.9** | Backend is at bar; the average is held down by UI axes that Phase 1's remaining frontend tasks will move |

## Open items (not done, not hidden)

1. ~~**ESLint + Prettier not configured**~~ — **CLOSED 2026-08-30**: flat config +
   Prettier config, both in `npm run gate`. ESLint **21 → 0 problems** at
   `--max-warnings=0`; Prettier **29 → 0 files**.
2. ~~**Coverage not measured**~~ — **CLOSED 2026-08-30** on both sides:
   - Studio: `@vitest/coverage-v8`; statements **63.92% → 82.24%** (branch 79.92%,
     functions 85.46%).
   - Backend: `pytest-cov` pinned; **90.54%** over 1967 statements, 219 tests.
     Wired as a hard gate in `pytest.ini` (`--cov-fail-under=80`), verified to
     fail with exit 1 when the threshold is raised to 95%.
3. **Browser Core Web Vitals (FCP/LCP/CLS)** unmeasured — needs a real browser.
4. **Electron binary skipped** (`ELECTRON_SKIP_BINARY_DOWNLOAD=1`); the packaged
   shell was never launched.
5. ~~`reportlab` not installed~~ — **CLOSED**: installed 5.0.1, PDF endpoint live (2.7 KB, valid %PDF). Persian PDF needs a Vazirmatn TTF embed — deferred.
6. ~~Assessment UI + history chart~~ — **CLOSED**: `pages/AssessmentJp7.tsx` with live preview, validation, history chart.
7. ~~TRAINER member scoping~~ — **CLOSED this iteration**: `app/auth/scope.py`
   now filters member lists and 404s unassigned access across members,
   assessments and injuries routers.
8. **Flutter client, Ollama, sync fabric** — Phases 5–6, untouched.

## Quality gate — iteration 16 (2026-08-30), all numbers measured

`npm run gate` = `lint && format:check && typecheck && coverage && build` → **exit 0**.

| Gate | Target | Before | After |
|------|--------|--------|-------|
| ESLint (`--max-warnings=0`) | 0 problems | 21 | **0** |
| Prettier `--check` | 0 files | 29 flagged | **0** |
| `tsc --noEmit` | exit 0 | exit 0 | **exit 0** |
| Unit tests | pass | 83 | **90 passed (10 files)** |
| Studio statement coverage | ≥ 80% | 63.92% | **82.24%** (branch 79.92%, funcs 85.46%) |
| Backend statement coverage | ≥ 80% | unmeasured | **90.54%** (219 tests, gated in `pytest.ini`) |
| Initial bundle | < 250 kB gzip | 94.81 kB | **95.33 kB** |

`max-lines-per-function` ≤ 50 was the last rule standing. Sub-component extraction
alone did **not** clear it (two extractions still landed at 60–66 lines); the volume
driver was inline `style={{…}}` literals. The order that worked: hoist styles to
module constants → extract JSX clusters → move fetching into `src/hooks/*`.

Two real defects surfaced during the pass and were fixed, not papered over:
- `ResultPanel`'s saved-confirmation lived in an unreachable `else` branch
  (found by the new page test).
- Moving Coach state into a hook dropped the stale-plan clear on athlete change
  (found by diffing old handler bodies; no test covered it).

Still open: backend `pytest-cov` (219 tests, no coverage number), browser Core Web
Vitals, Vazirmatn TTF for Persian PDF.

## Conflicts resolved

MASTER.md motion dial 4/10 vs FINN-LOOP cinematic → `presets.ts` exposes
`mode: 'dashboard' | 'cinematic'`; dense surfaces use dashboard, celebrations and
modals use cinematic. Asserted in `presets.test.ts`.

## Rule added to ERRORS.log after a self-inflicted defect

> Never paste an expected numeric literal you did not compute. Derive it with an
> independent calculation (python decimal) and cite the derivation in the test.
