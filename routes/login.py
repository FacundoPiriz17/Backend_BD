import jwt
from flask import Blueprint, request, jsonify
import datetime
from db import get_connection
from hash_function import hasheo, verificar_contrasena
from validation import requiere_rol, verificar_token
from validators import validar_ci, validar_email_ucu

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

    programa = data.get('programa') or {}
    nombre_plan = (programa.get('nombre_plan') or '').strip()
    rol_academico = (programa.get('rol') or '').strip()

    if not all([ci, nombre, apellido, email, rol, contrasena]) or not all(str(x).strip() for x in [ci, nombre, apellido, email, rol, contrasena]):
        return jsonify({'error': 'Datos insuficientes'}), 400

    if not validar_ci(ci):
        return jsonify({'error': 'Cédula inválida'}), 400

    if not validar_email_ucu(email):
        return jsonify({'error': 'Email no válido. Debe ser @correo.ucu.edu.uy o @ucu.edu.uy'}), 400

    if rol not in ('Participante', 'Funcionario', 'Administrador'):
        return jsonify({'error': "Rol inválido. Use 'Participante', 'Funcionario' o 'Administrador'"}), 400

    requiere_programa = (rol == 'Participante')
    if requiere_programa:
        if not all([nombre_plan, rol_academico]):
            return jsonify({'error': 'Faltan datos de programa académico: nombre_plan y rol'}), 400
        if rol_academico not in ('Alumno', 'Docente'):
            return jsonify({'error': "Rol académico inválido. Use 'Alumno' o 'Docente'"}), 400

    con = get_connection()
    cur = con.cursor(dictionary=True)
    try:
        cur.execute("SELECT 1 FROM usuario WHERE ci = %s OR email = %s LIMIT 1", (ci, email))
        if cur.fetchone():
            return jsonify({'error': 'Ya existe un usuario con esa CI o email'}), 400

        cur2 = con.cursor()
        cur2.execute(
            "INSERT INTO usuario (ci, nombre, apellido, email, rol) VALUES (%s, %s, %s, %s, %s)",
            (ci, nombre, apellido, email, rol)
        )

        contrasena_hasheada = hasheo(contrasena)
        cur2.execute(
            "INSERT INTO login (email, contrasena) VALUES (%s, %s)",
            (email, contrasena_hasheada)
        )

        if requiere_programa:
            cur2.execute("SELECT 1 FROM planAcademico WHERE nombre_plan = %s LIMIT 1", (nombre_plan,))
            if cur2.fetchone() is None:
                con.rollback()
                return jsonify({'error': 'El plan académico indicado no existe'}), 400

            cur2.execute("""
                         SELECT 1
                         FROM participanteProgramaAcademico
                         WHERE ci_participante = %s
                           AND nombre_plan = %s LIMIT 1
                         """, (ci, nombre_plan))
            if cur2.fetchone():
                con.rollback()
                return jsonify({'error': 'El participante ya está asociado a ese plan académico'}), 400

            cur2.execute("""
                         INSERT INTO participanteProgramaAcademico (ci_participante, nombre_plan, rol)
                         VALUES (%s, %s, %s)
                         """, (ci, nombre_plan, rol_academico))

        con.commit()
        return jsonify({'respuesta': 'Usuario creado correctamente'}), 201

    except Exception as e:
        con.rollback()
        return jsonify({'error': str(e)}), 400
    finally:
        cur.close();
        con.close()

@login_bp.route('/usuarios', methods=['GET'])
@verificar_token
@requiere_rol('Administrador', 'Funcionario')
def obtener_usuarios():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT ci, nombre, apellido, email, rol FROM usuario")
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

    if not validar_email_ucu(email):
        return jsonify({'error': 'Email no válido. Debe ser @correo.ucu.edu.uy o @ucu.edu.uy'}), 400

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:

        cursor.execute("SELECT email FROM usuario WHERE ci = %s", (ci,))
        row = cursor.fetchone()
        if not row:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        email_anterior = row['email']

        cursor = conn.cursor()
        cursor.execute("UPDATE usuario SET nombre = %s, apellido = %s, email = %s, rol = %s WHERE ci = %s",
                       (nombre, apellido, email, rol, ci))

        if cursor.rowcount == 0:
            return jsonify({'error': 'Usuario no encontrado'}), 404

        if contrasena:
            contrasena_hasheada = hasheo(contrasena)
            cursor.execute("UPDATE login SET contrasena = %s WHERE email = %s",
                           (contrasena_hasheada, email_anterior))
        if email != email_anterior:
            cursor.execute("UPDATE login SET email = %s WHERE email = %s",
                           (email, email_anterior))

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
    con = get_connection()
    cur = con.cursor(dictionary=True)
    try:
        cur.execute("SELECT email FROM usuario WHERE ci = %s", (ci,))
        row = cur.fetchone()
        if not row:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        email = row['email']

        cur2 = con.cursor()
        cur2.execute("DELETE FROM participanteProgramaAcademico WHERE ci_participante = %s", (ci,))


        cur2.execute("DELETE FROM reservaParticipante WHERE ci_participante = %s", (ci,))

        cur2.execute("DELETE FROM login WHERE email = %s", (email,))

        cur2.execute("DELETE FROM usuario WHERE ci = %s", (ci,))
        if cur2.rowcount == 0:
            con.rollback()
            return jsonify({'error': 'Usuario no encontrado'}), 404

        con.commit()
        return jsonify({'mensaje': 'Usuario eliminado correctamente'}), 200

    except Exception as e:
        con.rollback()
        err = str(e)
        if 'foreign key constraint' in err.lower():
            return jsonify({'error': 'No se puede eliminar: existen registros asociados'}), 400
        return jsonify({'error': err}), 400
    finally:
        cur.close();
        con.close()

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