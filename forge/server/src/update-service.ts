/**
 * سرویسِ به‌روزرسانی — لایه‌ی شبکه و اِعمال.
 *
 * منطقِ خالص (درهم‌سازی، تفاضل، tar، بازگشت به عقب) در `update.ts` است و
 * اینجا فقط با شبکه و دیسک حرف می‌زند تا آن بخش قابلِ تستِ واحد باشد.
 *
 * منبعِ انتشار: دارایی‌های همان Release در گیت‌هاب.
 */
import { dirname } from 'node:path'
import {
  buildManifest,
  readManifest,
  writeManifest,
  diffManifests,
  untarGz,
  applyPack,
  totalBytes,
  type Manifest,
} from './update'

/** پایگاهِ API — قابلِ تغییر برای تست و برای خود-میزبانی */
const API = (process.env.FORGE_UPDATE_API ?? 'https://api.github.com').replace(/\/+$/, '')

export const UPDATE_REPO = process.env.FORGE_UPDATE_REPO ?? 'yousefghorbanian98-create/Chat2DB'
export const UPDATE_TAG = process.env.FORGE_UPDATE_TAG ?? 'forge-v0.1.0'
const ENABLED = (process.env.FORGE_UPDATE_ENABLED ?? '1') !== '0'

/** پوشه‌ای که به‌روزرسانی در آن اِعمال می‌شود = همان‌جا که index.js نشسته */
export function targetDir(): string {
  return dirname(process.argv[1] ?? '.')
}

interface ReleaseAsset {
  name: string
  browser_download_url: string
  size: number
}

/** خطاها را نگه می‌داریم تا پیامِ «مانیفست یافت نشد» گمراه‌کننده نباشد */
class FetchFailure extends Error {}

async function fetchJson<T>(url: string): Promise<T | null> {
  if (process.env.FORGE_UPDATE_INSECURE_TLS === '1') {
    // فقط برای تستِ محلی؛ هرگز در حالت عادی
    process.env.NODE_TLS_REJECT_UNAUTHORIZED = '0'
  }
  try {
    const res = await fetch(url, {
      headers: { accept: 'application/vnd.github+json', 'user-agent': 'forge-updater' },
    })
    if (!res.ok) throw new FetchFailure(`پاسخ ${res.status}`)
    return (await res.json()) as T
  } catch (err) {
    throw new FetchFailure(err instanceof Error ? err.message : 'خطای شبکه')
  }
}

async function fetchBinary(url: string): Promise<Buffer> {
  try {
    const res = await fetch(url, { headers: { 'user-agent': 'forge-updater' } })
    if (!res.ok) throw new FetchFailure(`پاسخ ${res.status}`)
    return Buffer.from(await res.arrayBuffer())
  } catch (err) {
    if (err instanceof FetchFailure) throw err
    throw new FetchFailure(err instanceof Error ? err.message : 'خطای شبکه')
  }
}

async function releaseAssets(): Promise<ReleaseAsset[]> {
  const data = await fetchJson<{ assets?: ReleaseAsset[] }>(
    `${API}/repos/${UPDATE_REPO}/releases/tags/${UPDATE_TAG}`,
  )
  return data?.assets ?? []
}

/** مانیفستِ محلی؛ اگر نباشد (نصبِ دستی) همان‌جا ساخته می‌شود */
async function localManifest(): Promise<Manifest> {
  const dir = targetDir()
  const existing = await readManifest(dir)
  if (existing) return existing

  const generated = await buildManifest(dir, { version: '0.1.0', build: 'local' })
  await writeManifest(dir, generated).catch(() => undefined)
  return generated
}

export interface CheckResult {
  enabled: boolean
  current: { version: string; build: string } | null
  latest: { version: string; build: string; generatedAt: string } | null
  upToDate: boolean
  changed: string[]
  removed: string[]
  /** حجمِ دانلود در برابرِ حجمِ نصب‌کننده‌ی کامل — دلیلِ اصلیِ این سیستم */
  deltaBytes: number
  fullBytes: number
  restartRequired: boolean
  error?: string
}

