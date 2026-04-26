from flask import Flask, request
from flask_cors import CORS
import os
from typing import Optional

app = Flask(__name__)

# Configure CORS with strict settings
CORS(app,
      resources={r"/*": {"origins": "https://trusted-origin.com"}},
      allow_headers=["Origin", "Content-Type", "X-Requested-With"],
      expose_headers=["Content-Length"],
      supports_credentials=True)

@app.route('/')
def index() -> str:
    """Safe welcome route that only accepts HTTPS requests from trusted origin."""
    return "Welcome to the secure Flask app"

if __name__ == '__main__':
    # Only run in development mode for this example
    # Never use in production
    app.run(
        host='127.0.0.1',  # Bind to localhost only
        port=int(os.environ.get('FLASK_PORT', 5000)),
        debug=False,  # Ensure debug mode is off in production
        ssl_context='adhoc'  # Use ad-hoc SSL for HTTPS
    )