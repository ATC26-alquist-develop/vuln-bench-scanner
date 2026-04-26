from flask import Flask, request, render_template, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import os
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # Secure secret key generation

# Simulated database (in production, use a real database)
users = {}

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            return "Username and password are required", 400
        
        if username in users:
            return "Username already exists", 400
        
        # Securely hash the password
        hashed_password = generate_password_hash(password)
        users[username] = hashed_password
        
        return redirect(url_for('login'))
    
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
            return redirect(url_for('home'))
        
        return "Invalid credentials", 401
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=False)  # Ensure debug mode is off in production