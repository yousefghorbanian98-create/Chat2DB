# MASTER LOOP v2.0 — Execution Tracker (خطبهخط)

> Each line of the engineering map (see `PLAN_VERBATIM.md`) has an ID below.
> Status legend: ⬜ memorized/pending · 🔄 in progress · ✅ done & verified · ⚠️ blocked/needs decision
> Created: 2026-08-30 · **Nothing has been executed yet** — motions demo only (per user instruction).

## Prototype status (standalone demo — built 2026-08-30)

Per the user's instruction (“فعلا کلا هیچ چیز اجرا نکن … بعد عکسی از موشن‌ها نشونم بده،
موشن‌ها را بساز دقیق هر چند بی‌ربط به پروژه باشند”), the **motion components of
Sections B, C, D, E** were prototyped in a standalone demo:

- `master-loop-motions/` — Vite + React 18 + TS app mirroring the map's `src/` tree exactly
  (components/loading · landing · editor · style-match · hooks · providers · styles · utils).
- Every component file named in Section A exists with the map's behaviour:
  GSAP timeline 0.3→0.8→1.2→1.5→2.0→2.5→3.0s, GPU tier<1 + reduced-motion fallbacks,
  Icosahedron globe #0088ff, arcs by DB color, Stars 100/50/2000, autoRotate 0.5,
  WS mock fallback every 5s, Monaco typewriter 50ms + .ai-glow, spring 300/30,
  split 60/40, stagger 0.03, recharts animations, layoutId result-view, 500ms wave,
  600ms HSL morph, double helix + 6 nodes, score colors, react-colorful.
- Screenshots: `master-loop-motions/screenshots/` (17 PNGs + 4 animated GIFs).
- NOT yet done: integration into the real client, Sections F–R, scripts/, workflows/.

Integration into the real project = PENDING (tracker items below remain ⬜ until then).

## Reconciliation notes (to check BEFORE execution)
- Branch in the map: `arena/01a032fb-chat2db` — this session is fixed to `arena/01a05327-chat2db`. Reconcile at execution start.
- Map says integrate into `chat2db-client/src/` — this checkout has `chat2db-community-client/` (and `ce-app/frontend`). Confirm target client dir at execution start.
- Motions were prototyped in `master-loop-motions/` (standalone demo, per user: “هر چند بی‌ربط به پروژه باشند”). Integration into the real client = pending.


## SECTION A — PROJECT STRUCTURE

| ID | Item | Detail | Status |
|---|---|---|---|
| A-1 | components/loading/ | NEW: Loading Screen C — NeuralLoading.tsx · NeuralNodes.tsx · NeuralEdges.tsx · SignalPulse.tsx · CentralLogo.tsx · ProgressRing.tsx · StatusTypewriter.tsx | ⬜ |
| A-2 | components/landing/ | NEW: Landing Screen D — GlobeLanding.tsx · Globe3D.tsx · ConnectionArcs.tsx · PulseRing.tsx · StarField.tsx · QuickActionCards.tsx · LiveCounter.tsx · LiveIndicator.tsx · GlobeDataProvider.tsx | ⬜ |
| A-3 | components/editor/ | EXTEND: Editor Motions G+H — EditorWorkspace.tsx · SmartEditor.tsx · TypewriterReveal.ts · AIHighlight.ts · AIPanel.tsx · SuggestionCard.tsx · ResultPanel.tsx · ResultTable.tsx · ResultChart.tsx · ExecutionWave.tsx · ViewMorph.tsx | ⬜ |
| A-4 | components/style-match/ | NEW: Style Match I+J — StyleMatchWorkspace.tsx · ThemeGallery.tsx · ThemeCard.tsx · LivePreview.tsx · DNAHelix.tsx · HelixNode.tsx · MatchScore.tsx · useThemeMorph.ts | ⬜ |
| A-5 | hooks/ | NEW — useWebSocket.ts · useThemeMorph.ts · useAnimationFPS.ts · useReducedMotion.ts | ⬜ |
| A-6 | providers/ | NEW + EXTEND — GlobeDataProvider.tsx (NEW) · ThemeProvider.tsx (EXTEND) · AnimationProvider.tsx (NEW) | ⬜ |
| A-7 | styles/themes/ | NEW: CSS custom properties — dark.css · light.css · warm.css · variables.css | ⬜ |
| A-8 | styles/animations/ | NEW: keyframes — loading.css · landing.css · editor.css · style-match.css | ⬜ |
| A-9 | utils/ | NEW — hslInterpolation.ts · gpuDetect.ts · animationTimeline.ts | ⬜ |
| A-10 | scripts/ | NEW: Master loop tooling — loop-runner.sh · phase-gate.js · ai-review.sh · rebuild-dep-graph.sh · chaos-test.sh | ⬜ |
| A-11 | .github/workflows/ | NEW — master-loop.yml · full-loop.yml | ⬜ |
| A-12 | audit/ | NEW: Phase 0 outputs — inventory.json · dead-code.json · circular-deps.svg · complexity.json · baseline-perf.json | ⬜ |
| A-13 | root | NEW — stryker.conf.json · .semgrep.yml · .size-limit.json · ecosystem.config.js | ⬜ |
| A-14 | package.json | EXTEND — Add all new dependencies (Section P) | ⬜ |

