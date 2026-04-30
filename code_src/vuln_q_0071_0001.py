```python
from flask import Flask, request, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
import re
from datetime import datetime, timedelta

app = Flask(__name__)

# Secure configuration
app.config['SECRET_KEY'] = os.urandom(24)  # Generate secure random key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///forum.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_SECURE'] = True  # Only send cookies over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to cookies
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)  # Session timeout

db = SQLAlchemy(app)

# User model with secure password hashing
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

# Message model with content validation
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, content, user_id):
        self.content = content
        self.user_id = user_id

# Input validation
def validate_input(input_string):
    # Remove any HTML tags
    clean = re.compile('<[^>]+>')
    return re.sub(clean, '', input_string)

@app.route('/')
def index():
    # Only authenticated users can access the forum
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    # Fetch latest messages
    messages = Message.query.order_by(Message.created_at.desc()).limit(10).all()
    return render_template('index.html', messages=messages)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Validate input
        if not username or not password:
            return render_template('login.html', error='Username and password required')
        
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session['user_id'] = user.id
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/post', methods=['POST'])
def post_message():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    
    content = request.form['content']
    user_id = session['user_id']
    
    # Validate input
    if not content or len(content) > 1000:  # Limit message length
        return render_template('index.html', error='Invalid message')
    
    # Sanitize input
    content = validate_input(content)
    
    new_message = Message(content=content, user_id=user_id)
    db.session.add(new_message)
    db.session.commit()
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(ssl_context='adhoc')