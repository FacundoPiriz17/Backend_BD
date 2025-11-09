from flask import Blueprint, jsonify, request
from db import get_connection
from validators import (
    validar_disponibilidad_sala,
    validar_tipo_sala,
    validar_limites_reserva,
    validar_anticipacion_reserva,
    validar_cancelacion_reserva,
    validar_sanciones_activas,
)
from datetime import datetime
from validation import verificar_token, requiere_rol
reservas_bp = Blueprint('reservas', __name__, url_prefix='/reservas')

#Todas las reservas
@reservas_bp.route('/all', methods=['GET'])
@verificar_token
@requiere_rol('Participante')
def reservas():
    conection = get_connection()
    cursor = conection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM reserva")
        resultados = cursor.fetchall()  # Obtiene TODAS las filas del resultado
        return jsonify(resultados)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conection.close()

#Obtener una reserva específica
@reservas_bp.route('/<int:id>', methods=['GET'])
@verificar_token
@requiere_rol('Participante')
def reservaEspecifica(id):
    conection = get_connection()
    cursor = conection.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM reserva WHERE id_reserva = %s", (id,) )
        reserva = cursor.fetchone()
        if reserva:
            return jsonify(reserva)
        else:
            return jsonify({'mensaje': 'Reserva no encontrada'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conection.close()

#Añadir una reserva
@reservas_bp.route('/registrar', methods=['POST'])
@verificar_token
@requiere_rol('Participante', 'Administrador','Funcionario')
def aniadirReserva():
    conection = get_connection()
    cursor = conection.cursor()
    data = request.get_json()

    nombre_sala = data.get("nombre_sala")
    edificio = data.get("edificio")
    fecha = data.get("fecha")
    id_turno = data.get("id_turno")
    ci = data.get("ci")
    estado = data.get("estado")
    participantes_ci = data.get("participantes_ci", [])

    if not all([nombre_sala, edificio, fecha, id_turno, ci]):
        return jsonify({'error': 'Faltan datos requeridos'}), 400

    ok, msg = validar_disponibilidad_sala(nombre_sala, edificio)
    if not ok:
        return jsonify({'error': msg}), 400

    ok, msg = validar_sanciones_activas(ci)
    if not ok:
        return jsonify({'error': msg}), 400

    ok, msg = validar_tipo_sala(edificio, nombre_sala, ci, participantes_ci)
    if not ok:
        return jsonify({'error': msg}), 400

    ok, msg = validar_limites_reserva(ci, fecha)
    if not ok:
        return jsonify({'error': msg}), 400

    ok, msg = validar_anticipacion_reserva(id_turno, fecha)
    if not ok:
        return jsonify({'error': msg}), 400

    try:
        cursor.execute("""
                       INSERT INTO reserva (nombre_sala, edificio, fecha, id_turno, estado)
                       VALUES (%s, %s, %s, %s, %s)
                       """, (nombre_sala, edificio, fecha, id_turno, estado))
        conection.commit()

        id_reserva = cursor.lastrowid

        cursor.execute("""
                       INSERT INTO reservaParticipante (ci_participante, id_reserva, asistencia, confirmacion)
                       VALUES (%s, %s, %s, %s)
                       """, (ci, id_reserva, 'Asiste', True))
        conection.commit()

        return jsonify({
            'mensaje': 'Reserva registrada correctamente',
            'id_reserva': id_reserva
        }), 201
    except Exception as e:
        conection.rollback()
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conection.close()

@reservas_bp.route('/invitar', methods=['POST'])
@verificar_token
@requiere_rol('Participante')
def invitarParticipante():
    conection = get_connection()
    cursor = conection.cursor(dictionary=True)
    data = request.get_json()

    email_invitado = data.get("email_invitado")
    id_reserva = data.get("id_reserva")
    asistencia = data.get("asistencia", "Asiste")

    if not all([email_invitado, id_reserva]):
        return jsonify({'error': 'Faltan datos requeridos'}), 400

    try:

        cursor.execute("SELECT ci FROM usuario WHERE email = %s", (email_invitado,))
        invitado = cursor.fetchone()
        if not invitado:
            return jsonify({'error': 'No existe un usuario con ese email'}), 404

        ci_invitado = invitado["ci"]

        cursor.execute("""
            INSERT INTO reservaParticipante (ci_participante, id_reserva, asistencia, confirmacion)
            VALUES (%s, %s, %s, %s)
        """, (ci_invitado, id_reserva, asistencia, False))
        conection.commit()

        return jsonify({'mensaje': 'Invitado agregado correctamente a la reserva'}), 201

    except Exception as e:
        conection.rollback()
        if "Duplicate entry" in str(e):
            return jsonify({'error': 'El usuario ya está invitado a esta reserva'}), 400
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conection.close()
        
#Confirmar/cancela un invitado
@reservas_bp.route('/confirmacion/<int:id>', methods=['PATCH'])
@verificar_token
@requiere_rol('Participante')
def confirmarInvitado(id):
    conection = get_connection()
    cursor = conection.cursor()


    try:
        cursor.execute("UPDATE reservaParticipante SET confirmacion = NOT confirmacion WHERE id_reserva = %s", (id))
        conection.commit()
        return jsonify({'mensaje': 'Respuesta confirmada correctamente'}), 201

    except Exception as e:
        conection.rollback()
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conection.close()


#Sala reseñada 
@reservas_bp.route('/resena/<int:id>', methods=['PATCH'])
@verificar_token
@requiere_rol('Participante')
def actualizarResenia(id):
    conection = get_connection()
    cursor = conection.cursor()


    try:
        cursor.execute("UPDATE reservaParticipante SET resenado = NOT resenado WHERE id_reserva = %s", (id))
        conection.commit()
        return jsonify({'mensaje': 'Respuesta confirmada correctamente'}), 201

    except Exception as e:
        conection.rollback()
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conection.close()




#Modificar una reserva 
@reservas_bp.route('/modificar/<int:id>', methods=['PUT'])
@verificar_token
@requiere_rol('Funcionario','Administrador')
def modificarReserva(id):
    conection = get_connection()
    cursor = conection.cursor()
    data = request.get_json()
    nombre_sala = data.get("nombre_sala")
    edificio = data.get("edificio")
    fecha = data.get("fecha")
    id_turno = data.get("id_turno")
    estado = data.get("estado")

    try:
        cursor.execute("""
                       UPDATE reserva
                       SET nombre_sala = %s,
                           edificio    = %s,
                           fecha       = %s,
                           id_turno    = %s,
                           estado      = %s
                       WHERE id_reserva = %s
                       """, (nombre_sala, edificio, fecha, id_turno, estado, id))
        conection.commit()

        return jsonify({'mensaje': 'Reserva modificada correctamente'}), 200
    except Exception as e:

        conection.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conection.close()

#Cancela una reserva 
@reservas_bp.route('/cancelar/<int:id>', methods=['PATCH'])
@verificar_token
def cancelarReserva(id):
    conection = get_connection()
    cursor = conection.cursor()

    ok, msg = validar_cancelacion_reserva(id)
    if not ok:
        return jsonify({'error': msg}), 400

    try:
        cursor.execute("UPDATE reserva SET estado = 'Cancelada' WHERE id_reserva = %s", (id))
        conection.commit()
        return jsonify({'mensaje': 'Reserva cancelada correctamente'}), 201

    except Exception as e:
        conection.rollback()
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conection.close()

#Eliminar una reserva
@reservas_bp.route('/eliminar/<int:id>', methods=['DELETE'])
@verificar_token
@requiere_rol('Funcionario', 'Administrador')
def eliminarReserva(id):
    conection = get_connection()
    cursor = conection.cursor()

    try:
        cursor.execute("DELETE FROM reserva WHERE id_reserva = %s", (id,) )
        conection.commit()
        return jsonify({'mensaje':'Reserva eliminada correctamente'}), 204

    except Exception as e:
        conection.rollback()
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conection.close()

