```python
import os
from flask import Flask, request, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import secrets
import re

app = Flask(__name__)

# Secure configuration
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///secure_forum.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Database setup
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

@app.before_request
def require_login():
    allowed_routes = ['login', 'register', 'index', 'view_messages']
    if request.endpoint not in allowed_routes and 'username' not in session:
        return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['username'] = username
            return redirect(url_for('index'))
        return 'Invalid credentials', 401
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            return 'Username and password are required', 400
        
        if len(password) < 8:
            return 'Password must be at least 8 characters', 400
        
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return 'Invalid username format', 400
        
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return 'Username already exists', 400
        
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/index')
def index():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

@app.route('/view_messages')
def view_messages():
    if 'username' not in session:
        return redirect(url_for('login'))
    messages = Message.query.order_by(Message.timestamp.desc()).all()
    return render_template('view_messages.html', messages=messages)

@app.route('/post_message', methods=['POST'])
def post_message():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    content = request.form.get('content')
    if not content or len(content) > 500: