```python
from flask import Flask, request, jsonify, abort
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import re
from datetime import datetime, timedelta
import logging
from typing import Optional
import bleach

app = Flask(__name__)

# Configure secure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Simulated database - replace with actual database in production
users_db = {}

# Rate limiting
MAX_ATTEMPTS = 3
LOCKOUT_DURATION = 300  # 5 minutes

# Rate limiting cache
attempt_cache = {}

def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))

def validate_password(password: str) -> bool:
    """Validate password strength."""
    return (len(password) >= 12 and
            any(c.isupper() for c in password) and
            any(c.islower() for c in password) and
            any(c.isdigit() for c in password) and
            any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?') for c in password)

def generate_reset_token() -> str:
    """Generate secure password reset token."""
    return secrets.token_urlsafe(32)

@app.route('/reset_password', methods=['POST'])
def reset_password():
    """Handle password reset request."""
    try:
        # Validate input
        email = request.form.get('email')
        if not email or not validate_email(email):
            abort(400, description="Invalid email format")

        # Check rate limiting
        if email in attempt_cache:
            if attempt_cache[email] >= MAX_ATTEMPTS:
                abort(429, description="Too many attempts. Try again later.")
            else:
                # Reset cache after lockout period
                if datetime.now() > attempt_cache[email] + timedelta(seconds=LOCKOUT_DURATION):
                    del attempt_cache[email]
        
        # Check if user exists
        user = users_db.get(email)
        if not user:
            abort(404, description="User not found")

        # Generate reset token
        reset_token = generate_reset_token()
        
        # Store reset token with expiration
        expiration = datetime.now() + timedelta(hours=1)
        users_db[email]['reset_token'] = {
            'token': reset_token,
            'expires': expiration
        }

        # Send reset email (implementation not shown)
        # ...

        return jsonify({
            'message': 'Password reset instructions sent to your email',
            'token': reset_token
        }), 200

    except Exception as e:
        logger.error(f"Error during password reset: {str(e)}")
        abort(500, description="Internal server error")

@app.route('/reset_password/<token>', methods=['POST'])
def reset_password_with_token(token: str):
    """Handle password reset with token."""
    try:
        # Validate token
        if not token:
            abort(400, description="Invalid token")

        # Check token expiration
        for email, data in users_db.items():
            if 'reset_token' in data:
                if data['reset_token']['token'] == token:
                    if datetime.now() > data['reset_token']['expires']:
                        del users_db[email]['reset_token']
                        abort(400, description="Token expired")
                    break

        # Get user
        user = users_db[email]

        # Validate password
        new_password = request.form.get('new_password')
        if not new_password or not validate_password(new_password):
            abort(400, description="Invalid password")

        # Hash new password
        hashed_password = generate_password_hash(new_password)

        # Update user