from datetime import datetime, timedelta
from db import get_connection

def validar_ci(ci):
    ci = str(ci)
    if not ci or not ci.isdigit() or len(ci) != 8:
        return False
    factores = [2, 9, 8, 7, 6, 3, 4]
    suma = sum(int(ci[i]) * factores[i] for i in range(7))
    verificador = (10 - suma % 10) % 10

    return verificador == int(ci[7])

def validar_email_ucu(email):
    email = str(email)
    if not email:
        return False
    email = email.lower()
    return email.endswith("@correo.ucu.edu.uy") or email.endswith("@ucu.edu.uy")

def validar_capacidad(edificio, nombre_sala, cantidad_participantes):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT capacidad FROM salasDeEstudio WHERE nombre_sala=%s AND edificio=%s",
        (nombre_sala, edificio),
    )
    sala = cursor.fetchone()
    cursor.close()
    conn.close()
    if not sala:
        return False, "La sala especificada no existe."
    if cantidad_participantes > sala["capacidad"]:
        return False, f"La sala tiene capacidad máxima de {sala['capacidad']} participantes."
    return True, "Capacidad válida."

def validar_tipo_sala(edificio, nombre_sala, ci_principal, participantes_ci):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        "SELECT tipo_sala FROM salasDeEstudio WHERE nombre_sala=%s AND edificio=%s",
        (nombre_sala, edificio),
    )
    sala = cursor.fetchone()
    if not sala:
        cursor.close()
        conn.close()
        return False, "La sala especificada no existe."

    tipo_sala = sala["tipo_sala"]

    if tipo_sala == "Libre":
        cursor.close()
        conn.close()
        return True, "Sala libre, reserva permitida."

    cursor.execute(
        """
        SELECT pa.tipo, ppa.rol
        FROM participanteProgramaAcademico ppa
        JOIN planAcademico pa ON pa.nombre_plan = ppa.nombre_plan
        WHERE ppa.ci_participante = %s
        """,
        (ci_principal,),
    )
    principal = cursor.fetchone()
    if not principal:
        cursor.close()
        conn.close()
        return False, "El usuario principal no está asociado a ningún plan académico."

    tipo_principal = principal["tipo"]
    rol_principal = principal["rol"]

    if tipo_sala == "Posgrado" and not (tipo_principal == "Posgrado" or rol_principal == "Docente"):
        cursor.close()
        conn.close()
        return False, "Solo docentes o alumnos de posgrado pueden reservar esta sala."

    if tipo_sala == "Docente" and rol_principal != "Docente":
        cursor.close()
        conn.close()
        return False, "Solo docentes pueden reservar esta sala."

    for ci in participantes_ci:
        cursor.execute(
            """
            SELECT pa.tipo, ppa.rol
            FROM participanteProgramaAcademico ppa
            JOIN planAcademico pa ON pa.nombre_plan = ppa.nombre_plan
            WHERE ppa.ci_participante = %s
            """,
            (ci,),
        )

        participante = cursor.fetchone()
        if not participante:
            continue

        tipo_p = participante["tipo"]
        rol_p = participante["rol"]

        if tipo_sala == "Posgrado" and not (tipo_p == "Posgrado" or rol_p == "Docente"):
            cursor.close()
            conn.close()
            return False, f"El participante {ci} no puede usar una sala exclusiva de posgrado."
        if tipo_sala == "Docente" and rol_p != "Docente":
            cursor.close()
            conn.close()
            return False, f"El participante {ci} no puede usar una sala exclusiva de docentes."

    cursor.close()
    conn.close()
    return True, "Tipo de sala válido."


