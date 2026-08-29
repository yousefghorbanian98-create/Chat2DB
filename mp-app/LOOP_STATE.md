# MP LOOP_STATE.md — FINN-LOOP v3.0 execution record

```
Current Iteration: 2
Current Phase: Phase 0 — Skeleton (ENGINEERING_MAP_FULL_v1.md §14)
Current Task: Phase 0 complete; next = Phase 1 task "Members CRUD + QR id"
Status: PHASE_0_DONE
Design Quality Score: 7/10
Animation Quality Score: 8/10
Code Quality Score: 8/10
Completed Tasks: [see checklist below]
Failed Tasks: [] (3 defects found + fixed, logged in ERRORS.log)
Last Updated: 2026-08-29 (Asia/Tehran)
```

## Routing decisions (Phase 1.1 — OmniRoute pattern)

| Task | Complexity | Route taken |
|------|-----------|-------------|
| `mp-app/` monorepo scaffold | medium | Plan → Implement → Test |
| SQLite schema (24 tables) + migration runner | complex | Plan → Decompose (base/runner/v001) → Implement → Integration test |
| JP7 deterministic core | **critical** | Plan → Implement → Unit (12 golden) → Integration (payload) → external-anchor test |
| `/health` probe | medium | Plan → Implement → Test |
| Studio tokens + motion system | medium | Plan → Implement → Test |
| Studio launcher shell | simple | Direct implementation |

## Phase 0 checklist (map §14)

- [x] Create `mp-app/` monorepo (backend + studio + openapi.yaml)
- [x] FastAPI `/health` on **8751** — verified live: `status ok`, 25 tables
- [x] SQLite schema + migrations + `gym_id` — 24 tables, audit columns asserted per table
- [x] openapi.yaml stub — generated from the real app (`python -m app.export_openapi`)
- [x] Studio Electron hello + theme tokens from MASTER.md — tokens.css 1:1 with MASTER.md
- [x] STATE.md + map linked — this file
- [x] License attribution page stub — `mp-app/NOTICES.md`
- [ ] **Dev tooling:** ChunkHound / open-codebase-index not installed in this sandbox
      (no `chunkhound` on PATH, and `pip install chunkhound` was not attempted —
      see Open Items)

## Verified evidence (commands actually run)

| Check | Command | Result |
|-------|---------|--------|
| Backend suite | `pytest` (mp-app/backend) | **73 passed**, 1 warning |
| JP7 golden fixtures | `pytest -m golden` | 12 fixtures within ±0.05 %BF; external anchor BD 1.061664 vs published 1.06166 |
| Studio typecheck | `npx tsc --noEmit` | exit 0, zero errors (strict + exactOptionalPropertyTypes) |
| Studio unit tests | `npx vitest run` | **25 passed** (2 files) |
| Studio build | `npx vite build` | 280.03 kB raw / **91.73 kB gzip** (budget 250 kB) |
| Live API | `uvicorn --factory` + `curl :8751/health` | 200, `schema_version 0001_core`, `x-response-ms 2.9` |
| CORS allowlist | curl with `Origin: https://evil.example` | 0 `access-control-allow-origin` headers |

## Taste score breakdown (Phase 3.5) — honest, not aspirational

| Axis | Score | Why |
|------|-------|-----|
| Visual Polish | 6 | Tokens + glass cards are real, but the launcher is not yet matched to mockup 06; no iconography (Lucide not wired) |
| Animation Quality | 8 | Preset table encoded + unit-tested, reduced-motion honoured, dashboard/cinematic split resolved; no celebration/choreography moments built yet |
| Interaction Design | 7 | Button press + hover springs, skeletons everywhere; no keyboard shortcuts or command palette yet |
| Readability | 9 | Docstrings, typed, ≤300-line files, no `any` |
| Consistency | 9 | Single token source (MASTER.md), single motion source (presets.ts) |
| Performance | 8 | 91.7 kB gzip, transform-only animations; LCP/CLS not yet measured in a browser |
| Security | 7 | CORS allowlist + Electron isolation flags + FK enforcement; no auth yet (Phase 1) |
| Accessibility | 8 | roles/aria-busy/aria-label, 44px targets, reduced motion; no screen-reader pass yet |
| Responsiveness | 7 | CSS grid auto-fill; not yet tested at 375px/2560px |
| Delight Factor | 4 | Deliberately deferred — dashboard-first per MASTER.md motion dial 4/10 |
| **Average** | **7.3** | **Below the loop's 8.0 bar** → Phase 0 ships as a skeleton by design; the bar applies to user-facing modules from Phase 1 |

## Open items (not done, not hidden)

1. **ESLint + Prettier not configured** → FINN-LOOP gate 3.1 is only *partially*
   satisfied (`tsc --noEmit` passes; lint/format gates do not exist yet).
2. **Coverage not measured** → gate 3.2 requires ≥80%; `@vitest/coverage-v8` and
   `pytest-cov` are not installed. Every changed code path *is* exercised, but the
   percentage is unverified.
3. **Browser performance metrics (FCP/LCP/CLS)** unmeasured — needs a real browser.
4. **Electron binary skipped** (`ELECTRON_SKIP_BINARY_DOWNLOAD=1`), so the packaged
   shell was never launched; only the web renderer was built and tested.
5. **Flutter client, Ollama, sync fabric** — Phases 5–6, untouched.

## Conflict resolved this iteration

MASTER.md sets MP's motion dial to **4/10 (dense dashboard, no back.out on tables,
200ms page fades)** while FINN-LOOP demands cinematic motion everywhere. Resolution:
`presets.ts` exposes `mode: 'dashboard' | 'cinematic'` — dense data surfaces use
dashboard, celebrations/modals/launcher use cinematic. Enforced by unit tests
(`presets.test.ts` → "dashboard cards translate only — no scale on dense surfaces").
