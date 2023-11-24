from flask import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import *

DEFAULT_TASK_VIEW = 'all'
ENABLE_NOTIFICATIONS = True
THEME_PREFERENCE = 'dark'

@app.route('/api/user/preferences', methods=['GET'])
@jwt_required()
def get_user_preferences():
    current_user_id = get_jwt_identity()

    user_preferences = {
        'default_task_view': DEFAULT_TASK_VIEW,
        'enable_notifications': ENABLE_NOTIFICATIONS,
        'theme_preference': THEME_PREFERENCE,
    }

    return jsonify(user_preferences)
