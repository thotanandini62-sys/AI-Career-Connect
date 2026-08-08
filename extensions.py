from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

# Instantiate extensions without binding to app to prevent circular imports
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

# Configure login manager parameters
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Please log in to access this career tool.'
login_manager.login_message_category = 'warning'
