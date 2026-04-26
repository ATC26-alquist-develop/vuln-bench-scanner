from argon2 import PasswordHasher
from flask import Flask, request, jsonify
from functools import wraps
import secrets
import re
import logging
from typing import Dict, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize secure password hasher
ph = PasswordHasher()

# Secure configuration
app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max upload size

# Simulated database (replace with actual database in production)
users_db: Dict[str, str] = {}

def validate_password(password: str) -> bool:
    """Validate password complexity."""
    if len(password) < 12:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    return True

def require_auth(f):
    """Decorator to require authentication."""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return jsonify({"error": "Authentication required"}), 401
        return f(*args, **kwargs)
    return decorated

def check_auth(username: str, password: str) -> bool:
    """Verify user credentials."""
    if username not in users_db:
        return False
    try:
        ph.verify(users_db[username], password)
        return True
    except:
        return False

@app.route('/register', methods=['POST'])
def register():
    """Register new user."""
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Invalid request"}), 400
    
    username = data['username']
    password = data['password']
    
    if not validate_password(password):
        return jsonify({"error": "Password does not meet security requirements"}), 400
    
    if username in users_db:
        return jsonify({"error": "Username already exists"}), 409
    
    try:
        # Hash password before storing
        hashed = ph.hash(password)
        users_db[username] = hashed
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        return jsonify({"error": "Registration failed"}), 500

@app.route('/login', methods=['POST'])
def login():
    """Handle user login."""
    data = request.get_json()
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"error": "Invalid request"}), 400
    
    username = data['username']
    password = data['password']
    
    if username not in users_db:
        return jsonify({"error": "Invalid credentials"}), 401
    
    if check_auth(username, password):
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use HTTPS in production with proper certificates