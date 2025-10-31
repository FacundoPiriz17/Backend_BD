-- === USUARIOS ===
INSERT INTO usuario (ci, nombre, apellido, email, rol) VALUES
                                                           (55574121, 'Facundo', 'Piriz', 'facundo.piriz@correo.ucu.edu.uy', 'Participante'),
                                                           (56901393, 'Diego', 'De Oliveira', 'diego.deoliveira@correo.ucu.edu.uy', 'Participante'),
                                                           (55992757, 'Agustin', 'Garcia', 'agustin.garcia@correo.ucu.edu.uy', 'Participante'),
                                                           (58392015, 'Lucio', 'Martinez', 'lucio.martinez@correo.ucu.edu.uy', 'Administrador'),
                                                           (59283714, 'Maria', 'Gonzalez', 'maria.gonzalez@correo.ucu.edu.uy', 'Participante'),
                                                           (60123848, 'Sofia', 'Rodriguez', 'sofia.rodriguez@correo.ucu.edu.uy', 'Administrador'),
                                                           (60765436, 'Andres', 'Perez', 'andres.perez@correo.ucu.edu.uy', 'Funcionario'),
                                                           (61234569, 'Valentina', 'Suarez', 'valentina.suarez@correo.ucu.edu.uy', 'Administrador'),
                                                           (61890234, 'Camila', 'Fernandez', 'camila.fernandez@correo.ucu.edu.uy', 'Administrador'),
                                                           (62543214, 'Joaquin', 'Morales', 'joaquin.morales@correo.ucu.edu.uy', 'Participante');

-- === LOGIN ===
INSERT INTO login (email, contrasena) VALUES
                                          ('facundo.piriz@correo.ucu.edu.uy', '1234'),
                                          ('diego.deoliveira@correo.ucu.edu.uy', '1234'),
                                          ('agustin.garcia@correo.ucu.edu.uy', '1234'),
                                          ('lucio.martinez@correo.ucu.edu.uy', '1234'),
                                          ('maria.gonzalez@correo.ucu.edu.uy', '1234'),
                                          ('sofia.rodriguez@correo.ucu.edu.uy', '1234'),
                                          ('andres.perez@correo.ucu.edu.uy', '1234'),
                                          ('valentina.suarez@correo.ucu.edu.uy', '1234'),
                                          ('camila.fernandez@correo.ucu.edu.uy', '1234'),
                                          ('joaquin.morales@correo.ucu.edu.uy', '1234');

-- === FACULTADES ===
INSERT INTO facultad (nombre_facultad) VALUES
                                           ('Ingenieria'),
                                           ('Arquitectura'),
                                           ('Ciencias'),
                                           ('Medicina'),
                                           ('Derecho');

-- === PLANES ACADÉMICOS ===
INSERT INTO planAcademico (nombre_plan, id_Facultad, tipo) VALUES
                                                               ('Plan Ing 2025', 1, 'Grado'),
                                                               ('Plan Ing Posg', 1, 'Posgrado'),
                                                               ('Plan Arq 2024', 2, 'Grado'),
                                                               ('Plan Bio 2023', 3, 'Grado'),
                                                               ('Plan Bio Posg', 3, 'Posgrado'),
                                                               ('Plan Med 2022', 4, 'Posgrado'),
                                                               ('Plan Der 2025', 5, 'Grado'),
                                                               ('Plan Der Posg', 5, 'Posgrado'),
                                                               ('Plan Cs 2025', 3, 'Grado'),
                                                               ('Plan Cs 2026', 3, 'Grado');

-- === PARTICIPANTES EN PLANES ===
INSERT INTO participanteProgramaAcademico (ci_participante, nombre_plan, rol) VALUES
                                                                                  (55574121, 'Plan Ing 2025', 'Alumno'),
                                                                                  (56901393, 'Plan Arq 2024', 'Alumno'),
                                                                                  (55992757, 'Plan Bio 2023', 'Alumno'),
                                                                                  (58392015, 'Plan Med 2022', 'Docente'),
                                                                                  (59283714, 'Plan Der 2025', 'Alumno'),
                                                                                  (60123848, 'Plan Ing Posg', 'Docente'),
                                                                                  (60765436, 'Plan Cs 2025', 'Alumno'),
                                                                                  (61234569, 'Plan Bio Posg', 'Docente'),
                                                                                  (61890234, 'Plan Der Posg', 'Alumno'),
                                                                                  (62543214, 'Plan Cs 2026', 'Alumno');

-- === EDIFICIOS ===
INSERT INTO edificio (nombre_edificio, direccion, campus) VALUES
                                                              ('Edificio Central', 'Av. Principal 123', 'Campus Norte'),
                                                              ('Edificio Sur', 'Calle Falsa 456', 'Campus Sur'),
                                                              ('Edificio Este', 'Av. Este 789', 'Campus Este'),
                                                              ('Edificio Oeste', 'Av. Oeste 101', 'Campus Oeste'),
                                                              ('Edificio Norte', 'Calle Norte 202', 'Campus Norte');

