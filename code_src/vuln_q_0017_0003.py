from flask import Flask, request, make_response, session
from flask_wtf.csrf import CSRFProtect
import secrets
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)  # Secure secret key
csrf = CSRFProtect(app)

@app.route('/')
def index():
    # Use secure session management
    session.permanent = True
    session.httponly = True
    session.secure = True  # Only send cookies over HTTPS
    
    # Set secure cookie parameters
    response = make_response("Welcome!")
    response.set_cookie(
        'user_id', 
        session.get('user_id', ''),
        httponly=True,
        secure=True,
        samesite='Strict',
        max_age=3600  # 1 hour expiration
    )
    
    return response

@app.route('/logout')
def logout():
    # Clear all session data
    session.clear()
    return "Logged out"

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use HTTPS in development