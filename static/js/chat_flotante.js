document.addEventListener('DOMContentLoaded', () => {
    const socket = io();

    // Referencias al DOM
    const chatToggle = document.getElementById('chat-toggle');
    const chatBox = document.getElementById('chat-box');
    const chatClose = document.getElementById('chat-close');
    const chatContent = document.getElementById('chat-content');
    const chatForm = document.getElementById('chat-form');
    const chatMessage = document.getElementById('chat-message');

    // Mostrar/Ocultar el chat
    chatToggle.addEventListener('click', () => {
        chatBox.style.display = chatBox.style.display === 'none' ? 'block' : 'none';
    });

    // Cerrar el chat
    chatClose.addEventListener('click', () => {
        chatBox.style.display = 'none';
    });

    // Enviar mensaje al servidor
    chatForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const message = chatMessage.value.trim();
        if (message) {
            socket.emit('chatMessage', { user: 'Usuario', message });
            addMessageToChat('Tú', message);
            chatMessage.value = '';
        }
    });

    // Escuchar respuesta del servidor
    socket.on('message', (data) => {
        addMessageToChat(data.user, data.message);
    });

    // Función para agregar mensajes al chat
    function addMessageToChat(user, message) {
        const messageElement = document.createElement('div');
        messageElement.style.marginBottom = '10px';
        messageElement.innerHTML = `<strong>${user}:</strong> ${message}`;
        chatContent.appendChild(messageElement);
        chatContent.scrollTop = chatContent.scrollHeight;
    }
});

console.log("DOM cargado");
chatToggle.addEventListener('click', () => {
    console.log("Chat toggle presionado");
    chatBox.style.display = chatBox.style.display === 'none' ? 'block' : 'none';
});
