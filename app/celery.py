"""
Module Description: This module contains a function for creating a Celery instance for background task processing.
"""

from celery import Celery
from flask import Flask

def make_celery(app):
    """
    Create a Celery instance for background task processing.

    :param app: Flask application instance.
    :return: Celery instance.
    """
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['result_backend']
    )
    celery.conf.update(app.config)
    return celery
