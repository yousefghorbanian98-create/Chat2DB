# MP Changelog

Format: Keep a Changelog. Versioning: every release must move a measured number
(map rule C12).

## [0.1.0] — 2026-08-29 — Phase 0 skeleton

### Added
- `mp-app/` monorepo: `backend/` (FastAPI + SQLite), `studio/` (Electron + React),
  `openapi.yaml`.
- Local core on port **8751**: `GET /health` and `GET /api/v1/health` reporting
  service, version, SQLite version, table count and schema version.
- Versioned migration runner with SHA-256 checksums and drift detection
  (`MigrationDriftError`) — two gyms can never silently diverge.
- Core schema `0001_core`: **24 tables** from map §8, every one carrying
  `id, gym_id, created_at, updated_at, deleted_at, rev`; FKs enforced;
  `trg_gyms_self_tenant` makes a gym row its own tenant.
- `app/core/jp7.py` — deterministic Jackson–Pollock 7 (BD → Siri/Brozek → FM/LBM),
  with typed domain errors instead of silent coercion.
- Studio shell: MASTER.md tokens 1:1, FINN-LOOP motion presets, launcher grid,
  `CoreStatus` health pill with loading/online/offline states.
- Electron main process with `contextIsolation: true`, `nodeIntegration: false`,
  `sandbox: true` (map §15).
- `LOOP_STATE.md`, `DESIGN_SYSTEM.md`, `ERRORS.log`, `NOTICES.md`, `run.sh`.

### Measured
- Backend: **73 tests passed** (12 JP7 golden fixtures inside ±0.05 %BF;
  external anchor BD 1.061664 vs published 1.06166).
- Studio: **25 tests passed**, `tsc --noEmit` clean, production bundle
  **91.73 kB gzip** (budget 250 kB).
- Live `curl :8751/health` → `{"status":"ok", "db":{"table_count":25,
  "schema_version":"0001_core"}}`, `x-response-ms: 2.9`.

### Fixed
- Circular import between the migration runner and `v001_core` (moved
  `Migration` into `migrations/base.py`).
- `NOT NULL constraint failed: gyms.gym_id` on seed (nullable + trigger).
- Deprecated `on_event("shutdown")` → `lifespan` (warnings 17 → 1).
- `uvicorn` could not load the app (no module-level `app`) → `create_app_from_env`
  + `--factory` + `run.sh`.

### Known gaps
- No ESLint/Prettier config; no coverage measurement; browser Core Web Vitals
  unmeasured; Electron binary not downloaded in this environment.
