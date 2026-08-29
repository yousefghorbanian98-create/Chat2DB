import { describe, expect, it } from 'vitest';

import {
  emptyPaymentDraft,
  formatRial,
  parseRial,
  qrLooksComplete,
  validatePayment,
} from './opsValidation';

describe('formatRial', () => {
  it('groups thousands the way the receipt PDF does', () => {
    expect(formatRial(1234567)).toBe('1,234,567');
    expect(formatRial(0)).toBe('0');
    expect(formatRial(999)).toBe('999');
    expect(formatRial(1000)).toBe('1,000');
  });

  it('rounds and never emits decimals (Rial has none)', () => {
    expect(formatRial(1234.6)).toBe('1,235');
  });

  it('degrades gracefully on non-finite input', () => {
    expect(formatRial(Number.NaN)).toBe('—');
    expect(formatRial(Number.POSITIVE_INFINITY)).toBe('—');
  });
});

describe('parseRial', () => {
  it('accepts Persian digits and separators', () => {
    expect(parseRial('۱٬۲۳۴٬۵۶۷')).toBe(1234567);
    expect(parseRial('1,234,567')).toBe(1234567);
    expect(parseRial(' 2 500 000 ')).toBe(2500000);
  });

  it('rejects junk and empty input', () => {
    expect(parseRial('')).toBeNull();
    expect(parseRial('abc')).toBeNull();
    expect(parseRial('12.5')).toBeNull();
    expect(parseRial('-500')).toBeNull();
  });
});

describe('validatePayment', () => {
  it('requires a member and a positive amount', () => {
    const errors = validatePayment(emptyPaymentDraft);
    expect(errors.map((e) => e.field)).toEqual(['memberId', 'amountRial']);
  });

  it('passes for a complete draft', () => {
    expect(
      validatePayment({ ...emptyPaymentDraft, memberId: 3, amountRial: '500,000' }),
    ).toEqual([]);
  });

  it('rejects a zero amount', () => {
    const errors = validatePayment({
      ...emptyPaymentDraft,
      memberId: 3,
      amountRial: '0',
    });
    expect(errors).toHaveLength(1);
    expect(errors[0]?.field).toBe('amountRial');
  });
});

describe('qrLooksComplete', () => {
  it('needs the signed core fields', () => {
    expect(
      qrLooksComplete({ typ: 'member', gym: 1, mid: 7, exp: 9999999999, sig: 'abc' }),
    ).toBe(true);
    expect(qrLooksComplete({ gym: 1, mid: 7, exp: 1, sig: '' })).toBe(false);
    expect(qrLooksComplete({ mid: 7 })).toBe(false);
    expect(qrLooksComplete({})).toBe(false);
  });
});
