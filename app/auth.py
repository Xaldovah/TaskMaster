"""
app.auth

This module provides authentication routes for user registration, login, and logout.
"""

from flask import jsonify, request
from flask_login import logout_user, login_required
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from flask_login import current_user
from app import app, db, bcrypt
from app.models import User
from datetime import datetime


@app.route('/api/register', methods=['POST'])
def create_user():
    """
    Register a new user.

    Returns:
        jsonify: JSON response with user information.
    """
    try:
        data = request.get_json()
        password = data.get('password')

        # Hash password before saving
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(
            username=data['username'],
            email=data.get('email'),
            password=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'user_id': new_user.id, 'username': new_user.username}), 201

    except Exception as e:
        app.logger.error(f'Error during registration: {e}')
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/api/login', methods=['POST'])
def login():
    """
    User login.

    Returns:
        jsonify: JSON response with login information.
    """
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            access_token = create_access_token(identity=user.id)

            return jsonify({'message': 'Login successful', 'access_token': access_token}), 200
        else:
            return jsonify({'error': 'Invalid credentials'}), 401

    except Exception as e:
        app.logger.error(f'Error during login: {e}')
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/api/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    User logout.

    Returns:
        jsonify: JSON response with logout information.
    """
    current_user.logged_out_at = datetime.utcnow()
    db.session.commit()
    return jsonify({'message': 'Logout successful'}), 200
