```python
from flask import Flask, request, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import os
import re
from datetime import datetime
import jwt
from functools import wraps

app = Flask(__name__)

# Secure configuration
app.config['SECRET_KEY'] = os.urandom(24)  # Generate secure random key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///secure_status.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = 1800  # 30 minutes

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class Status(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(280), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return {'message': 'Token is missing'}, 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(id=data['user_id']).first()
        except:
            return {'message': 'Token is invalid'}, 401
        return f(current_user, *args, **kwargs)
    return decorated

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if not username or not password:
            return {'message': 'Username and password are required'}, 400
        
        if User.query.filter_by(username=username).first():
            return {'message': 'Username already exists'}, 400
        
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_user = User(username=username, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user and bcrypt.check_password_hash(user.password_hash, password):
            token = jwt.encode({
                'user_id': user.id,
                'exp': datetime.utcnow() + timedelta(hours=1)
            }, app.config['SECRET_KEY'], algorithm="HS256")
            return {'token': token}
        
        return {'message': 'Invalid credentials'}, 401
    
    return render_template('login.html')

@app.route('/status', methods=['POST'])
@token_required
def create_status(current_user):
    content = request.form['content']
    
    if not content or len(content) > 280:
        return {'message': 'Invalid content'}, 400
    
    if not re.match(r'^[a-zA-Z0-9\s,!?]+$', content):
        return {'message': 'Content contains invalid characters'}, 400
    
    new_status = Status(content=content, user_id=current_user.id)
    db.session