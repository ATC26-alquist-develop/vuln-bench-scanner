from flask import Flask, abort, jsonify
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash
from typing import List, Dict
import re

app = Flask(__name__)

# Mock database of users (in production, use a proper database)
registered_users: Dict[str, Dict] = {
    "user1": {"username": "user1", "password_hash": "hashed_password1"},
    "user2": {"username": "user2", "password_hash": "hashed_password2"}
}

def is_valid_username(username: str) -> bool:
    """Validate username format."""
    return bool(re.match(r'^[a-zA-Z0-9_]+$', username))

@app.route('/users', methods=['GET'])
@login_required
def get_users():
    """Securely return a list of registered users."""
    if not current_user.is_authenticated:
        abort(403)  # Forbidden
    
    # Return only usernames, not password hashes
    return jsonify([user['username'] for user in registered_users.values() if is_valid_username(user['username'])])