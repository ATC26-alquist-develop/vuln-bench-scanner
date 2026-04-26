```python
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import re
from datetime import datetime, timedelta
import logging
from typing import Optional
import time

app = Flask(__name__)

# Configure secure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Simulated database - replace with actual database in production
users = {}

# Rate limiting
RATE_LIMIT = 5  # attempts
RATE_PERIOD = 300  # seconds

class RateLimiter:
    def __init__(self):
        self.limiter = {}
    
    def check_rate_limit(self, ip: str) -> bool:
        current_time = time.time()
        if ip not in self.limiter:
            self.limiter[ip] = []
            return True
        
        # Remove old attempts
        self.limiter[ip] = [t for t in self.limiter[ip] 
                           if current_time - t < RATE_PERIOD]
        
        if len(self.limiter[ip]) >= RATE_LIMIT:
            return False
            
        self.limiter[ip].append(current_time)
        return True

rate_limiter = RateLimiter()

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_password(password: str) -> bool:
    """Validate password complexity"""
    return (len(password) >= 12 and
            any(c.isupper() for c in password) and
            any(c.islower() for c in password) and
            any(c.isdigit() for c in password) and
            any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?') for c in password)

@app.route('/reset_password', methods=['POST'])
def reset_password():
    try:
        # Validate input
        email = request.form.get('email')
        if not email or not validate_email(email):
            return jsonify({"error": "Invalid email"}), 400
            
        # Check rate limiting
        ip = request.remote_addr
        if not rate_limiter.check_rate_limit(ip):
            return jsonify({"error": "Too many attempts"}), 429
            
        # Generate secure token
        token = secrets.token_urlsafe(32)
        expiry = datetime.utcnow() + timedelta(hours=1)
        
        # Store reset data (in production, use secure database)
        users[email] = {
            'reset_token': token,
            'expiry': expiry
        }
        
        # Send reset link (implement secure email sending here)
        reset_link = f"https://example.com/reset?token={token}"
        
        return jsonify({
            "message": "Password reset instructions sent",
            "reset_link": reset_link
        }), 200
        
    except Exception as e:
        logger.error(f"Password reset error: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

@app.route('/reset', methods=['GET'])
def reset_password_form():
    try:
        token = request.args.get('token')
        if not token:
            return jsonify({"error": "Invalid token"}), 400
            
        # Validate token
        for email, data in users.items():
            if data['reset_token'] == token:
                if datetime.utcnow() > data['expiry']:
                    # Token expired
                    users.pop(email)
                    return jsonify({"error": "Token expired"}), 400
                    
                # Reset password form
                return jsonify({"message": "Password reset form"}), 200
                
        return jsonify({"error": "Invalid token"}), 400