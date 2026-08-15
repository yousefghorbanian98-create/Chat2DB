import { createHash } from 'node:crypto'
import { createWriteStream, existsSync, mkdirSync, readFileSync, readdirSync, renameSync, rmSync, statSync } from 'node:fs'
import { execFileSync } from 'node:child_process'
import path from 'node:path'
import { pipeline } from 'node:stream/promises'
import { Readable } from 'node:stream'

const root = path.resolve('resources/binaries')
const partials = new Set()
mkdirSync(root, { recursive: true })

function cleanup() {
  for (const file of partials) rmSync(file, { force: true })
}
process.once('SIGINT', () => { cleanup(); process.exit(130) })
process.once('SIGTERM', () => { cleanup(); process.exit(143) })

const baseHeaders = { 'User-Agent': 'youtube-auto-uploader-build/1.0' }
if (process.env.GITHUB_TOKEN) baseHeaders.Authorization = `Bearer ${process.env.GITHUB_TOKEN}`

async function withRetry(label, fn, attempts = 3) {
  let lastError
  for (let attempt = 1; attempt <= attempts; attempt++) {
    try { return await fn() } catch (error) {
      lastError = error
      console.warn(`${label}: attempt ${attempt}/${attempts} failed: ${error instanceof Error ? error.message : String(error)}`)
      if (attempt < attempts) await new Promise((resolve) => setTimeout(resolve, attempt * 5000))
    }
  }
  throw lastError
}

async function fetchText(url) {
  const response = await fetch(url, { redirect: 'follow', headers: baseHeaders })
  if (!response.ok) throw new Error(`Request failed (${response.status}): ${url}`)
  return response.text()
}

async function download(url, file) {
  const partial = `${file}.partial`
  partials.add(partial)
  rmSync(partial, { force: true })
  const response = await fetch(url, { redirect: 'follow', headers: baseHeaders })
  if (!response.ok || !response.body) throw new Error(`Download failed (${response.status}): ${url}`)
  await pipeline(Readable.fromWeb(response.body), createWriteStream(partial))
  renameSync(partial, file)
  partials.delete(partial)
}

function sha256(file) {
  return createHash('sha256').update(readFileSync(file)).digest('hex').toLowerCase()
}

function verify(file, expected, label) {
  const actual = sha256(file)
  if (!/^[a-f0-9]{64}$/.test(expected) || actual !== expected.toLowerCase()) {
    rmSync(file, { force: true })
    throw new Error(`${label} SHA-256 verification failed. Expected ${expected}; received ${actual}`)
  }
}

async function fetchYtDlp() {
  const exe = path.join(root, 'yt-dlp.exe')
  if (existsSync(exe)) return
  // Use the stable "latest/download" redirect instead of the REST API: unauthenticated
  // API calls from shared GitHub-runner IPs are frequently rate-limited (HTTP 403).
  const base = 'https://github.com/yt-dlp/yt-dlp/releases/latest/download'
  await withRetry('yt-dlp', async () => {
    const sums = await fetchText(`${base}/SHA2-256SUMS`)
    const expected = sums.split('\n').find((line) => /\syt-dlp\.exe\s*$/.test(line))?.trim().split(/\s+/)[0]
    if (!expected) throw new Error('yt-dlp.exe is absent from SHA2-256SUMS')
    await download(`${base}/yt-dlp.exe`, exe)
    verify(exe, expected, 'yt-dlp')
  })
}

function extractZip(zip, destination) {
  rmSync(destination, { recursive: true, force: true })
  mkdirSync(destination, { recursive: true })
  if (process.platform === 'win32') {
    try {
      // Windows 10+/Server 2019+ ship bsdtar as tar.exe, which extracts zip archives.
      execFileSync('tar', ['-x', '-f', zip, '-C', destination], { stdio: 'inherit' })
    } catch {
      // Fallback: Expand-Archive with paths passed via environment variables
      // (previously "-Command ... $args[0]" received null because -Command does not populate $args).
      execFileSync('powershell.exe', ['-NoLogo', '-NoProfile', '-NonInteractive', '-Command',
        'Expand-Archive -LiteralPath $env:FB_ZIP -DestinationPath $env:FB_DEST -Force'],
      { stdio: 'inherit', env: { ...process.env, FB_ZIP: zip, FB_DEST: destination } })
    }
  } else {
    execFileSync('unzip', ['-q', zip, '-d', destination], { stdio: 'inherit' })
  }
}

