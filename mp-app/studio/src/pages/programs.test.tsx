import { render, screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { afterEach, describe, expect, it, vi } from 'vitest';

import type { Member } from '../api/client';
import { Programs } from './Programs';

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
    active_injuries: 1,
  },
];

const GENERATED = {
  id: 42,
  status: 'draft',
  template: 'fb',
  days: [
    { name: 'A', exercises: ['ex007', 'ex010'], dropped: [] },
    { name: 'B', exercises: ['ex022'], dropped: [] },
  ],
  meta: {
    blocked_patterns: ['heavy_deadlift'],
    equipment_available: ['barbell', 'bodyweight'],
    dropped: [{ day: 'B', exercise: 'ex003', reason: 'hard_block' }],
    corrective_block_added: true,
  },
};

interface Route {
  method?: string;
  match: string;
  status?: number;
  body?: unknown;
}

function stubFetch(routes: Route[]): void {
  // Exact pathname matching: substring matching is ambiguous here because
  // `/api/v1/members/7/programs` contains `/api/v1/members` as well.
  vi.stubGlobal(
    'fetch',
    vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      const url = new URL(String(input), 'http://test.local');
      const method = (init?.method ?? 'GET').toUpperCase();
      const hit = routes.find((r) => url.pathname === r.match && (r.method ?? 'GET') === method);
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

/** Members + empty history, so every test starts from the same place. */
function baseRoutes(extra: Route[] = []): Route[] {
  return [
    { match: '/api/v1/members', body: MEMBERS },
    { match: '/api/v1/members/7/programs', body: [] },
    ...extra,
  ];
}

async function pickMember() {
  const user = userEvent.setup();
  await user.selectOptions(await screen.findByTestId('programs-member'), '7');
  return user;
}

describe('Programs', () => {
  it('explains what to do before anything is generated', async () => {
    stubFetch(baseRoutes());
    render(<Programs />);
    await screen.findByTestId('programs-member');
    expect(
      screen.getByText('یک عضو و قالب انتخاب کنید تا برنامهٔ قانون‌محور ساخته شود.'),
    ).toBeInTheDocument();
  });

  it('generates a program and shows every drop with a reason', async () => {
    stubFetch(
      baseRoutes([
        {
          method: 'POST',
          match: '/api/v1/members/7/programs/generate',
          status: 201,
          body: GENERATED,
        },
      ]),
    );
    render(<Programs />);
    const user = await pickMember();

    await user.click(screen.getByTestId('template-fb'));
    await user.click(screen.getByRole('button', { name: 'ساخت برنامه' }));

    const preview = await screen.findByTestId('program-preview');
    expect(within(preview).getByText('فول بادی')).toBeInTheDocument();
    // Injury filters in force are surfaced, not hidden.
    expect(screen.getByTestId('blocked-patterns')).toHaveTextContent('heavy_deadlift');
    expect(screen.getByTestId('dropped-list')).toHaveTextContent(
      'الگوی حرکتی به‌دلیل آسیب مسدود است',
    );
    expect(screen.getByTestId('dropped-list')).toHaveTextContent('ex003');
  });

  it('keeps apply disabled until a dry-run says it is safe', async () => {
    stubFetch(
      baseRoutes([
        {
          method: 'POST',
          match: '/api/v1/members/7/programs/generate',
          status: 201,
          body: GENERATED,
        },
        {
          method: 'POST',
          match: '/api/v1/programs/42/dry-run',
          body: {
            program_id: 42,
            status: 'draft',
            safe_to_apply: true,
            newly_blocked: [],
          },
        },
      ]),
    );
    render(<Programs />);
    const user = await pickMember();
    await user.click(screen.getByRole('button', { name: 'ساخت برنامه' }));
    await screen.findByTestId('program-preview');

    const applyBtn = screen.getByRole('button', { name: 'تأیید و اعمال' });
    expect(applyBtn).toBeDisabled();

    await user.click(screen.getByRole('button', { name: 'بررسی ایمنی (dry-run)' }));
    await waitFor(() =>
      expect(screen.getByTestId('dryrun-result')).toHaveTextContent('ایمن برای اعمال'),
    );
    expect(applyBtn).toBeEnabled();
  });

  it('refuses to enable apply when the dry-run finds new blocks', async () => {
    stubFetch(
      baseRoutes([
        {
          method: 'POST',
          match: '/api/v1/members/7/programs/generate',
          status: 201,
          body: GENERATED,
        },
        {
          method: 'POST',
          match: '/api/v1/programs/42/dry-run',
          body: {
            program_id: 42,
            status: 'draft',
            safe_to_apply: false,
            newly_blocked: ['ex003'],
          },
        },
      ]),
    );
    render(<Programs />);
    const user = await pickMember();
    await user.click(screen.getByRole('button', { name: 'ساخت برنامه' }));
    await screen.findByTestId('program-preview');

    await user.click(screen.getByRole('button', { name: 'بررسی ایمنی (dry-run)' }));
    await waitFor(() => expect(screen.getByTestId('dryrun-result')).toHaveTextContent('ex003'));
    expect(screen.getByRole('button', { name: 'تأیید و اعمال' })).toBeDisabled();
  });

  it('applies after a safe dry-run and refreshes history', async () => {
    stubFetch(
      baseRoutes([
        {
          method: 'POST',
          match: '/api/v1/members/7/programs/generate',
          status: 201,
          body: GENERATED,
        },
        {
          method: 'POST',
          match: '/api/v1/programs/42/dry-run',
          body: { program_id: 42, status: 'draft', safe_to_apply: true, newly_blocked: [] },
        },
        {
          method: 'POST',
          match: '/api/v1/programs/42/apply',
          body: { id: 42, status: 'trainer_approved', applied_at: '2026-08-29T20:00:00Z' },
        },
      ]),
    );
    render(<Programs />);
    const user = await pickMember();
    await user.click(screen.getByRole('button', { name: 'ساخت برنامه' }));
    await screen.findByTestId('program-preview');
    await user.click(screen.getByRole('button', { name: 'بررسی ایمنی (dry-run)' }));
    await screen.findByTestId('dryrun-result');

    await user.click(screen.getByRole('button', { name: 'تأیید و اعمال' }));
    await waitFor(() =>
      expect(screen.getByTestId('programs-notice')).toHaveTextContent('trainer_approved'),
    );
  });

  it('surfaces the C8 conflict when apply is blocked by a new injury', async () => {
    stubFetch(
      baseRoutes([
        {
          method: 'POST',
          match: '/api/v1/members/7/programs/generate',
          status: 201,
          body: GENERATED,
        },
        {
          method: 'POST',
          match: '/api/v1/programs/42/dry-run',
          body: { program_id: 42, status: 'draft', safe_to_apply: true, newly_blocked: [] },
        },
        {
          method: 'POST',
          match: '/api/v1/programs/42/apply',
          status: 409,
          body: { detail: 'injury filter now blocks exercises' },
        },
      ]),
    );
    render(<Programs />);
    const user = await pickMember();
    await user.click(screen.getByRole('button', { name: 'ساخت برنامه' }));
    await screen.findByTestId('program-preview');
    await user.click(screen.getByRole('button', { name: 'بررسی ایمنی (dry-run)' }));
    await screen.findByTestId('dryrun-result');

    await user.click(screen.getByRole('button', { name: 'تأیید و اعمال' }));
    await waitFor(() =>
      expect(screen.getByTestId('programs-notice')).toHaveTextContent('injury filter'),
    );
  });

  it('renders an empty history state', async () => {
    stubFetch(baseRoutes());
    render(<Programs />);
    await pickMember();
    await waitFor(() =>
      expect(screen.getByTestId('program-history')).toHaveTextContent('هنوز برنامه‌ای نیست'),
    );
  });

  it('lists existing programs from history', async () => {
    stubFetch([
      { match: '/api/v1/members', body: MEMBERS },
      {
        match: '/api/v1/members/7/programs',
        body: [
          {
            id: 1,
            member_id: 7,
            title: 'Full Body (rules)',
            status: 'trainer_approved',
            source: 'rules',
            payload: '{}',
            judge_score: null,
            generated_by: null,
            approved_by: null,
            applied_at: null,
            created_at: '2026-08-29',
          },
        ],
      },
    ]);
    render(<Programs />);
    await pickMember();
    await waitFor(() =>
      expect(screen.getByTestId('program-history')).toHaveTextContent('Full Body (rules)'),
    );
  });
});
