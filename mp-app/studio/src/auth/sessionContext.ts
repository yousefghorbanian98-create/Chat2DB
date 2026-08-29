import { createContext } from 'react';

export interface AuthState {
  role: string | null;
  gymId: number | null;
  login: (username: string, pin: string) => Promise<void>;
  logout: () => void;
}

/**
 * The session context object.
 *
 * Lives in its own component-free module so `AuthContext.tsx` exports only the
 * provider (React fast refresh requires that) and `useAuth.ts` can import the
 * context without pulling in a component.
 */
export const AuthContext = createContext<AuthState | null>(null);
