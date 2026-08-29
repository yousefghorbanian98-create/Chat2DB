import {
  createContext,
  useCallback,
  useContext,
  useMemo,
  useState,
  type ReactNode,
} from 'react';

import { api, tokenStore, type LoginResponse } from '../api/client';

interface AuthState {
  role: string | null;
  gymId: number | null;
  login: (username: string, pin: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthState | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [session, setSession] = useState<{ role: string; gymId: number } | null>(() => {
    // Restore a lightweight "am I logged in?" flag; the server re-verifies the
    // token on the first real request.
    try {
      const raw = localStorage.getItem('mp.session');
      if (!raw || !tokenStore.get()) return null;
      const parsed = JSON.parse(raw) as { role?: string; gym_id?: number };
      return parsed.role ? { role: parsed.role, gymId: parsed.gym_id ?? 1 } : null;
    } catch {
      return null;
    }
  });

  const login = useCallback(async (username: string, pin: string) => {
    const body: LoginResponse = await api.login(username, pin);
    tokenStore.set(body.token);
    try {
      localStorage.setItem('mp.session', JSON.stringify({ role: body.role, gym_id: body.gym_id }));
    } catch {
      /* private mode */
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

export function useAuth(): AuthState {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used inside <AuthProvider>');
  return ctx;
}