## SECTION B — LOADING SCREEN C (NEURAL DATABASE 3D)

| ID | Item | Detail | Status |
|---|---|---|---|
| B-1 | Neural Nodes | R3F InstancedMesh (single draw call); sphere positions = DB nodes MySQL/Postgres/Mongo/Redis/SQLite; fixed orbital positions; emissive glow | ⬜ |
| B-2 | Neural Edges | Line-drawing between connected nodes → R3F <Line>/QuadraticBezierLine (drei) curved connections | ⬜ |
| B-3 | Signal Pulse | Particles constrained to travel along edge curves (sin/cos back-and-forth) | ⬜ |
| B-4 | Central Logo | drei Text3D or Html SVG overlay 'Chat2DB'; UnrealBloomPass glow; scale 0→1 elastic | ⬜ |
| B-5 | Progress Ring | SVG circle stroke-dashoffset bound to app init progress events | ⬜ |
| B-6 | GSAP Timeline | gsap.timeline() — nodes(0.3s) → edges(0.8s) → signals(1.2s) → logo(1.5s) → progress(2.0s) → burst(2.5s) → exit(3.0s) | ⬜ |
| B-7 | GPU Detection | detect-gpu tier 0-3; tier<1 → skip 3D, static SVG + progress bar | ⬜ |
| B-8 | Reduced Motion | useReducedMotion(); if true → skip 3D & GSAP, simple fade-in | ⬜ |
| B-9 | Integration | Hook into startup sequence (src/main/); replace splash; read DB connection list from store (only configured DBs); pull logo SVG from assets | ⬜ |

## SECTION C — LANDING SCREEN D (LIVE GLOBE 3D)

| ID | Item | Detail | Status |
|---|---|---|---|
| C-1 | Globe Geometry | IcosahedronGeometry(detail=3) + MeshBasicMaterial wireframe #0088ff; lat/lng mapping | ⬜ |
| C-2 | Alternative Globe / Arcs | QuadraticBezierCurve3 arcs; R3F QuadraticBezierLine; color by DB type (MySQL=blue, PG=green, Mongo=orange) | ⬜ |
| C-3 | Connection Arcs Animated | drei <Line> dashed + useFrame dashOffset flowing animation | ⬜ |
| C-4 | Pulse Rings | On WS event spawn ring at connection point: scale 1→3, opacity 1→0 over 1s, remove | ⬜ |
| C-5 | Star Field | drei <Stars> radius=100 depth=50 count=2000 | ⬜ |
| C-6 | Orbit Controls | autoRotate, autoRotateSpeed=0.5, enableZoom=false, enablePan=false | ⬜ |
| C-7 | HTML Labels | drei <Html> — 'MySQL: 3 active' labels at node positions | ⬜ |
| C-8 | WebSocket Provider | socket.io-client pattern; events: connection:added, query:executed, db:health; fallback mock data every 5s | ⬜ |
| C-9 | Animated Counters | react-countup bound to live query count | ⬜ |
| C-10 | Quick Action Cards | framer-motion staggerChildren 0.1; item y:20→0 opacity | ⬜ |
| C-11 | Integration | Read connection list from store; IP→lat/lng geoip (or random); WS endpoint (check application.yml); links to /query /dashboard /ai /connections | ⬜ |

