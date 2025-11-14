DROP DATABASE IF EXISTS Obligatorio;
CREATE DATABASE Obligatorio;
USE Obligatorio;

CREATE TABLE usuario (
                         ci INT PRIMARY KEY,
                         nombre VARCHAR(32) NOT NULL CHECK (CHAR_LENGTH(nombre) >= 3),
                         apellido VARCHAR(32) NOT NULL CHECK (CHAR_LENGTH(apellido) >= 3),
                         email VARCHAR(50) UNIQUE CHECK (LOWER(email) LIKE '%@correo.ucu.edu.uy' OR LOWER(email) LIKE '%ucu.edu.uy'),
                         rol ENUM('Participante', 'Funcionario', 'Administrador') NOT NULL DEFAULT 'Participante'
);

CREATE TABLE login(
                      email VARCHAR(50) PRIMARY KEY CHECK (LOWER(email) LIKE '%@correo.ucu.edu.uy' OR LOWER(email) LIKE '%ucu.edu.uy'),
                      contrasena VARCHAR(255) NOT NULL,
                      FOREIGN KEY (email) REFERENCES usuario(email)
);

CREATE TABLE facultad (
                          id_Facultad INT AUTO_INCREMENT PRIMARY KEY,
                          nombre_facultad VARCHAR(64) CHECK (CHAR_LENGTH(nombre_facultad) >= 3)
);

CREATE TABLE planAcademico (
                               nombre_plan VARCHAR(80) PRIMARY KEY,
                               id_Facultad INT NOT NULL,
                               tipo ENUM('Grado', 'Posgrado') NOT NULL,
                               FOREIGN KEY (id_Facultad) REFERENCES facultad(id_Facultad)
);

CREATE TABLE participanteProgramaAcademico (
                                               idAlumnoPrograma INT PRIMARY KEY AUTO_INCREMENT,
                                               ci_participante INT CHECK (CHAR_LENGTH(ci_participante) = 8 ),
                                               nombre_plan VARCHAR(80) NOT NULL,
                                               rol ENUM('Alumno', 'Docente') NOT NULL,
                                               FOREIGN KEY (ci_participante) REFERENCES usuario(ci),
                                               FOREIGN KEY (nombre_plan) REFERENCES planAcademico(nombre_plan)
);

CREATE TABLE edificio (
                          nombre_edificio VARCHAR(64) PRIMARY KEY,
                          direccion VARCHAR(64) NOT NULL,
                          campus VARCHAR(64) NOT NULL CHECK (CHAR_LENGTH(campus) >= 5 )
);

CREATE TABLE salasDeEstudio (
                                nombre_sala VARCHAR(32),
                                edificio VARCHAR(64),
                                capacidad INT NOT NULL CHECK (capacidad > 0),
                                tipo_sala ENUM('Libre', 'Posgrado', 'Docente') NOT NULL,
                                disponible BOOLEAN DEFAULT TRUE,
                                puntaje INT CHECK (puntaje BETWEEN 1 AND 5) DEFAULT 3,
                                PRIMARY KEY(nombre_sala, edificio),
                                FOREIGN KEY (edificio) REFERENCES edificio(nombre_edificio)
);

CREATE TABLE turno (
                       id_turno INT AUTO_INCREMENT PRIMARY KEY,
                       hora_inicio TIME NOT NULL,
                       hora_fin TIME NOT NULL,
                       CONSTRAINT horario_valido CHECK(hora_inicio < hora_fin)
);

CREATE TABLE reserva (
                         id_reserva INT AUTO_INCREMENT PRIMARY KEY,
                         nombre_sala VARCHAR(32) NOT NULL,
                         edificio VARCHAR(64) NOT NULL,
                         fecha DATE DEFAULT (CURDATE()),
                         id_turno INT NOT NULL,
                         ci_organizador INT NOT NULL CHECK (CHAR_LENGTH(ci_organizador) = 8),
                         estado ENUM('Activa', 'Cancelada', 'Sin asistencia', 'Finalizada') DEFAULT 'Activa',
                         FOREIGN KEY (nombre_sala, edificio) REFERENCES salasDeEstudio(nombre_sala, edificio),
                         FOREIGN KEY (edificio) REFERENCES edificio(nombre_edificio),
                         FOREIGN KEY (id_turno) REFERENCES turno(id_turno),
                         FOREIGN KEY (ci_organizador) REFERENCES usuario(ci)
);

