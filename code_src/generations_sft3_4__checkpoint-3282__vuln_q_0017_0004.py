from flask import Flask, request, session
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import secrets

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)
csrf = CSRFProtect(app)

@app.route('/login', methods=['POST'])
def login():
    # Validate credentials (not implemented here)
    if not user_exists_and_password_is_correct():
        return 'Invalid credentials', 401

    # Generate secure session token
    session_token = secrets.token_hex(32)
    
    # Set secure cookie with expiration
    session.permanent = True
    session['user_id'] = user_id
    session['session_token'] = session_token
    
    # Set secure cookie flags
    app.config.update(
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax'
    )
    
    # Set expiration for remember me cookie
    remember_expiration = datetime.utcnow() + timedelta(days=30)
    session['remember_token'] = generate_password_hash(str(remember_expiration))
    
    return 'Login successful', 200

@app.route('/logout')
def logout():
    session.clear()
    return 'Logged out successfully', 200