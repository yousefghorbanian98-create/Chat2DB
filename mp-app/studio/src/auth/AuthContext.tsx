import { useCallback, useMemo, useState, type ReactNode } from 'react';

import { api, tokenStore, type LoginResponse } from '../api/client';
import { AuthContext, type AuthState } from './sessionContext';

/** Restore a lightweight "am I logged in?" flag; the server re-verifies the
 *  token on the first real request. */
function readStoredSession(): { role: string; gymId: number } | null {
  try {
    const raw = localStorage.getItem('mp.session');
    if (!raw || !tokenStore.get()) return null;
    const parsed = JSON.parse(raw) as { role?: string; gym_id?: number };
    return parsed.role ? { role: parsed.role, gymId: parsed.gym_id ?? 1 } : null;
  } catch {
    return null;
  }
}

/** Session provider. This file exports only the component (fast refresh). */
export function AuthProvider({ children }: { children: ReactNode }) {
  const [session, setSession] = useState<{ role: string; gymId: number } | null>(readStoredSession);

  const login = useCallback(async (username: string, pin: string) => {
    const body: LoginResponse = await api.login(username, pin);
    tokenStore.set(body.token);
    try {
      localStorage.setItem('mp.session', JSON.stringify({ role: body.role, gym_id: body.gym_id }));
    } catch {
      /* private mode: the session simply is not remembered */
    }
    setSession({ role: body.role, gymId: body.gym_id });
  }, []);

  const logout = useCallback(() => {
    tokenStore.clear();
    try {
      localStorage.removeItem('mp.session');
    } catch {
      /* noop */
    }
    setSession(null);
  }, []);

  const value = useMemo<AuthState>(
    () => ({
      role: session?.role ?? null,
      gymId: session?.gymId ?? null,
      login,
      logout,
    }),
    [session, login, logout],
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
