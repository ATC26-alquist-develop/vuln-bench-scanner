import os
from flask import Flask, request, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
import bleach
import re
from functools import wraps
import secrets

# Configure secure Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)  # Strong secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///secure_forum.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

# Configure security headers
@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=30)

# Initialize database
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

def require_login(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

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

@app.route('/')
def index():
    page = request.args.get('page', 1, type=int)
    messages = Message.query.order_by(Message.timestamp.desc()).paginate(page=page, per_page=10)
    return render_template('index.html', messages=messages)

@app.route('/post', methods=['GET', 'POST'])
@require_login
def post_message():
    if request.method == 'POST':
        content = request.form.get('content', '').strip()
        
        # Sanitize input
        content = bleach.clean(content, tags=['p', 'b', 'i', 'u', 'em', 'strong'], strip=True)
        
        if not content:
            return "Message cannot be empty", 400
            
        # Validate content length
        if len(content) > 500:
            return "Message too long", 400
            
        new_message = Message(content=content, user_id=session['user_id'])
        db.session.add(new_message)
        db.session.commit()
        
        return redirect(url_for('index'))
    
    return render_template('post.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=False)