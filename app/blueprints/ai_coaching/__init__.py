from flask import Blueprint

ai_coaching_bp = Blueprint('ai_coaching', __name__)

from app.blueprints.ai_coaching import routes
