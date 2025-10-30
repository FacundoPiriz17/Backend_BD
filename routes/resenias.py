
from flask import Blueprint, jsonify, request
from db import get_connection

resenias_bp = Blueprint('resenas', __name__, url_prefix='/resenas')

#Todas las reseñas
@resenias_bp.route('/all', methods=['GET'])
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
def aniadirResenia():
    conection = get_connection()
    cursor = conection.cursor()
    data = request.get_json()
    ci_participante = data.get("ci_participante")
    id_reserva = data.get("id_reserva")
    fecha_publicacion = data.get("fecha_publicacion")
    puntaje_general = data.get("puntaje_general")
    descripcion = data.get("descripcion")
    
    #Verifica que el usuario no haya hecho una reseña previa a esa sala
    cursor.execute("SELECT * FROM resena WHERE ci_participante = %s AND id_reserva = %s", (ci_participante, id_reserva))
    resultado = cursor.fetchone()
    if resultado:
        return jsonify({ "error": "El participante ya ha hecho una reseña a esta sala"})

    else:
        try:
            cursor.execute("INSERT INTO resena (id_reserva, ci_participante, fecha_publicacion, puntaje_general, descripcion) VALUES (%s,%s,%s,%s,%s)", (id_reserva, ci_participante, fecha_publicacion, puntaje_general, descripcion))
            conection.commit()
            return jsonify({'mensaje': 'Reseña registrada correctamente'}), 201

        except Exception as e:
            conection.rollback()
            return jsonify({'error': str(e)}), 500

        finally:
            cursor.close()
            conection.close()


#Modificar una reseña 
@resenias_bp.route('/modificar/<int:id>', methods=['PUT'])
def modificarResenia(id):
    conection = get_connection()
    cursor = conection.cursor()
    data = request.get_json()
    ci_participante = data.get("ci_participante")
    id_reserva = data.get("id_reserva")
    fecha_publicacion = data.get("fecha_publicacion")
    puntaje_general = data.get("puntaje_general")
    descripcion = data.get("descripcion")
    
    try:
        cursor.execute("UPDATE resena SET ci_participante = %s, id_reserva = %s, fecha_publicacion = %s, puntaje_general = %s, descripcion = %s WHERE id_resena = %s", (ci_participante, id_reserva, fecha_publicacion, puntaje_general, descripcion, id))
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

