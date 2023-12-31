"""
app.auth

This module provides authentication routes for user registration, login, and logout.
"""

from flask import Blueprint, jsonify, request, make_response, render_template, session, redirect, url_for
from flask_jwt_extended import create_access_token, jwt_required
from flask_login import login_required, login_user, current_user, logout_user
from flask_bcrypt import Bcrypt, check_password_hash
from flask_mail import Message, Mail
from .models import *
from . import db, ma
from datetime import datetime

mail = Mail()
bcrypt = Bcrypt()
auth = Blueprint('auth', __name__)


@auth.route('/', methods=['GET'])
def index():
    """Retrieve the home page."""
    return render_template('index.html')


@auth.route('/dashboard')
@login_required
def dashboard():
    """Render the dashboard page."""
    return render_template('dashboard.html')


@auth.route('/about')
def about():
    """Render the about page."""
    return render_template('about.html')


@auth.route('/contact', methods=['GET', 'POST'])
def contact():
    """Render the contact page."""
    return render_template('contact.html')


@auth.route('/register', methods=['OPTIONS'])
@auth.route('/login', methods=['OPTIONS'])
def handle_options():
    response = make_response()
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'POST')
    return response


@auth.route('/register', methods=['GET', 'POST'])
def register():
    """
    Register a new user.

    This endpoint handles user registration by validating input data, checking for existing users,
    hashing the password, and storing the user information in the database.

    Returns:
        jsonify: JSON response with user information or an error message.
    """
    if request.method == "POST":
        try:
            if request.is_json:
                data = request.json
                username = data.get('username')
                email = data.get('email')
                password = data.get('password')
            else:
                username = request.form.get('username')
                email = request.form.get('email')
                password = request.form.get('password')

            if not all((username, email, password)):
                return jsonify({'success': False, 'error': 'Missing required fields'}), 400

            if not (3 <= len(username) <= 50):
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

            # return user_schema.jsonify(user)
            return redirect(url_for('auth.login'))
        except Exception as e:
            print(e)
            return jsonify({'success': False, 'error': 'Registration failed'}), 400

    return render_template('register.html')


@auth.route('/login', methods=['GET', 'POST'])
def login():
    """
    User login.

    This endpoint handles user login by verifying credentials, generating an access token,
    and setting user information in the session.

    Returns:
        jsonify: JSON response with login information or an error message.
    """
    if request.method == "GET":
        return render_template('register.html')

    try:
        if request.is_json:
            data = request.json
            email = data.get('email')
            password = data.get('password')
        else:
            email = request.form.get('email')
            password = request.form.get('password')

        if not all((email, password)):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400

        # Fetch user from the database by email
        user = User.query.filter_by(email=email).first()

        if not user or not verify_password(password, user.password):
            return jsonify({'success': False, 'error': 'Invalid credentials'}), 401

        # Log the user in using Flask-Login
        login_user(user)

        # Generate an access token
        access_token = create_access_token(identity=user.id)

        # Set user information in the session (optional)
        session['user_id'] = user.id
        session['username'] = user.username
        session['email'] = user.email

        response_data = {
            'success': True,
            'message': 'Login successful!',
            'user_info': user_schema.dump(user),
            'access_token': access_token
        }

        response = make_response(jsonify(response_data), 200)
        response.headers['Authorization'] = f'Bearer {access_token}'

        # Redirect to the dashboard after successful login
        return response

    except Exception as e:
        print(e)
        return jsonify({'success': False, 'error': 'Login failed'}), 400

def verify_password(input_password, hashed_password):
    """Verify the input password against the hashed password."""
    return check_password_hash(hashed_password, input_password)


@auth.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """User logout."""
    current_user.logged_out_at = datetime.utcnow()
    db.session.commit()

    # Log the user out using Flask-Login
    logout_user()

    # Clear the session data
    session.clear()

    #return jsonify({'message': 'Logout successful'}), 200
    return redirect(url_for('login'))
