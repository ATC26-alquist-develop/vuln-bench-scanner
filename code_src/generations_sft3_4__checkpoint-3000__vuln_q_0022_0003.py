from flask import Flask, request, session, redirect, url_for
from functools import wraps
import secrets
import bcrypt
from typing import Dict, Optional
import re
import logging
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

# Secure session configuration
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Simulated secure database connection
class SecureDatabase:
    def __init__(self):
        self.users: Dict[str, Dict] = {}
    
    def get_user(self, username: str) -> Optional[Dict]:
        return self.users.get(username)
    
    def create_user(self, username: str, password: str) -> bool:
        if not self._is_valid_username(username) or not self._is_valid_password(password):
            return False
        if username in self.users:
            return False
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.users[username] = {
            'password': hashed,
            'created_at': datetime.utcnow().isoformat(),
            'last_login': None
        }
        return True
    
    def _is_valid_username(self, username: str) -> bool:
        return bool(re.match(r'^[a-zA-Z0-9_]{3,32}$', username))
    
    def _is_valid_password(self, password: str) -> bool:
        return len(password) >= 12 and any(c.isupper() for c in password) and \
               any(c.islower() for c in password) and any(c.isdigit() for c in password)

db = SecureDatabase()

def require_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('is_admin'):
            return "Access denied", 403
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if not username or not password:
        return "Missing credentials", 400
    
    user = db.get_user(username)
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        session['username'] = username
        session['is_admin'] = username == 'admin'
        session.permanent = True
        user['last_login'] = datetime.utcnow().isoformat()
        return "Login successful", 200
    return "Invalid credentials", 401

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/admin')
@require_admin
def admin_dashboard():
    username = session.get('username')
    user = db.get_user(username)
    if not user:
        return "User not found", 404
    
    return f"""
    <h1>Admin Dashboard</h1>
    <p>Welcome, {username}</p>
    <p>Last login: {user['last_login']}</p>
    <a href='/logout'>Logout</a>
    """

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use HTTPS in production