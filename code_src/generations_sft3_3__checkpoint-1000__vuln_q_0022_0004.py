import re
from typing import Dict, Optional
from flask import Flask, request, jsonify
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash

app = Flask(__name__)

# Mock database (replace with actual database in production)
users_db = {}

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
        password = request.form.get('password', '')
        
        # Input validation
        if not username or not email:
            return jsonify({"error": "Username and email are required"}), 400
        
        if not re.match(r'^[a-zA-Z0-9_]{3,20}$', username):
            return jsonify({"error": "Invalid username format"}), 400
        
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return jsonify({"error": "Invalid email format"}), 400
        
        if password:
            if len(password) < 8:
                return jsonify({"error": "Password must be at least 8 characters long"}), 400
            if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$', password):
                return jsonify({"error": "Password must contain at least one uppercase letter, one lowercase letter, one number, and one special character"}), 400
        
        # Update user settings
        users_db[current_user.id] = {
            'username': username,
            'email': email,
            'password_hash': generate_password_hash(password) if password else None
        }
        
        return jsonify({"message": "Account updated successfully"}), 200
    
    except Exception as e:
        app.logger.error(f"Error updating account: {str(e)}")
        return jsonify({"error": "An error occurred while updating your account"}), 500

if __name__ == '__main__':
    app.run(debug=False)  # Ensure debug mode is off in production