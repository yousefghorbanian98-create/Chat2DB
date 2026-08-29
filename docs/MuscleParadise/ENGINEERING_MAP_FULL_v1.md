# 🏋️ MUSCLE PARADISE (MP) — COMPLETE ENGINEERING MAP v1.1
## Zero-to-One Spec for Any AI Coding Agent

> **How to use this document**  
> Paste this entire file into an AI coding agent as the **single source of truth**.  
> Build **only** under `mp-app/` and `docs/MuscleParadise/`.  
> **NEVER modify** `ce-app/**` or `docs/CuttingEdge/**` (Cutting Edge is a separate product — pattern source only).

**Brand:** Muscle Paradise · Logo monogram **MP**  
**Owner domain:** Gym OS for a personal trainer who runs Jackson–Pollock 7-site body composition  
**Map version:** 1.1 (2026-08-29) — added §12.7 Dev-Agent Tooling + download links  
**Date locked (product rules):** 2026-08-28 (Asia/Tehran context)  
**Repo:** https://github.com/yousefghorbanian98-create/Chat2DB  
**Branch with this pack:** `arena/01a048a6-chat2db`  

### Direct download links (always use branch raw URLs)
| What | URL |
|------|-----|
| **This map (raw MD)** | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/01a048a6-chat2db/docs/MuscleParadise/ENGINEERING_MAP_FULL_v1.md |
| **This map (GitHub view)** | https://github.com/yousefghorbanian98-create/Chat2DB/blob/arena/01a048a6-chat2db/docs/MuscleParadise/ENGINEERING_MAP_FULL_v1.md |
| **Full ZIP pack (~1.9MB)** | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/01a048a6-chat2db/docs/MuscleParadise/releases/MuscleParadise-EngineeringPack-v1.zip |
| **Dev-agent tooling doc** | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/01a048a6-chat2db/docs/MuscleParadise/DEV_AGENT_TOOLING.md |
| **Folder on GitHub** | https://github.com/yousefghorbanian98-create/Chat2DB/tree/arena/01a048a6-chat2db/docs/MuscleParadise |
| **Release tag page** | https://github.com/yousefghorbanian98-create/Chat2DB/releases/tag/mp-eng-v1.0 |

---

# 0. ONE-SENTENCE PRODUCT

> **Muscle Paradise = local-first Gym Operating System with dual shells (Studio for coach, Client for athlete), scientific JP7 assessment, injury-aware personalized training/nutrition, optional local AI (Ollama), P2P sync (QR/BT/Wi-Fi), no mandatory cloud bill — architected like Cutting Edge’s brain pattern (measure → plan → validate → score → dry-run → apply).**

---

# 1. NON-NEGOTIABLE CONSTRAINTS

| # | Rule |
|---|------|
| C1 | **Local-first.** Core works offline. Internet is optional for Knowledge Pack refresh and optional AI gateway. |
| C2 | **No mandatory cloud server / SaaS fee** for day-to-day gym ops. |
| C3 | **Never edit Cutting Edge code/docs** (`ce-app/`, `docs/CuttingEdge/`). Copy patterns into `mp-app/` only. |
| C4 | **Dual product shells:** MP Studio (coach) sees everything; MP Client (athlete) sees **only self** (server-side enforced). |
| C5 | **Injury + movement limitations are hard filters** before any program is activated. |
| C6 | **LLM never invents measurements.** JP7, TDEE, macros = deterministic code. AI only plans text/structure within whitelist ops. |
| C7 | **Rule planner always in the race.** If Ollama/gateway fails or scores worse, rules win (Cutting Edge brain pattern). |
| C8 | **Dry-run before Apply** for AI programs; one undoable apply. |
| C9 | **Permissive licenses inside the main binary.** Avoid GPL/AGPL code linked into the app process (wger is AGPL — ideas/data only unless whole app goes AGPL). |
| C10 | **PII/medical minimization.** Fingerprint = template/hash only. QR payloads signed. Client API field-masked. |
| C11 | **Persian-first UI** + English; Jalali calendar; Rial money formatting. |
| C12 | **Every release moves a measured number** (tests with known-answer fixtures), not vibes. |

---

# 2. PRODUCT SURFACE — TWO APPS, ONE BACKEND

## 2.1 MP Studio (Coach / Owner)
**Platforms:** Windows desktop (Electron + React), optional same UI as PWA on LAN PC.  
**Users:** OWNER, ADMIN, TRAINER, RECEPTION, KIOSK role.  
**Can:** all members, JP7, AI program gen, nutrition, finance, attendance, sync, settings, backups, equipment inventory, injury dossiers, reports, PDF.

