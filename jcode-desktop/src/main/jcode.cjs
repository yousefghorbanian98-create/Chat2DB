'use strict';
/**
 * Locates, verifies and (when needed) self-downloads the real `jcode`
 * executable. jcode is the AI coding agent from https://github.com/1jehuang/jcode
 *
 * Resolution order:
 *   1. Bundled with the app   -> resources/bin/<platform>-<arch>/jcode[.exe]
 *   2. Self-downloaded cache  -> userData/bin/<platform>-<arch>/jcode[.exe]
 *
 * When missing, `ensure()` downloads the official release asset for the current
 * platform from GitHub and verifies its SHA256 against the release's SHA256SUMS
 * file. Progress is reported through the `onProgress` callback.
 */
const fs = require('fs');
const path = require('path');
const os = require('os');
const https = require('https');
const crypto = require('crypto');
const { spawn, execFile } = require('child_process');

const REPO = '1jehuang/jcode';
const GITHUB_API = 'https://api.github.com';
const GITHUB_DL = 'https://github.com';

function platformId() {
  const p = os.platform(); // win32 | darwin | linux
  const a = os.arch(); // x64 | arm64 | ...
  if (p === 'win32') return `win32-${a}`;
  if (p === 'darwin') return `macos-${a}`;
  return `linux-${a}`;
}

function binaryName(pid) {
  return pid.startsWith('win32') ? 'jcode.exe' : 'jcode';
}

function assetName(pid, tag) {
  // Official asset names, e.g. jcode-windows-x86_64.exe / jcode-linux-x86_64.tar.gz
  const map = {
    'win32-x64': 'jcode-windows-x86_64.exe',
    'win32-arm64': 'jcode-windows-aarch64.exe',
    'darwin-x64': 'jcode-macos-x86_64.tar.gz',
    'darwin-arm64': 'jcode-macos-aarch64.tar.gz',
    'linux-x64': 'jcode-linux-x86_64.tar.gz',
    'linux-arm64': 'jcode-linux-aarch64.tar.gz'
  };
  return map[pid] || `jcode-${pid.replace('_', '-')}.tar.gz`;
}

function bundledPath(processResourcesPath, pid) {
  if (!processResourcesPath) return null;
  return path.join(processResourcesPath, 'bin', pid, binaryName(pid));
}

function cachedPath(userDataPath, pid) {
  return path.join(userDataPath, 'bin', pid, binaryName(pid));
}

function resolve(userDataPath, processResourcesPath) {
  const pid = platformId();
  const candidates = [
    bundledPath(processResourcesPath, pid),
    cachedPath(userDataPath, pid)
  ];
  for (const c of candidates) {
    if (c && fs.existsSync(c)) return { path: c, pid, bundled: c === candidates[0] };
  }
  return { path: null, pid, bundled: false };
}

function versionOf(binPath, cb) {
  execFile(binPath, ['--version'], { timeout: 15000 }, (err, stdout) => {
    if (err) return cb(err);
    cb(null, (stdout || '').trim());
  });
}

/* ---------------- download helpers ---------------- */

function getJSON(url, cb) {
  const req = https.get(
    url,
    { headers: { 'User-Agent': 'jcode-desktop', Accept: 'application/vnd.github+json' } },
    (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        res.resume();
        return getJSON(res.headers.location, cb);
      }
      if (res.statusCode !== 200) {
        res.resume();
        return cb(new Error('HTTP ' + res.statusCode));
      }
      let body = '';
      res.setEncoding('utf8');
      res.on('data', (d) => (body += d));
      res.on('end', () => {
        try {
          cb(null, JSON.parse(body));
        } catch (e) {
          cb(e);
        }
      });
    }
  );
  req.on('error', cb);
  req.setTimeout(30000, () => req.destroy(new Error('timeout')));
}

function downloadTo(url, dest, onProgress, cb) {
  const req = https.get(
    url,
    { headers: { 'User-Agent': 'jcode-desktop', Accept: 'application/octet-stream' } },
    (res) => {
      if (res.statusCode >= 300 && res.statusCode < 400 && res.headers.location) {
        res.resume();
        return downloadTo(res.headers.location, dest, onProgress, cb);
      }
      if (res.statusCode !== 200) {
        res.resume();
        return cb(new Error('HTTP ' + res.statusCode));
      }
      const total = parseInt(res.headers['content-length'], 10) || 0;
      let received = 0;
      const tmp = dest + '.part';
      const out = fs.createWriteStream(tmp);
      res.on('data', (chunk) => {
        received += chunk.length;
        if (onProgress && total) onProgress({ received, total, pct: Math.round((received / total) * 100) });
      });
      res.pipe(out);
      out.on('finish', () => {
        out.close(() => {
          fs.renameSync(tmp, dest);
          cb(null, dest);
        });
      });
      out.on('error', cb);
    }
  );
  req.on('error', cb);
  req.setTimeout(60000, () => req.destroy(new Error('timeout')));
}

