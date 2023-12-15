"""
Module Description: This module contains API endpoints related to
user management.
"""

from flask import jsonify, request, redirect, url_for, current_app, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import app, bcrypt, db, ma
from app.auth import *
from app.models import *
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime


@app.route('/users', methods=['GET'])
@jwt_required()
def get_users():
    """
    Retrieve a list of all users.

    :return: JSON response with the list of users.
    """
    try:
         users = User.query.all()
         results = users_schema.dump(users)
         return jsonify(results)
    except SQLAlchemyError as e:
         return jsonify({'error': f'Database error: {str(e)}'}), 500


@app.route('/users/<id>', methods = ['GET'])
@jwt_required()
def get_single_user(id):
    current_user_id = get_jwt_identity()

    if user_id != current_user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    user = User.query.get(id)
    return user_schema.jsonify(user)


@app.route('/users/<id>', methods=['PUT'])
@jwt_required()
def update_user(id):
    """
    Update user preferences.

    :param user_id: ID of the user to be updated.
    :return: JSON response with the updated user preferences.
    """
    current_user_id = get_jwt_identity()

    if id != current_user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    user = User.query.get(id)

    if user is None:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()

    user.username = username
    user.email = email
    user.password = password

    db.session.commit()
    return user_schema.jsonify(user)


@app.route('/users/<id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    """
    Delete a user.

    :param user_id: ID of the user to be deleted.
    :return: JSON response indicating the success of the operation.
    """
    user = User.query.get(id)

    if user is None:
        return jsonify({'error': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()

    return user_schema.jsonify(user), 200
