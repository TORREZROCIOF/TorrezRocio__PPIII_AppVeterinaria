USE veterinaria;
INSERT INTO usuarios (nombre, email, password, rol, telefono) VALUES 
('Dr. Juan Pérez', 'juan.perez@vetclinic.com', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'admin', '3874-123456'),
('Dra. María González', 'maria.gonzalez@vetclinic.com', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'veterinario', '3874-234567'),
('Dr. Carlos Rodríguez', 'carlos.rodriguez@vetclinic.com', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'veterinario', '3874-345678'),
('Ana Martínez', 'ana.martinez@vetclinic.com', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'recepcionista', '3874-456789'),
('Laura Fernández', 'laura.fernandez@vetclinic.com', '$2y$10$92IXUNpkjO0rOQ5byMi.Ye4oKoEa3Ro9llC/.og/at2.uheWG/igi', 'recepcionista', '3874-567890');

INSERT INTO clientes (nombre, apellido, dni, email, telefono, direccion) VALUES 
('Roberto', 'López', '25123456', 'roberto.lopez@gmail.com', '3874-111222', 'Av. Belgrano 123, Salta Capital'),
('Sofía', 'García', '30456789', 'sofia.garcia@hotmail.com', '3874-222333', 'Calle Caseros 456, Salta Capital'),
('Miguel', 'Fernández', '28789012', 'miguel.fernandez@yahoo.com', '3874-333444', 'Pasaje San Martín 789, Cerrillos'),
('Lucía', 'Díaz', '35234567', 'lucia.diaz@outlook.com', '3874-444555', 'Av. Kennedy 321, Salta Capital'),
('Fernando', 'Sánchez', '32890123', 'fernando.sanchez@gmail.com', '3874-555666', 'Calle Balcarce 654, Salta Capital'),
('Valentina', 'Romero', '29567890', 'valentina.romero@gmail.com', '3874-666777', 'Av. Paraguay 987, Salta Capital'),
('Martín', 'Torres', '33123789', 'martin.torres@hotmail.com', '3874-777888', 'Calle España 147, Campo Quijano'),
('Carolina', 'Ruiz', '27456123', 'carolina.ruiz@gmail.com', '3874-888999', 'Av. San Martín 258, Rosario de la Frontera');

--  MASCOTAS 
INSERT INTO mascotas (cliente_id, nombre, especie, raza, sexo, fecha_nacimiento, peso, color, estado, alergias, observaciones) VALUES 
-- Cliente 1: Roberto López
(1, 'Max', 'perro', 'Labrador Retriever', 'macho', '2020-05-15', 32.50, 'Dorado', 'activo', NULL, 'Muy activo y juguetón'),
(1, 'Luna', 'gato', 'Siamés', 'hembra', '2021-08-20', 4.20, 'Crema con puntas oscuras', 'activo', NULL, 'Tímida con extraños'),

-- Cliente 2: Sofía García
(2, 'Rocky', 'perro', 'Pastor Alemán', 'macho', '2019-03-10', 38.00, 'Negro y marrón', 'activo', NULL, 'Entrenado como perro guardián'),
(2, 'Bella', 'perro', 'Golden Retriever', 'hembra', '2022-01-05', 28.00, 'Dorado claro', 'activo', NULL, 'Excelente con niños'),

-- Cliente 3: Miguel Fernández
(3, 'Michi', 'gato', 'Persa', 'macho', '2021-11-12', 5.50, 'Blanco', 'activo', 'Polen', 'Requiere aseo regular'),

-- Cliente 4: Lucía Díaz
(4, 'Coco', 'perro', 'French Poodle', 'hembra', '2020-07-25', 6.80, 'Blanco', 'activo', NULL, 'Muy cariñosa'),
(4, 'Pipo', 'ave', 'Loro', 'macho', '2019-02-14', 0.35, 'Verde y rojo', 'activo', NULL, 'Habla algunas palabras'),

-- Cliente 5: Fernando Sánchez
(5, 'Thor', 'perro', 'Rottweiler', 'macho', '2018-09-30', 45.00, 'Negro con marrón', 'activo', NULL, 'Necesita control de peso'),

-- Cliente 6: Valentina Romero
(6, 'Nala', 'gato', 'Angora', 'hembra', '2022-06-18', 3.80, 'Gris', 'activo', NULL, NULL),
(6, 'Simba', 'gato', 'Común Europeo', 'macho', '2022-06-18', 4.10, 'Naranja atigrado', 'activo', NULL, 'Hermano de Nala'),

