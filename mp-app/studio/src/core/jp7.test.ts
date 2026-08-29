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

/** One golden fixture row. An object (not a tuple) so the callback below
 *  stays within the <= 3-parameter contract. */
interface Golden {
  sex: 'male' | 'female';
  age: number;
  sum: number;
  bd: number;
  siri: number;
}

const GOLDEN: Golden[] = [
  { sex: 'male', age: 25, sum: 60, bd: 1.080674, siri: 8.0474 },
  { sex: 'male', age: 25, sum: 100, bd: 1.066794, siri: 14.0069 },
  { sex: 'male', age: 35, sum: 80, bd: 1.070632, siri: 12.3439 },
  { sex: 'male', age: 45, sum: 120, bd: 1.05475, siri: 19.3057 },
  { sex: 'male', age: 55, sum: 150, bd: 1.043272, siri: 24.4687 },
  { sex: 'female', age: 25, sum: 60, bd: 1.067626, siri: 13.6453 },
  { sex: 'female', age: 25, sum: 100, bd: 1.052422, siri: 20.3436 },
  { sex: 'female', age: 35, sum: 80, bd: 1.058517, siri: 17.6352 },
  { sex: 'female', age: 45, sum: 120, bd: 1.042926, siri: 24.6261 },
  { sex: 'female', age: 55, sum: 150, bd: 1.032088, siri: 29.6102 },
];

describe('frontend jp7 mirrors backend', () => {
  it.each(GOLDEN)('$sex age $age sum $sum -> BD $bd BF $siri', ({ sex, age, sum, bd, siri }) => {
    const sites = spread(sum);
    const density = bodyDensity(sex, sites, age);
    expect(density).toBeCloseTo(bd, 5);
    expect(bodyFatPercent(density)).toBeCloseTo(siri, 2);
  });

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
