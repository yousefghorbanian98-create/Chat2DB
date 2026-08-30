import { render } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import ClientApp from './ClientApp';
import { registerServiceWorker, serviceWorkerError } from './sw-register';

describe('service worker registration', () => {
  const original = Object.getOwnPropertyDescriptor(Navigator.prototype, 'serviceWorker');

  afterEach(() => {
    if (original) Object.defineProperty(Navigator.prototype, 'serviceWorker', original);
    vi.restoreAllMocks();
  });

  it('records a readable reason when the browser has no serviceWorker', () => {
    Object.defineProperty(Navigator.prototype, 'serviceWorker', {
      configurable: true,
      get: () => undefined,
    });
    registerServiceWorker();
    expect(serviceWorkerError()).toMatch(/پشتیبانی نمی‌کند/);
  });

  it('does nothing on a file:// shell, where a worker has no scope', () => {
    const register = vi.fn();
    Object.defineProperty(Navigator.prototype, 'serviceWorker', {
      configurable: true,
      get: () => ({ register }),
    });
    // jsdom will not let a single location property be redefined; swap the object.
    const original = window.location;
    Object.defineProperty(window, 'location', {
      configurable: true,
      value: { ...original, protocol: 'file:' },
    });

    registerServiceWorker();
    window.dispatchEvent(new Event('load'));

    expect(register).not.toHaveBeenCalled();
    Object.defineProperty(window, 'location', { configurable: true, value: original });
  });

  it('registers ./sw.js on load and keeps the error when it rejects', async () => {
    const register = vi.fn().mockRejectedValue(new Error('blocked by policy'));
    Object.defineProperty(Navigator.prototype, 'serviceWorker', {
      configurable: true,
      get: () => ({ register }),
    });

    registerServiceWorker();
    window.dispatchEvent(new Event('load'));
    await Promise.resolve();
    await Promise.resolve();

    expect(register).toHaveBeenCalledWith('./sw.js');
    expect(serviceWorkerError()).toBe('blocked by policy');
  });
});

describe('ClientApp (athlete PWA root)', () => {
  beforeEach(() => localStorage.clear());

  it('opens straight into athlete sign-in, not the coach surface', () => {
    const { getByTestId, getByText, queryByText } = render(<ClientApp />);
    expect(getByTestId('mode-member').getAttribute('aria-pressed')).toBe('true');
    expect(getByText('ورود ورزشکار — کد عضویت و پین')).toBeTruthy();
    expect(queryByText(/ارزیابی JP7/)).toBeNull();
  });
});
