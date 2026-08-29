# Muscle Paradise — Dev-Agent Tooling Guide
## Layer A: make coding agents faster (not part of the gym binary)

**Map version:** pairs with `ENGINEERING_MAP_FULL_v1.md` **v1.1+** §12.7  
**Product (Layer B) is unchanged:** JP7, Studio/Client, Ollama, free-exercise-db, etc.

---

## 0. Direct links

| Resource | Link |
|----------|------|
| Engineering map v1.1 (raw) | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/01a048a6-chat2db/docs/MuscleParadise/ENGINEERING_MAP_FULL_v1.md |
| This file (raw) | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/01a048a6-chat2db/docs/MuscleParadise/DEV_AGENT_TOOLING.md |
| ZIP pack | https://raw.githubusercontent.com/yousefghorbanian98-create/Chat2DB/arena/01a048a6-chat2db/docs/MuscleParadise/releases/MuscleParadise-EngineeringPack-v1.zip |
| Folder | https://github.com/yousefghorbanian98-create/Chat2DB/tree/arena/01a048a6-chat2db/docs/MuscleParadise |

---

## 1. Principle

```
┌──────────────────────────────────────────────┐
│ Layer A — Developer laptop / CI agent host   │
│ ChunkHound · codebase-index · Librarian      │
│ Copilot · Open Aware · SocratiCode (dev)     │
│ Sourcegraph · OSS Compass                    │
└──────────────────────┬───────────────────────┘
                       │ better context & fewer wrong files
                       ▼
┌──────────────────────────────────────────────┐
│ Layer B — Muscle Paradise product (shipped)  │
│ mp-app Studio/Client · FastAPI :8751         │
│ JP7 · injuries · Ollama · KB packs · QR      │
└──────────────────────────────────────────────┘
```

**Never** bundle Layer A servers into the Windows gym installer unless you deliberately productize them (you should not for v1).

---

## 2. Tool cards (evaluated for MP)

### 2.1 ChunkHound — **P0 recommended**
- **Repo:** https://github.com/chunkhound/chunkhound  
- **License:** MIT  
- **What:** Local-first codebase intelligence; semantic + regex; git history research; citations; MCP.  
- **MP use:** Index monorepo; ask “how does CE race planner work?”; copy patterns into `mp-app/` only.  
- **Install:**
  ```bash
  pip install chunkhound
  # or: uv tool install chunkhound
  cd /path/to/Chat2DB
  chunkhound index .
  chunkhound research "Where is the brain race/judge implemented in ce-app? Read only."
  ```

### 2.2 open-codebase-index / opencode-codebase-index — **P0**
- **Repo:** https://github.com/Helweg/open-codebase-index  
- **License:** MIT  
- **What:** Semantic index for OpenCode, Claude, Codex, Pi, MCP; tree-sitter; BM25; call graph; Ollama/OpenAI/Google embeddings.  
- **MP use:** Same as ChunkHound if your host is OpenCode-centric.  
- **Install:**
  ```bash
  npm install open-codebase-index
  # or npm install opencode-codebase-index
  ollama pull nomic-embed-text
  # then host-specific plugin config — see upstream README
  ```

### 2.3 Librarian (docs search) — **P0**
- **Repo:** https://github.com/iannuttall/librarian  
- **What:** Local CLI/MCP so agents search **current** framework docs (not training-cutoff guesses).  
- **MP use:** FastAPI jobs/WS, Electron updater, Flutter local_auth, Ant Design forms.  
- **Install:**
  ```bash
  npm i -g @iannuttall/librarian
  librarian setup
  librarian search --library fastapi/fastapi "BackgroundTasks websocket"
  librarian search --library electron/electron "contextIsolation preload"
  ```

### 2.4 Librarian CLI (tech repo explorer) — **P1**
- **Repo:** https://github.com/SkrOYC/librarian  
- **License:** Apache-2.0  
- **What:** Agentic explore of named technology checkouts.  
- **MP use:** Deep dives when implementing a new subsystem.

### 2.5 GitHub Copilot Chat (Agent mode) — **P0 if you have a seat**
- **Product:** https://github.com/features/copilot  
- **Docs (agent / semantic codebase):** GitHub Copilot docs + VS Code Copilot Chat  
- **MP use:** Daily multi-file implementation against this map; `#codebase` semantic attach.  
- **Rule:** Do not paste real athlete medical PII into cloud prompts; use synthetic fixtures.

