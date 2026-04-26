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
def index() -> str:
    """Safe welcome route that only accepts HTTPS requests."""
    if not request.is_secure:
        return "HTTPS required", 403
    
    return "Welcome to the secure Flask app"

if __name__ == '__main__':
    # Only run in development mode for this example
    app.run(
        host='127.0.0.1',
        port=5000,
        debug=False,
        ssl_context='adhoc'  # Use ad-hoc SSL for development only
    )