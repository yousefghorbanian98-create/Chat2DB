/**
 * به‌روزرسانیِ تفاضلی (delta update).
 *
 * ایده: نصب‌کننده ۲۱٫۷ مگابایت است، اما بیشترِ آن (پوسته‌ی Tauri و node.exe)
 * هیچ‌وقت عوض نمی‌شود. چیزی که واقعاً تغییر می‌کند دارایی‌های رابط و باندلِ
 * سرور است — معمولاً چندصد کیلوبایت. پس به‌جای دانلودِ کلِ نصب‌کننده،
 * فقط فایل‌های تغییرکرده را می‌گیریم.
 *
 * ایمنی: هیچ فایلی پیش از تأییدِ sha256 روی دیسک نوشته نمی‌شود، و هر اِعمال
 * ابتدا نسخه‌ی پشتیبان می‌گیرد تا در صورتِ خطا برگردانده شود.
 */
import { createHash } from 'node:crypto'
import { gunzipSync, gzipSync } from 'node:zlib'
import { readFile, writeFile, mkdir, rm, readdir, stat, rename, copyFile } from 'node:fs/promises'
import { join, dirname, resolve, relative, sep } from 'node:path'

export interface ManifestFile {
  path: string
  size: number
  sha256: string
}

export interface Manifest {
  channel: string
  version: string
  build: string
  /** بسته‌ی تفاضلی نسبت به کدام ساخت ساخته شده؛ برای تشخیصِ «عقب‌ماندن از چند انتشار» */
  from?: string | null
  generatedAt: string
  files: ManifestFile[]
}

export interface DeltaDiff {
  added: ManifestFile[]
  changed: ManifestFile[]
  removed: string[]
  /** مجموعِ حجمِ فایل‌هایی که باید دانلود شوند */
  downloadBytes: number
}

const MANIFEST_NAME = 'update-manifest.json'

