from flask import Flask, request, session
from werkzeug.security import safe_str_cmp
from sqlalchemy import text
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # Secure secret key generation

@app.route('/delete_account', methods=['POST'])
def delete_account():
    if 'user_id' not in session:
        return {'error': 'Unauthorized'}, 401
    
    user_id = session['user_id']
    
    try:
        # Use parameterized query to prevent SQL injection
        with app.db.connect() as conn:
            result = conn.execute(
                text("DELETE FROM users WHERE id = :user_id"),
                {"user_id": user_id}
            )
            
        if result.rowcount == 0:
            return {'error': 'User not found'}, 404
            
        # Clear session data
        session.clear()
        
        # Log the deletion attempt
        app.logger.info(f"Account {user_id} deleted by user {session.get('user_id', 'unknown')}")
        
        return {'message': 'Account deleted successfully'}, 200
        
    except Exception as e:
        app.logger.error(f"Error deleting account: {str(e)}")
        return {'error': 'Internal server error'}, 500