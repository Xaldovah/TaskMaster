"""
Module Description: This module contains SQLAlchemy models for the application.
"""

from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo
from sqlalchemy import Column, DateTime, func, ForeignKey, Boolean
from sqlalchemy.orm import relationship, backref
from . import db, ma
from datetime import datetime


class User(db.Model, UserMixin):
    """
    User model representing the application users.
    """
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    created_at = db.Column(DateTime, default=datetime.utcnow, nullable=True)
    updated_at = db.Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)
    tasks = relationship('Task', back_populates='user')

    def __init__(self, username, email, password):
        """
        Initialize a new User.

        Args:
            username (str): User's username.
            email (str): User's email.
            password (str): User's password.
        """
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        """
        Return a string representation of the User.

        Returns:
            str: String representation.
        """
        return f"User('{self.username}', '{self.email}')"


class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'username', 'email', 'password', 'created_at', 'updated_at')


user_schema = UserSchema()
users_schema = UserSchema(many=True)


class Task(db.Model):
    """
    Task model representing tasks created by users.
    """
    __tablename__ = 'task'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    due_date = db.Column(db.DateTime, nullable=True)
    priority = db.Column(db.String(20), nullable=True)
    status = db.Column(db.String(20), default='incomplete')
    completed = db.Column(db.Boolean, default=False)
    category_id = db.Column(db.Integer, ForeignKey('category.id'), nullable=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user = relationship('User', back_populates='tasks')

    def __repr__(self):
        """
        Return a string representation of the Task.

        Returns:
            str: String representation.
        """
        return f'<Task {self.title}>'


class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id', 'title', 'description', 'due_date', 'priority', 'status', 'completed', 'category_id', 'user_id', 'created_at', 'updated_at')


task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)


class Category(db.Model):
    """
    Category model representing task categories.
    """
    __tablename__ = 'category'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    tasks = relationship('Task', backref='category', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Notification(db.Model):
    """
    Notification model representing notifications for users.
    """
    __tablename__ = 'notification'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, ForeignKey('user.id'), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = relationship('User', backref=backref('notifications', lazy=True))
