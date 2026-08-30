#!/usr/bin/env node
/**
 * Minimal static server for the G6 visual gate.
 *
 * Serves the production build (dist/) produced by G5 with SPA fallback to
 * index.html — memory-light (~50MB) so the sandbox's ~4GB RAM can also fit
 * the Playwright Chromium without OOM kills (the webpack dev server alone
 * used ~2.7GB and died alongside the browser).
 */
'use strict';

const http = require('node:http');
const fs = require('node:fs');
const path = require('node:path');

const ROOT = path.resolve(__dirname, '../..');
const DIST = path.join(ROOT, 'dist');
const PORT = Number(process.env.PORT || 8889);
const HOST = process.env.HOST || '127.0.0.1';

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
  console.log(`serve-dist listening on http://${HOST}:${PORT} (${DIST})`);
});

process.on('SIGTERM', () => {
  server.close(() => process.exit(0));
});
