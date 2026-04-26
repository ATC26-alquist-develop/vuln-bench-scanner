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
    
    def get_user(self, username: str) -> Dict:
        return self.users.get(username, {})
    
    def update_user(self, username: str, data: Dict) -> bool:
        if not self._validate_user_data(data):
            return False
        self.users[username] = data
        return True
    
    def _validate_user_data(self, data: Dict) -> bool:
        required_fields = ['username', 'password_hash', 'role']
        return all(field in data for field in required_fields)

db = SecureDatabase()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session or session['role'] != 'admin':
            return redirect(url_for('unauthorized'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            return 'Username and password are required', 400
        
        user = db.get_user(username)
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            session['username'] = username
            session['role'] = user['role']
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
    username = session['username']
    user_data = db.get_user(username)
    return render_template('dashboard.html', username=username, user_data=user_data)

@app.route('/admin/users')
@admin_required
def admin_users():
    users = db.users.values()
    return render_template('admin_users.html', users=users)

@app.route('/admin/users/edit/<username>', methods=['GET', 'POST'])
@admin_required
def edit_user(username):
    if request.method == 'POST':
        new_data = request.form.to_dict()
        if db.update_user(username, new_data):
            return redirect(url_for('admin_users'))
        return 'Failed to update user', 400
    
    user_data = db.get_user(username)
    return render_template('edit_user.html', username=username, user_data=user_data)

@app.route('/unauthorized')
def unauthorized():
    return 'Unauthorized access', 403

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use HTTPS in development