// کپیِ دارایی‌های لازم در کنار خروجیِ بیلد شده،
// تا dist/ بتواند به‌تنهایی (بدن پوشهٔ src) اجرا شود.
import { cp, mkdir, access, writeFile, rm } from 'node:fs/promises'
import { resolve, dirname } from 'node:path'
import { fileURLToPath } from 'node:url'
import { execSync } from 'node:child_process'

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
    // پیش از کپی پاک می‌کنیم: وگرنه دارایی‌های نام‌گذاری‌شده‌ی ساخت‌های قبلی
    // (مثل index-B1IBHFUU.js) روی هم جمع می‌شوند و بسته هر بار بزرگ‌تر می‌شود
    await rm(resolve(target, 'skills'), { recursive: true, force: true })
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
    await rm(resolve(target, 'web'), { recursive: true, force: true })
    await cp(web, resolve(target, 'web'), { recursive: true })
    console.log('web assets copied → dist/web')
  } else {
    console.log('web assets not found (forge/dist) — skipped')
  }

  // مانیفستِ همین ساخت را کنارِ فایل‌ها می‌گذاریم.
  // چرا؟ برنامه‌ی نصب‌شده باید بداند «کدام ساخت» است تا بعداً بتواند از
  // بسته‌ی تفاضلی استفاده کند. اگر این‌جا نباشد، نخستین بررسیِ هر کاربر
  // شناسه را «local» می‌گذارد و تفاضل هیچ‌وقت به کار نمی‌افتد.
  await writeInstallManifest()
  console.log('assets ready')
}

/** شناسه‌ی ساخت: همان commit در CI، و در دستگاهِ توسعه از git */
function buildId() {
  if (process.env.GITHUB_SHA) return process.env.GITHUB_SHA.slice(0, 7)
  try {
    return execSync('git rev-parse --short HEAD', { cwd: root, stdio: ['ignore', 'pipe', 'ignore'] })
      .toString()
      .trim()
  } catch {
    return 'local'
  }
}

async function writeInstallManifest() {
  try {
    // test-api.js پیش از این اسکریپت ساخته شده است
    const { buildManifest } = await import('../dist/test-api.js')
    const manifest = await buildManifest(target, { version: '0.1.0', build: buildId() })
    await writeFile(
      resolve(target, 'update-manifest.json'),
      JSON.stringify({ ...manifest, from: null }, null, 2),
      'utf8',
    )
    console.log(`install manifest written — build ${manifest.build} · ${manifest.files.length} files`)
  } catch (err) {
    // مانیفست داده‌ی راهنماست؛ نبودنش بیلد را خراب نمی‌کند
    console.log(`install manifest skipped — ${err?.message ?? err}`)
  }
}

main().catch((err) => {
  console.error(err)
  process.exit(1)
})
