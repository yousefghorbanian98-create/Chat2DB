import test from 'node:test'
import assert from 'node:assert/strict'
import { createServer } from 'node:http'
import { ProviderAdapter, readSse, normalizeProvider } from '../dist/test-api.js'

/**
 * این تست‌ها ثابت می‌کنند «مغز» واقعاً با یک مدل حرف می‌زند —
 * چیزی که تا پیش از این در برنامه وجود نداشت.
 */

/** پایگاهِ مدلِ قلابی با همان قراردادِ OpenAI */
function startFake(openaiHandler) {
  return new Promise((resolvePromise) => {
    const server = createServer((req, res) => {
      let body = ''
      req.on('data', (d) => (body += d))
      req.on('end', () => {
        openaiHandler(req, res, body ? JSON.parse(body) : {})
      })
    })
    server.listen(0, '127.0.0.1', () => resolvePromise(server))
  })
}

test('تماس با مدل: پاسخِ جریانی جمع می‌شود و شمارشِ واقعی برمی‌گردد', async () => {
  let received = null
  const server = await startFake((req, res, body) => {
    received = body
    res.writeHead(200, { 'content-type': 'text/event-stream' })
    res.write(`data: ${JSON.stringify({ choices: [{ delta: { content: 'سلام ' } }] })}\n\n`)
    res.write(`data: ${JSON.stringify({ choices: [{ delta: { content: 'دنیا' } }] })}\n\n`)
    res.write(`data: ${JSON.stringify({ choices: [{}], usage: { prompt_tokens: 11, completion_tokens: 7 } })}\n\n`)
    res.write('data: [DONE]\n\n')
    res.end()
  })
  const port = server.address().port

  const provider = new ProviderAdapter({
    type: 'openai-compatible',
    baseUrl: `http://127.0.0.1:${port}/v1`,
    model: 'test-model',
    apiKey: 'k',
  })

  const result = await provider.complete([
    { role: 'system', content: 'دستورالعمل' },
    { role: 'user', content: 'چرا تست fail می‌شود؟' },
  ])

  assert.equal(result.text, 'سلام دنیا')
  assert.equal(result.promptTokens, 11)
  assert.equal(result.completionTokens, 7)

  // system prompt واقعاً فرستاده می‌شود (قبلاً اصلاً فرستاده نمی‌شد)
  assert.equal(received.messages[0].role, 'system')
  assert.equal(received.messages[0].content, 'دستورالعمل')
  assert.equal(received.model, 'test-model')

  server.close()
})

test('مدلِ پیکربندی‌نشده «missing» گزارش می‌شود، نه خطا', async () => {
  const provider = new ProviderAdapter(null)
  const status = await provider.health()
  assert.equal(status.state, 'missing')
})

test('خواندنِ SSE بسته‌های data را درست جدا می‌کند', async () => {
  const chunks = ['data: {"a":1}', '', 'data: {"a":2}', '', 'data: [DONE]', '']
  const stream = new ReadableStream({
    start(controller) {
      for (const c of chunks) controller.enqueue(new TextEncoder().encode(c + '\n'))
      controller.close()
    },
  })
  const out = []
  for await (const payload of readSse(stream)) out.push(payload)
  assert.deepEqual(out, ['{"a":1}', '{"a":2}', '[DONE]'])
})

test('پیکربندیِ ناقصِ مدل (بدون کلید یا مدل) پذیرفته نمی‌شود', () => {
  assert.equal(normalizeProvider({ type: 'openai-compatible', baseUrl: 'x', model: '', apiKey: 'k' }), null)
  assert.equal(normalizeProvider({ type: 'openai-compatible', baseUrl: 'x', model: 'm', apiKey: '' }), null)
  const ok = normalizeProvider({ type: 'openai-compatible', baseUrl: '', model: 'm', apiKey: 'k' })
  assert.equal(ok.baseUrl, 'https://api.openai.com/v1')
})
