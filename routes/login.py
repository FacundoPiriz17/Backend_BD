import jwt
from flask import Blueprint, request, jsonify
import datetime
from db import get_connection
from hash_function import hasheo, verificar_contrasena
from validation import requiere_rol, verificar_token

login_bp = Blueprint('login', __name__, url_prefix='/login')

SECRET_KEY = "clave_secreta" #Variable asignada en .env en la dockerización

@login_bp.route('/registro', methods=['POST'])
@verificar_token
@requiere_rol('Administrador')
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
@verificar_token
@requiere_rol('Administrador', 'Funcionario')
def obtener_usuarios():
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT * FROM usuario")
        usuarios = cursor.fetchall()
        return jsonify(usuarios), 200
    except Exception as e:
        return jsonify({'error': str(e)}, 400)
    finally:
        cursor.close()
        connection.close()

@login_bp.route('/usuarios/<int:ci>', methods=['GET'])
@verificar_token
@requiere_rol('Administrador', 'Funcionario', 'Participante')
def obtener_usuario_por_ci(ci):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT ci, nombre, apellido, email, rol FROM usuario WHERE ci = %s", (ci,))
        usuario = cursor.fetchone()
        if usuario:
            return jsonify(usuario), 200
        return jsonify({'error': 'Usuario no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        cursor.close()
        connection.close()

@login_bp.route('/usuarios/<int:ci>', methods=['PUT'])
@verificar_token
@requiere_rol('Administrador', 'Funcionario', 'Participante')
def actualizar_usuario(ci):
    data = request.get_json()
    nombre = data.get('nombre')
    apellido = data.get('apellido')
    email = data.get('email')
    rol = data.get('rol')
    contrasena = data.get('contrasena')

    if not all([nombre, apellido, email, rol]) or not all(str(x).strip() for x in [nombre, apellido, email, rol]):
        return jsonify({'error': 'Faltan datos requeridos'}), 400

    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE usuario SET nombre = %s, apellido = %s, email = %s, rol = %s WHERE ci = %s",
                       (nombre, apellido, email, rol, ci))

        if cursor.rowcount == 0:
            return jsonify({'error': 'Usuario no encontrado'}), 404

        if contrasena:
            contrasena_hasheada = hasheo(contrasena)
            cursor.execute("""
                UPDATE login
                SET contrasena = %s
                WHERE email = %s
            """, (contrasena_hasheada, email))

        conn.commit()
        return jsonify({'mensaje': 'Usuario actualizado correctamente'}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        cursor.close()
        conn.close()

@login_bp.route('/usuarios/<int:ci>', methods=['DELETE'])
@verificar_token
@requiere_rol('Administrador')
def eliminar_usuario(ci):
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("""
            DELETE FROM login
            WHERE email = (SELECT email FROM usuario WHERE ci = %s)
        """, (ci,))
        cursor.execute("DELETE FROM usuario WHERE ci = %s", (ci,))

        if cursor.rowcount == 0:
            return jsonify({'error': 'Usuario no encontrado'}), 404

        conn.commit()
        return jsonify({'mensaje': 'Usuario eliminado correctamente'}), 200
    except Exception as e:
        conn.rollback()
        error_msg = str(e)
        if 'foreign key constraint' in error_msg.lower():
            return jsonify({'error': 'No se puede eliminar un usuario con registros asociados'}), 400
        return jsonify({'error': error_msg}), 400
    finally:
        cursor.close()
        conn.close()

@login_bp.route('/inicio', methods=['POST'])
def login_usuario():
    data = request.get_json()
    email = data.get('email')
    contrasena = data.get('contrasena')

    if not all([email, contrasena]):
        return jsonify({'error': 'Faltan datos requeridos'}), 400

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT u.ci, u.nombre, u.apellido, u.email, u.rol, l.contrasena 
            FROM usuario u
            JOIN login l ON u.email = l.email
            WHERE u.email = %s
        """, (email,))
        usuario = cursor.fetchone()

        if usuario and verificar_contrasena(contrasena, usuario['contrasena']):
            token = jwt.encode(
                {
                    "ci": usuario["ci"],
                    "email": usuario["email"],
                    "rol": usuario["rol"],
                    "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=2)
                },
                SECRET_KEY,
                algorithm="HS256"
            )

            del usuario['contrasena']

            return jsonify({
                'mensaje': 'Inicio de sesión exitoso',
                'usuario': usuario,
                'token': token
            }), 200
        else:
            return jsonify({'error': 'Credenciales inválidas'}), 401
    except Exception as e:
        return jsonify({'error': str(e)}), 400
    finally:
        cursor.close()
        conn.close()