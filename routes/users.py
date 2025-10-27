from flask import Blueprint, request, jsonify
from db import get_connection

users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('/usuarios', methods=['GET'])
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