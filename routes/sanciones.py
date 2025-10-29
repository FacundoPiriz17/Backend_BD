from flask import Blueprint, jsonify, request
from db import get_connection

sanciones_bp = Blueprint('sanciones', __name__, url_prefix='/sanciones')

#Todas las sanciones
@sanciones_bp.route('/sanciones/all', methods=['GET'])
def sanciones():
    conection = get_connection()
    cursor = conection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM sancion_participante")
        resultados = cursor.fetchall()  # Obtiene TODAS las filas del resultado
        return jsonify(resultados)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conection.close()
        
#Obtener una sanción específica
@sanciones_bp.route('/sanciones/<int:id>', methods=['GET'])
def sancionEspecifica(id):
    conection = get_connection()
    cursor = conection.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM sancion_participante WHERE id_sancion = %s", (id,) )
        sancion = cursor.fetchone()  
        if sancion:
            return jsonify(sancion)
        else:
            return jsonify({'mensaje': 'Sanción no encontrada'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conection.close()

#Añadir una sancion
@sanciones_bp.route('/sanciones', methods=['POST'])
def aniadirSancion():
    conection = get_connection()
    cursor = conection.cursor()
    data = request.get_json()
    ci_participante = data.get("ci_participante")
    descripcion = data.get("descripcion")
    fecha_inicio = data.get("fecha_inicio")
    fecha_fin = data.get("fecha_fin")

    #Verifica que el usuario no una sanción previa
    cursor.execute("SELECT * FROM sancion_participante WHERE ci_participante = %s AND fecha_fin > CURDATE();", (ci_participante,) )
    resultado = cursor.fetchone()
    if resultado:
        return jsonify({ "error": "El participante ya tiene una sanción activa" })

    else:
        try:
            cursor.execute("INSERT INTO sancion_participante (ci_participante,descripcion,fecha_inicio, fecha_fin) VALUES (%s,%s,%s,%s)", (ci_participante,descripcion,fecha_inicio, fecha_fin))
            conection.commit()
            return jsonify({'mensaje': 'Sanción registrada correctamente'}), 201

        except Exception as e:
            conection.rollback()
            return jsonify({'error': str(e)}), 500

        finally:
            cursor.close()
            conection.close()

#Modificar una sanción 
@sanciones_bp.route('/sanciones/<int:id>', methods=['PUT'])
def modificarSancion(id):
    conection = get_connection()
    cursor = conection.cursor()
    data = request.get_json()
    ci_participante = data.get("ci_participante")
    descripcion = data.get("descripcion")
    fecha_inicio = data.get("fecha_inicio")
    fecha_fin = data.get("fecha_fin")
    
    try:
        cursor.execute("UPDATE sancion_participante SET  ci_participante = %s, descripcion = %s, fecha_inicio = %s, fecha_fin = %s WHERE id_sancion = %s", ( ci_participante,descripcion, fecha_inicio, fecha_fin, id))
        conection.commit()
        return jsonify({'mensaje': 'Sancion modificada correctamente'}), 200
    
    except Exception as e:
        conection.rollback()
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conection.close()

#eliminar una sanción
@sanciones_bp.route('/sanciones/<int:id>', methods=['DELETE'])
def eliminarSancion(id):
    conection = get_connection()
    cursor = conection.cursor()

    try:
        cursor.execute("DELETE FROM sancion_participante WHERE id_sancion = %s", (id,) )
        conection.commit()
        return jsonify({'mensaje':'Sanción eliminada correctamente'}), 204
        

    except Exception as e:
        conection.rollback()
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conection.close()

