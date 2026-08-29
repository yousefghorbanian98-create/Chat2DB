import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { afterEach, describe, expect, it, vi } from 'vitest';

import type { Member } from '../api/client';
import { CheckinPanel } from './CheckinPanel';
import { PaymentPanel } from './PaymentPanel';

afterEach(() => {
  vi.unstubAllGlobals();
  vi.restoreAllMocks();
});

const MEMBERS: Member[] = [
  {
    id: 7,
    membership_code: 'MP-0007',
    first_name: 'Sara',
    last_name: 'Azad',
    sex: 'female',
    birth_date: null,
    phone: null,
    membership_exp: null,
    guardian_consent: false,
    active_injuries: 0,
  },
];

interface StubRoute {
  method?: string;
  match: string;
  status?: number;
  body?: unknown;
}

/** Route fetches by URL substring so panels can be tested without a server. */
function stubFetch(routes: StubRoute[]): void {
  vi.stubGlobal(
    'fetch',
    vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      const url = String(input);
      const method = (init?.method ?? 'GET').toUpperCase();
      const hit = routes.find(
        (r) => url.includes(r.match) && (r.method ?? 'GET') === method,
      );
      if (!hit) throw new Error(`unexpected fetch ${method} ${url}`);
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

describe('CheckinPanel', () => {
  it('shows an empty state when the gym has no members', () => {
    render(<CheckinPanel members={[]} onCheckedIn={() => {}} />);
    expect(screen.getByTestId('checkin-empty')).toBeInTheDocument();
  });

  it('checks a member in and reports success', async () => {
    const onCheckedIn = vi.fn();
    stubFetch([
      {
        method: 'POST',
        match: '/attendance/check-in',
        status: 201,
        body: { id: 1, member_id: 7, method: 'manual' },
      },
    ]);
    const user = userEvent.setup();
    render(<CheckinPanel members={MEMBERS} onCheckedIn={onCheckedIn} />);

    await user.selectOptions(screen.getByTestId('checkin-member'), '7');
    await user.click(screen.getByRole('button', { name: 'ثبت ورود' }));

    await waitFor(() =>
      expect(screen.getByTestId('checkin-outcome')).toHaveTextContent('ورود ثبت شد'),
    );
    expect(onCheckedIn).toHaveBeenCalled();
  });

  it('translates a 402 into an actionable Persian message', async () => {
    stubFetch([
      {
        method: 'POST',
        match: '/attendance/check-in',
        status: 402,
        body: { detail: 'membership expired' },
      },
    ]);
    const user = userEvent.setup();
    render(<CheckinPanel members={MEMBERS} onCheckedIn={() => {}} />);

    await user.selectOptions(screen.getByTestId('checkin-member'), '7');
    await user.click(screen.getByRole('button', { name: 'ثبت ورود' }));

    await waitFor(() =>
      expect(screen.getByTestId('checkin-outcome')).toHaveTextContent('اشتراک منقضی'),
    );
  });

  it('rejects an unsigned QR before calling the API', async () => {
    const user = userEvent.setup();
    render(<CheckinPanel members={MEMBERS} onCheckedIn={() => {}} />);

    // Pasting JSON is not character typing: `{` is a user-event modifier,
    // so set the value the way a scanner paste would.
    fireEvent.change(screen.getByTestId('checkin-qr'), { target: { value: '{"mid":7}' } });
    await user.click(screen.getByRole('button', { name: 'چک‌این با QR' }));

    expect(screen.getByTestId('checkin-outcome')).toHaveTextContent('فاقد فیلدهای امضاشده');
  });

  it('rejects malformed JSON without a dead end', async () => {
    const user = userEvent.setup();
    render(<CheckinPanel members={MEMBERS} onCheckedIn={() => {}} />);

    fireEvent.change(screen.getByTestId('checkin-qr'), { target: { value: 'not json' } });
    await user.click(screen.getByRole('button', { name: 'چک‌این با QR' }));

    expect(screen.getByTestId('checkin-outcome')).toHaveTextContent('JSON نامعتبر');
  });
});

describe('PaymentPanel', () => {
  it('lists packages and fills the amount when one is picked', async () => {
    stubFetch([
      {
        match: '/packages',
        body: [
          {
            id: 2,
            name: 'یک ماهه',
            duration_days: 30,
            price_rial: 1500000,
            active: 1,
            created_at: '2026-01-01',
          },
        ],
      },
    ]);
    const user = userEvent.setup();
    render(<PaymentPanel members={MEMBERS} onPaid={() => {}} />);

    await user.click(await screen.findByTestId('package-2'));
    expect(screen.getByTestId('payment-amount')).toHaveValue('1500000');
  });

  it('blocks submit and names the problem when no member is chosen', async () => {
    stubFetch([{ match: '/packages', body: [] }]);
    const user = userEvent.setup();
    render(<PaymentPanel members={MEMBERS} onPaid={() => {}} />);

    await user.type(screen.getByTestId('payment-amount'), '500000');
    await user.click(screen.getByRole('button', { name: 'ثبت پرداخت' }));

    expect(screen.getByTestId('payment-error')).toHaveTextContent('یک عضو انتخاب کنید');
  });

  it('records a payment and links the receipt', async () => {
    const onPaid = vi.fn();
    stubFetch([
      { match: '/packages', body: [] },
      {
        method: 'POST',
        match: '/api/v1/payments',
        status: 201,
        body: {
          id: 11,
          member_id: 7,
          package_id: null,
          amount_rial: 500000,
          method: 'cash',
          receipt_no: 'R-0001',
          voided: 0,
          staff_id: 1,
          created_at: '2026-08-29',
        },
      },
    ]);
    const user = userEvent.setup();
    render(<PaymentPanel members={MEMBERS} onPaid={onPaid} />);

    await user.selectOptions(screen.getByTestId('payment-member'), '7');
    await user.type(screen.getByTestId('payment-amount'), '500,000');
    await user.click(screen.getByRole('button', { name: 'ثبت پرداخت' }));

    const success = await screen.findByTestId('payment-success');
    expect(success).toHaveTextContent('500,000');
    expect(success).toHaveTextContent('R-0001');
    expect(onPaid).toHaveBeenCalled();
  });
});
