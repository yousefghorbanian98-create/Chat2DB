import test from 'node:test'
import assert from 'node:assert/strict'
import { mkdtemp, writeFile, mkdir, readFile, rm, stat } from 'node:fs/promises'
import { join, dirname } from 'node:path'
import { tmpdir } from 'node:os'
import {
  buildManifest,
  diffManifests,
  createTarGz,
  untarGz,
  applyPack,
  readManifest,
  writeManifest,
  hashBuffer,
  totalBytes,
  pickPack,
} from '../dist/test-api.js'

/**
 * تست‌های به‌روزرسانیِ تفاضلی.
 *
 * هدف: ثابت کند فقط فایل‌های تغییرکرده منتقل می‌شوند، درهم‌سازی پیش از نوشتن
 * تأیید می‌شود، و در صورتِ خرابی وضعیت به حالتِ پیشین برمی‌گردد.
 */

async function makeDir(files) {
  const root = await mkdtemp(join(tmpdir(), 'forge-upd-'))
  for (const [rel, content] of Object.entries(files)) {
    const full = join(root, rel)
    await mkdir(dirname(full), { recursive: true })
    await writeFile(full, content)
  }
  return root
}

test('مانیفست همه‌ی فایل‌های پوشه را با درهم‌سازی فهرست می‌کند', async () => {
  const root = await makeDir({
    'index.js': 'console.log(1)',
    'web/assets/app.js': 'bundle',
    'skills/commands/genesis.md': '# genesis',
  })
  const m = await buildManifest(root, { version: '0.1.0', build: 'abc' })

  assert.equal(m.files.length, 3)
  assert.equal(m.build, 'abc')
  assert.ok(m.files.some((f) => f.path === 'web/assets/app.js'))
  // مسیرها با '/' یکسان‌سازی شده‌اند (بین ویندوز و لینوکس)
  assert.ok(!m.files.some((f) => f.path.includes('\\')))
  await rm(root, { recursive: true, force: true })
})

test('تفاضل فقط فایل‌های تغییرکرده را برمی‌گرداند', () => {
  const base = {
    version: '0.1.0',
    build: 'old',
    channel: 'stable',
    generatedAt: '',
    files: [
      { path: 'index.js', size: 3, sha256: 'aaa' },
      { path: 'web/app.js', size: 5, sha256: 'bbb' },
      { path: 'gone.txt', size: 2, sha256: 'ccc' },
    ],
  }
  const next = {
    ...base,
    build: 'new',
    files: [
      { path: 'index.js', size: 3, sha256: 'aaa' }, // بدون تغییر
      { path: 'web/app.js', size: 9, sha256: 'zzz' }, // تغییر کرده
      { path: 'web/new.css', size: 4, sha256: 'ddd' }, // جدید
    ],
  }

  const diff = diffManifests(base, next)
  assert.deepEqual(diff.changed.map((f) => f.path), ['web/app.js'])
  assert.deepEqual(diff.added.map((f) => f.path), ['web/new.css'])
  assert.deepEqual(diff.removed, ['gone.txt'])
  assert.equal(diff.downloadBytes, 9 + 4)
})

test('tar.gz ساخته و بی‌کم‌وکاست باز می‌شود (رفت‌وبرگشت)', () => {
  const files = new Map([
    ['index.js', Buffer.from('server code')],
    ['web/assets/app.js', Buffer.from('x'.repeat(5000))],
    ['skills/commands/genesis.md', Buffer.from('# genesis\n')],
  ])

  const gz = createTarGz(files)
  const back = untarGz(gz)

  assert.equal(back.size, 3)
  for (const [name, buf] of files) {
    assert.ok(back.has(name), `باید باشد: ${name}`)
    assert.equal(back.get(name).toString('utf8'), buf.toString('utf8'))
  }
})

test('اِعمالِ بسته: فایل‌ها جایگزین و مانیفست به‌روزرسانی می‌شود', async () => {
  const root = await makeDir({
    'index.js': 'v1',
    'web/app.js': 'v1',
    'old.txt': 'حذف شود',
  })
  const before = await buildManifest(root, { version: '0.1.0', build: 'b1' })
  await readManifest(root) // null است، مشکلی نیست
  await writeManifest(root, before)

  // بسته‌ی جدید: فقط web/app.js تغییر کرده + یک فایلِ تازه
  const nextFiles = {
    'index.js': 'v1',
    'web/app.js': 'v2',
    'web/new.css': 'body{}',
  }
  const staging = await makeDir(nextFiles)
  const remote = await buildManifest(staging, { version: '0.1.1', build: 'b2' })

  const pack = new Map([
    ['web/app.js', Buffer.from('v2')],
    ['web/new.css', Buffer.from('body{}')],
  ])

  const result = await applyPack(root, untarGz(createTarGz(pack)), remote)

  assert.equal(result.applied, 2)
  assert.equal(result.removed, 1) // old.txt
  assert.equal(result.restartRequired, false) // index.js تغییر نکرده
  assert.equal(await readFile(join(root, 'web/app.js'), 'utf8'), 'v2')
  assert.equal((await readManifest(root)).build, 'b2')

  await rm(root, { recursive: true, force: true })
  await rm(staging, { recursive: true, force: true })
})

