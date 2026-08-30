/**
 * Register the service worker.
 *
 * A registration failure must not break the app (private mode, an unsupported
 * browser, a file:// shell), but it must not be swallowed either: the reason is
 * kept here and announced on `window` so a surface can show it.
 */

let failure: string | null = null;

/** Why registration failed, or `null` when it did not. */
export function serviceWorkerError(): string | null {
  return failure;
}

export function registerServiceWorker(): void {
  // Check the value, not `in`: browsers expose the property as undefined when
  // the feature is off, and `in` would report it as present.
  if (!navigator.serviceWorker) {
    failure = 'این مرورگر از نصب آفلاین پشتیبانی نمی‌کند.';
    return;
  }
  if (window.location.protocol === 'file:') return; // no SW scope on file://

  window.addEventListener('load', () => {
    navigator.serviceWorker.register('./sw.js').catch((error: unknown) => {
      failure = error instanceof Error ? error.message : String(error);
      window.dispatchEvent(new CustomEvent('mp:sw-error', { detail: failure }));
    });
  });
}
