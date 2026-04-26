from flask import Flask, request, session, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
import secrets
from functools import wraps
import re
from datetime import timedelta

app = Flask(__name__)

# Use strong, randomly generated secret key
app.secret_key = secrets.token_hex(32)

# Configure session to use secure cookie and HTTPS only
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

def validate_password(password: str) -> bool:
    """Validate password strength"""
    if len(password) < 12:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    return True

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if not username or not password:
        return {'error': 'Missing credentials'}, 400
    
    # In production, fetch user from secure database
    # This is a simplified example
    if username == 'admin' and validate_password(password):
        session['user_id'] = username
        return {'message': 'Login successful'}, 200
    
    return {'error': 'Invalid credentials'}, 401

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/protected')
@require_auth
def protected():
    return {'message': f'Hello, {session["user_id"]}! This is a protected route.'}

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use HTTPS in production with proper SSL certificate