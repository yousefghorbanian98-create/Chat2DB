'use strict';

/**
 * Turns a raw channel + video list into actionable content research:
 * outliers, title patterns, best publish slots, length sweet-spot, Shorts ideas.
 */

const STOPWORDS = new Set([
  // Persian
  'و','در','به','از','که','این','را','با','های','برای','آن','یک','هم','تا','است','می','بر','شد','شده','کرد','کردن','خود','بود','ما','شما','او','ولی','اما','اگر','یا','هر','چه','چی','چرا','چطور','چگونه','همه','بی','بدون','روی','دیگر','باید','نیست','هست','کنید','کنیم','کردم','دارد','دارم','دارید','بیشتر','خیلی','قسمت','ویدیو','ویدئو','کانال','part',
  // English
  'the','a','an','and','or','but','if','of','to','in','on','for','with','at','by','from','is','are','was','were','be','been','this','that','these','those','it','its','as','how','why','what','when','which','who','you','your','my','me','we','our','i','do','does','did','not','no','yes','can','will','just','so','than','then','out','up','down','new','best','video','ep','episode','full','official',
]);

const clean = (s) =>
  String(s || '')
    .toLowerCase()
    .replace(/[\u200c\u200f\u200e]/g, ' ')
    .replace(/[^\p{L}\p{N}\s]/gu, ' ')
    .replace(/\s+/g, ' ')
    .trim();

const tokens = (s) =>
  clean(s)
    .split(' ')
    .filter((w) => w.length > 2 && !STOPWORDS.has(w) && !/^\d+$/.test(w));

const median = (arr) => {
  if (!arr.length) return 0;
  const s = [...arr].sort((a, b) => a - b);
  const m = s.length >> 1;
  return s.length % 2 ? s[m] : (s[m - 1] + s[m]) / 2;
};

const DAYS = ['یکشنبه', 'دوشنبه', 'سه‌شنبه', 'چهارشنبه', 'پنج‌شنبه', 'جمعه', 'شنبه'];
// JS getDay(): 0=Sunday ... 6=Saturday
const DAY_LABEL = ['یکشنبه', 'دوشنبه', 'سه‌شنبه', 'چهارشنبه', 'پنج‌شنبه', 'جمعه', 'شنبه'];

function daysSince(iso) {
  return Math.max(1, (Date.now() - new Date(iso).getTime()) / 86400000);
}

