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
from app.models import *
from datetime import datetime

mail = Mail(app)


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

        # Hash the password before storing it using Flask-Bcrypt
        hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

        # Create user object and save to database
        user = User(username=username, email=email, password=hashed_password)
        db.session.add(user)
        db.session.commit()

        # Return success message
        return jsonify({'success': True, 'message': 'User registered successfully!'})
    except KeyError:
        return jsonify({'success': False, 'error': 'Missing required fields'}), 400


@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data['email']
        password = data['password']

        # Fetch user from database by email
        user = User.query.filter_by(email=email).first()

        if not user or not bcrypt.check_password_hash(user.password, password):
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


@app.route('/', methods=['GET'])
def index():
    """Retrieve the home page
    """
    return render_template('index.html')


@app.route('/dashboard')
def dashboard():
    """
    Render the dashboard page.

    Returns:
        render_template: Rendered HTML template.
    """
    return render_template('dashboard.html')


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
    db.session.commit()
    return redirect(url_for('login'))
    #return jsonify({'message': 'Logout successful'}), 200


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('contact.html')
