/**
 * Client-side mirror of the backend JP7 math, used **only** for the live
 * preview in the assessment form. The backend remains the source of truth on
 * save (rule C6: the server recomputes; the client never persists a number).
 *
 * This file is unit-tested against the same 12 golden fixtures as
 * `backend/tests/test_jp7.py`, so the preview cannot silently diverge.
 */

export type Sex = 'male' | 'female';
export type Equation = 'siri' | 'brozek';

export const SITES = [
  'chest',
  'midaxillary',
  'triceps',
  'subscapular',
  'abdominal',
  'suprailiac',
  'thigh',
] as const;

export type SitesKey = (typeof SITES)[number];
/** A full 7-site map; indexing by a SITES key is always defined. */
export type SitesMap = Record<SitesKey, number>;

export interface Jp7Output {
  sumMm: number;
  bodyDensity: number;
  bodyFatPct: number;
  fatMassKg: number | null;
  leanMassKg: number | null;
  classification: string;
}

export function bodyDensity(sex: Sex, sites: SitesMap, age: number): number {
  const total = SITES.reduce((acc, s) => acc + sites[s], 0);
  if (sex === 'male') {
    return 1.112 - 0.00043499 * total + 0.00000055 * total * total - 0.00028826 * age;
  }
  return 1.097 - 0.00046971 * total + 0.00000056 * total * total - 0.00012828 * age;
}

export function bodyFatPercent(density: number, equation: Equation = 'siri'): number {
  if (density <= 0) throw new Error('body density must be > 0');
  return equation === 'siri'
    ? (4.95 / density - 4.5) * 100
    : (4.57 / density - 4.142) * 100;
}

const BANDS: Record<Sex, Array<[number, string]>> = {
  male: [
    [6, 'essential'],
    [14, 'athletic'],
    [18, 'fit'],
    [25, 'average'],
    [32, 'overfat'],
  ],
  female: [
    [14, 'essential'],
    [21, 'athletic'],
    [25, 'fit'],
    [32, 'average'],
    [40, 'overfat'],
  ],
};

export function classify(sex: Sex, pct: number): string {
  for (const [threshold, label] of BANDS[sex]) {
    if (pct < threshold) return label;
  }
  return 'obese';
}

export function computeJp7(opts: {
  sex: Sex;
  age: number;
  sites: SitesMap;
  weightKg?: number;
  equation?: Equation;
}): Jp7Output {
  const density = bodyDensity(opts.sex, opts.sites, opts.age);
  const pct = bodyFatPercent(density, opts.equation ?? 'siri');
  const fm = opts.weightKg ? (opts.weightKg * pct) / 100 : null;
  return {
    sumMm: SITES.reduce((a, s) => a + opts.sites[s], 0),
    bodyDensity: Number(density.toFixed(6)),
    bodyFatPct: Number(pct.toFixed(4)),
    fatMassKg: fm === null ? null : Number(fm.toFixed(4)),
    leanMassKg: opts.weightKg != null && fm !== null ? Number((opts.weightKg - fm).toFixed(4)) : null,
    classification: classify(opts.sex, pct),
  };
}
