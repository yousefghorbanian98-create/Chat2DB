/**
 * Browser session for Studio: OTP, rotating refresh token, one 401 retry, and logout.
 * Tokens stay in the existing browser storage contract; this is not an HttpOnly-cookie
 * boundary and must not be described as XSS-proof.
 */
export const API_BASE = "/api/v1";
export const ACCESS_TOKEN_KEY = "mp_token";
export const REFRESH_TOKEN_KEY = "mp_refresh";
export const SESSION_EXPIRED_EVENT = "mp:session-expired";

const AUTH_PATHS_WITHOUT_REFRESH = new Set([
  `${API_BASE}/auth/otp/request`,
  `${API_BASE}/auth/otp/verify`,
  `${API_BASE}/auth/refresh`,
  `${API_BASE}/auth/logout`,
]);

export interface TokenPair {
  access_token: string;
  refresh_token: string;
  token_type?: string;
  user?: { id: number; phone: string; role: string; full_name: string } | null;
}

export interface OtpRequestResult {
  phone: string;
  expires_in: number;
  dev_code?: string | null;
}

export interface PhoneChangeStepResult {
  challenge_id: string;
  expires_in: number;
  dev_code?: string | null;
}

export interface PhoneChangeResult {
  status: "phone_changed";
  phone: string;
}

interface RefreshOutcome {
  succeeded: boolean;
  pair: TokenPair | null;
}

interface RefreshFlight {
  generation: number;
  promise: Promise<RefreshOutcome>;
}

let sessionGeneration = 0;
let refreshInFlight: RefreshFlight | null = null;

export function getAccessToken(): string | null {
  return typeof localStorage === "undefined" ? null : localStorage.getItem(ACCESS_TOKEN_KEY);
}

export function getRefreshToken(): string | null {
  return typeof localStorage === "undefined" ? null : localStorage.getItem(REFRESH_TOKEN_KEY);
}

function persistTokenPair(pair: TokenPair): void {
  if (typeof localStorage === "undefined") throw new Error("ذخیرهٔ نشست در این محیط ممکن نیست");
  localStorage.setItem(ACCESS_TOKEN_KEY, pair.access_token);
  localStorage.setItem(REFRESH_TOKEN_KEY, pair.refresh_token);
}

export function storeTokenPair(pair: TokenPair): void {
  if (!pair.access_token || !pair.refresh_token) {
    throw new Error("پاسخ ورود توکن دسترسی یا نوسازی ندارد");
  }
  // A fresh login supersedes any refresh response still in flight for the old session.
  sessionGeneration += 1;
  persistTokenPair(pair);
}

export function clearSession(): void {
  // Invalidate refresh work before clearing storage so a late response cannot restore it.
  sessionGeneration += 1;
  if (typeof localStorage === "undefined") return;
  localStorage.removeItem(ACCESS_TOKEN_KEY);
  localStorage.removeItem(REFRESH_TOKEN_KEY);
}

function sessionExpired(): void {
  if (typeof window !== "undefined") window.dispatchEvent(new Event(SESSION_EXPIRED_EVENT));
}

async function responseError(response: Response, fallback: string): Promise<Error> {
  try {
    const body = (await response.json()) as {
      error?: { message?: string };
      detail?: string;
    };
    return new Error(body.error?.message ?? body.detail ?? fallback);
  } catch {
    return new Error(fallback);
  }
}

async function readTokenPair(response: Response): Promise<TokenPair> {
  if (!response.ok) throw await responseError(response, `درخواست ناموفق بود (${response.status})`);
  const body = (await response.json()) as Partial<TokenPair>;
  if (typeof body.access_token !== "string" || typeof body.refresh_token !== "string") {
    throw new Error("پاسخ سرور برای نشست معتبر نیست");
  }
  return body as TokenPair;
}

