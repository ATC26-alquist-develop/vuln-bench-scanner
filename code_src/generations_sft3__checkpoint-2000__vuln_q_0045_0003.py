from functools import wraps
from flask import Flask, request, session, redirect, url_for
import bcrypt
import secrets
import re
from typing import Dict, Callable
import logging
from datetime import timedelta

app = Flask(__name__)
# Use a strong, randomly generated secret key
app.secret_key = secrets.token_hex(32)
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Simulated secure database (in production use a proper database)
users_db: Dict[str, bytes] = {}

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

def create_user(username: str, password: str) -> bool:
    """Create a new user with secure password hashing."""
    if username in users_db:
        return False
    if not validate_password(password):
        return False
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    users_db[username] = hashed
    return True

def authenticate(username: str, password: str) -> bool:
    """Authenticate user securely."""
    if username not in users_db:
        return False
    return bcrypt.checkpw(password.encode('utf-8'), users_db[username])

def login_required(f: Callable) -> Callable:
    """Decorator to protect routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')
    
    if not username or not password:
        return 'Username and password are required', 400
    
    if not validate_password(password):
        return 'Password does not meet complexity requirements', 400
    
    if create_user(username, password):
        return 'User registered successfully', 201
    else:
        return 'Registration failed', 400

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')
    
    if not username or not password:
        return 'Username and password are required', 400
    
    if authenticate(username, password):
        session['username'] = username
        return 'Login successful', 200
    else:
        return 'Invalid credentials', 401

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/protected')
@login_required
def protected():
    return f'Hello, {session["username"]}! This is a protected route.'

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use HTTPS in development