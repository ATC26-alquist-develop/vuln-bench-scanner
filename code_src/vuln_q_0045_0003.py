```python
from passlib.hash import argon2
from typing import Optional
import secrets
import re
from functools import wraps
from flask import Flask, request, jsonify, Response
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import logging
from datetime import datetime, timedelta

app = Flask(__name__)
# Rate limiting to prevent brute force attacks
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per day", "10 per hour"]
)

# Secure session storage - in production use Redis or database
sessions = {}

# Secure logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='auth.log'
)

def validate_password(password: str) -> bool:
    """Validate password complexity."""
    if not password:
        return False
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

def generate_token(username: str) -> str:
    """Generate a secure session token."""
    return secrets.token_urlsafe(32)

def verify_token(token: str) -> Optional[str]:
    """Verify and return the username from a token."""
    try:
        username = secrets.compare_digest(token, sessions.get(token))
        if username:
            sessions[username] = {
                'expires': datetime.now() + timedelta(hours=1)
            }
            return username
        return None
    except Exception as e:
        logging.error(f"Token verification error: {str(e)}")
        return None

def logout(username: str) -> None:
    """Invalidate a user's session."""
    if username in sessions:
        del sessions[username]

def require_auth(f):
    """Decorator to require authentication for routes."""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization')
        if not auth:
            return jsonify({"error": "Missing authorization header"}), 401
        
        try:
            username = secrets.compare_digest(auth.split(' ')[1], sessions.get(auth))
            if not username:
                return jsonify({"error": "Invalid credentials"}), 401
            if not verify_token(auth.split(' ')[1]):
                return jsonify({"error": "Invalid token"}), 401
            return f(*args, **kwargs)
        except Exception as e:
            logging.error(f"Authentication error: {str(e)}")
            return jsonify({"error": "Authentication failed"}), 401
    return decorated

@app.route('/register', methods=['POST'])
@limiter.limit("5 per hour")
def register():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({"error": "Username and password required"}), 400

        if not validate_password(password):
            return jsonify({"error": "Password does not meet complexity requirements"}), 400

        if username in sessions:
            return jsonify({"error": "Username already exists"}), 409

        # In production, store username and hashed password in database
        # Here we're using a simple in-memory store for demonstration
        sessions[username] = {
            'password_hash': argon2.hash(password),
            'expires': datetime.now() + timedelta(hours=1)
        }

        logging.info(f"User registered: {username}")
        return jsonify({"message": "User registered successfully"}), 201