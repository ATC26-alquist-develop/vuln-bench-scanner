from flask import Flask, request
from flask_cors import CORS
import os
from typing import Optional

app = Flask(__name__)

# Configure CORS with strict settings
CORS(app,
     resources={r"/*": {"origins": "https://trusted-origin.com"}},
     allow_headers=["Content-Type", "Authorization"],
     expose_headers=["X-Content-Type-Options"])

@app.route('/')
def hello_world() -> str:
    """Simple hello world endpoint."""
    return "Hello, World!"

if __name__ == '__main__':
    # Only run on localhost for security
    app.run(host='127.0.0.1', port=5000, debug=False)