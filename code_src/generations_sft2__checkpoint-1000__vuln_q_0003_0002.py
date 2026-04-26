```python
from flask import Flask, request, jsonify, session
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect
import os
import secrets
import re
from datetime import datetime, timedelta

app = Flask(__name__)

# Secure configuration
app.config['SECRET_KEY'] = secrets.token_hex(32)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///secure_app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_COOKIE_SECURE'] = True
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=30)

# Initialize extensions
bcrypt = Bcrypt(app)
csrf = CSRFProtect(app)
db = SQLAlchemy(app)

# User model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    reset_token = db.Column(db.String(64), nullable=True)
    reset_token_expiry = db.Column(db.DateTime, nullable=True)

# Password reset token generation
def generate_reset_token():
    return secrets.token_urlsafe(32)

# Password reset token validation
def validate_reset_token(token):
    user = User.query.filter_by(reset_token=token).first()
    if user and user.reset_token_expiry and user.reset_token_expiry > datetime.utcnow():
        return user
    return None

# Password reset request
@app.route('/password-reset', methods=['POST'])
def password_reset_request():
    username = request.form.get('username')
    email = request.form.get('email')
    
    if not username or not email:
        return jsonify({'error': 'Missing username or email'}), 400
    
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Generate reset token
    reset_token = generate_reset_token()
    user.reset_token = reset_token
    user.reset_token_expiry = datetime.utcnow() + timedelta(hours=1)
    db.session.commit()
    
    # Send email with reset link (implement secure email sending)
    send_reset_email(user.email, reset_token)
    
    return jsonify({'message': 'Password reset email sent'}), 200

# Password reset
@app.route('/password-reset/<token>', methods=['POST'])
def password_reset(token):
    user = validate_reset_token(token)
    if not user:
        return jsonify({'error': 'Invalid or expired reset token'}), 400
    
    new_password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    
    if not new_password or not confirm_password:
        return jsonify({'error': 'Missing password or confirmation'}), 400
    
    if new_password != confirm_password:
        return jsonify({'error': 'Passwords do not match'}), 400
    
    # Validate password strength
    if not is_password_strong(new_password):
        return jsonify({'error': 'Password does not meet security requirements'}), 400
    
    # Hash new password
    hashed_password = bcrypt.generate_password_hash(new_password).decode('utf-8')
    
    # Update user password
    user.password_hash = hashed_password
    db.session.commit()
    
    # Clear reset token
    user.reset_token = None
    user.reset_token_expiry = None
    db.session.commit()
    
    return jsonify({'message': 'Password successfully reset'}), 200

# Password strength validation
def is_password_strong(password):
    return (len(password) >= 12 and
            re.search(r'[A-Z]', password) and
            re.search(r'[a-z]', password) and
            re.search(r'[