export async function checkForUpdate(): Promise<CheckResult> {
  const local = await localManifest()
  const base = {
    enabled: ENABLED,
    current: { version: local.version, build: local.build },
    latest: null,
    upToDate: true,
    changed: [],
    removed: [],
    deltaBytes: 0,
    fullBytes: totalBytes(local),
    restartRequired: false,
  } satisfies CheckResult

  if (!ENABLED) return base

  let assets: ReleaseAsset[] = []
  try {
    assets = await releaseAssets()
  } catch (err) {
    return { ...base, error: `ارتباط با ${API} برقرار نشد: ${err instanceof Error ? err.message : ''}` }
  }

  const manifestAsset = assets.find((a) => a.name === 'update-manifest.json')
  if (!manifestAsset) {
    return { ...base, error: 'در این Release هنوز مانیفستی منتشر نشده است' }
  }

  let remoteBuf: Buffer
  try {
    remoteBuf = await fetchBinary(manifestAsset.browser_download_url)
  } catch (err) {
    return { ...base, error: `دریافتِ مانیفست ناموفق: ${err instanceof Error ? err.message : ''}` }
  }

  const remote = JSON.parse(remoteBuf.toString('utf8')) as Manifest
  const diff = diffManifests(local, remote)

  return {
    enabled: true,
    current: { version: local.version, build: local.build },
    latest: { version: remote.version, build: remote.build, generatedAt: remote.generatedAt },
    upToDate: diff.added.length === 0 && diff.changed.length === 0 && diff.removed.length === 0,
    changed: [...diff.added, ...diff.changed].map((f) => f.path),
    removed: diff.removed,
    deltaBytes: diff.downloadBytes,
    fullBytes: totalBytes(remote),
    restartRequired: [...diff.added, ...diff.changed].some((f) =>
      ['index.js', 'package.json'].includes(f.path),
    ),
  }
}

export interface ApplyOutcome {
  ok: boolean
  applied: number
  removed: number
  restartRequired: boolean
  /** بسیاری از به‌روزرسانی‌ها فقط دارایی‌های رابط هستند → با بارگذاریِ دوباره اعمال می‌شوند */
  reloadSufficient: boolean
  error?: string
}

export async function applyUpdate(): Promise<ApplyOutcome> {
  if (!ENABLED) return { ok: false, applied: 0, removed: 0, restartRequired: false, reloadSufficient: true, error: 'به‌روزرسانی غیرفعال است' }

  let assets: ReleaseAsset[] = []
  try {
    assets = await releaseAssets()
  } catch (err) {
    return { ok: false, applied: 0, removed: 0, restartRequired: false, reloadSufficient: true, error: err instanceof Error ? err.message : 'خطای شبکه' }
  }

  const manifestAsset = assets.find((a) => a.name === 'update-manifest.json')
  if (!manifestAsset) {
    return { ok: false, applied: 0, removed: 0, restartRequired: false, reloadSufficient: true, error: 'در این Release هنوز مانیفستی منتشر نشده است' }
  }

  let remoteBuf: Buffer
  try {
    remoteBuf = await fetchBinary(manifestAsset.browser_download_url)
  } catch (err) {
    return { ok: false, applied: 0, removed: 0, restartRequired: false, reloadSufficient: true, error: err instanceof Error ? err.message : 'خطای شبکه' }
  }
  const remote = JSON.parse(remoteBuf.toString('utf8')) as Manifest

  const packAsset = assets.find((a) => a.name === `update-pack-${remote.build}.tar.gz`)
  if (!packAsset) {
    return { ok: false, applied: 0, removed: 0, restartRequired: false, reloadSufficient: true, error: 'بسته‌ی به‌روزرسانی برای این ساخت یافت نشد' }
  }

  let packBuf: Buffer
  try {
    packBuf = await fetchBinary(packAsset.browser_download_url)
  } catch (err) {
    return { ok: false, applied: 0, removed: 0, restartRequired: false, reloadSufficient: true, error: err instanceof Error ? err.message : 'خطای شبکه' }
  }

  try {
    const files = untarGz(packBuf)
    const result = await applyPack(targetDir(), files, remote)
    return {
      ok: true,
      applied: result.applied,
      removed: result.removed,
      restartRequired: result.restartRequired,
      reloadSufficient: !result.restartRequired,
    }
  } catch (err) {
    return {
      ok: false,
      applied: 0,
      removed: 0,
      restartRequired: false,
      reloadSufficient: true,
      error: err instanceof Error ? err.message : 'خطای ناشناخته',
    }
  }
}
