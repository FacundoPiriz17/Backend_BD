from flask import Blueprint, request, jsonify
from db import get_connection

edificio_bp = Blueprint('edificio', __name__, url_prefix='/edificio')

@edificio_bp.route('/todos', methods=['GET'])
def obtener_todos_los_usuarios():
    conection = get_connection()
    cursor = conection.cursor()

    try:
        cursor.execute("SELECT * FROM edificio")
        resultados = cursor.fetchall()
        cursor.close()
        conection.close()
        return jsonify(resultados)
    except Exception as e:
        cursor.close()
        conection.close()
        return jsonify({'error': str(e)}), 500


@edificio_bp.route('/todos/<string:nombre>', methods=['GET'])
def obtener_plan_por_id(nombre):
    conection = get_connection()
    cursor = conection.cursor()

    try:
        cursor.execute("SELECT * FROM edificio WHERE nombre_edificio = %s", (nombre,))
        edificio = cursor.fetchone()
        if edificio:
            return jsonify(edificio)
        else:
            return jsonify({'mensaje': 'Edificio no encontrado'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conection.close()