/*
 * Service Worker استودیو/کیوسک (M20) — به‌روزرسانی بدون نصب مجدد.
 * استراتژی: cache-first برای assets هش‌دار + network-first برای HTML/مانیفست.
 * فعال‌سازی نسخهٔ جدید با SKIP_WAITING + reload — بدون حذف/نصب.
 */
const CACHE = "mp-studio-v1";

self.addEventListener("install", () => {
  self.skipWaiting();
});

self.addEventListener("activate", (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((keys) => Promise.all(keys.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("message", (event) => {
  // پیام «به‌روزرسانی» از UI — فعال‌سازی فوری نسخهٔ جدید
  if (event.data === "SKIP_WAITING") self.skipWaiting();
});

self.addEventListener("fetch", (event) => {
  const url = new URL(event.request.url);
  // API و مانیفست: همیشه شبکه (دادهٔ تازه)
  if (url.pathname.startsWith("/api/")) return;
  // assets هش‌دار (Vite): cache-first
  if (url.pathname.startsWith("/assets/")) {
    event.respondWith(
      caches.match(event.request).then(
        (hit) =>
          hit ||
          fetch(event.request).then((resp) => {
            const copy = resp.clone();
            caches.open(CACHE).then((c) => c.put(event.request, copy));
            return resp;
          })
      )
    );
    return;
  }
  // HTML: شبکه با fallback کش (آفلاین)
  event.respondWith(
    fetch(event.request)
      .then((resp) => {
        const copy = resp.clone();
        caches.open(CACHE).then((c) => c.put(event.request, copy));
        return resp;
      })
      .catch(() => caches.match(event.request))
  );
});
