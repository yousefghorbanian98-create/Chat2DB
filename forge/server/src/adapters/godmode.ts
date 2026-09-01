import { readdir, readFile } from 'node:fs/promises'
import { join } from 'node:path'
import { config } from '../config'
import type { AdapterStatus, Agent, Command } from '../types'
import type { Adapter } from './types'

/**
 * لایهٔ گردش‌کار — Godmode.
 * SOURCE: https://github.com/patrickking67/godmode (Apache-2.0)
 * فایل‌ها در forge/skills/ وِندور شده‌اند (۹ دستور، ۵ ساب‌ایجنت).
 *
 * این Adapter فقط از دیسک می‌خواند؛ هیچ وابستگیِ خارجی ندارد،
 * بنابراین همیشه ready است (مگر اینکه پوشه پاک شده باشد).
 */

interface FrontMatter {
  name?: string
  description?: string
  [k: string]: string | undefined
}

const SOURCE_URL = 'https://github.com/patrickking67/godmode (Apache-2.0)'

function parseFrontMatter(raw: string): { meta: FrontMatter; body: string } {
  const m = /^---\r?\n([\s\S]*?)\r?\n---\r?\n?([\s\S]*)$/.exec(raw)
  if (!m) return { meta: {}, body: raw }
  const meta: FrontMatter = {}
  for (const line of m[1].split(/\r?\n/)) {
    const idx = line.indexOf(':')
    if (idx === -1) continue
    const key = line.slice(0, idx).trim()
    const value = line.slice(idx + 1).trim().replace(/^["']|["']$/g, '')
    if (key) meta[key] = value
  }
  return { meta, body: m[2].trim() }
}

export class GodmodeAdapter implements Adapter {
  readonly name = 'godmode'
  private commands: Command[] = []
  private agents: Agent[] = []

  private async loadDir<T>(dir: string, kind: 'command' | 'agent'): Promise<T[]> {
    const out: unknown[] = []
    let entries: string[] = []
    try {
      entries = (await readdir(dir)).filter((f) => f.endsWith('.md'))
    } catch {
      return out as T[]
    }
    for (const file of entries) {
      const path = join(dir, file)
      const raw = await readFile(path, 'utf8')
      const { meta, body } = parseFrontMatter(raw)
      const slug = file.replace(/\.md$/, '')
      out.push({
        slug,
        name: meta.name ?? slug,
        description: meta.description ?? '',
        body,
        path,
        source: SOURCE_URL,
        kind,
      })
    }
    return out as T[]
  }

  async load(): Promise<void> {
    this.commands = await this.loadDir<Command>(join(config.skillsDir, 'commands'), 'command')
    this.agents = await this.loadDir<Agent>(join(config.skillsDir, 'agents'), 'agent')
  }

  listCommands(): Command[] {
    return this.commands
  }

  listAgents(): Agent[] {
    return this.agents
  }

  findCommand(slug: string): Command | undefined {
    return this.commands.find((c) => c.slug === slug)
  }

  async health(): Promise<AdapterStatus> {
    if (!this.commands.length) await this.load()
    if (!this.commands.length) {
      return {
        name: this.name,
        state: 'missing',
        detail: `هیچ دستوری در ${config.skillsDir} یافت نشد`,
      }
    }
    return {
      name: this.name,
      state: 'ready',
      detail: `${this.commands.length} دستور · ${this.agents.length} ساب‌ایجنت`,
    }
  }
}
