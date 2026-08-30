import { AuthProvider } from './auth/AuthContext';
import { useAuth } from './auth/useAuth';
import { ClientShell } from './pages/ClientShell';
import { Login } from './pages/Login';

/**
 * Root of the athlete app (installed as its own PWA from `client.html`).
 *
 * A staff token has no business here, so anything that is not a MEMBER is sent
 * to the athlete sign-in rather than being shown a coach surface.
 */
function ClientGate() {
  const { role } = useAuth();
  return role === 'MEMBER' ? <ClientShell /> : <Login initialMode="member" />;
}

export function ClientApp() {
  return (
    <AuthProvider>
      <ClientGate />
    </AuthProvider>
  );
}

export default ClientApp;
