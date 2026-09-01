/**
 * تنظیماتِ ماندگار برنامه.
 *
 * تا پیش از این برنامه هیچ تنظیمی نداشت: نه می‌دانست کدام پوشه مقصدِ کار است،
 * نه می‌شد به مدلی وصلش کرد. برای همین «مغز» عملاً کاری نمی‌کرد.
 * اینجا هردو نگه داشته می‌شوند — روی دیسکِ خودِ کاربر.
 */
import { readFile, writeFile, mkdir } from 'node:fs/promises'
import { dirname, resolve } from 'node:path'
import { config } from '../config'
import type { ProviderConfig, Settings } from '../types'

const FILE = resolve(config.dataDir, 'settings.json')

export const DEFAULT_SETTINGS: Settings = {
  workspaceDir: null,
  provider: null,
  mcpEnabled: [],
  jcodePath: null,
}

export function normalizeProvider(raw: unknown): ProviderConfig | null {
  if (!raw || typeof raw !== 'object') return null
  const p = raw as Partial<ProviderConfig>
  const type = p.type === 'anthropic' ? 'anthropic' : 'openai-compatible'
  const model = typeof p.model === 'string' ? p.model.trim() : ''
  const apiKey = typeof p.apiKey === 'string' ? p.apiKey.trim() : ''
  const baseUrl =
    typeof p.baseUrl === 'string' && p.baseUrl.trim()
      ? p.baseUrl.trim().replace(/\/+$/, '')
      : type === 'anthropic'
        ? 'https://api.anthropic.com'
        : 'https://api.openai.com/v1'

  // بدونِ مدل و کلید عملاً اتصالی نیست
  if (!model || !apiKey) return null
  return { type, baseUrl, model, apiKey }
}

export async function loadSettings(): Promise<Settings> {
  try {
    const raw = JSON.parse(await readFile(FILE, 'utf8')) as Partial<Settings>
    return {
      workspaceDir: typeof raw.workspaceDir === 'string' && raw.workspaceDir ? raw.workspaceDir : null,
      provider: normalizeProvider(raw.provider),
      mcpEnabled: Array.isArray(raw.mcpEnabled) ? raw.mcpEnabled.filter((x) => typeof x === 'string') : [],
      jcodePath: typeof raw.jcodePath === 'string' && raw.jcodePath ? raw.jcodePath : null,
    }
  } catch {
    return { ...DEFAULT_SETTINGS }
  }
}

export async function saveSettings(next: Settings): Promise<Settings> {
  await mkdir(dirname(FILE), { recursive: true })
  await writeFile(FILE, JSON.stringify(next, null, 2), 'utf8')
  return next
}

/** به‌روزرسانیِ جزئی — فقط کلیدهای داده‌شده عوض می‌شوند */
/** اگر کاربر کلید را خالی/‏‎__KEEP__‎ بفرستد یعنی «همان کلیدِ قبلی را نگه دار» */
const KEEP = '__KEEP__'

export async function patchSettings(patch: Partial<Settings>): Promise<Settings> {
  const current = await loadSettings()
  let provider = current.provider

  if (patch.provider !== undefined) {
    if (patch.provider === null) {
      provider = null
    } else {
      const incoming = { ...patch.provider }
      if (!incoming.apiKey || incoming.apiKey === KEEP) {
        incoming.apiKey = current.provider?.apiKey ?? ''
      }
      provider = normalizeProvider(incoming)
    }
  }

  const next: Settings = {
    ...current,
    ...patch,
    provider,
    mcpEnabled: patch.mcpEnabled ?? current.mcpEnabled,
  }
  return saveSettings(next)
}
