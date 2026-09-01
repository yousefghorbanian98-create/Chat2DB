export type HealthState = 'ready' | 'degraded' | 'missing'
export type Stage = 'Thinking' | 'Grep' | 'Read' | 'Edit' | 'Done'

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
  category: string
  what: string
  transport: string
  target: string
  enabled?: boolean
}

export interface Usage {
  promptTokens: number
  completionTokens: number
  costUsd: number
  runs: number
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

export interface RunEvent {
  type: 'stage' | 'skills' | 'token' | 'result' | 'error' | 'done'
  stage?: Stage
  text?: string
  skills?: string[]
  payload?: { skills?: string[]; dispatched?: boolean }
}

/** نگاشتِ مرحله به توکنِ رنگِ DESIGN.md */
export const STAGE_TOKEN: Record<Stage, string> = {
  Thinking: 'thinking',
  Grep: 'grep',
  Read: 'read',
  Edit: 'edit',
  Done: 'done',
}
