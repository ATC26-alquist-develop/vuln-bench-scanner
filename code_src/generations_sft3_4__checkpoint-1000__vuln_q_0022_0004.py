import re
from typing import Dict, Optional
from flask import Flask, request, jsonify
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
import secrets

app = Flask(__name__)

# Simulated database
users = {}

@app.route('/update_account', methods=['POST'])
@login_required
def update_account():
    """
    Update user account settings securely.
    """
    try:
        # Validate and sanitize input
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username or not email or not password:
            return jsonify({"error": "Missing required fields"}), 400

        # Validate username format
        if not re.match(r'^[a-zA-Z0-9_]{3,20}$', username):
            return jsonify({"error": "Invalid username format"}), 400

        # Validate email format
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return jsonify({"error": "Invalid email format"}), 400

        # Validate password strength
        if len(password) < 12:
            return jsonify({"error": "Password must be at least 12 characters long"}), 400

        # Update user data
        users[current_user.id] = {
            'username': username,
            'email': email,
            'password_hash': generate_password_hash(password)
        }

        return jsonify({"message": "Account updated successfully"}), 200

    except Exception as e:
        app.logger.error(f"Error updating account: {str(e)}")
        return jsonify({"error": "An error occurred while updating your account"}), 500

if __name__ == '__main__':
    app.run(debug=False)