test('اگر فایلی با درهم‌سازی مطابق نباشد، هیچ چیز نوشته نمی‌شود و وضعیت برمی‌گردد', async () => {
  const root = await makeDir({ 'index.js': 'v1', 'web/app.js': 'v1' })
  const local = await buildManifest(root, { version: '0.1.0', build: 'b1' })
  await writeManifest(root, local)

  const remote = {
    ...local,
    build: 'b2',
    files: [
      { path: 'index.js', size: 2, sha256: hashBuffer(Buffer.from('v2')) },
      { path: 'web/app.js', size: 2, sha256: hashBuffer(Buffer.from('v1')) },
    ],
  }

  // بسته دستکاری شده: محتوا با درهم‌سازیِ اعلام‌شده نمی‌خواند
  const tampered = new Map([['index.js', Buffer.from('خراب')]])

  await assert.rejects(() => applyPack(root, tampered, remote))

  // هیچ چیز تغییر نکرده است
  assert.equal(await readFile(join(root, 'index.js'), 'utf8'), 'v1')
  assert.equal((await readManifest(root)).build, 'b1')

  await rm(root, { recursive: true, force: true })
})

test('مسیرِ مخرب در بسته رد می‌شود', async () => {
  const root = await makeDir({ 'index.js': 'v1' })
  const local = await buildManifest(root, { version: '0.1.0', build: 'b1' })
  await writeManifest(root, local)
  const evil = new Map([['../../evil.txt', Buffer.from('x')]])

  await assert.rejects(() => applyPack(root, evil, local))
  await rm(root, { recursive: true, force: true })
})

test('حجمِ تفاضلی در برابرِ کل — دلیلِ وجودیِ این سیستم', async () => {
  const root = await makeDir({
    'index.js': 'x'.repeat(400_000), // باندلِ سرور
    'web/app.js': 'y'.repeat(200_000),
    'skills/a.md': 'z'.repeat(1000),
  })
  const m = await buildManifest(root, { version: '0.1.0', build: 'b1' })

  // فقط یک فایلِ کوچک تغییر کرده
  const next = {
    ...m,
    build: 'b2',
    files: m.files.map((f) =>
      f.path === 'skills/a.md' ? { path: f.path, size: 1010, sha256: 'تغییر' } : f,
    ),
  }
  const diff = diffManifests(m, next)

  assert.equal(diff.downloadBytes, 1010)
  assert.ok(totalBytes(m) > 500_000)
  assert.ok(diff.downloadBytes < totalBytes(m) / 100, 'باید کمتر از یک‌صدمِ کل باشد')

  await rm(root, { recursive: true, force: true })
})

test('مانیفست خودش در شمارش نمی‌آید (وگرنه همیشه «به‌روزرسانی هست» نشان می‌دهد)', async () => {
  const root = await makeDir({
    'index.js': 'v1',
    'skills/commands/genesis.md': '# genesis',
  })
  // مانیفست روی دیسک هست — مثلِ هر نصبِ واقعی بعد از نخستین اجرا
  const local = await buildManifest(root, { version: '0.1.0', build: 'local' })
  await writeManifest(root, local)

  const scanned = await buildManifest(root, { version: '0.1.0', build: 'local2' })
  assert.ok(
    !scanned.files.some((f) => f.path === 'update-manifest.json'),
    'مانیفست نباید جزوِ پرونده‌های برنامه شمرده شود',
  )

  // حالا همان را با یک مانیفستِ منتشرشده مقایسه کنیم:
  // چیزی تغییر نکرده پس نباید تفاوتی گزارش شود
  const remote = await buildManifest(root, { version: '0.1.0', build: 'published' })
  const diff = diffManifests(scanned, remote)
  assert.equal(diff.added.length, 0)
  assert.equal(diff.changed.length, 0)
  assert.equal(diff.removed.length, 0)
  assert.equal(diff.downloadBytes, 0)

  await rm(root, { recursive: true, force: true })
})

test('انتخابِ بسته: اگر کاربر دقیقاً روی ساختِ مبناست، بسته‌ی تفاضلی', () => {
  const assets = [
    { name: 'update-pack-c.tar.gz', size: 900, browser_download_url: '' },
    { name: 'update-full-c.tar.gz', size: 400_000, browser_download_url: '' },
  ]
  const remote = { build: 'c', from: 'b', files: [] }
  const local = { build: 'b', files: [] }

  const pick = pickPack(assets, remote, local)
  assert.equal(pick.delta, true)
  assert.equal(pick.asset.name, 'update-pack-c.tar.gz')
})

test('انتخابِ بسته: اگر یک انتشار را پریده باشد، بسته‌ی کامل', () => {
  const assets = [
    { name: 'update-pack-c.tar.gz', size: 900, browser_download_url: '' },
    { name: 'update-full-c.tar.gz', size: 400_000, browser_download_url: '' },
  ]
  const remote = { build: 'c', from: 'b', files: [] }
  const local = { build: 'a', files: [] } // یک انتشار عقب‌تر

  const pick = pickPack(assets, remote, local)
  assert.equal(pick.delta, false)
  assert.equal(pick.asset.name, 'update-full-c.tar.gz')
})

test('انتخابِ بسته: بدونِ بسته‌ی تفاضلی، همان بسته‌ی کامل', () => {
  const assets = [{ name: 'update-full-c.tar.gz', size: 10, browser_download_url: '' }]
  const pick = pickPack(assets, { build: 'c', from: 'b', files: [] }, { build: 'b', files: [] })
  assert.equal(pick.delta, false)
  assert.equal(pick.asset.name, 'update-full-c.tar.gz')
})
