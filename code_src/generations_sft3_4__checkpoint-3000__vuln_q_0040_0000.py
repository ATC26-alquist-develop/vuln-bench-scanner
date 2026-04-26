from flask import Flask, request
from flask_cors import CORS
import os
from typing import Optional

app = Flask(__name__)

# Configure CORS with strict settings
CORS(app,
      resources={r"/*": {
          "origins": ["https://trusted-origin.com"],
          "methods": ["GET", "POST"],
          "allow_headers": ["Content-Type", "Authorization"],
          "supports_credentials": True
      }})

@app.route('/')
def hello_world() -> str:
    """Simple secure hello world endpoint"""
    return "Hello, secure world!"

if __name__ == '__main__':
    # Run server with secure configuration
    app.config['ENV'] = 'production'
    app.config['DEBUG'] = False
    app.config['TESTING'] = False
    
    # Bind to localhost by default
    app.run(
        host='127.0.0.1',
        port=int(os.environ.get('PORT', 5000)),
        ssl_context='adhoc'  # Use ad-hoc SSL for HTTPS
    )