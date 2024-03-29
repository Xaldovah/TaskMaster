"""
Module Description: This module contains an API endpoint
for retrieving user preferences.
"""

from flask import jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity

DEFAULT_TASK_VIEW = 'all'
ENABLE_NOTIFICATIONS = True
THEME_PREFERENCE = 'dark'

preferences = Blueprint('preferences', __name__)

@preferences.route('/user/preferences', methods=['GET'])
@jwt_required()
def get_user_preferences():
    """
    Retrieve user preferences for the current user.

    :return: JSON response with user preferences.
    """
    current_user_id = get_jwt_identity()

    user_preferences = {
        'default_task_view': DEFAULT_TASK_VIEW,
        'enable_notifications': ENABLE_NOTIFICATIONS,
        'theme_preference': THEME_PREFERENCE,
    }

    return jsonify(user_preferences)
