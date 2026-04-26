from flask import Flask, request, session, redirect, url_for
from werkzeug.security import check_password_hash
from typing import Dict, Any
import re

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Change this to a secure random value

def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password: str) -> bool:
    """Validate password strength."""
    return len(password) >= 12 and any(c.isupper() for c in password) and \
           any(c.islower() for c in password) and any(c.isdigit() for c in password)

@app.route('/update_settings', methods=['POST'])
def update_settings() -> str:
    if 'username' not in session:
        return "Unauthorized", 401

    new_email = request.form.get('email')
    new_password = request.form.get('password')
    new_fullname = request.form.get('fullname')

    if not new_email or not new_password or not new_fullname:
        return "Missing required fields", 400

    if not validate_email(new_email):
        return "Invalid email format", 400

    if not validate_password(new_password):
        return "Password does not meet security requirements", 400

    # Here you would typically call a database function to update the user's settings
    # This is just a mock implementation
    session['email'] = new_email
    session['fullname'] = new_fullname

    return "Settings updated successfully", 200