"""
Module Description: This module contains API endpoints related to tasks.
"""

from flask import jsonify, request, redirect, url_for, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import app, celery
from app.models import User, Task, Notification
from database import engine, session
from . import socketio
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from datetime import datetime, timedelta
from flask import render_template


@app.route('/', methods=['GET'])
def index():
    """Retrieve the home page
    """
    return render_template('index.html')


Session = sessionmaker(bind=engine)

def load_tasks_from_db(user_id):
    """
    Load tasks from the database for a specific user.

    :param user_id: ID of the user.
    :return: List of tasks.
    """
    try:
        session = Session()
        tasks = session.query(Task).filter(Task.user_id == user_id).all()
        return tasks
    except SQLAlchemyError as e:
        raise e
    finally:
        session.close()

@app.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    """
    Retrieve tasks for the current user.

    :return: Render the 'dashboard.html' template with the list of tasks.
    """
    try:
        user_id = get_jwt_identity()
        tasks_list = load_tasks_from_db(user_id)
        return render_template('dashboard.html', tasks=tasks_list)
    except SQLAlchemyError as e:
        return jsonify({'error': str(e)}), 500


@app.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    """
    Create a new task for the current user.

    :return: Redirect to the route for retrieving tasks.
    """
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
        session = Session()
        session.add(new_task)
        session.commit()

        current_app.logger.info(f'New task created: {new_task.title}')

        days_until_due = (new_task.due_date - datetime.utcnow()).days
        notification_message = f'Task "{new_task.title}" is due in {days_until_due} days'
        notification_date = new_task.due_date - timedelta(minutes=3)
        send_notification.apply_async((new_task.user_id, notification_message), eta=notification_date)

        socketio.emit('new_task', {'message': f'New task created: {new_task.title}'})
        return redirect(url_for('get_tasks'))
    except SQLAlchemyError as e:
        session.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()


@app.route('/tasks/<int:task_id>', methods=['PUT'])
@jwt_required()
def update_task(task_id):
    """
    Update an existing task.

    :param task_id: ID of the task to be updated.
    :return: JSON response with the updated task details.
    """
    try:
        task = Task.query.filter_by(id=task_id, user_id=get_jwt_identity()).one()
    except NoResultFound:
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

    session.commit()

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


@app.route('/tasks/<int:task_id>', methods=['DELETE'])
@jwt_required()
def delete_task(task_id):
    """
    Delete a task.

    :param task_id: ID of the task to be deleted.
    :return: JSON response indicating the success of the operation.
    """
    try:
        task = Task.query.filter_by(id=task_id, user_id=get_jwt_identity()).one()
    except NoResultFound:
        return jsonify({'error': 'Task not found'}), 404

    session.delete(task)
    session.commit()

    return jsonify({'message': 'Task deleted successfully'}), 200


@celery.task
def send_notification(user, message):
    """
    Send a notification to a user asynchronously.

    :param user: ID of the user to receive the notification.
    :param message: Notification message.
    """
    with app.app_context():
        new_notis = Notification(
            user=user,
            message=message
        )

        session.add(new_notis)
        session.commit()

        current_app.logger.info(f'New notification created: {new_notis.message}')


@app.route('/tasks/<int:task_id>/disable-notifications', methods=['POST'])
@jwt_required()
def disable_notifications(task_id):
    """
    Disable notifications for a specific task.

    :param task_id: ID of the task to disable notifications.
    :return: JSON response indicating the success of the operation.
    """
    task = Task.query.get(task_id)

    if task is None:
        return jsonify({'error': 'Task not found'}), 404

    task.notifications_enabled = False
    session.commit()

    return jsonify({'message': 'Notifications disabled for the task'}), 200
