import '@testing-library/jest-dom/vitest';

// recharts measures its container with ResizeObserver, which jsdom lacks.
// Without this the body-fat chart throws during render in tests.
class ResizeObserverStub {
  observe(): void {}
  unobserve(): void {}
  disconnect(): void {}
}

if (typeof globalThis.ResizeObserver === 'undefined') {
  globalThis.ResizeObserver = ResizeObserverStub as unknown as typeof ResizeObserver;
}
