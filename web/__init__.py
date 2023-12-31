"""
Module Description: This module contains the initialization
and configuration of a Flask application.
"""

from flask import Flask
from flask_login import LoginManager
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect
from flask_socketio import SocketIO
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from datetime import timedelta
from dotenv import load_dotenv
from os import path

db = SQLAlchemy()
ma = Marshmallow()
login_manager = LoginManager()
jwt = JWTManager()
socketio = SocketIO()

DB_NAME = "database.db"

def create_app():
    # Create Flask application instance
    app = Flask(__name__, template_folder='templates', static_url_path='/static')

    # Load the env file
    load_dotenv()

    # Secure key (should use secrets to autogenerate)
    secret_key = '4d95d7d31e4e8d50e7e53d1fa8db928a8bc9abfe94bfc6e8c892c1b78e159b14a03887a49e9e4737ac9aa1ee9e4c6b62'

    # Configure Flask application
    app.config['SECRET_KEY'] = secret_key
    app.config['WTF_CSRF_ENABLED'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = secret_key
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.config['JWT_BLACKLIST_ENABLED'] = True
    app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']

    # Enable Cross-Origin Resource Sharing (CORS)
    CORS(app, supports_credentials=True, origins=["http://arkwebs.tech", "http://localhost:5000"])

    # Create SocketIO instance
    socketio.init_app(app)

    # Create a csrf protection
    CSRFProtect(app)

    # Create and configure Flask-Migrate instance
    db.init_app(app)
    Migrate(app, db)

    # Create and configure Flask-Marshmallow
    ma.init_app(app)

    # Create and configure Flask-Bcrypt instance
    Bcrypt(app)

    # Create and configure Flask-JWT-Extended instance
    jwt.init_app(app)

    # Create and configure Flask-Login instance
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    # Import and register blueprints
    from .auth import auth
    from .notis import notis
    from .preferences import preferences
    from .tasks import tasks
    from .users import users

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(notis, url_prefix='/')
    app.register_blueprint(preferences, url_prefix='/')
    app.register_blueprint(tasks, url_prefix='/')
    app.register_blueprint(users, url_prefix='/')

    from .models import User, Task, Category, Notification

    create_database(app)

    return app

def create_database(app):
    if not path.exists('web/' + DB_NAME):
        with app.app_context():
            db.create_all()
        print('Database created!')

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
