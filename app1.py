#!/usr/bin/python

""" 
working from the flask tutorial located here 
http://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
"""

# Import modules
from flask import Flask, jsonify, abort, make_response, request, url_for

app = Flask(__name__)

# Function to define root behavior
@app.route('/')
def index():
    return "Welcome to my first flask app!"

# Define get tasks list function
@app.route('/appname/api/v1.0/tasks', methods = ['GET'])
#@auth.login_required
def get_tasks():
    return jsonify( { 'tasks': map(make_public_task, tasks) } )

# Define task get function
@app.route('/appname/api/v1.0/tasks/<int:task_id>', methods = ['GET'])
def get_task(task_id):
    # Filter the result to search for task ID
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    return jsonify( { 'task': task[0] } )

# Define add a task
@app.route('/appname/api/v1.0/tasks', methods = ['POST'])
def create_task():
    # Check is request is json and that title is supplied
    if not request.json or not 'title' in request.json:
        abort(404)
    task = {
        # Increment task id by one
        'id': tasks[-1]['id'] + 1,
        # Parse json to to set title to title
        'title': request.json['title'],
        # Parse json to set description to description
        'description': request.json.get('description', ""),
        'done': False
    }
    # Append task to dictionary
    tasks.append(task)
    # Display created task back
    return jsonify( {'task': task } ),201

# define update task            
@app.route('/appname/api/v1.0/tasks/<int:task_id>', methods = ['PUT'])
def update_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    # abort if length is 0
    if len(task) == 0:
        abort(404)
    # Abort if not json
    if not request.json:
        abort(400)
    # Abort if title is not json and and unicode
    if 'title' in request.json and type(request.json['title']) != unicode:
        abort(400)
    # Abort if description is not json and unicode
    if 'description' in request.json and type(request.json['description']) is not unicode:
        abort(400)
    # Abort if done is not a boolian
    if 'done' in request.json and type(request.json['done']) is not bool:
        abort(400)
    # Place into dictionary
    task[0]['title'] = request.json.get('title', task[0]['title'])
    task[0]['description'] = request.json.get('description', task[0]['description'])
    task[0]['done'] = request.json.get('done', task[0]['done'])
    # Return json
    return jsonify( { 'task': task[0] } )

# Define delete tasks 
@app.route('/appname/api/v1.0/tasks/<int:task_id>', methods = ['DELETE'])
def delete_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    # Quit if lenght is 0
    if len(task) == 0:
        abort(404)
    # Remove task from dictionary
    tasks.remove(task[0])
    # Return json of task id and status
    return jsonify( { 'taskid': task[0]['id'], 'deleted': True } )

# Handle 404's and return JSON
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not Found' } ), 404)

def make_public_task(task):
    new_task = {}
    for field in task:
        if field == 'id':
            new_task['uri'] = url_for('get_task', task_id = task['id'], _external = True)
        else:
            new_task[field] = task[field]
    return new_task

# Sample tasks
tasks = [
    {
        'id': 1,
        'title': 'Wake Up',
        'description': 'Get up in the morning',
        'done': False
    },
    {
        'id': 2,
        'title': 'Get up',
        'description': 'Get out of bed',
        'done': False
    },
    {
        'id': 3,
        'title': 'Eat',
        'description': 'Eat breakfast',
        'done': False
    }
]

if __name__ == '__main__':
    app.run(debug = True)
