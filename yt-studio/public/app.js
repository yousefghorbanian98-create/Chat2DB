'use strict';

const $ = (s) => document.querySelector(s);
const el = (tag, cls, html) => {
  const n = document.createElement(tag);
  if (cls) n.className = cls;
  if (html != null) n.innerHTML = html;
  return n;
};

let DATA = null;
let sortKey = 'views';
let sortDir = -1;

// ---------- formatting ----------
const FA = '۰۱۲۳۴۵۶۷۸۹';
const fa = (s) => String(s).replace(/\d/g, (d) => FA[+d]);

function num(n) {
  n = Number(n) || 0;
  if (n >= 1e9) return fa((n / 1e9).toFixed(1)) + ' میلیارد';
  if (n >= 1e6) return fa((n / 1e6).toFixed(n >= 1e7 ? 0 : 1)) + ' میلیون';
  if (n >= 1e3) return fa((n / 1e3).toFixed(n >= 1e4 ? 0 : 1)) + ' هزار';
  return fa(Math.round(n));
}
function dur(s) {
  s = Math.round(s || 0);
  const h = Math.floor(s / 3600), m = Math.floor((s % 3600) / 60), sec = s % 60;
  return fa(h ? `${h}:${String(m).padStart(2, '0')}:${String(sec).padStart(2, '0')}`
              : `${m}:${String(sec).padStart(2, '0')}`);
}
function when(iso) {
  const d = Math.floor((Date.now() - new Date(iso)) / 86400000);
  if (d < 1) return 'امروز';
  if (d < 30) return fa(d) + ' روز پیش';
  if (d < 365) return fa(Math.floor(d / 30)) + ' ماه پیش';
  return fa((d / 365).toFixed(1)) + ' سال پیش';
}
const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) =>
  ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

const thumbFor = (v) =>
  v.thumbnail
    ? `<img src="${esc(v.thumbnail)}" alt="" loading="lazy" onerror="this.outerHTML='<div class=thumb-ph>▶</div>'">`
    : '<div class="thumb-ph">▶</div>';

// ---------- boot ----------
fetch('/api/status')
  .then((r) => r.json())
  .then((s) => {
    const b = $('#keyBadge');
    if (s.hasKey) {
      b.textContent = '✅ کلید API متصل است';
      b.className = 'badge badge-ok';
    } else {
      b.textContent = '⚠️ بدون کلید API — حالت نمونه';
      b.className = 'badge badge-warn';
    }
  })
  .catch(() => {});

$('#form').addEventListener('submit', (e) => {
  e.preventDefault();
  run($('#channel').value.trim(), false);
});
$('#demoBtn').addEventListener('click', () => run('', true));
document.querySelectorAll('.chip[data-ch]').forEach((c) =>
  c.addEventListener('click', () => {
    $('#channel').value = c.dataset.ch;
    run(c.dataset.ch, false);
  }),
);

async function run(channel, demo) {
  if (!demo && !channel) {
    showError('لطفاً نام یا لینک کانال را وارد کنید.');
    return;
  }
  $('#error').classList.add('hidden');
  $('#notice').classList.add('hidden');
  $('#results').classList.add('hidden');
  $('#loading').classList.remove('hidden');
  $('#go').disabled = true;

  const qs = new URLSearchParams();
  if (demo) qs.set('demo', '1');
  else {
    qs.set('channel', channel);
    qs.set('limit', $('#limit').value);
  }

  try {
    const res = await fetch('/api/analyze?' + qs);
    const body = await res.json();
    if (!res.ok) throw new Error(body.error || 'خطا در دریافت داده');
    DATA = body;
    render(body);
  } catch (err) {
    showError(err.message);
  } finally {
    $('#loading').classList.add('hidden');
    $('#go').disabled = false;
  }
}

function showError(msg) {
  const e = $('#error');
  e.textContent = '❌ ' + msg;
  e.classList.remove('hidden');
}

