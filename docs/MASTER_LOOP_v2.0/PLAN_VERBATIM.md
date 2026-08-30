# MASTER LOOP v2.0 — Chat2DB — PLAN (VERBATIM COPY)

> This file is the **verbatim, line-by-line copy** of the engineering map the user
> sent on 2026-08-30. Nothing was edited, summarized or reordered. It is the
> single source of truth; `TRACKER.md` next to it is the execution checklist.
> Status: **MEMORIZED — nothing executed yet** (per user instruction).

---

```
================================================================================
COMPLETE ARCHITECTURE MAP + OPEN-SOURCE SOURCING GUIDE
MASTER LOOP v2.0 — Chat2DB
FOR AI DEVELOPER: BUILD INSTRUCTIONS
================================================================================

INSTRUCTION TO AI DEVELOPER:
You are building the Chat2DB Master Loop v2.0. For every component below,
I have specified EXACTLY which open-source repository to pull code from,
which directory/file to reference, and how to adapt it. The primary codebase
is the user's own fork:
  PRIMARY: https://github.com/yousefghorbanian98-create/Chat2DB
  BRANCH:  https://github.com/yousefghorbanian98-create/Chat2DB/tree/arena/01a032fb-chat2db
All new code must integrate into the existing chat2db-client/src/ structure.
Do NOT rewrite existing working code — extend and wrap it.

================================================================================
SECTION A: PROJECT STRUCTURE (WHERE EVERYTHING GOES)
================================================================================

chat2db-client/
├── src/
│   ├── components/
│   │   ├── loading/                    ← NEW: Loading Screen C
│   │   │   ├── NeuralLoading.tsx
│   │   │   ├── NeuralNodes.tsx
│   │   │   ├── NeuralEdges.tsx
│   │   │   ├── SignalPulse.tsx
│   │   │   ├── CentralLogo.tsx
│   │   │   ├── ProgressRing.tsx
│   │   │   └── StatusTypewriter.tsx
│   │   ├── landing/                    ← NEW: Landing Screen D
│   │   │   ├── GlobeLanding.tsx
│   │   │   ├── Globe3D.tsx
│   │   │   ├── ConnectionArcs.tsx
│   │   │   ├── PulseRing.tsx
│   │   │   ├── StarField.tsx
│   │   │   ├── QuickActionCards.tsx
│   │   │   ├── LiveCounter.tsx
│   │   │   ├── LiveIndicator.tsx
│   │   │   └── GlobeDataProvider.tsx
│   │   ├── editor/                     ← EXTEND: Editor Motions G+H
│   │   │   ├── EditorWorkspace.tsx
│   │   │   ├── SmartEditor.tsx
│   │   │   ├── TypewriterReveal.ts
│   │   │   ├── AIHighlight.ts
│   │   │   ├── AIPanel.tsx
│   │   │   ├── SuggestionCard.tsx
│   │   │   ├── ResultPanel.tsx
│   │   │   ├── ResultTable.tsx
│   │   │   ├── ResultChart.tsx
│   │   │   ├── ExecutionWave.tsx
│   │   │   └── ViewMorph.tsx
│   │   └── style-match/                ← NEW: Style Match I+J
│   │       ├── StyleMatchWorkspace.tsx
│   │       ├── ThemeGallery.tsx
│   │       ├── ThemeCard.tsx
│   │       ├── LivePreview.tsx
│   │       ├── DNAHelix.tsx
│   │       ├── HelixNode.tsx
│   │       ├── MatchScore.tsx
│   │       └── useThemeMorph.ts
│   ├── hooks/
│   │   ├── useWebSocket.ts             ← NEW
│   │   ├── useThemeMorph.ts            ← NEW
│   │   ├── useAnimationFPS.ts          ← NEW
│   │   └── useReducedMotion.ts         ← NEW
│   ├── providers/
│   │   ├── GlobeDataProvider.tsx        ← NEW
│   │   ├── ThemeProvider.tsx            ← EXTEND existing
│   │   └── AnimationProvider.tsx        ← NEW
│   ├── styles/
│   │   ├── themes/                     ← NEW: CSS custom properties
│   │   │   ├── dark.css
│   │   │   ├── light.css
│   │   │   ├── warm.css
│   │   │   └── variables.css
│   │   └── animations/                 ← NEW: keyframes
│   │       ├── loading.css
│   │       ├── landing.css
│   │       ├── editor.css
│   │       └── style-match.css
│   └── utils/
│       ├── hslInterpolation.ts          ← NEW
│       ├── gpuDetect.ts                 ← NEW
│       └── animationTimeline.ts         ← NEW
├── scripts/
│   ├── loop-runner.sh                   ← NEW: Master loop orchestrator
│   ├── phase-gate.js                    ← NEW
│   ├── ai-review.sh                     ← NEW
│   ├── rebuild-dep-graph.sh             ← NEW
│   └── chaos-test.sh                    ← NEW
├── .github/
│   └── workflows/
│       ├── master-loop.yml              ← NEW
│       └── full-loop.yml                ← NEW
├── audit/                               ← NEW: Phase 0 outputs
│   ├── inventory.json
│   ├── dead-code.json
│   ├── circular-deps.svg
│   ├── complexity.json
│   └── baseline-perf.json
├── stryker.conf.json                    ← NEW
├── .semgrep.yml                         ← NEW
├── .size-limit.json                     ← NEW
├── ecosystem.config.js                  ← NEW: PM2
└── package.json                         ← EXTEND with new deps


================================================================================
SECTION B: LOADING SCREEN C — NEURAL DATABASE (3D)
================================================================================

COMPONENT: src/components/loading/NeuralLoading.tsx
WHAT IT DOES: 3D neural network of database nodes with signal pulses,
              central logo reveal, and progress ring during app startup.

OPEN-SOURCE SOURCES (copy and adapt from these):

  1. R3F Canvas Setup + Neural Nodes:
     SOURCE: https://github.com/pmndrs/react-three-fiber
     FILE: packages/examples/src/demos/InstancedMesh.tsx
     WHAT TO TAKE: InstancedMesh pattern for rendering multiple nodes
                   in a single draw call. Adapt sphere positions to
                   represent DB nodes (MySQL, Postgres, Mongo, Redis, SQLite).
     ADAPTATION: Replace random positions with fixed orbital positions.
                 Add emissive material for glow effect.

  2. Neural Edges (Lines Between Nodes):
     SOURCE: https://github.com/vasturiano/react-force-graph
     FILE: src/forcegraph3d.tsx (line rendering logic)
     WHAT TO TAKE: The line-drawing logic between connected nodes.
     ADAPTATION: Convert to R3F <Line> from @react-three/drei.
                 Use QuadraticBezierLine for curved connections.

  3. Signal Pulse (Particle on Edge):
     SOURCE: https://github.com/pmndrs/drei
     FILE: src/core/Sparkles.tsx
     WHAT TO TAKE: Particle animation along a path using useFrame.
     ADAPTATION: Constrain particles to travel along edge curves.
                 Use sin/cos for smooth back-and-forth motion.

  4. Central Logo (3D Text/Plane):
     SOURCE: https://github.com/pmndrs/drei
     FILE: src/core/Text3D.tsx or src/core/Html.tsx
     WHAT TO TAKE: Text3D for "Chat2DB" logo or Html for SVG overlay.
     ADAPTATION: Add glow post-processing (UnrealBloomPass).
                 Scale animation: 0 → 1 with elastic easing.

  5. Progress Ring (SVG):
     SOURCE: https://github.com/framer/motion
     FILE: packages/framer-motion/src/components/AnimatePresence/
     WHAT TO TAKE: SVG circle stroke-dashoffset animation pattern.
     ADAPTATION: Bind to app initialization progress events.

  6. GSAP Timeline Orchestration:
     SOURCE: https://github.com/greensock/GSAP
     FILE: packages/gsap/src/gsap-core.js (timeline API)
     REFERENCE: https://gsap.com/docs/v3/GSAP/Timeline/
     WHAT TO TAKE: gsap.timeline() chaining pattern.
     ADAPTATION: Sequence: nodes(0.3s) → edges(0.8s) → signals(1.2s)
                 → logo(1.5s) → progress(2.0s) → burst(2.5s) → exit(3.0s)

  7. GPU Detection (Fallback):
     SOURCE: https://github.com/pmndrs/detect-gpu
     FILE: src/index.ts
     WHAT TO TAKE: GPU tier detection (0-3).
     ADAPTATION: If tier < 1, skip 3D → show static SVG + progress bar.

  8. Reduced Motion:
     SOURCE: https://github.com/framer/motion
     FILE: packages/framer-motion/src/motion/utils/use-reduced-motion.ts
     WHAT TO TAKE: useReducedMotion() hook.
     ADAPTATION: If true, skip all 3D and GSAP, show simple fade-in.

CHAT2DB-SPECIFIC INTEGRATION:
  - Hook into existing app startup sequence in chat2db-client/src/main/
  - Replace current splash screen (if any) with NeuralLoading
  - Read DB connection list from existing store to determine which
    nodes to show (only show nodes for DBs user has configured)
  - Pull logo SVG from existing assets in chat2db-client/src/assets/


================================================================================
SECTION C: LANDING SCREEN D — LIVE GLOBE (3D)
================================================================================

COMPONENT: src/components/landing/GlobeLanding.tsx
WHAT IT DOES: Interactive 3D wireframe globe showing live database
              connections as arcs, with real-time WebSocket data.

OPEN-SOURCE SOURCES:

  1. Globe Geometry (Wireframe Sphere):
     SOURCE: https://github.com/dataarts/webgl-globe (Google Data Arts)
     FILE: globe/globe.js
     WHAT TO TAKE: IcosahedronGeometry wireframe pattern with lat/lng mapping.
     ADAPTATION: Convert to R3F. Use IcosahedronGeometry(detail=3)
                 with MeshBasicMaterial({ wireframe: true, color: '#0088ff' }).

  2. Alternative Globe (simpler):
     SOURCE: https://github.com/vasturiano/globe.gl
     FILE: src/globe.js
     WHAT TO TAKE: Arc rendering logic (QuadraticBezierCurve3 between points).
     ADAPTATION: Convert arcs to R3F <QuadraticBezierLine> from drei.
                 Color arcs by DB type (MySQL=blue, PG=green, Mongo=orange).

  3. Connection Arcs (Animated):
     SOURCE: https://github.com/vasturiano/react-globe.gl
     FILE: src/arcs-layer.js
     WHAT TO TAKE: Arc animation (dash offset moving along curve).
     ADAPTATION: Use drei <Line> with dashed prop + useFrame for animation.
                 Animate dashOffset in useFrame for flowing effect.

  4. Pulse Rings (on new connection):
     SOURCE: https://github.com/pmndrs/drei
     FILE: src/core/Ring.tsx + examples
     WHAT TO TAKE: Expanding ring animation pattern.
     ADAPTATION: On WebSocket event, spawn ring at connection point.
                 Scale 1→3, opacity 1→0 over 1s, then remove.

  5. Star Field Background:
     SOURCE: https://github.com/pmndrs/drei
     FILE: src/core/Stars.tsx
     WHAT TO TAKE: Stars component (1000 points, random positions).
     ADAPTATION: Use as-is. Set radius=100, depth=50, count=2000.

  6. Orbit Controls (Auto-Rotate):
     SOURCE: https://github.com/pmndrs/drei
     FILE: src/core/OrbitControls.tsx
     WHAT TO TAKE: OrbitControls with autoRotate prop.
     ADAPTATION: autoRotateSpeed=0.5, enableZoom=false, enablePan=false.

  7. HTML Labels on Globe:
     SOURCE: https://github.com/pmndrs/drei
     FILE: src/core/Html.tsx
     WHAT TO TAKE: Html component for overlaying DOM on 3D positions.
     ADAPTATION: Show "MySQL: 3 active" labels at node positions.

  8. WebSocket Provider:
     SOURCE: https://github.com/socketio/socket.io-client
     FILE: lib/index.ts
     WHAT TO TAKE: io() connection + event listener pattern.
     ADAPTATION: Connect to Chat2DB backend WS endpoint.
                 Events: connection:added, query:executed, db:health.
                 Fallback: generate mock data every 5s if WS unavailable.

  9. Animated Counters:
     SOURCE: https://github.com/glennreyes/react-countup
     FILE: src/CountUp.tsx
     WHAT TO TAKE: CountUp component with duration and easing.
     ADAPTATION: Bind to live query count from WebSocket.

  10. Quick Action Cards (Stagger):
      SOURCE: https://github.com/framer/motion
      FILE: packages/framer-motion/src/components/AnimatePresence/
      WHAT TO TAKE: staggerChildren variant pattern.
      ADAPTATION: container: { hidden: {}, show: { transition: { staggerChildren: 0.1 } } }
                  item: { hidden: { y: 20, opacity: 0 }, show: { y: 0, opacity: 1 } }

CHAT2DB-SPECIFIC INTEGRATION:
  - Read connection list from existing chat2db-client store
    (look for connectionStore or similar in src/store/)
  - Map each connection to a point on globe (use DB server IP → lat/lng
    via free geoip API, or assign random positions)
  - WebSocket endpoint: check existing WS setup in Chat2DB backend
    (likely ws://localhost:10824 or similar — check application.yml)
  - Quick actions link to existing routes: /query, /dashboard, /ai, /connections


================================================================================
SECTION D: EDITOR MOTIONS G+H — SMART REVEAL + SPLIT MORPH
================================================================================

COMPONENT: src/components/editor/EditorWorkspace.tsx
WHAT IT DOES: Enhanced SQL editor with typewriter reveal, AI highlight,
              split view with animated results, and view morphing.

OPEN-SOURCE SOURCES:

  1. Monaco Editor (Base):
     SOURCE: https://github.com/microsoft/monaco-editor
     FILE: src/vs/editor/ (entire editor core)
     REACT WRAPPER: https://github.com/react-monaco-editor/react-monaco-editor
     FILE: src/index.tsx
     WHAT TO TAKE: Monaco editor setup with SQL language support.
     ADAPTATION: Chat2DB already uses Monaco — EXTEND existing setup.
                 Add custom decorations for AI highlights and typewriter.

  2. Typewriter Reveal (Monaco Decorations):
     SOURCE: https://github.com/microsoft/monaco-editor
     FILE: src/vs/editor/common/model/textModel.ts (deltaDecorations API)
     WHAT TO TAKE: editor.deltaDecorations() for line-by-line reveal.
     ADAPTATION: On first load, hide all lines (opacity 0 via CSS class).
                 Use setInterval to reveal lines one by one (50ms each).
                 Add CSS class .revealed { opacity: 1; transition: opacity 0.3s }

  3. AI Highlight (Glow Decoration):
     SOURCE: https://github.com/microsoft/monaco-editor
     FILE: src/vs/editor/contrib/inlineCompletions/ (inline suggestions)
     WHAT TO TAKE: Inline decoration pattern with custom CSS class.
     ADAPTATION: Add .ai-glow { box-shadow: 0 0 10px #00ff88; animation: pulse 2s }
                 Apply to lines where AI has suggestions.

  4. AI Suggestion Panel (Spring Animation):
     SOURCE: https://github.com/framer/motion
     FILE: packages/framer-motion/src/animation/hooks/use-spring.ts
     WHAT TO TAKE: type: "spring", stiffness: 300, damping: 30
     ADAPTATION: Panel slides up from bottom of editor.
                 AnimatePresence for enter/exit.

  5. Diff View (Green/Red):
     SOURCE: https://github.com/microsoft/monaco-editor
     FILE: src/vs/editor/standalone/browser/quickAccess/ (diff editor)
     REACT: https://github.com/react-monaco-editor/react-monaco-editor (DiffEditor)
     WHAT TO TAKE: Monaco DiffEditor for showing AI-suggested changes.
     ADAPTATION: Original = current SQL, Modified = AI-optimized SQL.
                 Inline diff with green/red highlighting.

  6. Split View (Resizable Panels):
     SOURCE: https://github.com/bvaughn/react-resizable-panels
     FILE: packages/react-resizable-panels/src/PanelGroup.tsx
     WHAT TO TAKE: PanelGroup + Panel + PanelResizeHandle.
     ADAPTATION: Left = editor (default 60%), Right = results (40%).
                 Add drag animation on resize handle.

  7. Result Table (Stagger Rows):
     SOURCE: https://github.com/framer/motion
     FILE: packages/framer-motion/src/components/MotionConfig/
     WHAT TO TAKE: AnimatePresence + staggerChildren for list items.
     ADAPTATION: Each row: initial={{ opacity: 0, x: -10 }}
                 animate={{ opacity: 1, x: 0 }}
                 transition={{ delay: index * 0.03 }}

  8. Result Charts (Grow Animation):
     SOURCE: https://github.com/recharts/recharts
     FILE: src/cartesian/Bar.tsx, src/polar/Pie.tsx
     WHAT TO TAKE: Bar chart with animation (isAnimationActive=true).
     ADAPTATION: Bar: grow from baseline (animationBegin=200, duration=800).
                 Line: draw path (strokeDasharray animation).
                 Pie: rotate in (startAngle → endAngle animation).

  9. View Morph (Table ↔ Chart):
     SOURCE: https://github.com/framer/motion
     FILE: packages/framer-motion/src/components/LayoutGroup/
     WHAT TO TAKE: layoutId prop for shared layout animations.
     ADAPTATION: <motion.div layoutId="result-view"> wraps both
                 Table and Chart. On tab switch, Framer Motion morphs
                 the container smoothly.

  10. Execution Wave (SVG Sweep):
      SOURCE: https://github.com/framer/motion
      FILE: packages/framer-motion/src/value/use-motion-value.ts
      WHAT TO TAKE: SVG path animation with useMotionValue.
      ADAPTATION: On Run click, animate SVG rect from left to right
                  across editor width. Duration: 500ms, fill: gradient blue.

CHAT2DB-SPECIFIC INTEGRATION:
  - Chat2DB already has Monaco editor in chat2db-client/src/pages/main/
    workspace/ — EXTEND this, don't replace.
  - Hook AI suggestions into existing AI chat API
    (check src/service/ai.ts or similar)
  - Result rendering: extend existing result table component
    (check src/components/ResultTable/ or similar)
  - Run button: find existing execute query handler and wrap with
    wave animation trigger


================================================================================
SECTION E: STYLE MATCH I+J — THEME MORPH + DNA HELIX
================================================================================

COMPONENT: src/components/style-match/StyleMatchWorkspace.tsx
WHAT IT DOES: Theme switching with smooth HSL morphing, live preview,
              3D DNA helix visualization of style properties.

OPEN-SOURCE SOURCES:

  1. Theme System (CSS Custom Properties):
     SOURCE: https://github.com/system-ui/theme-ui
     FILE: packages/theme-ui/src/color-modes.tsx
     WHAT TO TAKE: Theme provider with CSS custom properties switching.
     ADAPTATION: Define 30+ CSS vars (--bg-primary, --text-color, etc.)
                 Switch themes by changing :root variables.

  2. Alternative Theme System:
     SOURCE: https://github.com/chakra-ui/chakra-ui
     FILE: packages/components/color-mode/src/color-mode-provider.tsx
     WHAT TO TAKE: ColorModeProvider pattern with localStorage persistence.
     ADAPTATION: Use for dark/light/warm mode switching.

  3. HSL Color Interpolation:
     SOURCE: https://github.com/omgovich/colord
     FILE: src/plugins/lch.ts (or hsl.ts)
     WHAT TO TAKE: colord(color).toHsl() + manual lerp between HSL values.
     ADAPTATION: function lerpHSL(from, to, t) {
                   h: lerp(from.h, to.h, t),
                   s: lerp(from.s, to.s, t),
                   l: lerp(from.l, to.l, t)
                 }
                 Use requestAnimationFrame to animate t from 0→1 over 600ms.

  4. View Transitions API:
     SOURCE: https://github.com/nicolo-ribaudo/view-transitions-polyfill
     FILE: src/index.ts
     WHAT TO TAKE: document.startViewTransition() polyfill.
     ADAPTATION: Wrap theme switch in startViewTransition(() => setTheme(new)).
                 Fallback: CSS transition on all custom properties.

  5. Color Palette Generation:
     SOURCE: https://github.com/radix-ui/colors
     FILE: src/ (all color scales)
     WHAT TO TAKE: Pre-built accessible color scales (blue, green, red, etc.)
     ADAPTATION: Use as base palettes for theme presets.

  6. DNA Helix (3D Double Helix):
     SOURCE: https://github.com/mrdoob/three.js
     FILE: examples/webgl_geometry_shapes.html (parametric geometry)
     REFERENCE: https://threejs.org/examples/#webgl_geometry_shapes
     WHAT TO TAKE: ParametricCurve geometry for helix path.
     ADAPTATION: Create double helix:
       strand1(t) = { x: cos(t)*R, y: t*H, z: sin(t)*R }
       strand2(t) = { x: cos(t+π)*R, y: t*H, z: sin(t+π)*R }
       Use TubeGeometry along each curve.
       Rungs: CylinderGeometry between strand1(t) and strand2(t).

  7. Helix Nodes (Interactive Spheres):
     SOURCE: https://github.com/pmndrs/drei
     FILE: src/core/MeshDistortMaterial.tsx (for organic feel)
     WHAT TO TAKE: Interactive sphere with hover scale + tooltip.
     ADAPTATION: 6 nodes at helix intersections:
       Colors(red), Typography(blue), Spacing(green),
       Layout(yellow), Contrast(purple), Shadows(orange).
       On hover: scale 1→1.3, show tooltip with property details.
       On style change: pulse glow for 2s.

  8. Circular Progress (Match Score):
     SOURCE: https://github.com/kevinsqi/react-circular-progressbar
     FILE: src/CircularProgressbar.tsx
     WHAT TO TAKE: SVG circle with animated stroke-dashoffset.
     ADAPTATION: Bind to match score (0-100%).
                 Color: red(<50) → yellow(50-80) → green(>80) → gold(>90).

  9. Color Picker (Custom Theme):
     SOURCE: https://github.com/omgovich/react-colorful
     FILE: src/components/HslColorPicker.tsx
     WHAT TO TAKE: Lightweight HSL color picker.
     ADAPTATION: Allow user to customize individual theme colors.

CHAT2DB-SPECIFIC INTEGRATION:
  - Check existing theme system in chat2db-client/src/styles/ or
    src/theme/ — extend it, don't replace.
  - If Chat2DB uses Ant Design, extend its ConfigProvider theme token system.
  - DNA Helix is a NEW standalone component — no conflicts.
  - Theme presets should include Chat2DB's existing dark theme as default.


================================================================================
SECTION F: PHASE 0 — BASELINE AUDIT TOOLS
================================================================================

  1. Dependency Graph:
     SOURCE: https://github.com/pahen/madge
     FILE: src/index.js
     INSTALL: npm i -D madge
     USAGE: madge --circular --extensions ts,tsx src/ --image deps.svg

  2. Unused Dependencies:
     SOURCE: https://github.com/depcheck/depcheck
     FILE: src/index.js
     INSTALL: npm i -D depcheck
     USAGE: depcheck --ignores="@types/*"

  3. Dead Exports:
     SOURCE: https://github.com/nadeesha/ts-prune
     FILE: src/index.ts
     INSTALL: npm i -D ts-prune
     USAGE: ts-prune --error

  4. Comprehensive Dead Code:
     SOURCE: https://github.com/webpro/knip
     FILE: packages/knip/src/
     INSTALL: npm i -D knip
     USAGE: knip --include files,dependencies,unlisted

  5. Complexity Report:
     SOURCE: https://github.com/philbooth/complexity-report
     FILE: src/index.js
     INSTALL: npm i -D complexity-report
     USAGE: complexity-report src/ --format json --output audit/complexity.json


================================================================================
SECTION G: PHASE 5 — AUTO-DEBUG TOOLS
================================================================================

  1. Mutation Testing:
     SOURCE: https://github.com/stryker-mutator/stryker-js
     FILE: packages/core/src/
     INSTALL: npm i -D @stryker-mutator/core @stryker-mutator/typescript-checker
     CONFIG: stryker.conf.json
     USAGE: npx stryker run

  2. Error Tracking:
     SOURCE: https://github.com/getsentry/sentry-javascript
     FILE: packages/react/src/
     INSTALL: npm i @sentry/react @sentry/tracing
     USAGE: Sentry.init({ dsn, tracesSampleRate: 0.1 })

  3. AI Code Review:
     SOURCE: https://github.com/openai/openai-node
     FILE: src/index.ts
     INSTALL: npm i openai
     USAGE: Send changed files to GPT-4 API with prompt:
            "Review for: God Class, Long Method, Feature Envy, Data Clumps"


================================================================================
SECTION H: PHASE 6 — SECURITY TOOLS
================================================================================

  1. SAST:
     SOURCE: https://github.com/semgrep/semgrep
     FILE: cli/src/
     INSTALL: pip install semgrep (or Docker)
     USAGE: semgrep scan --config auto src/

  2. SCA:
     SOURCE: https://github.com/snyk/snyk
     FILE: src/cli/
     INSTALL: npm i -g snyk
     USAGE: snyk test

  3. Secret Detection:
     SOURCE: https://github.com/trufflesecurity/trufflehog
     FILE: main.go
     INSTALL: brew install trufflehog (or Docker)
     USAGE: trufflehog filesystem --no-update .

  4. Container Scan:
     SOURCE: https://github.com/aquasecurity/trivy
     FILE: pkg/
     INSTALL: brew install trivy
     USAGE: trivy image chat2db:latest

  5. DAST:
     SOURCE: https://github.com/zaproxy/zaproxy
     FILE: docker/
     INSTALL: Docker: owasp/zap2docker-stable
     USAGE: zap-baseline.py -t http://localhost:3000

  6. Electron Security:
     SOURCE: https://github.com/doyensec/electronegativity
     FILE: src/
     INSTALL: npm i -g @doyensec/electronegativity
     USAGE: electronegativity -i chat2db-client/


================================================================================
SECTION I: PHASE 7 — PERFORMANCE TOOLS
================================================================================

  1. Lighthouse CI:
     SOURCE: https://github.com/GoogleChrome/lighthouse-ci
     FILE: packages/cli/src/
     INSTALL: npm i -D @lhci/cli
     CONFIG: .lighthouserc.json
     USAGE: lhci autorun

  2. Bundle Analyzer:
     SOURCE: https://github.com/webpack-contrib/webpack-bundle-analyzer
     FILE: src/
     INSTALL: npm i -D webpack-bundle-analyzer
     USAGE: Add to webpack config plugins

  3. Size Limit:
     SOURCE: https://github.com/ai/size-limit
     FILE: packages/size-limit/
     INSTALL: npm i -D size-limit @size-limit/preset-app
     CONFIG: .size-limit.json
     USAGE: npx size-limit

  4. Memory Leak Detection:
     SOURCE: https://github.com/nicolo-ribaudo/chrome-devtools-protocol
     REFERENCE: https://pptr.dev/ (Puppeteer)
     INSTALL: npm i -D puppeteer
     USAGE: puppeteer heap snapshot before/after 100x open/close


================================================================================
SECTION J: PHASE 8-9 — TESTING + VISUAL TOOLS
================================================================================

  1. E2E Testing (Buttons):
     SOURCE: https://github.com/microsoft/playwright
     FILE: packages/playwright/src/
     INSTALL: npm i -D playwright @playwright/test
     USAGE: npx playwright test

  2. Visual Regression:
     SOURCE: https://github.com/percy/cli
     FILE: packages/cli/src/
     INSTALL: npm i -D @percy/cli @percy/playwright
     USAGE: percy exec -- npx playwright test

  3. Pixel Diff:
     SOURCE: https://github.com/mapbox/pixelmatch
     FILE: index.js
     INSTALL: npm i -D pixelmatch pngjs
     USAGE: pixelmatch(img1, img2, diff, width, height, { threshold: 0.1 })

  4. A11y Testing:
     SOURCE: https://github.com/dequelabs/axe-core
     FILE: axe.js
     INSTALL: npm i -D @axe-core/playwright
     USAGE: new AxeBuilder({ page }).analyze()


================================================================================
SECTION K: PHASE 12 — SELF-HEALING TOOLS
================================================================================

  1. Process Manager:
     SOURCE: https://github.com/Unitech/pm2
     FILE: lib/
     INSTALL: npm i -g pm2
     CONFIG: ecosystem.config.js
     USAGE: pm2 start ecosystem.config.js

  2. Dependency Auto-Update:
     SOURCE: https://github.com/renovatebot/renovate
     FILE: lib/
     INSTALL: GitHub App (free) or self-hosted
     CONFIG: renovate.json
     USAGE: Auto-creates PRs for dependency updates

  3. Chaos Engineering:
     SOURCE: https://github.com/Netflix/chaos-monkey (concept)
     LIGHTWEIGHT: https://github.com/bloomberg/powerfulseal
     ADAPTATION: Write custom scripts/chaos-test.sh:
       - kill -9 $(pgrep -f "node.*chat2db") → verify PM2 restart
       - tc qdisc add dev lo root netem delay 500ms → verify timeout
       - stress --vm 1 --vm-bytes 90% → verify graceful degradation


================================================================================
SECTION L: PHASE 13 — ADVANCED FEATURES TOOLS
================================================================================

  1. Contract Tests:
     SOURCE: https://github.com/pact-foundation/pact-js
     FILE: src/
     INSTALL: npm i -D @pact-foundation/pact
     USAGE: Pact provider/consumer verification

  2. Feature Flags:
     SOURCE: https://github.com/Unleash/unleash
     FILE: src/
     INSTALL: Docker: unleashorg/unleash-server
     SDK: npm i unleash-client
     USAGE: unleash.isEnabled('new-editor-motion')

  3. i18n:
     SOURCE: https://github.com/i18next/i18next
     FILE: src/
     INSTALL: npm i i18next react-i18next i18next-browser-languagedetector
     USAGE: i18n.t('editor.run')

  4. RTL Support:
     SOURCE: https://github.com/MohammadYounes/rtlcss
     FILE: lib/
     INSTALL: npm i -D rtlcss postcss-rtlcss
     USAGE: Add to PostCSS config

  5. Changelog:
     SOURCE: https://github.com/conventional-changelog/conventional-changelog
     FILE: packages/conventional-changelog-cli/
     INSTALL: npm i -D conventional-changelog-cli
     USAGE: conventional-changelog -p angular -i CHANGELOG.md -s


================================================================================
SECTION M: PHASE 14 — PUBLISH TOOLS
================================================================================

  1. Electron Builder:
     SOURCE: https://github.com/electron-userland/electron-builder
     FILE: packages/electron-builder/
     INSTALL: npm i -D electron-builder
     CONFIG: electron-builder.yml
     USAGE: electron-builder --win --mac --linux

  2. Auto Updater:
     SOURCE: https://github.com/electron-userland/electron-builder
     FILE: packages/electron-updater/
     INSTALL: npm i electron-updater
     USAGE: autoUpdater.checkForUpdatesAndNotify()

  3. Semantic Release:
     SOURCE: https://github.com/semantic-release/semantic-release
     FILE: src/
     INSTALL: npm i -D semantic-release
     CONFIG: .releaserc.json
     USAGE: npx semantic-release


================================================================================
SECTION N: ANIMATION LIBRARIES (SHARED ACROSS ALL MOTIONS)
================================================================================

  1. Framer Motion (Primary):
     SOURCE: https://github.com/framer/motion
     FILE: packages/framer-motion/src/
     INSTALL: npm i framer-motion
     USE FOR: All UI transitions, stagger, spring, layoutId, AnimatePresence

  2. GSAP (Timeline Orchestration):
     SOURCE: https://github.com/greensock/GSAP
     FILE: packages/gsap/src/
     INSTALL: npm i gsap @gsap/react
     USE FOR: Loading screen timeline, complex sequenced animations

  3. React Three Fiber (3D):
     SOURCE: https://github.com/pmndrs/react-three-fiber
     FILE: packages/fiber/src/
     INSTALL: npm i @react-three/fiber @react-three/drei three
     USE FOR: Loading neural network, landing globe, DNA helix

  4. Three.js (3D Core):
     SOURCE: https://github.com/mrdoob/three.js
     FILE: src/
     INSTALL: npm i three @types/three
     USE FOR: All 3D geometry, materials, lights, post-processing


================================================================================
SECTION O: LOOP ORCHESTRATION SCRIPT
================================================================================

FILE: scripts/loop-runner.sh
WHAT IT DOES: Runs all 15 phases sequentially with gates and retries.

STRUCTURE (pseudo-code):
  #!/bin/bash
  PHASES=(0 1 2 3 4 5 6 7 8 9 10 11 12 13 14)
  for phase in "${PHASES[@]}"; do
    echo "=== PHASE $phase ==="
    node scripts/phase-gate.js --phase $phase
    if [ $? -ne 0 ]; then
      echo "Phase $phase FAILED. Retrying (max 3)..."
      for retry in 1 2 3; do
        sleep $((retry * 10))
        node scripts/phase-gate.js --phase $phase --retry $retry
        [ $? -eq 0 ] && break
      done
      [ $? -ne 0 ] && echo "ALERT: Phase $phase failed after 3 retries"
    fi
  done

FILE: .github/workflows/master-loop.yml
TRIGGER: push, pull_request, schedule (0 2 * * *)
MATRIX: [ubuntu-latest, macos-latest, windows-latest]
STEPS: checkout → setup node → cache → install → run loop-runner.sh → upload artifacts

FILE: .github/workflows/full-loop.yml
TRIGGER: schedule (0 3 * * 0)
STEPS: ALL phases including chaos testing and visual regression


================================================================================
SECTION P: DEPENDENCY INSTALLATION COMMAND (RUN ONCE)
================================================================================

npm i @react-three/fiber @react-three/drei three framer-motion gsap @gsap/react \
  socket.io-client colord react-countup recharts react-resizable-panels \
  react-colorful @sentry/react @sentry/tracing i18next react-i18next \
  i18next-browser-languagedetector electron-updater unleash-client openai

npm i -D @types/three @stryker-mutator/core @stryker-mutator/typescript-checker \
  @lhci/cli madge depcheck ts-prune knip complexity-report size-limit \
  @size-limit/preset-app @axe-core/playwright pixelmatch pngjs playwright \
  @percy/cli @percy/playwright @pact-foundation/pact rtlcss postcss-rtlcss \
  conventional-changelog-cli semantic-release electron-builder \
  webpack-bundle-analyzer puppeteer @playwright/test react-monaco-editor


================================================================================
SECTION Q: EXECUTION SCHEDULE
================================================================================

Every Commit:  Phase 0, 5, 6, 8 (fast checks, ~3 min)
Every PR:      Phase 0-10 (full checks, ~15 min)
Every Night:   Phase 0-14 (complete loop, ~45 min)
Every Week:    Phase 12 Chaos + 13 Full Audit (~2 hours)
Every 4 Hours: Phase 0.5 Dependency Graph Rebuild (cron)
Every 30s:     Phase 12.6 WebSocket Heartbeat (runtime)


================================================================================
SECTION R: NEXT STEPS FOR AI DEVELOPER
================================================================================

1. Clone the repo:
   git clone https://github.com/yousefghorbanian98-create/Chat2DB.git
   git checkout arena/01a032fb-chat2db

2. Map existing structure:
   tree chat2db-client/src/ -L 3

3. Install all dependencies (Section P)

4. Start with Phase 0 (Section F) — audit before changing anything

5. Build motions in order: Loading → Landing → Editor → Style Match
   (Sections B → C → D → E)

6. Integrate tools phase by phase (Sections F → M)

7. Setup CI/CD (Section O)

8. Run full loop and iterate

IMPORTANT RULES:
- NEVER delete existing working code without backup
- ALWAYS check Chat2DB's existing implementation before adding new
- USE the open-source sources listed above as REFERENCE, not copy-paste
- ADAPT all code to fit Chat2DB's existing architecture and patterns
- TEST each phase before moving to the next
- KEEP bundle size under 500KB initial load
- MAINTAIN 60fps for all animations
- SUPPORT prefers-reduced-motion for accessibility

================================================================================
END OF COMPLETE ARCHITECTURE MAP + SOURCING GUIDE
================================================================================
```
