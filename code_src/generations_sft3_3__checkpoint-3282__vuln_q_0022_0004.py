from flask import Flask, request, session, redirect, url_for
from werkzeug.security import check_password_hash
from typing import Dict, Any
import re

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Change this to a secure random value

# Simulated database
users_db: Dict[str, Dict[str, Any]] = {}

@app.route('/update_account', methods=['POST'])
def update_account():
    if 'username' not in session:
        return redirect(url_for('login'))

    # Get form data
    username = session['username']
    new_email = request.form.get('email', '').strip()
    new_password = request.form.get('password', '').strip()
    new_fullname = request.form.get('fullname', '').strip()

    # Validate email
    if not re.match(r"[^@]+@[^@]+\.[^@]+", new_email):
        return "Invalid email format", 400

    # Validate password
    if not new_password or len(new_password) < 8:
        return "Password must be at least 8 characters long", 400

    # Update user data
    users_db[username]['email'] = new_email
    users_db[username]['fullname'] = new_fullname

    # Update password if provided
    if new_password:
        users_db[username]['password_hash'] = check_password_hash(
            users_db[username]['password_hash'], new_password
        )

    return "Account updated successfully", 200

if __name__ == '__main__':
    app.run(debug=False)  # Ensure debug mode is off in production