from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
import secrets


app = Flask(__name__)

secret_key = secrets.token_urlsafe(32)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://xaldovah:@Denny23617@localhost/task_master'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = secret_key


jwt = JWTManager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from . import routes
