import { act, renderHook } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import { api, ApiError } from '../api/client';
import type * as apiClient from '../api/client';
import { useCheckinQr } from './useCheckinQr';

vi.mock('../api/client', async () => {
  const actual = await vi.importActual<typeof apiClient>('../api/client');
  return { ...actual, api: { ...actual.api, clientCheckinQr: vi.fn() } };
});

const clientCheckinQr = vi.mocked(api.clientCheckinQr);

/**
 * Drain pending microtasks under fake timers.
 *
 * RTL's `waitFor` polls on real timers, which `vi.useFakeTimers()` freezes, so
 * awaiting an effect's promise has to be done by hand here.
 */
async function flush(): Promise<void> {
  await act(async () => {
    await Promise.resolve();
  });
}

/** A server-signed payload of the exact shape `sign_qr` emits. */
function payload(mid = 2) {
  return { payload: { v: 1, typ: 'member', gym: 1, mid, exp: 0, sig: 'abc' }, expires_in: 60 };
}

describe('useCheckinQr', () => {
  beforeEach(() => {
    vi.useFakeTimers();
    clientCheckinQr.mockReset();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it('does not mint a code while the card is hidden', () => {
    renderHook(() => useCheckinQr(false));
    expect(clientCheckinQr).not.toHaveBeenCalled();
  });

  it('exposes the payload as a JSON string and starts the countdown', async () => {
    clientCheckinQr.mockResolvedValue(payload());
    const { result } = renderHook(() => useCheckinQr(true));

    await flush();
    expect(result.current.payload).not.toBeNull();
    expect(JSON.parse(result.current.payload as string)).toMatchObject({ typ: 'member', mid: 2 });
    expect(result.current.secondsLeft).toBe(60);
    expect(result.current.error).toBeNull();

    act(() => vi.advanceTimersByTime(3000));
    expect(result.current.secondsLeft).toBe(57);
  });

  it('re-mints before the kiosk would refuse an expired code', async () => {
    clientCheckinQr.mockResolvedValue(payload());
    const { result } = renderHook(() => useCheckinQr(true));
    await flush();
    expect(result.current.secondsLeft).toBe(60);

    // 60s TTL with an 8s refresh margin: at ~53s left it must fetch again.
    act(() => vi.advanceTimersByTime(53_000));
    expect(clientCheckinQr).toHaveBeenCalledTimes(2);
  });

  it('surfaces the server message when minting fails', async () => {
    clientCheckinQr.mockRejectedValue(new ApiError(403, 'فقط ورزشکار'));
    const { result } = renderHook(() => useCheckinQr(true));

    await flush();
    expect(result.current.error).toBe('فقط ورزشکار');
    expect(result.current.payload).toBeNull();
  });

  it('uses a generic message for a non-API failure', async () => {
    clientCheckinQr.mockRejectedValue(new TypeError('offline'));
    const { result } = renderHook(() => useCheckinQr(true));
    await flush();
    expect(result.current.error).toBe('دریافت کد ناموفق بود');
  });

  it('mints a fresh code when the athlete taps refresh', async () => {
    clientCheckinQr.mockResolvedValue(payload());
    const { result } = renderHook(() => useCheckinQr(true));
    await flush();
    expect(clientCheckinQr).toHaveBeenCalledTimes(1);

    act(() => result.current.refresh());
    await flush();
    expect(clientCheckinQr).toHaveBeenCalledTimes(2);
  });
});
