from flask import Flask, request, session
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta
import secrets

app = Flask(__name__)

# Generate a secure secret key
app.secret_key = secrets.token_hex(32)

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Validate credentials (implement your own auth logic)
    if authenticate_user(username, password):
        # Generate secure session token
        session_token = secrets.token_hex(32)
        
        # Set secure cookie with expiration
        remember_me = request.form.get('remember_me', 'false').lower() == 'true'
        if remember_me:
            expiration = datetime.utcnow() + timedelta(days=30)
            session.permanent = True
            app.permanent_session_lifetime = timedelta(days=30)
            
            # Store session token securely
            session['session_token'] = session_token
            
            # Set secure cookie with expiration
            response = app.make_secure_response(('index.html'))
            response.set_cookie(
                'session',
                session_token,
                httponly=True,
                secure=True,
                samesite='Strict',
                max_age=30*24*60*60,
                expires=expiration
            )
            return response
        else:
            # Set secure cookie without expiration
            response = app.make_secure_response(('index.html'))
            response.set_cookie(
                'session',
                session_token,
                httponly=True,
                secure=True,
                samesite='Strict',
                max_age=30*24*60*60
            )
            return response
    else:
        return 'Invalid credentials', 401

def authenticate_user(username, password):
    # Implement your own authentication logic here
    # This is just a placeholder
    return False