/** مسیرها همیشه با '/' و نسبی نگه داشته می‌شوند تا بین ویندوز و لینوکس یکسان باشند */
function normalizePath(p: string): string {
  return p.split(sep).join('/').replace(/^\.\//, '')
}

export function hashBuffer(buf: Buffer): string {
  return createHash('sha256').update(buf).digest('hex')
}

/** همه‌ی فایل‌های یک پوشه را با درهم‌سازی برمی‌گرداند */
export async function scanDir(root: string): Promise<ManifestFile[]> {
  const out: ManifestFile[] = []

  async function walk(dir: string): Promise<void> {
    let entries: Array<{ name: string; isDirectory(): boolean }> = []
    try {
      entries = await readdir(dir, { withFileTypes: true })
    } catch {
      return
    }
    for (const entry of entries) {
      const full = join(dir, entry.name)
      if (entry.isDirectory()) {
        await walk(full)
      } else {
        const rel = normalizePath(relative(root, full))
        // مانیفست خودش «محتوای برنامه» نیست — فقط داده‌ی راهنماست.
        // اگر در شمارش بیاید، چون روی هر دستگاه تازه ساخته می‌شود همیشه
        // با نسخه‌ی منتشرشده فرق می‌کند و همیشه «به‌روزرسانی هست» نشان می‌دهد.
        if (rel === MANIFEST_NAME) continue
        const buf = await readFile(full)
        out.push({
          path: rel,
          size: buf.byteLength,
          sha256: hashBuffer(buf),
        })
      }
    }
  }

  await walk(root)
  return out.sort((a, b) => a.path.localeCompare(b.path))
}

export async function buildManifest(
  root: string,
  meta: { version: string; build: string; channel?: string },
): Promise<Manifest> {
  return {
    channel: meta.channel ?? 'stable',
    version: meta.version,
    build: meta.build,
    generatedAt: new Date().toISOString(),
    files: await scanDir(root),
  }
}

export async function readManifest(root: string): Promise<Manifest | null> {
  try {
    return JSON.parse(await readFile(join(root, MANIFEST_NAME), 'utf8')) as Manifest
  } catch {
    return null
  }
}

export async function writeManifest(root: string, manifest: Manifest): Promise<void> {
  await writeFile(join(root, MANIFEST_NAME), JSON.stringify(manifest, null, 2), 'utf8')
}

/** تفاوتِ دو مانیفست — پایه‌ی «تفاضلی بودن» همین است */
export function diffManifests(local: Manifest | null, remote: Manifest): DeltaDiff {
  const localMap = new Map<string, string>()
  for (const f of local?.files ?? []) localMap.set(f.path, f.sha256)

  const remotePaths = new Set<string>()
  const added: ManifestFile[] = []
  const changed: ManifestFile[] = []

  for (const f of remote.files) {
    remotePaths.add(f.path)
    const localHash = localMap.get(f.path)
    if (localHash === undefined) added.push(f)
    else if (localHash !== f.sha256) changed.push(f)
  }

  const removed = [...localMap.keys()].filter((p) => !remotePaths.has(p) && p !== MANIFEST_NAME)

  return {
    added,
    changed,
    removed,
    downloadBytes: [...added, ...changed].reduce((n, f) => n + f.size, 0),
  }
}

/* ────────────────────────────────────────────────────────────────
 * خواندنِ tar.gz — پیاده‌سازیِ حداقلیِ ustar، بدون وابستگیِ خارجی
 * ──────────────────────────────────────────────────────────────── */

function octal(str: string): number {
  const cleaned = str.replace(/\0.*$/, '').trim()
  return cleaned ? parseInt(cleaned, 8) : 0
}

export function untarGz(gz: Buffer): Map<string, Buffer> {
  const tar = gunzipSync(gz)
  const files = new Map<string, Buffer>()
  let offset = 0

  while (offset + 512 <= tar.byteLength) {
    const header = tar.subarray(offset, offset + 512)
    // دو بلوکِ صفر یعنی پایانِ آرشیو
    if (header.every((b) => b === 0)) break

    let name = header.subarray(0, 100).toString('utf8').replace(/\0.*$/, '')
    const size = octal(header.subarray(124, 136).toString('utf8'))
    const typeflag = String.fromCharCode(header[156] ?? 0)
    const prefix = header.subarray(345, 500).toString('utf8').replace(/\0.*$/, '')
    if (prefix) name = `${prefix}/${name}`

    offset += 512
    const data = tar.subarray(offset, offset + size)
    offset += Math.ceil(size / 512) * 512

    if (typeflag === 'L') {
      // نامِ بلندِ GNU: بلوکِ بعدی خودِ نام است
      name = data.toString('utf8').replace(/\0.*$/, '')
      continue
    }
    if (typeflag === '0' || typeflag === '\u0000' || typeflag === '7') {
      files.set(normalizePath(name), Buffer.from(data))
    }
    // بقیه‌ی نوع‌ها (پوشه، پیوند، PAX) نیازی به استخراج ندارند
  }

  return files
}

/* ────────────────────────────────────────────────────────────────
 * اِعمالِ بسته — با نسخه‌ی پشتیبان و بازگشت در صورتِ خطا
 * ──────────────────────────────────────────────────────────────── */

export interface ApplyResult {
  applied: number
  removed: number
  /** اگر باندلِ خودِ سرور عوض شده باشد، باید برنامه دوباره اجرا شود */
  restartRequired: boolean
}

const RESTART_TRIGGERS = new Set(['index.js', 'package.json', 'test-api.js'])

export async function applyPack(
  distDir: string,
  pack: Map<string, Buffer>,
  remote: Manifest,
): Promise<ApplyResult> {
  const root = resolve(distDir)
  const backup = `${root}.bak`
  await rm(backup, { recursive: true, force: true })

  // ۱) تأییدِ همه‌ی فایل‌ها پیش از نوشتنِ هر چیزی
  const expected = new Map<string, string>()
  for (const f of remote.files) expected.set(f.path, f.sha256)

  const toWrite: Array<[string, Buffer]> = []
  for (const [name, buf] of pack) {
    // ایمنی: مسیر نباید از پوشه بیرون بزند
    const target = resolve('/', name).slice(1)
    if (target.startsWith('..') || target.includes('..')) {
      throw new Error(`مسیرِ نامعتبر در بسته: ${name}`)
    }
    const want = expected.get(target)
    if (!want) throw new Error(`فایلِ ناشناس در بسته: ${name}`)
    if (hashBuffer(buf) !== want) throw new Error(`تطابق ندارد: ${name}`)
    toWrite.push([target, buf])
  }

  // ۲) نسخه‌ی پشتیبان
  await cpDir(root, backup)

  try {
    // ۳) نوشتن
    for (const [target, buf] of toWrite) {
      const full = join(root, target)
      await mkdir(dirname(full), { recursive: true })
      await writeFile(full, buf)
    }

    // ۴) حذفِ فایل‌های حذف‌شده
    const remotePaths = new Set(remote.files.map((f) => f.path))
    let removed = 0
    for (const f of (await readManifest(root))?.files ?? []) {
      if (!remotePaths.has(f.path)) {
        await rm(join(root, f.path), { force: true })
        removed++
      }
    }

    // ۵) مانیفستِ جدید
    await writeManifest(root, remote)

    return {
      applied: toWrite.length,
      removed,
      restartRequired: toWrite.some(([p]) => RESTART_TRIGGERS.has(p)),
    }
  } catch (err) {
    // برگرداندن به وضعِ پیشین
    await rm(root, { recursive: true, force: true })
    await rename(backup, root)
    throw err
  }
}

/** کپیِ بازگشتی — فقط برای نسخه‌ی پشتیبانِ همین‌جا */
async function cpDir(from: string, to: string): Promise<void> {
  await mkdir(to, { recursive: true })
  const entries = await readdir(from, { withFileTypes: true })
  for (const entry of entries) {
    const src = join(from, entry.name)
    const dst = join(to, entry.name)
    if (entry.isDirectory()) await cpDir(src, dst)
    else await copyFile(src, dst)
  }
}

/** حجمِ کلِ یک مانیفست — برای مقایسه با نصب‌کننده‌ی کامل */
export function totalBytes(m: Manifest): number {
  return m.files.reduce((n, f) => n + f.size, 0)
}

export async function dirExists(p: string): Promise<boolean> {
  try {
    await stat(p)
    return true
  } catch {
    return false
  }
}

/* ────────────────────────────────────────────────────────────────
 * نوشتنِ tar.gz — برای ساختِ بسته در CI و برای تستِ رفت‌وبرگشت
 * ──────────────────────────────────────────────────────────────── */

export function createTarGz(files: Map<string, Buffer>): Buffer {
  const chunks: Buffer[] = []

  for (const [name, buf] of [...files.entries()].sort((a, b) => a[0].localeCompare(b[0]))) {
    if (Buffer.byteLength(name) > 100) {
      throw new Error(`tar: نامِ بلند پشتیبانی نمی‌شود: ${name}`)
    }
    const header = Buffer.alloc(512)
    Buffer.from(name, 'utf8').copy(header, 0)
    header.write('000644 \0', 100, 8, 'ascii') // mode
    header.write('000000 \0', 108, 8, 'ascii') // uid
    header.write('000000 \0', 116, 8, 'ascii') // gid
    header.write(buf.byteLength.toString(8).padStart(11, '0') + '\0', 124, 12, 'ascii') // size
    header.write(Math.floor(Date.now() / 1000).toString(8).padStart(11, '0') + '\0', 136, 12, 'ascii') // mtime
    header.write('        ', 148, 8, 'ascii') // checksum (موقت)
    header.write('0', 156, 1, 'ascii') // typeflag: فایلِ معمولی
    header.write('ustar\0', 257, 6, 'ascii') // magic
    header.write('00', 263, 2, 'ascii') // version

    let sum = 0
    for (let i = 0; i < 512; i++) sum += header[i]!
    header.write(sum.toString(8).padStart(6, '0') + '\0 ', 148, 8, 'ascii')

    chunks.push(header, buf)
    const padding = (512 - (buf.byteLength % 512)) % 512
    if (padding) chunks.push(Buffer.alloc(padding))
  }

  // دو بلوکِ صفر = پایانِ آرشیو
  chunks.push(Buffer.alloc(1024))
  return gzipSync(Buffer.concat(chunks))
}
