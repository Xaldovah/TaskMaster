"""
Module Description: This module contains the initialization
and configuration of a Flask application.
"""

from flask import Flask, render_template, request, redirect, url_for
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect
from flask_socketio import SocketIO
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
from app.celery import make_celery
from datetime import timedelta

# Create Flask application instance
app = Flask(__name__, template_folder='templates')

# Secure key (should use secrets to autogenerate)
secret_key = '4d95d7d31e4e8d50e7e53d1fa8db928a8bc9abfe94bfc6e8c892c1b78e159b14a03887a49e9e4737ac9aa1ee9e4c6b62'

# Configure Flask application
app.config['SECRET_KEY'] = '4d95d7d31e4e8d50e7e53d1fa8db928a8bc9abfe94bfc6e8c892c1b78e159b14a03887a49e9e4737ac9aa1ee9e4c6b62'
app.config['WTF_CSRF_ENABLED'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://dhwok6z2d29k5t4yuu8k:pscale_pw_53OSRVYXEhZ0TmGug2ET8PvW18Hx7taYCkeR2uXrc2c@aws.connect.psdb.cloud/task_master'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://xaldovah:Denny23617@localhost/task_master'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = secret_key
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)
app.config['CELERY_BROKER_URL'] = 'pyamqp://guest:guest@localhost:5672//'
app.config['result_backend'] = 'rpc://'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access']

# Enable Cross-Origin Resource Sharing (CORS)
cors = CORS(app, supports_credentials=True, origins=["http://arkwebs.tech", "http://localhost:5000"])

# Create SocketIO instance
socketio = SocketIO(app)

# Create a csrf protection
csrf = CSRFProtect(app)

# Create and configure Flask-Migrate instance
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Create and configure Flask-Marshmallow
ma = Marshmallow(app)

# Create and configure Flask-Bcrypt instance
bcrypt = Bcrypt(app)

# Create and configure Flask-JWT-Extended instance
jwt = JWTManager(app)

# Create and configure Flask-Login instance
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Create Celery instance
celery = make_celery(app)

# Import application modules
from . import auth, extensions, notis, preferences, tasks, users
