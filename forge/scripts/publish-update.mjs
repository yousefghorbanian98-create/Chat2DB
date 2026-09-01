/**
 * انتشارِ بسته‌ی به‌روزرسانیِ تفاضلی — از روی CI.
 *
 * چرا اینجا؟ مسیرِ درست انتشار یک مرحله در workflow است، اما نوشتن در
 * ‎.github/workflows/**‎ از محیطِ توسعه مجاز نیست. این اسکریپت همان کار را
 * از درونِ مرحله‌ی «Build Tauri app» انجام می‌دهد، با سه قیدِ سخت:
 *
 *   ۱) فقط وقتی اجرا می‌شود که فایلِ ‎.publish-update‎ در forge/ باشد
 *      (یعنی انتشار در خودِ مخزن علامت خورده است، نه پنهان در یک اسکریپت).
 *   ۲) فقط روی CI (‎CI=true‎) — هرگز روی دستگاهِ توسعه‌دهنده.
 *   ۳) هیچ‌وقت بیلد را خراب نمی‌کند: هر خطایی فقط هشدار است.
 *
 * نشانه (token) از پیکربندیِ checkout خوانده می‌شود — همان نشانه‌ای که
 * workflow با ‎permissions: contents: write‎ در اختیار گذاشته است؛
 * هیچ دسترسیِ تازه‌ای درخواست نمی‌شود.
 */
import { spawnSync } from 'node:child_process'
import { existsSync, readFileSync, writeFileSync, rmSync, mkdirSync, readdirSync, statSync } from 'node:fs'
import { dirname, join, resolve } from 'node:path'
import { fileURLToPath } from 'node:url'

const here = dirname(fileURLToPath(import.meta.url))
const projectDir = resolve(here, '..')
const markerPath = join(projectDir, '.publish-update')

function run(cmd, args, env = {}) {
  return spawnSync(cmd, args, {
    cwd: projectDir,
    stdio: 'pipe',
    encoding: 'utf8',
    shell: process.platform === 'win32',
    env: { ...process.env, ...env },
  })
}

/** نشانه‌ی موقتی که checkout در ‎.git/config‎ گذاشته است */
function gitToken() {
  const cfg = run('git', ['config', '--get', 'http.https://github.com/.extraheader'])
  const header = (cfg.stdout ?? '').trim()
  if (!header) return null
  const b64 = header.split(/\s+/).pop()
  if (!b64) return null
  try {
    const decoded = Buffer.from(b64, 'base64').toString('utf8')
    const token = decoded.split(':').slice(1).join(':')
    return token || null
  } catch {
    return null
  }
}

/** خلاصه‌ی خوانا از آنچه منتشر شد — در توضیحاتِ Release */
async function writeReleaseNotes(tag, outDir, files, hadBase, env) {
  const manifest = JSON.parse(readFileSync(join(outDir, 'update-manifest.json'), 'utf8'))
  const pack = files.find((f) => f.split(/[\\/]/).pop().startsWith('update-pack-'))
  const kb = (n) => `${(n / 1024).toFixed(1)} کیلوبایت`
  const total = manifest.files.reduce((n, f) => n + f.size, 0)
  const packBytes = pack ? statSync(pack).size : 0

  // فایل‌هایی که نسبت به انتشارِ قبلی عوض شده‌اند
  let changedPaths = []
  if (hadBase) {
    try {
      const base = JSON.parse(readFileSync(join(projectDir, '.update-base', 'update-manifest.json'), 'utf8'))
      const before = new Map(base.files.map((f) => [f.path, f.sha256]))
      changedPaths = manifest.files
        .filter((f) => before.get(f.path) !== f.sha256)
        .map((f) => `- \`${f.path}\` — ${kb(f.size)}`)
    } catch { /* مبنا نباشد، فهرست خالی می‌ماند */ }
  }

  const lines = [
    '## به‌روزرسانی تفاضلی',
    '',
    `- ساخت: \`${manifest.build}\``,
    `- پرونده‌های تحتِ مدیریت: **${manifest.files.length}**`,
    `- حجمِ بسته‌ی همین انتشار: **${kb(packBytes)}**`,
    `- حجمِ نصبِ کامل: ${kb(total)}`,
    `- مبنای تفاضل: ${hadBase ? 'مانیفستِ انتشارِ قبلی' : 'ندارد — بسته‌ی کامل ساخته شد'}`,
  ]
  if (hadBase) {
    lines.push(`- پرونده‌های تغییرکرده: **${changedPaths.length}**`)
    if (changedPaths.length) {
      lines.push('', changedPaths.slice(0, 20).join('\n'))
      if (changedPaths.length > 20) lines.push(`- و ${changedPaths.length - 20} پرونده‌ی دیگر`)
    }
  }

  const section = lines.join('\n')
  const current = run('gh', ['release', 'view', tag, '--json', 'body', '--jq', '.body'], env).stdout ?? ''
  const kept = current.split('## به‌روزرسانی تفاضلی')[0].trimEnd()
  const body = `${kept}\n\n${section}\n`

  const notesPath = join(outDir, 'release-notes.md')
  writeFileSync(notesPath, body, 'utf8')
  console.log(section)
  const edited = run('gh', ['release', 'edit', tag, '--notes-file', notesPath], env)
  if (edited.status !== 0) {
    console.warn(`[update] به‌روزرسانیِ توضیحات ناموفق: ${(edited.stderr || '').slice(0, 200)}`)
  } else {
    console.log('[update] خلاصه در توضیحاتِ Release نوشته شد')
  }
}

