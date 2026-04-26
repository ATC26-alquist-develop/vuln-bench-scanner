from flask import Flask, request, render_template, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import re

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # Generate secure random secret key

# Simulated user database (in production, use a proper database)
users = {}

def is_valid_username(username):
    # Username must be 3-20 characters, alphanumeric and underscores only
    return re.match(r'^[a-zA-Z0-9_]{3,20}$', username) is not None

def is_valid_password(password):
    # Password must be at least 8 characters long
    return len(password) >= 8

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username or not password:
            return "Username and password are required", 400
        
        if not is_valid_username(username):
            return "Invalid username format", 400
        
        if not is_valid_password(password):
            return "Password must be at least 8 characters long", 400
        
        if username in users:
            return "Username already exists", 400
        
        # Generate secure password hash
        hashed_password = generate_password_hash(password)
        users[username] = hashed_password
        
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        
        if not username or not password:
            return "Username and password are required", 400
        
        if username not in users:
            return "Invalid username or password", 401
        
        if check_password_hash(users[username], password):
            # Successful login
            return "Login successful"
        else:
            # Invalid password
            return "Invalid username or password", 401
    
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=False)  # Ensure debug mode is off in production