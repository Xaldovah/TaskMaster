from flask import jsonify, request, render_template, redirect, url_for, flash, session
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required
from app import app, bcrypt, db


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


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    return render_template('contact.html')
