"""
Module Description: This module contains the initialization
and configuration of a Flask application.
"""

from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import *
from flask_cors import CORS
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from flask_login import LoginManager
# from flask_mail import Mail
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from app.celery import make_celery
import secrets

# Create Flask application instance
app = Flask(__name__)

# Generate a secure random key for Flask app
secret_key = secrets.token_urlsafe(32)

# Configure Flask application
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://xaldovah:Denny23617@localhost/task_master'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = secret_key
app.config['CELERY_BROKER_URL'] = 'pyamqp://guest:guest@localhost:5672//'
app.config['result_backend'] = 'rpc://'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']

# app.config['MAIL_SERVER'] = 'smtp.mailtrap.io'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USE_SSL'] = False
# app.config['MAIL_USERNAME'] = 'Dennis Kimani'
# app.config['MAIL_PASSWORD'] = 'Denny4390'

# Enable Cross-Origin Resource Sharing (CORS)
cors = CORS(app, supports_credentials=True, origins=["http://arkwebs.tech", "http://localhost:5000"])

# Create SocketIO instance
socketio = SocketIO(app)

# Create SQLAlchemy instance
db = SQLAlchemy(app)

# Create and configure Flask-Migrate instance
migrate = Migrate(app, db)

# Create and configure Flask-Bcrypt instance
bcrypt = Bcrypt(app)

# Create and configure Flask-JWT-Extended instance
jwt = JWTManager(app)

# Create and configure a Mail instance

# Create and configure Flask-Login instance
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Create Celery instance
celery = make_celery(app)

# Import application modules
from . import auth, extensions, notis, preferences, tasks, users