-- === SALAS ===
INSERT INTO salasDeEstudio (nombre_sala, edificio, capacidad, tipo_sala, disponible, puntaje) VALUES
                                                                                                  ('Sala 101', 'Edificio Central', 10, 'Libre', true, 4),
                                                                                                  ('Sala 102', 'Edificio Central', 13, 'Posgrado', true, 3),
                                                                                                  ('Sala 201', 'Edificio Sur', 11, 'Libre', true, 5),
                                                                                                  ('Sala 202', 'Edificio Sur', 8, 'Docente', true, 3),
                                                                                                  ('Sala A', 'Edificio Este', 7, 'Libre', true, 4),
                                                                                                  ('Sala B', 'Edificio Este', 7, 'Libre', true, 3),
                                                                                                  ('Sala C', 'Edificio Oeste', 10, 'Posgrado', true, 5),
                                                                                                  ('Sala D', 'Edificio Norte', 9, 'Libre', true, 3),
                                                                                                  ('Sala E', 'Edificio Norte', 8, 'Docente', true, 4),
                                                                                                  ('Sala F', 'Edificio Central', 14, 'Libre', true, 5);

-- === TURNOS ===
INSERT INTO turno (hora_inicio, hora_fin) VALUES
                                              ('08:00', '09:00'),
                                              ('10:00', '11:00'),
                                              ('12:00', '13:00'),
                                              ('14:00', '15:00'),
                                              ('16:00', '17:00'),
                                              ('17:00', '18:00');

-- === RESERVAS ===
INSERT INTO reserva (nombre_sala, edificio, fecha, id_turno, estado) VALUES
                                                                         ('Sala 101', 'Edificio Central', DATE_ADD(CURDATE(), INTERVAL 1 DAY), 1, 'Finalizada'),
                                                                         ('Sala 102', 'Edificio Central', DATE_ADD(CURDATE(), INTERVAL 2 DAY), 2, 'Sin asistencia'),
                                                                         ('Sala 201', 'Edificio Sur', DATE_ADD(CURDATE(), INTERVAL 3 DAY), 3, 'Finalizada'),
                                                                         ('Sala 202', 'Edificio Sur', DATE_ADD(CURDATE(), INTERVAL 4 DAY), 3, 'Activa'),
                                                                         ('Sala A', 'Edificio Este', DATE_ADD(CURDATE(), INTERVAL 5 DAY), 5, 'Activa'),
                                                                         ('Sala 101', 'Edificio Central', DATE_ADD(CURDATE(), INTERVAL 6 DAY), 1, 'Cancelada'),
                                                                         ('Sala 201', 'Edificio Sur', DATE_ADD(CURDATE(), INTERVAL 7 DAY), 2, 'Finalizada'),
                                                                         ('Sala B', 'Edificio Este', DATE_ADD(CURDATE(), INTERVAL 8 DAY), 4, 'Activa'),
                                                                         ('Sala C', 'Edificio Oeste', DATE_ADD(CURDATE(), INTERVAL 9 DAY), 6, 'Finalizada'),
                                                                         ('Sala 101', 'Edificio Central', DATE_ADD(CURDATE(), INTERVAL 10 DAY), 1, 'Sin asistencia');

-- === PARTICIPANTES EN RESERVAS ===
INSERT INTO reservaParticipante (ci_participante, id_reserva, asistencia, confirmacion) VALUES
                                                                                            (55574121, 1, 'Asiste', true),
                                                                                            (56901393, 2, 'Asiste', true),
                                                                                            (55992757, 3, 'No asiste', false),
                                                                                            (58392015, 4, 'Asiste', true),
                                                                                            (60123848, 5, 'Asiste', true),
                                                                                            (60765436, 6, 'No asiste', false),
                                                                                            (61234569, 7, 'Asiste', true),
                                                                                            (61890234, 8, 'Asiste', true),
                                                                                            (62543214, 9, 'Asiste', true),
                                                                                            (59283714, 10, 'Asiste', true),
                                                                                            (55574121, 10, 'Asiste', true),
                                                                                            (56901393, 1, 'Asiste', true),
                                                                                            (60123848, 3, 'No asiste', false);

-- === SANCIONES ===
INSERT INTO sancion_participante (ci_participante, motivo, fecha_inicio, fecha_fin) VALUES
                                                                                        (55574121, 'Uso indebido', CURDATE(), DATE_ADD(CURDATE(), INTERVAL 7 DAY)),
                                                                                        (56901393, 'Morosidad', CURDATE(), DATE_ADD(CURDATE(), INTERVAL 5 DAY)),
                                                                                        (55992757, 'Vandalismo', CURDATE(), DATE_ADD(CURDATE(), INTERVAL 10 DAY)),
                                                                                        (58392015, 'Inasistencia', CURDATE(), DATE_ADD(CURDATE(), INTERVAL 3 DAY)),
                                                                                        (60123848, 'Morosidad', CURDATE(), DATE_ADD(CURDATE(), INTERVAL 6 DAY)),
                                                                                        (60765436, 'Vandalismo', CURDATE(), DATE_ADD(CURDATE(), INTERVAL 4 DAY)),
                                                                                        (62543214, 'Morosidad', CURDATE(), DATE_ADD(CURDATE(), INTERVAL 7 DAY));

