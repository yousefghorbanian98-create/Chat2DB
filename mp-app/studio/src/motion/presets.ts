/**
 * FINN-LOOP v3.0 ANIMATION_SYSTEM, encoded as typed presets.
 *
 * CONFLICT RESOLUTION (important):
 * MASTER.md sets MP's motion dial to **4/10 — toned for a dense dashboard**
 * ("no back.out on dense tables", tiles stagger 40–60ms, 200ms page fades),
 * while FINN-LOOP asks for cinematic motion everywhere. Both are honoured via
 * `mode`:
 *   - `dashboard` (default): the MASTER.md contract — data surfaces stay calm.
 *   - `cinematic`: the FINN-LOOP contract — celebrations, modals, launcher.
 * Never use `cinematic` on table rows or dense forms.
 */

import type { Transition, Variants } from 'framer-motion';

export type MotionMode = 'dashboard' | 'cinematic';

/** Spring presets (FINN-LOOP springs block). */
export const springs = {
  snappy: { type: 'spring', stiffness: 500, damping: 30, mass: 1 },
  smooth: { type: 'spring', stiffness: 300, damping: 30, mass: 1 },
  bouncy: { type: 'spring', stiffness: 400, damping: 15, mass: 1 },
  gentle: { type: 'spring', stiffness: 150, damping: 25, mass: 1 },
  instant: { type: 'spring', stiffness: 700, damping: 35, mass: 0.5 },
  heavy: { type: 'spring', stiffness: 200, damping: 40, mass: 2 },
} as const satisfies Record<string, Transition>;

export type SpringName = keyof typeof springs;

/** Non-spring easing curves (FINN-LOOP easings block). */
export const easings = {
  appleEase: 'cubic-bezier(0.25, 0.1, 0.25, 1.0)',
  easeOutExpo: 'cubic-bezier(0.16, 1, 0.3, 1)',
  easeInOutQuart: 'cubic-bezier(0.76, 0, 0.24, 1)',
  easeOutBack: 'cubic-bezier(0.34, 1.56, 0.64, 1)',
  easeOutCirc: 'cubic-bezier(0, 0.55, 0.45, 1)',
  smoothDecel: 'cubic-bezier(0, 0.7, 0.1, 1)',
  dramatic: 'cubic-bezier(0.87, 0, 0.13, 1)',
} as const;

/** Duration scale in **seconds** (Framer Motion uses seconds, CSS uses ms). */
export const durations = {
  instant: 0.05,
  fast: 0.1,
  normal: 0.2,
  medium: 0.3,
  slow: 0.5,
  dramatic: 0.8,
  cinematic: 1.2,
} as const;

/** MASTER.md density rules: how far apart staggered items appear. */
export const stagger = {
  dashboardTiles: 0.05, // MASTER.md: 40–60ms on launcher tiles
  listItems: 0.04, // FINN-LOOP stagger_fade_up
  menuItems: 0.03, // FINN-LOOP dropdown cascade
  maxStaggeredItems: 20, // beyond this, virtualise instead (perf watchdog)
} as const;

/** Button press feedback — FINN-LOOP: every button must feel pressable. */
export const buttonVariants: Variants = {
  rest: { scale: 1 },
  hover: { scale: 1.03 },
  tap: { scale: 0.95 },
};

/** Card hover elevation. Cinematic mode gets the lift; dashboard stays flat. */
export function cardVariants(mode: MotionMode = 'dashboard'): Variants {
  if (mode === 'cinematic') {
    return {
      rest: { scale: 1, y: 0 },
      hover: { scale: 1.02, y: -4 },
      tap: { scale: 0.98, y: 0 },
    };
  }
  // MASTER.md: "Do NOT scale cards in data-dense tables" -> translate only.
  return {
    rest: { y: 0 },
    hover: { y: -2 },
    tap: { y: 0 },
  };
}

/** Modal: blurred backdrop + spring content (FINN-LOOP modal block). */
export const modalOverlayVariants: Variants = {
  hidden: { opacity: 0 },
  visible: { opacity: 1 },
  exit: { opacity: 0 },
};

export const modalContentVariants: Variants = {
  hidden: { opacity: 0, scale: 0.9, y: 40 },
  visible: { opacity: 1, scale: 1, y: 0 },
  exit: { opacity: 0, scale: 0.95, y: 20 },
};

/** Page transition: MASTER.md 200ms fade for dashboard, shared-axis for hero. */
export function pageVariants(mode: MotionMode = 'dashboard'): Variants {
  if (mode === 'cinematic') {
    return {
      hidden: { opacity: 0, x: '5%', scale: 0.98 },
      visible: { opacity: 1, x: '0%', scale: 1 },
      exit: { opacity: 0, x: '-5%', scale: 0.98 },
    };
  }
  return {
    hidden: { opacity: 0 },
    visible: { opacity: 1 },
    exit: { opacity: 0 },
  };
}

/** Staggered list container/item pair. */
export function listVariants(mode: MotionMode = 'dashboard') {
  const amount = mode === 'cinematic' ? stagger.listItems : stagger.dashboardTiles;
  const y = mode === 'cinematic' ? 20 : 12; // MASTER.md: tiles y:12
  const container: Variants = {
    hidden: {},
    visible: { transition: { staggerChildren: amount, delayChildren: 0.1 } },
  };
  const item: Variants = {
    hidden: { opacity: 0, y },
    visible: {
      opacity: 1,
      y: 0,
      transition: springs.smooth,
    },
  };
  return { container, item } as const;
}

/** Error shake (FINN-LOOP: every error must shake the relevant element). */
export const errorShake: Transition & { x: number[] } = {
  x: [0, -8, 8, -6, 6, -3, 3, 0],
  duration: durations.slow,
};

/**
 * Reduced-motion-safe wrapper: swaps any transition for an instant one.
 * Use as `<motion.div transition={respectReducedMotion(t)} />`.
 */
export function respectReducedMotion(transition: Transition, reduced: boolean): Transition {
  if (!reduced) return transition;
  return { duration: 0 };
}
