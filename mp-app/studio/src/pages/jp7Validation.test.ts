import { describe, expect, it } from 'vitest';

import {
  canCalculate,
  draftToPayload,
  emptyDraft,
  validateDraft,
  validateSite,
  SITE_ORDER,
} from './jp7Validation';

function validDraft() {
  const d = emptyDraft();
  d.weightKg = '62.5';
  d.ageYears = '30';
  for (const site of SITE_ORDER) d.sites[site] = '15';
  return d;
}

describe('validateSite', () => {
  it('accepts a plausible caliper reading', () => {
    expect(validateSite('chest', '15')).toBeNull();
    expect(validateSite('chest', '1.5')).toBeNull();
    expect(validateSite('chest', '80')).toBeNull();
  });

  it('rejects empty, zero, negative, non-numeric, and >80mm', () => {
    expect(validateSite('chest', '')).not.toBeNull();
    expect(validateSite('chest', '0')).not.toBeNull();
    expect(validateSite('chest', '-3')).not.toBeNull();
    expect(validateSite('chest', 'abc')).not.toBeNull();
    expect(validateSite('chest', '81')).not.toBeNull();
  });
});

describe('canCalculate', () => {
  it('is true only when every field is valid', () => {
    expect(canCalculate(validDraft())).toBe(true);
  });

  it('blocks when a single site is empty', () => {
    const d = validDraft();
    d.sites.thigh = '';
    expect(canCalculate(d)).toBe(false);
  });

  it('blocks when weight or age is missing', () => {
    const d = validDraft();
    d.weightKg = '';
    expect(canCalculate(d)).toBe(false);

    const d2 = validDraft();
    d2.ageYears = '9'; // below the 10 floor
    expect(canCalculate(d2)).toBe(false);
  });

  it('reports one error per bad field, and no more', () => {
    const d = emptyDraft(); // everything empty
    const errors = validateDraft(d);
    // 7 sites + weight + age = 9
    expect(errors).toHaveLength(9);
  });
});

describe('draftToPayload', () => {
  it('converts strings to numbers with the backend field names', () => {
    const payload = draftToPayload(validDraft());
    expect(payload.weight_kg).toBe(62.5);
    expect(payload.age_years).toBe(30);
    expect(payload.sites_mm.chest).toBe(15);
    expect(Object.keys(payload.sites_mm)).toHaveLength(7);
  });
});
