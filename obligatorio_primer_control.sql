DROP DATABASE IF EXISTS Obligatorio;
CREATE DATABASE Obligatorio;
USE Obligatorio;

DELIMITER //
CREATE FUNCTION validarCi(ci VARCHAR(20))
    RETURNS BOOLEAN
    DETERMINISTIC
BEGIN
    DECLARE numeros VARCHAR(20);
    DECLARE base VARCHAR(20);
    DECLARE verificador INT;
    DECLARE factores VARCHAR(14) DEFAULT '2987634';
    DECLARE suma INT DEFAULT 0;
    DECLARE i INT DEFAULT 1;
    DECLARE digito INT;
    DECLARE factor INT;
    DECLARE resto INT;
    DECLARE esperado INT;

    SET numeros = REPLACE(REPLACE(ci, '.', ''), '-', '');

    IF CHAR_LENGTH(numeros) <> 8 THEN
        RETURN FALSE;
    END IF;

    SET verificador = CAST(RIGHT(numeros, 1) AS UNSIGNED);
    SET base = LEFT(numeros, CHAR_LENGTH(numeros) - 1);

    WHILE i <= CHAR_LENGTH(base) DO
            SET digito = CAST(SUBSTRING(base, i, 1) AS UNSIGNED);
            SET factor = CAST(SUBSTRING(factores, i, 1) AS UNSIGNED);
            SET suma = suma + digito * factor;
            SET i = i + 1;
    END WHILE;

    SET resto = suma MOD 10;
    SET esperado = IF(resto = 0, 0, 10 - resto);
    RETURN esperado = verificador;
END//
DELIMITER ;

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

DELIMITER //
CREATE TRIGGER validar_ci_usuario
    BEFORE INSERT ON usuario
    FOR EACH ROW
BEGIN
    IF NOT validarCi(NEW.ci) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'La cédula tiene que ser válida.';
    END IF;
END;
//
DELIMITER ;

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

DELIMITER //
CREATE TRIGGER validar_ci_participanteProgramaAcademico
    BEFORE INSERT ON participanteProgramaAcademico
    FOR EACH ROW
BEGIN
    IF NOT validarCi(NEW.ci_participante) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'La cédula tiene que ser válida.';
    END IF;
END;
// DELIMITER ;

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
    disponible BOOLEAN default true,
    puntaje INT CHECK (puntaje BETWEEN 1 AND 5) default 3,
    PRIMARY KEY(nombre_sala, edificio),
    FOREIGN KEY (edificio) REFERENCES edificio(nombre_edificio)
);

CREATE TABLE turno (
    id_turno INT AUTO_INCREMENT PRIMARY KEY,
    hora_inicio TIME NOT NULL,
    hora_fin TIME NOT NULL,
    CONSTRAINT horario_valido CHECK(hora_inicio < hora_fin)
);

DELIMITER //
CREATE TRIGGER validar_turno
    BEFORE INSERT ON turno
    FOR EACH ROW
        BEGIN
            IF TIME(NEW.hora_inicio) < '08:00:00' OR TIME(NEW.hora_fin) > '23:00:00' THEN
                SIGNAL SQLSTATE '45000'
                SET MESSAGE_TEXT = 'El turno debe ser entre las 8 de la mañana y las 11 de la noche.';
            END IF;
        END;
// DELIMITER ;

CREATE TABLE reserva (
    id_reserva INT AUTO_INCREMENT PRIMARY KEY,
    nombre_sala VARCHAR(32) NOT NULL,
    edificio VARCHAR(64) NOT NULL,
    fecha DATE DEFAULT (CURDATE()),
    id_turno INT NOT NULL,
    estado ENUM('Activa', 'Cancelada', 'Sin asistencia', 'Finalizada') default 'Activa',
    FOREIGN KEY (nombre_sala, edificio) REFERENCES salasDeEstudio(nombre_sala, edificio),
    FOREIGN KEY (edificio) REFERENCES edificio(nombre_edificio),
    FOREIGN KEY (id_turno) REFERENCES turno(id_turno)
);

