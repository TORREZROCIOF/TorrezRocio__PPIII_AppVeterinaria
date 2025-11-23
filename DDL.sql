DROP DATABASE IF EXISTS veterinaria;
CREATE DATABASE veterinaria CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE veterinaria;
-- TABLA: usuarios
CREATE TABLE usuarios (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL COMMENT 'Hash bcrypt/pbkdf2',
    rol ENUM('admin', 'veterinario', 'recepcionista') DEFAULT 'recepcionista',
    telefono VARCHAR(20),
    estado BOOLEAN DEFAULT TRUE
);
-- TABLA: clientes
CREATE TABLE clientes (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    dni VARCHAR(20) UNIQUE,
    email VARCHAR(150),
    telefono VARCHAR(20) NOT NULL,
    direccion TEXT,
    estado BOOLEAN DEFAULT TRUE
);
-- TABLA: mascotas
CREATE TABLE mascotas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cliente_id INT NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    especie ENUM('perro', 'gato', 'ave', 'roedor', 'reptil', 'otro') NOT NULL,
    raza VARCHAR(100),
    sexo ENUM('macho', 'hembra') NOT NULL,
    fecha_nacimiento DATE,
    peso DECIMAL(6,2) COMMENT 'Peso en kilogramos',
    color VARCHAR(50),
    foto_url VARCHAR(255),
    estado ENUM('activo', 'fallecido', 'transferido') DEFAULT 'activo',
    alergias TEXT,
    observaciones TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);
-- TABLA: citas
CREATE TABLE citas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    mascota_id INT NOT NULL,
    veterinario_id INT NOT NULL,
    fecha_hora DATETIME NOT NULL,
    motivo VARCHAR(255) NOT NULL,
    estado ENUM('pendiente', 'confirmada', 'en_curso', 'completada', 'cancelada') DEFAULT 'pendiente',
    observaciones TEXT,
    duracion_minutos INT DEFAULT 30,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fecha_cancelacion TIMESTAMP NULL,
    FOREIGN KEY (mascota_id) REFERENCES mascotas(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (veterinario_id) REFERENCES usuarios(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);
-- TABLA: consultas
CREATE TABLE consultas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    cita_id INT NOT NULL,
    mascota_id INT NOT NULL,
    veterinario_id INT NOT NULL,
    fecha_consulta DATETIME NOT NULL,
    motivo_consulta TEXT NOT NULL,
    sintomas TEXT,
    diagnostico TEXT,
    tratamiento TEXT,
    peso_actual DECIMAL(6,2),
    temperatura DECIMAL(4,2),
    frecuencia_cardiaca INT,
    observaciones TEXT,
    proxima_visita DATE,
    fecha_creacion TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (cita_id) REFERENCES citas(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (mascota_id) REFERENCES mascotas(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (veterinario_id) REFERENCES usuarios(id)
        ON DELETE RESTRICT
        ON UPDATE CASCADE
);
-- TABLA: vacunas
CREATE TABLE vacunas (
    id INT PRIMARY KEY AUTO_INCREMENT,
    mascota_id INT NOT NULL,
    nombre_vacuna VARCHAR(100) NOT NULL,
    fecha_aplicacion DATE NOT NULL,
    proxima_dosis DATE,
    veterinario_id INT,
    observaciones TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (mascota_id) REFERENCES mascotas(id)
        ON DELETE CASCADE
        ON UPDATE CASCADE,
    FOREIGN KEY (veterinario_id) REFERENCES usuarios(id)
        ON DELETE SET NULL
        ON UPDATE CASCADE
) ;