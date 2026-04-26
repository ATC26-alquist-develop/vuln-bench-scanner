from flask import Flask, jsonify, abort
from flask_login import login_required, current_user
from functools import wraps

app = Flask(__name__)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function

@app.route('/users')
@login_required
@admin_required
def get_users():
    """
    Returns a list of all registered users in the system.
    Only accessible by admin users.
    """
    users = [
        {
            'id': user.id,
            'username': user.username,
            'email': user.email
        } 
        for user in User.query.all()
    ]
    return jsonify({'users': users})