-- === RESEÑAS ===
INSERT INTO resena (id_reserva, ci_participante, puntaje_general, descripcion) VALUES
                                                                                   (1, 55574121, 4, 'Consulta sobre sanción'),
                                                                                   (2, 56901393, 3, 'Pregunta sobre estado de sanción'),
                                                                                   (3, 55992757, 5, 'Reporte de incidente'),
                                                                                   (4, 58392015, 4, 'Consulta asistencia'),
                                                                                   (5, 59283714, 5, 'Reclamo por sanción'),
                                                                                   (6, 60123848, 3, 'Revisión de sanción'),
                                                                                   (7, 60765436, 4, 'Apelación de falta');

SELECT nombre_sala, COUNT(*) AS cantidad_reservas
FROM reserva
GROUP BY nombre_sala
ORDER BY cantidad_reservas DESC
LIMIT 1;

SELECT t.id_turno, t.hora_inicio, t.hora_fin, COUNT(*) AS cant_turnos
FROM turno t
         JOIN reserva r ON t.id_turno = r.id_turno
GROUP BY t.id_turno, t.hora_inicio, t.hora_fin
ORDER BY cant_turnos DESC
LIMIT 1;

SELECT r.nombre_sala, r.edificio, AVG(sub.cant_participantes) AS promedio_participantes
FROM reserva r
         JOIN (
    SELECT id_reserva, COUNT(ci_participante) AS cant_participantes
    FROM reservaParticipante
    GROUP BY id_reserva
) sub ON r.id_reserva = sub.id_reserva
GROUP BY r.nombre_sala, r.edificio;

SELECT f.nombre_facultad, pa.nombre_plan, COUNT(r.id_reserva) as cantidad
FROM reservaParticipante rp
         JOIN participanteProgramaAcademico ppa ON ppa.ci_participante = rp.ci_participante
         JOIN planAcademico pa ON pa.nombre_plan = ppa.nombre_plan
         JOIN facultad f ON f.id_Facultad = pa.id_Facultad
         JOIN reserva r ON r.id_reserva = rp.id_reserva
GROUP BY f.nombre_facultad, pa.nombre_plan
ORDER BY cantidad DESC;

SELECT e.nombre_edificio, ROUND((SUM(sub.ocupacion) / SUM(sub.capacidad)) * 100, 2) AS porcentaje_ocupacion
FROM (
         SELECT
             r.id_reserva,
             s.capacidad,
             COUNT(rp.ci_participante) AS ocupacion,
             r.edificio
         FROM reserva r
                  JOIN salasDeEstudio s ON r.nombre_sala = s.nombre_sala AND r.edificio = s.edificio
                  LEFT JOIN reservaParticipante rp
                            ON r.id_reserva = rp.id_reserva AND rp.asistencia = 'Asiste'
         GROUP BY r.id_reserva, s.capacidad, r.edificio
     ) sub
         JOIN edificio e ON e.nombre_edificio = sub.edificio
GROUP BY e.nombre_edificio;

SELECT pa.tipo,
       COUNT(CASE WHEN ppa.rol = 'Alumno' THEN 1 END) AS cant_alumnos,
       COUNT(CASE WHEN ppa.rol = 'Docente' THEN 1 END) AS cant_docentes,
       COUNT(r.id_reserva) AS reservas,
       COUNT(CASE WHEN rp.asistencia = 'Asiste' THEN 1 END) AS asistencias
FROM usuario u
         JOIN reservaParticipante rp ON u.ci = rp.ci_participante
         JOIN reserva r ON r.id_reserva = rp.id_reserva
         JOIN participanteProgramaAcademico ppa ON ppa.ci_participante = u.ci
         JOIN planAcademico pa ON ppa.nombre_plan = pa.nombre_plan
GROUP BY pa.tipo;

SELECT pa.tipo,
       COUNT(CASE WHEN ppa.rol = 'Alumno' THEN 1 END) AS cant_alumnos,
       COUNT(CASE WHEN ppa.rol = 'Docente' THEN 1 END) AS cant_docentes,
       COUNT(s.id_sancion) AS sanciones_totales
FROM usuario u
         JOIN participanteProgramaAcademico ppa ON ppa.ci_participante = u.ci
         JOIN planAcademico pa ON ppa.nombre_plan = pa.nombre_plan
         JOIN sancion_participante s ON s.ci_participante = u.ci
GROUP BY pa.tipo;

SELECT ROUND(COUNT(CASE WHEN r.estado = 'Finalizada' THEN 1 ELSE 0 END)/COUNT(*)*100, 2) AS porcentaje_utilizadas,
       ROUND(COUNT(CASE WHEN r.estado IN ('Cancelada', 'Sin asistencia') THEN 1 ELSE 0 END)/COUNT(*)*100, 2) AS porcentaje_fallido
FROM reserva r;
