import { render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';

import { MotionCard } from './MotionCard';

/**
 * jsdom ships no `matchMedia`, so without this stub `useReducedMotion()` always
 * resolved to false and the reduced-motion branch went untested. This lives in
 * its own file on purpose: framer-motion keeps the MediaQueryList it first
 * creates, so a file that already rendered with motion enabled cannot flip it.
 */
describe('MotionCard under prefers-reduced-motion', () => {
  it('renders fully but applies no entrance transform', () => {
    window.matchMedia = vi.fn(
      (query: string) =>
        ({
          matches: query.includes('prefers-reduced-motion'),
          media: query,
          onchange: null,
          addEventListener: vi.fn(),
          removeEventListener: vi.fn(),
          addListener: vi.fn(),
          removeListener: vi.fn(),
          dispatchEvent: vi.fn(() => true),
        }) as unknown as MediaQueryList,
    );

    render(
      <MotionCard title="عنوان" testId="reduced" animateOnMount>
        <p>body</p>
      </MotionCard>,
    );

    const card = screen.getByTestId('reduced');
    // Readable content is untouched; only the motion is removed, so nothing is
    // left invisible at opacity 0 or shifted off its final position.
    expect(card.textContent).toContain('عنوان');
    expect(card.textContent).toContain('body');
    const style = card.getAttribute('style') ?? '';
    expect(style).not.toContain('opacity: 0');
    expect(style).not.toContain('translateY(12px)');
  });
});
