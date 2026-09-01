import { spawn } from 'node:child_process'
import { config } from '../config'
import type { AdapterStatus } from '../types'
import type { Adapter } from './types'

/**
 * هستهٔ اجرا — Jcode.
 * SOURCE: https://github.com/1jehuang/jcode (MIT)
 *
 * Forge مدل اجرا نمی‌کند؛ فقط باینری jcode را صدا می‌زند و خروجی را بازمی‌گرداند.
 * اگر نصب نباشد: state = 'missing' و هیچ استثنایی بالا نمی‌آید.
 */

export interface RunResult {
  ok: boolean
  output: string
  exitCode: number | null
  reason?: string
}

export interface RunOptions {
  /** پوشه‌ی پروژه — بدون آن jcode در پوشه‌ی خودِ برنامه اجرا می‌شود و بی‌معناست */
  cwd?: string
}

export class JcodeAdapter implements Adapter {
  readonly name = 'jcode'

  /** امکانِ تعیینِ مسیرِ باینری — برای تست و نصب‌های غیر استاندارد */
  constructor(private bin: string = config.jcodeBin) {}

  /** امکانِ تغییرِ مسیرِ باینری از تنظیمات */
  setBinary(bin: string): void {
    this.bin = bin
  }

  private runOnce(args: string[], timeoutMs = 8000, cwd?: string): Promise<RunResult> {
    return new Promise((resolvePromise) => {
      let out = ''
      let err = ''
      let settled = false

      const child = spawn(this.bin, args, { shell: false, cwd: cwd ?? process.cwd() })

      const timer = setTimeout(() => {
        if (!settled) {
          settled = true
          child.kill()
          resolvePromise({ ok: false, output: '', exitCode: null, reason: 'timeout' })
        }
      }, timeoutMs)

      child.stdout?.on('data', (d) => (out += String(d)))
      child.stderr?.on('data', (d) => (err += String(d)))

      child.on('error', () => {
        if (settled) return
        settled = true
        clearTimeout(timer)
        resolvePromise({ ok: false, output: '', exitCode: null, reason: 'spawn-failed' })
      })

      child.on('close', (code) => {
        if (settled) return
        settled = true
        clearTimeout(timer)
        resolvePromise({
          ok: code === 0,
          output: (out || err).trim(),
          exitCode: code,
          reason: code === 0 ? undefined : `exit-${code}`,
        })
      })
    })
  }

  async version(): Promise<string | null> {
    const r = await this.runOnce(['--version'])
    return r.ok ? r.output.split('\n')[0]?.trim() ?? null : null
  }

  /**
   * اجرای یک دستور — فقط وقتی jcode آماده باشد معنا دارد.
   * `opts.cwd` پوشه‌ی پروژه است؛ اگر ندهیم، jcode در پوشه‌ی خودِ برنامه
   * اجرا می‌شود که نه مفید است و نه امن.
   */
  async run(prompt: string, opts: RunOptions = {}): Promise<RunResult> {
    return this.runOnce(['run', prompt], 120_000, opts.cwd)
  }

  async health(): Promise<AdapterStatus> {
    const version = await this.version()
    if (version) {
      return { name: this.name, state: 'ready', detail: version }
    }
    return {
      name: this.name,
      state: 'missing',
      detail: `باینری «${this.bin}» در PATH یافت نشد — اجرای واقعی غیرفعال است`,
    }
  }
}