## 2.2 MP Client (Athlete)
**Platforms:** Android (Flutter preferred) + installable PWA.  
**Auth:** username/password (membership code), optional device biometric.  
**Can only:** own profile, own workout log, own nutrition, own QR check-in, own payments history, own visible injury notes, coach messages to self.  
**Cannot:** list members, gym finance, other athletes, admin AI, server settings.

## 2.3 Kiosk mode
Locked Studio flavor: QR scan in/out only, auto-idle, PIN exit.

## 2.4 Roles (RBAC)

| Role | Scope |
|------|--------|
| OWNER | Everything + backup keys + destroy gym |
| ADMIN | Ops without owner-only |
| TRAINER | Assigned members; JP7; programs; notes; **no full finance** |
| RECEPTION | Check-in, renewals, cash payment entry |
| KIOSK | Scan only |
| MEMBER | Client app only |

---

# 3. MODULE CATALOG (BUILD THESE)

1. Auth (PIN / password / biometric / session lock)  
2. Members CRUD + photo + QR identity  
3. **Injury & Limitation dossier** (structured, not free-text-only)  
4. Jackson–Pollock 7 assessment + history charts + PDF  
5. Equipment inventory (filters AI exercises)  
6. Exercise library (seed from OSS)  
7. Rule-based program builder  
8. AI brain (Ollama + RAG + race/judge + dry-run)  
9. Nutrition (BMR/TDEE/macros + Iranian foods + allergies)  
10. Attendance check-in/out (QR signed + fingerprint optional)  
11. Payments / membership packages / receipts PDF  
12. Reports & dashboards  
13. Sync fabric (QR chunks / BT / Wi-Fi Direct / encrypted file)  
14. Knowledge Pack installer (offline zip)  
15. Delta app updater (electron-updater pattern)  
16. Settings / gym branding / i18n / About+licenses  
17. Consents & medical disclaimer signatures  
18. Messaging coach↔member  
19. Progress photos  
20. PT session packs (optional P1)

---

# 4. ARCHITECTURE

```
┌─────────────┐  ┌──────────────┐  ┌──────────┐  ┌─────────┐
│ Studio      │  │ Client       │  │ Kiosk    │  │ PWA     │
│ Electron+   │  │ Flutter/PWA  │  │ locked   │  │ same UI │
│ React       │  │              │  │ Studio   │  │         │
└──────┬──────┘  └──────┬───────┘  └────┬─────┘  └────┬────┘
       │                │               │             │
       └────────────────┴───────┬───────┴─────────────┘
                                ▼
                 MP Core  FastAPI + SQLite
                 default port **8751**  (do not use CE’s 8742)
                 Jobs + WebSocket progress + Cancel
                                │
          ┌─────────────────────┼─────────────────────┐
          ▼                     ▼                     ▼
   SQLite MP DB          Local AI stack         Sync + Backup
   + FTS5                Rule + Ollama          QR/BT/WiFi/file
                         + optional Gateway     CRDT/delta log
                         (OmniRoute)            encrypted packs
                         + RAG Knowledge Pack
```

### Stack (locked recommendation)

| Layer | Choice | Why |
|-------|--------|-----|
| Desktop UI | Electron 31 + React 18 + Vite + Ant Design 5 + Zustand + TanStack Query + Lucide + Vazirmatn | Copy **patterns** from Cutting Edge frontend |
| Local API | FastAPI + Uvicorn + SQLite (+ migrations) | CE pattern; simple offline |
| Jobs | Background tasks + WebSocket progress + cancel | Long AI/PDF/backup |
| Android | Flutter 3.x + sqflite/drift + local_auth + mobile_scanner | Member app |
| Charts Studio | Recharts or Ant Charts | |
| Charts Flutter | fl_chart | |
| PDF | reportlab and/or @react-pdf/renderer + Flutter `pdf` | |
| Local LLM | Ollama (llama3.1:8b on PC; smaller on weak HW) | Offline AI |
| Optional multi-model gateway | OmniRoute on :20128 | Dev/advanced only |
| Vectors | Chroma or LanceDB on PC; keep mobile thin (call PC on LAN) | RAG |
| CRDT/delta | Yjs or Automerge (MIT) | Multi-device merge |
| QR | qrcode + html5-qrcode / zxing / mobile_scanner | |
| Updates | electron-updater + GitHub Releases | CE UpdateCard pattern |

---

# 5. AI BRAIN (CUTTING EDGE PATTERN → SPORTS)

```
measurements = JP7 numbers + history delta + goals + injuries + limits + equipment + attendance adherence
        │
planners in parallel:
   A) Rule planner (deterministic templates PPL/UL/FB/corrective)
   B) Ollama planner (JSON program against schema, RAG context)
   C) optional second model via OpenAI-compatible gateway (OmniRoute)
        │
validator: whitelist ops only; clamp sets/reps/rest; drop unknown ops
        │
judge score (higher better):
   calorie_error ×3
   respects_limitations ×3
   equipment_available ×3
   muscle_balance ×2
   progressive_overload ×2
   novelty_vs_last ×1
        │
dry-run UI → trainer confirm → status trainer_approved → client_ack
```

**System prompt skeleton (FA/EN):** coach expert; never invent body-fat; only use provided measurements; respect contraindications list; output `mp.program/v1` JSON only.

**Priority of AI backends:**  
1) Rules always  
2) Ollama local default  
3) Optional `ai_base_url` (Ollama OpenAI compat OR OmniRoute `http://127.0.0.1:20128/v1`)  
4) Never require cloud; never send full PII when redact mode on

---

# 6. JACKSON–POLLOCK 7 (DETERMINISTIC)

### Sites (mm)
Chest, Midaxillary, Triceps, Subscapular, Abdominal, Suprailiac, Thigh

### Body density
**Men:**  
`BD = 1.112 − (0.00043499 × ΣSF) + (0.00000055 × ΣSF²) − (0.00028826 × Age)`

**Women:**  
`BD = 1.097 − (0.00046971 × ΣSF) + (0.00000056 × ΣSF²) − (0.00012828 × Age)`

### %BF
**Siri:** `%BF = (4.95/BD − 4.50) × 100`  
**Brozek:** `%BF = (4.57/BD − 4.142) × 100`

### Derived
`FM_kg = weight × BF/100`  
`LBM_kg = weight − FM`

### Classification (guide)
Men athletic ~6–13% … obese ≥32%; Women athletic ~14–20% … obese ≥40% (document source in UI disclaimer).

### Fallback protocols (P1)
JP3, JP4, Durnin-Womersley, Navy circumference — separate schema field `protocol`.

### Tests
Ship **≥10 golden fixtures** (M/F, ages, known sums) — assert BF within **0.05** absolute points.

---

# 7. INJURY & PERSONALIZATION (MANDATORY)

### Injury record fields
`body_region, side, label, status(active|recovering|cleared|chronic), pain_0_10, onset, cleared, aggravators[], contraindicated_patterns[], allowed_modifications[], clinician_note (Studio only), member_visible_note, requires_clearance, created_by`

### Regions enum
neck, cervical, thoracic, lumbar, SI, shoulder, scapula, elbow, wrist, hand, hip, groin, knee, ankle, foot, chest, abdomen, cardiovascular, respiratory, neurological, other

### Pipeline
```
exercise candidate
 → hard_block by region/pattern? DROP
 → replaceable? SWAP from allowed_mods / library
 → equipment missing? DROP
 → goal/JP7 score
 → publish only if trainer_approved (unless owner auto-publish)
```

### Client feedback
Athlete can flag “this move hurts” → `session_feedback` → Studio inbox → program `needs_review`.

### Program lifecycle
`draft → trainer_approved → client_ack → (needs_review|archived)`

---

# 8. DATABASE (SQLITE) — CORE TABLES

Implement with migrations (Alembic or custom). Every table: `id`, `gym_id`, `created_at`, `updated_at`, `deleted_at`, `rev`.

```
gyms, staff, members, member_trainer,
member_injuries, member_limitations,
body_assessments,
exercises, exercise_contraindications, gym_equipment,
training_programs, nutrition_plans,
attendance, payments, packages,
consents, messages, session_feedback, session_sets,
progress_photos, sync_log, devices, knowledge_packs_meta, audit_log
```

### Critical JSON schemas (versioned)
- `mp.assessment/v1`  
- `mp.program/v1` with ops: `addExercise|setSets|setReps|setRest|setRIR|addNote|swapExercise|addCorrectiveBlock`  
- `mp.nutrition/v1`  
- QR: `{v, typ, gym, mid, exp, sig}` HMAC/Ed25519  

### Soft-delete + tombstones
Required for sync. Never hard-delete rows that may exist on another device without tombstone.

---

# 9. API SKETCH (OpenAPI-first)

Base: `http://127.0.0.1:8751/api/v1`

