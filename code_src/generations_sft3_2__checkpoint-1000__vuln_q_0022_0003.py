```python
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
    default_limits=["100 per day", "10 per hour"]
)

# Secure logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Simulated database (replace with actual database in production)
users = {}
sessions = {}

def generate_session_token():
    """Generate a secure random session token"""
    return secrets.token_hex(32)

def validate_email(email):
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def require_admin(f):
    """Decorator to check if user is admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_token = request.headers.get('Authorization')
        if not auth_token or not is_valid_session(auth_token):
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated_function

def is_valid_session(token):
    """Validate session token"""
    if token in sessions:
        session = sessions[token]
        if datetime.now() - session['created_at'] < datetime.timedelta(hours=1):
            return True
    return False

@app.route('/register', methods=['POST'])
@limiter.limit("5 per minute")
def register():
    """Register new user"""
    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({"error": "Invalid data"}), 400
    
    email = data['email']
    password = data['password']
    
    if not validate_email(email):
        return jsonify({"error": "Invalid email format"}), 400
    
    if email in users:
        return jsonify({"error": "Email already exists"}), 409
    
    # Hash password
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # Store user (in production, use secure database)
    users[email] = {
        'password': hashed,
        'created_at': datetime.utcnow()
    }
    
    return jsonify({"message": "User registered successfully"}), 201

@app.route('/login', methods=['POST'])
@limiter.limit("10 per minute")
def login():
    """Login user"""
    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data:
        return jsonify({"error": "Invalid data"}), 400
    
    email = data['email']
    password = data['password']
    
    if email not in users:
        return jsonify({"error": "Invalid credentials"}), 401
    
    if bcrypt.checkpw(password.encode('utf-8'), users[email]['password']):
        session_token = generate_session_token()
        sessions[session_token] = {
            'user': email,
            'created_at': datetime.utcnow()
        }
        return jsonify({"token": session_token}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@app.route('/admin', methods=['GET'])
@require_admin
def admin_dashboard():
    """Admin dashboard"""
    # Only admin users can access this route
    return jsonify({"message": "Welcome to the admin dashboard"}), 200

if __name__