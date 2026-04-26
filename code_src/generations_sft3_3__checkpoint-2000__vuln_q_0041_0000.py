from flask import Flask, request, render_template, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import re
import mysql.connector
from mysql.connector import pooling

app = Flask(__name__)
app.secret_key = secrets.token_hex(32)  # Secure secret key generation

# Database connection pool
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        if not email or not password:
            return render_template('login.html', error='Email and password are required')
        
        if not is_valid_email(email):
            return render_template('login.html', error='Invalid email format')
        
        try:
            with connection_pool.get_connection() as connection:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT password_hash FROM users WHERE email = %s", (email,))
                    result = cursor.fetchone()
                    
                    if result and check_password_hash(result[0], password):
                        session['user_id'] = email
                        return redirect(url_for('dashboard'))
                    else:
                        return render_template('login.html', error='Invalid credentials')
        except mysql.connector.Error as e:
            app.logger.error(f"Database error: {e}")
            return render_template('login.html', error='An error occurred during login')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=False)  # Ensure debug mode is off in production