```
GET  /health
POST /auth/login
POST /auth/pin
GET  /me

# Studio
CRUD /members
CRUD /members/{id}/injuries
CRUD /members/{id}/assessments
POST /members/{id}/assessments/calculate   # pure JP7
POST /members/{id}/programs/generate       # job → ws progress
POST /programs/{id}/dry-run
POST /programs/{id}/apply
CRUD /payments
POST /attendance/check-in
GET  /reports/dashboard
POST /sync/push | /sync/pull
POST /backup/export | /backup/import
GET  /ai/runtime

# Client (auto-scoped)
GET  /client/home
GET  /client/program/active
POST /client/session-sets
POST /client/feedback
GET  /client/qr
GET  /client/payments
```

**MEMBER token:** middleware forces `member_id = auth.uid` on every query.  
**Field masking:** strip `clinician_note`, other members, full finance.

Long ops = **async jobs** with WebSocket `/ws/jobs/{id}` + Cancel (lesson from CE timeouts).

---

# 10. REPO / FOLDER LAYOUT (CREATE NEW)

```
mp-app/
  backend/
    app/  (fastapi routers, schemas, models, services)
    core/
      jp7.py
      brain/ (rules, ollama, judge, race, prompts)
      sync/
      auth/
    tests/  (golden JP7, rbac, judge)
    migrations/
  studio/   # Electron+React (CE-like)
    src/pages features components styles
    electron/
  client/   # Flutter
  packs/    # knowledge pack build scripts
  openapi.yaml
docs/MuscleParadise/   # already exists — keep extending
  ENGINEERING_MAP_FULL_v1.md  (this file)
  EXECUTIVE_SCHEMATIC_v1.md
  PRODUCT_PARAMS_v1.md
  OSS_INTEGRATION_UIUX_OMNIROUTE.md
  DEV_AGENT_TOOLING.md
  design-system/muscle-paradise/MASTER.md
  mockups/
  tools/ui-ux-pro-max/
  releases/
```

**Forbidden paths to edit:** `ce-app/**`, `docs/CuttingEdge/**`.

---

# 11. UI/UX DESIGN SYSTEM (ALREADY GENERATED)

**Master:** `docs/MuscleParadise/design-system/muscle-paradise/MASTER.md`  
**Tool:** UI/UX Pro Max Skill (installed under `docs/MuscleParadise/tools/ui-ux-pro-max/`)

### Brand colors (locked)
| Token | Hex |
|-------|-----|
| Primary emerald | `#00B86A` |
| Gold | `#FFD700` |
| BG | `#0B0F14` |
| Card glass | dark translucent + blur 16px |
| Destructive | `#EF4444` |
| Warning | `#F59E0B` |

### Typography
- EN display: Barlow Condensed  
- EN body: Barlow  
- FA: **Vazirmatn**  
- Tabular nums for JP7 & money  

### Icons
Lucide only — **no emoji icons**.

### Shells
- Studio: launcher tile grid (mockup 06)  
- Client: bottom nav ≤5 (mockup 09)  
- Kiosk: single purpose (mockup 10)  

### Mockups (visual reference)
```
docs/MuscleParadise/mockups/
  01_launcher_home.jpg … 05_logo_mp_brand.jpg
  06_studio_home_ds.jpg
  07_jp7_assessment_ds.jpg
  08_ai_coach_dryrun_ds.jpg
  09_client_home_ds.jpg
  10_kiosk_checkin_ds.jpg
```
Treat as **direction**, not pixel-perfect; numbers in images may be nonsensical — implement real formulas.

### Regenerate design intel
```bash
cd docs/MuscleParadise
python3 tools/ui-ux-pro-max/scripts/search.py "gym dashboard" --design-system -p "Muscle Paradise" -f markdown
python3 tools/ui-ux-pro-max/scripts/search.py "glassmorphism" --domain style
python3 tools/ui-ux-pro-max/scripts/search.py "touch target" --stack flutter
```

---

# 12. OPEN-SOURCE RESOURCES (USE / DON’T USE)

## 12.1 MUST USE (design & platform)

| Resource | URL | License | Use |
|----------|-----|---------|-----|
| UI/UX Pro Max Skill | https://github.com/nextlevelbuilder/ui-ux-pro-max-skill | MIT | Design intelligence; already vendored under docs |
| Vazirmatn font | https://github.com/rastikerdar/vazirmatn | OFL | Persian UI |
| Lucide icons | https://lucide.dev | ISC | Icons |
| Ant Design | https://ant.design | MIT | Studio UI kit |
| Electron + electron-builder + electron-updater | electron projects | MIT | Desktop + delta updates |
| FastAPI | https://fastapi.tiangolo.com | MIT | API |
| Ollama | https://github.com/ollama/ollama | MIT | Local LLM runtime |
| Yjs | https://github.com/yjs/yjs | MIT | CRDT sync |
| Automerge | https://github.com/automerge/automerge | MIT | Alt CRDT |
| Recharts | https://github.com/recharts/recharts | MIT | Charts |
| Flutter local_auth | pub.dev/packages/local_auth | BSD | Biometrics |
| qr_flutter / mobile_scanner | pub.dev | BSD/Apache | Client QR |
| fl_chart | pub.dev/packages/fl_chart | MIT | Mobile charts |

