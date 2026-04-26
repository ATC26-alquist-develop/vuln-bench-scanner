from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import datetime
from email_validator import validate_email, EmailNotValidError
from datetime import datetime, timedelta

app = Flask(__name__)

# Simulated database - replace with actual database in production
users = {}

def generate_token():
    return secrets.token_urlsafe(32)

def is_valid_email(email):
    try:
        valid = validate_email(email)
        return valid.email
    except EmailNotValidError:
        return False

@app.route('/reset_password', methods=['POST'])
def reset_password():
    try:
        email = request.json.get('email')
        if not is_valid_email(email):
            return jsonify({"error": "Invalid email"}), 400

        user = users.get(email)
        if not user:
            return jsonify({"error": "User not found"}), 404

        token = generate_token()
        expiration = datetime.utcnow() + timedelta(hours=1)
        
        # Store token with expiration
        user['reset_token'] = token
        user['reset_token_expiration'] = expiration

        # Send email with reset link (implementation not shown)
        # ...

        return jsonify({"message": "Password reset instructions sent", "token": token}), 200

    except Exception as e:
        return jsonify({"error": "An error occurred"}), 500

@app.route('/reset_password/<token>', methods=['POST'])
def reset_password_with_token(token):
    try:
        # Verify token
        user = next((u for u in users.values() if u.get('reset_token') == token), None)
        if not user or user['reset_token_expiration'] < datetime.utcnow():
            return jsonify({"error": "Invalid or expired token"}), 400

        # Get password reset data
        password = request.json.get('password')
        if not password:
            return jsonify({"error": "Password is required"}), 400

        # Hash password
        hashed_password = generate_password_hash(password)

        # Update user with new password
        user['password'] = hashed_password
        user['reset_token'] = None
        user['reset_token_expiration'] = None

        return jsonify({"message": "Password reset successful"}), 200

    except Exception as e:
        return jsonify({"error": "An error occurred"}), 500