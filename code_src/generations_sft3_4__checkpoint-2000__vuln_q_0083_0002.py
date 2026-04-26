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

def is_valid_username(username: str) -> bool:
    """Validate username format."""
    return bool(re.match(r'^[a-zA-Z0-9_]{3,20}$', username))

def is_valid_password(password: str) -> bool:
    """Validate password strength."""
    return len(password) >= 12 and any(c.isupper() for c in password) and \
           any(c.islower() for c in password) and any(c.isdigit() for c in password)

@app.route('/register', methods=['POST'])
@limiter.limit("5 per hour")
def register():
    """Register a new user."""
    username = request.json.get('username')
    password = request.json.get('password')
    
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400
    
    if not is_valid_username(username):
        return jsonify({"error": "Invalid username format"}), 400
    
    if not is_valid_password(password):
        return jsonify({"error": "Password does not meet complexity requirements"}), 400
    
    if username in users_db:
        return jsonify({"error": "Username already exists"}), 409
    
    # Securely hash the password
    hashed = ph.hash(password)
    users_db[username] = {"password": hashed}
    
    return jsonify({"message": "User registered successfully"}), 201

@app.route('/login', methods=['POST'])
@limiter.limit("10 per minute")
def login():
    """Authenticate user."""
    username = request.json.get('username')
    password = request.json.get('password')
    
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400
    
    user = users_db.get(username)
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401
    
    try:
        ph.verify(user['password'], password)
    except VerifyMismatchError:
        return jsonify({"error": "Invalid credentials"}), 401
    
    # Generate secure session token
    session['user_id'] = username
    session.permanent = True
    
    return jsonify({"message": "Login successful"}), 200

@app.route('/logout', methods=['POST'])
def logout():
    """Log out user."""
    session.clear()
    return jsonify({"message": "Logged out successfully"}), 200

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use HTTPS in production with proper SSL certificate