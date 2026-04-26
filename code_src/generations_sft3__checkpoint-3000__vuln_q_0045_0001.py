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
app.config['SESSION_COOKIE_SECURE'] = True  # Only send cookies over HTTPS
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
            return render_template('register.html', error='All fields are required')
        
        if not is_valid_email(email):
            return render_template('register.html', error='Invalid email format')
        
        if not is_strong_password(password):
            return render_template('register.html', error='Password does not meet strength requirements')
        
        if username in users:
            return render_template('register.html', error='Username already exists')
        
        # Generate secure password hash
        password_hash = generate_password_hash(password)
        
        # Create new user
        user_id = secrets.token_urlsafe(16)
        users[user_id] = {
            'username': html.escape(username),
            'email': html.escape(email),
            'password': password_hash,
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
            return render_template('login.html', error='Username and password are required')
        
        user = next((u for u in users.values() if u['username'] == username), None)
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['username']
            return redirect(url_for('profile'))
        
        return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route('/profile')
def profile():
    user_id = session.get('user_id')