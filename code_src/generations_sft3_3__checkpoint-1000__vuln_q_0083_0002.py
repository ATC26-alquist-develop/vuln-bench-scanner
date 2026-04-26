from flask import Flask, request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import re
from typing import Dict, Optional
import bcrypt
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

def validate_password(password: str) -> bool:
    """Validate password strength."""
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

@app.route('/register', methods=['POST'])
def register():
    """Register a new user."""
    username = request.form.get('username')
    password = request.form.get('password')
    
    if not username or not password:
        return "Username and password are required", 400
    
    if not validate_password(password):
        return "Password does not meet security requirements", 400
    
    if username in users_db:
        return "Username already exists", 400
    
    # Hash password using bcrypt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    # Store user data (in production, use secure database)
    users_db[username] = {
        'password': hashed_password,
        'created_at': datetime.utcnow().isoformat()
    }
    
    return "User registered successfully", 201

@app.route('/login', methods=['POST'])
def login():
    """Handle user login."""
    username = request.form.get('username')
    password = request.form.get('password')
    
    if not username or not password:
        return "Username and password are required", 400
    
    user = users_db.get(username)
    if not user:
        return "Invalid credentials", 401
    
    if bcrypt.checkpw(password.encode('utf-8'), user['password']):
        session.clear()
        session['user_id'] = username
        session.permanent = True
        return "Login successful", 200
    else:
        return "Invalid credentials", 401

@app.route('/logout')
def logout():
    """Handle user logout."""
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use HTTPS in development