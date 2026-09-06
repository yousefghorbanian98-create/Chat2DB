import { render, screen } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';

import { Landing } from './Landing';

describe('Landing (cinematic entrance)', () => {
  beforeEach(() => vi.useFakeTimers());

  it('renders the animated mark, wordmark and tagline', () => {
    render(<Landing onDone={vi.fn()} />);
    expect(screen.getByTestId('landing')).toBeTruthy();
    expect(screen.getByTestId('landing-mark')).toBeTruthy();
    expect(screen.getByTestId('landing-title').getAttribute('aria-label')).toBe('MUSCLE PARADISE');
    expect(screen.getByText(/سیستم‌عامل باشگاه/)).toBeTruthy();
  });

  it('hands off to the app automatically after the sequence', () => {
    const onDone = vi.fn();
    render(<Landing onDone={onDone} />);
    expect(onDone).not.toHaveBeenCalled();
    vi.advanceTimersByTime(3300);
    expect(onDone).toHaveBeenCalledTimes(1);
  });

  it('skips immediately when the user taps the splash', () => {
    const onDone = vi.fn();
    const { container } = render(<Landing onDone={onDone} />);
    (container.firstChild as HTMLElement).click();
    expect(onDone).toHaveBeenCalledTimes(1);
  });
});
