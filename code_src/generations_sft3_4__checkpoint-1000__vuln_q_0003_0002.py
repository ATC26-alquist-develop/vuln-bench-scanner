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

# Rate limit cache
rate_limit_cache = {}

def rate_limit(key: str, attempts: int) -> bool:
    """Implement rate limiting"""
    current_time = datetime.now()
    if key in rate_limit_cache:
        old_attempts, old_time = rate_limit_cache[key]
        if current_time - old_time > timedelta(seconds=RATE_LIMIT_WINDOW):
            rate_limit_cache.pop(key)
        else:
            attempts -= old_attempts
    if attempts >= MAX_ATTEMPTS:
        return False
    rate_limit_cache[key] = (attempts, current_time)
    return True

def validate_email(email: str) -> bool:
    """Validate email format"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_password(password: str) -> bool:
    """Validate password strength"""
    return (len(password) >= 12 and
            any(c.isupper() for c in password) and
            any(c.islower() for c in password) and
            any(c.isdigit() for c in password) and
            any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password))

@app.route('/reset_password', methods=['POST'])
def reset_password():
    """Handle password reset request"""
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
            
        # Check if user exists
        if email not in users:
            return jsonify({"error": "User not found"}), 404
            
        # Check rate limit
        if not rate_limit(email, 0):
            return jsonify({"error": "Too many attempts, please try again later"}), 429
            
        # Generate new password hash
        new_password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # Update user password
        users[email] = new_password_hash
        
        # Reset rate limit
        rate_limit_cache[email] = (0, datetime.now())
        
        return jsonify({"message": "Password reset successful"}), 200
        
    except Exception as e:
        logger.error(f"Error during password reset: {str(e)}")
        abort(500, description="An error occurred during password reset")

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use HTTPS in production