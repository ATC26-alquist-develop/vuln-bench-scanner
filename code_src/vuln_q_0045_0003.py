from flask import Flask, request, session, redirect, render_template
from werkzeug.security import generate_password_hash, check_password_hash
import os
import secrets
from datetime import datetime, timedelta

app = Flask(__name__)

# Secure secret key generation
app.secret_key = secrets.token_hex(32)

# Secure session configuration
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

# Simulated secure database (replace with actual database in production)
users_db = {}

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            return "Username and password are required", 400
            
        if username in users_db:
            return "Username already exists", 400
            
        # Secure password hashing
        hashed_password = generate_password_hash(password)
        users_db[username] = hashed_password
        
        return redirect('/login')
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            return "Username and password are required", 400
            
        stored_password = users_db.get(username)
        if stored_password and check_password_hash(stored_password, password):
            session.clear()
            session['user'] = username
            session.permanent = True
            return redirect('/dashboard')
        else:
            return "Invalid credentials", 401
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect('/login')
    return f"Welcome, {session['user']}!"

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Enable HTTPS in development