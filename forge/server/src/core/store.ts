import { mkdir, readFile, writeFile } from 'node:fs/promises'
import { join } from 'node:path'
import { randomUUID } from 'node:crypto'
import { config } from '../config'
import type { Message, Session, Usage } from '../types'

/**
 * انبارِ محلی — فایل JSON.
 *
 * تصمیمِ ثبت‌شده: به‌جای SQLite از فایل JSON استفاده شد.
 * دلیل: هیچ وابستگیِ بومی (native) معرفی نشود تا بیلد روی runner ویندوزی
 * قطعی و بدون کامپایل باشد. رابطِ Store طوری نوشته شده که بعداً بتوان
 * SQLite را بدون تغییر در لایه‌های بالاتر جایگزین کرد.
 */
interface DbShape {
  sessions: Session[]
  usage: Usage
}

const EMPTY: DbShape = {
  sessions: [],
  usage: { promptTokens: 0, completionTokens: 0, costUsd: 0, runs: 0 },
}

export class Store {
  private db: DbShape = structuredClone(EMPTY)
  private loaded = false
  private readonly file: string

  constructor(dataDir: string = config.dataDir) {
    this.file = join(dataDir, 'forge.json')
  }

  private async ensure(): Promise<void> {
    if (this.loaded) return
    try {
      await mkdir(config.dataDir, { recursive: true })
    } catch {
      // اگر نتوانستیم بسازیم، فقط در حافظه کار می‌کنیم
    }
    try {
      const raw = await readFile(this.file, 'utf8')
      const parsed = JSON.parse(raw) as Partial<DbShape>
      this.db = {
        sessions: Array.isArray(parsed.sessions) ? parsed.sessions : [],
        usage: { ...EMPTY.usage, ...(parsed.usage ?? {}) },
      }
    } catch {
      this.db = structuredClone(EMPTY)
    }
    this.loaded = true
  }

  private async flush(): Promise<void> {
    try {
      await writeFile(this.file, JSON.stringify(this.db, null, 2), 'utf8')
    } catch {
      // ذخیره‌سازی نباید باعث شکستِ پاسخ شود
    }
  }

  async listSessions(): Promise<Session[]> {
    await this.ensure()
    return [...this.db.sessions].sort((a, b) => b.createdAt.localeCompare(a.createdAt))
  }

  async createSession(title = 'نشست جدید'): Promise<Session> {
    await this.ensure()
    const session: Session = {
      id: randomUUID(),
      title,
      createdAt: new Date().toISOString(),
      messages: [],
    }
    this.db.sessions.push(session)
    await this.flush()
    return session
  }

  async getSession(id: string): Promise<Session | null> {
    await this.ensure()
    return this.db.sessions.find((s) => s.id === id) ?? null
  }

  async appendMessage(sessionId: string, message: Omit<Message, 'id' | 'at'>): Promise<Message | null> {
    await this.ensure()
    const session = this.db.sessions.find((s) => s.id === sessionId)
    if (!session) return null
    const full: Message = { ...message, id: randomUUID(), at: new Date().toISOString() }
    session.messages.push(full)
    if (session.messages.length === 1 && message.role === 'user') {
      session.title = message.text.slice(0, 48)
    }
    await this.flush()
    return full
  }

  async addUsage(promptTokens: number, completionTokens: number): Promise<Usage> {
    await this.ensure()
    this.db.usage.promptTokens += promptTokens
    this.db.usage.completionTokens += completionTokens
    this.db.usage.runs += 1
    await this.flush()
    return this.db.usage
  }

  async getUsage(): Promise<Usage> {
    await this.ensure()
    return this.db.usage
  }
}