function extractTarGz(src, destDir) {
  // Minimal tar.gz extraction using the `tar` binary present on macOS/Linux.
  return new Promise((resolve, reject) => {
    execFile('tar', ['-xzf', src, '-C', destDir], (err) => (err ? reject(err) : resolve()));
  });
}

function verifySha256(file, expected) {
  return new Promise((resolve, reject) => {
    const hash = crypto.createHash('sha256');
    const s = fs.createReadStream(file);
    s.on('data', (d) => hash.update(d));
    s.on('end', () => resolve(hash.digest('hex') === expected.trim().toLowerCase()));
    s.on('error', reject);
  });
}

/**
 * Ensures a jcode binary is available. Downloads it when missing.
 * @param {object} opts { userDataPath, processResourcesPath, force, onProgress }
 * @returns {Promise<{path:string, downloaded:boolean, version:string|null}>}
 */
function ensure(opts) {
  const { userDataPath, processResourcesPath } = opts;
  const pid = platformId();
  const cached = cachedPath(userDataPath, pid);
  const resolved = resolve(userDataPath, processResourcesPath);

  if (resolved.path && !opts.force) {
    return new Promise((res) => {
      versionOf(resolved.path, (err, v) => res({ path: resolved.path, downloaded: false, version: err ? null : v }));
    });
  }

  return new Promise((resolvePromise, rejectPromise) => {
    const onProgress = opts.onProgress || (() => {});
    onProgress({ phase: 'meta', pct: 0 });

    // 1. Find latest release + asset url + SHA256SUMS
    getJSON(`${GITHUB_API}/repos/${REPO}/releases/latest`, (err, release) => {
      if (err) return rejectPromise(new Error('Could not reach GitHub releases: ' + err.message));
      const asset = (release.assets || []).find((a) => a.name === assetName(pid, release.tag_name));
      if (!asset) return rejectPromise(new Error('No jcode binary for platform ' + pid + ' in release ' + release.tag_name));
      const sumsAsset = (release.assets || []).find((a) => a.name === 'SHA256SUMS');
      const tag = release.tag_name;

      const doDownload = (sumsText) => {
        const expectedLine = (sumsText || '').split('\n').find((l) => l.includes(asset.name));
        const expected = expectedLine ? expectedLine.split(/\s+/)[0] : null;
        fs.mkdirSync(path.dirname(cached), { recursive: true });

        downloadTo(
          `${GITHUB_DL}/${REPO}/releases/download/${tag}/${asset.name}`,
          cached + (asset.name.endsWith('.tar.gz') ? '.tar.gz' : ''),
          (p) => onProgress({ phase: 'download', ...p, asset: asset.name }),
          async (err2, downloaded) => {
            if (err2) return rejectPromise(new Error('Download failed: ' + err2.message));
            try {
              let finalPath = cached;
              if (asset.name.endsWith('.tar.gz')) {
                await extractTarGz(downloaded, path.dirname(cached));
                fs.unlinkSync(downloaded);
                const inner = path.join(path.dirname(cached), 'jcode');
                if (fs.existsSync(inner)) fs.renameSync(inner, finalPath);
                else {
                  const list = fs.readdirSync(path.dirname(cached));
                  const found = list.find((f) => /^jcode/i.test(f));
                  if (found) fs.renameSync(path.join(path.dirname(cached), found), finalPath);
                }
              }
              if (expected) {
                const ok = await verifySha256(finalPath, expected);
                if (!ok) {
                  fs.unlinkSync(finalPath);
                  return rejectPromise(new Error('Checksum mismatch for ' + asset.name));
                }
              }
              fs.chmodSync(finalPath, 0o755);
              onProgress({ phase: 'done', pct: 100 });
              versionOf(finalPath, (vErr, v) => resolvePromise({ path: finalPath, downloaded: true, version: vErr ? null : v }));
            } catch (e3) {
              rejectPromise(e3);
            }
          }
        );
      };

      if (!sumsAsset) return doDownload('');
      getJSON(`${GITHUB_API}/repos/${REPO}/releases/assets/${sumsAsset.id}`, () => {});
      downloadTo(
        `${GITHUB_DL}/${REPO}/releases/download/${tag}/SHA256SUMS`,
        path.join(path.dirname(cached), 'SHA256SUMS'),
        null,
        (err3, sumsFile) => {
          if (err3) return doDownload('');
          fs.readFile(sumsFile, 'utf8', (rerr, txt) => {
            fs.unlink(sumsFile, () => {});
            doDownload(rerr ? '' : txt);
          });
        }
      );
    });
  });
}

function spawnJcode(binPath, args, opts) {
  return spawn(binPath, args, {
    cwd: opts.cwd || os.homedir(),
    env: { ...process.env, TERM: 'xterm-256color', COLORTERM: 'truecolor', ...(opts.env || {}) },
    windowsHide: true
  });
}

module.exports = { resolve, ensure, versionOf, platformId, binaryName, spawnJcode, REPO };