// ---------- render ----------
function render(d) {
  if (d.notice) {
    $('#notice').textContent = 'ℹ️ ' + d.notice;
    $('#notice').classList.remove('hidden');
  }

  renderChannel(d.channel, d.summary);
  renderKpis(d.summary, d.channel);
  renderSuggestions(d.suggestions);
  renderShortIdeas(d.shortIdeas);
  renderKeywords(d.keywords);
  renderVideos('#outliers', d.outliers, true);
  renderVideos('#rising', d.rising, false);
  renderVideos('#under', d.underperformers, false);
  renderHooks(d.hooks);
  renderDays(d.dayStats);
  renderHours(d.hourBuckets);
  renderDurations(d.durBuckets);
  renderTable();

  $('#results').classList.remove('hidden');
  $('#results').scrollIntoView({ behavior: 'smooth', block: 'start' });
}

function renderChannel(c, s) {
  const av = c.thumbnail
    ? `<img src="${esc(c.thumbnail)}" alt="" onerror="this.outerHTML='<div class=ch-avatar-ph>📺</div>'">`
    : '<div class="ch-avatar-ph">📺</div>';
  const subs = c.hiddenSubscribers ? 'مخفی' : num(c.subscribers) + ' مشترک';
  $('#channelCard').innerHTML = `
    ${av}
    <div class="ch-meta">
      <h2>${esc(c.title)}</h2>
      <div class="ch-sub">${esc(c.handle || '')} · ${subs} · ${num(c.videoCount)} ویدیو · ${num(c.totalViews)} بازدید کل</div>
      ${c.description ? `<div class="ch-desc">${esc(c.description)}</div>` : ''}
    </div>
    ${c.url && c.url !== 'https://www.youtube.com/' ? `<a class="chip" href="${esc(c.url)}" target="_blank" rel="noopener">باز کردن در یوتیوب ↗</a>` : ''}`;
}

function renderKpis(s, c) {
  const trend = s.trend
    ? (s.trend >= 1
        ? `<span class="up">▲ ${fa(((s.trend - 1) * 100).toFixed(0))}٪ رشد</span>`
        : `<span class="down">▼ ${fa(((1 - s.trend) * 100).toFixed(0))}٪ افت</span>`)
    : '—';

  const items = [
    ['ویدیوهای تحلیل‌شده', fa(s.analyzed), `${fa(s.longCount)} بلند · ${fa(s.shortCount)} کوتاه`],
    ['میانه‌ی بازدید', num(s.medViews), 'به ازای هر ویدیو'],
    ['بازدید روزانه (میانه)', num(s.medVpd), 'سرعت رشد هر ویدیو'],
    ['نرخ تعامل', fa((s.medEngagement * 100).toFixed(1)) + '٪', 'لایک + کامنت ÷ بازدید'],
    ['فاصله‌ی انتشار', s.cadenceDays ? fa(s.cadenceDays.toFixed(1)) + ' روز' : '—', 'میانه‌ی فاصله بین ویدیوها'],
    ['روند ۹۰ روز اخیر', trend, 'نسبت به ۹۰ روز قبل‌تر'],
  ];

  $('#kpis').innerHTML = items
    .map(([l, v, n]) => `<div class="kpi"><div class="k-label">${l}</div><div class="k-val">${v}</div><div class="k-note">${n}</div></div>`)
    .join('');
}

function renderSuggestions(list) {
  const box = $('#suggestions');
  box.innerHTML = '';
  (list || []).forEach((s) => {
    const n = el('div', 'sug');
    n.innerHTML = `<button class="copy">کپی</button>
      <div class="s-text">${esc(s.text)}</div>
      <div class="s-why">${esc(s.why)}</div>`;
    n.querySelector('.copy').addEventListener('click', (e) => {
      navigator.clipboard?.writeText(s.text);
      e.target.textContent = '✓ کپی شد';
      e.target.classList.add('done');
      setTimeout(() => { e.target.textContent = 'کپی'; e.target.classList.remove('done'); }, 1600);
    });
    box.appendChild(n);
  });
  if (!box.children.length) box.innerHTML = '<p class="sub">داده‌ی کافی برای پیشنهاد نیست.</p>';
}

