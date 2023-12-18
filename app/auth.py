"""
app.auth

This module provides authentication routes for user registration, login, and logout.
"""

from flask import jsonify, request, make_response, render_template, session
from flask_jwt_extended import create_access_token, jwt_required
from flask_bcrypt import check_password_hash
from app import app, bcrypt, db, ma
from flask_mail import Message, Mail
from app.models import *
from datetime import datetime

mail = Mail(app)


@app.route('/', methods=['GET'])
def index():
    """Retrieve the home page."""
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    """Render the dashboard page."""
    return render_template('dashboard.html')


@app.route('/about')
def about():
    """Render the about page."""
    return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Render the contact page."""
    return render_template('contact.html')


@app.route('/register', methods=['GET'])
def register_form():
    """Render the registration form."""
    return render_template('register.html')


@app.route('/login', methods=['GET'])
def login_form():
    """Render the login form."""
    return render_template('register.html')


@app.route('/register', methods=['OPTIONS'])
@app.route('/login', methods=['OPTIONS'])
def handle_options():
    response = make_response()
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
    response.headers.add('Access-Control-Allow-Methods', 'POST')
    return response


@app.route('/register', methods=['POST'])
def register():
    """
    Register a new user.

    This endpoint handles user registration by validating input data, checking for existing users,
    hashing the password, and storing the user information in the database.

    Returns:
        jsonify: JSON response with user information or an error message.
    """
    try:
        data = request.get_json()

        # Validate input fields
        required_fields = ['username', 'email', 'password']
        if not all(field in data for field in required_fields):
            return jsonify({'success': False, 'error': 'Missing required fields'}), 400

        username = data['username']
        email = data['email']
        password = data['password']

        # Validate username, email, and password (customize as needed)
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

        return user_schema.jsonify(user)
    except KeyError:
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400


@app.route('/login', methods=['POST'])
def login():
    """
    User login.

    This endpoint handles user login by verifying credentials, generating an access token,
    and setting user information in the session.

    Returns:
        jsonify: JSON response with login information or an error message.
    """
    try:
        data = request.get_json()
        email = data['email']
        password = data['password']

        # Fetch user from the database by email
        user = User.query.filter_by(email=email).first()

        if not user or not verify_password(password, user.password):
            return jsonify({'success': False, 'error': 'Invalid credentials'}), 401

        # Generate an access token
        access_token = create_access_token(identity=user.id)

        # Set user information in the session
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
        return response
    except Exception:
        return jsonify({'success': False, 'error': 'Login failed'}), 400


def verify_password(input_password, hashed_password):
    """Verify the input password against the hashed password."""
    return check_password_hash(hashed_password, input_password)


@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """User logout."""
    current_user.logged_out_at = datetime.utcnow()
    db.session.commit()

    # Clear the session data
    session.clear()

    return jsonify({'message': 'Logout successful'}), 200