### 2.6 Open Aware — **P1**
- **Repo:** https://github.com/qodo-ai/open-aware  
- **What:** MCP “deep research” over **pre-indexed popular public OSS**.  
- **MP use:** “How do mature FastAPI apps structure long jobs?” without cloning everything.  
- **Limits:** Free public tier rate-limited; private code needs commercial Qodo Aware.

### 2.7 Sourcegraph Deep Search — **P1 / optional**
- **Docs:** https://sourcegraph.com/docs (Deep Search feature)  
- **What:** Natural-language agentic search over indexed code.  
- **MP use:** Public OSS examples on sourcegraph.com; full self-host is heavy for a thesis gym app.  
- **VS Code extension (search):** marketplace “Search by Sourcegraph”

### 2.8 SocratiCode — **P2 DEV ONLY**
- **Repo:** https://github.com/giancarloerra/socraticode  
- **License:** **AGPL-3.0**  
- **What:** Zero-config local MCP; hybrid semantic search; polyglot dependency graphs; huge monorepos.  
- **MP use:** Optional on **developer machine** for graph/blast-radius.  
- **Hard rule:** Do **not** link SocratiCode into the MP product binary (copyleft). Same policy as wger.

### 2.9 OSS Compass — **P3**
- **Site:** https://oss-compass.org  
- **Org:** https://github.com/oss-compass  
- **What:** Open-source **ecosystem health** analytics (not a code indexer).  
- **MP use:** Before adopting a gym/fitness dependency, check activity/community health — not star count alone.

### 2.10 Ziv — **unresolved name**
No single canonical public “Ziv” tool was locked for this map.  
If you have a specific GitHub URL, add it here and re-rank. **Do not block Phase 0** waiting on Ziv.

### 2.11 Already mapped (related, not new)
| Tool | Map section | Link |
|------|-------------|------|
| UI/UX Pro Max | §11 / §12.1 | https://github.com/nextlevelbuilder/ui-ux-pro-max-skill |
| OmniRoute | §12.4 | https://github.com/diegosouzapw/OmniRoute |
| Ollama | §5 | https://github.com/ollama/ollama |

---

## 3. Suggested default kit for this project

| You use… | Install |
|----------|---------|
| Any agent + local privacy | **ChunkHound** + **Librarian (iannuttall)** |
| OpenCode-first | **open-codebase-index** + Librarian |
| Paid GitHub seat | above + **Copilot Chat Agent** |
| Need OSS architecture research | + **Open Aware** |
| Huge graph needs | + **SocratiCode** (dev AGPL sandbox only) |
| Picking between gym OSS forks | **OSS Compass** glance |

---

## 4. Safe workflow with Cutting Edge

1. Index whole repo including `ce-app/` (read context).  
2. Agent prompt always includes: **NEVER modify `ce-app/**` or `docs/CuttingEdge/**`**.  
3. When copying a pattern (brain race, UpdateCard, jobs+WS): re-implement under `mp-app/`.  
4. Verify with MP tests (JP7 fixtures, RBAC), not by editing CE.

Example research prompts:
```
chunkhound research "Explain ce-app core/brain race between rule and ollama planners. Cite files. We will reimplement under mp-app/backend/core/brain only."

chunkhound research "How does UpdateCard + electron-updater flow work in ce-app frontend?"
```

---

## 5. What NOT to do

- ❌ Ship ChunkHound/SocratiCode/Sourcegraph as required runtime for gym check-in  
- ❌ Put AGPL indexer code inside MP installer  
- ❌ Use cloud agents with real member injury/national-id data  
- ❌ Treat OSS Compass or Open Aware as exercise/food databases  
- ❌ Skip free-exercise-db / JP7 golden tests because “the agent indexed something”

---

## 6. Phase 0 checklist (tooling)

- [ ] Engineering map v1.1 read  
- [ ] One of: ChunkHound **or** open-codebase-index installed and `index` run  
- [ ] Librarian setup (optional but recommended)  
- [ ] Agent bootstrap prompt from map §17 pasted  
- [ ] Confirm agent refuses to write under `ce-app/`  

---

## 7. Attribution

When documenting the **dev environment** (thesis appendix OK):
- ChunkHound — MIT — https://github.com/chunkhound/chunkhound  
- open-codebase-index — MIT — https://github.com/Helweg/open-codebase-index  
- Librarian packages — see their LICENSE files  
- SocratiCode — AGPL-3 — dev-only disclosure  
- Open Aware / Sourcegraph / Copilot / OSS Compass — per their terms  

Product About screen still lists **runtime** OSS only (map §12.1–12.4), not every dev tool.

---

**END DEV_AGENT_TOOLING**
