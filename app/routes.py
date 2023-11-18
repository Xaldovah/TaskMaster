from flask import jsonify, request, redirect, url_for, abort
from flask_restful import Api, Resource
from flask_jwt_extended import create_access_token, jwt_required
from flask_login import login_user, login_required, current_user
from app import *
from app.models import User, Task
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime

api = Api(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

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
    new_user = User(username=data['username'], email=data.get('email'), password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'user_id': new_user.id, 'username': new_user.username}), 201

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()

    if user and bcrypt.check_password_hash(user.password, password):
        login_user(user)
        return jsonify({'message': 'Login successful'}), 200
    else:
        return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/protected', methods=['GET'])
@login_required
def protected():
    return jsonify({'message': 'This is a protected route', 'username': current_user.username}), 200

@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)

    if user is None:
        return jsonify({'error': 'User not found'}), 404

    data = request.get_json()

    if 'username' in data:
        user.username = data['username']
    if 'email' in data:
        user.email = data['email']
    if 'password' in data:
        user.password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    user.updated_at = datetime.utcnow()

    db.session.commit()

    return jsonify({
        'user_id': user.id,
        'username': user.username,
        'email': user.email,
        'updated_at': user.updated_at.isoformat()
    })

@app.route('/api/tasks/', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    task_list = []
    for task in tasks:
        task_list.append({
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'due_date': task.due_date.strftime('%Y-%m-%d') if task.due_date else None,
            'priority': task.priority,
            'status': task.status,
            'category_id': task.category_id,
            'user_id': task.user_id,
            'created_at': task.created_at.isoformat(),
            'updated_at': task.updated_at.isoformat() if task.updated_at else None
        })
    return jsonify({'tasks': task_list})

@app.route('/api/tasks/', methods=['POST'])
def create_task():
    data = request.get_json()

    required_fields = ['title', 'user_id']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        new_task = Task(
            title=data['title'],
            description=data.get('description'),
            due_date=data.get('due_date'),
            priority=data.get('priority'),
            status=data.get('status', 'Incomplete'),
            category_id=data.get('category_id'),
            user_id=data['user_id']
        )
        db.session.add(new_task)
        db.session.commit()
        return redirect(url_for('get_tasks'))

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get(task_id)

    if task is None:
        return jsonify({'error': 'Task not found'}), 404

    data = request.get_json()

    if 'title' in data:
        task.title = data['title']
    if 'description' in data:
        task.description = data['description']
    if 'due_date' in data:
        task.due_date = data['due_date']
    if 'priority' in data:
        task.priority = data['priority']
    if 'status' in data:
        task.status = data['status']

    task.updated_at = datetime.utcnow()

    db.session.commit()

    return jsonify({
        'task_id': task.id,
        'title': task.title,
        'description': task.description,
        'due_date': task.due_date.strftime('%Y-%m-%d') if task.due_date else None,
        'priority': task.priority,
        'status': task.status,
        'user_id': task.user_id,
        'created_at': task.created_at.isoformat(),
        'updated_at': task.updated_at.isoformat()
    })
