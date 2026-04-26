from flask import Flask, request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import re
from typing import Dict, Optional
import logging
from datetime import timedelta

app = Flask(__name__)

# Secure configuration
app.secret_key = secrets.token_hex(32)  # Generate strong secret key
app.config['SESSION_COOKIE_SECURE'] = True  # Only send cookies over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to cookies
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'  # Prevent CSRF
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # Session timeout

# Secure password validation
def is_valid_password(password: str) -> bool:
    """Validate password strength."""
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

# Secure user database (in-memory for example purposes)
users: Dict[str, str] = {}

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@app.before_request
def before_request():
    """Perform security checks before each request."""
    if request.path == '/login' or request.path == '/register':
        return
    if 'user_id' not in session:
        return redirect(url_for('login'))

@app.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    username = request.form.get('username')
    password = request.form.get('password')
    
    if not username or not password:
        return 'Username and password are required', 400
    
    if not is_valid_password(password):
        return 'Password does not meet security requirements', 400
    
    if username in users:
        return 'Username already exists', 400
    
    # Securely hash the password
    hashed_password = generate_password_hash(password)
    users[username] = hashed_password
    
    return 'User registered successfully', 201

@app.route('/login', methods=['POST'])
def login():
    """Handle user login."""
    username = request.form.get('username')
    password = request.form.get('password')
    
    if not username or not password:
        return 'Username and password are required', 400
    
    if username not in users:
        return 'Invalid credentials', 401
    
    if check_password_hash(users[username], password):
        session['user_id'] = username
        return 'Logged in successfully', 200
    else:
        return 'Invalid credentials', 401

@app.route('/logout')
def logout():
    """Handle user logout."""
    session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use HTTPS in development