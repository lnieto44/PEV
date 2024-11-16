 // Inicializa el mapa sin ubicación inicial
 let map = L.map('map');

 // Agregar capa base al mapa
 L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
     maxZoom: 19,
     attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
 }).addTo(map);

 // Intentar obtener la ubicación del usuario
 if (navigator.geolocation) {
     navigator.geolocation.getCurrentPosition(
         (position) => {
             const { latitude, longitude } = position.coords;

             // Centrar el mapa en la ubicación del usuario
             map.setView([latitude, longitude], 15);

             // Agregar un marcador para la ubicación actual del usuario
             L.marker([latitude, longitude])
                 .addTo(map)
                 .bindPopup('<b>Estás aquí</b>')
                 .openPopup();

             // Cargar los centros de ayuda
             cargarCentrosAyuda(map);
         },
         () => {
             // Si la geolocalización falla o es rechazada
             map.setView([4.60971, -74.08175], 12); // Bogotá como referencia
             alert("No se pudo acceder a tu ubicación. Mostrando Bogotá como referencia.");
             cargarCentrosAyuda(map);
         }
     );
 } else {
     // Si el navegador no soporta geolocalización
     map.setView([4.60971, -74.08175], 12);
     alert("Geolocalización no soportada por tu navegador. Mostrando Bogotá como referencia.");
     cargarCentrosAyuda(map);
 }

 // Función para cargar los centros de ayuda desde la API
 function cargarCentrosAyuda(map) {
     fetch('/api/centros_ayuda')
         .then(response => response.json())
         .then(centros => {
             centros.forEach(centro => {
                 // Agregar un marcador para cada centro de ayuda
                 L.marker([centro.latitude, centro.longitude])
                     .addTo(map)
                     .bindPopup(`<strong>${centro.name}</strong><br>${centro.address}`);
             });
         })
         .catch(error => console.error('Error al cargar los centros de ayuda:', error));
 }

 function displayHelpCentersOnMap(centers) {
 centers.forEach(center => {
     // Crear marcador y agregar ventana emergente con nombre y dirección
     L.marker([center.latitude, center.longitude]).addTo(map)
         .bindPopup(`<b>${center.name}</b><br>${center.address}`);
 });
}


// IndexedDB: Guardar datos
function saveCentersToIndexedDB(centers) {
    const request = indexedDB.open('HelpCentersDB', 1);

    request.onupgradeneeded = event => {
        const db = event.target.result;
        if (!db.objectStoreNames.contains('centers')) {
            db.createObjectStore('centers', { keyPath: 'id' });
        }
    };

    request.onsuccess = event => {
        const db = event.target.result;
        const transaction = db.transaction('centers', 'readwrite');
        const store = transaction.objectStore('centers');

        store.clear(); // Limpia datos antiguos
        centers.forEach(center => store.put(center));
    };
}

// IndexedDB: Cargar datos
function loadCentersFromIndexedDB(callback) {
    const request = indexedDB.open('HelpCentersDB', 1);

    request.onsuccess = event => {
        const db = event.target.result;
        const transaction = db.transaction('centers', 'readonly');
        const store = transaction.objectStore('centers');
        const getAllRequest = store.getAll();

        getAllRequest.onsuccess = () => callback(getAllRequest.result);
    };
}
