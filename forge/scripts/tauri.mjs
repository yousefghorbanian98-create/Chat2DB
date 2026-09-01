/**
 * پوششِ سبک دورِ دستورِ tauri.
 *
 * چرا لازم شد؟ ساخت با یک triple مشخص (‎--target x86_64-pc-windows-msvc‎)
 * باعث می‌شود cargo خروجی را در ‎target/<triple>/release‎ بگذارد، در حالی که
 * پایپ‌لاین نصب‌کننده را از ‎target/release/bundle‎ برمی‌دارد. اینجا بعد از
 * موفقیتِ بیلد، نصب‌کننده‌ها را از هر کجای ‎target‎ که باشند پیدا کرده و به
 * مسیرِ استاندارد می‌آوریم — بدونِ فرض درباره‌ی چیدمانِ پوشه‌ها.
 */
import { spawnSync } from 'node:child_process'
import { maybePublishUpdate } from './publish-update.mjs'
import { existsSync, cpSync, mkdirSync, readdirSync, writeFileSync } from 'node:fs'
import { join, dirname, resolve, relative, basename } from 'node:path'
import { fileURLToPath } from 'node:url'

const here = dirname(fileURLToPath(import.meta.url))
const projectDir = resolve(here, '..')
const targetDir = join(projectDir, 'src-tauri', 'target')
const standard = join(targetDir, 'release', 'bundle')

const args = process.argv.slice(2)
const bin = process.platform === 'win32' ? 'tauri.cmd' : 'tauri'

const result = spawnSync(bin, args, {
  stdio: 'inherit',
  shell: process.platform === 'win32',
  cwd: projectDir,
})

/** همه‌ی فایل‌های زیرِ dir را به‌صورت بازگشتی برمی‌گرداند */
function walk(dir, out = []) {
  let entries = []
  try {
    entries = readdirSync(dir, { withFileTypes: true })
  } catch {
    return out
  }
  for (const entry of entries) {
    const full = join(dir, entry.name)
    if (entry.isDirectory()) walk(full, out)
    else if (entry.isFile()) out.push(full)
  }
  return out
}

/** جمع‌آوریِ نصب‌کننده‌ها از هر کجا که ساخته شده باشند */
function collectInstallers() {
  const found = []
  for (const file of walk(targetDir)) {
    const rel = relative(targetDir, file).replace(/\\/g, '/')
    if (/bundle\/nsis\/[^/]+\.exe$/i.test(rel)) found.push({ kind: 'nsis', file, rel })
    else if (/bundle\/msi\/[^/]+\.msi$/i.test(rel)) found.push({ kind: 'msi', file, rel })
  }
  return found
}

function mirror() {
  if (!existsSync(targetDir)) {
    console.log(`[forge] هیچ پوشه‌ی targetای در ${targetDir} نیست`)
    return
  }

  const found = collectInstallers()
  console.log(`[forge] نصب‌کننده‌های یافت‌شده: ${found.length || 'هیچ'} `)

  for (const { kind, file, rel } of found) {
    const destDir = join(standard, kind)
    const dest = join(destDir, basename(file))
    if (resolve(file) === resolve(dest)) {
      console.log(`[forge] ${rel} همین‌جا در مسیرِ استاندارد است`)
      continue
    }
    try {
      mkdirSync(destDir, { recursive: true })
      cpSync(file, dest, { force: true })
      console.log(`[forge] منتقل شد ${rel} → ${relative(projectDir, dest).replace(/\\/g, '/')}`)
    } catch (err) {
      console.warn(`[forge] انتقال ناموفق (${rel}): ${err?.message ?? err}`)
    }
  }

  // اگر چیزی پیدا نشد، درخت را تا دو سطح چاپ کن تا دفعه‌ی بعد معلوم شود کجاست
  if (found.length === 0) {
    const tree = []
    for (const entry of readdirSync(targetDir, { withFileTypes: true })) {
      if (!entry.isDirectory()) continue
      let children = []
      try {
        children = readdirSync(join(targetDir, entry.name)).slice(0, 20)
      } catch {
        /* نادیده گرفتن */
      }
      tree.push(`${entry.name}/ → ${children.join(', ') || '(خالی)'}`)
    }
    console.log('[forge] درختِ target:\n' + (tree.join('\n') || '(خالی)'))
  }

  // مانیفستِ کوچک برای دیباگ
  try {
    mkdirSync(standard, { recursive: true })
    writeFileSync(
      join(standard, 'MIRROR.txt'),
      found.map((f) => `${f.kind}\t${f.rel}`).join('\n') + '\n',
    )
  } catch {
    /* اختیاری */
  }
}

mirror()

// انتشارِ بسته‌ی تفاضلی — فقط روی CI و فقط با علامتِ .publish-update
await maybePublishUpdate()

process.exit(result.status ?? 1)
