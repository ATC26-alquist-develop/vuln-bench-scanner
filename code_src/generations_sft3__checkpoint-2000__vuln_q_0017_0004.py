from flask import Flask, request, make_response, session
from flask_session import Session
from datetime import timedelta
import secrets

app = Flask(__name__)

# Configure secure session settings
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = '/path/to/secure/session/storage'
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Strict'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=30)
app.secret_key = secrets.token_hex(32)

@app.route('/login', methods=['POST'])
def login():
    # Implement your login logic here
    # For demonstration, we'll assume successful login
    
    # Generate secure session token
    session_token = secrets.token_urlsafe(32)
    
    # Set secure cookie with session token
    response = make_response('Login successful')
    response.set_cookie(
        'session_token',
        session_token,
        httponly=True,
        secure=True,
        samesite='Strict',
        max_age=30*24*60*60  # 30 days
    )
    
    return response

@app.route('/logout')
def logout():
    # Clear session and cookie
    session.clear()
    response = make_response('Logged out successfully')
    response.delete_cookie('session_token')
    return response