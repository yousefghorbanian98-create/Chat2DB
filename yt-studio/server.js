'use strict';

const http = require('http');
const fs = require('fs');
const path = require('path');
const { getChannelData, YouTubeError } = require('./lib/youtube');
const { buildSample } = require('./lib/sample');
const { analyze } = require('./lib/analyze');

// ---- tiny .env loader (no dependencies) ------------------------------------
function loadEnv() {
  const file = path.join(__dirname, '.env');
  if (!fs.existsSync(file)) return;
  for (const line of fs.readFileSync(file, 'utf8').split('\n')) {
    const m = /^\s*([\w.-]+)\s*=\s*(.*)?\s*$/.exec(line);
    if (!m) continue;
    let val = (m[2] || '').trim();
    if (/^(['"]).*\1$/.test(val)) val = val.slice(1, -1);
    if (!process.env[m[1]]) process.env[m[1]] = val;
  }
}
loadEnv();

const PORT = Number(process.env.PORT || 3000);
const HOST = '0.0.0.0';
const PUBLIC = path.join(__dirname, 'public');

const MIME = {
  '.html': 'text/html; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.ico': 'image/x-icon',
};

const CACHE = new Map(); // key -> { at, payload }
const CACHE_TTL = 10 * 60 * 1000;

function json(res, code, obj) {
  const body = JSON.stringify(obj);
  res.writeHead(code, {
    'Content-Type': 'application/json; charset=utf-8',
    'Content-Length': Buffer.byteLength(body),
    'Cache-Control': 'no-store',
  });
  res.end(body);
}

function serveStatic(req, res, pathname) {
  const rel = pathname === '/' ? 'index.html' : pathname.replace(/^\/+/, '');
  const file = path.join(PUBLIC, rel);
  if (!file.startsWith(PUBLIC)) return json(res, 403, { error: 'forbidden' });

  fs.readFile(file, (err, buf) => {
    if (err) {
      res.writeHead(404, { 'Content-Type': 'text/plain; charset=utf-8' });
      return res.end('404 — صفحه پیدا نشد');
    }
    res.writeHead(200, {
      'Content-Type': MIME[path.extname(file)] || 'application/octet-stream',
      'Cache-Control': 'no-cache',
    });
    res.end(buf);
  });
}

const friendly = (e) => {
  if (!(e instanceof YouTubeError)) return { code: 500, msg: e.message || 'خطای ناشناخته' };
  switch (e.reason) {
    case 'quotaExceeded':
    case 'dailyLimitExceeded':
      return { code: 429, msg: 'سهمیه‌ی روزانه‌ی YouTube API تمام شد (۱۰٬۰۰۰ واحد). فردا دوباره تلاش کنید یا از حالت نمونه استفاده کنید.' };
    case 'keyInvalid':
    case 'badRequest':
      return { code: 400, msg: 'کلید API نامعتبر است. مقدار YOUTUBE_API_KEY را در فایل .env بررسی کنید.' };
    case 'accessNotConfigured':
      return { code: 403, msg: 'YouTube Data API v3 برای این پروژه فعال نشده. در Google Cloud Console آن را Enable کنید.' };
    case 'channelNotFound':
    case 'videoNotFound':
    case 'noUploads':
      return { code: 404, msg: e.message };
    default:
      return { code: e.status || 500, msg: e.message };
  }
};

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url, `http://${req.headers.host || 'localhost'}`);
  const p = url.pathname;

  if (p === '/api/status') {
    return json(res, 200, {
      hasKey: !!process.env.YOUTUBE_API_KEY,
      time: new Date().toISOString(),
    });
  }

  if (p === '/api/analyze') {
    const q = (url.searchParams.get('channel') || '').trim();
    const demo = url.searchParams.get('demo') === '1';
    const limit = Math.min(300, Math.max(20, Number(url.searchParams.get('limit') || 150)));
    const key = process.env.YOUTUBE_API_KEY;

    try {
      if (demo || !key) {
        const result = analyze(buildSample());
        result.notice = key
          ? 'حالت نمونه — داده‌ی ساختگی است.'
          : 'کلید YOUTUBE_API_KEY تنظیم نشده، بنابراین داده‌ی نمونه نمایش داده می‌شود. راهنمای فایل README را ببینید.';
        return json(res, 200, result);
      }
      if (!q) return json(res, 400, { error: 'نام یا لینک کانال را وارد کنید.' });

      const ck = `${q}::${limit}`;
      const hit = CACHE.get(ck);
      if (hit && Date.now() - hit.at < CACHE_TTL) {
        return json(res, 200, { ...hit.payload, cached: true });
      }

      const data = await getChannelData(q, key, limit);
      if (!data.videos.length) {
        return json(res, 404, { error: 'برای این کانال ویدیوی عمومی پیدا نشد.' });
      }
      const result = analyze(data);
      CACHE.set(ck, { at: Date.now(), payload: result });
      return json(res, 200, result);
    } catch (e) {
      const f = friendly(e);
      return json(res, f.code, { error: f.msg, reason: e.reason || null });
    }
  }

  if (p.startsWith('/api/')) return json(res, 404, { error: 'not found' });
  return serveStatic(req, res, p);
});

server.listen(PORT, HOST, () => {
  console.log(`YouTube Content Studio → http://${HOST}:${PORT}`);
  console.log(
    process.env.YOUTUBE_API_KEY
      ? '✅ کلید YouTube API پیدا شد — داده‌ی واقعی فعال است.'
      : '⚠️  کلید YouTube API تنظیم نشده — حالت نمونه فعال است (yt-studio/.env را بسازید).',
  );
});
