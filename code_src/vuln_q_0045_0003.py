import bcrypt
import secrets
from typing import Optional
from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import re

app = Flask(__name__)

# Rate limiting to prevent brute force attacks
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per day", "10 per hour"]
)

# Secure secret key generation
app.config['SECRET_KEY'] = secrets.token_hex(32)

# Secure password hashing
def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(stored_hash: bytes, provided_password: str) -> bool:
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_hash)

# Secure password validation
def is_password_strong(password: str) -> bool:
    return (len(password) >= 12 and
            re.search(r'[A-Z]', password) and
            re.search(r'[a-z]', password) and
            re.search(r'[0-9]', password) and
            re.search(r'[!@#$%^&*(),.?":{}|<>]', password))

# Secure user storage (in-memory for example)
users = {}

@app.route('/register', methods=['POST'])
@limiter.limit("5 per minute")  # Rate limiting for registration
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    if not is_password_strong(password):
        return jsonify({"error": "Password does not meet security requirements"}), 400

    if username in users:
        return jsonify({"error": "Username already exists"}), 409

    # Securely hash password
    hashed_password = hash_password(password)
    users[username] = hashed_password

    return jsonify({"message": "User registered successfully"}), 201

@app.route('/login', methods=['POST'])
@limiter.limit("10 per minute")  # Rate limiting for login
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400

    stored_hash = users.get(username)
    if not stored_hash:
        return jsonify({"error": "Invalid credentials"}), 401

    if verify_password(stored_hash, password):
        # In a real application, generate and return a secure token here
        return jsonify({"message": "Login successful"}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use HTTPS in development