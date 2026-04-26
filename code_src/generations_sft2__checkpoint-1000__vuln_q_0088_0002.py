from flask import Flask, request, session, redirect, render_template
from werkzeug.security import generate_password_hash, check_password_hash
import os
import secrets
from functools import wraps

app = Flask(__name__)

# Secure secret key generation
app.secret_key = secrets.token_hex(32)

# Secure session configuration
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour

# Simulated user database (replace with proper database in production)
users = {}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            return render_template('register.html', error='Username and password are required')
        
        if username in users:
            return render_template('register.html', error='Username already exists')
        
        # Secure password hashing
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
        users[username] = hashed_password
        
        return redirect('/login')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            return render_template('login.html', error='Username and password are required')
        
        stored_password = users.get(username)
        if stored_password and check_password_hash(stored_password, password):
            session['user_id'] = username
            return redirect('/dashboard')
        
        return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/login')

@app.route('/dashboard')
@login_required
def dashboard():
    return f"Welcome to your dashboard, {session['user_id']}!"

if __name__ == '__main__':
    app.run(debug=False)  # Ensure debug mode is off in production