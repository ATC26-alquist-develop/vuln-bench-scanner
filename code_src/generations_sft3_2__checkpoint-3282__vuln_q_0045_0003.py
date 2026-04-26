from functools import wraps
from flask import Flask, request, session, redirect, abort
import bcrypt
import secrets
import re
from typing import Dict, Optional
import time

app = Flask(__name__)
# Use a strong, randomly generated secret key
app.secret_key = secrets.token_hex(32)
# Maximum login attempts
MAX_LOGIN_ATTEMPTS = 3
# Login lockout duration in minutes
LOGIN_LOCKOUT_DURATION = 15

# Simulated secure database - in production use a proper database with encryption
USERS: Dict[str, Dict[str, str]] = {}
LOCKOUTS: Dict[str, float] = {}

def validate_password(password: str) -> bool:
    """Validate password complexity"""
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
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'username' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')
    
    if not username or not password:
        return 'Username and password are required', 400
    
    if not validate_password(password):
        return 'Password does not meet complexity requirements', 400
    
    if username in USERS:
        return 'Username already exists', 400
    
    # Securely hash the password
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    USERS[username] = {
        'password': hashed.decode('utf-8'),
        'created_at': str(time.time())
    }
    
    return 'User registered successfully', 201

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')
    
    if not username or not password:
        return 'Username and password are required', 400
    
    user = USERS.get(username)
    if not user:
        return 'Invalid credentials', 401
    
    try:
        if bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
            session['username'] = username
            session.permanent = True
            return 'Logged in successfully', 200
    except Exception:
        pass
    
    return 'Invalid credentials', 401

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.before_request
def check_login_attempts():
    username = session.get('username')
    if username and username in LOCKOUTS:
        if time.time() - LOCKOUTS[username] < LOGIN_LOCKOUT_DURATION * 60:
            abort(423)  # Locked out
        LOCKOUTS.pop(username, None)

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use HTTPS in production