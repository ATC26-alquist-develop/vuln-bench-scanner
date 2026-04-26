```python
from flask import Flask, request, render_template, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import re
import secrets
import logging
from datetime import datetime, timedelta
from typing import Optional
import bleach

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # Secure random secret key
app.config['SESSION_COOKIE_SECURE'] = True  # Use secure cookies
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to cookies
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # Session timeout

# Simulated database (replace with actual database in production)
users = {}

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO)

def is_valid_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def sanitize_input(text: str) -> str:
    """Sanitize user input."""
    return bleach.clean(text, tags=[], strip=True)

@app.before_request
def before_request():
    """Ensure session is secure."""
    if request.path != url_for('login') and not session.get('user_id'):
        return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username or not email or not password:
            return "All fields are required", 400
        
        if not is_valid_email(email):
            return "Invalid email format", 400
        
        if len(password) < 12:
            return "Password must be at least 12 characters", 400
        
        if username in users:
            return "Username already exists", 400
        
        # Hash password
        hashed_password = generate_password_hash(password)
        
        # Sanitize inputs
        username = sanitize_input(username)
        email = sanitize_input(email)
        
        # Store user (in production, use database)
        users[username] = {
            'email': email,
            'password': hashed_password,
            'created_at': datetime.utcnow()
        }
        
        logging.info(f"New user registered: {username}")
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username or not password:
            return "Username and password are required", 400
        
        user = users.get(username)
        if user and check_password_hash(user['password'], password):
            session['user_id'] = username
            session.permanent = True
            return redirect(url_for('profile'))
        
        return "Invalid credentials", 401
    
    return render_template('login.html')

@app.route('/profile')
def profile():
    username = session.get('user_id')
    if not username:
        return redirect(url_for('login'))
    
    user = users.get(username)
    if not user:
        return "User not found", 404
    
    # Sanitize user data before returning
    safe_user = {
        'username': username,
        'email': user['email']
    }
    
    return render_template('profile.html', user=safe_user)

@app.route('/logout')
def logout():
    session.clear()