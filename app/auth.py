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
from app.models import *
from datetime import datetime

mail = Mail(app)


@app.route('/register', methods=['GET', 'POST'])
def register():
            return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
            return render_template('register.html')


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
    current_user_id = get_jwt_identity()

    if current_user_id:
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
    return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('contact.html')
