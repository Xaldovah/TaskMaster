"""
Module Description: This module contains configurations for Flask extensions
such as Flask-RESTful, Flask-JWT-Extended, and Flask-Login.
"""

from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_login import LoginManager
from app import app
from app.models import User

api = Api(app)
jwt = JWTManager(app)
jwt_blocklist = set()

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    """
    Load user by user ID for Flask-Login.

    :param user_id: User ID.
    :return: User object.
    """
    return User.query.get(int(user_id))
