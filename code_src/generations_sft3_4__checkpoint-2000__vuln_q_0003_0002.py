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

# Secure secret key
app.config['SECRET_KEY'] = secrets.token_hex(32)

# Rate limiting
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per day", "10 per hour"]
)

# Password reset token expiration
RESET_TOKEN_EXPIRY = timedelta(hours=1)

class PasswordReset:
    def __init__(self):
        self.db = {}  # In-memory database for simplicity
    
    def _is_valid_email(self, email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

    def _is_strong_password(self, password: str) -> bool:
        """Check if password meets strength requirements"""
        return (len(password) >= 12 and
                re.search(r'[A-Z]', password) and
                re.search(r'[a-z]', password) and
                re.search(r'[0-9]', password) and
                re.search(r'[!@#$%^&*(),.?":{}|<>]', password))

    def _generate_token(self) -> str:
        """Generate secure token"""
        return secrets.token_urlsafe(32)

    def _validate_token(self, token: str) -> bool:
        """Validate token"""
        try:
            return token and isinstance(token, str) and len(token) == 43
        except Exception:
            return False

    def _hash_password(self, password: str) -> str:
        """Securely hash password"""
        return generate_password_hash(password)

    def _reset_password(self, email: str, new_password: str) -> bool:
        """Reset password"""
        if not self._is_valid_email(email):
            logger.warning(f"Invalid email format: {email}")
            return False
            
        if not self._is_strong_password(new_password):
            logger.warning(f"Weak password attempt: {email}")
            return False

        if email not in self.db:
            logger.info(f"Password reset requested for non-existent user: {email}")
            return False

        # Generate and store new token
        new_token = self._generate_token()
        self.db[email]['reset_token'] = new_token
        self.db[email]['reset_time'] = datetime.utcnow()
        
        # Send reset email (implementation not shown)
        # send_reset_email(email, new_token)
        
        logger.info(f"Password reset initiated for user: {email}")
        return True

@app.route('/reset_password', methods=['POST'])
@limiter.limit("5 per minute")
def reset_password():
    try:
        data = request.get_json()
        if not data or 'email' not in data or 'new_password' not in data:
            abort(400, description="Missing required fields")

        email = bleach.clean(data['email'].strip().lower())
        new_password = bleach.clean(data['new_password'])

        if not email or not new_password:
            abort(400, description="Invalid input")

        reset_service = PasswordReset()
        success = reset_service._reset_password(email, new_password)

        if success:
            return jsonify({"message": "Password reset initiated successfully"}), 200
        else:
            return jsonify({"error": "Password