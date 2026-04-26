from flask import Flask, request, render_template, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import re
import secrets
import os
from datetime import timedelta
import logging
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)
csrf = CSRFProtect(app)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Simulated database (replace with actual database in production)
users = {}

@app.before_request
def make_session_permanent():
    session.permanent = True

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        # Input validation
        if not username or not password:
            return "Username and password are required", 400
        
        if len(username) < 3 or len(username) > 50:
            return "Username must be between 3 and 50 characters", 400
        
        if len(password) < 8:
            return "Password must be at least 8 characters", 400
        
        # Password strength check
        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$', password):
            return "Password must contain at least one letter, one number, and one special character", 400
        
        # Check if username already exists
        if username in users:
            return "Username already exists", 400
        
        # Hash password
        hashed_password = generate_password_hash(password)
        
        # Store user (in production, use secure database)
        users[username] = {
            'password': hashed_password,
            'profile': {}
        }
        
        return redirect(url_for('profile', username=username))
    
    return render_template('register.html')

@app.route('/profile/<username>')
def profile(username):
    if not username or username not in users:
        return "User not found", 404
    
    # Check CSRF token
    if not session.get('csrf_token') or session['csrf_token'] != request.args.get('csrf_token'):
        return "Invalid CSRF token", 400
    
    return render_template('profile.html', username=username, profile=users[username]['profile'])

@app.route('/csrf_token')
def get_csrf_token():
    session['csrf_token'] = secrets.token_hex(16)
    return {'csrf_token': session['csrf_token']}

if __name__ == '__main__':
    app.run(debug=False)