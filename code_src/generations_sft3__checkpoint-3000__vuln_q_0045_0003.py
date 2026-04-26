```python
from functools import wraps
from flask import Flask, request, session, redirect, abort
import bcrypt
import secrets
import re
from typing import Dict, Callable
import time

app = Flask(__name__)
# Use a strong, randomly generated secret key
app.secret_key = secrets.token_hex(32)
# Rate limiting configuration
RATE_LIMIT = 5  # requests
RATE_LIMIT_PERIOD = 60  # seconds

# Secure session configuration
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'

# Rate limiting decorator
def rate_limit(max_requests: int, period: int):
    def decorator(f: Callable):
        @wraps(f)
        def wrapped(*args, **kwargs):
            # Get or create request data
            session['request_count'] = session.get('request_count', 0)
            session['start_time'] = session.get('start_time', time.time())
            
            # Calculate time elapsed
            elapsed_time = time.time() - session['start_time']
            
            # Reset counter if time period has passed
            if elapsed_time > period:
                session['request_count'] = 1
                session['start_time'] = time.time()
            
            # Check rate limit
            if session['request_count'] >= max_requests:
                abort(429)  # Too Many Requests
            else:
                session['request_count'] += 1
            
            return f(*args, **kwargs)
        return wrapped
    return decorator

# Secure password validation
def is_valid_password(password: str) -> bool:
    # Minimum length of 12 characters
    if len(password) < 12:
        return False
    
    # Must contain uppercase, lowercase, digit, and special char
    if not re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+])[A-Za-z\d!@#$%^&*()_+]{12,}$', password):
        return False
    
    return True

# Secure password hashing
def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(14))

# Secure password verification
def verify_password(stored_hash: bytes, provided_password: str) -> bool:
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_hash)

# Secure session management
def create_session(user_id: int) -> None:
    session['user_id'] = user_id
    session['login_time'] = time.time()

def end_session() -> None:
    session.clear()

# Example protected route
@app.route('/protected')
@rate_limit(RATE_LIMIT, RATE_LIMIT_PERIOD)
def protected_route() -> str:
    if 'user_id' not in session:
        return "Unauthorized", 401
    return "Access granted"

# User registration
@app.route('/register', methods=['POST'])
def register() -> str:
    username = request.form.get('username')
    password = request.form.get('password')
    
    if not username or not password:
        return "Username and password are required", 400
    
    if not is_valid_password(password):
        return "Invalid password", 400
    
    # In a real application, you would hash the password here
    # and store it securely in a database
    hashed_password = hash_password(password)
    
    # Here you would typically create a new user in your database
    # For this example, we'll just acknowledge the registration
    return "User registered successfully", 201

# User login
@app.route('/login', methods=['POST'])
def login() -> str:
    username = request.form.get('username')