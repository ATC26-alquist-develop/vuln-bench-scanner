from flask import Flask, request, jsonify
from flask_httpauth import HTTPBasicAuth
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# User loader callback
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# User model
class User(UserMixin):
    def __init__(self, user_id):
        self.id = user_id

# Authentication
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'admin':
        return 'password'
    return None

# Routes
@app.route('/')
@login_required
def home():
    return "Welcome, " + current_user.id

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    
    if username == 'admin' and password == 'password':
        user = User(username)
        login_user(user)
        return jsonify({'message': 'Login successful'})
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful'})

if __name__ == '__main__':
    app.run(debug=True)