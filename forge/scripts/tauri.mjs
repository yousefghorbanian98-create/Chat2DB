/**
 * پوششِ سبک دورِ دستورِ tauri.
 *
 * چرا لازم شد؟ اجرای بیلد با یک triple مشخص (‎--target x86_64-pc-windows-msvc‎)
 * باعث می‌شود cargo خروجی را در ‎target/<triple>/release‎ بگذارد نه ‎target/release‎.
 * مسیرِ استانداردِ آپلود در پایپ‌لاین دومی را می‌خواند، بنابراین اینجا
 * بعد از موفقیتِ بیلد، پوشه‌ی bundle را به مسیرِ استاندارد هم می‌آوریم.
 *
 * این کار فقط «کپیِ خروجی به جای مورد انتظار» است — خودِ بیلد دست‌نخورده است.
 */
import { spawnSync } from 'node:child_process'
import { existsSync, cp, mkdir, readdirSync, statSync } from 'node:fs'
import { join, dirname, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const here = dirname(fileURLToPath(import.meta.url))
const srcTauri = resolve(here, '../src-tauri')
const targetDir = join(srcTauri, 'target')

const args = process.argv.slice(2)
const bin = process.platform === 'win32' ? 'tauri.cmd' : 'tauri'

const result = spawnSync(bin, args, {
  stdio: 'inherit',
  shell: process.platform === 'win32',
  cwd: resolve(here, '..'),
})

/** کپیِ پوشه‌ی bundle از زیرشاخه‌ی triple به مسیرِ استاندارد */
function mirrorBundle() {
  if (!existsSync(targetDir)) {
    console.log(`[forge] no target dir at ${targetDir}`)
    return
  }
  console.log(`[forge] target entries: ${readdirSync(targetDir).join(', ') || '(none)'}`)
  const standard = join(targetDir, 'release', 'bundle')
  const candidates = []

  for (const entry of readdirSync(targetDir)) {
    const bundle = join(targetDir, entry, 'release', 'bundle')
    try {
      if (existsSync(bundle) && statSync(bundle).isDirectory()) candidates.push(bundle)
    } catch {
      // نادیده گرفتنِ ورودی‌های غیرقابل خواندن
    }
  }
  // bundle استاندارد هم ممکن است از قبل وجود داشته باشد
  if (existsSync(standard)) candidates.push(standard)

  for (const from of candidates) {
    if (resolve(from) === resolve(standard)) continue
    try {
      mkdir(standard, { recursive: true })
      // کپیِ تک‌تکِ فرزندان: با cp روی یک مقصدِ موجود، پوشه درون مقصد
      // می‌نشیند (‎bundle/bundle/...‎) که مسیرِ آپلود را خراب می‌کند
      for (const child of readdirSync(from)) {
        cp(join(from, child), join(standard, child), { recursive: true, force: true })
        console.log(`[forge] mirrored ${child} → ${join(standard, child)}`)
      }
    } catch (err) {
      console.warn(`[forge] bundle mirror skipped: ${err?.message ?? err}`)
    }
  }
}

mirrorBundle()

process.exit(result.status ?? 1)
