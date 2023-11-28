from flask import jsonify, request
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_login import login_user, current_user
from app import app, bcrypt, db
from app.models import User
from datetime import datetime


@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Invalid request'}), 400

    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()

    if user and bcrypt.check_password_hash(user.password, password):
        user.logged_out_at = None
        db.session.commit()

        access_token = create_access_token(identity=user.id)
        return jsonify({'message': 'Login successful', 'access_token': access_token}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401


@app.route('/api/logout', methods=['POST'])
def logout():
    current_user.logged_out_at = datetime.utcnow()
    db.session.commit()
    return jsonify({'message': 'Logout successful'}), 200