CREATE TABLE reservaParticipante (
                                     ci_participante INT NOT NULL CHECK (CHAR_LENGTH(ci_participante) = 8),
                                     id_reserva INT NOT NULL,
                                     fecha_solicitud_reserva DATE DEFAULT (CURDATE()),
                                     asistencia ENUM('Asiste', 'No asiste') NOT NULL,
                                     confirmacion BOOLEAN DEFAULT FALSE,
                                     resenado BOOLEAN DEFAULT FALSE,
                                     PRIMARY KEY (ci_participante, id_reserva),
                                     FOREIGN KEY (ci_participante) REFERENCES usuario(ci),
                                     FOREIGN KEY (id_reserva) REFERENCES reserva(id_reserva)
);

CREATE TABLE sancion_participante (
                                      id_sancion INT AUTO_INCREMENT PRIMARY KEY,
                                      ci_participante INT NOT NULL CHECK (CHAR_LENGTH(ci_participante) = 8),
                                      motivo ENUM('Uso indebido', 'Morosidad', 'Vandalismo', 'Inasistencia') NOT NULL,
                                      fecha_inicio DATE NOT NULL,
                                      fecha_fin DATE NOT NULL,
                                      FOREIGN KEY (ci_participante) REFERENCES usuario(ci)
);

CREATE TABLE resena (
                        id_resena INT AUTO_INCREMENT PRIMARY KEY,
                        id_reserva INT NOT NULL,
                        ci_participante INT NOT NULL CHECK (CHAR_LENGTH(ci_participante) = 8),
                        fecha_publicacion DATETIME NOT NULL DEFAULT NOW(),
                        puntaje_general INT NOT NULL CHECK (puntaje_general BETWEEN 1 AND 5),
                        descripcion VARCHAR(255) DEFAULT NULL,
                        FOREIGN KEY (ci_participante) REFERENCES usuario(ci),
                        FOREIGN KEY (id_reserva) REFERENCES reserva(id_reserva)
);

INSERT INTO usuario (ci, nombre, apellido, email, rol)
VALUES(55574121, 'Facundo', 'Piriz','facundo.piriz@correo.ucu.edu.uy','Administrador'),
      (56901393, 'Diego', 'De Olivera','diego.deoliveira@correo.ucu.edu.uy','Funcionario'),
      (55992757, 'Agustín', 'García','agustin.garciab@correo.ucu.edu.uy','Participante'),
      (10000008, 'Thiago','García','thiago.garcia@correo.ucu.edu.uy','Participante'),
      (10000014, 'Santiago','Aguerre','santiago.aguerre@correo.ucu.edu.uy','Participante'),
      (10000020, 'Agostina','Etchebarren','agostina.etchebarren@correo.ucu.edu.uy','Participante'),
      (10000036, 'Constanza','Blanco','constanza.blanco@correo.ucu.edu.uy','Funcionario'),
      (10000042, 'Manuel','Cabrera','manuel.cabrera@correo.ucu.edu.uy','Funcionario'),
      (10000058, 'Martin','Mujica','martin.mujica@correo.ucu.edu.uy','Administrador'),
      (10000064, 'Santiago','Blanco','santiago.blanco@correo.ucu.edu.uy','Administrador'),
      (10000070, 'Felipe','Paladino','felipe.paladino@correo.ucu.edu.uy','Administrador');

INSERT INTO login (email, contrasena) VALUES
                                          ('facundo.piriz@correo.ucu.edu.uy', '$2b$12$c2kgM37h6ri1RGeroGPsMOZoZJwXLMyKYhLkhtmMWJRkKQXdh1ey2'),
                                          ('diego.deoliveira@correo.ucu.edu.uy','$2b$12$c2kgM37h6ri1RGeroGPsMOZoZJwXLMyKYhLkhtmMWJRkKQXdh1ey2'),
                                          ('thiago.garcia@correo.ucu.edu.uy','$2b$12$c2kgM37h6ri1RGeroGPsMOZoZJwXLMyKYhLkhtmMWJRkKQXdh1ey2'),
                                          ('santiago.aguerre@correo.ucu.edu.uy','$2b$12$c2kgM37h6ri1RGeroGPsMOZoZJwXLMyKYhLkhtmMWJRkKQXdh1ey2'),
                                          ('agostina.etchebarren@correo.ucu.edu.uy','$2b$12$c2kgM37h6ri1RGeroGPsMOZoZJwXLMyKYhLkhtmMWJRkKQXdh1ey2'),
                                          ('constanza.blanco@correo.ucu.edu.uy','$2b$12$c2kgM37h6ri1RGeroGPsMOZoZJwXLMyKYhLkhtmMWJRkKQXdh1ey2'),
                                          ('manuel.cabrera@correo.ucu.edu.uy','$2b$12$c2kgM37h6ri1RGeroGPsMOZoZJwXLMyKYhLkhtmMWJRkKQXdh1ey2'),
                                          ('martin.mujica@correo.ucu.edu.uy','$2b$12$c2kgM37h6ri1RGeroGPsMOZoZJwXLMyKYhLkhtmMWJRkKQXdh1ey2'),
                                          ('santiago.blanco@correo.ucu.edu.uy','$2b$12$c2kgM37h6ri1RGeroGPsMOZoZJwXLMyKYhLkhtmMWJRkKQXdh1ey2'),
                                          ('felipe.paladino@correo.ucu.edu.uy','$2b$12$c2kgM37h6ri1RGeroGPsMOZoZJwXLMyKYhLkhtmMWJRkKQXdh1ey2'),
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
                                                               ('Dirección Avanzada de Empresas 2010', 3, 'Posgrado'),
                                                               ('Ingeniería en Electrónica 2022',1, 'Grado'),
                                                               ('Maestría en Dirección de Empresas 2022',3, 'Posgrado'),
                                                               ('Psicología Organizacional 2022',4, 'Posgrado');

