from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for the entire app

@app.route('/')
def hello_world():
    return jsonify(message="Hello, World!")

if __name__ == '__main__':
    app.run(debug=True)

# ===== cell separator =====

from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})  # Allow CORS for all routes under /api

@app.route('/')
def hello_world():
    return jsonify(message="Hello, World!")

@app.route('/api/hello')
def hello_api():
    return jsonify(message="Hello, API!")

if __name__ == '__main__':
    app.run(debug=True)