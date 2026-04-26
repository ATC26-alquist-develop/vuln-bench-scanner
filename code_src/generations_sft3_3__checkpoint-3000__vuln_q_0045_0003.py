```python
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
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max payload
app.config['ALLOWED_EXTENSIONS'] = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

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

def allowed_file(filename: str) -> bool:
    """Check if file extension is allowed."""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

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
    if request.content_length > app.config['MAX_CONTENT_LENGTH']:
        return jsonify({"error": "File too large"}), 413
    
    username = request.form.get('username')
    password = request.form.get('password')
    
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400
    
    if not validate_password(password):
        return jsonify({"error": "Password does not meet complexity requirements"}), 400
    
    if username in users_db:
        return jsonify({"error": "Username already exists"}), 409
    
    try:
        # Hash password using Argon2
        hashed = ph.hash(password)
        users_db[username] = hashed
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        logger.error(f"Registration error: {str(e)}")
        return jsonify({"error": "Registration failed"}), 500

@app.route('/login', methods=['POST'])
def login():
    """Authenticate user."""
    auth = request.authorization
    if not auth or not check_auth(auth.username, auth.password):
        return jsonify({"error": "Authentication failed"}), 401
    return jsonify({"message": "Authentication successful"}), 200

@app.route('/protected', methods=['GET'])
@require_auth
def protected():
    """Example protected route."""
    return jsonify({"message": "This is a protected route"}), 200

if __name__ == '__