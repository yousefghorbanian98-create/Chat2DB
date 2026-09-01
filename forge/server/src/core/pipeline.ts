import type { JcodeAdapter } from '../adapters/jcode'
import type { SoupAdapter } from '../adapters/soup'
import type { GodmodeAdapter } from '../adapters/godmode'
import type { RunEvent, Skill } from '../types'

/**
 * پایپ‌لاین: Soup (انتخاب skill) → Godmode (اگر دستور صدا زده شده) → Jcode (اجرا)
 *
 * مراحلِ نمایش‌داده‌شده در UI با امضای بصریِ DESIGN.md (۵ پاستیل) یکی است،
 * اما هر مرحله دقیقاً همان کاری را می‌گوید که در واقعیت انجام می‌شود:
 *   Thinking = تحلیلِ درخواست
 *   Grep     = جستجو در فهرستِ skillها
 *   Read     = بارگذاریِ skillهای انتخاب‌شده
 *   Edit     = ارسال به jcode
 *   Done     = پایان
 */
export class Pipeline {
  constructor(
    private readonly soup: SoupAdapter,
    private readonly godmode: GodmodeAdapter,
    private readonly jcode: JcodeAdapter,
  ) {}

  /** استخراجِ دستورِ صریح (مثل /genesis) از ابتدای پیام */
  private extractCommand(prompt: string): string | null {
    const m = /^\/([a-zA-Z-]+)/.exec(prompt.trim())
    if (!m) return null
    return this.godmode.findCommand(m[1]) ? m[1] : null
  }

  private estimateTokens(text: string): number {
    return Math.max(1, Math.ceil(text.length / 4))
  }

  async *run(prompt: string): AsyncGenerator<RunEvent> {
    yield { type: 'stage', stage: 'Thinking', text: 'تحلیل درخواست…' }

    const explicit = this.extractCommand(prompt)
    if (explicit) {
      yield { type: 'stage', stage: 'Grep', text: `دستور صریح شناسایی شد: /${explicit}` }
    } else {
      yield { type: 'stage', stage: 'Grep', text: 'جستجو در فهرست skillها…' }
    }

    const selected: Skill[] = explicit
      ? (this.godmode.findCommand(explicit)
          ? [
              {
                name: explicit,
                description: this.godmode.findCommand(explicit)!.description,
                instructions: this.godmode.findCommand(explicit)!.body,
                tags: ['command'],
                source: this.godmode.findCommand(explicit)!.source,
              },
            ]
          : [])
      : this.soup.prepare(prompt)

    yield {
      type: 'skills',
      skills: selected.map((s) => s.name),
      text: selected.length ? `${selected.length} skill انتخاب شد` : 'هیچ skill مرتبطی یافت نشد',
    }

    yield { type: 'stage', stage: 'Read', text: 'بارگذاری skillهای انتخاب‌شده…' }

    const contextBlock = selected.length
      ? selected.map((s) => `## ${s.name}\n${s.instructions}`).join('\n\n')
      : '(بدون skill مرتبط)'

    const composed = [
      '# زمینه (از لایهٔ Soup)',
      contextBlock,
      '',
      '# درخواست',
      prompt,
    ].join('\n')

    yield { type: 'token', text: String(this.estimateTokens(composed)) }

    yield { type: 'stage', stage: 'Edit', text: 'ارسال به هستهٔ اجرا…' }

    const state = await this.jcode.health()

    let answer: string
    if (state.state === 'ready') {
      const result = await this.jcode.run(prompt)
      answer = result.ok
        ? result.output
        : `اجرا ناموفق بود (${result.reason ?? 'خطای ناشناخته'}).\n\n${result.output}`
      yield { type: 'result', text: answer }
    } else {
      // حالت degraded — خروجی واقعی تولید نمی‌شود، فقط نشان می‌دهیم چه ارسال می‌شد.
      answer = [
        '**هستهٔ اجرا (jcode) در دسترس نیست** — بنابراین پاسخی از مدل تولید نشد.',
        '',
        'برای اینکه برنامه صادق بماند، به‌جای نمایش خروجیِ ساختگی،',
        'پرامپتی که ساخته شده نمایش داده می‌شود:',
        '',
        '```',
        composed,
        '```',
      ].join('\n')
      yield { type: 'result', text: answer }
    }

    yield { type: 'stage', stage: 'Done', text: 'پایان' }
    yield { type: 'done', payload: { skills: selected.map((s) => s.name), dispatched: state.state === 'ready' } }
  }
}
