from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash
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
users = {}

# Rate limiting
MAX_ATTEMPTS = 3
LOCKOUT_TIME = 300  # 5 minutes
lockouts = {}

def validate_password(password: str) -> bool:
    """Validate password complexity."""
    if len(password) < 12:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    return True

@app.route('/reset_password', methods=['POST'])
def reset_password():
    try:
        # Input validation
        data = request.get_json()
        if not data or 'email' not in data or 'new_password' not in data:
            return jsonify({"error": "Invalid request"}), 400

        email = bleach.clean(data['email'])
        new_password = bleach.clean(data['new_password'])

        # Rate limiting
        ip = request.remote_addr
        if ip in lockouts:
            if lockouts[ip] > datetime.now():
                return jsonify({"error": "Too many attempts. Try again later."}), 429

        # Validate email format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return jsonify({"error": "Invalid email format"}), 400

        # Validate password complexity
        if not validate_password(new_password):
            return jsonify({"error": "Password does not meet complexity requirements"}), 400

        # Generate secure reset token
        token = secrets.token_urlsafe(32)
        
        # Store reset info (in production, use secure database)
        users[email] = {
            'reset_token': token,
            'reset_expiry': datetime.now() + timedelta(hours=1),
            'new_password': new_password
        }

        # Send reset email (implementation not shown)
        # send_reset_email(email, token)

        return jsonify({"message": "Password reset initiated"}), 200

    except Exception as e:
        logger.error(f"Error during password reset: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use HTTPS in production