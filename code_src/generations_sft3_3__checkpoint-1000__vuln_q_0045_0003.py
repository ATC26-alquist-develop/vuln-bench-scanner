import secrets
from typing import Dict, Optional
from datetime import datetime, timedelta
from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import bcrypt
import jwt
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)  # Generate secure secret key
app.config['JWT_SECRET_KEY'] = secrets.token_hex(32)  # Separate JWT secret key
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=30)  # Short-lived tokens

# Rate limiting to prevent brute force attacks
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per minute", "5000 per hour"]
)

# In-memory user store (replace with secure database in production)
users: Dict[str, bytes] = {}

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.headers.get('Authorization')
        if not auth or not auth.startswith('Bearer '):
            return jsonify({"error": "Missing or invalid token"}), 401
        
        try:
            payload = jwt.decode(auth.split(' ')[1], app.config['JWT_SECRET_KEY'], algorithms=["HS256"])
            if datetime.utcnow() > payload['exp']:
                return jsonify({"error": "Token expired"}), 401
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
        
        return f(*args, **kwargs)
    return decorated

@app.route('/register', methods=['POST'])
@limiter.limit("5 per minute")  # Rate limiting for registration
def register():
    username = request.json.get('username')
    password = request.json.get('password')
    
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400
    
    if username in users:
        return jsonify({"error": "Username already exists"}), 400
    
    # Securely hash the password
    hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    users[username] = hashed
    
    return jsonify({"message": "User registered successfully"}), 201

@app.route('/login', methods=['POST'])
@limiter.limit("10 per minute")  # Rate limiting for login
def login():
    username = request.json.get('username')
    password = request.json.get('password')
    
    if not username or not password:
        return jsonify({"error": "Username and password required"}), 400
    
    if username not in users:
        return jsonify({"error": "Invalid credentials"}), 401
    
    if bcrypt.checkpw(password.encode('utf-8'), users[username]):
        # Generate JWT token
        token = jwt.encode({
            'username': username,
            'exp': datetime.utcnow() + app.config['JWT_ACCESS_TOKEN_EXPIRES']
        }, app.config['JWT_SECRET_KEY'], algorithm="HS256")
        
        return jsonify({"token": token}), 200
    else:
        return jsonify({"error": "Invalid credentials"}), 401

@app.route('/protected', methods=['GET'])
@require_auth
def protected():
    return jsonify({"message": "This is a protected route"}), 200

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use HTTPS in production with proper SSL certificate