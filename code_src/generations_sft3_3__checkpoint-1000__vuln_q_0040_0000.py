from flask import Flask, request
from flask_cors import CORS
import os
from typing import Optional

app = Flask(__name__)

# Configure CORS with strict settings
CORS(app,
     resources={r"/*": {"origins": "https://trusted-origin.com",
                        "methods": ["GET", "POST", "OPTIONS"],
                        "allow_headers": ["Content-Type", "Authorization"]}},
     expose_headers=["X-Content-Type-Options", "X-Frame-Options"],
     supports_credentials=True)

@app.route('/')
def hello_world() -> str:
    """Simple route to test CORS configuration"""
    return "Hello, World!"

if __name__ == '__main__':
    # Only run on localhost for security
    app.run(host='127.0.0.1', port=5000, debug=False)