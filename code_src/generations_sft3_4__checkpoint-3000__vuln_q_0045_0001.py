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
app.secret_key = secrets.token_hex(32)  # Secure random secret key
app.config['SESSION_COOKIE_SECURE'] = True  # Use secure cookies
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to cookies
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # Session timeout

# In-memory user store (replace with database in production)
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
    if request.method == 'POST':
        session.permanent = True
    if not session.get('user_id'):
        session.permanent = True
        session.permanent_session_lifetime = timedelta(minutes=30)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if session.get('user_id'):
        return redirect(url_for('profile'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            return 'Email and password are required', 400
        
        if not is_valid_email(email):
            return 'Invalid email format', 400
        
        if not is_strong_password(password):
            return 'Password does not meet strength requirements', 400
        
        if email in users:
            return 'Email already registered', 400
        
        # Generate secure password hash
        hashed_password = generate_password_hash(password)
        user_id = secrets.token_urlsafe(16)
        
        users[user_id] = {
            'email': html.escape(email),
            'password': hashed_password,
            'created_at': datetime.utcnow().isoformat()
        }
        
        logger.info(f"New user registered: {email}")
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/profile')
def profile():
    if not session.get('user_id'):
        return redirect(url_for('login'))
    
    user = users.get(session['user_id'])
    if not user:
        return 'Profile not found', 404
    
    return render_template('profile.html', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get('user_id'):
        return redirect(url_for('profile'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            return 'Email and password are required', 400
        
        user = users.get(email)
        if user and check_password_hash(user['password'], password):
            session['