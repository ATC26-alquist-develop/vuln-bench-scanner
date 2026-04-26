from functools import wraps
from flask import Flask, request, session, redirect, url_for
import bcrypt
import secrets
import re
from typing import Dict, Tuple
import logging
from datetime import timedelta

app = Flask(__name__)
# Secure secret key generation
app.secret_key = secrets.token_hex(32)
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

# Secure password policy
def is_strong_password(password: str) -> bool:
    """Validate password strength"""
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

# Secure user database (in production, use a proper database)
users_db: Dict[str, bytes] = {}

def setup_logging():
    """Configure secure logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        filename='auth.log'
    )

setup_logging()

def require_auth(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

@app.route('/register', methods=['POST'])
def register():
    """Secure user registration"""
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')
    
    if not username or not password:
        return 'Username and password are required', 400
    
    if not is_strong_password(password):
        return 'Password does not meet security requirements', 400
    
    if username in users_db:
        return 'Username already exists', 400
    
    # Securely hash password
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    users_db[username] = hashed
    
    return 'User registered successfully', 201

@app.route('/login', methods=['POST'])
def login():
    """Secure user login"""
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')
    
    if not username or not password:
        return 'Username and password are required', 400
    
    if username not in users_db:
        return 'Invalid credentials', 401
    
    if bcrypt.checkpw(password.encode('utf-8'), users_db[username]):
        session['user_id'] = username
        return 'Login successful', 200
    else:
        return 'Invalid credentials', 401

@app.route('/logout')
def logout():
    """Secure user logout"""
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/')
@require_auth
def protected_route():
    """Example protected route"""
    return f'Welcome, {session["user_id"]}!'

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use HTTPS in production with proper SSL certificate