function renderShortIdeas(list) {
  $('#shortIdeas').innerHTML = (list || []).length
    ? list.map((i) => `
      <div class="idea">
        <a class="i-src" href="${esc(i.sourceUrl)}" target="_blank" rel="noopener">${esc(i.sourceTitle)}</a>
        <div class="i-angle">💡 ${esc(i.angle)}</div>
        <div class="i-stat">${num(i.views)} بازدید · ×${fa(i.multiplier.toFixed(1))} بهتر از میانه</div>
      </div>`).join('')
    : '<p class="sub">ویدیوی بلند پربازده‌ای برای پیشنهاد پیدا نشد.</p>';
}

function renderKeywords(list) {
  $('#keywords').innerHTML = (list || []).length
    ? list.map((k) => {
        const cls = k.lift >= 1.4 ? 'kw-hot' : k.lift >= 1 ? 'kw-mid' : 'kw-low';
        return `<span class="kw ${cls}" title="${esc(k.best?.title || '')}">
          <b>${esc(k.word)}</b>
          <span class="kw-x">×${fa(k.lift.toFixed(1))}</span>
          <small>${fa(k.count)} بار</small></span>`;
      }).join('')
    : '<p class="sub">کلیدواژه‌ی تکرارشونده‌ای پیدا نشد.</p>';
}

function renderVideos(sel, list, showRank) {
  const box = $(sel);
  if (!list || !list.length) { box.innerHTML = '<p class="sub">موردی نیست.</p>'; return; }
  box.innerHTML = list.map((v, i) => {
    const mc = v.multiplier >= 1.5 ? 'hot' : v.multiplier < 0.6 ? 'cold' : '';
    return `<div class="vid">
      ${showRank ? `<div class="rank">${fa(i + 1)}</div>` : ''}
      ${thumbFor(v)}
      <div class="v-body">
        <a class="v-title" href="${esc(v.url)}" target="_blank" rel="noopener">${esc(v.title)}</a>
        <div class="v-stats">
          <span>👁 ${num(v.views)}</span>
          <span class="${mc}">×${fa((v.multiplier || 0).toFixed(1))}</span>
          <span>${num(v.vpd)}/روز</span>
          <span>${dur(v.durationSec)}</span>
          ${v.isShort ? '<span class="tagshort">Short</span>' : ''}
          <span>${when(v.publishedAt)}</span>
        </div>
      </div>
    </div>`;
  }).join('');
}

function bars(sel, rows) {
  const max = Math.max(...rows.map((r) => r.value), 1);
  $(sel).innerHTML = rows.map((r) => {
    const pct = Math.max(2, (r.value / max) * 100);
    const cls = r.value >= max * 0.7 ? 'good' : r.value >= max * 0.4 ? 'mid' : 'low';
    return `<div class="bar-row">
      <div class="bar-label" title="${esc(r.label)}">${esc(r.label)}</div>
      <div class="bar-track"><div class="bar-fill ${cls}" style="width:${pct}%"></div></div>
      <div class="bar-val">${r.display}${r.note ? `<small>${r.note}</small>` : ''}</div>
    </div>`;
  }).join('');
}

function renderHooks(hooks) {
  const rows = (hooks || []).filter((h) => h.lift != null).map((h) => ({
    label: h.label,
    value: h.lift,
    display: '×' + fa(h.lift.toFixed(2)),
    note: fa(h.count) + ' ویدیو',
  }));
  if (!rows.length) { $('#hooks').innerHTML = '<p class="sub">داده کافی نیست.</p>'; return; }
  bars('#hooks', rows);
}

