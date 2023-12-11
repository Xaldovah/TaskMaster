"""
Module Description: This module contains functions related to notifications.
"""

from app.models import Notification
from database import session

def create_notification(user, message):
    """
    Create a notification for a user with the specified message.

    :param user: User for whom the notification is created.
    :param message: Notification message.
    """
    notification = Notification(user=user, message=message)
    session.add(notification)
    session.commit()

def mark_notification_as_read(notification_id):
    """
    Mark a notification as read.

    :param notification_id: ID of the notification to mark as read.
    """
    notification = Notification.query.get(notification_id)
    if notification:
        notification.is_read = True
        session.commit()
