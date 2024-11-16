// Al instalar el Service Worker, cacheamos recursos estáticos y rutas necesarias
self.addEventListener('install', event => {
    event.waitUntil(
        caches.open('help-centers-cache').then(cache => {
            return cache.addAll([
                '/', 
                '/get_help_centers',
                '/static/css/styles.css', 
                '/static/js/centro_ayuda.js',
                'https://unpkg.com/leaflet/dist/leaflet.css',
                'https://unpkg.com/leaflet/dist/leaflet.js'
            ]);
        })
    );
    self.skipWaiting(); // Activar el SW inmediatamente después de instalarlo
});

// Intercepta las solicitudes para manejar respuestas offline
self.addEventListener('fetch', event => {
    event.respondWith(
        fetch(event.request)
            .then(response => {
                // Actualizamos el cache con nuevas respuestas
                const responseClone = response.clone();
                caches.open('help-centers-cache').then(cache => {
                    cache.put(event.request, responseClone);
                });
                return response;
            })
            .catch(() => {
                // Responder desde el cache si estamos offline
                return caches.match(event.request);
            })
    );
});

// Maneja la sincronización en segundo plano
self.addEventListener('sync', event => {
    if (event.tag === 'sync-help-centers') {
        event.waitUntil(syncHelpCenters());
    }
});

// Función para sincronizar centros desde IndexedDB con el servidor
async function syncHelpCenters() {
    try {
        const db = await openDB();
        const tx = db.transaction('centers', 'readonly');
        const store = tx.objectStore('centers');
        const centers = await store.getAll();

        // Enviar los datos al servidor
        await Promise.all(
            centers.map(center =>
                fetch('/sync_help_center', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(center)
                })
            )
        );
        console.log('Centros sincronizados exitosamente.');
    } catch (error) {
        console.error('Error al sincronizar los centros:', error);
    }
}

// Función para abrir la base de datos IndexedDB
async function openDB() {
    return new Promise((resolve, reject) => {
        const request = indexedDB.open('HelpCentersDB', 1);
        
        // Crear el almacén de datos si es la primera vez que se abre
        request.onupgradeneeded = event => {
            const db = event.target.result;
            if (!db.objectStoreNames.contains('centers')) {
                db.createObjectStore('centers', { keyPath: 'id' });
            }
        };

        request.onsuccess = () => resolve(request.result);
        request.onerror = event => reject(event.target.errorCode);
    });
}

