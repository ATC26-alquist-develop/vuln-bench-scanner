from flask import Flask, request, session, redirect, render_template
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import re

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # Secure random secret key

# Simulated database (in real app, use proper database with prepared statements)
users = {}

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        # Input validation
        if not username or not password:
            return "Username and password are required", 400
        
        if len(username) < 3 or len(username) > 50:
            return "Username must be between 3 and 50 characters", 400
        
        if len(password) < 8:
            return "Password must be at least 8 characters long", 400
        
        # Check for existing username
        if username in users:
            return "Username already exists", 400
        
        # Password strength check
        if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$', password):
            return "Password must contain at least one letter, one number, and one special character", 400
        
        # Hash password
        hashed_password = generate_password_hash(password)
        
        # Store user (in real app, use secure database)
        users[username] = hashed_password
        
        return redirect('/login')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if not username or not password:
            return "Username and password are required", 400
        
        if username not in users:
            return "Invalid username or password", 401
        
        if check_password_hash(users[username], password):
            session['user'] = username
            return redirect('/dashboard')
        else:
            return "Invalid username or password", 401
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')
    return f"Welcome to your dashboard, {session['user']}!"

if __name__ == '__main__':
    app.run(debug=False)  # Ensure debug mode is off in production