INSERT INTO participanteProgramaAcademico (ci_participante, nombre_plan, rol) VALUES
                                                                                  (55992757, 'Ingeniería en Informática 2021', 'Docente'),
                                                                                  (10000020, 'Ingeniería en Informática 2021',         'Alumno'),
                                                                                  (10000014, 'Ingeniería en Informática 2021',         'Alumno'),
                                                                                  (10000008, 'Maestría en Informática 2021',           'Docente');


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

INSERT INTO reserva (nombre_sala, edificio, id_turno, ci_organizador) VALUES
                                                                          ('Sala 1',      'Edificio Sacré Coeur', 1, 55992757),
                                                                          ('Sala 2',      'Edificio Sacré Coeur', 2, 10000020),
                                                                          ('Sala S1',     'Edificio Semprún',     3, 10000014),
                                                                          ('Sala Mullin 1','Edificio Mullin',     4, 55992757),
                                                                          ('Sala SJ 1',   'Edificio San José',    5, 10000008),
                                                                          ('Sala Sal1',   'Campus Salto',         6, 10000014),
                                                                          ('Sala C1',     'Edificio Candelaria',  7, 10000020),
                                                                          ('Sala SF1',    'San Fernando',         8, 55992757);

INSERT INTO reservaParticipante (ci_participante, id_reserva, asistencia, confirmacion, resenado) VALUES

(55992757, 1, 'Asiste',     TRUE,  TRUE),
(10000008, 1, 'Asiste',     TRUE,  FALSE),
(10000014, 1, 'No asiste',  FALSE, FALSE),

(10000020, 2, 'Asiste',     TRUE,  FALSE),
(10000036, 2, 'Asiste',     TRUE,  FALSE),

(10000014, 3, 'Asiste',     TRUE,  TRUE),
(55992757, 3, 'No asiste',  FALSE, FALSE),

(55992757, 4, 'Asiste',     TRUE,  TRUE),
(10000058, 4, 'Asiste',     TRUE,  FALSE),
(10000064, 4, 'No asiste',  FALSE, FALSE),

(10000008, 5, 'Asiste',     TRUE,  FALSE),
(10000070, 5, 'Asiste',     TRUE,  FALSE),

(10000008, 6, 'Asiste',     TRUE,  TRUE),
(10000014, 6, 'Asiste',     TRUE,  FALSE),
(10000020, 6, 'No asiste',  FALSE, FALSE),

(10000020, 7, 'No asiste',  TRUE,  FALSE),
(10000042, 7, 'Asiste',     TRUE,  FALSE),

(55992757, 8, 'Asiste',     TRUE,  FALSE),
(55574121, 8, 'Asiste',     TRUE,  FALSE),
(56901393, 8, 'No asiste',  FALSE, FALSE);

INSERT INTO sancion_participante (ci_participante, motivo, fecha_inicio, fecha_fin) VALUES
                                                                                        (10000014, 'Inasistencia', '2025-01-01', '2025-03-01'),
                                                                                        (55992757, 'Inasistencia', '2025-02-15', '2025-04-15'),
                                                                                        (10000020, 'Uso indebido', '2025-05-10', '2025-07-10');

INSERT INTO resena (id_reserva, ci_participante, puntaje_general, descripcion) VALUES
                                                                                   (1, 55992757, 5, 'Sala amplia y silenciosa. Ideal para trabajar en grupo.'),
                                                                                   (3, 10000014, 3, 'Había algo de ruido en el pasillo.'),
                                                                                   (4, 55992757, 5, 'Muy buena iluminación y sillas cómodas.'),
                                                                                   (6, 10000008, 4, 'Sala cómoda, pero la conexión Wi-Fi podría ser mejor.');