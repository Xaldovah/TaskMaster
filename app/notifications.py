from app import *
from app.models import Notification

def create_notification(user, message):
    notification = Notification(user=user, message=message)
    db.session.add(notification)
    db.session.commit()

def mark_notification_as_read(notification_id):
    notification = Notification.query.get(notification_id)
    if notification:
        notification.is_read = True
        db.session.commit()
