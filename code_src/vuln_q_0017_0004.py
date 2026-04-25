from flask import Flask, request, make_response, session
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
import secrets
import hmac
import hashlib

app = Flask(__name__)
bcrypt = Bcrypt(app)

# Set secure cookie parameters
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)

def generate_secure_token():
    return secrets.token_urlsafe(32)

def create_remember_me_token(username):
    # Generate a secure token
    token = generate_secure_token()
    
    # Create a secure hash of the token and username
    hash_input = f"{token}:{username}".encode('utf-8')
    hashed = hashlib.sha256(hash_input).hexdigest()
    
    # Store the hashed token in the database (implement your own database logic)
    # For example: db.set_remember_me_token(username, hashed)
    
    return token

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Validate credentials (implement your own logic)
    if not validate_credentials(username, password):
        return 'Invalid credentials', 401
    
    # Create remember me token
    remember_me_token = create_remember_me_token(username)
    
    # Set remember me cookie
    response = make_response('Logged in successfully')
    response.set_cookie('remember_me', remember_me_token, httponly=True, secure=True, samesite='Strict')
    
    # Set session
    session['user'] = username
    session.permanent = True
    
    return response

@app.route('/logout')
def logout():
    # Clear remember me cookie
    response = make_response('Logged out successfully')
    response.delete_cookie('remember_me')
    
    # Clear session
    session.clear()
    
    return response

def validate_credentials(username, password):
    # Implement your own authentication logic
    # This is just a placeholder
    return True