/**
 * گیت‌های طراحی (FE-4) به‌صورت خودکار.
 *
 * FE-4-G1  ui-ux-pro-max  → رنگ‌ها باید از توکن بیایند، نه از مقدار ثابت
 * FE-4-G2  taste-skill    → عمق فقط با خطِ مویی؛ بدون سایه
 * FE-4-G3  motion-design  → زمان‌بندی و easing از جدول؛ بدون linear برای حرکت مکانی
 *
 * این اسکریپت جایگزینِ اسکرین‌شات نیست، اما برخلافِ اسکرین‌شات
 * در هر محیطی (حتی بدون مرورگر) قابل اجرا و تکرارپذیر است.
 */
import { readdir, readFile } from 'node:fs/promises'
import { join, extname } from 'node:path'
import { fileURLToPath } from 'node:url'
import { dirname, resolve } from 'node:path'

const here = dirname(fileURLToPath(import.meta.url))
const srcDir = resolve(here, '../src')

const HEX = /#[0-9a-fA-F]{3,8}\b/g
const SHADOW = /box-shadow|shadow-(sm|md|lg|xl|2xl)|drop-shadow/g
const LINEAR = /easeLinear|easing:\s*\[?\s*['"]?linear/i

const ALLOWED_HEX_FILES = new Set(['index.css']) // فقط فایل توکن‌ها مجاز به hex است

async function walk(dir) {
  const out = []
  for (const entry of await readdir(dir, { withFileTypes: true })) {
    const p = join(dir, entry.name)
    if (entry.isDirectory()) out.push(...(await walk(p)))
    else if (['.tsx', '.ts', '.css'].includes(extname(entry.name))) out.push(p)
  }
  return out
}

const files = await walk(srcDir)
const violations = []

for (const file of files) {
  const name = file.split('/').pop()
  const text = await readFile(file, 'utf8')
  const lines = text.split('\n')

  lines.forEach((line, i) => {
    const where = `${name}:${i + 1}`

    // G1 — رنگ ثابت ممنوع (غیر از فایلِ توکن‌ها)
    if (!ALLOWED_HEX_FILES.has(name) && HEX.test(line)) {
      violations.push({ gate: 'FE-4-G1', where, why: 'رنگِ ثابت به‌جای توکن', line: line.trim() })
    }

    // G2 — سایه ممنوع
    if (SHADOW.test(line) && !line.includes('scrollbar')) {
      violations.push({ gate: 'FE-4-G2', where, why: 'سایه — عمق باید فقط با خطِ مویی باشد', line: line.trim() })
    }

    // G3 — حرکتِ مکانی نباید linear باشد
    if (LINEAR.test(line)) {
      violations.push({ gate: 'FE-4-G3', where, why: 'easing خطی برای حرکت', line: line.trim() })
    }
  })
}

if (violations.length) {
  console.error(`❌ ${violations.length} تخلف از قراردادِ طراحی:`)
  for (const v of violations) console.error(`   [${v.gate}] ${v.where} — ${v.why}\n      ${v.line}`)
  process.exit(1)
}

console.log(`✅ گیت‌های طراحی پاس شد — ${files.length} فایل بررسی شد`)
console.log('   FE-4-G1 رنگ فقط از توکن · FE-4-G2 بدون سایه · FE-4-G3 بدون easing خطی')
