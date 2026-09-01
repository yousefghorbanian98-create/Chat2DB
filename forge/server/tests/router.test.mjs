import test from 'node:test'
import assert from 'node:assert/strict'
import { SkillRouter } from '../dist/test-api.js'

/**
 * تست‌های مکانیکِ BM25 روی مجموعهٔ کوچکِ کنترل‌شده.
 * (اینکه «کدام skill برای کاربر درست است» در routing.test.mjs
 *  روی دادهٔ واقعی سنجیده می‌شود، چون نتیجه به کل corpus وابسته است.)
 */
const SKILLS = [
  { name: 'genesis', description: 'Build a new feature end to end from a spec', tags: ['build', 'feature'], instructions: 'x' },
  { name: 'exorcise', description: 'Debug and root-cause a failing test or bug', tags: ['debug', 'bug'], instructions: 'y' },
  { name: 'judgment', description: 'Review code and report blockers and nits', tags: ['review'], instructions: 'z' },
  { name: 'covenant', description: 'Prepare a commit and pull request message', tags: ['git', 'commit'], instructions: 'w' },
  { name: 'prophecy', description: 'Plan the next steps and guide the roadmap', tags: ['plan'], instructions: 'v' },
]

test('اندازهٔ فهرست درست است', () => {
  const router = new SkillRouter()
  router.register(SKILLS)
  assert.equal(router.size, 5)
})

test('درخواست نامربوط نباید skill تزریق کند', () => {
  const router = new SkillRouter()
  router.register(SKILLS)
  assert.equal(router.select('zzzz qqqq wwww', 3).length, 0)
})

test('محدودیتِ تعداد رعایت می‌شود', () => {
  const router = new SkillRouter()
  router.register(SKILLS)
  assert.equal(router.select('build a feature and review it', 1).length, 1)
})

test('نتایج بر اساس امتیاز نزولی مرتب‌اند', () => {
  const router = new SkillRouter()
  router.register(SKILLS)
  const picked = router.select('debug the bug and review the code', 5)
  assert.ok(picked.length > 1)
  for (let i = 1; i < picked.length; i++) {
    assert.ok(picked[i - 1].score >= picked[i].score)
  }
})

test('تگ‌ها امتیاز را تقویت می‌کنند', () => {
  const router = new SkillRouter()
  router.register(SKILLS)
  const withTag = router.select('git', 5)
  assert.equal(withTag[0].skill.name, 'covenant')
})

test('clear کردن فهرست را خالی می‌کند', () => {
  const router = new SkillRouter()
  router.register(SKILLS)
  router.clear()
  assert.equal(router.size, 0)
  assert.equal(router.select('build feature', 3).length, 0)
})
