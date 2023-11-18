from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
import secrets

app = Flask(__name__)

secret_key = secrets.token_urlsafe(32)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://xaldovah:Denny23617@localhost/task_master'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = secret_key

db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

from . import routes
