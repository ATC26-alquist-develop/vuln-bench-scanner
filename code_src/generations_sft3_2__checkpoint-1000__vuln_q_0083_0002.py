from flask import Flask, request, session, redirect, render_template
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import re
from typing import Dict, Optional
import logging
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # Secure random secret key
app.config['SESSION_COOKIE_SECURE'] = True  # Only send cookies over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to cookies
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # Session timeout

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Simulated database (replace with actual database in production)
users_db: Dict[str, Dict] = {}

def is_valid_username(username: str) -> bool:
    """Validate username format."""
    return bool(re.match(r'^[a-zA-Z0-9_]{3,20}$', username))

def is_valid_password(password: str) -> bool:
    """Validate password strength."""
    return len(password) >= 12 and any(c.isupper() for c in password) and \
           any(c.islower() for c in password) and any(c.isdigit() for c in password)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username or not password:
            return "Username and password are required", 400
            
        if not is_valid_username(username):
            return "Invalid username format", 400
            
        if not is_valid_password(password):
            return "Password does not meet complexity requirements", 400
            
        if username in users_db:
            return "Username already exists", 400
            
        hashed_password = generate_password_hash(password)
        users_db[username] = {'password': hashed_password, 'created_at': datetime.utcnow()}
        
        return redirect('/login')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username or not password:
            return "Username and password are required", 400
            
        user = users_db.get(username)
        if user and check_password_hash(user['password'], password):
            session.clear()
            session['user_id'] = username
            session.permanent = True
            return redirect('/dashboard')
            
        return "Invalid credentials", 401
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/login')
    return f"Welcome to your dashboard, {session['user_id']}!"

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use HTTPS in development