-- Cliente 7: Martín Torres
(7, 'Bobby', 'perro', 'Beagle', 'macho', '2021-04-22', 12.50, 'Tricolor', 'activo', NULL, 'Tendencia a sobrepeso'),

-- Cliente 8: Carolina Ruiz
(8, 'Pelusa', 'roedor', 'Conejo', 'hembra', '2023-01-10', 2.30, 'Blanco con manchas negras', 'activo', NULL, 'Dieta especial');

-- CITAS 
INSERT INTO citas (mascota_id, veterinario_id, fecha_hora, motivo, estado, observaciones, duracion_minutos) VALUES 
-- Citas pasadas (completadas)
(1, 2, '2024-11-15 10:00:00', 'Control anual y vacunación', 'completada', 'Animal en buen estado general', 45),
(2, 2, '2024-11-15 11:00:00', 'Vacunación antirrábica', 'completada', NULL, 30),
(3, 3, '2024-11-18 09:30:00', 'Consulta por cojera', 'completada', 'Se detectó displasia de cadera leve', 60),
(5, 2, '2024-11-20 14:00:00', 'Corte de pelo y limpieza', 'completada', NULL, 90),

-- Citas de hoy
(4, 2, '2024-11-21 10:00:00', 'Primera consulta - cachorro', 'confirmada', 'Traer libreta sanitaria', 45),
(8, 3, '2024-11-21 11:30:00', 'Control de peso', 'confirmada', NULL, 30),
(6, 2, '2024-11-21 15:00:00', 'Vacunación', 'pendiente', NULL, 30),

-- Citas futuras
(7, 2, '2024-11-22 09:00:00', 'Desparasitación', 'pendiente', NULL, 30),
(9, 3, '2024-11-22 10:30:00', 'Control semestral', 'pendiente', NULL, 30),
(10, 2, '2024-11-23 14:00:00', 'Revisión dental', 'pendiente', NULL, 45),
(11, 3, '2024-11-25 11:00:00', 'Control post-esterilización', 'pendiente', NULL, 30),
(12, 2, '2024-11-26 16:00:00', 'Control mensual', 'pendiente', 'Verificar dieta', 30);

--  CONSULTAS 
INSERT INTO consultas (cita_id, mascota_id, veterinario_id, fecha_consulta, motivo_consulta, sintomas, diagnostico, tratamiento, peso_actual, temperatura, frecuencia_cardiaca, observaciones, proxima_visita) VALUES 
(1, 1, 2, '2024-11-15 10:00:00', 'Control anual y vacunación', 'Ninguno', 'Animal sano, condición corporal óptima', 'Aplicación de vacuna séxtuple y antirrábica. Continuar con alimentación balanceada premium.', 32.50, 38.5, 85, 'Excelente estado general. Dueño comprometido con cuidados.', '2025-11-15'),

(2, 2, 2, '2024-11-15 11:00:00', 'Vacunación antirrábica', 'Ninguno', 'Gato sano, peso adecuado', 'Vacuna antirrábica aplicada. Refuerzo en un año.', 4.20, 38.2, 140, 'Gato tranquilo durante la consulta.', '2025-11-15'),

(3, 3, 3, '2024-11-18 09:30:00', 'Consulta por cojera en pata trasera izquierda', 'Cojera intermitente, dolor al levantarse', 'Displasia de cadera grado leve (grado 1)', 'Condroprotectores (Cosequin) 1 comprimido cada 12hs por 60 días. Control de peso. Ejercicio moderado.', 38.00, 38.7, 90, 'Se realizó radiografía de cadera. Pronóstico favorable con tratamiento.', '2025-01-18'),

(4, 5, 2, '2024-11-20 14:00:00', 'Corte de pelo y limpieza general', 'Pelo muy enredado, orejas sucias', 'Higiene deficiente, otitis externa leve', 'Limpieza profunda realizada. Gotas óticas (Otomax) 3 gotas cada 12hs por 7 días. Recomendar baño mensual.', 5.50, 38.4, 150, 'Dueño indicó que viaja mucho y a veces descuida el aseo del gato.', '2024-12-20');

--  VACUNAS 
INSERT INTO vacunas (mascota_id, nombre_vacuna, fecha_aplicacion, proxima_dosis, veterinario_id, observaciones) VALUES 
-- Max (perro 1)
(1, 'Séxtuple canina (Parvovirus, Moquillo, etc.)', '2024-11-15', '2025-11-15', 2, 'Primera dosis anual'),
(1, 'Antirrábica', '2024-11-15', '2025-11-15', 2, 'Obligatoria'),
(1, 'Tos de las perreras', '2023-11-10', '2024-11-10', 2, 'Vencida - reagendar'),

