import type { JcodeAdapter } from '../adapters/jcode'
import type { SoupAdapter } from '../adapters/soup'
import type { GodmodeAdapter } from '../adapters/godmode'
import type { ProviderAdapter } from '../adapters/provider'
import type { RunEvent, Settings, Skill } from '../types'

/**
 * پایپ‌لاین — مغزِ برنامه.
 *
 * سه حفره‌ی پیشین اینجا بود و بسته شد:
 *  ۱) هیچ «پروژه‌ای» انتخاب نمی‌شد → عامل روی پوشه‌ی خودِ برنامه کار می‌کرد.
 *     حالا مسیر از تنظیمات خوانده می‌شود و به jcode هم منتقل می‌شود.
 *  ۲) زمینه‌ای که از مهارت‌ها ساخته می‌شد دور ریخته می‌شد؛ فقط متنِ خامِ
 *     کاربر فرستاده می‌شد. حالا همان زمینه به مدل/عامل می‌رود.
 *  ۳) بدون jcode هیچ خروجی‌ای تولید نمی‌شد. حالا اگر مدلی پیکربندی شده باشد،
 *     خودِ Forge با آن تماس می‌گیرد.
 *
 * مراحلِ نمایش‌داده‌شده با امضای بصریِ DESIGN.md (۵ پاستیل) یکی است و هر مرحله
 * همان کاری را می‌گوید که واقعاً انجام می‌شود.
 */
export class Pipeline {
  constructor(
    private readonly soup: SoupAdapter,
    private readonly godmode: GodmodeAdapter,
    private readonly jcode: JcodeAdapter,
    private readonly provider: ProviderAdapter,
    private readonly getSettings: () => Settings,
  ) {}

  /** استخراجِ دستورِ صریح (مثل /genesis) از ابتدای پیام */
  private extractCommand(prompt: string): string | null {
    const m = /^\/([a-zA-Z-]+)/.exec(prompt.trim())
    if (!m) return null
    return this.godmode.findCommand(m[1]) ? m[1] : null
  }

  private buildSystemPrompt(skills: Skill[], workspace: string | null): string {
    const parts: string[] = [
      'تو «Forge» هستی — یک دستیارِ کدنویسی که روی دستگاهِ کاربر اجرا می‌شود.',
      workspace
        ? `پوشه‌ی پروژه‌ی کاربر: ${workspace} — هر مسیری می‌دهی نسبی به همین پوشه باشد.`
        : 'هیچ پوشه‌ی پروژه‌ای انتخاب نشده؛ از کاربر بخواه از تنظیمات یکی انتخاب کند.',
      '',
    ]
    if (skills.length) {
      parts.push('دستورالعمل‌های مهارت‌های انتخاب‌شده (از فهرستِ مهارتِ Forge):', '')
      for (const s of skills) parts.push(`## ${s.name}\n${s.instructions}`, '')
    }
    parts.push('پاسخ را به همان زبانی بده که کاربر پرسیده. کد را در بلوکِ ``` بگذار.')
    return parts.join('\n')
  }

