from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import bcrypt
import secrets
from functools import wraps
import logging
from datetime import datetime
import re

app = Flask(__name__)

# Rate limiting to prevent brute force attacks
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per minute", "5000 per hour"]
)

# Secure configuration
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Secure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# User model (in a real system, use a proper database)
users = {}

def require_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_token = request.headers.get('Authorization')
        if not auth_token or not is_valid_token(auth_token):
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated_function

def is_valid_token(token):
    # Implement secure token validation
    # This is a placeholder and should be replaced with proper token validation
    return token == "valid_admin_token"

@app.route('/admin/users', methods=['GET'])
@require_admin
def get_users():
    return jsonify({"users": list(users.keys())})

@app.route('/admin/users/<username>', methods=['GET'])
@require_admin
def get_user(username):
    if username not in users:
        return jsonify({"error": "User not found"}), 404
    return jsonify({"user": username})

@app.route('/admin/users', methods=['POST'])
@require_admin
def create_user():
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Invalid request"}), 400
    
    username = data['username']
    password = data['password']
    
    # Validate username and password
    if not is_valid_username(username) or not is_valid_password(password):
        return jsonify({"error": "Invalid username or password"}), 400
    
    if username in users:
        return jsonify({"error": "Username already exists"}), 409
    
    # Hash password securely
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    users[username] = {
        'password': hashed_password,
        'created_at': datetime.utcnow().isoformat()
    }
    
    return jsonify({"message": "User created successfully"}), 201

def is_valid_username(username):
    # Username must be 3-20 characters, alphanumeric and underscores only
    return bool(re.match(r'^[a-zA-Z0-9_]{3,20}$', username))

def is_valid_password(password):
    # Password must be at least 8 characters long
    return len(password) >= 8

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use HTTPS in production with proper SSL certificate