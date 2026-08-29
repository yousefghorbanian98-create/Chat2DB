# MP DESIGN_SYSTEM.md — how the loop's motion rules bind to MP's own spec

Single source of truth for visuals is
`docs/MuscleParadise/design-system/muscle-paradise/MASTER.md`.
Single source of truth for motion in code is `studio/src/motion/presets.ts`.
This file records the **decisions** where FINN-LOOP v3.0 and MASTER.md disagree.

## 1. The motion conflict, and how it was resolved

| | FINN-LOOP v3.0 | MASTER.md (MP product spec) |
|---|---|---|
| Motion dial | cinematic, award-winning | **4/10 — toned for a dense dashboard** |
| Cards | hover `scale 1.02, y -4` | "Do NOT scale cards in data-dense tables" |
| Page transition | shared-axis slide + blur | 200ms fade |
| Stagger | 40ms, `y: 20` | tiles 40–60ms, **y: 12**, no `back.out` on tables |
| Easing | spring only, "NO linear/ease" | gsap `power2.out` in its launcher example |

**Resolution — a typed two-mode system instead of picking a side:**

```ts
cardVariants('dashboard') // -> { hover: { y: -2 } }        no scale
cardVariants('cinematic') // -> { hover: { scale: 1.02, y: -4 } }
pageVariants('dashboard') // -> { hidden: { opacity: 0 } }   MASTER.md fade
pageVariants('cinematic') // -> { hidden: { opacity: 0, x: '5%', scale: 0.98 } }
```

Rule for future work: **dense data surfaces (tables, forms, JP7 inputs) use
`dashboard`. Celebrations, modals, the launcher hero use `cinematic`.**
This is asserted in `presets.test.ts`, so a future edit that scales a table row
fails a test instead of shipping.

## 2. Spring/easing/duration tables

All FINN-LOOP spring presets are encoded verbatim (`snappy 500/30/1`,
`smooth 300/30/1`, `bouncy 400/15/1`, `gentle 150/25/1`, `instant 700/35/0.5`,
`heavy 200/40/2`) and unit-tested against the table, so a typo is caught.

Durations are stored in **seconds** (Framer Motion convention) even though
FINN-LOOP lists them in ms — `durations.normal === 0.2`, not `200`.

## 3. Colour and type

Never hardcode. `studio/src/styles/tokens.css` mirrors MASTER.md 1:1
(`--color-primary: #00b86a`, gold `#FFD700`, bg `#0B0F14`, glass
`rgba(18,28,36,0.72)`, Barlow Condensed / Barlow / Vazirmatn). New hex values must
be added to MASTER.md first, then to tokens.css.

Persian-first: `<html lang="fa" dir="rtl">`; numeric fields (JP7 mm, rials) get
`class="numeric"` which forces `direction: ltr` + `tabular-nums`.

## 4. Accessibility floor (non-negotiable)

- `prefers-reduced-motion: reduce` → CSS collapses transitions **and**
  `useReducedMotion()` disables springs in components.
- Touch targets ≥ 44px (MASTER.md) — enforced in `MotionButton` (`minHeight: 44`).
- No emoji-as-icon (MASTER.md anti-pattern). Lucide only, from Phase 1.
- Every loading state is a labelled skeleton (`role="status"` + `aria-label`),
  never a blank block.
- Contrast ≥ 4.5:1 on glass — still to be verified with a real contrast pass.

## 5. What is deliberately NOT built yet

Command palette (Cmd+K), celebration/confetti, gesture system, ambient gradients,
premium chart choreography. They are queued behind Phase 1–2 per the map's
ordering ("no rework"): a celebration system on top of a schema that still
changes is wasted work.
