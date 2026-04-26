from flask import Flask, request, session, redirect, url_for
from werkzeug.security import check_password_hash
from functools import wraps
import re

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Change this to a secure random value

# Simulated database
users = {
    'alice': {
        'username': 'alice',
        'email': 'alice@example.com',
        'password_hash': 'hashed_password_here'
    }
}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/update_settings', methods=['POST'])
@login_required
def update_settings():
    # Input validation
    username = request.form.get('username', '').strip()
    email = request.form.get('email', '').strip()
    
    if not username and not email:
        return "Username and email are required", 400
    
    if not re.match(r'^[a-zA-Z0-9_]{3,20}$', username):
        return "Invalid username format", 400
    
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        return "Invalid email format", 400
    
    if username and username != session['username']:
        if username not in users:
            return "Username does not exist", 400
    
    # Update user settings
    if username:
        users[session['username']]['username'] = username
    
    if email:
        users[session['username']]['email'] = email
    
    # Save changes to database (simulated here)
    # db.update_user(session['username'], username, email)
    
    return "Settings updated successfully", 200

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username', '').strip()
    password = request.form.get('password', '')
    
    if not username or not password:
        return "Username and password are required", 400
    
    if username not in users:
        return "Invalid username or password", 401
    
    if check_password_hash(users[username]['password_hash'], password):
        session['username'] = username
        return redirect(url_for('update_settings'))
    else:
        return "Invalid username or password", 401

if __name__ == '__main__':
    app.run(debug=False)  # Set to False in production