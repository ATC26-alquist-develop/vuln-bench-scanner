from flask import Flask, request, session
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)
csrf = CSRFProtect(app)

def generate_secure_cookie():
    # Generate a secure random token
    token = secrets.token_hex(32)
    # Set secure and HTTPOnly flags
    return {
        'value': token,
        'httponly': True,
        'secure': True,
        'samesite': 'Strict',
        'max_age': 3600 * 24 * 30  # 30 days
    }

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Validate credentials (implement your own auth logic)
    if authenticate_user(username, password):
        # Generate secure cookie
        secure_cookie = generate_secure_cookie()
        
        # Set cookie with secure settings
        response = app.make_response('Login successful')
        response.set_cookie(**secure_cookie)
        
        return response
    else:
        return 'Invalid credentials', 401

@app.route('/logout')
def logout():
    # Remove secure cookie
    response = app.make_response('Logged out')
    response.delete_cookie('remember_me')
    return response

def authenticate_user(username, password):
    # Implement your own authentication logic here
    # This is just a placeholder
    return username == 'admin' and check_password_hash(generate_password_hash('password'), password)