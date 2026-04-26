from flask import Flask, request, session, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
import secrets
from functools import wraps
import re

app = Flask(__name__)
# Use strong, randomly generated secret key
app.secret_key = secrets.token_hex(32)

# Simulated user database (in production use secure database)
USERS = {
    'admin': generate_password_hash('secure_password')
}

def validate_password(password: str) -> bool:
    """Validate password complexity"""
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
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            return 'Username and password required', 400
            
        if username in USERS and \
           check_password_hash(USERS[username], password):
            session['username'] = username
            return redirect(url_for('protected'))
            
        return 'Invalid credentials', 401
    
    return 'Login page'  # Render login template

@app.route('/protected')
@require_auth
def protected():
    return f'Hello, {session["username"]}! This is a protected page.'

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use HTTPS in production