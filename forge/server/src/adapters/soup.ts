import { spawn } from 'node:child_process'
import { config } from '../config'
import type { AdapterStatus, Skill } from '../types'
import type { Adapter } from './types'
import { SkillRouter } from './router'

/**
 * لایهٔ انتخابِ skill (معادلِ Soup).
 *
 * دو backend:
 *  1. داخلی (TypeScript) — همیشه در دسترس؛ پیاده‌سازیِ همان منطقِ مسیریابی.
 *  2. پایتونی (soup-ai)  — اگر روی دستگاه نصب باشد، به‌عنوان_backend_ ترجیحی
 *     در health گزارش می‌شود تا کاربر بداند از نسخهٔ بالادستی استفاده می‌کند.
 *
 * در هر دو حالت مسیریابی کار می‌کند؛ نبودِ پایتون فقط یعنی degraded.
 */
export class SoupAdapter implements Adapter {
  readonly name = 'soup'
  private router = new SkillRouter()

  constructor(skills: Skill[] = []) {
    if (skills.length) this.router.register(skills)
  }

  setSkills(skills: Skill[]): void {
    this.router.clear()
    this.router.register(skills)
  }

  get skillCount(): number {
    return this.router.size
  }

  /** انتخابِ skillهای مرتبط — همان کارکردِ soup.prepare() */
  prepare(query: string, limit = config.maxSkillsPerCall): Skill[] {
    return this.router.select(query, limit).map((s) => s.skill)
  }

  /** نسخهٔ نمایشی: همراه با امتیاز، برای اینکه UI بتواند دلیلِ انتخاب را نشان دهد */
  explain(query: string, limit = config.maxSkillsPerCall) {
    return this.router.select(query, limit).map(({ skill, score }) => ({
      name: skill.name,
      score: Number(score.toFixed(3)),
      description: skill.description,
    }))
  }

  private pythonSoupAvailable(): Promise<boolean> {
    return new Promise((resolvePromise) => {
      const child = spawn(config.pythonBin, ['-c', 'import soup; print(soup.__name__)'], {
        stdio: 'ignore',
        shell: false,
      })
      const timer = setTimeout(() => {
        child.kill()
        resolvePromise(false)
      }, 5000)
      child.on('error', () => {
        clearTimeout(timer)
        resolvePromise(false)
      })
      child.on('close', (code) => {
        clearTimeout(timer)
        resolvePromise(code === 0)
      })
    })
  }

  async health(): Promise<AdapterStatus> {
    const py = await this.pythonSoupAvailable()
    if (py) {
      return {
        name: this.name,
        state: 'ready',
        detail: `soup-ai پایتونی در دسترس است · ${this.router.size} skill بارگذاری شده`,
      }
    }
    return {
      name: this.name,
      state: 'degraded',
      detail: `پایتون/‏soup-ai یافت نشد — از مسیریاب داخلی استفاده می‌شود · ${this.router.size} skill`,
    }
  }
}
