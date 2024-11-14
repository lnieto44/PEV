// Inicializa el mapa
let map;
document.getElementById('find_location').onclick = function() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showMap, showError);
    } else {
        alert("Geolocalización no es compatible con este navegador.");
    }
};

function showMap(position) {
    const userLat = position.coords.latitude;
    const userLng = position.coords.longitude;

    // Crea y centra el mapa en la ubicación del usuario
    map = L.map('map').setView([userLat, userLng], 13);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 19 }).addTo(map);

    L.marker([userLat, userLng]).addTo(map).bindPopup("<b>Tu ubicación</b>").openPopup();

    fetchHelpCenters();  // Carga los centros de ayuda
}

function fetchHelpCenters() {
    if (navigator.onLine) {
        fetch("/get_help_centers")
            .then(response => response.json())
            .then(data => {
                saveDataLocally(data);  // Guarda los datos para uso offline
                displayHelpCentersOnMap(data); // Muestra en el mapa
            })
            .catch(error => console.error("Error al obtener centros de ayuda:", error));
    } else {
        loadDataFromIndexedDB(displayHelpCentersOnMap);
    }
}


// Muestra los centros de ayuda en el mapa
function displayHelpCentersOnMap(centers) {
    centers.forEach(center => {
        L.marker([center.latitude, center.longitude]).addTo(map)
            .bindPopup(`<b>${center.name}</b><br>${center.address}`);
    });
}

// IndexedDB para almacenamiento offline
function saveDataLocally(data) { /* Código IndexedDB aquí */ }
function loadDataFromIndexedDB(callback) { /* Código IndexedDB aquí */ }

// Manejo de errores de geolocalización
function showError(error) {
    let errorMsg = "Error de geolocalización.";
    if (error.code === error.PERMISSION_DENIED) errorMsg = "Permiso de geolocalización denegado.";
    alert(errorMsg);
}

//registrar el Service Worker(sin conexion y conecta cuando vuelva la red)
if ('serviceWorker' in navigator && 'SyncManager' in window) {
    navigator.serviceWorker.register('/static/js/sw.js').then(registration => {
        console.log('Service Worker registrado con alcance:', registration.scope);
    }).catch(error => {
        console.error('Error al registrar el Service Worker:', error);
    });
}

//// Función para inicializar el mapa de centro_ayuda
function initMap() {
    const map = new google.maps.Map(document.getElementById("map"), {
        center: { lat: 4.6, lng: -74.08 }, // Coordenadas iniciales
        zoom: 12,
    });

    // Llamada para cargar los centros de ayuda
    fetchCentrosAyuda(map);
}

function fetchCentrosAyuda(map) {
    // Solicitar los centros de ayuda al servidor
    fetch('/api/centros_ayuda')
        .then(response => response.json())
        .then(data => {
            const centrosLista = document.getElementById('centros-lista');

            data.forEach(centro => {
                // Crear un marcador para cada centro en el mapa
                new google.maps.Marker({
                    position: { lat: parseFloat(centro.latitude), lng: parseFloat(centro.longitude) },
                    map: map,
                    title: centro.name,
                });

                // Agregar el centro a la lista de la página
                const listItem = document.createElement('li');
                listItem.className = 'list-group-item';
                listItem.innerHTML = `<i class="fas fa-map-marker-alt text-warning"></i> <strong>${centro.name}</strong> - ${centro.address}`;
                centrosLista.appendChild(listItem);
            });
        })
        .catch(error => console.error('Error al cargar los centros de ayuda:', error));
}


