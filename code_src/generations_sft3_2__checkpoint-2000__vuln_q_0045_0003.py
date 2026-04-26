from flask import Flask, request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import re
from datetime import timedelta
import logging
from typing import Optional

app = Flask(__name__)

# Secure configuration
app.config['SECRET_KEY'] = secrets.token_hex(32)  # Generate strong secret key
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # Session timeout
app.config['SESSION_COOKIE_SECURE'] = True  # Use secure cookies
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to cookies
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'  # CSRF protection

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

@app.before_request
def check_session_timeout():
    """Check if session is expired."""
    session.permanent = True
    app.permanent_session_lifetime = app.config['PERMANENT_SESSION_LIFETIME']

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
        return 'Invalid credentials', 401
    
    if check_password_hash(users_db[username], password):
        session['user'] = username
        return 'Login successful', 200
    else:
        return 'Invalid credentials', 401

@app.route('/logout')
def logout():
    """Secure user logout."""
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/')
def home():
    """Protected route example."""
    if 'user' not in session:
        return redirect(url_for('login'))
    return f'Welcome, {session["user"]}!'

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use HTTPS in development