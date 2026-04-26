from flask import Flask, request, session
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import secrets

app = Flask(__name__)

# Generate a secure secret key
app.secret_key = secrets.token_hex(32)

def create_remember_me_token(user_id):
    # Create a secure token with expiration
    expiration = datetime.utcnow() + timedelta(days=30)
    token = secrets.token_urlsafe(32)
    return {
        'token': token,
        'user_id': user_id,
        'expiration': expiration
    }

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Authenticate user (implementation not shown)
    if authenticate_user(username, password):
        # Create remember me token
        remember_token = create_remember_me_token(username)
        
        # Set secure cookie with expiration
        response = app.make_secure_response(redirect('/dashboard'))
        response.set_cookie(
            'remember_token',
            remember_token['token'],
            httponly=True,
            secure=True,
            samesite='Strict',
            max_age=30 * 24 * 60 * 60,  # 30 days
            path='/',
            domain='.example.com'  # Adjust as needed
        )
        
        response.set_cookie(
            'user_id',
            remember_token['user_id'],
            httponly=True,
            secure=True,
            samesite='Strict',
            max_age=30 * 24 * 60 * 60,
            path='/',
            domain='.example.com'
        )
        
        response.set_cookie(
            'expiration',
            remember_token['expiration'].isoformat(),
            httponly=True,
            secure=True,
            samesite='Strict',
            max_age=30 * 24 * 60 * 60,
            path='/',
            domain='.example.com'
        )
        
        return response
    else:
        return 'Invalid credentials', 401

def create_remember_me_token(user_id):
    expiration = datetime.utcnow() + timedelta(days=30)
    token = secrets.token_urlsafe(32)
    return {
        'token': token,
        'user_id': user_id,
        'expiration': expiration
    }

@app.route('/dashboard')
def dashboard():
    if 'remember_token' in session:
        token = session.get('remember_token')
        user_id = session.get('user_id')
        expiration = session.get('expiration')
        
        # Verify token
        remember_token = create_remember_me_token(user_id)
        if token == remember_token['token'] and \
           datetime.utcnow() < datetime.fromisoformat(expiration):
            return f"Welcome back, {user_id}!"
        else:
            # Invalidate token
            session.clear()
            return "Invalid or expired remember me token"
    return "Unauthorized", 401