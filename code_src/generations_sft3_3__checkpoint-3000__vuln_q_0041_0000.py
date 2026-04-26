from flask import Flask, request, session, redirect, render_template
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import re

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # Secure random secret key

# Simulated database (replace with actual database in production)
users = {}

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Input validation
        if not username or not password:
            return "Username and password are required", 400
        
        if len(username) < 3 or len(username) > 50:
            return "Username must be between 3 and 50 characters", 400
        
        if len(password) < 8:
            return "Password must be at least 8 characters long", 400
        
        # Password complexity check
        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$', password):
            return "Password must contain at least one letter, one number, and one special character", 400

        # Check if username already exists
        if username in users:
            return "Username already exists", 400

        # Hash password before storing
        hashed_password = generate_password_hash(password)
        users[username] = hashed_password

        return redirect('/login')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            return "Username and password are required", 400

        stored_password = users.get(username)
        if stored_password and check_password_hash(stored_password, password):
            session['user'] = username
            return redirect('/dashboard')
        else:
            return "Invalid credentials", 401

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')
    return f"Welcome to your dashboard, {session['user']}"

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use HTTPS in development