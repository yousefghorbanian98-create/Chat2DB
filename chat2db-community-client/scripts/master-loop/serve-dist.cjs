#!/usr/bin/env node
/**
 * Minimal static server for the production build (dist/).
 *
 * Serves the production build with SPA fallback to index.html — memory-light
 * so it can run next to a browser on small machines.
 *
 * Works in two layouts:
 *   - repository layout:  <client>/scripts/master-loop/serve-dist.cjs  → <client>/dist
 *   - packaged layout:    <pkg>/serve-dist.cjs with <pkg>/dist/ next to it
 *
 * Usage:
 *   node serve-dist.cjs [--open]        (PORT=8890 to change the port)
 */
'use strict';

const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');
const { exec } = require('node:child_process');

const SCRIPT_DIR = __dirname;
const LOCAL_DIST = path.join(SCRIPT_DIR, 'dist');
const REPO_DIST = path.resolve(SCRIPT_DIR, '../..', 'dist');

const args = process.argv.slice(2);
const openBrowser = args.includes('--open');

const PORT = Number(process.env.PORT || 8889);
const HOST = process.env.HOST || '127.0.0.1';

// Layout detection:
//   - packaged: <pkg>/serve-dist.cjs + <pkg>/index.html next to it
//   - packaged v2: <pkg>/dist/  + <pkg>/serve-dist.cjs
//   - repository: <client>/scripts/master-loop/serve-dist.cjs → <client>/dist
let DIST = null;
if (fs.existsSync(path.join(SCRIPT_DIR, 'index.html'))) {
  DIST = SCRIPT_DIR;
} else if (fs.existsSync(path.join(LOCAL_DIST, 'index.html'))) {
  DIST = LOCAL_DIST;
} else if (fs.existsSync(path.join(REPO_DIST, 'index.html'))) {
  DIST = REPO_DIST;
}
if (!DIST) {
  console.error(
    'dist/index.html not found — run the build first (yarn build:web:community) or place this script next to the dist files',
  );
  process.exit(1);
}

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'text/javascript',
  '.css': 'text/css',
  '.json': 'application/json',
  '.png': 'image/png',
  '.svg': 'image/svg+xml',
  '.ico': 'image/x-icon',
  '.woff': 'font/woff',
  '.woff2': 'font/woff2',
  '.ttf': 'font/ttf',
  '.map': 'application/json',
};

const server = http.createServer((req, res) => {
  let pathname = decodeURIComponent(new URL(req.url, `http://${req.headers.host}`).pathname);
  if (pathname === '/') pathname = '/index.html';
  let filePath = path.join(DIST, pathname);
  if (!filePath.startsWith(DIST)) {
    res.writeHead(403);
    res.end('forbidden');
    return;
  }
  if (!fs.existsSync(filePath) || fs.statSync(filePath).isDirectory()) {
    // The build uses relative asset paths ("./umi.js"), which the browser
    // resolves against the nested route (e.g. /settings/umi.js). Resolve
    // asset-like paths against the dist root; everything else is SPA-routed.
    const basename = path.basename(pathname);
    const rootFile = path.join(DIST, basename);
    if (path.extname(basename) && fs.existsSync(rootFile)) {
      filePath = rootFile;
    } else {
      filePath = path.join(DIST, 'index.html'); // SPA fallback
    }
  }
  const ext = path.extname(filePath).toLowerCase();
  res.writeHead(200, {
    'Content-Type': MIME[ext] || 'application/octet-stream',
    'Cache-Control': 'no-store',
  });
  fs.createReadStream(filePath).pipe(res);
});

server.listen(PORT, HOST, () => {
  const url = `http://${HOST}:${PORT}`;
  console.log(`serve-dist listening on ${url} (serving ${DIST})`);
  if (openBrowser) {
    const cmd =
      process.platform === 'win32'
        ? `start "" "${url}"`
        : process.platform === 'darwin'
          ? `open "${url}"`
          : `xdg-open "${url}" >/dev/null 2>&1 || sensible-browser "${url}" >/dev/null 2>&1 || true`;
    exec(cmd, (err) => {
      if (err) {
        console.log(`open the browser manually: ${url}`);
      } else {
        console.log(`browser opened at ${url}`);
      }
    });
  }
});

process.on('SIGTERM', () => {
  server.close(() => process.exit(0));
});
