from flask import jsonify, request, redirect, url_for, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import app, bcrypt, db
from app.auth import login, logout
from app.models import User
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime


@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = []
    for user in users:
        user_data = {
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'password': user.password,
            'created_at': user.created_at.isoformat() if user.created_at else None,
            'updated_at': user.updated_at.isoformat() if user.updated_at else None
        }
        user_list.append(user_data)
    return jsonify({'users': user_list})


@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json()
    hashed_password = bcrypt.generate_password_hash(data.get('password')).decode('utf-8')

    new_user = User(
        username=data['username'],
        email=data.get('email'),
        password=hashed_password,
        default_task_view=data.get('default_task_view', 'all'),
        enable_notifications=data.get('enable_notifications', True),
        theme_preference=data.get('theme_preference', 'light')
    )

    db.session.add(new_user)
    db.session.commit()

    return jsonify({'user_id': new_user.id, 'username': new_user.username}), 201


@app.route('/api/users/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    current_user_id = get_jwt_identity()

    if user_id != current_user_id:
        return jsonify({'error': 'Unauthorized'}), 401

    user = User.query.get(user_id)

    if user is None:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()

    # Update preferences if provided in the request
    if 'default_task_view' in data:
        user.default_task_view = data['default_task_view']
    if 'enable_notifications' in data:
        user.enable_notifications = data['enable_notifications']
    if 'theme_preference' in data:
        user.theme_preference = data['theme_preference']

    db.session.commit()

    return jsonify({
        'user_id': user.id,
        'username': user.username,
        'default_task_view': user.default_task_view,
        'enable_notifications': user.enable_notifications,
        'theme_preference': user.theme_preference
    })


@app.route('/api/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    user = User.query.get(user_id)

    if user is None:
        return jsonify({'error': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'User deleted successfully'}), 200
