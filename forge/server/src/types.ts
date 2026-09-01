export type HealthState = 'ready' | 'degraded' | 'missing'

export interface AdapterStatus {
  name: string
  state: HealthState
  detail: string
}

export type Stage = 'Thinking' | 'Grep' | 'Read' | 'Edit' | 'Done'

export interface Skill {
  name: string
  description: string
  instructions: string
  tags: string[]
  examples?: string[]
  source?: string
}

export interface Command {
  slug: string
  name: string
  description: string
  body: string
  path: string
  source: string
}

export interface Agent {
  slug: string
  name: string
  description: string
  body: string
  path: string
  source: string
}

export interface McpServer {
  id: string
  name: string
  category: 'Docs' | 'Code intelligence' | 'Browser' | 'Cloud'
  what: string
  transport: 'npx' | 'http'
  target: string
}

export interface Message {
  id: string
  role: 'user' | 'agent' | 'system'
  text: string
  at: string
  stage?: Stage
  skills?: string[]
}

export interface Session {
  id: string
  title: string
  createdAt: string
  messages: Message[]
}

export interface Usage {
  promptTokens: number
  completionTokens: number
  costUsd: number
  runs: number
}

export interface RunEvent {
  type: 'stage' | 'skills' | 'token' | 'result' | 'error' | 'done'
  stage?: Stage
  text?: string
  skills?: string[]
  payload?: unknown
}

/* ────────────────────────────────────────────────────────────
 * تنظیماتِ برنامه (تا پیش از این اصلاً وجود نداشت)
 * ──────────────────────────────────────────────────────────── */

/** اتصال به مدل — «مغز»ی که Forge بدون آن فقط پوسته است */
export interface ProviderConfig {
  /** openai-compatible: OpenAI و هر سازگار (Groq، OpenRouter، Ollama، LM Studio) */
  type: 'openai-compatible' | 'anthropic'
  baseUrl: string
  model: string
  /** فقط روی همین دستگاه و در همین فایل نگه داشته می‌شود؛ جایی ارسال نمی‌شود */
  apiKey: string
}

export interface Settings {
  /** پوشه‌ای که عامل روی آن کار می‌کند — بدون آن اجرا بی‌معناست */
  workspaceDir: string | null
  provider: ProviderConfig | null
  mcpEnabled: string[]
  jcodePath: string | null
}

export interface RunOptions {
  workspaceDir?: string | null
}
