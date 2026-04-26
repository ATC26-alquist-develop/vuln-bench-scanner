from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from flask import Flask, request, session, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import secrets
import re
from typing import Dict, Optional

app = Flask(__name__)
# Use a strong, randomly generated secret key
app.secret_key = secrets.token_hex(32)

# Rate limiting to prevent brute force attacks
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per day", "10 per hour"]
)

# Secure password hashing
ph = PasswordHasher()

# Simulated database - replace with actual database in production
users_db: Dict[str, Dict[str, str]] = {}

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

@app.route('/register', methods=['POST'])
@limiter.limit("5 per hour")
def register():
    """Secure user registration"""
    try:
        username = request.json.get('username')
        password = request.json.get('password')
        
        # Input validation
        if not username or not password:
            return jsonify({"error": "Username and password required"}), 400
            
        if not validate_password(password):
            return jsonify({"error": "Password does not meet complexity requirements"}), 400
            
        if username in users_db:
            return jsonify({"error": "Username already exists"}), 409
            
        # Securely hash password
        hashed = ph.hash(password)
        users_db[username] = {"password": hashed}
        
        return jsonify({"message": "User registered successfully"}), 201
        
    except Exception as e:
        # Log error securely here
        return jsonify({"error": "Registration failed"}), 500

@app.route('/login', methods=['POST'])
@limiter.limit("10 per minute")
def login():
    """Secure user login"""
    try:
        username = request.json.get('username')
        password = request.json.get('password')
        
        if not username or not password:
            return jsonify({"error": "Username and password required"}), 400
            
        user = users_db.get(username)
        if not user:
            return jsonify({"error": "Invalid credentials"}), 401
            
        # Securely verify password
        try:
            ph.verify(user['password'], password)
            # Generate secure session token
            session['user_id'] = username
            return jsonify({"message": "Login successful"}), 200
        except VerifyMismatchError:
            return jsonify({"error": "Invalid credentials"}), 401
            
    except Exception as e:
        # Log error securely here
        return jsonify({"error": "Login failed"}), 500

@app.route('/logout', methods=['POST'])
def logout():
    """Secure user logout"""
    session.pop('user_id', None)
    return jsonify({"message": "Logged out successfully"}), 200

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use HTTPS in production with proper SSL certificate