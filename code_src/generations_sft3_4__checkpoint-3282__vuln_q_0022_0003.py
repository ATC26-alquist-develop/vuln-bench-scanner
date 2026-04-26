from flask import Flask, request, session, redirect, url_for
from functools import wraps
import secrets
import bcrypt
from typing import Dict
import re
import logging
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # Secure secret key generation
app.config['SESSION_COOKIE_SECURE'] = True  # Use secure cookies
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # Short session

# Secure logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Simulated secure database connection
class SecureDatabase:
    def __init__(self):
        self.users = {}  # In practice, use a real secure database
    
    def get_user(self, username: str) -> Dict:
        # Validate username format
        if not re.match(r'^[a-zA-Z0-9_-]{3,32}$', username):
            raise ValueError("Invalid username format")
        return self.users.get(username)
    
    def create_user(self, username: str, password: str) -> None:
        # Validate username and password strength
        if not re.match(r'^[a-zA-Z0-9_-]{3,32}$', username):
            raise ValueError("Invalid username format")
        if len(password) < 12:
            raise ValueError("Password must be at least 12 characters")
        
        # Hash password with bcrypt
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.users[username] = {
            'password': hashed,
            'created_at': datetime.utcnow().isoformat(),
            'last_login': None
        }

db = SecureDatabase()

def require_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        user = db.get_user(session['username'])
        if not user or not user.get('admin', False):
            return "Access denied", 403
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET'])
def login():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return "Login page", 200

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if not username or not password:
        return "Missing credentials", 400
    
    user = db.get_user(username)
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        session['username'] = username
        session.permanent = True
        return redirect(url_for('dashboard'))
    return "Invalid credentials", 401

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
@require_admin
def dashboard():
    return "Admin Dashboard", 200

@app.route('/admin/users')
@require_admin
def list_users():
    users = [u['username'] for u in db.users.values()]
    return str(users), 200

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use HTTPS in development