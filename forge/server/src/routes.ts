import type { IncomingMessage, ServerResponse } from 'node:http'
import { stat, readFile } from 'node:fs/promises'
import { join, extname, resolve, normalize } from 'node:path'
import { config } from './config'
import type { AppContext } from './context'
import { checkForUpdate, applyUpdate } from './update-service'

const MIME: Record<string, string> = {
  '.html': 'text/html; charset=utf-8',
  '.js': 'text/javascript; charset=utf-8',
  '.css': 'text/css; charset=utf-8',
  '.json': 'application/json; charset=utf-8',
  '.svg': 'image/svg+xml',
  '.png': 'image/png',
  '.ico': 'image/x-icon',
  '.woff2': 'font/woff2',
  '.woff': 'font/woff',
  '.map': 'application/json; charset=utf-8',
}

/**
 * سروِ فایل‌های رابط کاربری (تک-مبدأ).
 * اگر پوشه‌ی رابط وجود نداشته باشد، ۵۰۳ می‌دهد تا علت روشن باشد.
 */
export async function serveStatic(req: IncomingMessage, res: ServerResponse): Promise<void> {
  if (!config.webDir) {
    res.writeHead(503, { 'content-type': 'text/plain; charset=utf-8' })
    res.end('رابط کاربری ساخته نشده است (webDir یافت نشد)')
    return
  }

  const url = new URL(req.url ?? '/', `http://${req.headers.host ?? 'localhost'}`)
  const requested = decodeURIComponent(url.pathname)
  const root = config.webDir

  // ایمنی: مسیر باید درون پوشه‌ی ریشه بماند (جلوگیری از path traversal)
  const candidate = resolve(join(root, normalize(requested)))
  if (!candidate.startsWith(resolve(root))) {
    res.writeHead(403, { 'content-type': 'text/plain; charset=utf-8' })
    res.end('forbidden')
    return
  }

  const tryServe = async (file: string): Promise<boolean> => {
    try {
      const info = await stat(file)
      if (!info.isFile()) return false
      const body = await readFile(file)
      res.writeHead(200, {
        'content-type': MIME[extname(file)] ?? 'application/octet-stream',
        'cache-control': extname(file) === '.html' ? 'no-store' : 'public, max-age=3600',
      })
      res.end(body)
      return true
    } catch {
      return false
    }
  }

  if (await tryServe(candidate)) return
  // فایل نبود → index.html (برای مسیرهای SPA)
  if (await tryServe(join(root, 'index.html'))) return

  res.writeHead(404, { 'content-type': 'text/plain; charset=utf-8' })
  res.end('not found')
}

function sendJson(res: ServerResponse, status: number, body: unknown): void {
  const payload = JSON.stringify(body)
  res.writeHead(status, {
    'content-type': 'application/json; charset=utf-8',
    'cache-control': 'no-store',
    'access-control-allow-origin': '*',
  })
  res.end(payload)
}

async function readBody(req: IncomingMessage): Promise<string> {
  const chunks: Buffer[] = []
  for await (const c of req) chunks.push(c as Buffer)
  return Buffer.concat(chunks).toString('utf8')
}

