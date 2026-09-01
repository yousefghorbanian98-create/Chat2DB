/**
 * Live preview server for Jcode Desktop.
 * Serves the renderer + a real PTY (bash) over WebSocket so the terminal is
 * genuinely functional in the browser preview. In the packaged desktop app the
 * same renderer talks to the Electron main process instead.
 */
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import os from 'node:os';
import { fileURLToPath } from 'node:url';
import { createRequire } from 'node:module';
import { WebSocketServer } from 'ws';

const require = createRequire(import.meta.url);
const pty = require('node-pty');

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(__dirname, '..');
const PORT = process.env.PORT || 4173;

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.mjs': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.gif': 'image/gif',
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.mp4': 'video/mp4',
  '.webm': 'video/webm',
  '.ico': 'image/x-icon',
  '.woff2': 'font/woff2',
  '.woff': 'font/woff',
  '.map': 'application/json'
};

const server = http.createServer((req, res) => {
  let urlPath = decodeURIComponent(new URL(req.url, 'http://x').pathname);
  if (urlPath === '/') urlPath = '/src/renderer/index.html';

  // Guard against path traversal
  const file = path.normalize(path.join(ROOT, urlPath));
  if (!file.startsWith(ROOT)) { res.writeHead(403); return res.end('forbidden'); }

  fs.stat(file, (err, stat) => {
    if (err || !stat.isFile()) { res.writeHead(404); return res.end('not found'); }
    res.writeHead(200, {
      'Content-Type': MIME[path.extname(file).toLowerCase()] || 'application/octet-stream',
      'Cache-Control': 'no-store'
    });
    fs.createReadStream(file).pipe(res);
  });
});

const wss = new WebSocketServer({ server });

const sessions = new Map();

function welcomeBanner() {
  return [
    '\u001b[38;5;141m',
    '  ╭──────────────────────────────────────────────────────────╮\r\n',
    '  │          ✦  JCODE DESKTOP — LIVE PREVIEW  ✦             │\r\n',
    '  │   This preview runs a real shell inside the cosmic UI.  │\r\n',
    '  │   In the installed Windows app this pane runs the real  │\r\n',
    '  │   jcode AI agent (github.com/1jehuang/jcode).           │\r\n',
    '  ╰──────────────────────────────────────────────────────────╯\r\n',
    '\u001b[0m'
  ].join('');
}

wss.on('connection', (ws) => {
  ws.on('message', (raw) => {
    let msg;
    try { msg = JSON.parse(raw.toString()); } catch (_) { return; }

    if (msg.type === 'create') {
      const shell = process.platform === 'win32' ? 'powershell.exe' : (process.env.SHELL || '/bin/bash');
      try {
        const term = pty.spawn(shell, [], {
          name: 'xterm-256color',
          cols: msg.cols || 110,
          rows: msg.rows || 32,
          cwd: (msg.cwd && msg.cwd !== '~') ? msg.cwd : os.homedir(),
          env: { ...process.env, TERM: 'xterm-256color', COLORTERM: 'truecolor' }
        });
        sessions.set(msg.id, term);
        term.onData((data) => ws.send(JSON.stringify({ type: 'data', id: msg.id, data })));
        term.onExit(({ exitCode }) => {
          sessions.delete(msg.id);
          ws.send(JSON.stringify({ type: 'exit', id: msg.id, code: exitCode, signal: 0 }));
        });
        ws.send(JSON.stringify({ type: 'created', id: msg.id, meta: { cwd: msg.cwd || '~', pid: term.pid } }));
        term.write(welcomeBanner());
        term.write(`\r\n\u001b[38;5;245m${(msg.cwd && msg.cwd !== '~') ? msg.cwd : os.homedir()}\u001b[0m $ `);
      } catch (err) {
        ws.send(JSON.stringify({ type: 'error', id: msg.id, error: err.message }));
      }
    } else if (msg.type === 'write') {
      const t = sessions.get(msg.id);
      if (t) t.write(msg.data);
    } else if (msg.type === 'resize') {
      const t = sessions.get(msg.id);
      if (t && msg.cols > 0 && msg.rows > 0) { try { t.resize(msg.cols, msg.rows); } catch (_) {} }
    } else if (msg.type === 'kill') {
      const t = sessions.get(msg.id);
      if (t) { try { t.kill(); } catch (_) {} sessions.delete(msg.id); }
    }
  });

  ws.on('close', () => {
    for (const [id, t] of sessions) { try { t.kill(); } catch (_) {} sessions.delete(id); }
  });
});

server.listen(PORT, '0.0.0.0', () => {
  console.log(`Jcode Desktop preview → http://localhost:${PORT}`);
});
