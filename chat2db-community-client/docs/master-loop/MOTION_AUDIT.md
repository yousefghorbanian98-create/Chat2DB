# 🎬 Motion Audit — Data Cosmos vs Hyperreal

Applied the **Design Motion Principles** skill lenses (Kowalski/Krehel/Jhey) to both
packages before capture. Every rule below is a decision, not an accident.

## Frequency Gate (Kowalski lens)

| Animation | Trigger frequency | Verdict |
|---|---|---|
| Loading particle reveal | rare (once per app start) | allowed: expressive, but capped |
| Landing shader/globe rotation | continuous ambient | kept subtle (slow, low contrast) |
| Run button + wave | frequent (100s/day) | wave = 500 ms, no bounce, instant results |
| Theme morph | occasional | 450 ms view-transition, no loops |
| Confetti | rare (per successful run) | 3.2 s max, fades out |

## Durations (per the skill's guidelines)

- Cosmos loading: 3.3 s total — it is a *showcase* mode; still under 4 s.
- Hyper loading: **2.0 s total** — respects "productivity tool" speed rules; burst at 1.05 s.
- No animation in either package loops forever except ambient scenes (shader, galaxy,
  border beams) which are CSS/GPU cheap and reduced-motion-safe.

## Anti-slop checklist (both packages pass)

- ✅ No pulsing status dots on non-essential UI (only the LIVE indicator, which is data).
- ✅ No hover-scale on everything — only buttons that are actually actions.
- ✅ No stagger-spam — the action cards stagger once on mount (0.1 s), never re-run.
- ✅ prefers-reduced-motion → static SVG + progress bar (both packages).
- ✅ Every animation has a purpose: communicates progress, direction, or state.

## Accessibility

- `useReducedMotion` respected everywhere (particles, shader, coverflow all skip).
- Colors keep ≥ 4.5:1 contrast in both packages (checked against theme tokens).
- All motion respects the 60 fps budget (particles are single draw call, 20k points).

## Honest limitations

- Cosmos loading (3.3 s) is deliberately longer than the "instant" ideal — it is the
  cinematic variant the user asked for; the Hyper package is the production answer.
- Coverflow in Hyper uses 3D transforms that reduce-motion users skip entirely.