function renderDays(days) {
  bars('#days', (days || []).map((d) => ({
    label: d.label,
    value: d.medVpd,
    display: num(d.medVpd),
    note: fa(d.count) + ' ویدیو',
  })));
}
function renderHours(hb) {
  bars('#hours', (hb || []).map((b) => ({
    label: b.label,
    value: b.medVpd,
    display: num(b.medVpd),
    note: fa(b.count) + ' ویدیو',
  })));
}
function renderDurations(db) {
  bars('#durations', (db || []).map((b) => ({
    label: b.label,
    value: b.medVpd,
    display: num(b.medVpd),
    note: fa(b.count) + ' ویدیو',
  })));
}

// ---------- table ----------
function allVideos() {
  const seen = new Set(), out = [];
  for (const g of ['topByViews', 'outliers', 'rising', 'underperformers']) {
    for (const v of DATA[g] || []) if (!seen.has(v.id)) { seen.add(v.id); out.push(v); }
  }
  return out;
}

function renderTable() {
  const q = ($('#filter').value || '').trim().toLowerCase();
  let rows = allVideos();
  if (q) rows = rows.filter((v) => v.title.toLowerCase().includes(q));
  rows.sort((a, b) => {
    const x = a[sortKey], y = b[sortKey];
    if (typeof x === 'string') return sortDir * x.localeCompare(y, 'fa');
    return sortDir * ((y ?? 0) - (x ?? 0)) * -1 * -1;
  });
  if (sortKey === 'publishedAt') {
    rows.sort((a, b) => sortDir * (new Date(b.publishedAt) - new Date(a.publishedAt)) * -1 * -1);
  }

  $('#table tbody').innerHTML = rows.map((v) => `
    <tr>
      <td><a href="${esc(v.url)}" target="_blank" rel="noopener">${esc(v.title)}</a>${v.isShort ? ' <span class="tagshort">S</span>' : ''}</td>
      <td class="num">${num(v.views)}</td>
      <td class="num">${num(v.vpd)}</td>
      <td class="num">×${fa((v.multiplier || 0).toFixed(1))}</td>
      <td class="num">${fa(((v.engagement || 0) * 100).toFixed(1))}٪</td>
      <td class="num">${dur(v.durationSec)}</td>
      <td class="num">${when(v.publishedAt)}</td>
    </tr>`).join('') || '<tr><td colspan="7" style="text-align:center;color:var(--tx3);padding:24px">موردی یافت نشد</td></tr>';
}

document.querySelectorAll('th[data-sort]').forEach((th) =>
  th.addEventListener('click', () => {
    const k = th.dataset.sort;
    if (sortKey === k) sortDir *= -1; else { sortKey = k; sortDir = -1; }
    renderTable();
  }),
);
$('#filter').addEventListener('input', renderTable);

$('#csv').addEventListener('click', () => {
  const rows = allVideos();
  const head = ['title', 'views', 'views_per_day', 'multiplier', 'engagement', 'duration_sec', 'published_at', 'url'];
  const csv = [head.join(',')].concat(
    rows.map((v) => [
      `"${v.title.replace(/"/g, '""')}"`,
      v.views, Math.round(v.vpd), (v.multiplier || 0).toFixed(2),
      (v.engagement || 0).toFixed(4), v.durationSec, v.publishedAt, v.url,
    ].join(',')),
  ).join('\n');
  const url = URL.createObjectURL(new Blob(['\ufeff' + csv], { type: 'text/csv;charset=utf-8' }));
  const a = document.createElement('a');
  a.href = url;
  a.download = `${(DATA.channel.handle || DATA.channel.title || 'channel').replace(/[^\w@-]/g, '_')}.csv`;
  a.click();
  URL.revokeObjectURL(url);
});

// ---------- tabs ----------
document.querySelectorAll('.tab').forEach((t) =>
  t.addEventListener('click', () => {
    document.querySelectorAll('.tab').forEach((x) => x.classList.remove('active'));
    document.querySelectorAll('.panel').forEach((x) => x.classList.remove('active'));
    t.classList.add('active');
    $('#panel-' + t.dataset.tab).classList.add('active');
  }),
);