export async function requestOtp(phone: string): Promise<OtpRequestResult> {
  const response = await fetch(`${API_BASE}/auth/otp/request`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ phone }),
  });
  if (!response.ok) throw await responseError(response, "ارسال کد ورود ناموفق بود");
  return (await response.json()) as OtpRequestResult;
}

export async function verifyOtp(phone: string, code: string): Promise<TokenPair> {
  const response = await fetch(`${API_BASE}/auth/otp/verify`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ phone, code }),
  });
  return readTokenPair(response);
}

async function readAuthenticatedResponse<T>(response: Response): Promise<T> {
  if (!response.ok) throw await responseError(response, "درخواست احراز هویت ناموفق بود");
  return (await response.json()) as T;
}

export async function requestPhoneChange(newPhone: string): Promise<PhoneChangeStepResult> {
  const response = await sessionFetch(`${API_BASE}/auth/phone-change/request`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ new_phone: newPhone }),
  });
  return readAuthenticatedResponse<PhoneChangeStepResult>(response);
}

export async function verifyOldPhoneChange(
  challengeId: string,
  code: string,
): Promise<PhoneChangeStepResult> {
  const response = await sessionFetch(`${API_BASE}/auth/phone-change/verify-old`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ challenge_id: challengeId, code }),
  });
  return readAuthenticatedResponse<PhoneChangeStepResult>(response);
}

export async function confirmPhoneChange(
  challengeId: string,
  code: string,
): Promise<PhoneChangeResult> {
  const response = await sessionFetch(`${API_BASE}/auth/phone-change/confirm`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ challenge_id: challengeId, code }),
  });
  return readAuthenticatedResponse<PhoneChangeResult>(response);
}

function expireSessionIfCurrent(generation: number, refreshToken: string | null): void {
  if (sessionGeneration !== generation || getRefreshToken() !== refreshToken) return;
  clearSession();
  sessionExpired();
}

async function refreshSessionRequest(
  generation: number,
  refreshToken: string | null,
): Promise<RefreshOutcome> {
  if (!refreshToken) {
    expireSessionIfCurrent(generation, refreshToken);
    return { succeeded: false, pair: null };
  }
  try {
    const response = await fetch(`${API_BASE}/auth/refresh`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh_token: refreshToken }),
    });
    if (!response.ok) {
      expireSessionIfCurrent(generation, refreshToken);
      return { succeeded: false, pair: null };
    }
    const pair = (await response.json()) as Partial<TokenPair>;
    if (typeof pair.access_token !== "string" || typeof pair.refresh_token !== "string") {
      expireSessionIfCurrent(generation, refreshToken);
      return { succeeded: false, pair: null };
    }
    // A logout, new login, or another tab's token rotation makes this response stale.
    if (sessionGeneration !== generation || getRefreshToken() !== refreshToken) {
      return { succeeded: false, pair: null };
    }
    persistTokenPair(pair as TokenPair);
    return { succeeded: true, pair: pair as TokenPair };
  } catch {
    expireSessionIfCurrent(generation, refreshToken);
    return { succeeded: false, pair: null };
  }
}

/** Refresh callers share one request, preventing a burst of 401s rotating one token repeatedly. */
export function refreshSession(): Promise<boolean> {
  const generation = sessionGeneration;
  const existing = refreshInFlight;
  if (existing?.generation === generation) {
    return existing.promise.then((outcome) => outcome.succeeded);
  }

  const refreshToken = getRefreshToken();
  const flight: RefreshFlight = {
    generation,
    promise: Promise.resolve({ succeeded: false, pair: null }),
  };
  refreshInFlight = flight;
  flight.promise = refreshSessionRequest(generation, refreshToken).finally(() => {
    if (refreshInFlight === flight) refreshInFlight = null;
  });
  return flight.promise.then((outcome) => outcome.succeeded);
}

