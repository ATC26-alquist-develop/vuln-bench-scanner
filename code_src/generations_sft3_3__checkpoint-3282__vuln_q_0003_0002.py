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
LOCKOUT_TIME = 1800  # 30 minutes

def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def generate_reset_token() -> str:
    """Generate secure random token for password reset."""
    return secrets.token_urlsafe(32)

def check_rate_limit(ip: str) -> bool:
    """Check if IP address has exceeded rate limit."""
    if ip not in users:
        users[ip] = {'attempts': 0, 'last_attempt': None}
    
    if users[ip]['attempts'] >= MAX_ATTEMPTS:
        last_attempt = users[ip]['last_attempt']
        if last_attempt and datetime.now() - last_attempt < timedelta(seconds=LOCKOUT_TIME):
            return False
    
    users[ip]['attempts'] += 1
    users[ip]['last_attempt'] = datetime.now()
    return True

@app.route('/reset_password', methods=['POST'])
def reset_password():
    try:
        # Input validation
        data = request.get_json()
        if not data or 'email' not in data:
            return jsonify({'error': 'Invalid request'}), 400

        email = bleach.clean(data['email'].strip().lower())
        
        if not validate_email(email):
            return jsonify({'error': 'Invalid email format'}), 400

        # Rate limiting check
        if not check_rate_limit(request.remote_addr):
            return jsonify({'error': 'Too many attempts. Try again later.'}), 429

        # Find user
        user = users.get(email)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Generate reset token
        reset_token = generate_reset_token()
        
        # Store token with expiration
        expiration = datetime.now() + timedelta(hours=1)
        user['reset_token'] = reset_token
        user['reset_token_expires'] = expiration

        # Send reset email (implementation not shown)
        # send_reset_email(email, reset_token)

        return jsonify({
            'message': 'Password reset instructions sent',
            'token': reset_token
        }), 200

    except Exception as e:
        logger.error(f"Error during password reset: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use HTTPS in production