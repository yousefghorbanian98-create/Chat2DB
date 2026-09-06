/**
 * AssessmentJp7 page smoke tests.
 *
 * The page was decomposed into `components/assessment/*` + `pages/assessment/*`
 * hooks; this file is the guard that the wiring still holds end to end, and it
 * pins the displayed number to the SAME golden fixture as core/jp7.test.ts and
 * backend/tests/test_jp7.py (female, age 25, ΣSF 60 → Siri 13.6453 %BF).
 */
import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { afterEach, describe, expect, it, vi } from 'vitest';

import type { Assessment, Injury, Member } from '../api/client';
import { SITE_META, SITE_ORDER } from './jp7Validation';
import { AssessmentJp7 } from './AssessmentJp7';

afterEach(() => {
  vi.unstubAllGlobals();
  vi.restoreAllMocks();
});

const MEMBER: Member = {
  id: 1,
  membership_code: 'MP-0100',
  first_name: 'Nasim',
  last_name: 'Rahimi',
  sex: 'female',
  birth_date: null,
  phone: null,
  membership_exp: null,
  guardian_consent: false,
  active_injuries: 1,
};

const SHOULDER: Injury = {
  id: 1,
  member_id: 1,
  body_region: 'shoulder',
  label: 'Rotator cuff strain',
  status: 'active',
  pain_0_10: 4,
  contraindicated_patterns: ['overhead_press'],
  member_visible_note: 'Avoid overhead pressing.',
};

const STORED: Assessment = {
  id: 7,
  member_id: 1,
  protocol: 'jp7',
  equation: 'siri',
  age_years: 25,
  weight_kg: 58,
  sum_mm: 60,
  body_density: 1.067626,
  body_fat_pct: 13.6453,
  fat_mass_kg: 7.9143,
  lean_mass_kg: 50.0857,
  classification: 'athletic',
  created_at: '2026-08-29T10:00:00',
};

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

/** Standard roster + empty history. Tests override injuries via the second arg. */
function stubPage(injuries: Injury[] = []): void {
  stubFetch([
    { match: '/api/v1/members', body: [MEMBER] },
    { match: '/api/v1/members/1/assessments', body: [] },
    { match: '/api/v1/members/1/injuries', body: injuries },
    { method: 'POST', match: '/api/v1/members/1/assessments', body: STORED },
  ]);
}

/** ΣSF 60 split so every entry is an exact decimal (10×5 + 5 + 5). */
const SITE_VALUES = ['10', '10', '10', '10', '10', '5', '5'] as const;

/**
 * Fill the seven caliper sites.
 *
 * Input ids come from `SITE_META[key].en` (see NumberField), so derive them
 * from the same table rather than guessing — `abdominal` renders as "Abdomen".
 */
function fillSites(): void {
  SITE_ORDER.forEach((key, i) => {
    const el = document.getElementById(`jp7-${SITE_META[key].en}`);
    expect(el).not.toBeNull();
    if (el) fireEvent.change(el, { target: { value: SITE_VALUES[i] ?? '10' } });
  });
}

describe('AssessmentJp7 page', () => {
  it('shows a labelled skeleton while the roster is in flight', () => {
    // A fetch that never settles keeps the load phase observable.
    vi.stubGlobal(
      'fetch',
      vi.fn(() => new Promise<Response>(() => {})),
    );
    render(<AssessmentJp7 />);

    // Skeleton exposes its label as aria-label, not as text.
    expect(screen.getByRole('status', { name: 'بارگذاری اعضا' })).toBeInTheDocument();
    expect(screen.queryByTestId('assessment-member')).not.toBeInTheDocument();
  });

  it('reaches the member picker once the roster lands', async () => {
    stubPage();
    render(<AssessmentJp7 />);

    expect(await screen.findByTestId('assessment-member')).toBeInTheDocument();
  });

  it('keeps Calculate blocked until the form is valid', async () => {
    stubPage();
    render(<AssessmentJp7 />);
    await screen.findByTestId('assessment-member');

    // No athlete chosen yet: the button must not be reachable.
    expect(screen.getByRole('button', { name: 'محاسبه' })).toBeDisabled();
  });

  it('surfaces the injury banner for an active limitation', async () => {
    stubPage([SHOULDER]);
    render(<AssessmentJp7 />);
    await screen.findByTestId('assessment-member');

    await userEvent.selectOptions(screen.getByTestId('assessment-member'), '1');
    expect(await screen.findByTestId('injury-banner')).toBeInTheDocument();
  });

  it('lists field errors instead of silently computing', async () => {
    stubPage();
    const user = userEvent.setup();
    render(<AssessmentJp7 />);
    await screen.findByTestId('assessment-member');

    await user.selectOptions(screen.getByTestId('assessment-member'), '1');
    // An out-of-range site must be rejected with a reason, not a number.
    const chest = document.getElementById('jp7-Chest');
    expect(chest).not.toBeNull();
    if (chest) await user.type(chest, '999');
    fireEvent.blur(chest as HTMLElement);

    expect(await screen.findByTestId('error-summary')).toBeInTheDocument();
  });

  it('renders the golden Siri result for ΣSF 60 (female, 25)', async () => {
    stubPage();
    const user = userEvent.setup();
    render(<AssessmentJp7 />);
    await screen.findByTestId('assessment-member');

    await user.selectOptions(screen.getByTestId('assessment-member'), '1');
    fillSites();

    const weight = document.getElementById('jp7-Weight');
    const age = document.getElementById('jp7-Age');
    expect(weight).not.toBeNull();
    expect(age).not.toBeNull();
    if (weight) fireEvent.change(weight, { target: { value: '58' } });
    if (age) fireEvent.change(age, { target: { value: '25' } });

    await user.click(screen.getByRole('button', { name: 'محاسبه' }));

    // 13.6453 → toFixed(1) === '13.6'
    const preview = await screen.findByTestId('bf-preview');
    await waitFor(() => expect(preview.textContent?.trim()).toBe('13.6%'));
  });

  it('saves through the core and shows the stored confirmation', async () => {
    stubPage();
    const user = userEvent.setup();
    render(<AssessmentJp7 />);
    await screen.findByTestId('assessment-member');

    await user.selectOptions(screen.getByTestId('assessment-member'), '1');
    fillSites();

    const weight = document.getElementById('jp7-Weight');
    const age = document.getElementById('jp7-Age');
    if (weight) fireEvent.change(weight, { target: { value: '58' } });
    if (age) fireEvent.change(age, { target: { value: '25' } });

    await user.click(screen.getByRole('button', { name: 'محاسبه' }));
    await screen.findByTestId('bf-preview');

    // Save is only meaningful once a preview exists (C4 — core re-derives it).
    const save = screen.getByRole('button', { name: 'ذخیره ارزیابی' });
    await user.click(save);

    const stored = await screen.findByTestId('bf-saved');
    await waitFor(() => expect(stored.textContent).toContain('13.6%'));
  });
});
