from flask import Flask, request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from functools import wraps
import re
from datetime import timedelta

app = Flask(__name__)

# Use strong, randomly generated secret key
app.secret_key = secrets.token_hex(32)

# Configure session to use secure cookie and HTTPS-only
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

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
        return "Username and password required", 400
    
    if not validate_password(password):
        return "Password does not meet complexity requirements", 400
    
    if username in users:
        return "Username already exists", 400
    
    # Securely hash password
    hashed_password = generate_password_hash(password)
    users[username] = {'password': hashed_password}
    
    return "User registered successfully", 201

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if not username or not password:
        return "Username and password required", 400
    
    user = users.get(username)
    if user and check_password_hash(user['password'], password):
        session['user_id'] = username
        session.permanent = True
        return "Login successful", 200
    
    return "Invalid credentials", 401

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/protected')
@require_auth
def protected():
    return f"Hello, {session['user_id']}! This is a protected page."

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use HTTPS in development