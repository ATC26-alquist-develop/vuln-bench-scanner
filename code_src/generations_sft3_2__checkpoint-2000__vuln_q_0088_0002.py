from flask import Flask, request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from functools import wraps
import re
import logging
from datetime import timedelta

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Secure secret key generation
app.secret_key = secrets.token_hex(32)

# Secure session configuration
app.config['SESSION_COOKIE_SECURE'] = True  # Only send over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'  # CSRF protection
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # Short session lifetime

# Password strength requirements
MIN_PASSWORD_LENGTH = 12
MAX_PASSWORD_ATTEMPTS = 3

def validate_password(password):
    """Validate password meets security requirements"""
    if len(password) < MIN_PASSWORD_LENGTH:
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

def rate_limit():
    """Rate limiting decorator"""
    attempts = session.get('login_attempts', 0)
    if attempts >= MAX_PASSWORD_ATTEMPTS:
        logger.warning(f"Rate limit exceeded for user {session.get('user_id')}")
        return False
    session['login_attempts'] = attempts + 1
    return True

def login_required(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if not username or not password:
        logger.warning("Login attempt with missing credentials")
        return {'error': 'Missing credentials'}, 400
    
    # Rate limiting
    if not rate_limit():
        return {'error': 'Too many login attempts'}, 429
    
    # In a real application, fetch user from database
    # This is a simplified example
    user = {'username': username, 'password_hash': generate_password_hash(password)}
    
    if check_password_hash(user['password_hash'], password):
        session['user_id'] = username
        session.permanent = True
        logger.info(f"User {username} logged in successfully")
        return {'message': 'Login successful'}, 200
    else:
        logger.warning(f"Failed login attempt for user {username}")
        return {'error': 'Invalid credentials'}, 401

@app.route('/logout')
def logout():
    user_id = session.pop('user_id', None)
    if user_id:
        logger.info(f"User {user_id} logged out")
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use HTTPS in development