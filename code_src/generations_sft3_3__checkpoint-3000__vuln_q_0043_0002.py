from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import datetime
from email_validator import validate_email, EmailNotValidError
from datetime import datetime
import re

app = Flask(__name__)

# Simulated database - replace with actual database in production
users = {}

def is_valid_email(email):
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False

def is_valid_password(password):
    # Implement strong password policy
    return len(password) >= 12 and re.search(r'[A-Z]', password) and \
           re.search(r'[a-z]', password) and re.search(r'[0-9]', password) and \
           re.search(r'[!@#$%^&*(),.?":{}|<>]', password)

@app.route('/reset_password', methods=['POST'])
def reset_password():
    try:
        email = request.json.get('email')
        if not email or not is_valid_email(email):
            return jsonify({'error': 'Invalid email'}), 400

        token = request.json.get('token')
        if not token:
            return jsonify({'error': 'Token is required'}), 400

        # Verify token and expiration
        user = users.get(email)
        if not user or not verify_reset_token(token):
            return jsonify({'error': 'Invalid or expired token'}), 401

        # Get new password
        new_password = request.json.get('new_password')
        if not new_password or not is_valid_password(new_password):
            return jsonify({'error': 'Invalid password'}), 400

        # Hash the new password
        hashed_password = generate_password_hash(new_password)

        # Update user's password
        user['password'] = hashed_password
        user['reset_token'] = None
        user['reset_token_expiration'] = None

        return jsonify({'message': 'Password reset successful'}), 200

    except Exception as e:
        return jsonify({'error': 'An error occurred'}), 500

def generate_reset_token():
    return secrets.token_urlsafe(32)

def verify_reset_token(token):
    expiration = users.get(token)['reset_token_expiration']
    if not expiration:
        return False
    if expiration < datetime.utcnow():
        return False
    return True