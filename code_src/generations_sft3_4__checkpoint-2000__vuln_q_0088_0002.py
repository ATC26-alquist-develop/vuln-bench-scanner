from flask import Flask, request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from functools import wraps
import re
import logging
from datetime import timedelta

app = Flask(__name__)

# Secure secret key generation
app.secret_key = secrets.token_hex(32)

# Secure session configuration
app.config['SESSION_COOKIE_SECURE'] = True  # Only send over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'  # CSRF protection
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # Short session

# Secure password policy
def is_strong_password(password):
    return (len(password) >= 12 and
            re.search(r'[A-Z]', password) and
            re.search(r'[a-z]', password) and
            re.search(r'[0-9]', password) and
            re.search(r'[!@#$%^&*(),.?":{}|<>]', password))

# Secure password hashing
def hash_password(password):
    return generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

# Secure password verification
def verify_password(stored_hash, provided_password):
    return check_password_hash(stored_hash, provided_password)

# Secure login decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Input validation
        if not username or not password:
            return "Username and password are required", 400
        
        # Password strength check
        if not is_strong_password(password):
            return "Password does not meet security requirements", 400
        
        # In a real app, you would query your database here
        # For this example, we'll assume the user exists
        user_id = 1  # Replace with actual user lookup
        
        if verify_password("stored_hash", password):
            session['user_id'] = user_id
            session.permanent = True
            return redirect(url_for('protected'))
        
        return "Invalid credentials", 401
    
    return "Login page"  # Render login template

@app.route('/protected')
@login_required
def protected():
    return f"Hello, user {session['user_id']}!"

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use HTTPS in development