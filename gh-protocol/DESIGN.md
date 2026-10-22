# Gh Protocol — Design System (v0.1, P0 baseline)

Status: baseline for P1. Refined in P3 (motion/onboarding) under the golden
screenshot gate (G1, Roborazzi, 12 pages × 2 themes).

## 1. Principles

1. **RTL-first, Persian-first.** UI is authored RTL; LTR is the fallback.
   Brand name ("Gh Protocol") is never translated.
2. **Honesty is a design language.** Network state (connected / degraded /
   cut-off) is always visible, in plain words, with the exact implications.
   No fake progress, no "connecting…" theater during a full cutoff.
3. **One tap.** The primary action (Connect) is one thumb-reach, ≥48dp, always
   reachable without scrolling.
4. **Calm urgency.** Restricted-network users are stressed. Palette is
   low-saturation blue on ink; motion is short (≤300ms) and `reducedMotion`
   safe.
5. **Zero chrome.** No onboarding walls, no accounts, no analytics, no ads.

## 2. Color (Material 3)

| Role | Light | Dark | Notes |
|---|---|---|---|
| primary | `#2E6BFF` (GhBlue) | `#8FB0FF` | connect action, links |
| onPrimary | `#FFFFFF` | `#0B1220` | |
| secondary | `#0B1220` | `#2E6BFF` | |
| background | `#F7F9FE` | `#0B1220` (GhInk) | |
| surface | `#F7F9FE` | `#111A2E` | cards, sheets |
| onSurface | `#0B1220` | `#E8EDF7` | |
| onSurfaceVariant | `#46536E` | `#9AA7C0` | secondary text |
| outline | `#C9D3E6` | `#2A3A5C` | dividers, borders |
| error | `#BA1A1A` / `#FFB4AB` (M3 defaults) | | |

Status semantics (F-11): connected = primary; degraded = `#F5A524` amber;
cut-off = `#E5484D` red — with WCAG AA contrast on both themes.

## 3. Type

- **Family:** Vazirmatn (OFL-1.1, rastikerdar/vazirmatn): Regular/Medium/Bold.
- Scale (sp): displaySmall 34/Bold · headlineMedium 26/Bold · titleMedium 18/Medium
  · bodyLarge 16 · bodyMedium 14 · labelSmall 12.
- Digits: Persian (۰–۹) in fa locale; line-height 1.4 for body.

## 4. Shape & space

- 4dp grid. Card radius 16dp; button radius 12dp; FAB/full-bleed 28dp.
- Screen padding 24dp; component gap 12dp; section gap 24dp.

## 5. Iconography

- Material Symbols (Apache-2.0), 24dp grid, weight 400 regular / 500 active.
- Launcher: adaptive icon, ink background + 3-bar signal mark (blue ramp).

## 6. Motion

- Standard: `fastOutSlowIn`, 220ms; enter/exit 280ms; `≤300ms` cap (P3).
- Lottie (Apache-2.0) only for the success loader (P3), LottieFiles free assets.
- Always respect `LocalConfiguration` reduced-motion.

## 7. Accessibility

- WCAG AA contrast minimum; tap targets ≥48dp; full TalkBack labels in fa/en;
  status changes announced via `LiveRegion` (importantForAccessibility).

## 8. Screens (G1 golden set, 12)

1. Home (connected) 2. Home (degraded) 3. Home (cut-off) 4. First-run
5. Settings 6. Config source 7. Clean-IP scanner 8. Balancer/routes
9. Blackout-prep 10. Guide (alternatives) 11. About/security 12. QR/share
