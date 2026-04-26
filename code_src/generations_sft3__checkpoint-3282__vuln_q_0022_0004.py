from flask import Flask, request, session, redirect, url_for
from werkzeug.security import check_password_hash
from functools import wraps
import re

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Change this to a secure random value

# Simulated database
users = {
    'user1': {
        'username': 'user1',
        'email': 'user1@example.com',
        'password_hash': 'hashed_password_here'
    }
}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET'])
def login():
    return "Login page"

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/update_settings', methods=['POST'])
@login_required
def update_settings():
    # Validate CSRF token
    if not session.get('csrf_token') or session['csrf_token'] != request.form.get('csrf_token'):
        return "Invalid CSRF token", 400

    # Validate and sanitize input
    username = request.form.get('username')
    email = request.form.get('email')

    if not username and not email:
        return "Username or email is required", 400

    if username:
        if not re.match(r'^[a-zA-Z0-9_]{3,20}$', username):
            return "Invalid username format", 400
        if username in users:
            if users[username]['username'] != session['username']:
                return "Username already exists", 400

    if email:
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return "Invalid email format", 400

    # Update user settings
    if username:
        users[session['username']]['username'] = username
    if email:
        users[session['username']]['email'] = email

    return "Settings updated successfully", 200