## 12.2 FITNESS DATA (seed)

| Resource | URL | License | Use |
|----------|-----|---------|-----|
| free-exercise-db | https://github.com/yuhonas/free-exercise-db | **MIT** | **Primary exercise JSON seed (~800)** |
| free-exercise-db-with-videos | https://github.com/amiinwani/free-exercise-db-with-videos | MIT meta; check videos | Optional offline demos |
| USDA FoodData Central | https://fdc.nal.usda.gov/ | Public domain | Macro base |
| Open Food Facts | https://world.openfoodfacts.org/data | ODbL | Packaged foods; share-alike DB rules |
| ComprehensiveFoodDatabase | https://github.com/lxaw/ComprehensiveFoodDatabase | check LICENSE | Research seed |

## 12.3 GYM PRODUCT IDEAS (read; careful copy)

| Resource | URL | Notes |
|----------|-----|-------|
| wger | https://github.com/wger-project/wger | **AGPL-3** — do **not** link code into MP binary unless MP becomes AGPL. OK: UX ideas, API shape, CC exercise text if license allows |
| RJGATON007/gyms | https://github.com/RJGATON007/gyms | QR attendance + membership expire ideas |
| QR-Attendance-System | https://github.com/AzeemIdrisi/QR-Attendance-System | LAN QR check-in idea |
| GYM-One | https://github.com/mayerbalintdev/GYM-One | Module brainstorm |
| laravel-gymie | https://github.com/lubusIN/laravel-gymie | CRM ideas |
| fastnfitness | https://github.com/brodeurlv/fastnfitness | Android workout log UX |

## 12.4 AI GATEWAY (optional sidecar)

| Resource | URL | License | Use |
|----------|-----|---------|-----|
| OmniRoute | https://github.com/diegosouzapw/OmniRoute | MIT | Optional OpenAI-compatible gateway `:20128` for dev/advanced; **not** required offline core |
| Docs in-repo | `docs/MuscleParadise/OSS_INTEGRATION_UIUX_OMNIROUTE.md` | — | Integration policy |

## 12.5 PATTERN SOURCE (read-only in this monorepo)

| Path | Steal as pattern |
|------|------------------|
| `ce-app/backend` FastAPI+SQLite+jobs+ws | Core server shape |
| `ce-app/backend/core/brain/*` | Race/judge/planners |
| `ce-app/backend/core/assistant/planner.py` | Whitelist ops + validate |
| `ce-app/frontend` Electron React Ant Zustand i18n | Studio shell |
| `ce-app/frontend/src/components/UpdateCard.tsx` | In-app update UX |
| `ce-app/frontend/src/components/AiRuntimeCard.tsx` (if present) / GPU card | AI runtime status |
| `docs/CuttingEdge/BRAIN_DESIGN.md` | Philosophy: LLM doesn’t measure |
| `docs/CuttingEdge/ROADMAP_1.0.md` | Release = measured metric |

## 12.6 DO NOT SHIP INSIDE MAIN PROCESS
- GPL/AGPL libraries that force copyleft on whole app  
- Cloud-only SDKs as hard dependencies  
- Raw fingerprint images  
- Scrapers violating site ToS for exercise content  

## 12.7 DEV-AGENT TOOLING (build faster — NOT product runtime)

> These tools make the **coding agent** smarter while building `mp-app`.  
> They are **Layer A (developer laptop)**.  
> They do **not** replace JP7, free-exercise-db, Ollama, or Studio/Client (**Layer B = product**).  
> Full install notes: `docs/MuscleParadise/DEV_AGENT_TOOLING.md`

### Critical split
```
Layer A — Dev tools (this section)     →  speed/accuracy of AI coding agents
Layer B — Product runtime (rest of map) →  what the gym coach/athlete runs
```

### Recommended stack for building MP

