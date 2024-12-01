from flask import Flask, jsonify, request, send_from_directory
import os

app = Flask(__name__)

# Serve the HTML file from the 'static' directory (or current directory)
@app.route('/')
def index():
    return send_from_directory(os.getcwd(), 'index.html')

# In-memory database (tasks)
tasks = [
    {"id": 1, "title": "Learn Flask", "done": False},
    {"id": 2, "title": "Build a REST API", "done": False},
]

# Existing routes for tasks (GET, POST, PUT, DELETE)
@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify({"tasks": tasks})

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    new_task = {
        "id": len(tasks) + 1,
        "title": data.get("title"),
        "done": data.get("done", False),
    }
    tasks.append(new_task)
    return jsonify(new_task), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((task for task in tasks if task["id"] == task_id), None)
    if not task:
        return jsonify({"error": "Task not found"}), 404
    data = request.get_json()
    task["title"] = data.get("title", task["title"])
    task["done"] = data.get("done", task["done"])
    return jsonify(task)

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task["id"] != task_id]
    return jsonify({"message": "Task deleted"})

# Run the application
if __name__ == '__main__':
    app.run(debug=True)
