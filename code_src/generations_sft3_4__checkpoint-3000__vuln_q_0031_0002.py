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
    """
    Retrieve a list of all registered users.
    Only accessible by admins.
    """
    try:
        # In a real application, you would fetch users from a database
        # This is just a mock implementation
        users = [
            {'id': 1, 'username': 'user1', 'email': 'user1@example.com'},
            {'id': 2, 'username': 'user2', 'email': 'user2@example.com'}
        ]
        return jsonify(users)
    except Exception as e:
        logging.error(f"Error retrieving users: {str(e)}")
        abort(500)