def validar_limites_reserva(ci_usuario_principal, fecha_str):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT pa.tipo, ppa.rol
        FROM participanteProgramaAcademico ppa
        JOIN planAcademico pa ON ppa.nombre_plan = pa.nombre_plan
        WHERE ppa.ci_participante = %s
        """,
        (ci_usuario_principal,),
    )
    datos = cursor.fetchone()
    if not datos:
        cursor.close()
        conn.close()
        return False, "El usuario principal no está asociado a ningún plan académico."

    tipo = datos["tipo"]
    rol = datos["rol"]

    if tipo == "Posgrado" or rol == "Docente":
        cursor.close()
        conn.close()
        return True, "Sin restricciones por tipo de usuario."

    fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
    lunes = fecha - timedelta(days=fecha.weekday())
    domingo = lunes + timedelta(days=6)

    cursor.execute(
        """
        SELECT COUNT(*) AS cant
        FROM reserva
        WHERE ci_usuario_principal = %s
          AND fecha BETWEEN %s AND %s
          AND estado = 'Activa'
        """,
        (ci_usuario_principal, lunes, domingo),
    )
    cant_semana = cursor.fetchone()["cant"]

    cursor.execute(
        """
        SELECT COUNT(*) AS cant
        FROM reserva r
        JOIN turno t ON r.id_turno = t.id_turno
        WHERE r.ci_usuario_principal = %s
          AND r.fecha = %s
          AND r.estado = 'Activa'
        """,
        (ci_usuario_principal, fecha),
    )
    cant_dia = cursor.fetchone()["cant"]

    cursor.close()
    conn.close()

    if cant_semana >= 3:
        return False, "El usuario ya tiene 3 reservas activas en la misma semana."
    if cant_dia >= 2:
        return False, "El usuario ya tiene 2 horas reservadas en el mismo día."
    return True, "Límites de reserva válidos."

def validar_anticipacion_reserva(id_turno, fecha_str):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT hora_inicio FROM turno WHERE id_turno = %s", (id_turno,))
    turno = cursor.fetchone()

    cursor.close()
    conn.close()

    if not turno:
        return False, "El turno especificado no existe."

    hora_turno = turno["hora_inicio"]
    fecha_turno = datetime.strptime(fecha_str, "%Y-%m-%d").date()
    fecha_hora_turno = datetime.combine(fecha_turno, hora_turno)

    ahora = datetime.now()

    # No puede reservar si falta menos de una hora
    if fecha_hora_turno - ahora < timedelta(hours=1):
        return False, "No se puede reservar con menos de una hora de anticipación."

    return True, "Reserva con anticipación válida."

def validar_cancelacion_reserva(id_reserva):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("""
        SELECT r.fecha, t.hora_inicio
        FROM reserva r
        JOIN turno t ON r.id_turno = t.id_turno
        WHERE r.id_reserva = %s
    """, (id_reserva,))
    reserva = cursor.fetchone()

    cursor.close()
    conn.close()

    if not reserva:
        return False, "La reserva especificada no existe."

    fecha_hora_reserva = datetime.combine(reserva["fecha"], reserva["hora_inicio"])
    ahora = datetime.now()

    if fecha_hora_reserva - ahora <= timedelta(hours=1):
        return False, "No se puede cancelar la reserva con menos de una hora de anticipación."

    return True, "Cancelación válida."

def validar_insercion_usuario(rol):
    rol = rol.capitalize().strip()
    if rol in ("Funcionario", "Administrador"):
        return False, "Usuario sin programa académico asociado (rol administrativo)."
    return True, "Usuario participante: se deben insertar datos académicos."

def validar_disponibilidad_sala(nombre_sala, edificio):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        """
        SELECT disponible 
        FROM salasDeEstudio 
        WHERE nombre_sala = %s AND edificio = %s
        """,
        (nombre_sala, edificio),
    )
    sala = cursor.fetchone()
    cursor.close()
    conn.close()

    if not sala:
        return False, "La sala especificada no existe."
    if not sala["disponible"]:
        return False, "La sala seleccionada no está disponible actualmente."

    return True, "Sala disponible para reservar."

def validar_resena_unica(id_reserva, ci_participante):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT resenado 
        FROM reservaParticipante 
        WHERE id_reserva = %s AND ci_participante = %s
        """,
        (id_reserva, ci_participante),
    )
    registro = cursor.fetchone()

    cursor.close()
    conn.close()

    if not registro:
        return False, "No existe registro de participación en la reserva."
    if registro["resenado"]:
        return False, "Ya se ha realizado una reseña para esta reserva."

    return True, "Reseña permitida."

def validar_sanciones_activas(ci_participante):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute(
        """
        SELECT COUNT(*) AS activas
        FROM sancion_participante
        WHERE ci_participante = %s
          AND CURDATE() BETWEEN fecha_inicio AND fecha_fin
        """,
        (ci_participante,),
    )
    resultado = cursor.fetchone()

    cursor.close()
    conn.close()

    if resultado["activas"] > 0:
        return False, "El usuario tiene sanciones activas y no puede realizar reservas."

    return True, "El usuario no tiene sanciones activas."