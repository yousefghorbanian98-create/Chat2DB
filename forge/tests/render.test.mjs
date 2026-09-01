import test from 'node:test'
import assert from 'node:assert/strict'
import React from 'react'
import { renderToStaticMarkup } from 'react-dom/server'
import {
  App,
  StatusPills,
  StagePill,
  SessionList,
  Welcome,
  SetupSheet,
} from '../dist-ssr/app.js'

/**
 * رندرِ واقعیِ درختِ کامپوننت‌ها در Node.
 * این جایگزینِ اسکرین‌شات نیست، اما ثابت می‌کند رابط بدون خطا ساخته می‌شود
 * و توکن‌های DESIGN.md واقعاً در خروجی حضور دارند.
 */

test('AC-6: درختِ اصلی بدون خطا رندر می‌شود و سه ستون دارد', () => {
  const html = renderToStaticMarkup(React.createElement(App))
  assert.ok(html.includes('Forge'), 'نام برنامه باید در خروجی باشد')
  assert.ok(html.includes('نشست‌ها'), 'ستونِ نشست‌ها باید باشد')
  assert.ok(html.includes('مهارت‌ها'), 'پنلِ کناری باید باشد')
  assert.ok(html.includes('کنسولِ عامل‌های کدنویسی'))
})

test('AC-7: توکن‌های DESIGN.md در خروجی استفاده شده‌اند، نه رنگِ ثابت', () => {
  const html = renderToStaticMarkup(React.createElement(App))
  // کلاس‌های توکن
  assert.ok(html.includes('bg-canvas') || html.includes('bg-canvas-soft'))
  assert.ok(html.includes('border-hairline'))
  // هیچ رنگِ هگز در خروجیِ کامپوننت‌ها نباید باشد
  const hexInMarkup = html.match(/#[0-9a-fA-F]{6}\b/g)
  assert.equal(hexInMarkup, null, `رنگ ثابت در خروجی: ${hexInMarkup}`)
})

test('وضعیتِ Adapterها با توکنِ درست نمایش داده می‌شود', () => {
  const html = renderToStaticMarkup(
    React.createElement(StatusPills, {
      health: {
        ok: true,
        service: 'forge',
        version: '0.1.0',
        port: 8787,
        skillsDir: '/x',
        adapters: [
          { name: 'jcode', state: 'missing', detail: 'x' },
          { name: 'godmode', state: 'ready', detail: 'y' },
          { name: 'soup', state: 'degraded', detail: 'z' },
        ],
      },
    }),
  )
  assert.ok(html.includes('--color-muted'), 'غایب ← توکنِ muted')
  assert.ok(html.includes('--color-success'), 'آماده ← توکنِ success')
  assert.ok(html.includes('--color-done'), 'ناقص ← توکنِ done')
})

test('قرصِ مرحله از پاستیلِ تایم‌لاین استفاده می‌کند', () => {
  const html = renderToStaticMarkup(React.createElement(StagePill, { stage: 'Grep', text: 'x' }))
  assert.ok(html.includes('--color-grep'))
  assert.ok(html.includes('rounded-full'), 'قرص باید pill باشد')
})

test('فهرستِ نشست‌ها در حالت خالی پیام مناسب دارد', () => {
  const html = renderToStaticMarkup(
    React.createElement(SessionList, { sessions: [], activeId: null, onSelect: () => {}, onNew: () => {} }),
  )
  assert.ok(html.includes('هنوز نشستی نیست'))
})

test('صفحه‌ی آغاز پیشنهاد می‌دهد و ابزارهای ناقص را پنهان نمی‌کند', () => {
  const html = renderToStaticMarkup(
    React.createElement(Welcome, {
      health: {
        ok: true,
        service: 'forge',
        version: '0.1.0',
        port: 8787,
        skillsDir: '/x',
        adapters: [{ name: 'jcode', state: 'missing', detail: 'x' }],
      },
      onPick: () => {},
      onOpenSetup: () => {},
    }),
  )
  // چهار شروع‌کننده باید باشند
  assert.ok(html.includes('این کدبیس را توضیح بده'))
  assert.ok(html.includes('یک قابلیتِ جدید بساز'))
  // ابزارِ ناقص باید دیده شود، نه پنهان
  assert.ok(html.includes('jcode'), 'ابزارِ ناقص باید در صفحه‌ی آغاز ذکر شود')
})

test('راهنمای وصل‌کردن برای هر ابزار نیازمندی و نشانی دارد', () => {
  const html = renderToStaticMarkup(
    React.createElement(SetupSheet, {
      open: true,
      onClose: () => {},
      health: {
        ok: true,
        service: 'forge',
        version: '0.1.0',
        port: 8787,
        skillsDir: '/x',
        adapters: [
          { name: 'jcode', state: 'missing', detail: 'باینری یافت نشد' },
          { name: 'soup', state: 'degraded', detail: 'مسیریابِ داخلی' },
        ],
      },
    }),
  )
  assert.ok(html.includes('github.com/1jehuang/jcode'), 'نشانیِ منبع باید باشد')
  assert.ok(html.includes('github.com/southwind-ai/soup'))
  assert.ok(html.includes('غایب') && html.includes('ناقص'))
})

test('مقیاسِ تایپوگرافیِ DESIGN.md به‌کار رفته، نه اندازه‌ی دلخواه', () => {
  const html = renderToStaticMarkup(React.createElement(App))
  const arbitrary = html.match(/text-\[\d+px\]/g)
  assert.equal(arbitrary, null, `اندازه‌ی دلخواه در خروجی: ${arbitrary}`)
})