function isAuthEndpoint(input: RequestInfo | URL): boolean {
  const raw = typeof input === "string" ? input : input instanceof URL ? input.href : input.url;
  try {
    const pathname = new URL(
      raw,
      typeof window === "undefined" ? "http://localhost" : window.location.href,
    ).pathname;
    return AUTH_PATHS_WITHOUT_REFRESH.has(pathname);
  } catch {
    return false;
  }
}

/**
 * Adds the current bearer token and retries one 401 after refreshing. 403 is never
 * refreshed. Bodies are replayed once; request callers use JSON/text bodies.
 */
function headerRecord(headers?: HeadersInit): Record<string, string> {
  if (!headers) return {};
  if (typeof Headers !== "undefined" && headers instanceof Headers) {
    return Object.fromEntries(headers.entries());
  }
  if (Array.isArray(headers)) return Object.fromEntries(headers);
  return { ...(headers as Record<string, string>) };
}

function setHeader(headers: Record<string, string>, name: string, value: string): void {
  const existing = Object.keys(headers).find((key) => key.toLowerCase() === name.toLowerCase());
  if (existing) delete headers[existing];
  headers[name] = value;
}

function deleteHeader(headers: Record<string, string>, name: string): void {
  const existing = Object.keys(headers).find((key) => key.toLowerCase() === name.toLowerCase());
  if (existing) delete headers[existing];
}

export async function sessionFetch(
  input: RequestInfo | URL,
  init: RequestInit = {},
): Promise<Response> {
  const requestGeneration = sessionGeneration;
  const accessTokenAtRequest = getAccessToken();
  const requestBase = typeof Request !== "undefined" && input instanceof Request ? input.clone() : input;
  const requestHeaders =
    typeof Request !== "undefined" && requestBase instanceof Request
      ? headerRecord(requestBase.headers)
      : {};
  const buildInit = (retry: boolean): RequestInit => {
    const headers = { ...requestHeaders };
    for (const [key, value] of Object.entries(headerRecord(init.headers))) {
      setHeader(headers, key, value);
    }
    if (retry) {
      const token = getAccessToken();
      if (token) setHeader(headers, "Authorization", `Bearer ${token}`);
      else deleteHeader(headers, "Authorization");
    } else if (!Object.keys(headers).some((key) => key.toLowerCase() === "authorization")) {
      const token = getAccessToken();
      if (token) setHeader(headers, "Authorization", `Bearer ${token}`);
    }
    return { ...init, headers };
  };
  const send = (retry: boolean) => {
    const request =
      typeof Request !== "undefined" && requestBase instanceof Request
        ? requestBase.clone()
        : requestBase;
    return fetch(request, buildInit(retry));
  };

  const response = await send(false);
  if (response.status !== 401 || isAuthEndpoint(input)) return response;
  if (sessionGeneration !== requestGeneration) return response;

  // A concurrent request may already have rotated this session's access token.
  // Retry with it instead of rotating the refresh token a second time.
  const accessTokenChanged = getAccessToken() !== accessTokenAtRequest;
  const canRetry = accessTokenChanged
    ? Boolean(getAccessToken())
    : await refreshSession();
  if (!canRetry || sessionGeneration !== requestGeneration) return response;

  const retryAccessToken = getAccessToken();
  const retried = await send(true);
  if (
    retried.status === 401 &&
    sessionGeneration === requestGeneration &&
    getAccessToken() === retryAccessToken
  ) {
    clearSession();
    sessionExpired();
  }
  return retried;
}

/** Always clears the local session; the result tells the UI whether server revocation was confirmed. */
export async function logoutSession(refreshTokenOverride?: string): Promise<boolean> {
  const refreshToken = refreshTokenOverride ?? getRefreshToken();
  // Remove browser credentials synchronously; server revocation may be slow or fail.
  clearSession();
  if (!refreshToken) return false;
  try {
    const response = await fetch(`${API_BASE}/auth/logout`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh_token: refreshToken }),
    });
    return response.ok;
  } catch {
    return false;
  }
}
