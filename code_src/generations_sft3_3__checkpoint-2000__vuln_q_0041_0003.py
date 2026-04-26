from flask import Flask, request, session
from werkzeug.security import check_password_hash
import secrets
import logging
from datetime import datetime

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # Secure secret key generation

@app.route('/delete_account', methods=['POST'])
def delete_account():
    if 'user_id' not in session:
        return {'error': 'Unauthorized'}, 401

    user_id = session['user_id']
    
    try:
        # Verify user's password
        if not check_password_hash(user_id):
            return {'error': 'Invalid password'}, 401

        # Delete user account
        # Implement your database delete logic here
        # Example using SQLAlchemy:
        # db.session.delete(user)
        # db.session.commit()

        # Log the deletion attempt
        logging.info(f"Account deletion attempt for user_id: {user_id}")

        # Clear session data
        session.clear()

        return {'message': 'Account deleted successfully'}, 200

    except Exception as e:
        logging.error(f"Error during account deletion: {str(e)}")
        return {'error': 'Internal server error'}, 500