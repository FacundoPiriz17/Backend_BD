from flask import Blueprint, jsonify, request
from db import get_connection
from validators import validar_resena_unica, validar_ci
from validation import verificar_token, requiere_rol
resenias_bp = Blueprint('resenas', __name__, url_prefix='/resenas')

#Todas las reseñas
@resenias_bp.route('/all', methods=['GET'])
@verificar_token
@requiere_rol('Funcionario','Administrador')
def resenias():
    conection = get_connection()
    cursor = conection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM resena")
        resultados = cursor.fetchall()  # Obtiene TODAS las filas del resultado
        return jsonify(resultados)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conection.close()

#Obtener una reseña específica
@resenias_bp.route('/resena/<int:id>', methods=['GET'])
@verificar_token
@requiere_rol('Administrador', 'Funcionario')
def reseniasEspecifica(id):
    conection = get_connection()
    cursor = conection.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM resena WHERE id_resena = %s", (id,) )
        resenia = cursor.fetchone()
        if resenia:
            return jsonify(resenia)
        else:
            return jsonify({'mensaje': 'Reseña no encontrada'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conection.close()

#Añadir una reseña
@resenias_bp.route('/registrar', methods=['POST'])
@verificar_token
@requiere_rol('Participante')
def aniadirResenia():
    conection = get_connection()
    cursor = conection.cursor()
    data = request.get_json()
    ci_participante = data.get("ci_participante")
    id_reserva = data.get("id_reserva")
    puntaje_general = data.get("puntaje_general")
    descripcion = data.get("descripcion")

    if not all([ci_participante, id_reserva, puntaje_general]):
        return jsonify({'error': 'Faltan datos requeridos'}), 400

    if not validar_ci(ci_participante):
        return jsonify({'error': 'Cédula inválida'}), 400

    try:
        punt = int(puntaje_general)
    except Exception:
        return jsonify({'error': 'Puntaje debe ser un número entre 1 y 5'}), 400

    if not (1 <= punt <= 5):
        return jsonify({'error': 'Puntaje debe ser entre 1 y 5'}), 400

    ok, msg = validar_resena_unica(id_reserva, ci_participante)
    if not ok:
        return jsonify({'error': msg}), 400

    try:
        cursor.execute("""
            INSERT INTO resena (id_reserva, ci_participante, puntaje_general, descripcion)
            VALUES (%s, %s, %s, %s)
        """, (id_reserva, ci_participante, punt, descripcion))

        cursor.execute("""
            UPDATE reservaParticipante
            SET resenado = TRUE
            WHERE id_reserva = %s AND ci_participante = %s
        """, (id_reserva, ci_participante))

        cursor.execute("""
            SELECT nombre_sala, edificio FROM reserva WHERE id_reserva = %s
        """, (id_reserva,))
        sala = cursor.fetchone()

        if sala:
            nombre_sala, edificio = sala

            cursor.execute("""
                SELECT AVG(r.puntaje_general)
                FROM resena r
                JOIN reserva re ON r.id_reserva = re.id_reserva
                WHERE re.nombre_sala = %s AND re.edificio = %s
            """, (nombre_sala, edificio))
            promedio = cursor.fetchone()[0]

            cursor.execute("""
                UPDATE salasDeEstudio
                SET puntaje = ROUND(%s,2)
                WHERE nombre_sala = %s AND edificio = %s
            """, (promedio, nombre_sala, edificio))

        conection.commit()
        return jsonify({'mensaje': 'Reseña registrada y puntaje actualizado correctamente'}), 201

    except Exception as e:
        conection.rollback()
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conection.close()


#Modificar una reseña 
@resenias_bp.route('/modificar/<int:id>', methods=['PUT'])
@verificar_token
@requiere_rol('Participante')
def modificarResenia(id):
    conection = get_connection()
    cursor = conection.cursor()
    data = request.get_json()
    ci_participante = data.get("ci_participante")
    id_reserva = data.get("id_reserva")
    puntaje_general = data.get("puntaje_general")
    descripcion = data.get("descripcion")

    if not all([ci_participante, id_reserva, puntaje_general]):
        return jsonify({'error': 'Faltan datos requeridos'}), 400

    if not validar_ci(ci_participante):
        return jsonify({'error': 'Cédula inválida'}), 400

    try:
        punt = int(puntaje_general)
    except Exception:
        return jsonify({'error': 'Puntaje debe ser un número entre 1 y 5'}), 400

    if not (1 <= punt <= 5):
        return jsonify({'error': 'Puntaje debe ser entre 1 y 5'}), 400

    try:
        cursor.execute("UPDATE resena SET ci_participante = %s, id_reserva = %s, puntaje_general = %s, descripcion = %s WHERE id_resena = %s", (ci_participante, id_reserva, puntaje_general, descripcion, id))
        conection.commit()
        return jsonify({'mensaje': 'Reseña modificada correctamente'}), 200

    except Exception as e:
        conection.rollback()
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conection.close()

#eliminar una reseña
@resenias_bp.route('/eliminar/<int:id>', methods=['DELETE'])
@verificar_token
@requiere_rol('Administrador','Funcionario')
def eliminarResenia(id):
    conection = get_connection()
    cursor = conection.cursor()

    try:
        cursor.execute("DELETE FROM resena WHERE id_resena = %s", (id,) )
        conection.commit()
        return jsonify({'mensaje':'Reseña eliminada correctamente'}), 204


    except Exception as e:
        conection.rollback()
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conection.close()

