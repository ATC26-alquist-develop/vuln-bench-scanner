from flask import Flask, request, session, redirect, url_for
from werkzeug.security import check_password_hash
import secrets
import re

app = Flask(__name__)

# Generate a secure random key for session management
app.secret_key = secrets.token_hex(32)

@app.route('/delete_account', methods=['POST'])
def delete_account():
    # Verify user is logged in
    if 'user_id' not in session:
        return "Unauthorized", 401
    
    # Verify user is authorized
    user = get_user_from_session(session['user_id'])
    if not user:
        return "Unauthorized", 401
    
    # Verify password
    if not check_password_hash(user.password_hash, request.form.get('password')):
        return "Invalid credentials", 401
    
    # Verify account is not already deleted
    if user.is_deleted:
        return "Account already deleted", 400
    
    # Delete user account
    user.is_deleted = True
    user.password_hash = None  # Clear password hash
    
    # Log the deletion attempt
    log_deletion_attempt(user.id)
    
    return redirect(url_for('account_deleted'))