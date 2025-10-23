from dotenv import load_dotenv
import os
import mysql.connector

load_dotenv()
def get_connection():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password = 'rootpassword',
        database='Obligatorio',
        auth_plugin='mysql_native_password'
    )

# password=os.getenv("MYSQL_ROOT_PASSWORD"),