## SECTION D — EDITOR MOTIONS G+H (SMART REVEAL + SPLIT MORPH)

| ID | Item | Detail | Status |
|---|---|---|---|
| D-1 | Monaco Base | Extend existing Monaco SQL setup (do NOT replace) | ⬜ |
| D-2 | Typewriter Reveal | editor.deltaDecorations() line-by-line reveal; 50ms interval; .revealed class opacity transition 0.3s | ⬜ |
| D-3 | AI Highlight | Inline decoration .ai-glow { box-shadow: 0 0 10px #00ff88; animation: pulse 2s } on AI-suggested lines | ⬜ |
| D-4 | AI Suggestion Panel | framer-motion spring stiffness:300 damping:30; slides up from bottom; AnimatePresence enter/exit | ⬜ |
| D-5 | Diff View | Monaco DiffEditor — Original=current SQL, Modified=AI-optimized; green/red inline | ⬜ |
| D-6 | Split View | react-resizable-panels PanelGroup; left=editor 60%, right=results 40%; drag animation on handle | ⬜ |
| D-7 | Result Table Stagger | Rows: initial {opacity:0,x:-10} → {opacity:1,x:0} delay index*0.03 | ⬜ |
| D-8 | Result Charts | recharts: Bar grow (begin 200, dur 800), Line strokeDasharray draw, Pie rotate startAngle→endAngle | ⬜ |
| D-9 | View Morph | motion.div layoutId='result-view' wraps Table & Chart; smooth morph on tab switch | ⬜ |
| D-10 | Execution Wave | On Run: SVG rect sweep left→right across editor, 500ms, gradient blue | ⬜ |
| D-11 | Integration | Extend pages/main/workspace Monaco; AI suggestions via src/service/ai.ts; extend existing ResultTable; wrap existing execute handler with wave | ⬜ |

## SECTION E — STYLE MATCH I+J (THEME MORPH + DNA HELIX)

| ID | Item | Detail | Status |
|---|---|---|---|
| E-1 | Theme System CSS vars | 30+ CSS vars (--bg-primary, --text-color…); switch via :root variables | ⬜ |
| E-2 | Alternative Theme | ColorModeProvider pattern with localStorage persistence; dark/light/warm | ⬜ |
| E-3 | HSL Interpolation | colord toHsl + manual lerp h/s/l; rAF t 0→1 over 600ms | ⬜ |
| E-4 | View Transitions API | document.startViewTransition(() => setTheme(new)); fallback CSS transition on custom properties | ⬜ |
| E-5 | Color Palette Generation | radix-ui/colors accessible scales as base presets | ⬜ |
| E-6 | DNA Helix | Three.js double helix: strand1=(cos t·R, t·H, sin t·R), strand2=(cos(t+π)·R, t·H, sin(t+π)·R); TubeGeometry; rungs CylinderGeometry | ⬜ |
| E-7 | Helix Nodes | 6 interactive spheres: Colors(red) Typography(blue) Spacing(green) Layout(yellow) Contrast(purple) Shadows(orange); hover scale 1→1.3 + tooltip; pulse glow 2s on style change | ⬜ |
| E-8 | Match Score | Circular progress 0-100%: red(<50) → yellow(50-80) → green(>80) → gold(>90) | ⬜ |
| E-9 | Color Picker | react-colorful HSL picker to customize individual theme colors | ⬜ |
| E-10 | Integration | Extend existing theme system/styles (Ant Design ConfigProvider tokens if used); DNA Helix standalone; Chat2DB dark theme = default preset | ⬜ |

## SECTION F — PHASE 0: BASELINE AUDIT TOOLS

| ID | Item | Detail | Status |
|---|---|---|---|
| F-1 | madge | INSTALL: npm i -D madge — USAGE: madge --circular --extensions ts,tsx src/ --image deps.svg | ⬜ |
| F-2 | depcheck | INSTALL: npm i -D depcheck — USAGE: depcheck --ignores="@types/*" | ⬜ |
| F-3 | ts-prune | INSTALL: npm i -D ts-prune — USAGE: ts-prune --error | ⬜ |
| F-4 | knip | INSTALL: npm i -D knip — USAGE: knip --include files,dependencies,unlisted | ⬜ |
| F-5 | complexity-report | INSTALL: npm i -D complexity-report — USAGE: complexity-report src/ --format json --output audit/complexity.json | ⬜ |

## SECTION G — PHASE 5: AUTO-DEBUG TOOLS

| ID | Item | Detail | Status |
|---|---|---|---|
| G-1 | Stryker mutation | INSTALL: npm i -D @stryker-mutator/core @stryker-mutator/typescript-checker — USAGE: stryker.conf.json; npx stryker run | ⬜ |
| G-2 | Sentry | INSTALL: npm i @sentry/react @sentry/tracing — USAGE: Sentry.init({ dsn, tracesSampleRate: 0.1 }) | ⬜ |
| G-3 | OpenAI code review | INSTALL: npm i openai — USAGE: Send changed files to GPT-4: God Class, Long Method, Feature Envy, Data Clumps | ⬜ |

## SECTION H — PHASE 6: SECURITY TOOLS

| ID | Item | Detail | Status |
|---|---|---|---|
| H-1 | Semgrep SAST | INSTALL: pip install semgrep — USAGE: semgrep scan --config auto src/ | ⬜ |
| H-2 | Snyk SCA | INSTALL: npm i -g snyk — USAGE: snyk test | ⬜ |
| H-3 | TruffleHog | INSTALL: brew install trufflehog — USAGE: trufflehog filesystem --no-update . | ⬜ |
| H-4 | Trivy | INSTALL: brew install trivy — USAGE: trivy image chat2db:latest | ⬜ |
| H-5 | ZAP DAST | INSTALL: owasp/zap2docker-stable — USAGE: zap-baseline.py -t http://localhost:3000 | ⬜ |
| H-6 | Electronegativity | INSTALL: npm i -g @doyensec/electronegativity — USAGE: electronegativity -i chat2db-client/ | ⬜ |

## SECTION I — PHASE 7: PERFORMANCE TOOLS

| ID | Item | Detail | Status |
|---|---|---|---|
| I-1 | Lighthouse CI | INSTALL: npm i -D @lhci/cli — USAGE: .lighthouserc.json; lhci autorun | ⬜ |
| I-2 | Bundle Analyzer | INSTALL: npm i -D webpack-bundle-analyzer — USAGE: add to webpack plugins | ⬜ |
| I-3 | Size Limit | INSTALL: npm i -D size-limit @size-limit/preset-app — USAGE: .size-limit.json; npx size-limit | ⬜ |
| I-4 | Memory Leak | INSTALL: npm i -D puppeteer — USAGE: heap snapshot before/after 100x open/close | ⬜ |

## SECTION J — PHASE 8-9: TESTING + VISUAL TOOLS

| ID | Item | Detail | Status |
|---|---|---|---|
| J-1 | Playwright E2E | INSTALL: npm i -D playwright @playwright/test — USAGE: npx playwright test | ⬜ |
| J-2 | Percy visual | INSTALL: npm i -D @percy/cli @percy/playwright — USAGE: percy exec -- npx playwright test | ⬜ |
| J-3 | Pixelmatch | INSTALL: npm i -D pixelmatch pngjs — USAGE: pixelmatch(img1,img2,diff,w,h,{threshold:0.1}) | ⬜ |
| J-4 | Axe a11y | INSTALL: npm i -D @axe-core/playwright — USAGE: new AxeBuilder({page}).analyze() | ⬜ |

## SECTION K — PHASE 12: SELF-HEALING TOOLS

| ID | Item | Detail | Status |
|---|---|---|---|
| K-1 | PM2 | INSTALL: npm i -g pm2 — USAGE: ecosystem.config.js; pm2 start ecosystem.config.js | ⬜ |
| K-2 | Renovate | INSTALL: GitHub App (free) or self-hosted — USAGE: renovate.json; auto PRs for dependency updates | ⬜ |
| K-3 | Chaos test | INSTALL: custom scripts/chaos-test.sh — USAGE: kill -9 node.chat2db → verify PM2 restart; tc netem 500ms delay → timeout; stress --vm 90% → graceful degradation | ⬜ |

## SECTION L — PHASE 13: ADVANCED FEATURES TOOLS

| ID | Item | Detail | Status |
|---|---|---|---|
| L-1 | Pact contract tests | INSTALL: npm i -D @pact-foundation/pact — USAGE: provider/consumer verification | ⬜ |
| L-2 | Unleash feature flags | INSTALL: Docker unleashorg/unleash-server; npm i unleash-client — USAGE: unleash.isEnabled('new-editor-motion') | ⬜ |
| L-3 | i18next | INSTALL: npm i i18next react-i18next i18next-browser-languagedetector — USAGE: i18n.t('editor.run') | ⬜ |
| L-4 | RTL CSS | INSTALL: npm i -D rtlcss postcss-rtlcss — USAGE: add to PostCSS config | ⬜ |
| L-5 | Conventional changelog | INSTALL: npm i -D conventional-changelog-cli — USAGE: conventional-changelog -p angular -i CHANGELOG.md -s | ⬜ |

## SECTION M — PHASE 14: PUBLISH TOOLS

| ID | Item | Detail | Status |
|---|---|---|---|
| M-1 | Electron Builder | INSTALL: npm i -D electron-builder — USAGE: electron-builder.yml; electron-builder --win --mac --linux | ⬜ |
| M-2 | Auto Updater | INSTALL: npm i electron-updater — USAGE: autoUpdater.checkForUpdatesAndNotify() | ⬜ |
| M-3 | Semantic Release | INSTALL: npm i -D semantic-release — USAGE: .releaserc.json; npx semantic-release | ⬜ |

## SECTION N — ANIMATION LIBRARIES (SHARED)

| ID | Item | Detail | Status |
|---|---|---|---|
| N-1 | Framer Motion | INSTALL: npm i framer-motion — USAGE: UI transitions, stagger, spring, layoutId, AnimatePresence | ⬜ |
| N-2 | GSAP | INSTALL: npm i gsap @gsap/react — USAGE: loading timeline, complex sequenced animations | ⬜ |
| N-3 | React Three Fiber | INSTALL: npm i @react-three/fiber @react-three/drei three — USAGE: loading neural net, landing globe, DNA helix | ⬜ |
| N-4 | Three.js | INSTALL: npm i three @types/three — USAGE: geometry, materials, lights, post-processing | ⬜ |

## SECTION O — LOOP ORCHESTRATION

| ID | Item | Detail | Status |
|---|---|---|---|
| O-1 | scripts/loop-runner.sh | PHASES=(0..14); per phase: node scripts/phase-gate.js --phase N; on fail retry max 3 (sleep retry*10); ALERT after 3 fails | ⬜ |
| O-2 | .github/workflows/master-loop.yml | Trigger: push, pull_request, schedule (0 2 * * *); matrix [ubuntu,macos,windows]; steps: checkout→setup node→cache→install→run loop-runner.sh→upload artifacts | ⬜ |
| O-3 | .github/workflows/full-loop.yml | Trigger: schedule (0 3 * * 0); ALL phases incl. chaos testing + visual regression | ⬜ |

## SECTION P — DEPENDENCY INSTALLATION (RUN ONCE)

| ID | Item | Detail | Status |
|---|---|---|---|
| P-1 | Runtime deps | @react-three/fiber @react-three/drei three framer-motion gsap @gsap/react socket.io-client colord react-countup recharts react-resizable-panels react-colorful @sentry/react @sentry/tracing i18next react-i18next i18next-browser-languagedetector electron-updater unleash-client openai | ⬜ |
| P-2 | Dev deps | @types/three @stryker-mutator/core @stryker-mutator/typescript-checker @lhci/cli madge depcheck ts-prune knip complexity-report size-limit @size-limit/preset-app @axe-core/playwright pixelmatch pngjs playwright @percy/cli @percy/playwright @pact-foundation/pact rtlcss postcss-rtlcss conventional-changelog-cli semantic-release electron-builder webpack-bundle-analyzer puppeteer @playwright/test react-monaco-editor | ⬜ |

## SECTION Q — EXECUTION SCHEDULE

| ID | Item | Detail | Status |
|---|---|---|---|
| Q-1 | Every Commit | Phase 0, 5, 6, 8 (fast checks, ~3 min) | ⬜ |
| Q-2 | Every PR | Phase 0-10 (full checks, ~15 min) | ⬜ |
| Q-3 | Every Night | Phase 0-14 (complete loop, ~45 min) | ⬜ |
| Q-4 | Every Week | Phase 12 Chaos + 13 Full Audit (~2 hours) | ⬜ |
| Q-5 | Every 4 Hours | Phase 0.5 Dependency Graph Rebuild (cron) | ⬜ |
| Q-6 | Every 30s | Phase 12.6 WebSocket Heartbeat (runtime) | ⬜ |

## SECTION R — NEXT STEPS FOR AI DEVELOPER

| ID | Item | Detail | Status |
|---|---|---|---|
| R-1 | Clone | git clone https://github.com/yousefghorbanian98-create/Chat2DB.git; git checkout arena/01a032fb-chat2db | ⬜ |
| R-2 | Map structure | tree chat2db-client/src/ -L 3 | ⬜ |
| R-3 | Install deps | Section P | ⬜ |
| R-4 | Phase 0 first | audit before changing anything (Section F) | ⬜ |
| R-5 | Build motions in order | Loading → Landing → Editor → Style Match (B → C → D → E) | ⬜ |
| R-6 | Integrate tools phase by phase | Sections F → M | ⬜ |
| R-7 | Setup CI/CD | Section O | ⬜ |
| R-8 | Run full loop and iterate |  | ⬜ |

## IMPORTANT RULES

| ID | Item | Detail | Status |
|---|---|---|---|
| RULE-1 | Backup | NEVER delete existing working code without backup | ⬜ |
| RULE-2 | Check first | ALWAYS check Chat2DB's existing implementation before adding new | ⬜ |
| RULE-3 | Reference not copy | USE open-source sources as REFERENCE, not copy-paste | ⬜ |
| RULE-4 | Adapt | ADAPT all code to fit Chat2DB's existing architecture and patterns | ⬜ |
| RULE-5 | Test each phase | TEST each phase before moving to the next | ⬜ |
| RULE-6 | Bundle size | KEEP bundle size under 500KB initial load | ⬜ |
| RULE-7 | 60fps | MAINTAIN 60fps for all animations | ⬜ |
| RULE-8 | A11y | SUPPORT prefers-reduced-motion for accessibility | ⬜ |

---
**Total tracked items: 119 · Done: 0 · Pending: 119**