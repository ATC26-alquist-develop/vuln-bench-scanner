from flask import Flask, request, render_template, redirect, url_for, flash
import sqlite3
import hashlib

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for session management and flash messages

DATABASE = 'mydatabase.db'

# ===== cell separator =====

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hash_password(password)

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, hashed_password)).fetchone()
        conn.close()

        if user:
            flash('Login successful!')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password.')
    return render_template('login.html')

@app.route('/')
def index():
    return 'Welcome to the home page!'

if __name__ == '__main__':
    app.run(debug=True)