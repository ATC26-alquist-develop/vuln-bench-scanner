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

@app.route('/update_account', methods=['POST'])
def update_account():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Get form data
    new_email = request.form.get('email', '').strip()
    new_password = request.form.get('password', '').strip()
    new_fullname = request.form.get('fullname', '').strip()

    # Validate email
    if not new_email or not validate_email(new_email):
        return "Invalid email format", 400

    # Validate password
    if new_password and not validate_password(new_password):
        return "Password must be at least 12 characters long and contain uppercase, lowercase, and digits", 400

    # Update user data
    try:
        # Here you would typically call a database function to update the user's email and password
        # For this example, we'll just return a success message
        return "Account updated successfully", 200
    except Exception as e:
        # Log the error securely
        print(f"Error updating account: {str(e)}")
        return "An error occurred while updating your account", 500

if __name__ == '__main__':
    app.run(debug=False)  # Ensure debug mode is off in production