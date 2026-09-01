/**
 * ساختِ مانیفست و بسته‌ی به‌روزرسانیِ تفاضلی.
 *
 * استفاده:
 *   node scripts/build-update-manifest.mjs --dist ../server/dist --out ../dist-update \
 *        --build <sha> --version 0.1.1 [--base update-manifest.json]
 *
 * خروجی در پوشه‌ی مقصد:
 *   update-manifest.json              ← فهرستِ کاملِ فایل‌ها با sha256
 *   update-pack-<build>.tar.gz        ← فقط فایل‌های تغییرکرده (اگر base داده شود)
 *
 * بدونِ --base، بسته‌ی کامل ساخته می‌شود (برای نخستین انتشار).
 */
import { readFile, writeFile, mkdir, rm } from 'node:fs/promises'
import { dirname, join, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'
import { createTarGz, buildManifest, diffManifests, totalBytes } from '../server/dist/test-api.js'

const here = dirname(fileURLToPath(import.meta.url))

function arg(name, fallback) {
  const i = process.argv.indexOf(`--${name}`)
  return i !== -1 && process.argv[i + 1] ? process.argv[i + 1] : fallback
}

const distDir = resolve(here, arg('dist', '../server/dist'))
const outDir = resolve(here, arg('out', '../dist-update'))
const basePath = arg('base', null)
const build = arg('build', new Date().toISOString().replace(/[-:]/g, '').slice(0, 14))
const version = arg('version', '0.1.0')

/** خواندنِ مانیفستِ منتشرشده‌ی قبلی (برای محاسبه‌ی تفاضل) */
async function readBase() {
  if (!basePath) return null
  try {
    return JSON.parse(await readFile(resolve(here, basePath), 'utf8'))
  } catch {
    console.log('[update] مانیفستِ پایه یافت نشد — بسته‌ی کامل ساخته می‌شود')
    return null
  }
}

const manifest = await buildManifest(distDir, { version, build })
const base = await readBase()
const diff = diffManifests(base, manifest)

await rm(outDir, { recursive: true, force: true })
await mkdir(outDir, { recursive: true })

// بسته: فقط فایل‌های جدید و تغییرکرده
const pack = new Map()
const targets = base ? [...diff.added, ...diff.changed] : manifest.files
for (const f of targets) {
  const buf = await readFile(join(distDir, f.path))
  pack.set(f.path, buf)
}

const gz = createTarGz(pack)
const packName = `update-pack-${build}.tar.gz`
await writeFile(join(outDir, packName), gz)
await writeFile(join(outDir, 'update-manifest.json'), JSON.stringify(manifest, null, 2), 'utf8')

const pct = base && totalBytes(manifest) > 0
  ? ((diff.downloadBytes / totalBytes(manifest)) * 100).toFixed(1)
  : '100.0'

console.log(`[update] نسخه ${version} · ساخت ${build}`)
console.log(`[update] فایل‌های کل: ${manifest.files.length}`)
console.log(`[update] تغییرکرده: ${diff.added.length + diff.changed.length} · حذف‌شده: ${diff.removed.length}`)
console.log(`[update] حجمِ بسته: ${(gz.byteLength / 1024).toFixed(1)} کیلوبایت (${pct}% از کلِ ${(totalBytes(manifest) / 1048576).toFixed(2)} مگابایت)`)
console.log(`[update] خروجی: ${outDir}`)
