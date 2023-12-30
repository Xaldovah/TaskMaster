"""
Module Description: This module contains API endpoints related to user management.
"""
from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from web.models import User
from sqlalchemy.exc import SQLAlchemyError

users = Blueprint('users', __name__)


@users.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    """
    Retrieve a list of all users.

    Returns:
        jsonify: JSON response with the list of users.
    """
    try:
        users = User.query.all()
        results = users_schema.dump(users)
        return jsonify(results)
    except SQLAlchemyError as e:
        return jsonify({'error': f'Database error: {str(e)}'}), 500


@users.route('/users/<id>', methods=['GET'])
@jwt_required()
def get_single_user(id):
    """
    Retrieve information about a single user.

    Args:
        id (str): ID of the user.

    Returns:
        jsonify: JSON response with user information.
    """
    current_user_id = get_jwt_identity()

    if id != current_user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    user = User.query.get(id)
    return user_schema.jsonify(user)


@users.route('/users/<id>', methods=['PUT'])
@jwt_required()
def update_user(id):
    """
    Update user preferences.

    Args:
        id (str): ID of the user to be updated.

    Returns:
        jsonify: JSON response with the updated user preferences.
    """
    current_user_id = get_jwt_identity()

    if id != current_user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    user = User.query.get(id)

    if user is None:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()

    # Update user attributes based on the received data
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    user.password = data.get('password', user.password)

    db.session.commit()
    return user_schema.jsonify(user)


@users.route('/users/<id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    """
    Delete a user.

    Args:
        id (str): ID of the user to be deleted.

    Returns:
        jsonify: JSON response indicating the success of the operation.
    """
    user = User.query.get(id)

    if user is None:
        return jsonify({'error': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify(user), 200
