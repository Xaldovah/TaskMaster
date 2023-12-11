"""
Module Description: This module contains API endpoints related to
user management.
"""

from flask import jsonify, request, redirect, url_for, current_app, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import app, bcrypt
from app.auth import *
from app.models import User
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime
from database import engine, session
from sqlalchemy import text


def load_users_from_db():
    with engine.connect() as conn:
        query = text("SELECT * FROM user")
        res = conn.execute(query)
        users = [dict(row) for row in res.fetchall()]
        return users


@app.route('/users', methods=['GET'])
def get_users():
    """
    Retrieve a list of all users.

    :return: JSON response with the list of users.
    """
    try:
        user_list = load_users_from_db()
        return render_template('users.html', users=user_list)
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500


@app.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    """
    Update user preferences.

    :param user_id: ID of the user to be updated.
    :return: JSON response with the updated user preferences.
    """
    current_user_id = get_jwt_identity()

    if user_id != current_user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    user = User.query.get(user_id)

    if user is None:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()

    # Update preferences if provided in the request
    if 'default_task_view' in data:
        user.default_task_view = data['default_task_view']
    if 'enable_notifications' in data:
        user.enable_notifications = data['enable_notifications']
    if 'theme_preference' in data:
        user.theme_preference = data['theme_preference']

    session.commit()

    return jsonify({
        'user_id': user.id,
        'username': user.username,
        'default_task_view': user.default_task_view,
        'enable_notifications': user.enable_notifications,
        'theme_preference': user.theme_preference
    })


@app.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    """
    Delete a user.

    :param user_id: ID of the user to be deleted.
    :return: JSON response indicating the success of the operation.
    """
    user = User.query.get(user_id)

    if user is None:
        return jsonify({'error': 'User not found'}), 404

    session.delete(user)
    session.commit()

    return jsonify({'message': 'User deleted successfully'}), 200
