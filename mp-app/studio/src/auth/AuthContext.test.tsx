import { act, render, screen, waitFor } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';

import { api } from '../api/client';
import { AuthProvider } from '../auth/AuthContext';
import { useAuth } from '../auth/useAuth';

import type * as clientModule from '../api/client';

vi.mock('../api/client', async () => {
  const actual = await vi.importActual<typeof clientModule>('../api/client');
  return { ...actual, api: { ...actual.api, login: vi.fn(), memberLogin: vi.fn() } };
});

/** Exposes the session so assertions can read it without reaching into context. */
function Probe() {
  const { role, gymId, login, memberLogin, logout } = useAuth();
  return (
    <div>
      <span data-testid="role">{role ?? 'none'}</span>
      <span data-testid="gym">{gymId ?? 'none'}</span>
      <button type="button" onClick={() => void login('owner', '1111')}>
        staff
      </button>
      <button type="button" onClick={() => void memberLogin('MP-DEMO-1', '1234')}>
        member
      </button>
      <button type="button" onClick={logout}>
        out
      </button>
    </div>
  );
}

const STAFF = { token: 'tok-staff', role: 'TRAINER', gym_id: 1, expires_in: 60 };
const MEMBER = { token: 'tok-member', role: 'MEMBER', gym_id: 1, expires_in: 60 };

describe('AuthProvider session handling', () => {
  beforeEach(() => {
    localStorage.clear();
    sessionStorage.clear();
    vi.mocked(api.login).mockReset().mockResolvedValue(STAFF);
    vi.mocked(api.memberLogin).mockReset().mockResolvedValue(MEMBER);
  });

  it('starts signed out with no stored session', () => {
    render(
      <AuthProvider>
        <Probe />
      </AuthProvider>,
    );
    expect(screen.getByTestId('role').textContent).toBe('none');
  });

  it('does not trust the session flag when no token is stored', () => {
    localStorage.setItem('mp.session', JSON.stringify({ role: 'OWNER', gym_id: 3 }));
    render(
      <AuthProvider>
        <Probe />
      </AuthProvider>,
    );
    expect(screen.getByTestId('role').textContent).toBe('none');
  });

  it('restores role and gym when both the flag and a token exist', () => {
    sessionStorage.setItem('mp.token', 'tok');
    localStorage.setItem('mp.session', JSON.stringify({ role: 'OWNER', gym_id: 3 }));
    render(
      <AuthProvider>
        <Probe />
      </AuthProvider>,
    );
    expect(screen.getByTestId('role').textContent).toBe('OWNER');
    expect(screen.getByTestId('gym').textContent).toBe('3');
  });

  it('survives a corrupt session blob instead of crashing', () => {
    sessionStorage.setItem('mp.token', 'tok');
    localStorage.setItem('mp.session', '{not json');
    render(
      <AuthProvider>
        <Probe />
      </AuthProvider>,
    );
    expect(screen.getByTestId('role').textContent).toBe('none');
  });

  it('staff login stores the token and the session flag', async () => {
    render(
      <AuthProvider>
        <Probe />
      </AuthProvider>,
    );
    await act(async () => {
      screen.getByText('staff').click();
    });
    await waitFor(() => expect(screen.getByTestId('role').textContent).toBe('TRAINER'));
    expect(sessionStorage.getItem('mp.token')).toBe('tok-staff');
    expect(JSON.parse(localStorage.getItem('mp.session') ?? '{}')).toEqual({
      role: 'TRAINER',
      gym_id: 1,
    });
  });

  it('athlete login yields a MEMBER session through the same provider', async () => {
    render(
      <AuthProvider>
        <Probe />
      </AuthProvider>,
    );
    await act(async () => {
      screen.getByText('member').click();
    });
    await waitFor(() => expect(screen.getByTestId('role').textContent).toBe('MEMBER'));
    expect(api.memberLogin).toHaveBeenCalledWith('MP-DEMO-1', '1234');
    expect(sessionStorage.getItem('mp.token')).toBe('tok-member');
  });

  it('logout clears both stores', async () => {
    render(
      <AuthProvider>
        <Probe />
      </AuthProvider>,
    );
    await act(async () => {
      screen.getByText('member').click();
    });
    await waitFor(() => expect(screen.getByTestId('role').textContent).toBe('MEMBER'));

    await act(async () => {
      screen.getByText('out').click();
    });
    expect(screen.getByTestId('role').textContent).toBe('none');
    expect(sessionStorage.getItem('mp.token')).toBeNull();
    expect(localStorage.getItem('mp.session')).toBeNull();
  });
});
