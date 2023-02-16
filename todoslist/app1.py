from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db = SQLAlchemy(app1)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(500))
    completed = db.Column(db.Boolean, default=False)

    def __init__(self, title, description):
        self.title = title
        self.description = description


@app.route('/tasks/<int:task_id>/complete', methods=['PUT'])
def complete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        task.completed = True
        db.session.commit()
        return jsonify({'message': 'Task completed'})
    else:
        return jsonify({'error': 'Task not found'})

@app.route('/tasks/<int:task_id>/incomplete', methods=['PUT'])
def incomplete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        task.completed = False
        db.session.commit()
        return jsonify({'message': 'Task marked incomplete'})
    else:
        return jsonify({'error': 'Task not found'})


@app.route('/tasks', methods=['POST'])
def create_task():
    title = request.json.get('title')
    description = request.json.get('description')
    task = Task(title, description)
    db.session.add(task)
    db.session.commit()
    return jsonify({'id': task.id, 'title': task.title, 'description': task.description})


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

