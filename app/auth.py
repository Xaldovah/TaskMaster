"""
app.auth

This module provides authentication routes for user registration, login, and logout.
"""

from flask import jsonify, request, render_template, redirect, url_for, flash, session
from flask_login import logout_user, login_required
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from flask_login import current_user
from flask_mail import Message, Mail
from app import app, bcrypt, db
from flask_bcrypt import generate_password_hash, check_password_hash
from app.models import *
from datetime import datetime

mail = Mail(app)

@app.route('/', methods=['GET'])
def index():
    """Retrieve the home page
    """
    return render_template('index.html')


@app.route('/register', methods=['GET'])
def register_form():
  return render_template('register.html')


@app.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()

        # Validate input fields
        if 'username' not in data or 'email' not in data or 'password' not in data:
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400

        username = data['username']
        email = data['email']
        password = data['password']

        # Validate username, email, and password (customize as needed)
        if len(username) < 3 or len(username) > 50:
            return jsonify({'success': False, 'error': 'Invalid username length'}), 400

        if not email or '@' not in email or '.' not in email:
            return jsonify({'success': False, 'error': 'Invalid email format'}), 400

        if len(password) < 6:
            return jsonify({'success': False, 'error': 'Password must be at least 6 characters long'}), 400

        # Check if the email is already associated with a user
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'success': False, 'error': 'Email address already in use'}), 400

        # Hash the password before storing it using Flask-Bcrypt
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        # Create user object and save to the database
        user = User(username=username, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        # Return success message
        return jsonify({'success': True, 'message': 'User registered successfully!'})
    except KeyError:
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400


@app.route('/logout', methods=['POST'])
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


@app.route('/hash_password', methods=['POST'])
def hash_password():
    try:
        data = request.get_json()

        # Ensure the request includes the 'password' field
        if 'password' not in data:
            return jsonify({'success': False, 'error': 'Missing password field'}), 400

        # Extract the password from the request data
        password = data['password']

        # Hash the password using bcrypt
        hashed_password = generate_password_hash(password)

        # Return the hashed password
        return jsonify({'success': True, 'hashedPassword': hashed_password})

    except Exception as e:
        print(f"Error during password hashing: {str(e)}")
        return jsonify({'success': False, 'error': 'Internal server error'}), 500


@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data['email']
        password = data['password']

        # Fetch user from database by email
        user = User.query.filter_by(email=email).first()

        if not user or not verify_password(password, user.password):
            return jsonify({'success': False, 'error': 'Invalid credentials'}), 401

        # Generate access token
        access_token = create_access_token(identity=user.id)

        # Set user information in the session
        session['user_id'] = user.id
        session['username'] = user.username
        session['email'] = user.email

        # Return success message and include the access token
        return jsonify({
            'success': True,
            'message': 'Login successful!',
            'access_token': access_token,
            'user_info': {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }
        })
    except KeyError:
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400


@app.route('/get_access_token', methods=['GET'])
@jwt_required(optional=True)
def get_access_token():
    try:
        current_user_id = get_jwt_identity()
        if current_user_id:
            access_token = create_access_token(identity=current_user_id)
            return jsonify(access_token=access_token), 200
        else:
            return jsonify(error='Unauthorized'), 401
    except Exception as e:
        return jsonify(error=str(e)), 500


def verify_password(input_password, hashed_password):
    """Verify the input password against the hashed password."""
    return check_password_hash(hashed_password, input_password)
