from flask import Flask, request, session, redirect, url_for, render_template
from werkzeug.security import check_password_hash
from functools import wraps
import re

app = Flask(__name__)
app.secret_key = 'your-secret-key'  # Change this to a strong, random key

# Simulated database - replace with actual database in production
users = {
    'user1': {'username': 'user1', 'email': 'user1@example.com', 'password_hash': 'hashed_password_here'}
}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/update_settings', methods=['GET', 'POST'])
@login_required
def update_settings():
    if request.method == 'POST':
        # Validate and sanitize input
        username = request.form.get('username', '').strip()
        email = request.form.get('email', '').strip()
        
        # Input validation
        if not username or not email:
            return "Username and email are required", 400
        
        if not re.match(r'^[a-zA-Z0-9_]{3,20}$', username):
            return "Invalid username format", 400
        
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return "Invalid email format", 400
        
        # Update user settings
        session['username'] = username
        session['email'] = email
        
        return "Settings updated successfully", 200
    
    return render_template('update_settings.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if username in users and check_password_hash(users[username]['password_hash'], password):
            session['username'] = username
            return redirect(url_for('update_settings'))
        else:
            return "Invalid credentials", 401
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=False)  # Set to False in production