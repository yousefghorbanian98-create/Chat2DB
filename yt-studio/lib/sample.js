'use strict';

/**
 * Deterministic demo dataset, so the app is fully usable before an API key exists.
 * Numbers are synthetic but shaped like a real mid-size channel.
 */

function mulberry32(seed) {
  let a = seed >>> 0;
  return function () {
    a |= 0;
    a = (a + 0x6d2b79f5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

const TEMPLATES = [
  ['۷ اشتباه رایج در {topic} که همه مرتکب می‌شوند', 2.6],
  ['چطور در ۱۰ دقیقه {topic} را یاد بگیریم؟', 2.1],
  ['{topic} در ۲۰۲۶ — همه چیزی که باید بدانید', 1.5],
  ['آیا {topic} واقعاً ارزشش را دارد؟', 1.7],
  ['راز {topic} که هیچ‌کس به شما نمی‌گوید', 3.1],
  ['{topic}: از صفر تا صد (آموزش کامل)', 1.2],
  ['۵ ابزار رایگان برای {topic}', 1.9],
  ['یک ماه {topic} را امتحان کردم — نتیجه شوکه‌کننده بود', 2.8],
  ['مقایسه {topic} با روش قدیمی', 0.9],
  ['بزرگ‌ترین اشتباه من در {topic}', 1.4],
  ['{topic} را متوقف کنید! این را ببینید', 2.3],
  ['بررسی کامل {topic} بعد از ۶ ماه استفاده', 1.1],
  ['{topic} برای مبتدی‌ها — قسمت اول', 0.7],
  ['چرا ۹۰٪ مردم در {topic} شکست می‌خورند', 2.9],
  ['پاسخ به سوالات شما درباره {topic}', 0.6],
  ['{topic} در عمل: یک پروژه واقعی', 0.8],
  ['بهترین تنظیمات {topic} که پیدا کردم', 1.3],
  ['{topic} رایگان در مقابل پولی — کدام؟', 1.6],
];

const TOPICS = [
  'ادیت ویدیو',
  'رشد کانال یوتیوب',
  'هوش مصنوعی',
  'تولید محتوا',
  'سئو ویدیو',
  'موبایل‌گرافی',
  'درآمد آنلاین',
  'میکروفن و صدا',
  'نورپردازی',
  'اسکریپت‌نویسی',
  'تدوین با موبایل',
  'برندسازی شخصی',
];

function buildSample() {
  const rnd = mulberry32(20260814);
  const videos = [];
  const now = Date.now();
  const base = 14000;

  for (let i = 0; i < 96; i++) {
    const t = TEMPLATES[Math.floor(rnd() * TEMPLATES.length)];
    const topic = TOPICS[Math.floor(rnd() * TOPICS.length)];
    const title = t[0].replace('{topic}', topic);
    const boost = t[1];

    // Newer videos slightly bigger channel; older ones fewer views.
    const ageDays = Math.floor(rnd() * 700) + 3;
    const publishedAt = new Date(now - ageDays * 86400000);
    // Nudge toward evening uploads on Tue/Thu/Sat
    const hourPool = [9, 12, 17, 18, 19, 19, 20, 20, 21, 22];
    publishedAt.setHours(hourPool[Math.floor(rnd() * hourPool.length)], Math.floor(rnd() * 60), 0, 0);

    const growth = 1 + (700 - ageDays) / 700;
    const luck = 0.35 + rnd() * rnd() * 3.4;
    const isShort = rnd() < 0.32;
    const durationSec = isShort
      ? 18 + Math.floor(rnd() * 42)
      : 240 + Math.floor(rnd() * 1500);
    const shortMult = isShort ? 2.4 : 1;

    const views = Math.round(base * boost * growth * luck * shortMult);
    const likeRate = 0.028 + rnd() * 0.045;
    const commentRate = 0.0016 + rnd() * 0.006;

    videos.push({
      id: `demo${String(i).padStart(3, '0')}`,
      title,
      description: `ویدیوی نمونه درباره ${topic}.`,
      publishedAt: publishedAt.toISOString(),
      durationSec,
      isShort: durationSec <= 60,
      views,
      likes: Math.round(views * likeRate),
      comments: Math.round(views * commentRate),
      tags: [topic, 'یوتیوب', 'آموزش'],
      thumbnail: '',
      url: 'https://www.youtube.com/',
      demo: true,
    });
  }

  videos.sort((a, b) => new Date(b.publishedAt) - new Date(a.publishedAt));
  const totalViews = videos.reduce((s, v) => s + v.views, 0);

  return {
    channel: {
      id: 'UCdemo00000000000000000',
      title: 'کانال نمونه (داده‌ی آزمایشی)',
      handle: '@demo-channel',
      description:
        'این یک کانال ساختگی است تا بتوانید بدون کلید API با داشبورد کار کنید. برای داده‌ی واقعی، کلید YouTube Data API v3 را در فایل .env قرار دهید.',
      country: 'IR',
      publishedAt: new Date(now - 900 * 86400000).toISOString(),
      thumbnail: '',
      banner: '',
      subscribers: 128400,
      hiddenSubscribers: false,
      totalViews,
      videoCount: videos.length,
      url: 'https://www.youtube.com/',
    },
    videos,
    demo: true,
  };
}

module.exports = { buildSample };
