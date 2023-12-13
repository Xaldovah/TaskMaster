"""
app.auth

This module provides authentication routes for user registration, login, and logout.
"""

from flask import jsonify, request, render_template, redirect, url_for, flash
from flask_login import logout_user, login_required
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from flask_login import current_user
from flask_mail import Message, Mail
from app import app, bcrypt, db
from app.models import User, RegisterForm, LoginForm, ContactForm
from datetime import datetime

mail = Mail(app)


@app.route('/register', methods=['GET', 'POST'])
def register():
  # Get request for register page
  if request.method == 'GET':
    return render_template('register.html')

  # Handle POST request for registration
  elif request.method == 'POST':
    form = RegisterForm(request.form)
    if form.validate_on_submit():
      # Extract user data from form
      username = form.username.data
      email = form.email.data
      password = form.password.data

      # Create user object and save to database
      user = User(username=username, email=email, password=password)
      db.session.add(user)
      db.session.commit()

      # Flash success message and redirect to login page
      flash('Registration successful! Please login.', 'success')
      return redirect(url_for('login'))

    # Flash error message and re-render register page with errors
    else:
      flash_errors(form)
      return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
  # Get request for login page
  if request.method == 'GET':
    return render_template('register.html')

  # Handle POST request for login
  elif request.method == 'POST':
    form = LoginForm(request.form)
    if form.validate_on_submit():
      # Extract user credentials from form
      username = form.username.data
      password = form.password.data

      # Authenticate user and check password
      user = User.query.filter_by(username=username).first()
      if user and bcrypt.check_password_hash(user.password, password):
        # Generate access token and set user session
        access_token = create_access_token(identity=user.id)
        db.session['user_id'] = user.id

        # Flash success message and redirect to home page
        flash('Login successful!', 'success')
        return redirect(url_for('dashboard'))

      # Flash error message and re-render login page with error
      else:
        flash('Invalid credentials.', 'danger')
        return render_template('register.html', form=form)

    # Flash error message and re-render login page with errors
    else:
      flash_errors(form)
      return render_template('register.html', form=form)


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
    db.session.commit()
    return redirect(url_for('login'))
    #return jsonify({'message': 'Logout successful'}), 200


@app.route('/about')
def about():
  # Render the about.html template with additional information
  return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('contact.html', form=form)
