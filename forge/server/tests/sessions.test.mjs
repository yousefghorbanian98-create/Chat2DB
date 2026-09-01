import test from 'node:test'
import assert from 'node:assert/strict'
import { Store } from '../dist/test-api.js'

/**
 * حذفِ نشست — بعداً اضافه شد تا برنامه «کامل» باشد:
 * کاربر بتواند نشستی را که ساخته پاک هم بکند.
 */
test('نشست ساخته، خوانده و حذف می‌شود', async () => {
  const store = new Store()

  const created = await store.createSession('نشستِ آزمایشی')
  assert.equal(created.title, 'نشستِ آزمایشی')
  assert.equal(created.messages.length, 0)

  await store.appendMessage(created.id, { role: 'user', text: 'سلام' })
  const loaded = await store.getSession(created.id)
  assert.equal(loaded.messages.length, 1)

  assert.equal(await store.deleteSession(created.id), true)
  assert.equal(await store.getSession(created.id), null)
})

test('حذفِ نشستِ ناموجود false برمی‌گرداند و چیزی را خراب نمی‌کند', async () => {
  const store = new Store()
  const before = await store.listSessions()

  assert.equal(await store.deleteSession('وجود-ندارد'), false)
  assert.equal((await store.listSessions()).length, before.length)
})
