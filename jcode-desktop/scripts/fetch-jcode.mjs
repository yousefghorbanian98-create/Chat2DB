/**
 * Downloads the official jcode binary into resources/bin for electron-builder.
 *
 *   node scripts/fetch-jcode.mjs [--all] [version-tag]
 *
 * By default it fetches ONLY the binary for the current platform:
 *   win32  -> resources/bin/win32-x64/jcode.exe
 *   linux  -> resources/bin/linux-x64/jcode
 *   darwin -> resources/bin/macos-{arch}/jcode
 * Pass --all to fetch every platform.
 *
 * Robustness notes (CI-friendly):
 *  - Prefers the `gh` CLI when available (pre-authenticated on Actions).
 *  - Otherwise resolves the latest tag from the `releases/latest` redirect
 *    (no api.github.com dependency → no unauthenticated rate limits).
 *  - Streams downloads to disk and retries transient failures.
 */
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
const BIN = path.join(ROOT, 'resources', 'bin');
const REPO = '1jehuang/jcode';
const WEB = 'https://github.com';

const ALL_TARGETS = [
  { pid: 'win32-x64', asset: 'jcode-windows-x86_64.exe', out: 'jcode.exe' },
  { pid: 'win32-arm64', asset: 'jcode-windows-aarch64.exe', out: 'jcode.exe' },
  { pid: 'linux-x64', asset: 'jcode-linux-x86_64.tar.gz', out: 'jcode', extract: true },
  { pid: 'linux-arm64', asset: 'jcode-linux-aarch64.tar.gz', out: 'jcode', extract: true },
  { pid: 'macos-x64', asset: 'jcode-macos-x86_64.tar.gz', out: 'jcode', extract: true },
  { pid: 'macos-arm64', asset: 'jcode-macos-aarch64.tar.gz', out: 'jcode', extract: true }
];

function currentPid() {
  const p = os.platform();
  const a = os.arch();
  if (p === 'win32') return a === 'arm64' ? 'win32-arm64' : 'win32-x64';
  if (p === 'darwin') return a === 'arm64' ? 'macos-arm64' : 'macos-x64';
  return a === 'arm64' ? 'linux-arm64' : 'linux-x64';
}

function pickTargets(all) {
  if (all) return ALL_TARGETS;
  const pid = currentPid();
  return ALL_TARGETS.filter((t) => t.pid === pid);
}

function hasGh() {
  try {
    execFileSync('gh', ['--version'], { stdio: 'ignore' });
    return true;
  } catch (_) {
    return false;
  }
}

function ghJson(args) {
  const out = execFileSync('gh', ['api', ...args], { encoding: 'utf8', stdio: ['ignore', 'pipe', 'ignore'] });
  return JSON.parse(out);
}

function ghTagLatest() {
  // --jq returns the raw string, not JSON.
  const out = execFileSync('gh', ['api', `repos/${REPO}/releases/latest`, '--jq', '.tag_name'], {
    encoding: 'utf8',
    stdio: ['ignore', 'pipe', 'ignore']
  });
  return out.trim();
}

/** Resolve the latest release tag. Tries, in order: gh api → releases/latest redirect. */
async function resolveTag(versionArg) {
  if (versionArg) return versionArg;
  if (hasGh()) {
    try {
      const tag = ghTagLatest();
      if (tag) return tag;
    } catch (e) {
      console.log('  gh api failed (' + e.message + '), falling back to redirect…');
    }
  }
  const res = await fetch(`${WEB}/${REPO}/releases/latest`, { redirect: 'manual', headers: { 'User-Agent': 'jcode-desktop' } });
  const loc = res.headers.get('location') || '';
  const m = loc.match(/\/tag\/([^/?]+)/);
  if (res.status === 302 && m) return m[1];
  throw new Error('Could not resolve latest release tag (HTTP ' + res.status + ')');
}

async function httpDownload(url, dest, tries = 3) {
  let lastErr;
  for (let i = 1; i <= tries; i++) {
    try {
      const res = await fetch(url, { headers: { 'User-Agent': 'jcode-desktop', Accept: 'application/octet-stream' }, redirect: 'follow' });
      if (!res.ok || !res.body) throw new Error('HTTP ' + res.status);
      const total = Number(res.headers.get('content-length') || 0);
      fs.mkdirSync(path.dirname(dest), { recursive: true });
      const tmp = dest + '.part';
      const out = fs.createWriteStream(tmp);
      let received = 0;
      for await (const chunk of res.body) {
        out.write(chunk);
        received += chunk.length;
        if (total && i === 1) process.stdout.write(`\r  ${(received / 1024 / 1024).toFixed(1)} / ${(total / 1024 / 1024).toFixed(1)} MB`);
      }
      out.end();
      await new Promise((resolve, reject) => out.on('finish', resolve).on('error', reject));
      process.stdout.write('\n');
      fs.renameSync(tmp, dest);
      return;
    } catch (e) {
      lastErr = e;
      process.stderr.write(`  attempt ${i}/${tries}: ${e.message}\n`);
      if (i < tries) await new Promise((r) => setTimeout(r, 2000 * i));
    }
  }
  throw lastErr;
}

function ghDownload(asset, dest, tag) {
  execFileSync('gh', [
    'release', 'download', tag,
    '--repo', REPO,
    '--pattern', asset,
    '--output', dest,
    '--clobber'
  ], { stdio: 'inherit' });
}

function extractTarGz(src, destDir) {
  execFileSync('tar', ['-xzf', src, '-C', destDir], { stdio: 'inherit' });
}

async function main() {
  const args = process.argv.slice(2);
  const all = args.includes('--all');
  const versionArg = args.find((a) => /^v\d/.test(a));

  console.log('· jcode engine fetch — platform:', currentPid(), all ? '(all)' : '');
  const tag = await resolveTag(versionArg);
  console.log('· release: ' + tag);

  for (const t of pickTargets(all)) {
    const destDir = path.join(BIN, t.pid);
    const dest = path.join(destDir, t.out);
    fs.mkdirSync(destDir, { recursive: true });
    const url = `${WEB}/${REPO}/releases/download/${tag}/${t.asset}`;
    console.log('· ' + t.asset + ' → resources/bin/' + t.pid + '/' + t.out);

    let ok = false;
    if (hasGh()) {
      try {
        ghDownload(t.asset, dest, tag);
        ok = true;
      } catch (e) {
        console.log('  gh download failed (' + e.message + '), falling back to HTTPS…');
      }
    }
    if (!ok) await httpDownload(url, dest);

    if (t.extract) {
      const tmp = dest + '.tar.gz';
      fs.renameSync(dest, tmp);
      extractTarGz(tmp, destDir);
      fs.rmSync(tmp, { force: true });
      const extracted = fs.readdirSync(destDir).find((f) => /^jcode$/i.test(f));
      if (extracted && extracted !== t.out) fs.renameSync(path.join(destDir, extracted), dest);
    }

    try { fs.chmodSync(dest, 0o755); } catch (_) {}
    const size = fs.statSync(dest).size;
    console.log('  ✓ ' + (size / 1024 / 1024).toFixed(1) + ' MB');
  }
  console.log('Done.');
}

main().catch((e) => {
  console.error('\nfetch-jcode failed:', e && e.message ? e.message : e);
  if (e && e.stack) console.error(e.stack);
  process.exit(1);
});
