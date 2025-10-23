from flask import Blueprint, request, jsonify
from db import get_connection
from hash_function import hasheo, verificar_contrasena

login_bp = Blueprint('login', __name__, url_prefix='/login')

@login_bp.route('/registro/usuario', methods=['POST'])
def registrar_usuario():
    data = request.get_json()
    ci = data.get('ci')
    nombre = data.get('nombre')
    apellido = data.get('apellido')
    email = data.get('email')
    rol = data.get('rol')
    contrasena = data.get('contrasena')

    if not all([ci, nombre, apellido, email, rol, contrasena]) or not all(str(x).strip() for x in [ci, nombre, apellido, email, rol, contrasena]):
        return jsonify({'error': 'Datos insuficientes'}), 400

    conection = get_connection()
    cursor = conection.cursor()
    try:
        cursor.execute(
            "INSERT INTO usuario (ci, nombre, apellido, email, rol) VALUES (%s, %s, %s, %s, %s)",
            (ci, nombre, apellido, email, rol)
        )

        contrasena_hasheada = hasheo(contrasena)

        cursor.execute(
            "INSERT INTO login (email, contrasena) VALUES (%s, %s)",
            (email, contrasena_hasheada)
        )

        conection.commit()
        return jsonify({'respuesta': 'Usuario creado correctamente'}), 201
    except Exception as e:
        conection.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        cursor.close()
        conection.close()

@login_bp.route('/usuarios', methods=['GET'])
def obtener_todos_los_usuarios():
    conection = get_connection()
    cursor = conection.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM usuario")
        resultados = cursor.fetchall()
        cursor.close()
        conection.close()
        return jsonify(resultados)
    except Exception as e:
        cursor.close()
        conection.close()
        return jsonify({'error': str(e)}), 500
