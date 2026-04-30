```python
import secrets
import bcrypt
from datetime import datetime, timedelta
from typing import Dict, Optional
from flask import Flask, request, jsonify, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import re

app = Flask(__name__)
limiter = Limiter(app, key_func=get_remote_address)

# Secure password reset token storage (in-memory for demonstration)
# In production, use a secure database with proper encryption
password_reset_tokens: Dict[str, Dict] = {}

# Rate limiting for password reset attempts
PASSWORD_RESET_RATE_LIMIT = 5  # attempts per hour
PASSWORD_RESET_WINDOW = timedelta(hours=1)

def is_valid_email(email: str) -> bool:
    """Validate email format."""
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(email_regex, email) is not None

def generate_reset_token(email: str) -> str:
    """Generate a secure random token for password reset."""
    return secrets.token_urlsafe(32)

def is_token_valid(token: str, email: str) -> bool:
    """Check if the token is valid and not expired."""
    if token not in password_reset_tokens:
        return False
    token_data = password_reset_tokens[token]
    if token_data['email'] != email:
        return False
    if datetime.utcnow() > token_data['expires_at']:
        del password_reset_tokens[token]
        return False
    return True

@app.route('/request_password_reset', methods=['POST'])
@limiter.limit(PASSWORD_RESET_RATE_LIMIT, key_func=get_remote_address)
def request_password_reset():
    email = request.json.get('email')
    if not email or not is_valid_email(email):
        abort(400, description="Invalid email address")
    
    if email in password_reset_tokens:
        abort(409, description="Email already used for password reset")
    
    token = generate_reset_token(email)
    expires_at = datetime.utcnow() + timedelta(hours=1)
    password_reset_tokens[token] = {'email': email, 'expires_at': expires_at}
    
    # In production, send the token via secure channel (e.g., email)
    return jsonify({'message': 'Password reset token sent'}), 200

@app.route('/reset_password', methods=['POST'])
@limiter.limit(PASSWORD_RESET_RATE_LIMIT, key_func=get_remote_address)
def reset_password():
    token = request.json.get('token')
    new_password = request.json.get('password')
    
    if not token or not is_valid_token(token, new_password):
        abort(400, description="Invalid or expired token")
    
    if not new_password or len(new_password) < 12:
        abort(400, description="Password must be at least 12 characters long")
    
    # Hash the new password (in production, use a secure database)
    hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
    
    # In production, update the user's password in the database
    return jsonify({'message': 'Password updated successfully'}), 200

def is_valid_token(token: str, new_password: str) -> bool:
    """Helper function to validate token and check expiration."""
    return is_token_valid(token, new_password) and datetime.utcnow() < password_reset_tokens[token]['expires_at']

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use HTTPS in production with proper SSL certificate
```


This implementation includes several security measures:

1. Rate limiting to prevent brute-force attacks
2. Secure token generation using `secrets.token_urlsafe()`
3. Token expiration to limit the window of opportunity for attacks
4. Email validation to prevent abuse
5. Password complexity requirements