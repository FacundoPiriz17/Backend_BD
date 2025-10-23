from flask_cors import CORS
import flask
from flask import Flask
from routes.login import login_bp


app = Flask(__name__)
CORS(app)

app.register_blueprint(login_bp)

@app.route('/')
def init():
    return 'Bienvenidos a la api del obligatorio de BD 2025'

if __name__ == '__main__':
    app.run(debug=True)