from flask import Flask, abort, request, redirect, url_for
from flask_login import LoginManager, login_required, current_user
from functools import wraps

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'  # Change this to a strong, random secret key
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    # Implement your user loading logic here
    # For example: return User.query.get(int(user_id))
    pass

def require_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)  # Forbidden
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin')
@login_required
@require_admin
def admin_page():
    return "Admin page"

@app.route('/user')
@login_required
def user_page():
    return "User page"

if __name__ == '__main__':
    app.run(debug=False)  # Ensure debug mode is off in production