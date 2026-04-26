from flask import Flask, request, session, redirect, url_for
from werkzeug.security import check_password_hash
from typing import Dict, Any
import re

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Change this to a secure random key

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
    new_full_name = request.form.get('full_name', '').strip()

    # Validate email
    if not new_email or not validate_email(new_email):
        return "Invalid email format", 400

    # Validate password
    if new_password and not validate_password(new_password):
        return "Password must be at least 12 characters long and contain uppercase, lowercase, and digits", 400

    # Update user data
    try:
        # In a real application, you would use an ORM like SQLAlchemy
        # to safely update the database
        # Example:
        # user = User.query.filter_by(username=session['username']).first()
        # user.email = new_email
        # user.password_hash = check_password_hash(app.config['PASSWORD_HASHER'], new_password)
        # db.session.commit()
        pass
    except Exception as e:
        app.logger.error(f"Error updating account: {str(e)}")
        return "An error occurred while updating your account", 500

    return "Account updated successfully", 200