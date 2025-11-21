import mysql.connector
from config import (
    DB_HOST, DB_NAME,
    DB_APP_USER, DB_APP_PASSWORD,
    DB_ADMIN_USER, DB_ADMIN_PASSWORD,
    DB_FUNC_USER, DB_FUNC_PASSWORD,
    DB_PART_USER, DB_PART_PASSWORD,
)

def get_connection(rol=None):
    if rol == "Administrador":
        user, pwd = DB_ADMIN_USER, DB_ADMIN_PASSWORD
    elif rol == "Funcionario":
        user, pwd = DB_FUNC_USER, DB_FUNC_PASSWORD
    elif rol == "Participante":
        user, pwd = DB_PART_USER, DB_PART_PASSWORD
    else:
        user, pwd = DB_APP_USER, DB_APP_PASSWORD

    return mysql.connector.connect(
        host=DB_HOST,
        user=user,
        password=pwd,
        database=DB_NAME,
        auth_plugin='mysql_native_password'
    )
