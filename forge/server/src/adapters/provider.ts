/**
 * اتصال به مدل — «مغزِ» برنامه.
 *
 * تا پیش از این Forge هیچ تماسی با هیچ مدلی نداشت و فقط منتظرِ jcode بود؛
 * یعنی اگر jcode نصب نبود، کلِ خروجیِ برنامه صفر بود. اینجا دو خانواده‌ی
 * استاندارد پشتیبانی می‌شوند:
 *
 *   · openai-compatible — OpenAI و هر سازگار (Groq، OpenRouter، Ollama، LM Studio)
 *   · anthropic         — Messages API
 *
 * کلید فقط در settings.json روی دستگاهِ کاربر می‌ماند و تنها به همان
 * پایگاهی فرستاده می‌شود که خودش تعیین کرده است.
 */
import type { AdapterStatus, ProviderConfig } from '../types'
import type { Adapter } from './types'

export interface ProviderResult {
  text: string
  /** اگر پایگاه شمارش واقعی بفرستد؛ در غیر این صورت null یعنی «نامعلوم» */
  promptTokens: number | null
  completionTokens: number | null
}

export interface ProviderMessage {
  role: 'user' | 'assistant' | 'system'
  content: string
}

const ANTHROPIC_VERSION = '2023-06-01'

export class ProviderAdapter implements Adapter {
  readonly name = 'provider'

  constructor(private config: ProviderConfig | null = null) {}

  setConfig(config: ProviderConfig | null): void {
    this.config = config
  }

  private get baseUrl(): string {
    return this.config?.baseUrl ?? ''
  }

  async health(): Promise<AdapterStatus> {
    if (!this.config) {
      return {
        name: this.name,
        state: 'missing',
        detail: 'هیچ مدلی پیکربندی نشده — از تنظیمات یک مدل اضافه کنید',
      }
    }
    return {
      name: this.name,
      state: 'ready',
      detail: `${this.config.model} · ${new URL(this.baseUrl).host}`,
    }
  }

  /** بررسیِ سبکِ اتصال — فقط برای دکمه‌ی «تستِ اتصال» در تنظیمات */
  async ping(): Promise<{ ok: boolean; message: string }> {
    if (!this.config) return { ok: false, message: 'مدلی پیکربندی نشده است' }
    try {
      const result = await this.complete([
        { role: 'user', content: 'پاسخ فقط یک کلمه: ok' },
      ])
      return { ok: result.text.trim().length > 0, message: result.text.trim().slice(0, 120) }
    } catch (err) {
      return { ok: false, message: err instanceof Error ? err.message : 'خطای ناشناخته' }
    }
  }

  async complete(messages: ProviderMessage[]): Promise<ProviderResult> {
    if (!this.config) throw new Error('مدلی پیکربندی نشده است')
    return this.config.type === 'anthropic'
      ? this.completeAnthropic(messages)
      : this.completeOpenAI(messages)
  }

  /* ──────────────── OpenAI-compatible ──────────────── */

  private async completeOpenAI(messages: ProviderMessage[]): Promise<ProviderResult> {
    const cfg = this.config!
    const res = await fetch(`${cfg.baseUrl}/chat/completions`, {
      method: 'POST',
      headers: {
        'content-type': 'application/json',
        authorization: `Bearer ${cfg.apiKey}`,
      },
      body: JSON.stringify({
        model: cfg.model,
        messages,
        stream: true,
        stream_options: { include_usage: true },
      }),
    })

    if (!res.ok || !res.body) {
      const body = await res.text().catch(() => '')
      throw new Error(`پایگاه پاسخ نداد (${res.status}) ${body.slice(0, 180)}`)
    }

    let text = ''
    let promptTokens: number | null = null
    let completionTokens: number | null = null

    // stream_options فقط وقتی usage می‌فرستد که درخواستِ پایگاه پشتیبانی کند
    for await (const payload of readSse(res.body)) {
      if (payload === '[DONE]') break
      try {
        const json = JSON.parse(payload) as {
          choices?: Array<{ delta?: { content?: string } }>
          usage?: { prompt_tokens?: number; completion_tokens?: number }
        }
        const delta = json.choices?.[0]?.delta?.content
        if (delta) text += delta
        if (json.usage?.prompt_tokens != null) promptTokens = json.usage.prompt_tokens
        if (json.usage?.completion_tokens != null) completionTokens = json.usage.completion_tokens
      } catch {
        // بسته‌ی ناقص را نادیده بگیر
      }
    }

    return { text, promptTokens, completionTokens }
  }

  /* ──────────────── Anthropic ──────────────── */

  private async completeAnthropic(messages: ProviderMessage[]): Promise<ProviderResult> {
    const cfg = this.config!
    const system = messages
      .filter((m) => m.role === 'system')
      .map((m) => m.content)
      .join('\n\n')

    const rest = messages.filter((m) => m.role !== 'system')

    const res = await fetch(`${cfg.baseUrl}/v1/messages`, {
      method: 'POST',
      headers: {
        'content-type': 'application/json',
        'x-api-key': cfg.apiKey,
        'anthropic-version': ANTHROPIC_VERSION,
      },
      body: JSON.stringify({
        model: cfg.model,
        max_tokens: 4096,
        system: system || undefined,
        messages: rest.map((m) => ({ role: m.role, content: m.content })),
        stream: true,
      }),
    })

    if (!res.ok || !res.body) {
      const body = await res.text().catch(() => '')
      throw new Error(`پایگاه پاسخ نداد (${res.status}) ${body.slice(0, 180)}`)
    }

    let text = ''
    let promptTokens: number | null = null
    let completionTokens: number | null = null

    for await (const payload of readSse(res.body)) {
      try {
        const json = JSON.parse(payload) as {
          type?: string
          delta?: { type?: string; text?: string }
          usage?: { input_tokens?: number; output_tokens?: number }
          message?: { usage?: { input_tokens?: number; output_tokens?: number } }
        }
        if (json.type === 'content_block_delta' && json.delta?.text) text += json.delta.text
        if (json.usage?.input_tokens != null) promptTokens = json.usage.input_tokens
        if (json.usage?.output_tokens != null) completionTokens = json.usage.output_tokens
        if (json.message?.usage?.output_tokens != null) {
          completionTokens = json.message.usage.output_tokens
          promptTokens = json.message.usage.input_tokens ?? promptTokens
        }
      } catch {
        // نادیده گرفتنِ بسته‌ی ناقص
      }
    }

    return { text, promptTokens, completionTokens }
  }
}

/** خواندنِ جریانِ SSE از پاسخِ fetch */
export async function* readSse(body: ReadableStream<Uint8Array>): AsyncGenerator<string> {
  const reader = body.getReader()
  const decoder = new TextDecoder()
  let buffer = ''

  while (true) {
    const { done, value } = await reader.read()
    if (done) break
    buffer += decoder.decode(value, { stream: true })

    let index: number
    while ((index = buffer.indexOf('\n\n')) !== -1) {
      const chunk = buffer.slice(0, index)
      buffer = buffer.slice(index + 2)
      for (const line of chunk.split('\n')) {
        const trimmed = line.trim()
        if (!trimmed.startsWith('data:')) continue
        const data = trimmed.slice(5).trim()
        if (data) yield data
      }
    }
  }
}
