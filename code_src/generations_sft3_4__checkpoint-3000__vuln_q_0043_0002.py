from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash
import secrets
import datetime
from datetime import datetime
import re

app = Flask(__name__)

# Simulated database - replace with actual database in production
users = {}

def generate_reset_token():
    return secrets.token_urlsafe(32)

def validate_password(password):
    # Check password complexity
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
        data = request.get_json()
        
        # Validate required fields
        if not all(key in data for key in ('email', 'token', 'new_password')):
            return jsonify({'error': 'Missing required fields'}), 400
            
        email = data['email']
        token = data['token']
        new_password = data['new_password']
        
        # Validate email format
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            return jsonify({'error': 'Invalid email format'}), 400
            
        # Validate password complexity
        if not validate_password(new_password):
            return jsonify({'error': 'Password does not meet complexity requirements'}), 400
            
        # Validate token
        if not token or not secrets.compare_digest(token, users[email]['reset_token']):
            return jsonify({'error': 'Invalid or expired token'}), 401
            
        # Generate new password hash
        new_password_hash = generate_password_hash(new_password)
        
        # Update user password
        users[email]['password'] = new_password_hash
        users[email]['reset_token'] = None
        users[email]['reset_token_expiry'] = None
        
        return jsonify({'message': 'Password reset successful'}), 200
        
    except Exception as e:
        return jsonify({'error': 'An error occurred during password reset'}), 500