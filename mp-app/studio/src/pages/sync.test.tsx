import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';

import type { BackupBlob, RestoreResult, SyncDelta } from '../api/client';
import { Sync } from './Sync';

afterEach(() => {
  vi.unstubAllGlobals();
  vi.restoreAllMocks();
});

const DELTA: SyncDelta = {
  cursor: '2026-08-29T20:12:18',
  total: 3,
  changes: {
    members: [{ id: 1 }],
    payments: [{ id: 1 }, { id: 2 }],
  },
};

const BACKUP: BackupBlob = { blob_b64: btoa('MPBK1 fake ciphertext'), bytes: 42 };
const RESTORED: RestoreResult = { restored: { members: 1, payments: 2 }, rows: 3 };

interface Route {
  method?: string;
  match: string;
  status?: number;
  body?: unknown;
}

function stubFetch(routes: Route[]): void {
  vi.stubGlobal(
    'fetch',
    vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      const url = new URL(String(input), 'http://test.local');
      const method = (init?.method ?? 'GET').toUpperCase();
      const hit = routes.find(
        (r) => url.pathname === r.match && (r.method ?? 'GET') === method,
      );
      if (!hit) throw new Error(`unexpected fetch ${method} ${url.pathname}`);
      const status = hit.status ?? 200;
      return {
        ok: status >= 200 && status < 300,
        status,
        statusText: String(status),
        json: async () => hit.body ?? {},
      };
    }),
  );
}

beforeEach(() => {
  // jsdom lacks object URLs. Patch the two statics onto the real URL global —
  // replacing it wholesale would break `new URL(...)`, which the stub needs.
  const anyUrl = URL as unknown as Record<string, unknown>;
  anyUrl.createObjectURL = vi.fn(() => 'blob:fake');
  anyUrl.revokeObjectURL = vi.fn();
});

describe('Sync', () => {
  it('explains the full-snapshot behaviour before the first sync', () => {
    stubFetch([]);
    render(<Sync />);
    expect(screen.getByText(/کل داده‌ها به‌عنوان نخستین تصویر/)).toBeInTheDocument();
  });

  it('shows per-table changes and stores the cursor', async () => {
    stubFetch([{ match: '/api/v1/sync/delta', body: DELTA }]);
    const user = userEvent.setup();
    render(<Sync />);

    await user.click(screen.getByRole('button', { name: 'همگام‌سازی اولیه' }));

    const result = await screen.findByTestId('sync-result');
    expect(result).toHaveTextContent('3 ردیف در 2 جدول');
    expect(result).toHaveTextContent('members');
    expect(screen.getByText(/cursor: 2026-08-29T20:12:18/)).toBeInTheDocument();
  });

  it('reports an idle second sync instead of an empty box', async () => {
    stubFetch([
      { match: '/api/v1/sync/delta', body: { cursor: 'c1', total: 0, changes: {} } },
    ]);
    const user = userEvent.setup();
    render(<Sync />);

    await user.click(screen.getByRole('button', { name: 'همگام‌سازی اولیه' }));
    await waitFor(() =>
      expect(screen.getByTestId('sync-empty')).toHaveTextContent(
        'تغییری از آخرین همگام‌سازی رخ نداده',
      ),
    );
  });

  it('keeps backup disabled until the password is strong enough', () => {
    stubFetch([]);
    render(<Sync />);
    expect(screen.getByRole('button', { name: 'تهیهٔ بکاپ' })).toBeDisabled();
  });

  it('creates an encrypted backup and reports its size', async () => {
    stubFetch([{ method: 'POST', match: '/api/v1/admin/backup', body: BACKUP }]);
    const user = userEvent.setup();
    render(<Sync />);

    await user.type(screen.getByTestId('backup-password'), 's3cret-pass');
    await user.click(screen.getByRole('button', { name: 'تهیهٔ بکاپ' }));

    await waitFor(() => expect(screen.getByTestId('backup-note')).toHaveTextContent('42 بایت'));
  });

  it('tells a non-owner why backup is refused', async () => {
    stubFetch([
      { method: 'POST', match: '/api/v1/admin/backup', status: 403, body: { detail: 'no' } },
    ]);
    const user = userEvent.setup();
    render(<Sync />);

    await user.type(screen.getByTestId('backup-password'), 's3cret-pass');
    await user.click(screen.getByRole('button', { name: 'تهیهٔ بکاپ' }));

    await waitFor(() =>
      expect(screen.getByTestId('backup-note')).toHaveTextContent('فقط OWNER'),
    );
  });

  it('restores and confirms the verified row count', async () => {
    stubFetch([
      { method: 'POST', match: '/api/v1/admin/backup/restore', body: RESTORED },
    ]);
    const user = userEvent.setup();
    render(<Sync />);

    await user.type(screen.getByTestId('backup-password'), 's3cret-pass');
    await user.type(screen.getByTestId('restore-blob'), 'TVBCSzEgZmFrZQ==');
    await user.click(screen.getByRole('button', { name: 'بازیابی' }));

    await waitFor(() =>
      expect(screen.getByTestId('restore-result')).toHaveTextContent('3 ردیف در 2 جدول'),
    );
  });

  it('surfaces a wrong-password restore failure', async () => {
    stubFetch([
      {
        method: 'POST',
        match: '/api/v1/admin/backup/restore',
        status: 422,
        body: { detail: 'wrong password or corrupt backup' },
      },
    ]);
    const user = userEvent.setup();
    render(<Sync />);

    await user.type(screen.getByTestId('backup-password'), 's3cret-pass');
    await user.type(screen.getByTestId('restore-blob'), 'TVBCSzEgZmFrZQ==');
    await user.click(screen.getByRole('button', { name: 'بازیابی' }));

    await waitFor(() =>
      expect(screen.getByTestId('restore-error')).toHaveTextContent('wrong password'),
    );
  });
});
