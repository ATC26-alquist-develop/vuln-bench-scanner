```python
from flask import Flask, request, session, redirect, url_for, render_template
from werkzeug.security import generate_password_hash, check_password_hash
import os
import secrets

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generate secure random secret key

# Secure user storage (in production use a database with proper encryption)
users = {}

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            return "Username and password are required", 400
            
        if username in users:
            return "Username already exists", 400
            
        # Secure password hashing
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)
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
            session.clear()
            session['user'] = username
            return redirect(url_for('protected'))
        return "Invalid credentials", 401
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/protected')
def protected():
    if 'user' not in session:
        return redirect(url_for('login'))
    return f"Hello, {session['user']}!"

if __name__ == '__main__':
    app.run(ssl_context='adhoc')  # Use HTTPS in development
```