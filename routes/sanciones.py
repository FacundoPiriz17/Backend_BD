from flask import Blueprint, jsonify, request
from db import get_connection
from validators import validar_ci
from datetime import datetime
from validation import verificar_token, requiere_rol

sanciones_bp = Blueprint('sanciones', __name__, url_prefix='/sanciones')

#Todas las sanciones
@sanciones_bp.route('/all', methods=['GET'])
@verificar_token
@requiere_rol('Administrador','Funcionario')
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
@sanciones_bp.route('/sancion/<int:id>', methods=['GET'])
@verificar_token
@requiere_rol('Administrador', 'Funcionario')
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
@sanciones_bp.route('/registrar', methods=['POST'])
@verificar_token
@requiere_rol('Administrador', 'Funcionario')
def aniadirSancion():
    conection = get_connection()
    cursor = conection.cursor()
    data = request.get_json()
    ci_participante = data.get("ci_participante")
    descripcion = data.get("descripcion")
    fecha_inicio = data.get("fecha_inicio")
    fecha_fin = data.get("fecha_fin")

    if not all([ci_participante, descripcion, fecha_inicio, fecha_fin]):
        return jsonify({'error': 'Faltan datos requeridos'}), 400

    if not validar_ci(ci_participante):
        return jsonify({'error': 'Cédula inválida'}), 400

    #Verifica que el usuario no una sanción previa
    cursor.execute("SELECT * FROM sancion_participante WHERE ci_participante = %s AND fecha_fin > CURDATE();",
                   (ci_participante,))
    resultado = cursor.fetchone()
    if resultado:
        cursor.close()
        conection.close()
        return jsonify({"error": "El participante ya tiene una sanción activa"}), 400

    # Validar fechas: fecha_fin > fecha_inicio
    try:
        fi = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
        ff = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
    except Exception:
        return jsonify({'error': 'Formato de fecha inválido. Use YYYY-MM-DD'}), 400

    if ff <= fi:
        return jsonify({'error': 'La fecha de fin debe ser posterior a la de inicio.'}), 400

    try:
        cursor.execute(
            "INSERT INTO sancion_participante (ci_participante, motivo, fecha_inicio, fecha_fin) VALUES (%s,%s,%s,%s)",
            (ci_participante, descripcion, fecha_inicio, fecha_fin))
        conection.commit()
        return jsonify({'mensaje': 'Sanción registrada correctamente'}), 201

    except Exception as e:
        conection.rollback()
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conection.close()

#Modificar una sanción 
@sanciones_bp.route('/modificar/<int:id>', methods=['PUT'])
@verificar_token
@requiere_rol('Administrador', 'Funcionario')
def modificarSancion(id):
    conection = get_connection()
    cursor = conection.cursor()
    data = request.get_json()
    ci_participante = data.get("ci_participante")
    descripcion = data.get("descripcion")
    fecha_inicio = data.get("fecha_inicio")
    fecha_fin = data.get("fecha_fin")

    if not all([ci_participante, descripcion, fecha_inicio, fecha_fin]):
        return jsonify({'error': 'Faltan datos requeridos'}), 400

    if not validar_ci(ci_participante):
        return jsonify({'error': 'Cédula inválida'}), 400

    try:
        from datetime import datetime
        fi = datetime.strptime(fecha_inicio, "%Y-%m-%d").date()
        ff = datetime.strptime(fecha_fin, "%Y-%m-%d").date()
    except Exception:
        return jsonify({'error': 'Formato de fecha inválido. Use YYYY-MM-DD'}), 400

    if ff <= fi:
        return jsonify({'error': 'La fecha de fin debe ser posterior a la de inicio.'}), 400

    try:
        cursor.execute(
            "UPDATE sancion_participante SET  ci_participante = %s, motivo = %s, fecha_inicio = %s, fecha_fin = %s WHERE id_sancion = %s",
            (ci_participante, descripcion, fecha_inicio, fecha_fin, id))
        conection.commit()
        return jsonify({'mensaje': 'Sancion modificada correctamente'}), 200

    except Exception as e:
        conection.rollback()
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conection.close()


#eliminar una sanción
@sanciones_bp.route('/eliminar/<int:id>', methods=['DELETE'])
@verificar_token
@requiere_rol('Administrador', 'Funcionario')
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

