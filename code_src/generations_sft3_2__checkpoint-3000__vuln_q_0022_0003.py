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
    
    def create_user(self, username: str, password: str) -> bool:
        if not self._validate_username(username) or not self._validate_password(password):
            return False
        if username in self.users:
            return False
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        self.users[username] = {
            'password': hashed,
            'created_at': datetime.utcnow().isoformat(),
            'last_login': None
        }
        return True
    
    def authenticate(self, username: str, password: str) -> bool:
        if username not in self.users:
            return False
        return bcrypt.checkpw(password.encode(), self.users[username]['password'])
    
    def _validate_username(self, username: str) -> bool:
        return bool(re.match(r'^[a-zA-Z0-9_-]{3,32}$', username))
    
    def _validate_password(self, password: str) -> bool:
        return len(password) >= 12 and any(c.isupper() for c in password) and \
               any(c.islower() for c in password) and any(c.isdigit() for c in password)

db = SecureDatabase()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if not username or not password:
        return 'Missing credentials', 400
    
    if db.authenticate(username, password):
        session['username'] = username
        session.permanent = True
        db.users[username]['last_login'] = datetime.utcnow().isoformat()
        return 'Login successful', 200
    else:
        return 'Invalid credentials', 401

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    username = session['username']
    user_data = db.users[username]
    return f"Welcome, {username}! Last login: {user_data['last_login']}"

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Enable HTTPS