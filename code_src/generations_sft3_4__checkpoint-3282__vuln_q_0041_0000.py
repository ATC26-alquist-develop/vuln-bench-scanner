from flask import Flask, request, render_template, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
import secrets
import re

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # Secure random secret key

# Simulated database (in production, use a proper database)
users = {}

# Secure password policy
def is_strong_password(password):
    return (len(password) >= 12 and
            re.search(r'[A-Z]', password) and
            re.search(r'[a-z]', password) and
            re.search(r'[0-9]', password) and
            re.search(r'[!@#$%^&*(),.?":{}|<>]', password))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        # Input validation
        if not username or not password:
            return "Username and password are required", 400
        
        if not is_strong_password(password):
            return "Password must be at least 12 chars with uppercase, lowercase, number, and special char", 400
        
        if username in users:
            return "Username already exists", 400
        
        # Securely hash password
        hashed_password = generate_password_hash(password)
        users[username] = hashed_password
        
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        if not username or not password:
            return "Username and password are required", 400
        
        stored_password = users.get(username)
        if stored_password and check_password_hash(stored_password, password):
            # In a real application, you would generate a session token here
            return "Login successful"
        else:
            return "Invalid credentials", 401
    
    return render_template('login.html')

if __name__ == '__main__':
    app.run(debug=False)  # Ensure debug mode off in production