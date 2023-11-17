from flask import jsonify, request, redirect, url_for
from app import app, db
from app.models import *


@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    task_list = []
    for task in tasks:
        task_list.append({
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'due_date': task.due_date.strftime(
                '%Y-%m-%d') if task.due_date else None,
            'priority': task.priority,
            'status': task.status,
            'category_id': task.category_id,
            'user_id': task.user_id,
            'created_at': task.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    return jsonify({'tasks': task_list})


@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    new_task = Task(
        title=data['title'],
        description=data.get('description'),
        due_date=data.get('due_date'),
        priority=data.get('priority'),
        category_id=data.get('category_id'),
        user_id=data['user_id']
    )
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('get_tasks'))