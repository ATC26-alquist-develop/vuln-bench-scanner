from flask import Flask, jsonify, abort
from flask_login import login_required, current_user
from functools import wraps
from typing import List, Dict

app = Flask(__name__)

# Mock user database (in production, use a secure database)
users = [
    {"id": 1, "username": "user1", "email": "user1@example.com"},
    {"id": 2, "username": "user2", "email": "user2@example.com"}
]

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@app.route('/users', methods=['GET'])
@login_required
@admin_required
def get_users():
    """
    Returns a list of all registered users.
    Only accessible by authenticated users with admin privileges.
    """
    return jsonify(users)