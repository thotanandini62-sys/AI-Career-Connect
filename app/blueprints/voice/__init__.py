from flask import Blueprint

voice_bp = Blueprint('voice', __name__)

from app.blueprints.voice import routes
