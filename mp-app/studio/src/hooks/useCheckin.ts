import { useCallback, useState } from 'react';

import { api, ApiError } from '../api/client';
import { qrLooksComplete } from '../ops/opsValidation';
import type { ButtonState } from '../components/MotionButton';

export type Outcome = { kind: 'ok'; text: string } | { kind: 'fail'; text: string } | null;

export interface CheckinController {
  state: ButtonState;
  outcome: Outcome;
  qrText: string;
  setQrText: (v: string) => void;
  checkInManual: (memberId: number) => void;
  submitQr: () => void;
}

/** Translate the door-facing HTTP codes into Persian the reception can act on. */
function describeError(err: unknown): string {
  if (err instanceof ApiError) {
    if (err.status === 402) return 'اشتراک منقضی شده — تمدید در پذیرش';
    if (err.status === 409) return 'این عضو همین حالا داخل باشگاه است';
    if (err.status === 401) return 'QR نامعتبر یا دستکاری‌شده';
    if (err.status === 404) return 'عضو پیدا نشد';
    return err.detail;
  }
  return 'خطای ناشناخته';
}

/**
 * Door-control state machine.
 *
 * Kept out of the component so the two entry points (manual desk entry and
 * kiosk QR paste) share one loading/error/success path instead of duplicating it.
 */
export function useCheckin(onCheckedIn: () => void): CheckinController {
  const [state, setState] = useState<ButtonState>('idle');
  const [outcome, setOutcome] = useState<Outcome>(null);
  const [qrText, setQrText] = useState('');

  const fail = useCallback((text: string) => {
    setState('error');
    setOutcome({ kind: 'fail', text });
  }, []);

  const run = useCallback(
    async (task: () => Promise<unknown>, okText: string) => {
      setState('loading');
      setOutcome(null);
      try {
        await task();
        setState('success');
        setOutcome({ kind: 'ok', text: okText });
        onCheckedIn();
      } catch (err) {
        fail(describeError(err));
      }
    },
    [onCheckedIn, fail],
  );

  const checkInManual = useCallback(
    (memberId: number) => void run(() => api.checkInManual(memberId), 'ورود ثبت شد'),
    [run],
  );

  const submitQr = useCallback(() => {
    let payload: Record<string, unknown>;
    try {
      payload = JSON.parse(qrText) as Record<string, unknown>;
    } catch {
      fail('JSON نامعتبر — خروجی اسکنر را بچسبانید');
      return;
    }
    if (!qrLooksComplete(payload)) {
      fail('QR فاقد فیلدهای امضاشده (mid/gym/exp/sig)');
      return;
    }
    void run(() => api.checkInQr(payload), 'چک‌این با QR انجام شد');
  }, [qrText, fail, run]);

  return { state, outcome, qrText, setQrText, checkInManual, submitQr };
}
