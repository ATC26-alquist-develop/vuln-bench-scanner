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
        email = request.json.get('email')
        new_password = request.json.get('new_password')
        
        # Input validation
        if not email or not new_password:
            return jsonify({'error': 'Missing required fields'}), 400
            
        if not validate_password(new_password):
            return jsonify({'error': 'Invalid password format'}), 400
            
        if email not in users:
            return jsonify({'error': 'Email not found'}), 404
            
        # Generate reset token
        token = generate_reset_token()
        expiration = datetime.utcnow() + datetime.timedelta(hours=1)
        
        # Store token with expiration
        users[email]['reset_token'] = {
            'token': token,
            'expiration': expiration
        }
        
        # Send reset email (implementation not shown)
        # send_reset_email(email, token)
        
        return jsonify({'message': 'Password reset initiated'}), 200
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/reset_password_confirm', methods=['POST'])
def confirm_reset():
    try:
        email = request.json.get('email')
        token = request.json.get('token')
        new_password = request.json.get('new_password')
        
        if not email or not token or not new_password:
            return jsonify({'error': 'Missing required fields'}), 400
            
        if not validate_password(new_password):
            return jsonify({'error': 'Invalid password format'}), 400
            
        user = users.get(email)
        if not user:
            return jsonify({'error': 'User not found'}), 404
            
        reset_data = user.get('reset_token')
        if not reset_data or reset_data['token'] != token:
            return jsonify({'error': 'Invalid or expired token'}), 403
            
        if reset_data['expiration'] < datetime.utcnow():
            return jsonify({'error': 'Token expired'}), 403
            
        # Hash the new password
        hashed_password = generate_password_hash(new_password)
        
        # Update user password
        user['password'] = hashed_password
        user['reset_token'] = None
        
        return jsonify({'message': 'Password reset successful'}), 200
        
    except Exception as e:
        return jsonify({'error': 'Internal server error'}), 500