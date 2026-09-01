import test from 'node:test'
import assert from 'node:assert/strict'
import { JcodeAdapter, SoupAdapter, McpClient, config } from '../dist/test-api.js'

test('AC-3: نبود jcode باعث crash نمی‌شود و missing گزارش می‌شود', async () => {
  // یک باینری که قطعاً وجود ندارد
  const adapter = new JcodeAdapter('forge-jcode-does-not-exist')

  const status = await adapter.health()
  assert.equal(status.state, 'missing')
  assert.ok(status.detail.length > 0)

  const result = await adapter.run('hello')
  assert.equal(result.ok, false)
})

test('health() هرگز پرتاب نمی‌کند', async () => {
  const adapters = [new JcodeAdapter(), new SoupAdapter(), new McpClient()]
  for (const a of adapters) {
    const s = await a.health()
    assert.ok(['ready', 'degraded', 'missing'].includes(s.state))
  }
})

test('مسیریاب در نبود پایتون هم کار می‌کند (degraded اما فعال)', async () => {
  const soup = new SoupAdapter([
    { name: 'a', description: 'alpha database indexing', tags: ['db'], instructions: 'x' },
    { name: 'b', description: 'beta react component', tags: ['ui'], instructions: 'y' },
  ])
  const status = await soup.health()
  assert.ok(['ready', 'degraded'].includes(status.state))
  const picked = soup.prepare('optimize database index', 2)
  assert.equal(picked[0].name, 'a')
})

test('رجیستری MCP ده سرور دارد', () => {
  const mcp = new McpClient()
  assert.equal(mcp.list().length, 10)
})

test('پیکربندی پیش‌فرض معتبر است', () => {
  assert.ok(config.port > 0)
  assert.ok(config.skillsDir.length > 0)
})
