import { createContext, useCallback, useContext, useEffect, useState, type ReactNode } from "react";
import { roleFromToken } from "../lib/roleNav";
import {
  API_BASE,
  SESSION_EXPIRED_EVENT,
  clearSession,
  getAccessToken,
  getRefreshToken,
  logoutSession,
  sessionFetch,
  storeTokenPair,
  verifyOtp,
} from "../lib/session";

export type AuthStatus = "checking" | "authenticated" | "unauthenticated";

interface AuthContextValue {
  status: AuthStatus;
  notice: string | null;
  signIn: (phone: string, code: string) => Promise<void>;
  signOut: () => Promise<boolean>;
}

const noProvider: AuthContextValue = {
  status: "authenticated",
  notice: null,
  signIn: async () => undefined,
  signOut: async () => false,
};
const AuthContext = createContext<AuthContextValue>(noProvider);

const STUDIO_ROLES = new Set(["super_admin", "admin", "manager", "coach", "reception"]);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [status, setStatus] = useState<AuthStatus>("checking");
  const [notice, setNotice] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    const onSessionExpired = () => {
      setNotice("نشست معتبر نیست؛ دوباره وارد شوید.");
      setStatus("unauthenticated");
    };
    window.addEventListener(SESSION_EXPIRED_EVENT, onSessionExpired);

    const restore = async () => {
      if (!getAccessToken() && !getRefreshToken()) {
        if (active) setStatus("unauthenticated");
        return;
      }
      try {
        const response = await sessionFetch(`${API_BASE}/members/me`);
        const role = roleFromToken(getAccessToken());
        if (response.ok && STUDIO_ROLES.has(role)) {
          if (active) setStatus("authenticated");
          return;
        }
        if (response.ok) await logoutSession();
        else clearSession();
        if (active) setStatus("unauthenticated");
      } catch {
        // A network error cannot restore a protected screen; leave no authenticated UI.
        if (active) setStatus("unauthenticated");
      }
    };
    void restore();

    return () => {
      active = false;
      window.removeEventListener(SESSION_EXPIRED_EVENT, onSessionExpired);
    };
  }, []);

  const signIn = useCallback(async (phone: string, code: string) => {
    const pair = await verifyOtp(phone, code);
    const role = roleFromToken(pair.access_token);
    if (!STUDIO_ROLES.has(role)) {
      await logoutSession(pair.refresh_token);
      throw new Error("این حساب مجاز به ورود به استودیو نیست");
    }
    storeTokenPair(pair);
    setNotice(null);
    setStatus("authenticated");
  }, []);

  const signOut = useCallback(async () => {
    const revocation = logoutSession();
    // Hide protected UI immediately; the server call only confirms remote revocation.
    setStatus("unauthenticated");
    const serverRevoked = await revocation;
    setNotice(
      serverRevoked
        ? "از حساب خارج شدید."
        : "از این مرورگر خارج شدید، اما لغو نشست سرور تأیید نشد.",
    );
    return serverRevoked;
  }, []);

  return <AuthContext.Provider value={{ status, notice, signIn, signOut }}>{children}</AuthContext.Provider>;
}

export function useAuth(): AuthContextValue {
  return useContext(AuthContext);
}
