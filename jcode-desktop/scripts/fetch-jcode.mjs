/**
 * Downloads the official jcode binaries into resources/bin so electron-builder
 * can bundle them (extraResources). Run on a machine with full internet access,
 * or in CI (see .github/workflows/build-windows.yml).
 *
 *   node scripts/fetch-jcode.mjs [version]
 *
 * Defaults to the latest GitHub release.
 */
import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { execFileSync } from 'node:child_process';

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
const BIN = path.join(ROOT, 'resources', 'bin');
const API = 'https://api.github.com';
const DL = 'https://github.com';
const REPO = '1jehuang/jcode';

const TARGETS = [
  { pid: 'win32-x64', asset: 'jcode-windows-x86_64.exe', out: 'jcode.exe' },
  { pid: 'linux-x64', asset: 'jcode-linux-x86_64.tar.gz', out: 'jcode', extract: true }
];

function getJSON(url) {
  return fetch(url, { headers: { 'User-Agent': 'jcode-desktop', Accept: 'application/vnd.github+json' } }).then((r) => {
    if (!r.ok) throw new Error('HTTP ' + r.status + ' for ' + url);
    return r.json();
  });
}

async function download(url, dest) {
  const res = await fetch(url, { headers: { 'User-Agent': 'jcode-desktop', Accept: 'application/octet-stream' }, redirect: 'follow' });
  if (!res.ok) throw new Error('HTTP ' + res.status);
  const buf = Buffer.from(await res.arrayBuffer());
  fs.mkdirSync(path.dirname(dest), { recursive: true });
  fs.writeFileSync(dest, buf);
  return buf.length;
}

async function main() {
  const argVersion = process.argv[2];
  console.log('· Fetching jcode release info…');
  const release = argVersion
    ? await getJSON(`${API}/repos/${REPO}/releases/tags/${argVersion}`)
    : await getJSON(`${API}/repos/${REPO}/releases/latest`);
  const tag = release.tag_name;
  console.log('· Release: ' + tag);

  for (const t of TARGETS) {
    const destDir = path.join(BIN, t.pid);
    const dest = path.join(destDir, t.out);
    fs.mkdirSync(destDir, { recursive: true });
    const url = `${DL}/${REPO}/releases/download/${tag}/${t.asset}`;
    console.log('· Downloading ' + t.asset + ' …');
    const tmp = path.join(destDir, t.asset);
    const bytes = await download(url, tmp);
    console.log('  → ' + (bytes / 1024 / 1024).toFixed(1) + ' MB');
    if (t.extract) {
      execFileSync('tar', ['-xzf', tmp, '-C', destDir]);
      fs.rmSync(tmp);
      const extracted = fs.readdirSync(destDir).find((f) => /^jcode$/i.test(f));
      if (extracted && extracted !== t.out) fs.renameSync(path.join(destDir, extracted), dest);
    } else {
      fs.renameSync(tmp, dest);
    }
    fs.chmodSync(dest, 0o755);
    console.log('  ✓ ' + path.join('resources', 'bin', t.pid, t.out));
  }
  console.log('Done.');
}

main().catch((e) => {
  console.error('fetch-jcode failed:', e.message);
  process.exit(1);
});
