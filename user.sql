-- Crear tabla de roles
CREATE TABLE IF NOT EXISTS roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_name TEXT NOT NULL UNIQUE
);

-- Insertar roles iniciales (admin y user)
INSERT INTO roles (role_name) VALUES ('admin'), ('user');

-- Crear tabla de usuarios con role_id como clave foránea
CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    tipo_documento TEXT,
    cedula INTEGER,
    primer_nombre TEXT,
    segundo_nombre TEXT,
    primer_apellido TEXT,
    segundo_apellido TEXT,
    edad INTEGER,
    role_id INTEGER NOT NULL,  -- Llave foránea que referencia roles.id
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES roles(id) ON DELETE SET NULL ON UPDATE CASCADE
);

-- Insertar usuarios en la tabla usuarios
INSERT INTO usuarios (username, password, email, tipo_documento, cedula, primer_nombre, segundo_nombre, primer_apellido, segundo_apellido, edad, role_id) VALUES
('admin1', 'hashed_password1', 'admin1@example.com', 'CC', 12345678, 'Juan', '', 'Pérez', '', 35, 1),
('admin2', 'hashed_password2', 'admin2@example.com', 'CC', 87654321, 'Ana', '', 'Gómez', '', 40, 1),
('user1', 'hashed_password3', 'user1@example.com', 'TI', 11223344, 'Carlos', 'Andrés', 'Rodríguez', '', 20, 2),
('user2', 'hashed_password4', 'user2@example.com', 'TI', 55667788, 'María', 'José', 'López', 'García', 28, 2),
('user3', 'hashed_password5', 'user3@example.com', 'CC', 99001122, 'Luis', '', 'Martínez', 'Hernández', 32, 2),
('user4', 'hashed_password6', 'user4@example.com', 'CC', 33445566, 'Laura', '', 'Fernández', '', 26, 2),
('user5', 'hashed_password7', 'user5@example.com', 'CE', 77889900, 'José', 'Luis', 'Torres', '', 30, 2),
('user6', 'hashed_password8', 'user6@example.com', 'CC', 55443322, 'Sofía', '', 'Ramos', '', 24, 2),
('user7', 'hashed_password9', 'user7@example.com', 'TI', 66778899, 'Camila', 'Andrea', 'Morales', '', 27, 2),
('user8', 'hashed_password10', 'user8@example.com', 'CE', 11224455, 'Miguel', 'Ángel', 'Ruiz', '', 29, 2);

-- Crear tabla de centros de ayuda
CREATE TABLE IF NOT EXISTS centros_ayuda (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    address TEXT,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL
);

-- Insertar centros de ayuda en la tabla centros_ayuda
INSERT INTO centros_ayuda (name, address, latitude, longitude) VALUES
('Centro de Atención Norte', 'Carrera 15 #45-10', 4.710989, -74.072092),
('Centro de Ayuda Sur', 'Calle 20 #30-40', 4.609710, -74.081750),
('Centro de Emergencias Este', 'Avenida 68 #50-40', 4.628500, -74.061500),
('Punto de Atención Oeste', 'Calle 80 #90-10', 4.690000, -74.100000),
('Centro Integral de Apoyo', 'Carrera 30 #45-90', 4.649900, -74.072000),
('Centro de Ayuda Central', 'Avenida Caracas #50-60', 4.621700, -74.073200),
('Unidad de Soporte Social', 'Calle 53 #30-20', 4.631200, -74.085300),
('Centro Familiar de Ayuda', 'Carrera 70 #40-15', 4.676400, -74.108800),
('Punto de Asistencia Norte', 'Calle 100 #15-10', 4.692300, -74.054500),
('Centro de Apoyo Psicológico', 'Carrera 10 #70-20', 4.657000, -74.059000);

-- Crear tabla de denuncias
CREATE TABLE IF NOT EXISTS denuncias (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL,
    incident_type TEXT NOT NULL,
    location TEXT NOT NULL,
    user_id INTEGER NOT NULL,       -- Llave foránea que referencia usuarios.id
    center_id INTEGER,              -- Llave foránea opcional que referencia centros_ayuda.id
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES usuarios(id) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (center_id) REFERENCES centros_ayuda(id) ON DELETE SET NULL ON UPDATE CASCADE
);

-- Crear tabla de registros de actividad (logs)
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,       -- Llave foránea que referencia usuarios.id
    action TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    details TEXT,
    FOREIGN KEY (user_id) REFERENCES usuarios(id) ON DELETE CASCADE ON UPDATE CASCADE
);


-- Obtener todos los logs
SELECT * FROM logs ORDER BY timestamp DESC;

-- Obtener los logs de un usuario específico
SELECT * FROM logs WHERE user_id = 1 ORDER BY timestamp DESC;

SELECT * FROM logs WHERE action IN ('obtener_centros_ayuda', 'sync_help_center') ORDER BY timestamp DESC;

