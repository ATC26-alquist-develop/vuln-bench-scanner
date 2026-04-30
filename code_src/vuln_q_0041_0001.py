from flask import Flask, request, render_template, redirect, url_for, session
from werkzeug.security import check_password_hash, generate_password_hash
import re
import os
from datetime import datetime, timedelta

app = Flask(__name__)

# Secure secret key generation
app.secret_key = os.urandom(24)

# Secure session configuration
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

# Simulated database (replace with actual database in production)
users = {}

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username and password:
            if username in users and check_password_hash(users[username]['password'], password):
                session['user'] = username
                session.permanent = True
                return redirect(url_for('profile'))
        
        return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    user = session['user']
    
    if request.method == 'POST':
        # Validate and sanitize input
        name = request.form.get('name')
        email = request.form.get('email')
        new_password = request.form.get('new_password')
        
        # Input validation
        if not name or not email or not new_password:
            return render_template('profile.html', error='All fields are required')
        
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return render_template('profile.html', error='Invalid email format')
        
        # Update user data
        users[user] = {
            'name': name,
            'email': email,
            'password': generate_password_hash(new_password) if new_password else None
        }
        
        return redirect(url_for('profile'))
    
    return render_template('profile.html', user=user)

if __name__ == '__main__':
    app.run(debug=False)