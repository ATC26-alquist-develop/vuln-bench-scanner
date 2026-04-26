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

    def check(self, ip: str, method: str) -> bool:
        now = datetime.now()
        
        # Check if IP has exceeded rate limit
        if ip in self.attempts and method in self.attempts[ip]:
            attempts, last_check = self.attempts[ip][method]
            if now - last_check < timedelta(seconds=RATE_LIMIT_WINDOW):
                if attempts >= MAX_ATTEMPTS:
                    return False
                self.attempts[ip][method] = (attempts + 1, last_check)
            else:
                self.attempts[ip][method] = (1, now)
        else:
            self.attempts[ip] = {method: [1, now]}
        
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
        if not request.is_json:
            abort(400, description="Invalid content type")

        data = request.get_json()
        
        # Validate email
        if not validate_email(data.get('email')):
            abort(400, description="Invalid email format")

        # Check rate limit
        ip = request.remote_addr
        if not rate_limiter.check(ip, 'POST'):
            abort(429, description="Too many requests")

        # Validate password
        if not validate_password(data.get('password')):
            abort(400, description="Password does not meet security requirements")

        # Generate reset token
        token = secrets.token_urlsafe(32)
        expiration = datetime.now() + timedelta(hours=1)

        # Store reset data
        if 'reset_data' not in users:
            users['reset_data'] = {}
        users['reset_data'][token] = {
            'email': data['email'],
            'expiration': expiration
        }

        # Send reset email (implementation not shown)
        # ...

        return jsonify({"message": "Password reset request sent", "token": token}), 200

    except Exception as e:
        logger.error(f"Error during password reset: {str(e)}")
        abort(500, description="Internal server error")

@app.route('/reset_password/<token>', methods=['POST'])
def verify_reset_token(token: str):
    try:
        # Validate token
        if token not in users['reset_data']:
            abort(400, description="Invalid or expired reset token")

        # Check if token has expired
        if users['