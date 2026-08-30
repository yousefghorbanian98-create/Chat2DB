/**
 * Muscle Paradise service worker.
 *
 * Caching policy, chosen deliberately:
 *  - navigations  -> network first, cached shell when the core is unreachable
 *  - hashed assets -> cache first (filenames are content-hashed, so immutable)
 *  - icons/manifest -> stale-while-revalidate
 *  - /api and /health -> NEVER cached. Serving a stale member row or a stale
 *    membership-expiry date would be a correctness bug, not an optimisation.
 */
const VERSION = 'mp-v0.19.0';
const SHELL = `${VERSION}-shell`;
const ASSETS = `${VERSION}-assets`;

const PRECACHE = ['./', './client.html', './manifest.webmanifest', './client.webmanifest'];

/** True for the API and health endpoints, which must always hit the core. */
function isApi(url) {
  return url.pathname.startsWith('/api/') || url.pathname === '/health' || url.pathname === '/meta';
}

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches
      .open(SHELL)
      .then((cache) => cache.addAll(PRECACHE))
      .catch(() => undefined) // offline install must not fail the whole worker
      .then(() => self.skipWaiting()),
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches
      .keys()
      .then((keys) =>
        Promise.all(keys.filter((k) => !k.startsWith(VERSION)).map((k) => caches.delete(k))),
      )
      .then(() => self.clients.claim()),
  );
});

/** Cache-first for immutable hashed bundles. */
function assetFirst(request) {
  return caches.match(request).then(
    (hit) =>
      hit ||
      fetch(request).then((response) => {
        if (response.ok) {
          const copy = response.clone();
          caches.open(ASSETS).then((cache) => cache.put(request, copy));
        }
        return response;
      }),
  );
}

/** Network-first with a cached-shell fallback, so the app opens offline. */
function shellFirst(request, fallback) {
  return fetch(request)
    .then((response) => {
      if (response.ok) {
        const copy = response.clone();
        caches.open(SHELL).then((cache) => cache.put(fallback, copy));
      }
      return response;
    })
    .catch(() => caches.match(fallback).then((hit) => hit || caches.match('./')));
}

self.addEventListener('fetch', (event) => {
  const { request } = event;
  if (request.method !== 'GET') return;

  const url = new URL(request.url);
  if (url.origin !== self.location.origin) return;
  if (isApi(url)) return; // always live

  if (request.mode === 'navigate') {
    const fallback = url.pathname.endsWith('client.html') ? './client.html' : './';
    event.respondWith(shellFirst(request, fallback));
    return;
  }

  if (url.pathname.startsWith('/assets/')) {
    event.respondWith(assetFirst(request));
    return;
  }

  event.respondWith(
    caches.match(request).then(
      (hit) =>
        hit ||
        fetch(request).then((response) => {
          if (response.ok) {
            const copy = response.clone();
            caches.open(ASSETS).then((cache) => cache.put(request, copy));
          }
          return response;
        }),
    ),
  );
});
