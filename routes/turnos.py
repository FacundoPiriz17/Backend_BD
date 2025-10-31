from flask import Blueprint, jsonify, request
from db import get_connection
from validation import verificar_token

turno_bp = Blueprint('/turnos', __name__, url_prefix='/turnos')

#Todos los turnos
@turno_bp.route('/all', methods=['GET'])
@verificar_token
def turnos():
    conection = get_connection()
    cursor = conection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM turno")
        resultados = cursor.fetchall()  # Obtiene TODAS las filas del resultado
        return jsonify(resultados)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conection.close()

#Obtener un turno específica
@turno_bp.route('/turno/<int:id>', methods=['GET'])
@verificar_token
def turnoEspecifico(id):
    conection = get_connection()
    cursor = conection.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM turno WHERE id_turno = %s", (id,) )
        turno = cursor.fetchone()
        if turno:
            return jsonify(turno)
        else:
            return jsonify({'mensaje': 'Turno no encontrado'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conection.close()