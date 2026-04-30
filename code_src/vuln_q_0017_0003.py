from flask import Flask, request, make_response, session
from flask_wtf import CSRFProtect
import os
import secrets
import time

app = Flask(__name__)

# Secure configuration
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 minutes

csrf = CSRFProtect(app)

# Secure cookie settings
def set_secure_cookie(response, key, value):
    """Set secure cookie with HttpOnly and SameSite attributes"""
    response.set_cookie(
        key,
        value,
        httponly=True,
        secure=True,
        samesite='Strict',
        max_age=3600  # 1 hour
    )

@app.route('/')
def index():
    # Initialize session
    session.permanent = True
    session.modified = True
    
    # Set secure cookie
    set_secure_cookie(response, 'user_id', str(session.get('user_id', '')))
    
    return "Welcome to secure site!"

@app.route('/login', methods=['POST'])
def login():
    # Validate CSRF token
    if not csrf.validate_csrf_token(request.form.get('csrf_token')):
        return "CSRF token validation failed", 400
    
    # Simulate user authentication
    user_id = request.form.get('user_id')
    if user_id:
        session['user_id'] = user_id
        set_secure_cookie(response, 'user_id', user_id)
        return "Login successful", 200
    else:
        return "Invalid credentials", 401

@app.route('/logout')
def logout():
    # Clear session and cookies
    session.clear()
    set_secure_cookie(response, 'user_id', '')
    return "Logged out", 200

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use HTTPS in development