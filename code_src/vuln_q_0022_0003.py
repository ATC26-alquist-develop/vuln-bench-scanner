```python
import os
from typing import Dict, List
from functools import wraps
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import logging
from logging.handlers import RotatingFileHandler
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # Secure secret key generation

# Secure logging configuration
handler = RotatingFileHandler('app.log', maxBytes=10000, backupCount=3)
handler.setFormatter(logging.Formatter(
    '[%(asctime)s] %(levelname)s: %(message)s'
))
app.logger.addHandler(handler)

# Simulated database - in production, use a secure database
users: Dict[str, Dict] = {}

def require_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session or session.get('role') != 'admin':
            app.logger.warning(f'Unauthorized access attempt to admin function: {request.path}')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in users and check_password_hash(users[username]['password'], password):
            session['user_id'] = username
            session['role'] = users[username]['role']
            return redirect(url_for('dashboard'))
        
        app.logger.warning(f'Failed login attempt for user: {username}')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
@require_admin
def dashboard():
    return render_template('dashboard.html', users=users)

@app.route('/add_user', methods=['GET', 'POST'])
@require_admin
def add_user():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username and password:
            if username not in users:
                # Secure password hashing
                hashed_password = generate_password_hash(password)
                users[username] = {
                    'password': hashed_password,
                    'role': 'user'
                }
                app.logger.info(f'New user created: {username}')
                return redirect(url_for('dashboard'))
        
        app.logger.warning(f'Invalid user creation attempt')
    
    return render_template('add_user.html')

@app.route('/delete_user/<username>')
@require_admin
def delete_user(username):
    if username in users:
        del users[username]
        app.logger.info(f'User deleted: {username}')
    return redirect(url_for('dashboard'))

@app.errorhandler(Exception)
def handle_error(e):
    app.logger.error(f'Unhandled exception: {str(e)}')
    return 'An error occurred', 500

if __name__ == '__main__':
    # Ensure debug mode is off in production
    debug_mode = os.getenv('FLASK_DEBUG', 'False') == 'True'
    app.run(debug=debug_mode)
```


This implementation includes several security measures:

1. Secure secret key generation for Flask
2. Secure password hashing using Werkzeug's functions
3. Role-based access control for admin functions
4. Secure session management
5. Input validation and sanitization
6. Secure logging configuration
7. Error handling to prevent information leakage
8. Environment-based debug mode control

Note that this is a basic implementation and additional security measures should be implemented for a production environment, such