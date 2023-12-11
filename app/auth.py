"""
app.auth

This module provides authentication routes for user registration, login, and logout.
"""

from flask import jsonify, request, render_template, redirect, url_for
from flask_login import logout_user, login_required
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from flask_login import current_user
from app import app, bcrypt
from database import session
from sqlalchemy.orm import sessionmaker
from app.models import User
from datetime import datetime


@app.route('/register', methods=['POST'])
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
        session.add(new_user)
        session.commit()

        return jsonify({'user_id': new_user.id, 'username': new_user.username}), 201
    except Exception as e:
        app.logger.error(f'Error during registration: {e}')
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/login', methods=['POST'])
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


@app.route('/dashboard')
def dashboard():
    """
    Render the dashboard page.

    Returns:
        render_template: Rendered HTML template.
    """
    if current_user.is_authenticated:
        return render_template('dashboard.html')
    else:
        return redirect(url_for('login'))


@app.route('/home')
@jwt_required()
def home():
    """
    Render the home page.

    Returns:
        render_template: Rendered HTML template.
    """
    current_user_id = get_jwt_identity()

    if current_user_id:
        return render_template('dashboard.html')
    else:
        # If user is not authenticated, redirect to the login page
        return redirect(url_for('login'))


@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """
    User logout.

    Returns:
        jsonify: JSON response with logout information.
    """
    current_user.logged_out_at = datetime.utcnow()
    session.commit()
    return jsonify({'message': 'Logout successful'}), 200
