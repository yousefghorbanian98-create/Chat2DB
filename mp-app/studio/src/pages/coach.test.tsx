import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { afterEach, describe, expect, it, vi } from 'vitest';

import type { AiRuntime, Member, NutritionPlan } from '../api/client';
import { Coach } from './Coach';

afterEach(() => {
  vi.unstubAllGlobals();
  vi.restoreAllMocks();
});

const MEMBERS: Member[] = [
  {
    id: 1,
    membership_code: 'MP-0100',
    first_name: 'Aria',
    last_name: 'Zaker',
    sex: 'male',
    birth_date: null,
    phone: null,
    membership_exp: null,
    guardian_consent: false,
    active_injuries: 0,
  },
];

// The live-verified numbers for LBM 71.8327 / active / cut.
const PLAN: NutritionPlan = {
  member_id: 1,
  lean_mass_kg: 71.8327,
  bmr_kcal: 1921.6,
  tdee_kcal: 3314.7,
  target_kcal: 2817.5,
  protein_g: 129.3,
  carbs_g: 399.0,
  fat_g: 78.3,
};

const OFFLINE: AiRuntime = {
  available: false,
  base_url: 'http://127.0.0.1:11434',
  model: null,
  models: [],
  error: 'ConnectError: [Errno 111] Connection refused',
  note: 'Rules remain authoritative even when a local LLM is present (C7).',
};

interface Route {
  method?: string;
  match: string;
  status?: number;
  body?: unknown;
}

/** Exact-pathname stub (substring matching is ambiguous across these URLs). */
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

function baseRoutes(extra: Route[] = []): Route[] {
  return [
    { match: '/api/v1/members', body: MEMBERS },
    { match: '/api/v1/ai/runtime', body: OFFLINE },
    ...extra,
  ];
}

describe('Coach', () => {
  it('reports offline AI honestly and keeps the rules story (C7)', async () => {
    stubFetch(baseRoutes());
    render(<Coach />);

    await waitFor(() => expect(screen.getByTestId('ai-available')).toBeInTheDocument());
    expect(screen.getByTestId('ai-available')).toHaveTextContent('مدل محلی در دسترس نیست');
    expect(screen.getByTestId('ai-note')).toHaveTextContent('C7');
  });

  it('does not invent numbers when the member has no assessment', async () => {
    stubFetch(
      baseRoutes([
        {
          method: 'POST',
          match: '/api/v1/nutrition/members/1/plan',
          status: 422,
          body: { detail: 'no assessment with lean mass — run a JP7 assessment first' },
        },
      ]),
    );
    const user = userEvent.setup();
    render(<Coach />);

    await user.selectOptions(await screen.findByTestId('nutrition-member'), '1');
    await user.click(screen.getByRole('button', { name: 'محاسبهٔ انرژی و ماکرو' }));

    await waitFor(() =>
      expect(screen.getByTestId('nutrition-error')).toHaveTextContent(
        'ابتدا یک ارزیابی JP7 ثبت کنید',
      ),
    );
    expect(screen.queryByTestId('nutrition-result')).not.toBeInTheDocument();
  });

  it('shows the server-computed macros, not client maths', async () => {
    stubFetch(
      baseRoutes([
        {
          method: 'POST',
          match: '/api/v1/nutrition/members/1/plan',
          status: 201,
          body: PLAN,
        },
      ]),
    );
    const user = userEvent.setup();
    render(<Coach />);

    await user.selectOptions(await screen.findByTestId('nutrition-member'), '1');
    await user.click(screen.getByTestId('goal-cut'));
    await user.selectOptions(screen.getByTestId('nutrition-activity'), 'active');
    await user.click(screen.getByRole('button', { name: 'محاسبهٔ انرژی و ماکرو' }));

    const result = await screen.findByTestId('nutrition-result');
    // Independently verified: 370 + 21.6*71.8327 = 1921.6; *1.725 = 3314.7; *0.85 = 2817.5
    expect(result).toHaveTextContent('1922'); // BMR rounded
    expect(result).toHaveTextContent('3315'); // TDEE rounded
    expect(result).toHaveTextContent('2818'); // target rounded
    expect(result).toHaveTextContent('71.83'); // LBM
  });

  it('carries the clinical disclaimer with every plan', async () => {
    stubFetch(
      baseRoutes([
        {
          method: 'POST',
          match: '/api/v1/nutrition/members/1/plan',
          status: 201,
          body: PLAN,
        },
      ]),
    );
    const user = userEvent.setup();
    render(<Coach />);

    await user.selectOptions(await screen.findByTestId('nutrition-member'), '1');
    await user.click(screen.getByRole('button', { name: 'محاسبهٔ انرژی و ماکرو' }));

    await waitFor(() =>
      expect(screen.getByTestId('nutrition-result')).toHaveTextContent('جای توصیهٔ پزشک'),
    );
  });

  it('keeps the compute button disabled until a member is chosen', async () => {
    stubFetch(baseRoutes());
    render(<Coach />);
    await screen.findByTestId('nutrition-member');
    expect(screen.getByRole('button', { name: 'محاسبهٔ انرژی و ماکرو' })).toBeDisabled();
  });
});
