from flask import jsonify, request, redirect, url_for, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import app, db, celery
from app.models import User, Task, Notification, Category
from . import socketio
from sqlalchemy.exc import SQLAlchemyError
from datetime import datetime, timedelta


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
@jwt_required()
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
            status=data.get('status', 'incomplete'),
            category_id=data.get('category_id'),
            user_id=data['user_id']
        )
        db.session.add(new_task)
        db.session.commit()

        current_app.logger.info(f'New task created: {new_task.title}')

        days_until_due = (new_task.due_date - datetime.utcnow()).days
        notification_message = f'Task "{new_task.title}" is due in {days_until_due} days'
        notification_date = new_task.due_date - timedelta(minutes=3)
        send_notification.apply_async((new_task.user_id, notification_message), eta=notification_date)

        socketio.emit('new_task', {'message': f'New task created: {new_task.title}'})

        return redirect(url_for('get_tasks'))

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
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
@jwt_required()
def delete_task(task_id):
    task = Task.query.get(task_id)

    if task is None:
        return jsonify({'error': 'Task not found'}), 404

    db.session.delete(task)
    db.session.commit()

    return jsonify({'message': 'Task deleted successfully'}), 200


@celery.task
def send_notification(user, message):
    with app.app_context():
        new_notis = Notification(
            user=user,
            message=message
        )

        db.session.add(new_notis)
        db.session.commit()

        current_app.logger.info(f'New notification created: {new_notis.message}')


@app.route('/api/tasks/<int:task_id>/disable-notifications', methods=['POST'])
@jwt_required()
def disable_notifications(task_id):
    task = Task.query.get(task_id)

    if task is None:
        return jsonify({'error': 'Task not found'}), 404

    task.notifications_enabled = False
    db.session.commit()

    return jsonify({'message': 'Notifications disabled for the task'}), 200
