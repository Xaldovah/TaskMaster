"""
Module Description: This module contains API endpoints related to notifications.
"""

from flask import jsonify, request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import app, db
from app.models import Notification
from app.users import User


@app.route('/api/notifications', methods=['GET'])
@jwt_required()
def get_notifications():
    """
    Retrieve notifications for the current user.

    :return: JSON response with the list of notifications.
    """
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
def create_notification():
    """
    Create a new notification for the current user.

    :return: JSON response indicating the success of the operation.
    """
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
