/**
 * Pure helpers for the Operations console (Phase 2).
 *
 * Kept free of React so the money maths and validation are unit-testable —
 * the loop forbids vibes-based numbers, so Rial formatting is asserted.
 */

export interface PaymentDraft {
  memberId: number | null;
  amountRial: string;
  method: 'cash' | 'card' | 'transfer' | 'pos';
  packageId: number | null;
}

export const emptyPaymentDraft: PaymentDraft = {
  memberId: null,
  amountRial: '',
  method: 'cash',
  packageId: null,
};

export interface OpsFieldError {
  field: 'memberId' | 'amountRial';
  message: string;
}

/** Persian-first money display: grouped thousands, no decimals (Rial has none). */
export function formatRial(value: number): string {
  if (!Number.isFinite(value)) return '—';
  return Math.round(value)
    .toString()
    .replace(/\B(?=(\d{3})+(?!\d))/g, ',');
}

/** Parse a user-typed Rial amount, tolerating Persian digits and separators. */
export function parseRial(raw: string): number | null {
  const normalized = raw
    .replace(/[۰-۹]/g, (d) => String(d.charCodeAt(0) - 0x06f0))
    .replace(/[٬,،\s]/g, '');
  if (normalized === '') return null;
  if (!/^\d+$/.test(normalized)) return null;
  const n = Number(normalized);
  return Number.isFinite(n) ? n : null;
}

/** Validate a payment draft before it ever reaches the API. */
export function validatePayment(draft: PaymentDraft): OpsFieldError[] {
  const errors: OpsFieldError[] = [];
  if (draft.memberId === null) {
    errors.push({ field: 'memberId', message: 'یک عضو انتخاب کنید' });
  }
  const amount = parseRial(draft.amountRial);
  if (amount === null) {
    errors.push({ field: 'amountRial', message: 'مبلغ را به ریال وارد کنید' });
  } else if (amount <= 0) {
    errors.push({ field: 'amountRial', message: 'مبلغ باید بزرگ‌تر از صفر باشد' });
  }
  return errors;
}

/** A QR payload is only worth sending if it carries the signed core fields. */
export function qrLooksComplete(payload: Record<string, unknown>): boolean {
  return (
    typeof payload.mid === 'number' &&
    typeof payload.gym === 'number' &&
    typeof payload.exp === 'number' &&
    typeof payload.sig === 'string' &&
    payload.sig.length > 0
  );
}
