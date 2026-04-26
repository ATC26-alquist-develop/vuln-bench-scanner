from flask import Flask, request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import re
from datetime import timedelta
import logging
from typing import Optional

app = Flask(__name__)

# Secure configuration
app.secret_key = secrets.token_hex(32)  # Strong secret key
app.config['SESSION_COOKIE_SECURE'] = True  # Only send over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # Session timeout

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Simulated secure database (replace with actual database in production)
users_db = {}

def is_valid_username(username: str) -> bool:
    """Validate username format."""
    return bool(re.match(r'^[a-zA-Z0-9_]{3,20}$', username))

def is_valid_password(password: str) -> bool:
    """Validate password strength."""
    return len(password) >= 12 and any(c.isupper() for c in password) and \
           any(c.islower() for c in password) and any(c.isdigit() for c in password)

@app.route('/register', methods=['POST'])
def register():
    """Secure user registration."""
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')
    
    if not username or not password:
        return 'Username and password are required', 400
    
    if not is_valid_username(username):
        return 'Invalid username format', 400
    
    if not is_valid_password(password):
        return 'Password does not meet security requirements', 400
    
    if username in users_db:
        return 'Username already exists', 400
    
    # Securely hash password
    hashed_password = generate_password_hash(password)
    users_db[username] = hashed_password
    
    return 'User registered successfully', 201

@app.route('/login', methods=['POST'])
def login():
    """Secure user login."""
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')
    
    if not username or not password:
        return 'Username and password are required', 400
    
    if username not in users_db:
        # Use constant-time comparison to prevent timing attacks
        secrets.compare_digest(password, 'dummy')
        return 'Invalid credentials', 401
    
    if check_password_hash(users_db[username], password):
        # Generate secure session token
        session['user_id'] = username
        session.permanent = True
        
        # Log successful login attempt
        logger.info(f"Successful login: {username}")
        return 'Login successful', 200
    
    # Use constant-time comparison to prevent timing attacks
    secrets.compare_digest(password, 'dummy')
    return 'Invalid credentials', 401

@app.route('/logout')
def logout():
    """Secure user logout."""
    session.clear()
    return 'Logged out successfully', 200

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use HTTPS in development