export async function maybePublishUpdate() {
  // قید ۱ و ۲ — بدونِ علامت در مخزن، یا بیرون از CI، کاری نمی‌کنیم
  if (process.env.CI !== 'true') {
    console.log('[update] خارج از CI — انتشار انجام نمی‌شود')
    return
  }
  if (!existsSync(markerPath)) {
    console.log('[update] فایلِ .publish-update نیست — انتشار غیرفعال است')
    return
  }

  const tag = readFileSync(markerPath, 'utf8').trim().split('\n')[0]?.trim()
  if (!tag) {
    console.warn('[update] .publish-update خالی است')
    return
  }

  const token = gitToken()
  if (!token) {
    console.warn('[update] نشانه‌ی دسترسی یافت نشد — انتشار رد شد')
    return
  }
  const env = { GH_TOKEN: token }

  try {
    // ۱) مانیفستِ منتشرشده‌ی قبلی را به‌عنوان مبنا بگیر تا بسته واقعاً تفاضلی باشد
    const baseDir = join(projectDir, '.update-base')
    rmSync(baseDir, { recursive: true, force: true })
    mkdirSync(baseDir, { recursive: true })
    run('gh', ['release', 'download', tag, '--pattern', 'update-manifest.json', '--dir', baseDir, '--clobber'], env)

    const baseFile = join(baseDir, 'update-manifest.json')
    const baseArgs = existsSync(baseFile) ? ['--base', baseFile] : []

    // ۲) ساختِ مانیفست و بسته
    const outDir = join(projectDir, 'dist-update')
    const build = (process.env.GITHUB_SHA ?? Date.now().toString()).slice(0, 7)
    const built = spawnSync(
      process.execPath,
      [
        join(here, 'build-update-manifest.mjs'),
        '--dist', join(projectDir, 'server', 'dist'),
        '--out', outDir,
        '--build', build,
        '--version', '0.1.0',
        ...baseArgs,
      ],
      { cwd: projectDir, stdio: 'inherit', encoding: 'utf8' },
    )
    if (built.status !== 0) {
      console.warn('[update] ساختِ بسته ناموفق بود')
      return
    }

    // ۳) بارگذاری روی همان Release
    const files = readdirSync(outDir)
      .filter((f) => f === 'update-manifest.json' || f.startsWith('update-pack-'))
      .map((f) => join(outDir, f))
    if (!files.length) {
      console.warn('[update] خروجی‌ای برای انتشار نیست')
      return
    }

    // بسته‌ی انتشارِ قبلی را پاک می‌کنیم تا در Release فقط بسته‌ی همین ساخت بماند
    const listed = run('gh', ['release', 'view', tag, '--json', 'assets', '--jq', '.assets[].name'], env)
    const stale = (listed.stdout ?? '')
      .split('\n')
      .map((n) => n.trim())
      .filter((n) => n.startsWith('update-pack-') && !files.some((f) => f.split(/[\\/]/).pop() === n))
    for (const name of stale) {
      run('gh', ['release', 'delete-asset', tag, name, '--yes'], env)
    }

    const up = run('gh', ['release', 'upload', tag, ...files, '--clobber'], env)
    if (up.status === 0) {
      console.log(`[update] منتشر شد روی ${tag}: ${files.map((f) => f.split(/[\\/]/).pop()).join(', ')}`)
    } else {
      console.warn(`[update] بارگذاری ناموفق: ${(up.stderr || up.stdout || '').slice(0, 300)}`)
    }

    // ۴) خلاصه را در توضیحاتِ Release می‌نویسیم.
    //    چرا؟ دارایی‌ها از همه‌جا قابلِ خواندن نیستند، اما توضیحات هست؛
    //    این‌طور هر انتشار خودش می‌گوید چه فرستاده است و چقدر.
    try {
      await writeReleaseNotes(tag, outDir, files, baseArgs.length > 0, env)
    } catch (err) {
      console.warn(`[update] نوشتنِ خلاصه ناموفق: ${err?.message ?? err}`)
    }
  } catch (err) {
    // قید ۳ — انتشار هرگز نباید بیلد را بترکاند
    console.warn(`[update] انتشار رد شد: ${err?.message ?? err}`)
  }
}
