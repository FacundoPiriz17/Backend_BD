import jwt
from flask import request, jsonify
from functools import wraps

SECRET_KEY = "clave_secreta" #Variable asignada en .env en la dockerización

def verificar_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = None
        if 'Authorization' in request.headers:
            partes = request.headers['Authorization'].split(" ")
            if len(partes) == 2:
                token = partes[1]

        if not token:
            return jsonify({'error': 'Token no proporcionado'}), 401

        try:
            datos = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            request.usuario_actual = datos
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'El token ha expirado'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Token inválido'}), 401

        return func(*args, **kwargs)
    return wrapper

def requiere_rol(*roles_permitidos):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            usuario = getattr(request, 'usuario_actual', None)
            if not usuario:
                return jsonify({'error': 'Token no proporcionado o inválido'}), 401

            if usuario.get("rol") not in roles_permitidos:
                return jsonify({'error': f'Acceso denegado para el rol {usuario.get("rol")}'}), 403

            return func(*args, **kwargs)
        return wrapper
    return decorator