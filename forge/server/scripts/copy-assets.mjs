// کپیِ دارایی‌های لازم در کنار خروجیِ بیلد شده،
// تا dist/ بتواند به‌تنهایی (بدن پوشهٔ src) اجرا شود.
import { cp, mkdir, access } from 'node:fs/promises'
import { resolve, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'

const here = dirname(fileURLToPath(import.meta.url))
const root = resolve(here, '..')
const target = resolve(root, 'dist')

async function exists(p) {
  try {
    await access(p)
    return true
  } catch {
    return false
  }
}

async function main() {
  await mkdir(target, { recursive: true })

  // skills/ معمولاً یک سطح بالاتر است (forge/skills) و خودش کپی نمی‌شود،
  // چون مسیر آن در زمان اجرا نسبت به dist پیدا می‌شود. فقط package.json
  // production را کنار dist می‌گذاریم تا اجرای sidecar ساده باشد.
  const pkg = resolve(root, 'package.json')
  if (await exists(pkg)) {
    await cp(pkg, resolve(target, 'package.json'))
  }

  // مهم: skills را هم داخل dist می‌گذاریم تا workflow ویندوزی
  // (که فقط server/dist را کپی می‌کند) همه چیز را یک‌جا منتقل کند.
  const skills = resolve(root, '../skills')
  if (await exists(skills)) {
    await cp(skills, resolve(target, 'skills'), { recursive: true })
    console.log('skills copied → dist/skills')
  } else {
    console.log('skills not found — skipped')
  }

  // مهم: خروجیِ فرانت‌اند را هم کنارِ سرور می‌گذاریم (dist/web)،
  // تا workflow ویندوزی بدون نیاز به تغییر، همه چیز را یک‌جا کپی کند
  // و سرور بتواند رابط را سرو کند (تک-مبدأ).
  const web = resolve(root, '../dist')
  if (await exists(web)) {
    await cp(web, resolve(target, 'web'), { recursive: true })
    console.log('web assets copied → dist/web')
  } else {
    console.log('web assets not found (forge/dist) — skipped')
  }

  console.log('assets ready')
}

main().catch((err) => {
  console.error(err)
  process.exit(1)
})