-- Luna (gato 2)
(2, 'Triple felina', '2024-11-15', '2025-11-15', 2, NULL),
(2, 'Antirrábica felina', '2024-11-15', '2025-11-15', 2, NULL),

-- Rocky (perro 3)
(3, 'Séxtuple canina', '2024-03-10', '2025-03-10', 3, NULL),
(3, 'Antirrábica', '2024-03-10', '2025-03-10', 3, NULL),

-- Bella (perro 4)
(4, 'Séxtuple canina', '2024-02-05', '2025-02-05', 2, 'Cachorro - primera dosis'),
(4, 'Antirrábica', '2024-05-05', '2025-05-05', 2, 'Aplicada a los 4 meses'),

-- Michi (gato 5)
(5, 'Triple felina', '2023-12-12', '2024-12-12', 2, 'Próxima a vencer'),
(5, 'Antirrábica felina', '2023-12-12', '2024-12-12', 2, 'Próxima a vencer'),

-- Coco (perro 6)
(6, 'Séxtuple canina', '2024-07-25', '2025-07-25', 2, NULL),
(6, 'Antirrábica', '2024-07-25', '2025-07-25', 2, NULL),

-- Thor (perro 8)
(8, 'Séxtuple canina', '2024-09-30', '2025-09-30', 3, NULL),
(8, 'Antirrábica', '2024-09-30', '2025-09-30', 3, NULL);


--  Ver todos los usuarios activos
SELECT * FROM usuarios WHERE estado = TRUE;

--  Ver todos los clientes con sus datos de contacto
SELECT nombre, apellido, telefono, email, direccion 
FROM clientes 
WHERE estado = TRUE
ORDER BY apellido, nombre;

--  Ver todas las mascotas activas
SELECT nombre, especie, raza, sexo 
FROM mascotas 
WHERE estado = 'activo'
ORDER BY nombre;

-- Ver citas pendientes y confirmadas
SELECT * FROM citas 
WHERE estado IN ('pendiente', 'confirmada')
ORDER BY fecha_hora;
--  Ver mascotas con el nombre de su dueño
SELECT 
    m.nombre AS mascota,
    m.especie,
    m.raza,
    CONCAT(c.nombre, ' ', c.apellido) AS dueño,
    c.telefono
FROM mascotas m
INNER JOIN clientes c ON m.cliente_id = c.id
WHERE m.estado = 'activo'
ORDER BY c.apellido;

--  Ver citas con todos los detalles (mascota, dueño, veterinario)
SELECT 
    cit.id AS cita_id,
    cit.fecha_hora,
    cit.motivo,
    cit.estado,
    m.nombre AS mascota,
    m.especie,
    CONCAT(cli.nombre, ' ', cli.apellido) AS dueño,
    cli.telefono AS telefono_dueño,
    u.nombre AS veterinario
FROM citas cit
INNER JOIN mascotas m ON cit.mascota_id = m.id
INNER JOIN clientes cli ON m.cliente_id = cli.id
INNER JOIN usuarios u ON cit.veterinario_id = u.id
ORDER BY cit.fecha_hora DESC;

--  Historial médico completo de una mascota (ID = 1)
SELECT 
    con.fecha_consulta,
    con.motivo_consulta,
    con.diagnostico,
    con.tratamiento,
    con.peso_actual,
    u.nombre AS veterinario
FROM consultas con
INNER JOIN usuarios u ON con.veterinario_id = u.id
WHERE con.mascota_id = 1
ORDER BY con.fecha_consulta DESC;

--  Ver vacunas por mascota con información del dueño
SELECT 
    m.nombre AS mascota,
    CONCAT(c.nombre, ' ', c.apellido) AS dueño,
    v.nombre_vacuna,
    v.fecha_aplicacion,
    v.proxima_dosis,
    DATEDIFF(v.proxima_dosis, CURDATE()) AS dias_para_refuerzo
FROM vacunas v
INNER JOIN mascotas m ON v.mascota_id = m.id
INNER JOIN clientes c ON m.cliente_id = c.id
ORDER BY v.proxima_dosis;

-- Contar mascotas por especie
SELECT 
    especie,
    COUNT(*) AS cantidad
FROM mascotas
WHERE estado = 'activo'
GROUP BY especie
ORDER BY cantidad DESC;

