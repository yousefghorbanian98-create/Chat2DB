# MP Changelog

Format: Keep a Changelog. Versioning: every release must move a measured number
(map rule C12).

## [0.19.0] — 2026-08-30 — Jalali dates, athlete nutrition, installers + differential update

### Added (packaging & update)
- `app/updater.py` + `mp update` — differential self-update. Every package and
  every install carries a `MANIFEST.json` (version + sha256 per file); the
  updater diffs them and writes **only** the files that differ. `--dry-run`
  shows the plan first (map rule: dry-run before apply).
- Transactional apply: the current tree is archived, the result is re-hashed
  against the new manifest, and a mismatch restores the previous version.
  `venv/`, `bin/` and `*.db*` are protected — the gym's database is never
  touched (verified: identical sha256 across an update).
- `build_dist.sh` emits `patch-<old>-to-<new>.tar.gz` via `MP_PATCH_FROM`, which
  applies through the same `mp update`: 13 KB where the full package is 684 KB.
- Single-service mode (`MP_STATIC_DIR`) so one process serves the API and the
  prebuilt Studio shell on one port; installers (`install.sh` / `install.ps1`)
  and a `mp init|demo|start|update|test` launcher.


### Added
- `studio/src/core/jalali.ts` — dependency-free Gregorian → Jalali conversion
  (published jalaali arithmetic, MIT) plus `faDigits`. `Intl`'s Persian calendar
  is not present on every target (old kiosks, jsdom), so the math is ours and
  unit-pinned. Nine golden anchors cross-checked against an independent
  implementation (Python `jdatetime`) — including Nowruz 1405 (2026-03-21) and a
  leap Esfand (2025-03-20 → 1403-12-30).
- `ClientShell` renders assessment dates **and** membership expiry as Jalali;
  both were raw ISO slices before (a Persian-first contract gap).
- `GET /client/me/nutrition` — the athlete's own plan, force-scoped and passed
  through the new `mask_nutrition_row`, which strips the internal `payload`
  envelope (PII minimization). `NutritionCard` shows kcal + macros.

### Fixed
- `requirements.txt` was missing `cryptography` (a fresh install could not even
  import the app — `app/core/backup.py` needs Fernet) and `PyMuPDF` (its absence
  silently skipped the PDF text-extraction test).

### Measured (C12)
- Backend tests **231 → 249** (+3 client-nutrition, +10 updater); coverage
  **90.81%**, gate exit 0. Studio tests **96 → 110** (+13 jalali anchors/cases, +1 nutrition card);
  `tsc --noEmit` 0, `eslint .` 0.
- Live E2E on the running core: coach plan (LBM 50.0857 → BMR 1451.9, TDEE
  2250.4, protein 90.2 — all match `370 + 21.6·LBM`, `×1.55`, `1.8 g/kg` by
  hand); athlete read returns the same numbers with **no `payload`**; staff
  token on `/client/me/nutrition` → **403**.

## [0.18.0] — 2026-08-30 — Athlete web client shell (§5, dual-shell isolation)

### Added
- `studio/src/pages/ClientShell.tsx` + `hooks/useClientData.ts` — the athlete
  shell: Persian profile, masked assessment trend and program list, all read
  only from `/client/*` (server strips clinician notes, C9). Loading / error /
  empty / success states.
- Dual-mode `Login` — a Staff / Athlete toggle; athlete mode signs in with
  membership code + PIN via `POST /auth/member-pin` (added to the api client).
- `App` routes a MEMBER token to `<ClientShell>` instead of the coach shell.

### Measured (C12)
- Live E2E on the running core: `POST /auth/member-pin` (MP-DEMO-1/1234) → MEMBER
  token; `GET /client/me` → masked profile; wrong PIN → 401; **staff token on
  `/client` → 403** (isolation holds).
- Studio tests **90 → 96** (+6: ClientShell render/empty/error, Login dual-mode);
  `tsc --noEmit` 0, `eslint .` 0.

## [0.17.0] — 2026-08-30 — Persian demo seed (C12, demoable out of the box)