  async *run(prompt: string): AsyncGenerator<RunEvent> {
    yield { type: 'stage', stage: 'Thinking', text: 'تحلیل درخواست…' }

    const settings = this.getSettings()
    const workspace = settings.workspaceDir

    const explicit = this.extractCommand(prompt)
    if (explicit) {
      yield { type: 'stage', stage: 'Grep', text: `دستور صریح شناسایی شد: /${explicit}` }
    } else {
      yield { type: 'stage', stage: 'Grep', text: 'جستجو در فهرست skillها…' }
    }

    const selected: Skill[] = explicit
      ? (() => {
          const cmd = this.godmode.findCommand(explicit)
          return cmd
            ? [
                {
                  name: cmd.slug,
                  description: cmd.description,
                  instructions: cmd.body,
                  tags: ['command'],
                  source: cmd.source,
                },
              ]
            : []
        })()
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

    const systemPrompt = this.buildSystemPrompt(selected, workspace)
    const composed = [
      '# زمینه (از لایهٔ مهارت‌ها)',
      contextBlock,
      '',
      '# درخواست',
      prompt,
    ].join('\n')

    // تخمین — شفاف می‌گوییم تخمین است، نه عددِ واقعی
    const estimated = Math.max(1, Math.ceil(composed.length / 4))
    yield { type: 'token', text: String(estimated) }

    const providerState = await this.provider.health()
    const jcodeState = await this.jcode.health()

    if (providerState.state === 'ready') {
      yield {
        type: 'stage',
        stage: 'Edit',
        text: `ارسال به مدل (${settings.provider?.model ?? 'مدل'})…`,
      }
      try {
        const result = await this.provider.complete([
          { role: 'system', content: systemPrompt },
          { role: 'user', content: composed },
        ])
        yield { type: 'result', text: result.text || '(پاسخی دریافت نشد)' }
        // اگر پایگاه شمارش واقعی داده باشد، همان را جایگزینِ تخمین می‌کنیم
        if (result.promptTokens != null) {
          yield { type: 'token', text: String(result.promptTokens) }
        }
        yield { type: 'stage', stage: 'Done', text: 'پایان' }
        yield {
          type: 'done',
          payload: { skills: selected.map((s) => s.name), dispatched: true },
        }
        return
      } catch (err) {
        // خطای مدل را پنهان نمی‌کنیم، اما مسیرِ جایگزین را امتحان می‌کنیم
        const message = err instanceof Error ? err.message : 'خطای ناشناخته'
        yield { type: 'error', text: `خطا در تماس با مدل: ${message}` }
        if (jcodeState.state !== 'ready') {
          yield { type: 'stage', stage: 'Done', text: 'پایان' }
          yield { type: 'done', payload: { skills: selected.map((s) => s.name), dispatched: false } }
          return
        }
      }
    }

    if (jcodeState.state === 'ready') {
      yield { type: 'stage', stage: 'Edit', text: 'ارسال به هستهٔ اجرا (jcode)…' }
      // زمینه‌ی کامل را می‌فرستیم (قبلاً فقط متنِ خام می‌رفت) و در پوشه‌ی پروژه اجرا می‌کنیم
      const result = await this.jcode.run(composed, { cwd: workspace ?? undefined })
      yield {
        type: 'result',
        text: result.ok
          ? result.output
          : `اجرا ناموفق بود (${result.reason ?? 'خطای ناشناخته'}).\n\n${result.output}`,
      }
      yield { type: 'stage', stage: 'Done', text: 'پایان' }
      yield { type: 'done', payload: { skills: selected.map((s) => s.name), dispatched: true } }
      return
    }

    // هیچ مغزی وصل نیست — صادقانه می‌گوییم و به‌جای خروجیِ ساختگی،
    // همان چیزی را نشان می‌دهیم که قرار بود فرستاده شود
    yield { type: 'stage', stage: 'Edit', text: 'هیچ هسته‌ی اجرایی در دسترس نیست' }
    const answer = [
      '**هیچ مغزی وصل نیست** — نه مدلی پیکربندی شده و نه `jcode` در دسترس است،',
      'بنابراین پاسخی از مدل تولید نشد.',
      '',
      'برای فعال کردن، یکی از این دو را در «تنظیمات» انجام دهید:',
      '  · یک مدل اضافه کنید (كلید + نامِ مدل)، یا',
      '  · `jcode` را نصب کنید.',
      '',
      'برای اینکه برنامه صادق بماند، به‌جای نمایش خروجیِ ساختگی،',
      'پرامپتی که ساخته شده نمایش داده می‌شود:',
      '',
      '```',
      composed,
      '```',
    ].join('\n')
    yield { type: 'result', text: answer }
    yield { type: 'stage', stage: 'Done', text: 'پایان' }
    yield { type: 'done', payload: { skills: selected.map((s) => s.name), dispatched: false } }
  }
}
