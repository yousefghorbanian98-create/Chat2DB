'use strict';

/**
 * YouTube Data API v3 client.
 * Requires an API key from Google Cloud Console (YouTube Data API v3 -> Credentials -> API key).
 */

const API = 'https://www.googleapis.com/youtube/v3';

class YouTubeError extends Error {
  constructor(message, status, reason) {
    super(message);
    this.name = 'YouTubeError';
    this.status = status;
    this.reason = reason;
  }
}

async function call(endpoint, params, key) {
  const url = new URL(`${API}/${endpoint}`);
  for (const [k, v] of Object.entries(params)) {
    if (v !== undefined && v !== null && v !== '') url.searchParams.set(k, v);
  }
  url.searchParams.set('key', key);

  const res = await fetch(url, { headers: { Accept: 'application/json' } });
  const text = await res.text();
  let body;
  try {
    body = JSON.parse(text);
  } catch {
    throw new YouTubeError(`پاسخ نامعتبر از YouTube API (HTTP ${res.status})`, res.status, 'badResponse');
  }

  if (!res.ok) {
    const err = body?.error?.errors?.[0] || {};
    const reason = err.reason || 'unknown';
    const msg = body?.error?.message || `HTTP ${res.status}`;
    throw new YouTubeError(msg, res.status, reason);
  }
  return body;
}

/** Extract a channel handle / id / search term from anything the user pastes. */
function parseChannelInput(raw) {
  const input = String(raw || '').trim();
  if (!input) return null;

  // Bare channel id
  if (/^UC[\w-]{22}$/.test(input)) return { type: 'id', value: input };
  // Bare handle
  if (/^@[\w.\-]{3,30}$/.test(input)) return { type: 'handle', value: input.slice(1) };

  let u = null;
  try {
    u = new URL(input.startsWith('http') ? input : `https://${input}`);
  } catch {
    return { type: 'search', value: input };
  }

  if (!/(^|\.)youtube\.com$|(^|\.)youtu\.be$/.test(u.hostname)) {
    return { type: 'search', value: input };
  }

  const parts = u.pathname.split('/').filter(Boolean);

  // /watch?v=... or /shorts/ID or youtu.be/ID -> resolve channel via the video
  if (parts[0] === 'watch' && u.searchParams.get('v')) {
    return { type: 'video', value: u.searchParams.get('v') };
  }
  if ((parts[0] === 'shorts' || parts[0] === 'live' || parts[0] === 'embed') && parts[1]) {
    return { type: 'video', value: parts[1] };
  }
  if (u.hostname.endsWith('youtu.be') && parts[0]) {
    return { type: 'video', value: parts[0] };
  }

  for (let i = 0; i < parts.length; i++) {
    const p = parts[i];
    if (p.startsWith('@')) return { type: 'handle', value: p.slice(1) };
    if (p === 'channel' && parts[i + 1]) return { type: 'id', value: parts[i + 1] };
    if ((p === 'c' || p === 'user') && parts[i + 1]) {
      return { type: 'search', value: decodeURIComponent(parts[i + 1]) };
    }
  }
  return { type: 'search', value: input };
}

const CHANNEL_PARTS = 'snippet,statistics,contentDetails,brandingSettings';

async function resolveChannel(raw, key) {
  const parsed = parseChannelInput(raw);
  if (!parsed) throw new YouTubeError('نام یا لینک کانال را وارد کنید.', 400, 'emptyInput');

  if (parsed.type === 'id') {
    const r = await call('channels', { part: CHANNEL_PARTS, id: parsed.value }, key);
    if (r.items?.length) return r.items[0];
  }

  if (parsed.type === 'handle') {
    const r = await call('channels', { part: CHANNEL_PARTS, forHandle: parsed.value }, key);
    if (r.items?.length) return r.items[0];
    // fall back to search if the handle lookup misses
    parsed.type = 'search';
  }

  if (parsed.type === 'video') {
    const v = await call('videos', { part: 'snippet', id: parsed.value }, key);
    const cid = v.items?.[0]?.snippet?.channelId;
    if (cid) {
      const r = await call('channels', { part: CHANNEL_PARTS, id: cid }, key);
      if (r.items?.length) return r.items[0];
    }
    throw new YouTubeError('ویدیوی این لینک پیدا نشد.', 404, 'videoNotFound');
  }

  // search (costs 100 quota units)
  const s = await call(
    'search',
    { part: 'snippet', type: 'channel', q: parsed.value, maxResults: 1 },
    key,
  );
  const cid = s.items?.[0]?.snippet?.channelId || s.items?.[0]?.id?.channelId;
  if (!cid) throw new YouTubeError('کانالی با این مشخصات پیدا نشد.', 404, 'channelNotFound');
  const r = await call('channels', { part: CHANNEL_PARTS, id: cid }, key);
  if (!r.items?.length) throw new YouTubeError('کانالی با این مشخصات پیدا نشد.', 404, 'channelNotFound');
  return r.items[0];
}

