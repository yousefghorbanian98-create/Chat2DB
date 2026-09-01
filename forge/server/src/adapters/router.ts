import type { Skill } from '../types'

/**
 * پیاده‌سازی داخلیِ منطقِ مسیریابیِ Soup (بدون نیاز به پایتون).
 *
 * SOURCE: https://github.com/southwind-ai/soup (MIT)
 * الهام: انتخابِ skill بر اساس description + examples با وزن‌دهیِ BM25،
 *        به‌علاوه تقویتِ تگ‌ها (tag boost) مطابق مستنداتِ Soup.
 *
 * چرا اینجا پیاده‌سازی شده؟ چون پایتونِ ۳٫۱۲+ روی هر دستگاه ویندوزی تضمین‌شده
 * نیست و اصلِ حاکم این است: «هیچ وابستگی‌ای نباید برنامه را بترکاند.»
 */

const STOP_WORDS = new Set([
  'the', 'a', 'an', 'and', 'or', 'but', 'if', 'then', 'of', 'to', 'in', 'on',
  'for', 'with', 'is', 'are', 'be', 'this', 'that', 'it', 'as', 'at', 'by',
  'from', 'use', 'using', 'را', 'به', 'از', 'در', 'با', 'برای', 'یک',
])

export function tokenize(text: string): string[] {
  return text
    .toLowerCase()
    .replace(/[^a-z0-9\u0600-\u06ff]+/gi, ' ')
    .split(/\s+/)
    .filter((t) => t.length > 1 && !STOP_WORDS.has(t))
}

/** متنِ قابل جستجوی یک skill — همان چیزی که Soup به‌عنوان سیگنال استفاده می‌کند. */
function searchableText(skill: Skill): string {
  return [skill.name, skill.description, ...(skill.examples ?? [])].join(' \n ')
}

/**
 * امتیازدهی BM25 روی یک مجموعهٔ کوچک از skillها.
 * k1 و b مقادیر استانداردِ BM25 هستند.
 */
export class SkillRouter {
  private skills: Skill[] = []
  private docTokens = new Map<string, string[]>()
  private docLen = new Map<string, number>()
  private avgLen = 0
  private idf = new Map<string, number>()

  constructor(private readonly k1 = 1.5, private readonly b = 0.75) {}

  register(skills: Skill[]): void {
    for (const s of skills) this.skills.push(s)
    this.reindex()
  }

  clear(): void {
    this.skills = []
    this.docTokens.clear()
    this.docLen.clear()
    this.idf.clear()
    this.avgLen = 0
  }

  get size(): number {
    return this.skills.length
  }

  private reindex(): void {
    this.docTokens.clear()
    this.docLen.clear()
    let total = 0

    for (const skill of this.skills) {
      const tokens = tokenize(searchableText(skill))
      this.docTokens.set(skill.name, tokens)
      this.docLen.set(skill.name, tokens.length)
      total += tokens.length
    }
    this.avgLen = this.skills.length ? total / this.skills.length : 0

    // محاسبه IDF روی کل مجموعه
    const df = new Map<string, number>()
    for (const [, tokens] of this.docTokens) {
      for (const t of new Set(tokens)) df.set(t, (df.get(t) ?? 0) + 1)
    }
    const n = this.skills.length
    this.idf.clear()
    for (const [term, freq] of df) {
      this.idf.set(term, Math.log(1 + (n - freq + 0.5) / (freq + 0.5)))
    }
  }

  /** امتیازِ BM25 برای یک عبارت در یک سند. */
  private scoreDoc(queryTokens: string[], name: string): number {
    const tokens = this.docTokens.get(name) ?? []
    if (!tokens.length) return 0
    const len = this.docLen.get(name) ?? 0
    const counts = new Map<string, number>()
    for (const t of tokens) counts.set(t, (counts.get(t) ?? 0) + 1)

    let score = 0
    for (const q of queryTokens) {
      const tf = counts.get(q) ?? 0
      if (!tf) continue
      const idf = this.idf.get(q) ?? 0
      const denom = tf + this.k1 * (1 - this.b + (this.b * len) / (this.avgLen || 1))
      score += idf * ((tf * (this.k1 + 1)) / denom)
    }
    return score
  }

  /**
   * skillهای مرتبط با یک درخواست را برمی‌گرداند؛ مرتب‌شده نزولی.
   * تقویتِ تگ: اگر تگی از skill در درخواست ظاهر شود، امتیاز افزایش می‌یابد.
   */
  select(query: string, limit = 3): Array<{ skill: Skill; score: number }> {
    const queryTokens = tokenize(query)
    if (!queryTokens.length) return []

    const scored = this.skills.map((skill) => {
      let score = this.scoreDoc(queryTokens, skill.name)
      const qLower = query.toLowerCase()
      for (const tag of skill.tags) {
        if (qLower.includes(tag.toLowerCase())) score += 1.25
      }
      if (qLower.includes(skill.name.toLowerCase())) score += 2
      return { skill, score }
    })

    return scored
      .filter((s) => s.score > 0)
      .sort((a, b) => b.score - a.score || a.skill.name.localeCompare(b.skill.name))
      .slice(0, limit)
  }
}