### Added
- `app/seed_demo.py` — idempotent CLI that creates one Persian demo member
  («نسیم رحیمی», code MP-DEMO-1, PIN 1234) with a stored JP7 assessment whose
  number equals the deterministic core, a package, a payment and a check-in.
  Re-running creates nothing new (verified).

### Measured (C12)
- Backend tests **229 → 231** (+2 seed tests); coverage **90.38%**.

## [0.16.0] — 2026-08-30 — Member self-service PIN login (client shell, §5)

### Added
- Migration `0002_member_pin`: `members.pin_hash` (PBKDF2, never plaintext, never
  in any read projection).
- `POST /api/v1/auth/member-pin` — membership code + PIN → MEMBER-scoped token
  (identical 401 for unknown/unset/wrong: no enumeration).
- `POST /api/v1/members/{id}/pin` — front-desk writers (OWNER/ADMIN/RECEPTION)
  set a member's PIN; readers (TRAINER) get 403.

### Measured (C12)
- Backend tests **225 → 229** (+4 member-PIN tests); coverage **90.66%**.

## [0.15.0] — 2026-08-30 — Persian cash/card receipt

### Changed
- `receipt_pdf.py` renders Persian by default (same `persian` module + font),
  English fallback; `_rial(value, persian=False)` stays backward compatible.
- Verified by rendering: title «ماسل پارادایز — رسید», Persian labels, grouped
  amount in accent green, status «پرداخت شد».

### Measured (C12)
- Backend tests **224 → 225** (+1 Persian receipt test); suite green with
  python-bidi (LGPL) uninstalled.

## [0.14.0] — 2026-08-30 — Persian PDF + backend coverage gate