/** Pull up to `limit` most recent uploads (cheap: 1 unit per 50 items). */
async function fetchUploads(uploadsPlaylistId, key, limit = 150) {
  const ids = [];
  let pageToken;
  while (ids.length < limit) {
    const r = await call(
      'playlistItems',
      {
        part: 'contentDetails',
        playlistId: uploadsPlaylistId,
        maxResults: Math.min(50, limit - ids.length),
        pageToken,
      },
      key,
    );
    for (const it of r.items || []) {
      const id = it.contentDetails?.videoId;
      if (id) ids.push(id);
    }
    pageToken = r.nextPageToken;
    if (!pageToken) break;
  }
  return ids;
}

async function fetchVideoDetails(ids, key) {
  const out = [];
  for (let i = 0; i < ids.length; i += 50) {
    const chunk = ids.slice(i, i + 50);
    const r = await call(
      'videos',
      { part: 'snippet,statistics,contentDetails', id: chunk.join(',') },
      key,
    );
    out.push(...(r.items || []));
  }
  return out;
}

/** ISO-8601 duration -> seconds */
function parseDuration(iso) {
  const m = /^P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+(?:\.\d+)?)S)?$/.exec(iso || '');
  if (!m) return 0;
  const [, d, h, mi, s] = m;
  return (+d || 0) * 86400 + (+h || 0) * 3600 + (+mi || 0) * 60 + Math.round(+s || 0);
}

function normalizeVideo(v) {
  const sec = parseDuration(v.contentDetails?.duration);
  const views = Number(v.statistics?.viewCount || 0);
  const likes = Number(v.statistics?.likeCount || 0);
  const comments = Number(v.statistics?.commentCount || 0);
  const publishedAt = v.snippet?.publishedAt;
  const thumbs = v.snippet?.thumbnails || {};
  return {
    id: v.id,
    title: v.snippet?.title || '',
    description: (v.snippet?.description || '').slice(0, 400),
    publishedAt,
    durationSec: sec,
    isShort: sec > 0 && sec <= 60,
    views,
    likes,
    comments,
    tags: v.snippet?.tags || [],
    thumbnail:
      thumbs.medium?.url || thumbs.high?.url || thumbs.default?.url ||
      `https://i.ytimg.com/vi/${v.id}/mqdefault.jpg`,
    url: `https://www.youtube.com/watch?v=${v.id}`,
  };
}

async function getChannelData(raw, key, limit = 150) {
  const ch = await resolveChannel(raw, key);
  const uploads = ch.contentDetails?.relatedPlaylists?.uploads;
  if (!uploads) throw new YouTubeError('این کانال لیست آپلود عمومی ندارد.', 404, 'noUploads');

  const ids = await fetchUploads(uploads, key, limit);
  const details = await fetchVideoDetails(ids, key);

  return {
    channel: {
      id: ch.id,
      title: ch.snippet?.title || '',
      handle: ch.snippet?.customUrl || '',
      description: (ch.snippet?.description || '').slice(0, 500),
      country: ch.snippet?.country || '',
      publishedAt: ch.snippet?.publishedAt,
      thumbnail:
        ch.snippet?.thumbnails?.medium?.url || ch.snippet?.thumbnails?.default?.url || '',
      banner: ch.brandingSettings?.image?.bannerExternalUrl || '',
      subscribers: Number(ch.statistics?.subscriberCount || 0),
      hiddenSubscribers: !!ch.statistics?.hiddenSubscriberCount,
      totalViews: Number(ch.statistics?.viewCount || 0),
      videoCount: Number(ch.statistics?.videoCount || 0),
      url: `https://www.youtube.com/channel/${ch.id}`,
    },
    videos: details.map(normalizeVideo).filter((v) => v.publishedAt),
  };
}

module.exports = { getChannelData, parseChannelInput, parseDuration, YouTubeError };
