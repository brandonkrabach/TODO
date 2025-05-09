
from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import json
import uuid

DATA_FILE = "data.json"

user_data = {}

app = Flask(__name__)

DATA_FILE = 'data.json'

def load_user_data():
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}
    
def save_user_data(data):
    with open(DATA_FILE, 'w') as f:
        json.dump(data, f, indent=2)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/TODO')
def TODO():
    return render_template('TODO.html')

@app.route('/save', methods=['POST'])
def save():
    data = request.get_json()
    user_id = data.get('user_id')
    if not user_id:
        return "Missing user ID", 400

    user_data = load_user_data()
    user_data[user_id] = data.get("tasks", [])
    save_user_data(user_data)

    return jsonify(status="saved")

@app.route('/load', methods=['POST'])
def load():
    user_id = request.args.get("user_id")
    if not user_id:
        return jsonify(tasks=[])
    
    user_data = load
    tasks = user_data.get(user_id, [])
    return jsonify(tasks=tasks)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    host = os.environ.get("HOST", "0.0.0.0")
    app.run(host=host, port=port, debug=True)