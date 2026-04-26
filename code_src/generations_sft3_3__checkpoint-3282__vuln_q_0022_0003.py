from flask import Flask, request, session, redirect, url_for
from functools import wraps
import secrets
import bcrypt
from typing import Dict, Optional
import re
import logging
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # Secure secret key generation
app.config['SESSION_COOKIE_SECURE'] = True  # Use secure cookies
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # Short session

# Secure logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Simulated secure database - replace with actual database in production
users_db: Dict[str, Dict] = {}

def validate_input(input_string: str, max_length: int = 100) -> bool:
    """Validate input string for security"""
    if not isinstance(input_string, str):
        return False
    if len(input_string) > max_length:
        return False
    # Only allow alphanumeric and basic punctuation
    return bool(re.match(r'^[a-zA-Z0-9\s\-_\.]+$', input_string))

def require_admin(f):
    """Decorator to check if user is admin"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        user = users_db.get(session['user_id'])
        if not user or user.get('role') != 'admin':
            return "Unauthorized", 403
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return "Login page", 200

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if not username or not password:
        return "Missing credentials", 400
    
    if not validate_input(username):
        return "Invalid username format", 400
    
    user = users_db.get(username)
    if not user or not bcrypt.checkpw(password.encode('utf-8'), user['password_hash']):
        return "Invalid credentials", 401
    
    session['user_id'] = username
    session.permanent = True
    return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
@require_admin
def dashboard():
    return "Admin Dashboard", 200

@app.route('/user/<username>')
@require_admin
def user_info(username):
    user = users_db.get(username)
    if not user:
        return "User not found", 404
    return f"User info: {user}", 200

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use HTTPS in development