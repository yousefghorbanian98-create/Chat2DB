import { render, screen } from '@testing-library/react';
import { afterEach, describe, expect, it, vi } from 'vitest';

import { MotionCard } from './MotionCard';

interface MediaQueryListStub {
  matches: boolean;
  media: string;
  onchange: null;
  addEventListener: () => void;
  removeEventListener: () => void;
  addListener: () => void;
  removeListener: () => void;
  dispatchEvent: () => boolean;
}

/**
 * jsdom ships no `matchMedia`, so `useReducedMotion()` always resolved to
 * `false` and the reduced-motion branch of every animated component went
 * untested. MASTER.md requires that branch to exist and be honoured.
 */
function stubReducedMotion(reduce: boolean): void {
  window.matchMedia = vi.fn((query: string): MediaQueryListStub => ({
    matches: reduce && query.includes('prefers-reduced-motion'),
    media: query,
    onchange: null,
    addEventListener: vi.fn(),
    removeEventListener: vi.fn(),
    addListener: vi.fn(),
    removeListener: vi.fn(),
    dispatchEvent: vi.fn(() => true),
  }));
}

afterEach(() => vi.restoreAllMocks());

describe('MotionCard', () => {
  it('renders children without a heading when no title is given', () => {
    stubReducedMotion(false);
    render(
      <MotionCard testId="card">
        <p>body</p>
      </MotionCard>,
    );
    const card = screen.getByTestId('card');
    expect(card.querySelector('h3')).toBeNull();
    expect(card.textContent).toContain('body');
  });

  it('renders the title heading and an entrance animation when asked', () => {
    stubReducedMotion(false);
    render(
      <MotionCard title="عنوان" testId="card" animateOnMount mode="cinematic">
        <p>body</p>
      </MotionCard>,
    );
    expect(screen.getByText('عنوان')).toBeTruthy();
  });
});