### Added
- `app/core/persian.py` — Persian font registration + MIT shaping (`arabic-reshaper`
  for joining, an in-house UAX #9 subset for RTL reordering). No copyleft runtime
  dependency (see Security note).
- Assessment PDF now renders in **Persian** by default when a font is present,
  with English fallback; verified visually (rendered PNG) and by PyMuPDF
  round-trip. Numbers stay Latin and intact (rule C6).
- `mp-app/assets/fonts/PersianSans-Regular.ttf` (bundled, honest provenance).
- Backend coverage gate: `pytest-cov` pinned; `pytest.ini` fails below 80%.

### Security (C11)
- Rejected `python-bidi` (LGPL-3.0) after catching its COPYING at install time;
  replaced with the in-house MIT reorderer. `arabic-reshaper` (MIT) is the only
  runtime shaping dep.

### Fixed
- NOTICES.md no longer falsely claims the bundled font is "Vazirmatn / OFL"; it
  is documented as DejaVu Sans 2.37.

### Measured (C12)
- Backend tests **219 → 224** (+5 Persian-PDF tests); coverage **90.55%**, gate ≥80.
- Persian PDF embeds a ~53 KB TrueType subset (FontFile2), 100% glyph coverage.

## [0.13.0] — 2026-08-30 — Studio quality gate closed (lint · format · coverage)

### Added
- ESLint flat config + Prettier config, both wired into `npm run gate`
  (`lint && format:check && typecheck && coverage && build`).
- `@vitest/coverage-v8` — coverage is now a measured number, not a claim.
- `pages/assessmentJp7.test.tsx` — 7 tests rendering the whole assessment page:
  labelled skeleton, member picker, injury banner, blocked-calculate, field-error
  summary, the golden Siri result, and save-through-the-core.
- `ResizeObserver` stub in `vitest.setup.ts` (recharts measures its container;
  jsdom does not implement it, so `BodyFatChart` could not render under test).

### Changed — structure (behaviour preserved)
- Every surface decomposed to satisfy `max-lines-per-function` ≤ 50. Inline
  `style={{…}}` literals were hoisted to module constants (`styles/blocks.ts`),
  which also removes a per-render allocation.
- New hooks: `useCoreHealth`, `useOpsKpis`, `useCheckin`, `usePayment`,
  `useSyncOps` (`useSyncOps`/`useBackupCreate`/`useRestore`), `useNutrition`,
  `useProgramPlanner` + `useProgramActions`.
- New components: `components/assessment/*` (6 files), `OpsKpis`, and the
  sub-components each page was split into.
- `api/client.ts` split into `api/types.ts` (26 declarations) + `client.ts`.
- `auth/` split into `sessionContext.ts` + `AuthContext.tsx` + `useAuth.ts` so
  `react-refresh/only-export-components` is satisfied.

### Fixed
- **Unreachable success state:** `ResultPanel` rendered the "saved"
  confirmation in an `else` branch after `preview ?`, while save is only enabled
  once a preview exists — the confirmation could never appear. It now renders
  alongside the preview. Found by the new test, not by review.
- **Stale-result regression introduced and reverted in this same pass:** moving
  Coach's state into a hook dropped the plan-clear on athlete change. `selectMember`
  now clears plan/error/state; the same pattern guards `useProgramPlanner`.

### Measured (C12 — every release moves a number)
- ESLint: **21 → 0 problems** with `--max-warnings=0`.
- Prettier: **29 files → 0**.
- Tests: **83 → 90 passed** (10 files).
- Statement coverage: **63.92% → 82.24%** (branch 79.92%, functions 85.46%).
- `tsc --noEmit` exit 0; `npm run gate` exit 0.
- Backend: **90.54%** statement coverage (219 tests, 1967 statements) — first
  measurement. `pytest-cov` pinned and wired as a hard gate in `pytest.ini`
  (`--cov-fail-under=80`); verified to exit 1 when the bar is raised to 95%.
  The only 0% files are the two CLI dev scripts (`export_openapi.py`,
  `seed_exercises.py`), which are entry points rather than library code.
- Initial bundle **95.33 kB gzip** (gate < 250 kB); `AssessmentJp7` + recharts
  stays in its own lazy chunk at **112.05 kB gzip**.

## [0.12.0] — 2026-08-29 — Studio sync & backup surface (Phase 6 UI)

### Added
- `pages/Sync.tsx` — delta-sync console plus password-encrypted backup/restore.
  - Delta: first sync pulls a full snapshot, then the cursor is carried forward;
    an idle sync says so in words instead of rendering an empty box.
  - Backup: Fernet blob downloaded client-side as `mp-backup-<date>.mpbk`; the
    password is never persisted, and a non-OWNER is told why it was refused.
  - Restore: reports the **verified** row count (the server re-checks every table
    after reload), and a wrong password surfaces the server's own message.
- `api/client.ts` — `createBackup` / `restoreBackup` with `BackupBlob` /
  `RestoreResult` types.

### Measured
- Studio: **83 tests passed** (was 75) — 8 new covering snapshot wording,
  per-table changes, cursor storage, idle sync, the password gate, backup size,
  the 403 path, verified restore, and wrong-password failure.
- `tsc --noEmit` clean; initial bundle **94.81 kB gzip**; `Sync` code-split at
  **2.02 kB gzip**.
- Live E2E on the running core: backup 200 (4258 bytes, magic `MPBK1\x00`),
  ciphertext leak check passed (`members` and `first_name` absent from the blob),
  restore with the right password 200 → **59 rows across 25 tables** with counts
  verified, restore with a wrong password 422.

## [0.11.0] — 2026-08-29 — Studio coach surface (Phase 4 UI)

### Added
- `pages/Coach.tsx` — deterministic nutrition (goal × activity → BMR / TDEE /
  target / protein / carbs / fat) plus an honest AI-runtime card.
  - **No client-side nutrition maths**: every kcal and gram is the server's
    answer. A 422 (no assessment with LBM) is translated into "register a JP7
    assessment first" — the client never fabricates a number (rule C4).
  - AI card states plainly when no local model is reachable and always shows the
    C7 note that rules stay authoritative.
  - Clinical disclaimer travels with every plan.

### Measured
- Studio: **75 tests passed** (was 70) — 5 new covering offline-AI honesty, the
  no-assessment guard, server-computed macros, the disclaimer, and the disabled
  compute button.
- `tsc --noEmit` clean; initial bundle **94.69 kB gzip**; `Coach` code-split at
  **2.18 kB gzip**.
- Nutrition math independently re-derived and matched the live server:
  LBM 71.8327 → BMR `370 + 21.6×71.8327 = 1921.6`; TDEE `×1.725 = 3314.7`;
  cut target `×0.85 = 2817.5`; protein `×1.8 = 129.3`; fat `25%÷9 = 78.3`;
  carbs `399.0`.

## [0.10.0] — 2026-08-29 — Studio program planner (Phase 3 UI)

### Added
- `pages/Programs.tsx` — rule-planner console: member + template (PPL / UL /
  Full Body / Corrective) → generate → dry-run → apply → history. Apply stays
  **disabled until a dry-run returns `safe_to_apply`** (rules C6 + C8), and a 409
  from the server is surfaced rather than swallowed.
- `components/ProgramPreview.tsx` — the transparency surface: days with their
  exercises, the injury filters in force, and **every dropped exercise with a
  Persian reason** (hard block / equipment / duplicate / no candidate).
- `api/client.ts` — `generateProgram`, `listPrograms`, `dryRunProgram`,
  `applyProgram`, `archiveProgram`, `planNutrition`, `getNutrition`, with types
  derived from `openapi.yaml` and a live response (not from memory).

### Measured
- Studio: **70 tests passed** (was 62) — 8 new covering generate, drop reasons,
  the apply gate in both dry-run outcomes, the C8 409, and history empty/full.
- `tsc --noEmit` clean; initial bundle **94.60 kB gzip**; `Programs` code-split
  into **2.80 kB gzip**.
- Live E2E on the running core (after seeding the 30-exercise library):
  generate 201 → day A `ex007/ex010/ex026`, day B `ex022/ex025`; dry-run
  `safe_to_apply: true`; apply 200 → `trainer_approved`; archive 200 → `archived`.

## [0.9.0] — 2026-08-29 — Studio Operations console (Phase 2 UI)

### Added
- `pages/Operations.tsx` — daily-ops console: door KPIs for everyone, money KPIs
  only for OWNER/ADMIN (§2.4), with loading / error+retry / success states.
- `components/CheckinPanel.tsx` — manual check-in + signed-QR paste. HTTP codes
  become actionable Persian: 402 expired, 409 already inside, 401 tampered QR.
- `components/PaymentPanel.tsx` — package quick-pick, Rial entry, method chips,
  receipt PDF link.
- `ops/opsValidation.ts` — pure `formatRial` / `parseRial` (Persian digits +
  separators) / `validatePayment` / `qrLooksComplete`.
- `.mp-input` + `.mp-chip` in `tokens.css` with hover/focus/active states;
  motion is transform+opacity only and neutralised by `prefers-reduced-motion`.

### Fixed
- `api/client.ts` shipped wrong paths/types: packages are at `/api/v1/packages`
  (the payments router has no prefix), `/attendance/today` returns `check_ins`
  not `count`, and the dashboard/payment/package field names did not match the
  server. All verified live against the running core.

### Measured
- Studio: **62 tests passed** (was 45); `tsc --noEmit` clean.
- Build: initial **94.40 kB gzip** (< 250 kB bar); `Operations` split into its
  own **3.43 kB gzip** chunk; recharts stays in the lazy `AssessmentJp7` chunk.
- Live E2E on the running core: check-in 201 → repeat 409; payment 201 with
  `receipt_no` `R-1-000001`; dashboard moved `check_ins_today` 0→1 and
  `revenue_rial_this_month` 0→1,500,000 (C12: a measured number moved).

## [0.8.0] — 2026-08-29 — Phase 6 sync & harden (backend slice)

### Added
- `core/backup.py` — password-encrypted backup (Fernet + LZMA, PBKDF2-HMAC-SHA256
  200k iterations) over every business table; `restore_backup` reloads and
  `verify_row_counts` asserts the restore (success metric: counts match).
- `core/sync.py` + `GET /api/v1/sync/delta` — cursor-based delta sync (max
  updated_at), full snapshot on empty cursor, tombstones included.
- `POST /api/v1/admin/backup` + `/restore` — OWNER-only.
- Dependency: `cryptography` 50.0.1 (Fernet) installed into `.venv-mp`.

### Measured
- Backend: **219 tests passed** (backup ciphertext/round-trip/wrong-password/
  bad-magic, sync cursor + RBAC, 39 OpenAPI paths).

### Deferred
- electron-updater, Kiosk flavour, Persian demo seed, thesis packaging (client side).

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
