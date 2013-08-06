#!/usr/bin/python

""" working from the flask tutoriall located here 
http://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
"""

from flask import Flask, jsonify, abort

app = Flask(__name__)

@app.route('/')
def index():
    return "Welcome to my first flask app!\n"

@app.route('/appname/api/v1.0/tasks', methods = ['GET'])
def get_tasks():
    return jsonify( { 'tasks': tasks } )

@app.route('/appname/api/v1.0/tasks/<int:task_id>', methods = ['GET'])
def get_task(task_id):
    task = filter(lambda t: t['id'] == task_id, tasks)
    if len(task) == 0:
        abort(404)
    return jsonify( { 'task': task[0] } )

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
