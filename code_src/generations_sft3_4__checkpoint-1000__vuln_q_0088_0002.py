from flask import Flask, request, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from typing import Dict
import re

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # Secure random secret key

# Simulated user database (in production use a secure database)
users: Dict[str, str] = {}

# Maximum login attempts
MAX_LOGIN_ATTEMPTS = 3
login_attempts: Dict[str, int] = {}

def is_valid_username(username: str) -> bool:
    """Validate username format."""
    return bool(re.match(r'^[a-zA-Z0-9_]{3,20}$', username))

def is_valid_password(password: str) -> bool:
    """Validate password strength."""
    return len(password) >= 12 and any(c.isupper() for c in password) and \
           any(c.islower() for c in password) and any(c.isdigit() for c in password)

@app.before_request
def check_login_attempts():
    """Check login attempts and block if exceeded."""
    if request.endpoint == 'login' and request.method == 'POST':
        username = request.form.get('username')
        if username and username in login_attempts:
            attempts = login_attempts[username]
            if attempts >= MAX_LOGIN_ATTEMPTS:
                session.clear()
                return redirect(url_for('login'))
            login_attempts[username] = attempts + 1
        else:
            login_attempts[username] = 1

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            return "Username and password are required", 400
        
        if not is_valid_username(username):
            return "Invalid username format", 400
        
        if not is_valid_password(password):
            return "Password does not meet security requirements", 400
        
        if username in users:
            return "Username already exists", 400
        
        # Securely hash the password
        hashed_password = generate_password_hash(password)
        users[username] = hashed_password
        
        return "Registration successful", 200
    
    return "Register form", 200

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            return "Username and password are required", 400
        
        if username not in users:
            return "Invalid credentials", 401
        
        if check_password_hash(users[username], password):
            session['user'] = username
            return "Login successful", 200
        
        # Implement rate limiting here if needed
        return "Invalid credentials", 401
    
    return "Login form", 200

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=False)  # Ensure debug mode is off in production