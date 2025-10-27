from flask import Blueprint, request, jsonify
from db import get_connection

edificio_bp = Blueprint('stats', __name__, url_prefix='/stats')