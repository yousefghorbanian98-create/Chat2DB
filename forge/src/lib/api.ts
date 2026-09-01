import type { Agent, Command, McpServer, RunEvent, Session, Usage } from './types.ts'

const BASE = '/api'

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE}${path}`)
  if (!res.ok) throw new Error(`${path} → ${res.status}`)
  return (await res.json()) as T
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
