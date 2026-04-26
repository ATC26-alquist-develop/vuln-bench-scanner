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

# Whitelist of allowed login URLs
ALLOWED_LOGIN_DOMAINS = {'https://example.com', 'https://subdomain.example.com'}

def is_safe_url(target):
    """Validate if URL is safe to redirect to"""
    ref_url = "https://example.com"  # Set your base domain here
    url_root = ref_url[: -len(request.path)]
    test = urlparse(target).netloc in ALLOWED_LOGIN_DOMAINS or url_root == target[: -len(request.path)]
    return test

def validate_password(password):
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
    """Decorator to require authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login', next=request.url))
        return f(*args, **kwargs)
    return decorated

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            return 'Username and password are required', 400
            
        if not validate_password(password):
            return 'Password does not meet security requirements', 400
            
        # In production, use proper database query with parameterized queries
        # This is a simplified example
        user = get_user_from_db(username)
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            session.permanent = True
            return redirect(url_for('protected'))
            
    return 'Login page'  # Render login template

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/protected')
@require_auth
def protected():
    return 'This is a protected page'