/** Title "hooks" — structural features that correlate with performance. */
const HOOKS = [
  { key: 'number', label: 'عدد در عنوان', test: (t) => /\d|[۰-۹]/.test(t) },
  { key: 'question', label: 'عنوان سوالی', test: (t) => /[?؟]/.test(t) || /^(چطور|چرا|چگونه|آیا|چه|how|why|what|should|is|can)\b/i.test(t.trim()) },
  { key: 'howto', label: 'آموزشی (چطور/راهنما)', test: (t) => /(چطور|چگونه|آموزش|راهنما|قدم به قدم|از صفر|how to|tutorial|guide|step)/i.test(t) },
  { key: 'curiosity', label: 'کنجکاوی/راز', test: (t) => /(راز|هیچ‌?کس|هیچ کس|نمی‌?گوید|شوکه|باورنکردنی|واقعاً|حقیقت|secret|nobody|truth|shocking|actually)/i.test(t) },
  { key: 'negative', label: 'هشدار/اشتباه', test: (t) => /(اشتباه|نکنید|متوقف|خطر|شکست|بدترین|هشدار|stop|mistake|don.?t|worst|fail|avoid)/i.test(t) },
  { key: 'listicle', label: 'لیستی (۵ تا، ۷ تا…)', test: (t) => /^\s*[\d۰-۹]+\s|(\b[\d۰-۹]+)\s*(تا|روش|نکته|ابزار|اشتباه|دلیل|things|ways|tips|tools|reasons)/i.test(t) },
  { key: 'versus', label: 'مقایسه‌ای (در برابر)', test: (t) => /(در مقابل|در برابر|مقایسه|بهتر است|کدام|\bvs\b|versus|compared)/i.test(t) },
  { key: 'personal', label: 'تجربه شخصی', test: (t) => /(امتحان کردم|تجربه|یک ماه|۳۰ روز|30 روز|من |تستش کردم|i tried|my |experience|days)/i.test(t) },
  { key: 'year', label: 'سال‌دار (۲۰۲۶ …)', test: (t) => /(20[2-3]\d|۲۰[۲-۳][۰-۹]|۱۴۰[۰-۹])/.test(t) },
  { key: 'bracket', label: 'پرانتز/براکت', test: (t) => /[([\]{}）】]/.test(t) },
];

function analyze(data, opts = {}) {
  const nowIso = new Date().toISOString();
  const all = (data.videos || []).slice();
  const channel = data.channel || {};

  // ---- enrich -------------------------------------------------------------
  for (const v of all) {
    v.ageDays = daysSince(v.publishedAt);
    v.vpd = v.views / v.ageDays; // views per day
    v.engagement = v.views > 0 ? (v.likes + v.comments) / v.views : 0;
    const d = new Date(v.publishedAt);
    v.dow = d.getDay();
    v.hour = d.getHours();
  }

  const longs = all.filter((v) => !v.isShort);
  const shorts = all.filter((v) => v.isShort);

  // ---- outliers: performance vs the channel's own median ------------------
  // Compare within format so Shorts don't drown out long videos.
  const medLong = median(longs.map((v) => v.vpd)) || 1;
  const medShort = median(shorts.map((v) => v.vpd)) || 1;
  for (const v of all) {
    const baseline = v.isShort ? medShort : medLong;
    v.multiplier = baseline > 0 ? v.vpd / baseline : 0;
  }

  const topByViews = [...all].sort((a, b) => b.views - a.views).slice(0, 12);
  const outliers = [...all]
    .filter((v) => v.ageDays >= 3)
    .sort((a, b) => b.multiplier - a.multiplier)
    .slice(0, 12);
  const rising = [...all]
    .filter((v) => v.ageDays <= 45 && v.ageDays >= 1)
    .sort((a, b) => b.vpd - a.vpd)
    .slice(0, 8);
  const underperformers = [...all]
    .filter((v) => v.ageDays >= 30)
    .sort((a, b) => a.multiplier - b.multiplier)
    .slice(0, 6);

  // ---- title hooks --------------------------------------------------------
  const overallMedVpd = median(all.map((v) => v.vpd)) || 1;
  const hooks = HOOKS.map((h) => {
    const hit = all.filter((v) => h.test(v.title));
    const miss = all.filter((v) => !h.test(v.title));
    if (hit.length < 3 || miss.length < 3) {
      return { key: h.key, label: h.label, count: hit.length, lift: null, medVpd: median(hit.map((v) => v.vpd)) };
    }
    const a = median(hit.map((v) => v.vpd));
    const b = median(miss.map((v) => v.vpd));
    return {
      key: h.key,
      label: h.label,
      count: hit.length,
      medVpd: a,
      lift: b > 0 ? a / b : null,
    };
  })
    .filter((h) => h.count > 0)
    .sort((a, b) => (b.lift ?? -1) - (a.lift ?? -1));

  // ---- keywords -----------------------------------------------------------
  const kw = new Map();
  for (const v of all) {
    for (const w of new Set(tokens(v.title))) {
      if (!kw.has(w)) kw.set(w, { word: w, count: 0, vpds: [], views: 0, best: null });
      const e = kw.get(w);
      e.count++;
      e.vpds.push(v.vpd);
      e.views += v.views;
      if (!e.best || v.views > e.best.views) e.best = { title: v.title, views: v.views, url: v.url };
    }
  }
  const keywords = [...kw.values()]
    .filter((e) => e.count >= 2)
    .map((e) => ({
      word: e.word,
      count: e.count,
      medVpd: median(e.vpds),
      lift: overallMedVpd > 0 ? median(e.vpds) / overallMedVpd : 0,
      views: e.views,
      best: e.best,
    }))
    .sort((a, b) => b.lift * Math.log2(1 + b.count) - a.lift * Math.log2(1 + a.count))
    .slice(0, 24);

  // ---- publish timing -----------------------------------------------------
  const dayStats = DAY_LABEL.map((label, i) => {
    const vs = all.filter((v) => v.dow === i);
    return { day: i, label, count: vs.length, medVpd: median(vs.map((v) => v.vpd)) };
  });
  const hourBuckets = [
    { label: '۰۰–۰۶ بامداد', from: 0, to: 5 },
    { label: '۰۶–۱۰ صبح', from: 6, to: 9 },
    { label: '۱۰–۱۴ ظهر', from: 10, to: 13 },
    { label: '۱۴–۱۸ عصر', from: 14, to: 17 },
    { label: '۱۸–۲۱ شب', from: 18, to: 20 },
    { label: '۲۱–۲۴ آخر شب', from: 21, to: 23 },
  ].map((b) => {
    const vs = all.filter((v) => v.hour >= b.from && v.hour <= b.to);
    return { ...b, count: vs.length, medVpd: median(vs.map((v) => v.vpd)) };
  });

  // ---- duration sweet spot (long-form only) -------------------------------
  const durBuckets = [
    { label: 'زیر ۱ دقیقه (Shorts)', from: 0, to: 60 },
    { label: '۱–۴ دقیقه', from: 61, to: 240 },
    { label: '۴–۸ دقیقه', from: 241, to: 480 },
    { label: '۸–۱۵ دقیقه', from: 481, to: 900 },
    { label: '۱۵–۲۵ دقیقه', from: 901, to: 1500 },
    { label: 'بالای ۲۵ دقیقه', from: 1501, to: 1e9 },
  ].map((b) => {
    const vs = all.filter((v) => v.durationSec >= b.from && v.durationSec <= b.to);
    return {
      ...b,
      count: vs.length,
      medVpd: median(vs.map((v) => v.vpd)),
      medViews: median(vs.map((v) => v.views)),
    };
  }).filter((b) => b.count > 0);

  // ---- upload cadence -----------------------------------------------------
  const sorted = [...all].sort((a, b) => new Date(a.publishedAt) - new Date(b.publishedAt));
  const gaps = [];
  for (let i = 1; i < sorted.length; i++) {
    gaps.push(
      (new Date(sorted[i].publishedAt) - new Date(sorted[i - 1].publishedAt)) / 86400000,
    );
  }
  const cadenceDays = median(gaps);

  // ---- last 90 days snapshot ---------------------------------------------
  const recent = all.filter((v) => v.ageDays <= 90);
  const prior = all.filter((v) => v.ageDays > 90 && v.ageDays <= 180);
  const trend =
    prior.length && recent.length
      ? median(recent.map((v) => v.vpd)) / (median(prior.map((v) => v.vpd)) || 1)
      : null;

  // ---- Shorts ideas -------------------------------------------------------
  const shortIdeas = outliers
    .filter((v) => !v.isShort)
    .slice(0, 8)
    .map((v) => ({
      sourceTitle: v.title,
      sourceUrl: v.url,
      views: v.views,
      multiplier: v.multiplier,
      angle: shortAngle(v.title),
    }));

  // ---- title suggestions --------------------------------------------------
  const topWords = keywords.slice(0, 6).map((k) => k.word);
  const winningHooks = hooks.filter((h) => h.lift && h.lift > 1.15).slice(0, 4);
  const suggestions = buildTitleSuggestions(topWords, winningHooks);

  return {
    generatedAt: nowIso,
    demo: !!data.demo,
    channel,
    summary: {
      analyzed: all.length,
      longCount: longs.length,
      shortCount: shorts.length,
      medViews: median(all.map((v) => v.views)),
      medVpd: overallMedVpd,
      medEngagement: median(all.map((v) => v.engagement)),
      cadenceDays,
      trend,
      oldest: sorted[0]?.publishedAt || null,
      newest: sorted[sorted.length - 1]?.publishedAt || null,
    },
    topByViews,
    outliers,
    rising,
    underperformers,
    hooks,
    keywords,
    dayStats,
    hourBuckets,
    durBuckets,
    shortIdeas,
    suggestions,
  };
}

function shortAngle(title) {
  if (/(اشتباه|نکنید|mistake|stop)/i.test(title)) return 'تک‌اشتباه اصلی را در ۳۰ ثانیه بگو، با هوک «این کار را نکن».';
  if (/(چطور|چگونه|آموزش|how|tutorial)/i.test(title)) return 'فقط سریع‌ترین میان‌بر آموزش را نشان بده؛ جزئیات را به ویدیوی بلند ارجاع بده.';
  if (/(راز|secret|هیچ)/i.test(title)) return 'با جمله‌ی «هیچ‌کس این را نمی‌گوید…» شروع کن و یک نکته‌ی متضاد انتظار بده.';
  if (/(مقایسه|vs|در مقابل|کدام)/i.test(title)) return 'مقایسه‌ی دو گزینه در قالب اسپلیت‌اسکرین با یک برنده در ثانیه‌ی آخر.';
  if (/([\d۰-۹]+\s*(تا|روش|نکته|ابزار)|tips|ways|tools)/i.test(title)) return 'قوی‌ترین آیتم لیست را به‌تنهایی کلیپ کن — نه کل لیست.';
  return 'جذاب‌ترین ۳۰ ثانیه را جدا کن و هوک را به ۳ ثانیه‌ی اول منتقل کن.';
}

function buildTitleSuggestions(words, hooks) {
  const w = (i) => words[i % Math.max(1, words.length)] || 'موضوع کانال';
  const out = [];
  const add = (text, why) => out.push({ text, why });

  const has = (k) => hooks.some((h) => h.key === k);

  if (has('number') || has('listicle')) add(`۷ اشتباه در ${w(0)} که بازدید شما را می‌خورد`, 'عنوان‌های عددی/لیستی در این کانال بهتر جواب داده‌اند.');
  if (has('curiosity')) add(`چیزی که هیچ‌کس درباره ${w(1)} به شما نمی‌گوید`, 'قلاب کنجکاوی در این کانال بازدهی بالاتری داشته.');
  if (has('question')) add(`آیا ${w(2)} هنوز ارزشش را دارد؟`, 'عنوان‌های سوالی در این کانال عملکرد بهتری دارند.');
  if (has('negative')) add(`${w(0)} را همین امروز متوقف کنید — این را جایگزین کنید`, 'قلاب هشدار/اشتباه در این کانال مؤثر بوده.');
  if (has('personal')) add(`۳۰ روز ${w(3)} را امتحان کردم — نتیجه غیرمنتظره بود`, 'روایت تجربه‌ی شخصی در این کانال جواب داده.');
  if (has('howto')) add(`${w(1)} از صفر تا صد در ۱۰ دقیقه`, 'محتوای آموزشی در این کانال پایدارترین بازدید را دارد.');
  if (has('versus')) add(`${w(2)} در برابر ${w(4)} — کدام برنده است؟`, 'عنوان‌های مقایسه‌ای اینجا بالاتر از میانه‌اند.');

  // generic fillers so the list is never empty
  add(`راهنمای کامل ${w(0)} برای مبتدی‌ها (۲۰۲۶)`, 'ترکیب کلیدواژه‌ی پرتکرار کانال با سال جاری.');
  add(`بهترین روش ${w(1)} که بعد از ۶ ماه پیدا کردم`, 'ترکیب اعتبار تجربی با کلیدواژه‌ی موفق کانال.');

  return out.slice(0, 8);
}

module.exports = { analyze, median, tokens };
