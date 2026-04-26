I'll help you implement a secure password reset feature. Before we dive into the code, let me explain the key security considerations:

1. Password reset tokens should be secure and time-limited
2. Passwords should be hashed using strong algorithms
3. The process should include email verification
4. Tokens should expire after a short time
5. Passwords should be validated against password policies

Here's a secure implementation using Python with Flask:

```python
from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import datetime
from email_validator import validate_email, EmailNotValidError
from passlib.hash import argon2
import smtplib
from email.mime.text import MIMEText
from typing import Dict, Optional

app = Flask(__name__)

# Simulated database
users = {}

def generate_token() -> str:
    return secrets.token_urlsafe(32)

def send_email(to_email: str, subject: str, body: str) -> bool:
    # This is a placeholder - in real implementation, use proper email service
    print(f"Sending email to {to_email}")
    return True

@app.route('/reset_password', methods=['POST'])
def reset_password():
    try:
        data = request.get_json()
        
        # Validate email
        email = data.get('email')
        if not email:
            return jsonify({'error': 'Email is required'}), 400
        
        # Validate email format
        try:
            valid = validate_email(email)
            email = valid.email
        except EmailNotValidError:
            return jsonify({'error': 'Invalid email format'}), 400

        # Check if user exists
        user = users.get(email)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Generate reset token
        token = generate_token()
        expiration = datetime.datetime.now() + datetime.timedelta(hours=1)

        # Store reset data (in real app, use secure database)
        reset_data = {
            'token': token,
            'expiration': expiration,
            'user_id': user['id']
        }
        users[email]['reset_data'] = reset_data

        # Send reset email
        reset_link = f"https://example.com/reset?token={token}"
        subject = "Password Reset Request"
        body = f"Click the link to reset your password: {reset_link}"
        if not send_email(email, subject, body):
            return jsonify({'error': 'Failed to send reset email'}), 500

        return jsonify({'message': 'Password reset email sent'}), 200

    except Exception as e:
        app.logger.error(f"Error during password reset: {str(e)}")
        return jsonify({'error': 'Internal server error'}), 500

@app.route('/reset', methods=['GET'])
def reset_password_form():
    token = request.args.get('token')
    if not token:
        return jsonify({'error': 'Token is required'}), 400

    # Validate token
    for email, user_data in users.items():
        if user_data.get('reset_data') and user_data['reset_data']['token'] == token:
            expiration = user_data['reset_data']['expiration']
            if datetime.datetime.now() < expiration:
                return jsonify({'form': 'reset_password_form'}), 200

    return jsonify({'error': 'Invalid or expired token'}), 400

@app.route('/reset', methods=['POST'])
def reset_password_with_token():
    try:
        data = request.get_json()
        token = data.get('token')
        new_password = data.get('new_password')

        # Validate password
        if not new_password or len(new_password) < 12:
            return jsonify({'error