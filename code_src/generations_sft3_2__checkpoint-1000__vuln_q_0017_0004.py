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
        'max_age': 30 * 24 * 60 * 60,  # 30 days
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
        session['remember_me'] = secure_cookie['value']
        session['expiration'] = secure_cookie['expires']
        
        return 'Login successful', 200
    else:
        return 'Invalid credentials', 401

@app.route('/logout')
def logout():
    if 'remember_me' in session:
        # Remove secure cookie
        session.pop('remember_me', None)
        session.pop('expiration', None)
    return 'Logged out', 200

@app.before_request
def check_remember_me():
    if 'remember_me' in session:
        # Check if cookie has expired
        if datetime.datetime.now() > session['expiration']:
            session.pop('remember_me', None)
            session.pop('expiration', None)
        else:
            # Set secure cookie in response
            response = app.make_response('')
            response.set_cookie(**session['remember_me'])
            session['expiration'] = datetime.datetime.now() + datetime.timedelta(days=30)
    else:
        # Remove any existing secure cookie
        response = app.make_response('')
        response.delete_cookie('remember_me')