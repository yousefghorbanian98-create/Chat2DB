import { describe, expect, it } from 'vitest';

import {
  buttonVariants,
  cardVariants,
  durations,
  easings,
  errorShake,
  listVariants,
  modalContentVariants,
  pageVariants,
  respectReducedMotion,
  springs,
  stagger,
} from './presets';

describe('ANIMATION_SYSTEM springs', () => {
  it('matches the FINN-LOOP preset table exactly', () => {
    expect(springs.snappy).toEqual({ type: 'spring', stiffness: 500, damping: 30, mass: 1 });
    expect(springs.bouncy).toEqual({ type: 'spring', stiffness: 400, damping: 15, mass: 1 });
    expect(springs.instant).toEqual({ type: 'spring', stiffness: 700, damping: 35, mass: 0.5 });
  });

  it('every preset is a real spring (loop forbids linear/ease on transitions)', () => {
    for (const [name, preset] of Object.entries(springs)) {
      expect(preset.type, name).toBe('spring');
      expect(preset.damping, name).toBeGreaterThan(0);
      expect(preset.stiffness, name).toBeGreaterThan(0);
    }
  });
});

describe('easing curves', () => {
  it('are valid cubic-bezier strings', () => {
    for (const [name, curve] of Object.entries(easings)) {
      expect(curve, name).toMatch(/^cubic-bezier\([-0-9., ]+\)$/);
      const parts = curve.slice('cubic-bezier('.length, -1).split(',').map(Number);
      expect(parts).toHaveLength(4);
      expect(parts.every((n) => Number.isFinite(n)), name).toBe(true);
    }
  });
});

describe('duration scale', () => {
  it('is ordered from instant to cinematic (seconds, not ms)', () => {
    const values = Object.values(durations);
    expect(values).toEqual([...values].sort((a, b) => a - b));
    expect(durations.instant).toBeLessThan(0.1);
    expect(durations.cinematic).toBe(1.2);
  });
});

describe('MASTER.md vs FINN-LOOP conflict resolution', () => {
  it('dashboard cards translate only — no scale on dense surfaces', () => {
    const dashboard = cardVariants('dashboard');
    expect(dashboard.hover).not.toHaveProperty('scale');
    expect(dashboard.hover).toEqual({ y: -2 });
  });

  it('cinematic cards get the lift + scale', () => {
    expect(cardVariants('cinematic').hover).toEqual({ scale: 1.02, y: -4 });
  });

  it('dashboard page transition is the MASTER.md 200ms fade, not a slide', () => {
    const fade = pageVariants('dashboard');
    expect(fade.hidden).toEqual({ opacity: 0 });
    expect(pageVariants('cinematic').hidden).toHaveProperty('x', '5%');
  });

  it('launcher stagger stays inside MASTER.md 40–60ms', () => {
    expect(stagger.dashboardTiles).toBeGreaterThanOrEqual(0.04);
    expect(stagger.dashboardTiles).toBeLessThanOrEqual(0.06);
  });

  it('caps staggered items before requiring virtualisation', () => {
    expect(stagger.maxStaggeredItems).toBe(20);
  });
});

describe('list variants', () => {
  it('dashboard items travel 12px (MASTER.md), cinematic 20px', () => {
    expect(listVariants('dashboard').item.hidden).toEqual({ opacity: 0, y: 12 });
    expect(listVariants('cinematic').item.hidden).toEqual({ opacity: 0, y: 20 });
  });

  it('items use a spring transition, not a linear one', () => {
    const visible = listVariants().item.visible as { transition: { type: string } };
    expect(visible.transition.type).toBe('spring');
  });
});

describe('shared component variants', () => {
  it('button tap feedback is scale 0.95', () => {
    expect(buttonVariants.tap).toEqual({ scale: 0.95 });
    expect(buttonVariants.hover).toEqual({ scale: 1.03 });
  });

  it('modal content enters from below and exits faster than it enters', () => {
    expect(modalContentVariants.hidden).toMatchObject({ scale: 0.9, y: 40 });
    expect(modalContentVariants.exit).toMatchObject({ scale: 0.95, y: 20 });
  });

  it('error shake returns to origin so nothing is left displaced', () => {
    expect(errorShake.x[0]).toBe(0);
    expect(errorShake.x[errorShake.x.length - 1]).toBe(0);
  });
});

describe('reduced motion', () => {
  it('collapses any transition to zero duration', () => {
    expect(respectReducedMotion(springs.bouncy, true)).toEqual({ duration: 0 });
  });

  it('leaves the transition untouched when motion is allowed', () => {
    expect(respectReducedMotion(springs.bouncy, false)).toBe(springs.bouncy);
  });
});
