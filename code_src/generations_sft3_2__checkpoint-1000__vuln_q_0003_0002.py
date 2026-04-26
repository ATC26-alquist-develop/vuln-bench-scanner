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
MAX_ATTEMPTS = 3
RATE_LIMIT_WINDOW = 300  # 5 minutes

class RateLimiter:
    def __init__(self):
        self.attempts = {}
        self.last_check = {}

    def check(self, ip: str, action: str) -> bool:
        now = datetime.now()
        
        # Check if IP has exceeded rate limit
        if ip in self.attempts and action in self.attempts[ip]:
            attempts, last_check = self.attempts[ip][action]
            if now - last_check < timedelta(seconds=RATE_LIMIT_WINDOW):
                if attempts >= MAX_ATTEMPTS:
                    return False
                self.attempts[ip][action] = (attempts + 1, last_check)
            else:
                self.attempts[ip][action] = (1, now)
        else:
            self.attempts[ip] = {action: [1, now]}
        
        return True

rate_limiter = RateLimiter()

def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_password(password: str) -> bool:
    """Validate password strength."""
    return len(password) >= 12 and any(c.isupper() for c in password) and \
           any(c.islower() for c in password) and any(c.isdigit() for c in password) and \
           any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)

@app.route('/reset_password', methods=['POST'])
def reset_password():
    try:
        # Validate input
        email = request.json.get('email')
        password = request.json.get('password')
        
        if not email or not password:
            abort(400, description="Email and password are required")
            
        if not validate_email(email):
            abort(400, description="Invalid email format")
            
        if not validate_password(password):
            abort(400, description="Password does not meet complexity requirements")
            
        # Check rate limiting
        if not rate_limiter.check(request.remote_addr, 'password_reset'):
            abort(429, description="Too many requests. Please try again later.")
            
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
        abort(500, description="An error occurred during password reset")

@app.route('/verify_reset_token', methods=['POST'])
def verify_reset_token():
    try:
        token = request