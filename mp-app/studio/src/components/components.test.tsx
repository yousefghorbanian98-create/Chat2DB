import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { afterEach, describe, expect, it, vi } from 'vitest';

import { CoreStatus, type CoreHealth } from './CoreStatus';
import { MotionButton } from './MotionButton';
import { MotionCard } from './MotionCard';
import { Skeleton } from './Skeleton';

afterEach(() => {
  vi.restoreAllMocks();
});

function mockHealth(body: CoreHealth, ok = true): void {
  vi.stubGlobal(
    'fetch',
    vi.fn(async () => ({
      ok,
      status: ok ? 200 : 503,
      json: async () => body,
    })),
  );
}

describe('MotionButton', () => {
  it('renders its label and fires onClick', async () => {
    const user = userEvent.setup();
    const onClick = vi.fn();
    render(<MotionButton onClick={onClick}>ثبت عضو</MotionButton>);

    await user.click(screen.getByRole('button', { name: 'ثبت عضو' }));
    expect(onClick).toHaveBeenCalledTimes(1);
  });

  it('is busy + blocked while loading, and says so to assistive tech', () => {
    render(<MotionButton state="loading">ذخیره</MotionButton>);
    const button = screen.getByRole('button');
    expect(button).toBeDisabled();
    expect(button).toHaveAttribute('aria-busy', 'true');
  });

  it('shows a recovery message on error (never a dead end)', () => {
    render(<MotionButton state="error">ذخیره</MotionButton>);
    expect(screen.getByRole('alert')).toHaveTextContent('خطا');
  });

  it('never renders a disabled-looking clickable as clickable', () => {
    render(<MotionButton disabled>ذخیره</MotionButton>);
    expect(screen.getByRole('button')).toBeDisabled();
  });
});

describe('MotionCard', () => {
  it('renders as an article with the glass class and its title', () => {
    render(<MotionCard title="ارزیابی JP7" testId="card">محتوا</MotionCard>);
    const card = screen.getByTestId('card');
    expect(card.tagName).toBe('ARTICLE');
    expect(card).toHaveClass('glass');
    expect(card).toHaveTextContent('ارزیابی JP7');
  });
});

describe('Skeleton', () => {
  it('is announced as a status region with a real label', () => {
    render(<Skeleton label="در حال بارگذاری اعضا" />);
    expect(screen.getByRole('status')).toHaveAccessibleName('در حال بارگذاری اعضا');
  });
});

describe('CoreStatus (health contract)', () => {
  it('shows a skeleton first, then the online detail', async () => {
    mockHealth({
      status: 'ok',
      service: 'muscle-paradise-core',
      version: '0.1.0',
      db: { ok: true, schema_version: '0001_core', table_count: 25 },
    });
    render(<CoreStatus />);

    expect(screen.getByRole('status')).toHaveAccessibleName(
      'بررسی وضعیت هستهٔ محلی',
    );
    await waitFor(() => expect(screen.getByTestId('mp-core-status')).toHaveAttribute('data-phase', 'online'));
    expect(screen.getByTestId('mp-core-status')).toHaveTextContent('0001_core');
  });

  it('reports offline when the core answers degraded', async () => {
    mockHealth({
      status: 'degraded',
      service: 'muscle-paradise-core',
      version: '0.1.0',
      db: { ok: false },
    });
    render(<CoreStatus />);
    await waitFor(() =>
      expect(screen.getByTestId('mp-core-status')).toHaveAttribute('data-phase', 'offline'),
    );
  });

  it('reports offline when the core is unreachable (fetch throws)', async () => {
    vi.stubGlobal(
      'fetch',
      vi.fn(async () => {
        throw new Error('ECONNREFUSED');
      }),
    );
    render(<CoreStatus />);
    await waitFor(() =>
      expect(screen.getByTestId('mp-core-status')).toHaveAttribute('data-phase', 'offline'),
    );
    expect(screen.getByTestId('mp-core-status')).toHaveTextContent('ECONNREFUSED');
  });
});