| Priority | Tool | URL | License | Role for MP |
|----------|------|-----|---------|-------------|
| **P0** | **ChunkHound** | https://github.com/chunkhound/chunkhound | MIT | Local semantic + regex + git-history research with citations; index monorepo so agent finds CE patterns without editing `ce-app` |
| **P0** | **open-codebase-index** / `opencode-codebase-index` | https://github.com/Helweg/open-codebase-index | MIT | Semantic codebase index for OpenCode, Claude, Codex, MCP; tree-sitter + BM25 + call graph; Ollama embeddings |
| **P0** | **Librarian (docs)** | https://github.com/iannuttall/librarian | check repo | Up-to-date library/docs search for agents (FastAPI, Flutter, Electron…) so models stop inventing APIs |
| **P0** | **GitHub Copilot Chat (Agent)** | https://github.com/features/copilot | proprietary SaaS | Daily multi-file agent + semantic `#codebase` if you have a seat |
| **P1** | **Librarian CLI (tech explore)** | https://github.com/SkrOYC/librarian | Apache-2.0 | Agentic explore of technology repos (“how does X handle Y?”) |
| **P1** | **Open Aware** | https://github.com/qodo-ai/open-aware | see repo | MCP deep research on **pre-indexed public OSS** (FastAPI/React patterns); free tier rate-limited; private repos = commercial |
| **P1** | **Sourcegraph Deep Search** | https://sourcegraph.com/docs · product Deep Search | freemium / enterprise | NL questions over large codebases; use public sourcegraph.com for OSS examples; full self-host is overkill for thesis |
| **P2** | **SocratiCode** | https://github.com/giancarloerra/socraticode | **AGPL-3** | Excellent local MCP hybrid search + dependency graphs at huge scale — **DEV MACHINE ONLY**; never link into MP binary (copyleft) |
| **P3** | **OSS Compass** | https://oss-compass.org · https://github.com/oss-compass | AGPL components | Ecosystem **health** scores before forking gym/fitness repos (activity, not stars alone) |
| — | **Ziv** | *(name ambiguous — no canonical public tool locked)* | — | If you meant a specific repo, add its URL under DEV_AGENT_TOOLING; do not block Phase 0 on it |

### Related already-in-map (do not confuse)
| Tool | Section | Notes |
|------|---------|-------|
| UI/UX Pro Max | §11, §12.1 | Design intelligence for UI generation |
| OmniRoute | §12.4 | Optional **product/dev** LLM gateway, not a codebase indexer |
| Ollama | §5, §12.1 | Product local LLM **and** can embed for ChunkHound/indexers |

### Install sketch (developer machine only)
```bash
# --- Codebase intelligence (pick one primary) ---
# A) ChunkHound
pip install chunkhound          # or: uv tool install chunkhound
cd /path/to/Chat2DB
chunkhound index .
chunkhound research "How does ce-app brain race planner work? Do not edit ce-app."

# B) open-codebase-index (OpenCode / MCP hosts)
npm install open-codebase-index
# configure host per https://github.com/Helweg/open-codebase-index
ollama pull nomic-embed-text    # local embeddings

# --- Fresh framework docs for the agent ---
npm i -g @iannuttall/librarian
librarian setup
librarian search --library fastapi/fastapi "background tasks websocket"

# --- Optional deep OSS research (MCP) ---
# Open Aware: follow https://github.com/qodo-ai/open-aware README (MCP client config)

# --- Optional AGPL indexer (dev only, never ship in MP) ---
# SocratiCode: https://github.com/giancarloerra/socraticode
```

### Agent rules when using these tools
1. Index may include `ce-app/` as **read-only context** — still **never write** there.  
2. Prefer citations/file:line from ChunkHound / codebase-index over free-form memory.  
3. For gym **domain data**, still use §12.2 (free-exercise-db, USDA, OFF) — indexers don’t replace seeds.  
4. SocratiCode/OSS Compass AGPL code stays on the **dev** box; MP product stays MIT/Apache-friendly.  
5. Copilot/Sourcegraph cloud: avoid pasting raw member medical PII into prompts.

### What these tools do NOT replace
- JP7 golden tests · injury filters · RBAC Client isolation · offline Knowledge Packs · electron-updater · free-exercise-db seed  

---

# 13. KNOWLEDGE PACK FORMAT

Offline zip installed by Studio:

```
mp-kb-YYYY.MM/
  manifest.json       # version, hash, locale
  exercises.sqlite    # from free-exercise-db + FA translations
  foods_ir.sqlite
  foods_usda_subset.sqlite
  corrective_rules.json
  program_templates.json
  rag/embeddings + chunks.jsonl
  LICENSE-ATTRIBUTION.md
```

App update ≠ KB update (separate delta channels).

---

# 14. DEVELOPMENT ROADMAP (ORDERED, NO REWORK)

