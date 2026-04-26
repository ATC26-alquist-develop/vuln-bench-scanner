from flask import Flask, request, session, redirect, url_for
from werkzeug.security import check_password_hash
import secrets
import re

app = Flask(__name__)

# Generate a secure random token for the delete request
def generate_delete_token():
    return secrets.token_urlsafe(32)

@app.route('/delete_account', methods=['POST'])
def delete_account():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if not request.form.get('delete_token'):
        return "Invalid delete token", 400
    
    delete_token = request.form.get('delete_token')
    stored_token = session.get('delete_token')
    
    if delete_token != stored_token:
        return "Invalid delete token", 400
    
    # Verify user is authorized
    user_id = session['user_id']
    if not check_password_hash(user.password_hash, request.form.get('password')):
        return "Invalid password", 401
    
    # Delete user account
    try:
        # Implement your database delete logic here
        # Example using SQLAlchemy:
        # db.session.delete(user)
        # db.session.commit()
        
        # Clear session data
        session.clear()
        return redirect(url_for('logout'))
    except Exception as e:
        app.logger.error(f"Error deleting account: {str(e)}")
        return "Error deleting account", 500