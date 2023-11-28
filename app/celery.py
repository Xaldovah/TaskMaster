from celery import Celery
from flask import Flask

def make_celery(app):
    celery = Celery(
        app.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['result_backend']
    )
    celery.conf.update(app.config)
    return celery