### Phase 0 — Skeleton (week 1)
- [ ] Create `mp-app/` monorepo  
- [ ] FastAPI `/health` on **8751**  
- [ ] SQLite schema + migrations + `gym_id`  
- [ ] openapi.yaml stub  
- [ ] Studio Electron hello + theme tokens from MASTER.md  
- [ ] STATE.md + this map linked  
- [ ] License attribution page stub  
- [ ] **Dev tooling:** install ChunkHound *or* open-codebase-index; index repo; optional Librarian docs (§12.7)  

### Phase 1 — Identity & JP7 (weeks 2–3)
- [ ] Staff auth PIN  
- [ ] Members CRUD + QR id  
- [ ] `jp7.py` + 10 golden tests  
- [ ] Assessment UI (mockup 07) + history chart  
- [ ] PDF assessment report  
- [ ] Injury/limitation CRUD + safety card UI  

### Phase 2 — Ops (weeks 4–5)
- [ ] Attendance QR signed check-in  
- [ ] Packages + payments + receipt PDF  
- [ ] Dashboard KPIs  
- [ ] Equipment inventory  
- [ ] Seed exercises from free-exercise-db + 30 FA translations  

### Phase 3 — Programs without AI (week 6)
- [ ] Rule templates PPL/UL/FB/corrective  
- [ ] Contraindication graph filter  
- [ ] Program JSON v1 + apply/archive  

### Phase 4 — AI (weeks 7–8)
- [ ] Ollama detect + AiRuntime settings  
- [ ] RAG over KB pack  
- [ ] Race rule vs Ollama + judge  
- [ ] Dry-run UI (mockup 08)  
- [ ] Nutrition rules + Katch-McArdle from LBM + FA foods subset  

### Phase 5 — Client app (weeks 9–10)
- [ ] Flutter auth scoped API  
- [ ] Home / workout logger / QR / payments self  
- [ ] Feedback pain → Studio  
- [ ] Field-mask tests (penetration style unit tests)  

### Phase 6 — Sync & harden (weeks 11–12)
- [ ] Delta sync + backup encrypt/restore test  
- [ ] electron-updater  
- [ ] Kiosk flavor  
- [ ] Demo Persian seed data  
- [ ] Thesis packaging: docs, screenshots, license screen  

### Success metrics (examples)
| Feature | Pass if |
|---------|---------|
| JP7 | fixture error < 0.05 %BF |
| Check-in | < 800ms local scan→OK |
| AI offline | 100% programs without Ollama via rules |
| AI with bad model | score ≤ rules never applied |
| Client isolation | zero cross-member rows in API tests |
| Backup | restore row counts match |

---

# 15. SECURITY CHECKLIST

- [ ] Password/PIN hashed (argon2/bcrypt)  
- [ ] JWT or session secrets local-only  
- [ ] QR HMAC/Ed25519 with gym secret  
- [ ] MEMBER RBAC server-side  
- [ ] SQL injection via ORM/params only  
- [ ] Electron: contextIsolation, no nodeIntegration in renderer  
- [ ] Backup: password-based encryption  
- [ ] Audit log for override injury filters & payment voids  
- [ ] Consent records versioned  
- [ ] Youth: guardian consent flag  

---

# 16. I18N & LOCALE

- Default `fa` with `en` toggle  
- Jalali primary in FA (`moment-jalaali` or dayjs jalali)  
- Currency: ریال display; store integer rials  
- RTL layout for FA; numeric fields `dir=ltr`  

---

# 17. AGENT BOOTSTRAP PROMPT (COPY THIS TOO)

```
You are building Muscle Paradise (MP), a local-first gym OS.
Read and obey: docs/MuscleParadise/ENGINEERING_MAP_FULL_v1.md (v1.1+)
Also: PRODUCT_PARAMS_v1.md, EXECUTIVE_SCHEMATIC_v1.md,
OSS_INTEGRATION_UIUX_OMNIROUTE.md, DEV_AGENT_TOOLING.md,
design-system/muscle-paradise/MASTER.md.

Rules:
- Create code only under mp-app/ and docs/MuscleParadise/
- NEVER modify ce-app/ or docs/CuttingEdge/ (read-only pattern source)
- Dual shells Studio vs Client with server-side isolation
- JP7 is pure code with golden tests
- Injuries hard-filter programs
- AI = rules + optional Ollama + dry-run + judge (CE brain pattern)
- UI: emerald #00B86A, gold #FFD700, dark glass, Vazirmatn, Lucide
- Port 8751 for API
- Prefer MIT/Apache deps; no AGPL in-process (wger, SocratiCode)
- Dev-only tools (ChunkHound, codebase-index, Librarian, Copilot, Open Aware)
  improve YOUR context — do not ship them inside the gym binary
- Every feature needs a measurable test

Start with Phase 0 skeleton (+ optional codebase index), then Phase 1 JP7+members+injuries.
```

