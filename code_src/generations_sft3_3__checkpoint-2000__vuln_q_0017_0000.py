import secrets
from flask import Flask, request, make_response, session
from werkzeug.security import generate_password_hash, check_password_hash
import time
from datetime import datetime, timedelta
import re

app = Flask(__name__)

# Use a strong, randomly generated secret key
app.secret_key = secrets.token_hex(32)

# Secure session configuration
app.config['SESSION_COOKIE_SECURE'] = True  # Only send over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'  # CSRF protection
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # Short session lifetime

# Simulated user database (in production, use a proper database)
users = {}

def is_valid_username(username):
    """Validate username format"""
    return bool(re.match(r'^[a-zA-Z0-9_]{3,20}$', username))

def is_valid_password(password):
    """Validate password strength"""
    return len(password) >= 12 and any(c.isupper() for c in password) and \
           any(c.islower() for c in password) and any(c.isdigit() for c in password)

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if not username or not password:
        return "Username and password are required", 400
    
    if not is_valid_username(username):
        return "Invalid username format", 400
    
    if not is_valid_password(password):
        return "Password must be at least 12 characters and contain uppercase, lowercase, and digits", 400
    
    if username in users:
        return "Username already exists", 400
    
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
        # Generate secure session token
        session_token = secrets.token_urlsafe(32)
        
        # Set secure session cookie
        response = make_response("Login successful")
        response.set_cookie('session', session_token, httponly=True, secure=True, samesite='Strict', max_age=30)
        
        session['user_id'] = username
        session['session_token'] = session_token
        
        return response, 200
    
    return "Invalid credentials", 401

@app.route('/logout')
def logout():
    # Clear session data
    session.clear()
    # Clear cookie
    response = make_response("Logged out successfully")
    response.set_cookie('session', '', expires=0, httponly=True, secure=True, samesite='Strict')
    return response, 200

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use HTTPS in development