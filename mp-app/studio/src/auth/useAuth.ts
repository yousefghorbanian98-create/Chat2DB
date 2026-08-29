import { useContext } from 'react';

import { AuthContext, type AuthState } from './sessionContext';

/**
 * Read the current session. Kept out of `AuthContext.tsx` so that file exports
 * only the provider component — mixing a hook in breaks React fast refresh.
 *
 * @throws when used outside `<AuthProvider>` (fail loudly, never silently).
 */
export function useAuth(): AuthState {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error('useAuth must be used inside <AuthProvider>');
  return ctx;
}