DELIMITER //
CREATE TRIGGER validar_fecha_reserva
    BEFORE INSERT ON reserva
    FOR EACH ROW
BEGIN
    IF NEW.fecha < CURDATE() THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'La reserva no puede hacerse en días anteriores al actual o en el día actual';
    END IF;
END;
// DELIMITER ;

CREATE TABLE reservaParticipante (
    ci_participante INT NOT NULL CHECK (CHAR_LENGTH(ci_participante) = 8),
    id_reserva INT NOT NULL,
    fecha_solicitud_reserva DATE DEFAULT (CURDATE()),
    asistencia ENUM('Asiste', 'No asiste') NOT NULL,
    confirmacion BOOLEAN default false,
    resenado BOOLEAN default false,
    PRIMARY KEY (ci_participante, id_reserva),
    FOREIGN KEY (ci_participante) REFERENCES usuario(ci),
    FOREIGN KEY (id_reserva) REFERENCES reserva(id_reserva)
);

DELIMITER //
CREATE TRIGGER validar_fecha_reservaParticipante
    BEFORE INSERT ON reservaParticipante
    FOR EACH ROW
BEGIN
    IF NEW.fecha_solicitud_reserva > CURDATE() THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'La fecha de solicitud no puede ser futura.';
    END IF;
END;
// DELIMITER ;

DELIMITER //
CREATE TRIGGER validar_ci_reservaParticipante
    BEFORE INSERT ON reservaParticipante
    FOR EACH ROW
BEGIN
    IF NOT validarCi(NEW.ci_participante) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'La cédula tiene que ser válida.';
    END IF;
END;
// DELIMITER ;

DELIMITER //
CREATE TRIGGER validar_anio_reservaParticipante
    BEFORE INSERT ON reservaParticipante
    FOR EACH ROW
BEGIN
    IF NEW.fecha_solicitud_reserva > CURDATE() THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'La fecha de solicitud no puede ser futura.';
    END IF;

END;
// DELIMITER ;

CREATE TABLE sancion_participante (
    id_sancion INT AUTO_INCREMENT PRIMARY KEY,
    ci_participante INT NOT NULL CHECK (CHAR_LENGTH(ci_participante) = 8),
    motivo ENUM('Uso indebido', 'Morosidad', 'Vandalismo', 'Inasistencia') NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE NOT NULL,
    FOREIGN KEY (ci_participante) REFERENCES usuario(ci)
);

DELIMITER //
CREATE TRIGGER validar_ci_sancion_participante
    BEFORE INSERT ON sancion_participante
    FOR EACH ROW
BEGIN
    IF NOT validarCi(NEW.ci_participante) THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'La cédula tiene que ser válida.';
    END IF;
END;//
DELIMITER ;

DELIMITER //
CREATE TRIGGER validar_fechas_sancion
    BEFORE INSERT ON sancion_participante
    FOR EACH ROW
BEGIN
    IF NEW.fecha_fin <= NEW.fecha_inicio THEN
        SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'La fecha de fin debe ser posterior a la de inicio.';
    END IF;
END;
// DELIMITER ;

CREATE TABLE resena (
    id_resena INT AUTO_INCREMENT PRIMARY KEY,
    id_reserva INT NOT NULL,
    ci_participante INT NOT NULL CHECK (CHAR_LENGTH(ci_participante) = 8),
    fecha_publicacion DATETIME NOT NULL DEFAULT NOW(),
    puntaje_general INT NOT NULL CHECK (puntaje_general BETWEEN 1 AND 5),
    descripcion VARCHAR(255) default null,
    FOREIGN KEY (ci_participante) REFERENCES usuario(ci),
    FOREIGN KEY (id_reserva) REFERENCES reserva(id_reserva)
);