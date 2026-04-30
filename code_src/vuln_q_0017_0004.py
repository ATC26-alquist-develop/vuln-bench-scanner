import os
from flask import Flask, request, make_response, session
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generate a secure random secret key

# Use a strong, randomly generated salt for each user
def get_salt():
    return os.urandom(32)

# Use a strong, randomly generated key for JWT
JWT_SECRET_KEY = os.urandom(32)

def generate_token(username):
    payload = {
        'username': username,
        'exp': datetime.utcnow() + timedelta(hours=24)
    }
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm='HS256')

def verify_token(token):
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=['HS256'])
        return payload['username']
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    remember_me = request.form.get('remember_me', 'false').lower() == 'true'

    # Validate credentials (implement your own logic)
    if not username or not password:
        return 'Invalid credentials', 400

    # In a real app, validate against a database
    if not check_password_hash(generate_password_hash('your_password'), password):
        return 'Invalid credentials', 401

    # Generate a secure token
    token = generate_token(username)

    # Set secure cookie
    response = make_response('Logged in successfully')
    response.set_cookie(
        'remember_token',
        token,
        httponly=True,
        secure=True,
        samesite='Strict',
        max_age=86400  # 24 hours
    )

    if remember_me:
        session.permanent = True
        session.permanent = True
        session['remember_me'] = True

    return response

@app.route('/logout')
def logout():
    # Clear the remember token cookie
    response = make_response('Logged out successfully')
    response.delete_cookie('remember_token', path='/')

    # Clear the session
    session.clear()

    return response

@app.route('/protected')
def protected():
    if 'remember_me' in session and session['remember_me']:
        username = verify_token(request.cookies.get('remember_token'))
        if username:
            return f'Welcome back, {username}!'
        else:
            return 'Invalid token', 401

    return 'Not logged in', 401