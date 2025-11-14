from flask import Blueprint, jsonify, request
from db import get_connection
from validation import verificar_token, requiere_rol
from validators import validate_turno_rango

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

@turno_bp.route("", methods=["POST"])
@verificar_token
@requiere_rol('Administrador')
def crear_turno():
    data = request.get_json() or {}
    hora_inicio = data.get("hora_inicio")
    hora_fin = data.get("hora_fin")

    conn = None
    cur = None
    try:
        if not hora_inicio or not hora_fin:
            raise ValueError("Faltan campos: hora_inicio, hora_fin.")
        validate_turno_rango(hora_inicio, hora_fin)

        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO turno (hora_inicio, hora_fin) VALUES (%s, %s)",
            (hora_inicio, hora_fin),
        )
        conn.commit()
        return jsonify({"id_turno": cur.lastrowid}), 201

    except ValueError as ve:
        if conn: conn.rollback()
        return jsonify({"error": str(ve)}), 400
    except Exception:
        if conn: conn.rollback()
        return jsonify({"error": "Error interno"}), 500
    finally:
        try:
            if cur: cur.close()
        finally:
            if conn: conn.close()