---

# 18. QUICK INSTALL COMMANDS (DEV MACHINE)

```bash
# API
python -m venv .venv && source .venv/bin/activate
pip install fastapi uvicorn sqlalchemy pydantic alembic httpx reportlab

# Ollama
# https://ollama.ai — then:
ollama pull llama3.1:8b

# Optional gateway
# npm i -g omniroute && omniroute   # :20128

# Studio (when scaffolded)
# cd mp-app/studio && npm i && npm run electron:dev

# Exercise seed
git clone --depth 1 https://github.com/yuhonas/free-exercise-db /tmp/free-exercise-db
# import JSON into exercises table via script

# UI skill search
cd docs/MuscleParadise
python3 tools/ui-ux-pro-max/scripts/search.py "fitness dashboard" --domain ux

# Dev-agent codebase intelligence (optional but recommended) — see §12.7
# pip install chunkhound && chunkhound index .
# npm i -g @iannuttall/librarian && librarian setup
```

---

# 19. RELATED DOCS IN THIS REPO (READ ORDER)

1. `docs/MuscleParadise/ENGINEERING_MAP_FULL_v1.md` ← **you are here (v1.1)**  
2. `docs/MuscleParadise/DEV_AGENT_TOOLING.md` — ChunkHound, codebase-index, Librarian, Copilot, Open Aware, SocratiCode, OSS Compass  
3. `docs/MuscleParadise/PRODUCT_PARAMS_v1.md` — dual shell, injuries, backlog P0–P3  
4. `docs/MuscleParadise/EXECUTIVE_SCHEMATIC_v1.md` — gaps vs v1 map, CE reuse matrix  
5. `docs/MuscleParadise/OSS_INTEGRATION_UIUX_OMNIROUTE.md` — Pro Max + OmniRoute policy  
6. `docs/MuscleParadise/design-system/muscle-paradise/MASTER.md` — tokens  
7. `docs/MuscleParadise/design-system/muscle-paradise/pages/*.md` — page overrides  
8. `docs/MuscleParadise/mockups/*.jpg` — visual targets  
9. Read-only patterns: `docs/CuttingEdge/BRAIN_DESIGN.md`, `ce-app/` structure  

**External product links (owner’s other work — reference only):**  
- Repo: https://github.com/yousefghorbanian98-create/Chat2DB  
- Branch pack: https://github.com/yousefghorbanian98-create/Chat2DB/tree/arena/01a048a6-chat2db/docs/MuscleParadise  
- Cutting Edge release example: https://github.com/yousefghorbanian98-create/Chat2DB/releases/tag/v0.9.38  
- Map raw download: https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/01a048a6-chat2db/docs/MuscleParadise/ENGINEERING_MAP_FULL_v1.md  
- ZIP pack: https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/01a048a6-chat2db/docs/MuscleParadise/releases/MuscleParadise-EngineeringPack-v1.zip  

---

# 20. DEFINITION OF DONE (v1.0 PRODUCT)

A clean Windows install + Android Client on gym LAN with **no internet**:
1. Register member with knee injury limitation  
2. Enter JP7 → correct BF% vs fixture math  
3. Generate program → blocked exercises swapped → dry-run → apply  
4. Athlete logs in Client → sees only own program → logs sets → flags pain  
5. QR check-in works; expired membership denied  
6. Cash payment + PDF receipt  
7. Encrypted backup → restore on second PC → data matches  
8. About screen lists OSS licenses  

---

# 21. FINAL ARCHITECTURE SLOGAN FOR THE AGENT

```
MEASURE (JP7, attendance, payments) in code.
PLAN (rules ⊕ local AI) with whitelist JSON.
VALIDATE + SCORE + DRY-RUN like Cutting Edge.
FILTER every plan through injuries & equipment.
SHIP two windows (Studio / Client) on one local core.
PACK knowledge offline; cloud never required.
```

---

**END OF ENGINEERING MAP v1.1**  
File path: `docs/MuscleParadise/ENGINEERING_MAP_FULL_v1.md`  
Changelog 1.0 → 1.1: §12.7 Dev-Agent Tooling; download link table; Phase 0 + bootstrap + §18/§19 updates.  
Cutting Edge tree: untouched by design.
