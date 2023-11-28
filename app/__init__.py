from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from app.celery import make_celery
import secrets

app = Flask(__name__)

secret_key = secrets.token_urlsafe(32)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://xaldovah:Denny23617@localhost/task_master'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = secret_key
app.config['CELERY_BROKER_URL'] = 'pyamqp://guest:guest@localhost:5672//'
app.config['result_backend'] = 'rpc://'

socketio = SocketIO(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
celery = make_celery(app)

from . import auth, extensions, notis, preferences, tasks, users
