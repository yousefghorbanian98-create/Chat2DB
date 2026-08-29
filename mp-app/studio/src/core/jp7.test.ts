/**
 * Frontend JP7 mirror must match the backend golden fixtures.
 * Values are the SAME literals as backend/tests/test_jp7.py — derived
 * independently with python decimal, never guessed.
 */
import { describe, expect, it } from 'vitest';

import { bodyDensity, bodyFatPercent, classify, computeJp7, SITES, type SitesMap } from './jp7';

function spread(total: number): SitesMap {
  const per = total / SITES.length;
  const out = {} as SitesMap;
  for (const s of SITES) out[s] = per;
  return out;
}

type Row = [string, number, number, number, number];
const GOLDEN: Row[] = [
  ['male', 25, 60, 1.080674, 8.0474],
  ['male', 25, 100, 1.066794, 14.0069],
  ['male', 35, 80, 1.070632, 12.3439],
  ['male', 45, 120, 1.05475, 19.3057],
  ['male', 55, 150, 1.043272, 24.4687],
  ['female', 25, 60, 1.067626, 13.6453],
  ['female', 25, 100, 1.052422, 20.3436],
  ['female', 35, 80, 1.058517, 17.6352],
  ['female', 45, 120, 1.042926, 24.6261],
  ['female', 55, 150, 1.032088, 29.6102],
];

describe('frontend jp7 mirrors backend', () => {
  it.each(GOLDEN)(
    '%s age %i sum %f -> BD %f BF %f',
    (sex, age, sum, bd, siri) => {
      const sites = spread(sum);
      expect(bodyDensity(sex as 'male' | 'female', sites, age)).toBeCloseTo(bd, 5);
      expect(bodyFatPercent(bodyDensity(sex as 'male' | 'female', sites, age))).toBeCloseTo(siri, 2);
    },
  );

  it('published anchor: male 35 sum107 -> BD 1.06166', () => {
    expect(bodyDensity('male', spread(107), 35)).toBeCloseTo(1.06166, 4);
  });

  it('derived FM/LBM sum back to weight', () => {
    const out = computeJp7({ sex: 'male', age: 25, sites: spread(60), weightKg: 80 });
    expect(out.sumMm).toBeCloseTo(60);
    expect((out.fatMassKg ?? 0) + (out.leanMassKg ?? 0)).toBeCloseTo(80, 5);
  });

  it('classification bands match the map', () => {
    expect(classify('male', 8)).toBe('athletic');
    expect(classify('male', 32)).toBe('obese');
    expect(classify('female', 16)).toBe('athletic');
    expect(classify('female', 40)).toBe('obese');
  });
});
