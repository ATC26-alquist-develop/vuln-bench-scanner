from flask import Flask, request, session, redirect, url_for
from werkzeug.security import check_password_hash
from functools import wraps
import re

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Change this to a strong, random key

# Simulated database - replace with actual database in production
users = {
    'user1': {'username': 'user1', 'email': 'user1@example.com', 'password_hash': 'hashed_password_here'}
}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/update_settings', methods=['POST'])
@login_required
def update_settings():
    # Validate CSRF token
    if not request.form.get('csrf_token') or request.form['csrf_token'] != session.get('csrf_token'):
        return 'Invalid CSRF token', 400

    # Validate and sanitize input
    username = request.form.get('username')
    email = request.form.get('email')
    
    if not username or not email:
        return 'Username and email are required', 400

    # Validate email format
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        return 'Invalid email format', 400

    # Check if new username is already taken
    if username in users:
        return 'Username already exists', 400

    # Update user settings
    users[session['username']]['username'] = username
    users[session['username']]['email'] = email

    # Clear CSRF token
    session['csrf_token'] = None

    return 'Settings updated successfully', 200

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if not username or not password:
        return 'Username and password are required', 400

    if username in users and check_password_hash(users[username]['password_hash'], password):
        session['username'] = username
        session['csrf_token'] = 'new_csrf_token_here'  # Generate new CSRF token
        return 'Login successful', 200
    else:
        return 'Invalid credentials', 401

if __name__ == '__main__':
    app.run(debug=False)  # Set debug to False in production