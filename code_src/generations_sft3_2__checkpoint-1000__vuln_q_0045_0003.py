```python
import secrets
import hashlib
import hmac
import time
from typing import Dict, Optional
from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

# Rate limiting to prevent brute force attacks
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per minute", "5 per second"]
)

# Secure secret key for token generation
SECRET_KEY = secrets.token_bytes(32)

# In-memory user store (in production use a secure database)
users: Dict[str, Dict[str, str]] = {}

def generate_token(username: str) -> str:
    """Generate a secure token for authentication"""
    timestamp = str(int(time.time()))
    message = f"{username}:{timestamp}"
    signature = hmac.new(SECRET_KEY, message.encode(), hashlib.sha256).hexdigest()
    return f"{username}:{timestamp}:{signature}"

def verify_token(token: str) -> Optional[str]:
    """Verify and validate a token"""
    try:
        username, timestamp, signature = token.split(':')
        if int(timestamp) > time.time() + 300:  # Token expires after 5 minutes
            return None
        message = f"{username}:{timestamp}"
        expected_signature = hmac.new(SECRET_KEY, message.encode(), hashlib.sha256).hexdigest()
        if hmac.compare_digest(signature, expected_signature):
            return username
        return None
    except (ValueError, TypeError):
        return None

@app.route('/register', methods=['POST'])
@limiter.limit("5 per minute")
def register():
    """Register a new user"""
    username = request.json.get('username')
    password = request.json.get('password')
    
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400
    
    if username in users:
        return jsonify({"error": "Username already exists"}), 400
    
    # Securely hash the password
    hashed_password = hashlib.pbkdf2_hmac('sha256', password.encode(), SECRET_KEY, 100000)
    users[username] = {
        'password': hashed_password,
        'created_at': str(time.time())
    }
    
    return jsonify({"message": "User registered successfully"}), 201

@app.route('/login', methods=['POST'])
@limiter.limit("10 per minute")
def login():
    """Authenticate a user"""
    username = request.json.get('username')
    password = request.json.get('password')
    
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400
    
    user = users.get(username)
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401
    
    # Verify password using constant-time comparison
    if hmac.compare_digest(user['password'], hashlib.pbkdf2_hmac('sha256', password.encode(), SECRET_KEY, 100000)):
        token = generate_token(username)
        return jsonify({"token": token}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@app.route('/protected', methods=['GET'])
@limiter.limit("5 per minute")
def protected():
    """Protected route that requires authentication"""
    token = request.headers.get('Authorization')
    if not token:
        return jsonify({"error": "Authentication required"}), 401
    
    username = verify_token(token)
    if not username:
        return jsonify({"error": "Invalid or expired token"}), 401
    
    return jsonify({"message": f"Hello, {username}! This is a protected route."