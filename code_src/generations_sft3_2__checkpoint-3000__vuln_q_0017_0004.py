from flask import Flask, request, make_response, session
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
from datetime import datetime, timedelta

app = Flask(__name__)

# Generate a secure random key for session management
app.secret_key = secrets.token_hex(32)

def create_secure_cookie(name, value, max_age=None):
    """
    Create a secure cookie with appropriate flags and parameters
    """
    cookie = {
        'value': value,
        'httponly': True,  # Prevent XSS attacks
        'secure': request.is_secure,  # Only send over HTTPS
        'samesite': 'Strict',  # Protect against CSRF
        'max_age': max_age or 30 * 24 * 60 * 60  # 30 days
    }
    return cookie

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Verify credentials (implement your own secure auth logic)
    if verify_credentials(username, password):
        # Generate secure token
        token = secrets.token_hex(32)
        hashed_token = generate_password_hash(token)
        
        # Create secure cookie
        remember_cookie = create_secure_cookie('remember_token', hashed_token)
        
        # Create session
        session['user_id'] = username
        session['token'] = token
        
        # Set remember cookie
        response = make_response('Login successful')
        response.set_cookie(**remember_cookie)
        
        return response
    else:
        return 'Invalid credentials', 401

@app.route('/logout')
def logout():
    # Clear session and cookies
    session.clear()
    response = make_response('Logged out successfully')
    response.delete_cookie('remember_token')
    return response

def verify_credentials(username, password):
    # Implement your own secure authentication logic here
    # This is just a placeholder
    return username == 'admin' and check_password_hash(generate_password_hash('password'), password)

def get_user_from_session():
    # Implement your own secure session management
    # This is just a placeholder
    return session.get('user_id')

# Additional security measures
@app.before_request
def check_https():
    if not request.is_secure:
        return 'Please use HTTPS', 403

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use HTTPS in development