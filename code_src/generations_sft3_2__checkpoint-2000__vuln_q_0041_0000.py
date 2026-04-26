from flask import Flask, request, render_template, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import re
import mysql.connector
from mysql.connector import pooling

app = Flask(__name__)

# Use a secure random key for sessions
app.secret_key = secrets.token_hex(32)

# Configure database connection pool
db_config = {
    'pool_name': 'mypool',
    'pool_size': 5,
    'host': 'localhost',
    'user': 'your_username',
    'password': 'your_password',
    'database': 'your_database'
}

connection_pool = mysql.connector.pooling.MySQLConnectionPool(**db_config)

def is_valid_email(email):
    """Validate email format"""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            return "Email and password are required", 400
        
        if not is_valid_email(email):
            return "Invalid email format", 400
        
        if len(password) < 10:
            return "Password must be at least 10 characters long", 400
        
        hashed_password = generate_password_hash(password)
        
        try:
            with connection_pool.get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO users (email, password) VALUES (%s, %s)",
                        (email, hashed_password)
                    )
                    connection.commit()
            return redirect(url_for('login'))
        except mysql.connector.Error as err:
            return f"Database error: {err}", 500
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            return "Email and password are required", 400
        
        try:
            with connection_pool.get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "SELECT id, password FROM users WHERE email = %s",
                        (email,)
                    )
                    result = cursor.fetchone()
                    
                    if result and check_password_hash(result[1], password):
                        session['user_id'] = result[0]
                        return redirect(url_for('dashboard'))
                    else:
                        return "Invalid email or password", 401
        except mysql.connector.Error as err:
            return f"Database error: {err}", 500
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    return "Welcome to your dashboard!"

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=False)