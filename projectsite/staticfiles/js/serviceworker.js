self.addEventListener('install', function (e) {
    e.waitUntil(
        caches.open('projectsite-cache-v1').then(function (cache) {
            return cache.addAll([
                '/',
            ]).catch(function(error) {
                console.log('Cache install failed:', error);
            });
        })
    );
    self.skipWaiting();
});

self.addEventListener('activate', function (e) {
    e.waitUntil(clients.claim());
});

self.addEventListener('fetch', function (e) {
    // Only handle http and https requests, ignore chrome-extension and other schemes
    if (!e.request.url.startsWith('http')) {
        return;
    }
    
    e.respondWith(
        fetch(e.request)
            .then(function (response) {
                if (response && response.status === 200) {
                    var responseToCache = response.clone();
                    caches.open('projectsite-cache-v1').then(function (cache) {
                        cache.put(e.request, responseToCache);
                    });
                }
                return response;
            })
            .catch(function () {
                return caches.match(e.request);
            })
    );
});
