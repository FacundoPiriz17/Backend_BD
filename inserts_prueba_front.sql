INSERT INTO usuario (ci, nombre, apellido, email, rol)
VALUES(55574121, 'Facundo', 'Piriz', 'facundo.piriz@correo.ucu.edu.uy', 'Administrador'),
      (56901393, 'Diego', 'De Olivera', 'diego.deoliveira@correo.ucu.edu.uy', 'Funcionario'),
      (55992757, 'Agustín', 'García', 'agustin.garciab@correo.ucu.edu.uy', 'Participante');

INSERT INTO login (email, contrasena) VALUES
('facundo.piriz@correo.ucu.edu.uy', '$2b$12$c2kgM37h6ri1RGeroGPsMOZoZJwXLMyKYhLkhtmMWJRkKQXdh1ey2'),
('diego.deoliveira@correo.ucu.edu.uy','$2b$12$c2kgM37h6ri1RGeroGPsMOZoZJwXLMyKYhLkhtmMWJRkKQXdh1ey2'),
('agustin.garciab@correo.ucu.edu.uy','$2b$12$c2kgM37h6ri1RGeroGPsMOZoZJwXLMyKYhLkhtmMWJRkKQXdh1ey2');

INSERT INTO facultad (nombre_facultad) VALUES
('Ingeniería y Tecnologías'),
('Derecho y Ciencias Humanas'),
('Ciencias Empresariales'),
('Ciencias de la Salud');

INSERT INTO planAcademico (nombre_plan, id_Facultad, tipo) VALUES
('Ingeniería en Informática 2021', 1, 'Grado'),
('Maestría en Informática 2021', 1, 'Grado'),
('Administración de Empresas 2020', 2, 'Grado'),
('Psicología Clínica 2019', 4, 'Grado'),
('Dirección Avanzada de Empresas 2010', 3, 'Posgrado');

INSERT INTO participanteProgramaAcademico (ci_participante, nombre_plan, rol) VALUES
(55574121, 'Ingeniería en Informática 2021', 'Docente'),
(56901393, 'Ingeniería en Informática 2021', 'Alumno'),
(56901393, 'Ingeniería en Informática 2021', 'Alumno');

INSERT INTO edificio (nombre_edificio, direccion, campus) VALUES
('Edificio Sacré Coeur','Av. 8 de Octubre 2738','Montevideo'),
('Edificio Semprún','Estero Bellaco 2771','Montevideo'),
('Edificio Mullin','Comandante Braga 2715','Montevideo'),
('Edificio San Ignacio','Cornelio Cantera 2733','Montevideo'),
('Edificio Athanasius','Gral. Urquiza 2871','Montevideo'),
('Edificio Madre Marta','Av. Garibaldi 2831','Montevideo'),
('Casa Xalambrí','Cornelio Cantera 2728','Montevideo'),
('Edificio San José','Av. 8 de Octubre 2733','Montevideo'),
('Campus Salto', 'Artigas 1251', 'Salto'),
('Edificio Candelaria', 'Av. Roosevelt y Florencia, parada 7 y 1/2', 'Punta del este'),
('San Fernando', 'Av. Roosevelt y Oslo, parada 7 y 1/2', 'Punta del este');

INSERT INTO salasDeEstudio (nombre_sala, edificio, capacidad, tipo_sala, disponible) VALUES
                                                                                         ('Sala 1', 'Edificio Sacré Coeur', 20, 'Libre', TRUE),
                                                                                         ('Sala 2', 'Edificio Sacré Coeur', 8, 'Docente', TRUE),
                                                                                         ('Sala S1', 'Edificio Semprún', 16, 'Posgrado', TRUE),
                                                                                         ('Sala S2', 'Edificio Semprún', 10, 'Libre', FALSE),
                                                                                         ('Sala Mullin 1', 'Edificio Mullin', 12, 'Posgrado', TRUE),
                                                                                         ('Sala Mullin 2', 'Edificio Mullin', 6, 'Libre', TRUE),
                                                                                         ('Sala San Ignacio A', 'Edificio San Ignacio', 15, 'Docente', TRUE),
                                                                                         ('Sala San Ignacio B', 'Edificio San Ignacio', 10, 'Libre', TRUE),
                                                                                         ('Sala Athanasius 1A', 'Edificio Athanasius', 14, 'Posgrado', FALSE),
                                                                                         ('Sala Athanasius 2B', 'Edificio Athanasius', 8, 'Libre', TRUE),
                                                                                         ('Sala Madre Marta 1', 'Edificio Madre Marta', 12, 'Docente', TRUE),
                                                                                         ('Sala Madre Marta 2', 'Edificio Madre Marta', 6, 'Libre', TRUE),
                                                                                         ('Sala X1', 'Casa Xalambrí', 10, 'Libre', FALSE),
                                                                                         ('Sala SJ 1', 'Edificio San José', 18, 'Posgrado', TRUE),
                                                                                         ('Sala SJ 2', 'Edificio San José', 8, 'Docente', TRUE),
                                                                                         ('Sala Sal1', 'Campus Salto', 20, 'Libre', TRUE),
                                                                                         ('Sala Sal2', 'Campus Salto', 10, 'Posgrado', TRUE),
                                                                                         ('Sala C1', 'Edificio Candelaria', 14, 'Docente', TRUE),
                                                                                         ('Sala SF1', 'San Fernando', 12, 'Libre', TRUE),
                                                                                         ('Sala SF2', 'San Fernando', 20, 'Posgrado', FALSE);

INSERT INTO turno (hora_inicio, hora_fin) VALUES
                                              ('08:00:00', '09:00:00'),
                                              ('09:00:00', '10:00:00'),
                                              ('10:00:00', '11:00:00'),
                                              ('11:00:00', '12:00:00'),
                                              ('12:00:00', '13:00:00'),
                                              ('13:00:00', '14:00:00'),
                                              ('14:00:00', '15:00:00'),
                                              ('15:00:00', '16:00:00'),
                                              ('16:00:00', '17:00:00'),
                                              ('17:00:00', '18:00:00'),
                                              ('18:00:00', '19:00:00'),
                                              ('19:00:00', '20:00:00'),
                                              ('20:00:00', '21:00:00'),
                                              ('21:00:00', '22:00:00'),
                                              ('22:00:00', '23:00:00');

