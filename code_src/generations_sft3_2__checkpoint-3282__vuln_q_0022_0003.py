from flask import Flask, request, session, redirect, url_for
from functools import wraps
import secrets
import bcrypt
from typing import Dict
import re

app = Flask(__name__)
# Secure secret key generation
app.secret_key = secrets.token_hex(32)

# Simulated secure database connection
class SecureDatabase:
    def __init__(self):
        self.users: Dict[str, Dict] = {}
    
    def create_user(self, username: str, password: str) -> bool:
        # Validate username and password
        if not self._validate_username(username) or not self._validate_password(password):
            return False
        
        # Hash password with bcrypt
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Check for existing user
        if username in self.users:
            return False
            
        # Store user with hashed password
        self.users[username] = {
            'password': hashed,
            'role': 'user'
        }
        return True
    
    def _validate_username(self, username: str) -> bool:
        return bool(re.match(r'^[a-zA-Z0-9_]{3,20}$', username))
    
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

@app.route('/login', methods=['GET'])
def login():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return 'Login page'

@app.route('/login', methods=['POST'])
def login_post():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if not username or not password:
        return 'Username and password required', 400
    
    user = db.users.get(username)
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password']):
        session['username'] = username
        return redirect(url_for('dashboard'))
    
    return 'Invalid credentials', 401

@app.route('/dashboard')
@login_required
def dashboard():
    return 'Admin Dashboard'

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Enable HTTPS