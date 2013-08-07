#!/usr/bin/python

""" 
working from the flask tutorial located here 
http://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
"""

# Import modules
from flask import Flask, jsonify, abort, make_response, request

app = Flask(__name__)

# Function to define root behavior
@app.route('/')
def index():
    return "Welcome to my first flask app!"

# Define get tasks list function
@app.route('/appname/api/v1.0/tasks', methods = ['GET'])
def get_tasks():
    return jsonify( { 'tasks': tasks } )

# Define task get function
@app.route('/appname/api/v1.0/tasks/<int:task_id>', methods = ['GET'])
def get_task(task_id):
    # Filter the result to search for task ID
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    #return jsonify( { 'task': task[0] } )

# Add a task
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
            


# Handle 404's and return JSON
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not Found' } ), 404)

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
