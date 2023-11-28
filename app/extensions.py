from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from app import app
from app.models import *

api = Api(app)
jwt = JWTManager(app)
jwt_blocklist = set()

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
