from functools import wraps
from flask import Flask, request, abort
from flask_login import login_required, current_user

app = Flask(__name__)

def require_auth(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(403)  # Forbidden
        return func(*args, **kwargs)
    return decorated

def require_admin(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)  # Forbidden
        return func(*args, **kwargs)
    return decorated

@app.route('/protected')
@login_required
def protected():
    return f"Hello, {current_user.username}!"

@app.route('/admin')
@require_admin
def admin():
    return "Admin area"

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Enable HTTPS