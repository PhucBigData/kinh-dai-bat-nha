/**
 * Prajñā Reader Service Worker (v10)
 * Network-first for all code/HTML assets to ensure instant UI updates
 */

const CACHE_NAME = 'prajna-cache-v10';

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
  './js/search_fulltext.js',
  './js/glossary.js',
  './js/audio.js',
  './data/toc.json',
  './data/glossary.json',
  './assets/icon-192.svg',
  './assets/icon-512.svg'
];

self.addEventListener('install', (e) => {
  self.skipWaiting();
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) => cache.addAll(STATIC_ASSETS))
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

  // Network-first for HTML, root slash, CSS, JS, JSON
  const isCodeAsset = 
    url.pathname.endsWith('/') ||
    url.pathname.endsWith('.html') ||
    url.pathname.endsWith('.css') ||
    url.pathname.endsWith('.js') ||
    url.pathname.endsWith('.json');

  if (isCodeAsset) {
    e.respondWith(
      fetch(e.request)
        .then((networkResp) => {
          if (networkResp && networkResp.status === 200) {
            const copy = networkResp.clone();
            caches.open(CACHE_NAME).then((cache) => cache.put(e.request, copy));
          }
          return networkResp;
        })
        .catch(() => caches.match(e.request).then(cached => cached || caches.match('./index.html')))
    );
    return;
  }

  // Cache-first for markdown scriptures & images
  e.respondWith(
    caches.match(e.request).then((cachedResp) => {
      if (cachedResp) return cachedResp;
      return fetch(e.request).then((networkResp) => {
        if (networkResp && networkResp.status === 200) {
          const copy = networkResp.clone();
          caches.open(CACHE_NAME).then((cache) => cache.put(e.request, copy));
        }
        return networkResp;
      });
    })
  );
});
