from flask import Flask, request, make_response, session
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from datetime import datetime, timedelta
import os

app = Flask(__name__)

# Generate a secure random key for session management
app.secret_key = secrets.token_hex(32)

def create_secure_cookie(name, value, max_age=3600):
    """
    Create a secure cookie with proper attributes
    """
    cookie = {
        'value': value,
        'httponly': True,
        'secure': os.environ.get('HTTPS') == 'on',
        'samesite': 'Strict',
        'max_age': max_age
    }
    return cookie

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Verify credentials (implementation not shown)
    if verify_credentials(username, password):
        # Generate secure session token
        session_token = secrets.token_hex(32)
        
        # Create remember me cookie
        remember_cookie = create_secure_cookie(
            'remember_token',
            session_token,
            max_age=30 * 24 * 60 * 60  # 30 days
        )
        
        # Create login cookie
        login_cookie = create_secure_cookie(
            'login_token',
            username,
            max_age=3600  # 1 hour
        )
        
        # Set cookies
        response = make_response('Login successful')
        response.set_cookie(**remember_cookie)
        response.set_cookie(**login_cookie)
        
        return response
    else:
        return 'Invalid credentials', 401

@app.route('/logout')
def logout():
    # Remove all session cookies
    response = make_response('Logged out successfully')
    response.delete_cookie('login_token')
    response.delete_cookie('remember_token')
    return response

def verify_credentials(username, password):
    # Implement secure credential verification
    # This is a placeholder - actual implementation would use secure password hashing
    return True