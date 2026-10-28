/**
 * Prajñā Reader Service Worker (v2)
 * High performance offline caching with network-first updates for app shell
 */

const CACHE_NAME = 'prajna-cache-v4';

const STATIC_ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './css/themes.css',
  './css/app.css',
  './js/app.js',
  './js/parser.js',
  './js/storage.js',
  './js/search.js',
  './js/audio.js',
  './data/toc.json',
  './assets/icon-192.svg',
  './assets/icon-512.svg'
];

self.addEventListener('install', (e) => {
  self.skipWaiting();
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(STATIC_ASSETS);
    })
  );
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then((keys) => {
      return Promise.all(
        keys.map((key) => {
          if (key !== CACHE_NAME) {
            return caches.delete(key);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', (e) => {
  const url = new URL(e.request.url);

  // Network-first for html and css to ensure instant UI updates
  if (url.pathname.endsWith('.html') || url.pathname.endsWith('.css') || url.pathname.endsWith('.js')) {
    e.respondWith(
      fetch(e.request)
        .then((networkResp) => {
          if (networkResp && networkResp.status === 200) {
            const copy = networkResp.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(e.request, copy));
          }
          return networkResp;
        })
        .catch(() => caches.match(e.request))
    );
    return;
  }

  // Cache-first for markdown texts & large assets
  e.respondWith(
    caches.match(e.request).then((cachedResp) => {
      if (cachedResp) {
        return cachedResp;
      }
      return fetch(e.request)
        .then((networkResp) => {
          if (!networkResp || networkResp.status !== 200) {
            return networkResp;
          }
          const respToCache = networkResp.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(e.request, respToCache);
          });
          return networkResp;
        })
        .catch(() => caches.match('./index.html'));
    })
  );
});
