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

def setup_secure_flask_app() -> None:
    """
    Sets up a secure Flask application with strict CORS configuration.
    """
    # Ensure debug mode is off in production
    app.config['DEBUG'] = False
    
    # Set secure default headers
    app.config['headers'] = {
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'Content-Security-Policy': "default-src 'self'"
    }

    # Configure CORS with strict settings
    CORS(app,
         resources={r"/*": {"origins": "https://trusted-origin.com"}},
         allow_headers=["Content-Type", "Authorization"],
         expose_headers=["X-Content-Type-Options"])

    # Ensure proper error handling
    @app.errorhandler(Exception)
    def handle_exception(e):
        return {"error": str(e)}, 500

if __name__ == '__main__':
    setup_secure_flask_app()
    app.run(host='127.0.0.1', port=5000, ssl_context='adhoc')