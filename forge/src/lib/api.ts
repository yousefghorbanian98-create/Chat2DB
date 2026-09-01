import type { Agent, Command, McpServer, RunEvent, Session, Usage } from './types.ts'

const BASE = '/api'

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE}${path}`)
  if (!res.ok) throw new Error(`${path} → ${res.status}`)
  return (await res.json()) as T
}

export interface UpdateCheck {
  enabled: boolean
  current: { version: string; build: string } | null
  latest: { version: string; build: string; generatedAt: string } | null
  upToDate: boolean
  changed: string[]
  removed: string[]
  deltaBytes: number
  fullBytes: number
  restartRequired: boolean
  error?: string
}

export interface UpdateApply {
  ok: boolean
  applied: number
  removed: number
  restartRequired: boolean
  reloadSufficient: boolean
  error?: string
}

export interface HealthResponse {
  ok: boolean
  service: string
  version: string
  port: number
  skillsDir: string
  adapters: Array<{ name: string; state: 'ready' | 'degraded' | 'missing'; detail: string }>
}

export const api = {
  health: () => get<HealthResponse>('/health'),
  sessions: () => get<Session[]>('/sessions'),
  createSession: async (title: string) => {
    const res = await fetch(`${BASE}/sessions`, {
      method: 'POST',
      headers: { 'content-type': 'application/json' },
      body: JSON.stringify({ title }),
    })
    if (!res.ok) throw new Error('create session failed')
    return (await res.json()) as Session
  },
  session: (id: string) => get<Session>(`/sessions/${id}`),
  commands: () => get<Command[]>('/commands'),
  agents: () => get<Agent[]>('/agents'),
  mcp: () => get<Array<McpServer & { enabled: boolean }>>('/mcp'),
  usage: () => get<Usage>('/usage'),
  route: (q: string) => get<Array<{ name: string; score: number }>>(`/route?q=${encodeURIComponent(q)}`),
  updateCheck: () => get<UpdateCheck>('/update/check'),
  updateApply: async () => {
    const res = await fetch(`${BASE}/update/apply`, { method: 'POST' })
    if (!res.ok) throw new Error(`update/apply → ${res.status}`)
    return (await res.json()) as UpdateApply
  },
}

/**
 * اجرای جریانی (SSE).
 * تابعِ برگشتی برای بستنِ اتصال است — قطعِ تمیز هنگامِ unmount.
 */
export function runStream(
  prompt: string,
  sessionId: string | null,
  onEvent: (event: RunEvent) => void,
): () => void {
  const url = `${BASE}/run?prompt=${encodeURIComponent(prompt)}${
    sessionId ? `&sessionId=${encodeURIComponent(sessionId)}` : ''
  }`
  const source = new EventSource(url)

  source.onmessage = (ev) => {
    try {
      onEvent(JSON.parse(ev.data) as RunEvent)
    } catch {
      // رویدادِ ناقص را نادیده بگیر — جریان ادامه می‌یابد
    }
  }

  source.onerror = () => {
    // پایانِ طبیعیِ جریان هم با onerror گزارش می‌شود؛ اتصال را می‌بندیم
    source.close()
  }

  return () => source.close()
}
