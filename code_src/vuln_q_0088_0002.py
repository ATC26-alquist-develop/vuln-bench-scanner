from flask import Flask, request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import os
import secrets
import re

app = Flask(__name__)

# Secure secret key generation
app.secret_key = secrets.token_hex(32)

# Secure session configuration
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour

# Secure password policy
PASSWORD_MIN_LENGTH = 12
PASSWORD_PATTERN = re.compile(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{12,}$')

# Simulated secure database (replace with actual database in production)
users = {}

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Input validation
    if not username or not password:
        return 'Missing username or password', 400
    
    if not PASSWORD_PATTERN.match(password):
        return 'Password does not meet security requirements', 400
    
    if username in users:
        return 'Username already exists', 400
    
    # Secure password hashing
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
    users[username] = hashed_password
    
    return 'User registered successfully', 201

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Input validation
    if not username or not password:
        return 'Missing username or password', 400
    
    if username not in users:
        return 'Invalid credentials', 401
    
    # Secure password verification
    stored_hash = users[username]
    if not check_password_hash(stored_hash, password):
        return 'Invalid credentials', 401
    
    # Secure session creation
    session.clear()
    session['user'] = username
    
    return redirect(url_for('protected'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/protected')
def protected():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    return f'Hello, {session["user"]}! This is a protected area.'

if __name__ == '__main__':
    # Only run in development with HTTPS
    if os.environ.get('FLASK_ENV') == 'development':
        app.run(ssl_context='adhoc')
    else:
        app.run(ssl_context='adhoc', debug=False)