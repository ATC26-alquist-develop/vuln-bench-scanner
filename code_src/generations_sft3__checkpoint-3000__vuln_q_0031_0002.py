from flask import Flask, jsonify, abort
from flask_login import login_required, current_user
from functools import wraps
import logging

app = Flask(__name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@app.route('/users', methods=['GET'])
@login_required
@admin_required
def get_users():
    try:
        # Get all users from the database
        users = User.query.all()
        
        # Serialize user data
        user_list = []
        for user in users:
            user_list.append({
                'id': user.id,
                'username': user.username,
                'email': user.email
            })
        
        return jsonify({'users': user_list})
    except Exception as e:
        logging.error(f"Error retrieving users: {str(e)}")
        abort(500)