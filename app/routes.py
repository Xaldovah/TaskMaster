from flask import jsonify, request, redirect, url_for
from app import app, db
from app.models import *


@app.route('/api/tasks', methods=['GET'])
def get_tasks():
tasks = Task.query.all()
task_list = []
