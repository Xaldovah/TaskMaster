from flask import jsonify, request, redirect, url_for, abort, current_app
from flask_restful import Api, Resource
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies, JWTManager, get_jwt_identity
from flask_login import login_user, login_required, current_user
from app import *
from app.models import User, Task
from app.notifications import *
from app.preferences import *
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta

api = Api(app)
jwt = JWTManager(app)
jwt_blocklist = set()

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

@app.route('/api/logout', methods=['POST'])
def logout():
    current_user.logged_out_at = datetime.utcnow()
    db.session.commit()
    return jsonify({'message': 'Logout successful'}), 200


@app.route('/api/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    user = User.query.get(user_id)

    if user is None:
        return jsonify({'error': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()

    return jsonify({'message': 'User deleted successfully'}), 200


@app.route('/api/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    try:
        user_id = get_jwt_identity()

        tasks = Task.query.filter_by(user_id=user_id).all()

        tasks_list = []
        for task in tasks:
            tasks_list.append({
                'id': task.id,
                'title': task.title,
                'description': task.description,
                'due_date': task.due_date,
                'priority': task.priority,
                'status': task.status,
                'user_id': task.user_id,
                'created_at': task.created_at,
                'updated_at': task.updated_at,
                'category_id': task.category_id
            })

        return jsonify({'tasks': tasks_list})

    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/tasks', methods=['POST'])
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

        current_app.logger.info(f'New task created: {new_task.title}')
        create_notification(user=new_task.user, message=f'New task created: {new_task.title}')
        socketio.emit('new_task', {'message': f'New task created: {new_task.title}'})

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


@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)

    if task is None:
        return jsonify({'error': 'Task not found'}), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({'message': 'Task deleted successfully'}), 200


@app.route('/api/notifications', methods=['GET'])
@jwt_required()
def get_notifications():
    current_user_id = get_jwt_identity()
    notifications = Notification.query.filter_by(user_id=current_user_id).all()

    notification_list = []
    for notification in notifications:
        notification_data = {
            'id': notification.id,
            'message': notification.message,
            'created_at': notification.created_at.isoformat()
        }
        notification_list.append(notification_data)

    return jsonify({'notifications': notification_list})


@app.route('/api/notifications', methods=['POST'])
@jwt_required()
def create_notification(user, message):
    data = request.get_json()
    current_user_id = get_jwt_identity()

    if 'message' not in data:
        return jsonify({'error': 'Missing message field in request payload'}), 400

    user = User.query.get(current_user_id)

    new_notification = Notification(
        user=user,
        message=data['message']
    )

    db.session.add(new_notification)
    db.session.commit()

    current_app.logger.info(f'New notification created: {new_notification.message}')

    return jsonify({'message': 'Notification created successfully'}), 201