export async function handleApi(
  req: IncomingMessage,
  res: ServerResponse,
  ctx: AppContext,
): Promise<boolean> {
  const url = new URL(req.url ?? '/', `http://${req.headers.host ?? 'localhost'}`)
  const path = url.pathname

  if (!path.startsWith('/api/')) return false

  if (req.method === 'OPTIONS') {
    res.writeHead(204, {
      'access-control-allow-origin': '*',
      'access-control-allow-methods': 'GET,POST,OPTIONS',
      'access-control-allow-headers': 'content-type',
    })
    res.end()
    return true
  }

  // ---- وضعیت سلامت (AC-1 و AC-2) ----
  if (path === '/api/health' && req.method === 'GET') {
    const statuses = await Promise.all(ctx.adapters.map((a) => a.health()))
    sendJson(res, 200, {
      ok: true,
      service: 'forge',
      version: '0.1.0',
      port: config.port,
      skillsDir: config.skillsDir,
      adapters: statuses,
    })
    return true
  }

  if (path === '/api/commands' && req.method === 'GET') {
    sendJson(res, 200, ctx.godmode.listCommands())
    return true
  }

  if (path === '/api/agents' && req.method === 'GET') {
    sendJson(res, 200, ctx.godmode.listAgents())
    return true
  }

  if (path === '/api/skills' && req.method === 'GET') {
    sendJson(res, 200, {
      count: ctx.soup.skillCount,
      names: ctx.godmode.listCommands().map((c) => c.slug).concat(ctx.godmode.listAgents().map((a) => a.slug)),
    })
    return true
  }

  if (path === '/api/mcp' && req.method === 'GET') {
    sendJson(res, 200, ctx.mcp.list())
    return true
  }

  if (path === '/api/usage' && req.method === 'GET') {
    sendJson(res, 200, await ctx.store.getUsage())
    return true
  }

  // ---- به‌روزرسانیِ تفاضلی ----
  if (path === '/api/update/check' && req.method === 'GET') {
    sendJson(res, 200, await checkForUpdate())
    return true
  }

  if (path === '/api/update/apply' && req.method === 'POST') {
    sendJson(res, 200, await applyUpdate())
    return true
  }

  // ---- نشست‌ها ----
  if (path === '/api/sessions' && req.method === 'GET') {
    sendJson(res, 200, await ctx.store.listSessions())
    return true
  }

  if (path === '/api/sessions' && req.method === 'POST') {
    const raw = await readBody(req)
    let title = 'نشست جدید'
    try {
      const parsed = JSON.parse(raw || '{}') as { title?: string }
      if (parsed.title) title = parsed.title
    } catch {
      // بدنه نامعتبر → عنوان پیش‌فرض
    }
    sendJson(res, 201, await ctx.store.createSession(title))
    return true
  }

  const sessionMatch = /^\/api\/sessions\/([\w-]+)$/.exec(path)
  if (sessionMatch && req.method === 'DELETE') {
    const ok = await ctx.store.deleteSession(sessionMatch[1])
    sendJson(res, ok ? 200 : 404, ok ? { deleted: true } : { error: 'session-not-found' })
    return true
  }

  if (sessionMatch && req.method === 'GET') {
    const session = await ctx.store.getSession(sessionMatch[1])
    if (!session) {
      sendJson(res, 404, { error: 'session-not-found' })
      return true
    }
    sendJson(res, 200, session)
    return true
  }

  // ---- اجرا (SSE) ----
  if (path === '/api/run' && req.method === 'GET') {
    const prompt = (url.searchParams.get('prompt') ?? '').trim()
    if (!prompt) {
      sendJson(res, 400, { error: 'missing-prompt' })
      return true
    }
    const sessionId = url.searchParams.get('sessionId')

    res.writeHead(200, {
      'content-type': 'text/event-stream; charset=utf-8',
      'cache-control': 'no-cache, no-transform',
      connection: 'keep-alive',
      'access-control-allow-origin': '*',
      'x-accel-buffering': 'no',
    })

    const write = (event: unknown) => res.write(`data: ${JSON.stringify(event)}\n\n`)
    let promptTokens = 0

    try {
      if (sessionId) {
        await ctx.store.appendMessage(sessionId, { role: 'user', text: prompt })
      }
      let finalText = ''
      for await (const ev of ctx.pipeline.run(prompt)) {
        write(ev)
        if (ev.type === 'token') promptTokens = Number(ev.text ?? 0)
        if (ev.type === 'result') finalText = ev.text ?? ''
      }
      if (sessionId) {
        await ctx.store.appendMessage(sessionId, { role: 'agent', text: finalText, stage: 'Done' })
        await ctx.store.addUsage(promptTokens, Math.max(1, Math.ceil(finalText.length / 4)))
      }
    } catch (err) {
      write({ type: 'error', text: err instanceof Error ? err.message : 'خطای ناشناخته' })
    } finally {
      res.end()
    }
    return true
  }

  // ---- پیش‌نمایشِ مسیریابی (بدون اجرا) ----
  if (path === '/api/route' && req.method === 'GET') {
    const q = url.searchParams.get('q') ?? ''
    sendJson(res, 200, ctx.soup.explain(q))
    return true
  }

  sendJson(res, 404, { error: 'not-found', path })
  return true
}
