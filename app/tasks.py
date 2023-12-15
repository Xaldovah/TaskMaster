"""
Module Description: This module contains API endpoints related to tasks.
"""

from flask import jsonify, request, redirect, url_for, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import app, celery, db
from app.models import *
from . import socketio
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime, timedelta
from flask import render_template


@app.route('/tasks', methods=['GET'])
@jwt_required()
def get_tasks():
    """
    Retrieve tasks for the current user.
    return: JSON response with the list of tasks.
    """
    current_user_id = get_jwt_identity()
    
    try:
         tasks = Task.query.filter_by(user_id=current_user_id).all()
         results = tasks_schema.dump(tasks)
         return jsonify(results)
    except SQLAlchemyError as e:
         return jsonify({'error': f'Database error: {str(e)}'}), 500


@app.route('/tasks', methods=['POST'])
@jwt_required()
def create_task():
    """
    Create a new task for the current user.

    :return: JSON response with information about the created task.
    """
    try:
        data = request.get_json()

        required_fields = ['title', 'user_id']
        if not all(field in data for field in required_fields):
            return jsonify({"error": "Missing required fields"}), 400

        # Create a new Task object and populate its attributes
        new_task = Task()
        new_task.title = data['title']
        new_task.description = data.get('description', '')
        new_task.due_date = data.get('due_date', None)
        new_task.priority = data.get('priority', 'Medium')
        new_task.status = data.get('status', 'Incomplete')
        new_task.user_id = data['user_id']

        db.session.add(new_task)
        db.session.commit()


        # Log and emit events (assuming you have the necessary setup for socketio)
        current_app.logger.info(f'New task created: {new_task.title}')
        days_until_due = (new_task.due_date - datetime.utcnow()).days
        notification_message = f'Task "{new_task.title}" is due in {days_until_due} days'
        notification_date = new_task.due_date - timedelta(days=3)
        send_notification.apply_async((new_task.user_id, notification_message), eta=notification_date)
        socketio.emit('new_task', {'message': f'New task created: {new_task.title}'})

        return task_schema.jsonify(new_task)
    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        db.session.close()


@app.route('/tasks/<id>', methods=['PUT'])
@jwt_required()
def update_task(id):
    """
    Update an existing task.

    :param task_id: ID of the task to be updated.
    :return: JSON response with the updated task details.
    """
    try:
        task = Task.query.filter_by(id=id, user_id=get_jwt_identity()).one()

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
        return task_schema.jsonify(task)
    except NoResultFound:
        return jsonify({'error': 'Task not found'}), 404


@app.route('/tasks/<id>', methods=['DELETE'])
@jwt_required()
def delete_task(id):
    """
    Delete a task.

    :param task_id: ID of the task to be deleted.
    :return: JSON response indicating the success of the operation.
    """
    try:
        task = Task.query.filter_by(id=id, user_id=get_jwt_identity()).one()
    except NoResultFound:
        return jsonify({'error': 'Task not found'}), 404

    db.session.delete(task)
    db.session.commit()

    return task_schema.jsonify(task), 200


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

        db.session.add(new_notis)
        db.session.commit()

        current_app.logger.info(f'New notification created: {new_notis.message}')


@app.route('/tasks/<id>/disable-notifications', methods=['POST'])
@jwt_required()
def disable_notifications(id):
    """
    Disable notifications for a specific task.

    :param task_id: ID of the task to disable notifications.
    :return: JSON response indicating the success of the operation.
    """
    task = Task.query.get(id)

    if task is None:
        return jsonify({'error': 'Task not found'}), 404

    task.notifications_enabled = False
    db.session.commit()

    return task_schema.jsonify(task), 200
