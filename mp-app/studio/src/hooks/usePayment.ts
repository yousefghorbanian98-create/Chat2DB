import { useCallback, useEffect, useState } from 'react';

import { api, ApiError, type MembershipPackage, type Payment } from '../api/client';
import {
  emptyPaymentDraft,
  parseRial,
  validatePayment,
  type PaymentDraft,
} from '../ops/opsValidation';
import type { ButtonState } from '../components/MotionButton';

/** Build the request body. */
function toBody(draft: PaymentDraft) {
  // exactOptionalPropertyTypes: omit package_id entirely rather than
  // passing `undefined`.
  return {
    member_id: draft.memberId as number,
    amount_rial: parseRial(draft.amountRial) as number,
    method: draft.method,
    ...(draft.packageId === null ? {} : { package_id: draft.packageId }),
  };
}

export interface PaymentState {
  packages: MembershipPackage[];
  draft: PaymentDraft;
  state: ButtonState;
  paid: Payment | null;
  error: string | null;
  setDraft: (updater: (d: PaymentDraft) => PaymentDraft) => void;
  pickPackage: (pkg: MembershipPackage) => void;
  submit: () => void;
}

/**
 * Front-desk payment state.
 *
 * Packages are optional: if the local core has none the cashier still enters a
 * free amount, so a failed package fetch never blocks a payment.
 */
export function usePayment(onPaid: () => void): PaymentState {
  const [packages, setPackages] = useState<MembershipPackage[]>([]);
  const [draft, setDraft] = useState<PaymentDraft>(emptyPaymentDraft);
  const [state, setState] = useState<ButtonState>('idle');
  const [paid, setPaid] = useState<Payment | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let alive = true;
    (async () => {
      try {
        const list = await api.listPackages();
        if (alive) setPackages(list);
      } catch {
        /* packages are optional; a cashier can still enter a free amount */
      }
    })();
    return () => {
      alive = false;
    };
  }, []);

  const pickPackage = useCallback((pkg: MembershipPackage) => {
    setDraft((d) => ({ ...d, packageId: pkg.id, amountRial: String(pkg.price_rial) }));
  }, []);

  const submit = useCallback(() => {
    const problems = validatePayment(draft);
    if (problems.length > 0) {
      setState('error');
      setError(problems[0]?.message ?? 'فرم ناقص است');
      return;
    }
    setState('loading');
    setError(null);
    void api
      .recordPayment(toBody(draft))
      .then((res) => {
        setPaid(res);
        setState('success');
        setDraft(emptyPaymentDraft);
        onPaid();
      })
      .catch((err: unknown) => {
        setState('error');
        setError(err instanceof ApiError ? err.detail : 'ثبت پرداخت ناموفق بود');
      });
  }, [draft, onPaid]);

  return { packages, draft, state, paid, error, setDraft, pickPackage, submit };
}
