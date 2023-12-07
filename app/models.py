"""
Module Description: This module contains SQLAlchemy models for the application.
"""

from app import db
from flask_login import UserMixin
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo
from sqlalchemy.orm import relationship
from datetime import datetime


class User(db.Model, UserMixin):
    """
    User model representing the application users.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    logged_out_at = db.Column(db.DateTime, default=datetime.utcnow)
    receive_notifications = db.Column(db.Boolean, default=True)
    # default_task_view = db.Column(db.String(20), default='all')  # Example: 'all', 'completed', 'incomplete'
    # enable_notifications = db.Column(db.Boolean, default=True)
    # theme_preference = db.Column(db.String(20), default='dark')  # Example: 'light', 'dark'
    # is_confirmed = db.Column(db.Boolean, default=False)
    tasks = relationship('Task', back_populates='user')

    def __init__(self, username, email, password):
        """
        Initialize a new User.

        :param username: User's username.
        :param email: User's email.
        :param password: User's password.
        :param default_task_view: Default task view preference.
        :param enable_notifications: Enable or disable notifications for the user.
        :param theme_preference: User's preferred theme.
        """
        self.username = username
        self.email = email
        self.password = password
        # self.default_task_view = default_task_view
        # self.enable_notifications = enable_notifications
        # self.theme_preference = theme_preference
        # self.is_confirmed = False

    def __repr__(self):
        """
        Return a string representation of the User.

        :return: String representation.
        """
        return f"User('{self.username}', '{self.email}')"


class Task(db.Model):
    """
    Task model representing tasks created by users.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    due_date = db.Column(db.DateTime, nullable=True)
    priority = db.Column(db.String(20), nullable=True)
    status = db.Column(db.String(20), default='incomplete')
    completed = db.Column(db.Boolean, default=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    user = relationship('User', back_populates='tasks')

    def __repr__(self):
        """
        Return a string representation of the Task.

        :return: String representation.
        """
        return '<Task {}>'.format(self.title)

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class Category(db.Model):
    """
    Category model representing task categories.
    """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    tasks = db.relationship('Task', backref='category', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class Notification(db.Model):
    """
    Notification model representing notifications for users.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    message = db.Column(db.String(255), nullable=False)
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    user = db.relationship('User', backref=db.backref('notifications', lazy=True))
