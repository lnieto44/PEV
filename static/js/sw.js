self.addEventListener('install', event => {
    event.waitUntil(
        caches.open('help-centers-cache').then(cache => {
            return cache.addAll([
                '/', 
                '/get_help_centers',
                '/static/css/styles.css', 
                '/static/js/app.js',
                'https://unpkg.com/leaflet/dist/leaflet.css',
                'https://unpkg.com/leaflet/dist/leaflet.js'
            ]);
        })
    );
    self.skipWaiting();
});

self.addEventListener('fetch', event => {
    event.respondWith(
        fetch(event.request).catch(() => caches.match(event.request))
    );
});

self.addEventListener('sync', event => {
    if (event.tag === 'sync-help-centers') {
        event.waitUntil(syncHelpCenters());
    }
});

async function syncHelpCenters() {
    const db = await openDB();
    const tx = db.transaction('centers', 'readonly');
    const store = tx.objectStore('centers');
    const centers = await store.getAll();

    centers.forEach(center => {
        fetch('/sync_help_center', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(center)
        });
    });
}

async function openDB() {
    return new Promise((resolve, reject) => {
        const request = indexedDB.open('HelpCentersDB', 1);
        request.onsuccess = () => resolve(request.result);
        request.onerror = event => reject(event.target.errorCode);
    });
}
