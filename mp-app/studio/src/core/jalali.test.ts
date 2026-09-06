import { describe, expect, it } from 'vitest';

import { faDate, faDigits, toJalali } from './jalali';

/**
 * Golden anchors cross-checked against an independent implementation
 * (`jdatetime`, Python) on 2026-08-30 — not derived from this module.
 */
interface Anchor {
  iso: string;
  jy: number;
  jm: number;
  jd: number;
}

const ANCHORS: Anchor[] = [
  { iso: '2026-08-30', jy: 1405, jm: 6, jd: 8 },
  { iso: '2026-03-21', jy: 1405, jm: 1, jd: 1 }, // Nowruz 1405
  { iso: '2025-03-20', jy: 1403, jm: 12, jd: 30 }, // last day of a leap Esfand
  { iso: '2001-03-21', jy: 1380, jm: 1, jd: 1 }, // Nowruz 1380
  { iso: '2024-03-19', jy: 1402, jm: 12, jd: 29 },
  { iso: '2000-01-01', jy: 1378, jm: 10, jd: 11 },
  { iso: '1999-12-31', jy: 1378, jm: 10, jd: 10 },
  { iso: '2026-12-31', jy: 1405, jm: 10, jd: 10 },
  { iso: '2030-07-04', jy: 1409, jm: 4, jd: 13 },
];

describe('jalali conversion', () => {
  it.each(ANCHORS)('$iso -> $jy/$jm/$jd', (a) => {
    expect(toJalali(a.iso)).toEqual({ jy: a.jy, jm: a.jm, jd: a.jd });
  });

  it('accepts a full ISO timestamp and ignores the time part', () => {
    expect(toJalali('2026-08-30T22:09:18.938Z')).toEqual({ jy: 1405, jm: 6, jd: 8 });
  });

  it('rejects anything that is not an ISO date instead of guessing', () => {
    expect(() => toJalali('not-a-date')).toThrow(/not an ISO date/);
  });

  it('renders a zero-padded Persian date', () => {
    expect(faDate('2026-08-30T00:00:00Z')).toBe('۱۴۰۵/۰۶/۰۸');
  });

  it('converts latin digits to persian ones', () => {
    expect(faDigits(1405)).toBe('۱۴۰۵');
    expect(faDigits('0')).toBe('۰');
  });
});
