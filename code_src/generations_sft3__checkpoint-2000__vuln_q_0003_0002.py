```python
from flask import Flask, request, jsonify, abort
from werkzeug.security import generate_password_hash, check_password_hash
import secrets
import re
from datetime import datetime, timedelta
import logging
from typing import Optional
import bleach

app = Flask(__name__)

# Configure secure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Secure secret key
app.config['SECRET_KEY'] = secrets.token_hex(32)

# Rate limiting
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["100 per day", "10 per hour"]
)

# Secure database connection (using SQLAlchemy)
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()
engine = create_engine('sqlite:///users.db', echo=True)
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    reset_token = Column(String(255), nullable=True)
    reset_token_expiry = Column(DateTime, nullable=True)

Base.metadata.create_all(engine)

def validate_email(email: str) -> bool:
    """Validate email format."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))

def validate_password(password: str) -> bool:
    """Validate password strength."""
    return (len(password) >= 12 and
            any(c.isupper() for c in password) and
            any(c.islower() for c in password) and
            any(c.isdigit() for c in password) and
            any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password))

@app.route('/reset_password', methods=['POST'])
@limiter.limit("5 per minute")
def reset_password():
    try:
        data = request.get_json()
        
        # Validate input
        if not data or 'email' not in data:
            abort(400, description="Missing email")
            
        email = data['email']
        
        # Validate email
        if not validate_email(email):
            abort(400, description="Invalid email format")
            
        # Check if user exists
        session = Session()
        user = session.query(User).filter_by(email=email).first()
        session.close()
        
        if not user:
            abort(404, description="User not found")
            
        # Generate secure token
        token = secrets.token_urlsafe(32)
        expiry = datetime.utcnow() + timedelta(hours=1)
        
        # Update user with token
        user.reset_token = token
        user.reset_token_expiry = expiry
        session = Session()
        session.add(user)
        session.commit()
        session.close()
        
        # Send reset email (implementation not shown)
        # ...
        
        return jsonify({"message": "Password reset instructions sent"}), 200
        
    except Exception as e:
        logger.error(f"Error during password reset: {str(e)}")
        abort(500, description="Internal server error")

@app.route('/reset_password/<token>', methods=['POST'])
def reset_password_with_token(token: str):
    try:
        # Validate token
        session = Session()
        user = session.query(User).filter_by(reset_token=token).first()
        session.close()
        
        if not user or user.reset_token_expiry