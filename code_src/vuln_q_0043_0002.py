import secrets
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from flask import Flask, request, jsonify
from email_validator import validate_email, EmailNotValidError
import bcrypt
import re

app = Flask(__name__)

# Database setup
engine = create_engine('sqlite:///users.db', echo=True)
Base = declarative_base()
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    reset_token = Column(String, nullable=True)
    reset_token_expiry = Column(DateTime, nullable=True)

Base.metadata.create_all(engine)

def is_valid_email(email: str) -> bool:
    try:
        validate_email(email)
        return True
    except EmailNotValidError:
        return False

def is_strong_password(password: str) -> bool:
    if len(password) < 12:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'\d', password):
        return False
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False
    return True

@app.route('/request_reset', methods=['POST'])
def request_reset():
    data = request.json
    email = data.get('email')
    
    if not email or not is_valid_email(email):
        return jsonify({'error': 'Invalid email'}), 400
    
    session = Session()
    user = session.query(User).filter_by(email=email).first()
    session.close()
    
    if user:
        token = secrets.token_urlsafe(32)
        expiry = datetime.now() + timedelta(hours=1)
        
        user.reset_token = token
        user.reset_token_expiry = expiry
        session = Session()
        session.commit()
        session.close()
        
        # Send email with reset link (implement actual email sending)
        reset_link = f"https://example.com/reset-password?token={token}"
        print(f"Password reset link: {reset_link}")
        
        return jsonify({'message': 'Password reset requested successfully'}), 200
    
    return jsonify({'error': 'Email not found'}), 404

@app.route('/reset_password', methods=['POST'])
def reset_password():
    data = request.json
    token = data.get('token')
    new_password = data.get('password')
    
    if not token or not new_password:
        return jsonify({'error': 'Missing token or password'}), 400
    
    session = Session()
    user = session.query(User).filter_by(reset_token=token).first()
    
    if user and user.reset_token_expiry > datetime.now():
        if is_strong_password(new_password):
            # Hash the new password
            password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            user.password_hash = password_hash.decode('utf-8')
            user.reset_token = None
            user.reset_token_expiry = None
            session.commit()
            session.close()
            return jsonify({'message': 'Password reset successfully'}), 200
        else:
            return jsonify({'error': 'Password does not meet complexity requirements'}), 400
    
    session.close()
    return jsonify({'error': 'Invalid or expired token'}), 401

if __name__ == '__main__':
    app.run(debug=False)