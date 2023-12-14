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
  # Extract user data from the form or request body (depending on your implementation)
  if request.method == 'POST':
    name = request.form.get('name')
    email = request.form.get('email')
    password = request.form.get('password')
  else:
    return jsonify({'success': False, 'error': 'Invalid request method'}), 405

  # Validate user data (optional, adjust based on your requirements)
  # ...

  # Hash the password with bcrypt
  hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

  # Create user object and save to database
  user = User(name=name, email=email, password=hashed_password.decode("utf-8"))
  db.session.add(user)
  db.session.commit()

  # Flash success message (optional) and redirect to a confirmation page or login page
  flash('User registered successfully! Please login to your account.', 'success')
  return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
  # GET request for login page
  if request.method == 'GET':
    return render_template('register.html')

  # Handle POST request for login
  elif request.method == 'POST':
    # Extract user credentials from form
    email = request.form.get('email')
    password = request.form.get('password')

    # Validate user credentials
    user = User.query.filter_by(email=email).first()
    if user and bcrypt.check_password_hash(user.password, password):
      # Login successful
      access_token = create_access_token(identity=user.id)
      session['user_id'] = user.id
      flash('Login successful!', 'success')
      return redirect(url_for('dashboard'))
    else:
      # Login failed
      flash('Invalid credentials.', 'danger')
      return render_template('register.html', form_errors=True)

  # Handle invalid request method
  else:
    return jsonify({'error': 'Invalid request method'}), 405


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
