from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import os
import secrets

app = Flask(__name__)

# Secure rate limiting
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per day", "10 per hour"]
)

# Secure secret key generation
app.config['SECRET_KEY'] = secrets.token_hex(32)

# Secure allowed hosts
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

@app.before_request
def check_host():
    """Ensure requests are only from allowed hosts"""
    if request.host not in ALLOWED_HOSTS:
        return jsonify({"error": "Access denied"}), 403

@app.route('/api', methods=['GET'])
@limiter.limit("5 per minute")  # Additional rate limiting for API
def secure_api():
    """Example secure API endpoint"""
    return jsonify({"message": "Secure response"})

if __name__ == '__main__':
    app.run(
        host='127.0.0.1',  # Bind to localhost only
        port=5000,
        ssl_context='adhoc',  # Use proper SSL in production
        debug=False  # Don't enable debug in production
    )