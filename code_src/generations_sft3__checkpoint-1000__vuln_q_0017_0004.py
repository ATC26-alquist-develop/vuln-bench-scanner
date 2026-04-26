from flask import Flask, request, session
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)
csrf = CSRFProtect(app)

def generate_secure_cookie():
    """Generate a secure cookie with expiration"""
    secure_cookie = secrets.token_hex(32)
    expiration = datetime.datetime.now() + datetime.timedelta(days=30)
    return {
        'secure': True,
        'httponly': True,
        'samesite': 'Strict',
        'max_age': 2592000,  # 30 days
        'value': secure_cookie,
        'expires': expiration
    }

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Validate credentials (implement your own auth logic)
    if authenticate_user(username, password):
        # Generate secure cookie
        secure_cookie = generate_secure_cookie()
        
        # Set secure cookie in session
        session.clear()
        session.update(secure_cookie)
        
        return 'Login successful', 200
    else:
        return 'Invalid credentials', 401

@app.route('/logout')
def logout():
    # Clear all session data
    session.clear()
    return 'Logged out successfully', 200