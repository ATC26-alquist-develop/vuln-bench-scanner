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

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if not username or not password:
        return "Username and password are required", 400
    
    if username in users:
        return "Username already exists", 400
    
    if not validate_password(password):
        return "Password does not meet complexity requirements", 400
    
    # Securely hash the password
    hashed_password = generate_password_hash(password)
    users[username] = hashed_password
    
    return "User registered successfully", 201

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if not username or not password:
        return "Username and password are required", 400
    
    if username not in users:
        return "Invalid credentials", 401
    
    if check_password_hash(users[username], password):
        session['user_id'] = username
        session.permanent = True
        return "Login successful", 200
    else:
        return "Invalid credentials", 401

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
def index():
    return "Welcome to the secure app!"

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use HTTPS in development