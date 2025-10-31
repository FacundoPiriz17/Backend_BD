from flask import Blueprint, jsonify, request
from db import get_connection

salas_bp = Blueprint('salas', __name__, url_prefix='/salas')

# Mostrar todas las salas
@salas_bp.route('/mostrar_salas', methods=['GET'])
def mostrar_salas():
    conection = get_connection()
    cursor = conection.cursor(dictionary=True)
    try:
        cursor.execute("'SELECT *  FROM salaDeEstudio"'')
        resultados = cursor.fetchall()
        return jsonify(resultados)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conection.close()

# Mostrar las salas disponibles
@salas_bp.route('/salas_disponibles', methods=['GET'])
def salas_disponibles():
    conection = get_connection()
    cursor = conection.cursor(dictionary=True)
    try:
        cursor.execute('''SELECT * 
                        FROM salaDeEstudio
                        WHERE disponible = TRUE''')
        resultados = cursor.fetchall()
        return jsonify(resultados)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

    finally:
        cursor.close()
        conection.close()

# Agregar una nueva sala
@salas_bp.route('/addSala', methods=['POST'])
def addSala():
    data = request.get_json()
    nombre_sala = data.get('nombre_sala')
    edificio = data.get('edificio')
    capacidad = data.get('capacidad')
    tipo_sala = data.get('tipo_sala')

    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("INSERT INTO salaDeEstudio(nombre_sala, edificio, capacidad, tipo_sala) VALUES (%s,%s,%s,%s)", (nombre_sala, edificio, capacidad, tipo_sala))
        connection.commit()
        return jsonify({'mensaje': 'Sala insertada correctamente'}), 201
    except Exception as e:
        connection.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        connection.close()


#Falta revisar posible prevencion de que la sala ya se encuentre en el sistema


#Modificar Sala:
@salas_bp.route('/modificarSala/<string : nombre_sala>/<string:edificio> ', methods=['PUT'])
def modificarsala(nombre_sala, edificio):
    data = request.get_json()
