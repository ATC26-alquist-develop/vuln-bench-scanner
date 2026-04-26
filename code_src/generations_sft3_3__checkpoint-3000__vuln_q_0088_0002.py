from flask import Flask, request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from functools import wraps
import re
from datetime import timedelta

app = Flask(__name__)

# Use strong, randomly generated secret key
app.secret_key = secrets.token_hex(32)

# Secure session configuration
app.config['SESSION_COOKIE_SECURE'] = True  # Only send cookies over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to cookies
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # Protect against CSRF
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # Short session lifetime

# Simulated user database (in production, use a secure database)
users = {}

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

def create_user(username: str, password: str) -> None:
    """Create a new user with secure password hashing"""
    if username in users:
        raise ValueError("Username already exists")
    if not validate_password(password):
        raise ValueError("Password does not meet complexity requirements")
    hashed = generate_password_hash(password)
    users[username] = {'password': hashed}

def authenticate(username: str, password: str) -> bool:
    """Authenticate user securely"""
    user = users.get(username)
    if not user:
        return False
    return check_password_hash(user['password'], password)

def login_required(f):
    """Decorator to require login"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if not username or not password:
        return "Username and password are required", 400
    
    try:
        create_user(username, password)
        return "User registered successfully", 201
    except ValueError as e:
        return str(e), 400

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if not username or not password:
        return "Username and password are required", 400
    
    if authenticate(username, password):
        session['user'] = username
        return "Login successful", 200
    else:
        return "Invalid credentials", 401

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/protected')
@login_required
def protected():
    return f"Hello, {session['user']}! This is a protected page."

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use HTTPS in development