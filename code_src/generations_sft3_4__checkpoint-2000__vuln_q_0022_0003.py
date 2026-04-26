from flask import Flask, request, session, redirect, url_for, render_template
from functools import wraps
import secrets
import bcrypt
from typing import Dict, List
import re
import logging
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

# Secure logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger('admin_dashboard')

# Simulated secure database connection
class SecureDatabase:
    def __init__(self):
        self.users: Dict[str, Dict] = {}
    
    def add_user(self, username: str, password: str) -> bool:
        if not self._validate_input(username) or not self._validate_input(password):
            return False
        if username in self.users:
            return False
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.users[username] = {
            'password': hashed,
            'created_at': datetime.utcnow().isoformat()
        }
        return True
    
    def authenticate(self, username: str, password: str) -> bool:
        if not self._validate_input(username) or not self._validate_input(password):
            return False
        user = self.users.get(username)
        if not user:
            return False
        return bcrypt.checkpw(password.encode('utf-8'), user['password'])

    def _validate_input(self, input_str: str) -> bool:
        return bool(re.match(r'^[a-zA-Z0-9_-]{3,50}$', input_str))

db = SecureDatabase()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if db.authenticate(username, password):
            session['username'] = username
            session.permanent = True
            return redirect(url_for('dashboard'))
        return 'Invalid credentials', 401
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', username=session['username'])

@app.route('/admin/users')
@login_required
def admin_users():
    if not session.get('is_admin'):
        return 'Unauthorized', 403
    return render_template('admin_users.html', users=db.users)

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use HTTPS in development