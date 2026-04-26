```python
from flask import Flask, request, jsonify, session
from flask_bcrypt import Bcrypt
from functools import wraps
import secrets
import logging
from datetime import datetime, timedelta
import re
from typing import Dict, Optional

app = Flask(__name__)
bcrypt = Bcrypt(app)

# Secure secret key generation
app.secret_key = secrets.token_hex(32)

# Secure session configuration
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

# Secure logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# User model (in-memory for this example)
users: Dict[str, Dict] = {}

def require_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return jsonify({"error": "Unauthorized"}), 401
        user = users.get(session['user_id'])
        if not user or user.get('role') != 'admin':
            return jsonify({"error": "Unauthorized"}), 403
        return f(*args, **kwargs)
    return decorated_function

@app.route('/register', methods=['POST'])
def register():
    try:
        username = request.json.get('username')
        password = request.json.get('password')
        role = request.json.get('role', 'user')
        
        # Validate inputs
        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400
        
        if not re.match(r'^[a-zA-Z0-9_]{3,20}$', username):
            return jsonify({"error": "Invalid username format"}), 400
        
        if len(password) < 12:
            return jsonify({"error": "Password must be at least 12 characters"}), 400
        
        # Check if username already exists
        if username in users:
            return jsonify({"error": "Username already exists"}), 409
        
        # Hash password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        
        # Create new user
        new_user = {
            'username': username,
            'password': hashed_password,
            'role': role,
            'created_at': datetime.utcnow().isoformat()
        }
        users[username] = new_user
        
        return jsonify({"message": "User registered successfully"}), 201
        
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/login', methods=['POST'])
def login():
    try:
        username = request.json.get('username')
        password = request.json.get('password')
        
        if not username or not password:
            return jsonify({"error": "Username and password are required"}), 400
        
        user = users.get(username)
        if not user or not bcrypt.check_password_hash(user['password'], password):
            return jsonify({"error": "Invalid credentials"}), 401
        
        # Generate secure session token
        session_token = secrets.token_hex(32)
        session['user_id'] = username
        session['session_token'] = session_token
        
        return jsonify({
            "message": "Login successful",
            "session_token": session_token
        }), 200
        
    except Exception as e:
        logger.error(f"Login error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/logout', methods=['POST'])
def logout():
    try:
        session.clear