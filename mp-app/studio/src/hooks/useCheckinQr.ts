import { useCallback, useEffect, useState } from 'react';

import { ApiError, api, type CheckinQr } from '../api/client';

export interface CheckinState {
  /** The signed payload, base64url-free JSON string ready for a QR symbol. */
  payload: string | null;
  /** Whole seconds left before the kiosk will refuse it. */
  secondsLeft: number;
  error: string | null;
  refresh: () => void;
}

/** Refresh this many seconds early so the scan never lands on an expired code. */
const REFRESH_MARGIN = 8;

/**
 * A short-lived, signed check-in code the athlete shows at the kiosk (map §8).
 *
 * The server mints it with a 60 s TTL; this hook re-mints just before expiry so
 * a phone left open on this screen keeps working. An expired-but-still-shown
 * code is worse than none, hence the countdown.
 */
export function useCheckinQr(enabled: boolean): CheckinState {
  const [qr, setQr] = useState<CheckinQr | null>(null);
  const [secondsLeft, setSecondsLeft] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [tick, setTick] = useState(0);

  const refresh = useCallback(() => setTick((t) => t + 1), []);

  useEffect(() => {
    if (!enabled) return;
    let alive = true;
    void api
      .clientCheckinQr()
      .then((res) => {
        if (!alive) return;
        setQr(res);
        setSecondsLeft(res.expires_in);
        setError(null);
      })
      .catch((err: unknown) => {
        if (alive) setError(err instanceof ApiError ? err.detail : 'دریافت کد ناموفق بود');
      });
    return () => {
      alive = false;
    };
  }, [enabled, tick]);

  useEffect(() => {
    if (!enabled || qr === null) return;
    const id = window.setInterval(() => {
      setSecondsLeft((s) => {
        if (s <= REFRESH_MARGIN + 1) {
          refresh();
          return qr.expires_in;
        }
        return s - 1;
      });
    }, 1000);
    return () => window.clearInterval(id);
  }, [enabled, qr, refresh]);

  return { payload: qr ? JSON.stringify(qr.payload) : null, secondsLeft, error, refresh };
}
