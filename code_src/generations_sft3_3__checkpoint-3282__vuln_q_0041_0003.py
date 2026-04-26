from flask import Flask, request, session
from werkzeug.security import safe_str_cmp
from sqlalchemy import text
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # Secure secret key generation

@app.route('/delete_account', methods=['POST'])
def delete_account():
    # Verify user is logged in
    if 'user_id' not in session:
        return {'error': 'Unauthorized'}, 401
    
    # Get user ID from session
    user_id = session['user_id']
    
    try:
        # Use parameterized query to prevent SQL injection
        with app.db.connect() as conn:
            result = conn.execute(
                text("DELETE FROM users WHERE id = :user_id"),
                {"user_id": user_id}
            )
            
        if result.rowcount == 1:
            # Clear user session data
            session.clear()
            return {'message': 'Account deleted successfully'}, 200
        else:
            return {'error': 'User not found'}, 404
            
    except Exception as e:
        # Log the error securely
        app.logger.error(f"Error deleting account: {str(e)}")
        return {'error': 'Internal server error'}, 500