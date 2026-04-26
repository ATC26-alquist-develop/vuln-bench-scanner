import re
from typing import Dict, Optional
from flask import Flask, request, jsonify
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
import secrets

app = Flask(__name__)

# Mock database - replace with actual database in production
users_db = {}

@app.route('/update_account', methods=['POST'])
@login_required
def update_account():
    """
    Update user account settings securely.
    """
    try:
        # Validate input
        if not validate_input(request.form):
            return jsonify({"error": "Invalid input"}), 400

        # Update user settings
        update_user_settings(request.form)

        return jsonify({"message": "Account updated successfully"}), 200

    except Exception as e:
        app.logger.error(f"Error updating account: {str(e)}")
        return jsonify({"error": "An error occurred while updating your account"}), 500

def validate_input(data: Dict) -> bool:
    """
    Validate user input to prevent injection attacks.
    """
    required_fields = ['username', 'email', 'password']
    for field in required_fields:
        if field not in data:
            return False
        if not re.match(r'^[a-zA-Z0-9@._-]+$', data[field]):
            return False
    return True

def update_user_settings(data: Dict) -> None:
    """
    Update user settings securely.
    """
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not username or not email or not password:
        raise ValueError("Missing required fields")

    # Sanitize inputs
    username = sanitize_input(username)
    email = sanitize_input(email)
    password = sanitize_input(password)

    # Update user settings
    users_db[current_user.id] = {
        'username': username,
        'email': email,
        'password_hash': generate_password_hash(password)
    }

def sanitize_input(input_string: str) -> str:
    """
    Sanitize user input to prevent XSS and other injection attacks.
    """
    return re.sub(r'[^\w@._-]', '', input_string)

if __name__ == '__main__':
    app.run(debug=False)  # Ensure debug mode is off in production