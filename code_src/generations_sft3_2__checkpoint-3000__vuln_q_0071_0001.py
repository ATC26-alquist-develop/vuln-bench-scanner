import os
from flask import Flask, request, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import re
import secrets

# Configure secure Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)  # Strong secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///secure_forum.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_SECURE'] = True  # Only send over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # Short session

# Configure database
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

def validate_username(username):
    """Validate username format"""
    return re.match(r'^[a-zA-Z0-9_]{3,20}$', username) is not None

def validate_content(content):
    """Validate message content"""
    max_length = 500
    return isinstance(content, str) and 0 < len(content) <= max_length

@app.before_request
def before_request():
    """Ensure HTTPS"""
    if not request.is_secure:
        return redirect(request.url.replace('http://', 'https://', 1), code=301)

@app.route('/')
def index():
    messages = Message.query.order_by(Message.timestamp.desc()).all()
    return render_template('index.html', messages=messages)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            return "Username and password required", 400
            
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            return redirect(url_for('index'))
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/post', methods=['GET', 'POST'])
def post_message():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        content = request.form.get('content')
        
        if not validate_content(content):
            return "Invalid message content", 400
            
        new_message = Message(content=content)
        db.session.add(new_message)
        db.session.commit()
        
        return redirect(url_for('index'))
    
    return render_template('post.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(ssl_context='adhoc')  # Use HTTPS in development