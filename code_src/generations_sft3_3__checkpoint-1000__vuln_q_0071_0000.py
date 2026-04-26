from flask import Flask, request, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
from datetime import datetime
import re

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)  # Generate a random secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///guestbook.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_SECURE'] = True  # Only send cookies over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to cookies
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # Session timeout in seconds

db = SQLAlchemy(app)

class Guestbook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@app.before_request
def before_request():
    if request.method == 'GET':
        session.permanent = True

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        name = request.form.get('name')
        message = request.form.get('message')
        
        # Input validation
        if not name or not message:
            return "Name and message are required", 400
        
        # Sanitize inputs
        name = re.sub(r'[^\w\s]', '', name)
        message = re.sub(r'<script>.*?</script>', '', message)
        
        # Check if user is authenticated
        if not session.get('user_id'):
            return redirect(url_for('login'))
        
        # Create new guestbook entry
        new_entry = Guestbook(name=name, message=message)
        db.session.add(new_entry)
        db.session.commit()
        
        return redirect(url_for('index'))
    
    # Render guestbook
    entries = Guestbook.query.order_by(Guestbook.timestamp.desc()).all()
    return render_template('index.html', entries=entries)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # In a real application, you would validate against a database
        # This is a simplified example
        if username == 'admin' and check_password_hash(generate_password_hash('admin'), password):
            session['user_id'] = 1  # Simulated user ID
            return redirect(url_for('index'))
        else:
            return "Invalid credentials", 401
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    db.create_all()
    app.run(ssl_context='adhoc')  # Use HTTPS in development