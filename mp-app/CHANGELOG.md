# MP Changelog

Format: Keep a Changelog. Versioning: every release must move a measured number
(map rule C12).

## [0.3.0] — 2026-08-29 — Phase 1 PDF assessment report

### Added
- `app/core/pdf_report.py` — reportlab A4 report: branding, member line, result
  table (Siri primary + Brozek), the 7 measured sites, a history table, and the
  population-equation disclaimer. `compress` flag lets tests read the text layer.
- `GET /api/v1/members/{id}/assessments/{id}/pdf` returns `application/pdf` with a
  `Content-Disposition: attachment` header; 404s unknown and cross-member ids.

### Measured
- Backend: **140 tests passed** (5 PDF unit + 3 PDF API tests incl. cross-member 404).
- Live over HTTP: 200, `application/pdf`, 2767 bytes, magic `%PDF-`.

### Notes
- Body text is English for now (reportlab ships only Latin base fonts); embedding
  Vazirmatn (OFL) for a true Persian PDF is deferred and tracked in LOOP_STATE.

## [0.2.1] — 2026-08-29 — Phase 1 assessment UI (frontend)

### Added
- `pages/AssessmentJp7.tsx` — mockup 07 layout: athlete card, 7-site form with
  numbered silhouette markers, results panel, injury safety banner, error
  summary, and a BF% trend chart at the bottom. RTL + `dir="ltr"` numerics.
- `pages/jp7Validation.ts` — pure form validation (validate on blur; block
  Calculate on empty/<=0), unit-tested (7 tests).
- `core/jp7.ts` — client-side mirror of the JP7 math for the live preview,
  unit-tested against the same golden fixtures as the backend.
- `components/` — `NumberField` (decimal, ltr, tabular), `StatCard` (count-in),
  `BodyFatChart` (Recharts, animated draw, labelled empty state).
- `auth/AuthContext.tsx` + `pages/Login.tsx` — staff PIN login; 401 gives a
  single neutral message (no user enumeration).

### Performance (Performance Watchdog)
- Initial bundle was 204.51 kB gzip once recharts landed — over the loop's own
  comfort zone — so the assessment route is now `React.lazy` code-split:
  **initial 93.97 kB gzip**, assessment chunk 111.06 kB lazy.

### Measured
- Studio `npm run gate`: `tsc --noEmit` clean, **45 tests passed**, build OK.
- Live over the Vite proxy: login → member → assessment save (BF 10.2092,
  "athletic") → history rows 1.

### Known gaps
- PDF assessment report (Phase 1) still pending (`reportlab` not installed).
- Lucide icons not yet wired (no-emoji rule still relies on text markers).

## [0.2.0] — 2026-08-29 — Phase 1 identity & JP7 (backend)

### Added
- `app/core/security.py` — PBKDF2-HMAC-SHA256 (200k iters, random salt,
  constant-time compare), machine-local HMAC session tokens with expiry, and
  HMAC-signed 60s QR payloads per map §8. Machine key auto-created at mode 0600.
- `app/auth/deps.py` — bearer-token principal, role guards, and a 401 that
  cannot distinguish "no such user" from "wrong PIN" (no user enumeration).
- `app/auth/scope.py` — TRAINER scoping: member lists filtered to assigned
  members, unassigned access returns **404** so a trainer cannot even learn the
  member exists.
- Staff PIN login (`POST /api/v1/auth/pin`), `/auth/me`, members CRUD with
  tombstones, signed `GET /members/{id}/qr`.
- JP7 assessments: `POST /members/{id}/assessments` (compute + persist, sex read
  from the member record, never from the request), history endpoint, and a
  stateless `POST /assessments/calculate` for live form previews.
- Injury dossier: CRUD, contraindication patterns + allowed modifications,
  `GET /members/{id}/filters` (the exact input Phase 3's filter graph needs), and
  a field-masked member view that strips `clinician_note` server-side.
- `app/bootstrap.py` — seeds the gym + OWNER from `MP_OWNER_PIN`.

### Measured
- Backend: **132 tests passed** (24 security, 33 schema, 32 golden, 43 API/RBAC).
- Live E2E over real HTTP on :8752: login → member → JP7 (BD **1.050006**, BF
  **21.4259**, FM 13.3912, LBM 49.1088, "fit") → injury → filters → masked view
  (`clinician_note leaked? False`) → signed QR → injury badge = 1.
- OpenAPI regenerated: **13 paths / 13 schemas**.

### Fixed
- RBAC hole: `require_staff` included KIOSK, so the kiosk could create/list
  members. Split into read/write role sets; KIOSK is now 403 on both.
- RBAC hole: TRAINER could read every member — `staff_can_see_member()` existed
  but had zero call sites. Now enforced across members, assessments, injuries.
- A test asserted a **guessed** %BF literal (21.5437 vs the true 21.4259); the
  implementation was right. Rule added: never paste an uncomputed literal.

### Known gaps
- Assessment UI + history chart and the PDF report (Phase 1) are still pending;
  `reportlab` is not installed. ESLint/Prettier and coverage remain unconfigured.

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
