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
    
    def check(self, ip: str, action: str) -> bool:
        now = time.time()
        if ip not in self.limiter:
            self.limiter[ip] = []
        # Remove old attempts
        self.limiter[ip] = [t for t in self.limiter[ip] if now - t < RATE_PERIOD]
        if len(self.limiter[ip]) >= RATE_LIMIT:
            return False
        self.limiter[ip].append(now)
        return True

rate_limiter = RateLimiter()

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_password(password: str) -> bool:
    """Validate password complexity"""
    return len(password) >= 12 and any(c.isupper() for c in password) and \
           any(c.islower() for c in password) and any(c.isdigit() for c in password) and \
           any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)

@app.route('/reset_password', methods=['POST'])
def reset_password():
    try:
        # Validate input
        email = request.form.get('email')
        if not email or not validate_email(email):
            return jsonify({"error": "Invalid email"}), 400

        # Check rate limiting
        if not rate_limiter.check(request.remote_addr, 'reset_password'):
            return jsonify({"error": "Too many attempts. Please try again later."}), 429

        # Find user
        user = users.get(email)
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Generate new password
        new_password = secrets.token_urlsafe(32)
        hashed_password = generate_password_hash(new_password)

        # Update user password
        user['password'] = hashed_password
        user['last_password_change'] = datetime.utcnow().isoformat()

        # Log successful reset
        logger.info(f"Password reset successful for user: {email}")

        # Send password reset email (implementation not shown)

        return jsonify({"message": "Password reset successful. A new password has been sent to your email."}), 200

    except Exception as e:
        # Log error without exposing details
        logger.error(f"Password reset error: {str(e)}")
        return jsonify({"error": "An error occurred during password reset"}), 500

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use HTTPS in production