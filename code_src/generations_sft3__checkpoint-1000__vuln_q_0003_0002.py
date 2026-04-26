```python
from flask import Flask, request, jsonify, abort
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import re
from datetime import datetime, timedelta
import logging
from typing import Optional
import bcrypt

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Simulated database (replace with actual database in production)
users = {}

# Rate limiting
RATE_LIMIT = 5  # attempts per minute
RATE_LIMIT_PERIOD = 60  # seconds

class RateLimiter:
    def __init__(self):
        self.rates = {}
    
    def check(self, key, ip):
        if key not in self.rates:
            self.rates[key] = []
        
        now = datetime.now()
        self.rates[key] = [t for t in self.rates[key] if t > now - timedelta(minutes=1)]
        
        if len(self.rates[key]) >= RATE_LIMIT:
            return False
        
        self.rates[key].append(now)
        return True

rate_limiter = RateLimiter()

def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_password(password: str) -> bool:
    """Validate password strength."""
    return (len(password) >= 12 and
            any(c.isupper() for c in password) and
            any(c.islower() for c in password) and
            any(c.isdigit() for c in password) and
            any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password))

@app.route('/reset_password', methods=['POST'])
def reset_password():
    try:
        # Validate input
        email = request.json.get('email')
        password = request.json.get('password')
        
        if not email or not password:
            return jsonify({"error": "Email and password are required"}), 400
            
        if not validate_email(email):
            return jsonify({"error": "Invalid email format"}), 400
            
        if not validate_password(password):
            return jsonify({"error": "Password does not meet security requirements"}), 400
            
        # Check rate limit
        if not rate_limiter.check(email, request.remote_addr):
            return jsonify({"error": "Too many attempts. Please try again later."}), 429
            
        # Generate secure token
        token = secrets.token_urlsafe(32)
        
        # Hash password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Store user data (in production, use secure database)
        users[token] = {
            'email': email,
            'password_hash': hashed_password,
            'reset_token': token,
            'reset_token_expiry': datetime.utcnow() + timedelta(hours=1)
        }
        
        # Send reset email (implement secure email sending here)
        logger.info(f"Password reset request for user: {email}")
        
        return jsonify({"message": "Password reset request sent", "token": token}), 200
        
    except Exception as e:
        logger.error(f"Error during password reset: {str(e)}")
        return jsonify({"error": "An error occurred during password reset"}), 500

@app.route('/verify_reset_token', methods=['POST'])
def verify_reset_token():
    try:
        token = request.json.get('token')
        password = request.json.get('password')
        
        if not token or not password:
            return jsonify({"error": "Token and password are required"}), 400