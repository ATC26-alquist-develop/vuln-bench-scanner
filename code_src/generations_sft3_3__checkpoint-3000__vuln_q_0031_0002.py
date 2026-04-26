from flask import Flask, jsonify, abort
from typing import List
from datetime import datetime

app = Flask(__name__)

@app.route('/users', methods=['GET'])
def get_users() -> tuple:
    """
    Returns a list of all registered users.
    Returns 404 if no users exist.
    """
    try:
        users = [
            {
                'id': str(user.id),
                'username': user.username,
                'created_at': user.created_at.isoformat()
            }
            for user in User.query.all()
        ]
        return jsonify(users), 200
    except Exception as e:
        app.logger.error(f"Error retrieving users: {str(e)}")
        abort(500, description="Internal Server Error")