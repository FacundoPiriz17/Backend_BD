from flask import Blueprint, jsonify, request
from db import get_connection

reservas_bp = Blueprint('reservas', __name__, url_prefix='/reservas')

#Todas las reservas
@reservas_bp.route('/all', methods=['GET'])
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
def aniadirReserva():
    conection = get_connection()
    cursor = conection.cursor()
    data = request.get_json()
    nombre_sala = data.get("nombre_sala")
    edificio = data.get("edificio")
    fecha = data.get("fecha")
    id_turno = data.get("id_turno")
    ci_usuario_principal = data.get("ci_usuario_principal")
    estado = data.get("estado")

    try:
        cursor.execute("INSERT INTO reserva (nombre_sala,edificio,fecha, id_turno, ci_usuario_principal,estado ) VALUES (%s,%s,%s,%s,%s,%s)", (nombre_sala,edificio,fecha, id_turno, ci_usuario_principal, estado))            
        conection.commit()
        return jsonify({'mensaje': 'Reserva registrada correctamente'}), 201

    except Exception as e:
        conection.rollback()
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conection.close()

#Modificar una reserva 
@reservas_bp.route('/modificar/<int:id>', methods=['PUT'])
def modificarReserva(id):
    conection = get_connection()
    cursor = conection.cursor()
    data = request.get_json()
    nombre_sala = data.get("nombre_sala")
    edificio = data.get("edificio")
    fecha = data.get("fecha")
    id_turno = data.get("id_turno")
    ci_usuario_principal = data.get("ci_usuario_principal")
    estado = data.get("estado")

    try:
        cursor.execute("UPDATE reserva SET nombre_sala = %s, edificio = %s, fecha = %s, id_turno = %s, ci_usuario_principal = %s, estado = %s WHERE id_reserva = %s", (nombre_sala,edificio,fecha, id_turno, ci_usuario_principal, estado, id))
        conection.commit()
        return jsonify({'mensaje': 'Reserva registrada correctamente'}), 201

    except Exception as e:
        conection.rollback()
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conection.close()

#Cancela una reserva 
@reservas_bp.route('/cancelar/<int:id>', methods=['PATCH'])
def cancelarReserva(id):
    conection = get_connection()
    cursor = conection.cursor()
    data = request.get_json()
    estado = data.get("estado")

    try:
        cursor.execute("UPDATE reserva SET estado = 'Cancelada' WHERE id_reserva = %s", ( estado, id))
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

