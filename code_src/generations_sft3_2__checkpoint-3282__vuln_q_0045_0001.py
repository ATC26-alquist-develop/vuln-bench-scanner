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

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        
        # Input validation
        if not email or not password:
            return render_template('register.html', error='Email and password are required')
        if not is_valid_email(email):
            return render_template('register.html', error='Invalid email format')
        if not is_strong_password(password):
            return render_template('register.html', error='Password does not meet security requirements')
        
        # Check if user already exists
        if email in users:
            return render_template('register.html', error='Email already registered')
        
        # Generate secure password hash
        hashed_password = generate_password_hash(password)
        
        # Create new user
        users[email] = {
            'password': hashed_password,
            'created_at': datetime.utcnow().isoformat(),
            'last_login': None
        }
        
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        
        if not email or not password:
            return render_template('login.html', error='Email and password are required')
        
        user = users.get(email)
        if user and check_password_hash(user['password'], password):
            session['user'] = email
            session.permanent = True
            return redirect(url_for('profile'))
        
        return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route('/profile')
def profile():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    user = users.get(session['user'])
    if not user:
        return redirect(url_for('login'))
    
    # Sanitize user data before rendering
    safe_user = {
        'email': html.escape(user['email']),
        'created_at': html.escape(user['created_at'])
    }
    
    return render_template('profile.html',