# MP Changelog

Format: Keep a Changelog. Versioning: every release must move a measured number
(map rule C12).

## [0.7.0] — 2026-08-29 — Phase 5 client API (scoped + masked)

### Added
- `core/field_mask.py` — single choke point: `mask_member_row` / `mask_assessment_row`
  strip `note`/`clinician_note`/`created_by` for MEMBER, leave staff untouched.
- `/api/v1/client/{me,me/assessments,me/programs}` — MEMBER-only, force-scoped to
  the token's member_id; staff tokens are 403.

### Measured
- Backend: **208 tests passed** (penetration-style field-mask + scope tests).
- OpenAPI: 36 paths.

### Deferred
- Flutter client UI (home/logger/QR/payments-self) and pain feedback → Phase 6/7.

## [0.6.0] — 2026-08-29 — Phase 4 AI (backend slice: nutrition + runtime + race)

### Added
- `core/nutrition.py` — deterministic Katch–McArdle BMR from LBM, TDEE by activity
  factor, goal-adjusted target + macro split; golden-tested.
- `POST /api/v1/nutrition/members/{id}/plan` computes from the member's latest
  assessment LBM (422 if no assessment) and stores it; `GET .../plan` returns latest.
- `core/ai_brain.py` — weighted judge (map §5) + `race()` implementing rule C7:
  rules win when the LLM is absent, on ties, or when the LLM violates limitations;
  the LLM wins only when strictly better and safe. Injectable Ollama probe.
- `GET /api/v1/ai/runtime` — Ollama detection from `MP_AI_BASE_URL`; never required.

### Measured
- Backend: **203 tests passed** (nutrition golden + API, brain race/judge with a
  fake LLM, runtime detection incl. unreachable/500 paths, RBAC).
- OpenAPI: 33 paths.

### Deferred (documented, not dropped)
- RAG over the Knowledge Pack (needs a vector store + embeddings; no Ollama here).
- The AI-flavoured dry-run UI (mockup 08) — the backend dry-run endpoint already
  shipped in Phase 3.
- Iranian FA foods subset (nutrition math shipped; food database later).

## [0.5.0] — 2026-08-29 — Phase 3 programs without AI

### Added
- `core/program_builder.py` — pure, deterministic rule builder with PPL / UL / FB /
  corrective templates and per-pattern loading. Pipeline mirrors map §7:
  hard_block DROP → SWAP → equipment DROP → corrective block. Serialises to
  `mp.program/v1` whitelist ops only.
- `repo/programs.py` — lifecycle state machine
  (draft → trainer_approved → client_ack/needs_review → archived; archived terminal).
- Endpoints: `POST /members/{id}/programs/generate`, `GET /members/{id}/programs`,
  `POST /programs/{id}/dry-run`, `POST /programs/{id}/apply`,
  `POST /programs/{id}/archive`.
- C8 enforced twice: dry-run re-validates stored ops against the member's CURRENT
  injury filters, and apply 409s if any stored op is now hard-blocked.

### Measured
- Backend: **179 tests passed** (8 builder safety unit tests + 9 programs API
  integration tests incl. swap/drop, corrective block, dry-run-before-apply 409,
  terminal archive, RBAC 403).
- OpenAPI: 31 paths.

### Design notes
- Equipment availability uses the inventory `category` token (barbell/dumbbell/
  trap_bar/...) to match library equipment tokens; bodyweight always available.
- Rule C7 holds: the rule planner is the only planner shipped so far.

## [0.4.0] — 2026-08-29 — Phase 2 Ops (attendance, payments, equipment, seed)

### Added
- Attendance: `POST /attendance/check-in` (signed 60s QR or manual) verifying the
  HMAC signature and **denying expired memberships (402)**; double check-in is a
  409; `POST /attendance/check-out/{member_id}`; `GET /attendance/today`.
- Payments: packages CRUD (finance-only create), `POST /payments` (RECEPTION can
  enter cash, per map §2.4), `GET /payments/{id}/receipt` (A5 landscape PDF with
  grouped Rial), `POST /payments/{id}/void` (finance-only, tombstoned not deleted).
- Equipment inventory CRUD + availability toggle (OWNER/ADMIN manage).
- `GET /reports/dashboard` — members/active/injury/check-ins/revenue KPIs,
  finance-gated (TRAINER and RECEPTION get 403).
- Exercise library: `packs/exercises_seed.json` (30 exercises, all with FA names,
  18 with contraindications) + idempotent `python -m app.seed_exercises`;
  `GET /exercises` and `GET /exercises/{key}/contraindications`.

### Measured
- Backend: **162 tests passed** (attendance incl. expired-membership 402 + tampered
  QR 401; payments incl. receipt %PDF + void RBAC; equipment; dashboard; seed
  idempotency + contraindication-integration).
- Seed CLI: 30 inserted on first run, 0 on re-run.
- OpenAPI: 26 paths / 19 schemas.

### Notes
- The seed is a curated, MIT-friendly local JSON (`source: "curated"`); a real
  free-exercise-db export can be imported later through the same loader.
- KIOSK remains scan-only: it cannot read the exercise library or member list.

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
