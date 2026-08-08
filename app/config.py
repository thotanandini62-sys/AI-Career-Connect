import os
from dotenv import load_dotenv

# Load variables from .env if present
basedir = os.path.abspath(os.path.dirname(__file__))
parent_dir = os.path.abspath(os.path.join(basedir, os.pardir))
load_dotenv(os.path.join(parent_dir, '.env'))

class Config:
    """Base application configuration."""
    SECRET_KEY = os.getenv('SECRET_KEY', 'ai-career-connect-default-dev-secret-key-98213')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Mistral AI API settings
    MISTRAL_API_KEY = os.getenv('MISTRAL_API_KEY', '')
    MISTRAL_MODEL = os.getenv('MISTRAL_MODEL', 'mistral-small-latest')
    
    # Audio Upload / TTS configurations
    UPLOAD_FOLDER = os.path.join(basedir, 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload size
    
    @staticmethod
    def init_app(app):
        os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
        # Ensure instance directory exists for SQLite db
        instance_path = os.path.join(parent_dir, 'instance')
        os.makedirs(instance_path, exist_ok=True)

class DevelopmentConfig(Config):
    """Development environment configuration using SQLite."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 
        f"sqlite:///{os.path.join(parent_dir, 'instance', 'app.db')}"
    )

class TestingConfig(Config):
    """Testing environment configuration using in-memory SQLite."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    """Production environment configuration."""
    DEBUG = False
    _db_url = os.getenv('DATABASE_URL')
    if _db_url:
        if _db_url.startswith("postgres://"):
            _db_url = _db_url.replace("postgres://", "postgresql://", 1)
        SQLALCHEMY_DATABASE_URI = _db_url
    else:
        SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(parent_dir, 'instance', 'app.db')}"

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': ProductionConfig if os.getenv('RENDER') or os.getenv('FLASK_CONFIG') == 'production' else DevelopmentConfig
}

