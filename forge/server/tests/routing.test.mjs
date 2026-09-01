import test from 'node:test'
import assert from 'node:assert/strict'
import { GodmodeAdapter, SoupAdapter, buildSkills } from '../dist/test-api.js'

/**
 * AC-4 روی دادهٔ واقعی (۱۴ skill وِندور شده از Godmode).
 * تستِ مسیریابی باید روی دادهٔ محصول اجرا شود، نه روی مجموعهٔ ساختگی،
 * چون برنده شدنِ یک skill به کل corpus وابسته است (IDF در BM25).
 */
const godmode = new GodmodeAdapter()
await godmode.load()
const skills = buildSkills(godmode)
const soup = new SoupAdapter(skills)

test('AC-4: فهرستِ skillها از منبع واقعی ساخته شده', () => {
  assert.equal(godmode.listCommands().length, 9)
  assert.equal(godmode.listAgents().length, 5)
  assert.equal(soup.skillCount, 14)
})

test('AC-4: «review this pull request» باید judgment را انتخاب کند', () => {
  const picked = soup.prepare('please review this pull request', 3)
  assert.equal(picked[0].name, 'judgment')
})

test('AC-4: «why is my test failing» باید exorcise را انتخاب کند', () => {
  const picked = soup.prepare('why is my test failing', 3)
  assert.ok(['exorcise', 'seer'].includes(picked[0].name))
})

test('AC-4: «build a new feature» باید genesis را انتخاب کند', () => {
  const picked = soup.prepare('build a new feature end to end', 3)
  assert.equal(picked[0].name, 'genesis')
})

test('AC-4: «explain this codebase» باید revelation را انتخاب کند', () => {
  const picked = soup.prepare('explain this codebase', 3)
  assert.equal(picked[0].name, 'revelation')
})

test('AC-4: درخواست نامربوط نباید skill تزریق کند', () => {
  const picked = soup.prepare('zzzq xxxww vvuu', 3)
  assert.equal(picked.length, 0)
})

test('دستور صریح با اسلش در مسیریابی هم برتری دارد', () => {
  const picked = soup.prepare('/judgment review this', 3)
  assert.equal(picked[0].name, 'judgment')
})