function installFfmpegFrom(unpack) {
  const folder = readdirSync(unpack).map((name) => path.join(unpack, name)).find((name) => existsSync(path.join(name, 'bin', 'ffmpeg.exe')))
  if (!folder) throw new Error('FFmpeg archive layout is not recognized')
  for (const name of ['ffmpeg.exe', 'ffprobe.exe']) {
    rmSync(path.join(root, name), { force: true })
    renameSync(path.join(folder, 'bin', name), path.join(root, name))
  }
}

async function fetchFfmpegFromGyan() {
  const base = 'https://www.gyan.dev/ffmpeg/builds'
  const zip = path.resolve('resources/ffmpeg-release-essentials.zip')
  const expected = (await fetchText(`${base}/ffmpeg-release-essentials.zip.sha256`)).trim().split(/\s+/)[0]
  await download(`${base}/ffmpeg-release-essentials.zip`, zip)
  verify(zip, expected, 'FFmpeg archive (gyan.dev)')
  const unpack = path.resolve('resources/.ffmpeg-unpack')
  extractZip(zip, unpack)
  installFfmpegFrom(unpack)
  rmSync(zip, { force: true })
  rmSync(unpack, { recursive: true, force: true })
}

async function fetchFfmpegFromBtbn() {
  // Fallback mirror: official FFmpeg static builds published on GitHub by BtbN,
  // fetched through the stable "latest/download" redirect with a checksum file.
  const base = 'https://github.com/BtbN/FFmpeg-Builds/releases/latest/download'
  const asset = 'ffmpeg-master-latest-win64-gpl.zip'
  const zip = path.resolve(`resources/${asset}`)
  const sums = await fetchText(`${base}/checksums.sha256`)
  const expected = sums.split('\n').find((line) => line.includes(asset))?.trim().split(/\s+/)[0]
  if (!expected) throw new Error(`${asset} is absent from checksums.sha256`)
  await download(`${base}/${asset}`, zip)
  verify(zip, expected, 'FFmpeg archive (BtbN)')
  const unpack = path.resolve('resources/.ffmpeg-unpack')
  extractZip(zip, unpack)
  installFfmpegFrom(unpack)
  rmSync(zip, { force: true })
  rmSync(unpack, { recursive: true, force: true })
}

async function fetchFfmpeg() {
  const ffmpeg = path.join(root, 'ffmpeg.exe')
  const ffprobe = path.join(root, 'ffprobe.exe')
  if (existsSync(ffmpeg) && existsSync(ffprobe)) return
  try {
    await withRetry('FFmpeg (gyan.dev)', fetchFfmpegFromGyan, 2)
  } catch (error) {
    console.warn(`gyan.dev source failed (${error instanceof Error ? error.message : String(error)}); falling back to BtbN FFmpeg builds`)
    await withRetry('FFmpeg (BtbN)', fetchFfmpegFromBtbn, 3)
  }
}

function createBackgroundMusic() {
  const output = path.resolve('resources/music/background_lofi.mp3')
  if (existsSync(output)) return
  mkdirSync(path.dirname(output), { recursive: true })
  execFileSync(path.join(root, 'ffmpeg.exe'), ['-hide_banner','-loglevel','error','-f','lavfi','-i','sine=frequency=220:duration=30:sample_rate=44100','-f','lavfi','-i','sine=frequency=277.18:duration=30:sample_rate=44100','-filter_complex','[0:a]volume=0.12[a0];[1:a]volume=0.08[a1];[a0][a1]amix=inputs=2,lowpass=f=2200,afade=t=in:d=2,afade=t=out:st=28:d=2[a]','-map','[a]','-codec:a','libmp3lame','-b:a','128k','-y',output], { stdio: 'inherit' })
}

try {
  await Promise.all([fetchYtDlp(), fetchFfmpeg()])
  createBackgroundMusic()
  for (const name of ['yt-dlp.exe', 'ffmpeg.exe', 'ffprobe.exe']) {
    const file = path.join(root, name)
    console.log(`${name}: ${(statSync(file).size / 1_048_576).toFixed(1)} MB, SHA-256 ${sha256(file)}`)
  }
} catch (error) {
  cleanup()
  throw error
}
