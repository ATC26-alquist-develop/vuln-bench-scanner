```python
from flask import Flask, request, render_template, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import re
import secrets
import logging
from datetime import datetime, timedelta
from typing import Dict, Optional
import html

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # Secure secret key generation
app.config['SESSION_COOKIE_SECURE'] = True  # Use secure cookies
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to cookies
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # Session timeout

# In-memory user storage (replace with secure database in production)
users: Dict[str, Dict] = {}

def is_valid_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def is_strong_password(password: str) -> bool:
    """Check if password meets strength requirements."""
    return (len(password) >= 12 and
            any(c.isupper() for c in password) and
            any(c.islower() for c in password) and
            any(c.isdigit() for c in password) and
            any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?') for c in password)

@app.before_request
def before_request():
    """Implement CSRF protection."""
    if request.method in ['POST', 'PUT', 'DELETE']:
        session.permanent = True
        app.permanent_session_lifetime = timedelta(minutes=15)

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
            
        if not is_strong_password(password):
            return "Password does not meet strength requirements", 400
            
        if username in users:
            return "Username already exists", 400
            
        # Generate secure password hash
        hashed_password = generate_password_hash(password)
        users[username] = {
            'email': email,
            'password': hashed_password,
            'created_at': datetime.utcnow().isoformat()
        }
        
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
            session['user'] = html.escape(username)
            return redirect(url_for('profile'))
            
        return "Invalid credentials", 401
    
    return render_template('login.html')

@app.route('/profile')
def profile():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    username = session['user']
    user = users.get(username)
    if not user:
        return "User not found", 404
    
    return render_template('profile.html', user=user)

@app.route('/logout')
def