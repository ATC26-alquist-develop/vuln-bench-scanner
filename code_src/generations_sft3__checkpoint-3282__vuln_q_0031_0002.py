from flask import Flask, jsonify, abort
from flask_login import login_required, current_user
from functools import wraps
from typing import List

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
    users = [
        {
            'id': user.id,
            'username': user.username,
            'email': user.email
        } 
        for user in current_user.get_followed_users()
    ]
    return jsonify(users)