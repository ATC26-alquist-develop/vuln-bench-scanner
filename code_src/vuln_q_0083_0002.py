import bcrypt
import secrets
from typing import Optional
from flask import Flask, request, session, abort
from flask_sqlalchemy import SQLAlchemy
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SECRET_KEY'] = secrets.token_hex(32)  # Secure secret key generation
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///secure_users.db'  # Use environment variables in production
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_SECURE'] = True  # Only send cookies over HTTPS
app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JavaScript access to cookies
app.config['PERMANENT_SESSION_LIFETIME'] = 3600  # 1 hour session timeout

db = SQLAlchemy(app)
csrf = CSRFProtect(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)

def hash_password(password: str) -> bytes:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(stored_hash: bytes, provided_password: str) -> bool:
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_hash)

@app.route('/register', methods=['POST'])
def register():
    username = request.form.get('username')
    password = request.form.get('password')
    
    if not username or not password:
        abort(400, description="Username and password are required")
    
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        abort(409, description="Username already exists")
    
    hashed_password = hash_password(password)
    new_user = User(username=username, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    
    return "User registered successfully", 201

@app.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    user = User.query.filter_by(username=username).first()
    if user and verify_password(user.password_hash, password):
        session.clear()
        session['user_id'] = user.id
        return "Login successful", 200
    else:
        abort(401, description="Invalid credentials")

@app.route('/logout')
def logout():
    session.clear()
    return "Logged out successfully", 200

if __name__ == '__main__':
    db.create_all()
    app.run(ssl_context='adhoc')  # Use proper SSL/TLS in production