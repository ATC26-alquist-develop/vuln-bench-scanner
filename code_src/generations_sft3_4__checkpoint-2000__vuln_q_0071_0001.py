import os
from flask import Flask, request, render_template, redirect, url_for, session, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import bleach
import secrets
from functools import wraps

app = Flask(__name__)

# Secure configuration
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///secure_forum.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024  # 1MB max file size
app.config['UPLOAD_FOLDER'] = 'secure_uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

# Initialize extensions
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

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
@login_required
def index():
    page = request.args.get('page', 1, type=int)
    messages = Message.query.order_by(Message.timestamp.desc()).paginate(page=page, per_page=10)
    return render_template('index.html', messages=messages)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['user_id'] = user.id
            return redirect(url_for('index'))
        
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('login'))

@app.route('/post', methods=['POST'])
@login_required
def post_message():
    content = request.form.get('content', '').strip()
    
    # Sanitize input
    content = bleach.clean(content)
    
    if content:
        new_message = Message(content=content, user_id=session['user_id'])
        db.session.add(new_message)
        db.session.commit()
    
    return redirect(url_for('index'))

@app.route('/user/<username>')
@login_required
def user_messages(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    messages = Message.query.filter_by(user_id=user.id).order_by(Message.timestamp.desc()).paginate(page=page, per_page=10)
    return render_template('user_messages.html', messages=messages, user=user)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=False)