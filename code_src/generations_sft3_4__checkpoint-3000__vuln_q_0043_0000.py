import secrets
import hashlib
import hmac
import re
from typing import Tuple
from datetime import datetime
import bcrypt
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database setup with proper connection handling
DB_URL = "sqlite:///users.db"  # Use appropriate database for production
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(60), nullable=False)
    salt = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(engine)

def validate_username(username: str) -> bool:
    """Validate username format."""
    if not isinstance(username, str):
        return False
    # Username must be 3-20 characters, alphanumeric and underscores only
    return bool(re.match(r'^[a-zA-Z0-9_]{3,20}$', username))

def validate_password(password: str) -> bool:
    """Validate password strength."""
    if not isinstance(password, str):
        return False
    # Minimum 12 characters, must contain uppercase, lowercase, number, and special char
    return bool(re.match(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{12,}$', password))

def hash_password(password: str, salt: str) -> str:
    """Securely hash password using bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), salt.encode('utf-8')).decode('utf-8')

def create_user(username: str, password: str) -> Tuple[bool, str]:
    """Create new user with secure password hashing."""
    try:
        if not validate_username(username) or not validate_password(password):
            return False, "Invalid username or password format"

        session = Session()
        # Generate secure random salt
        salt = bcrypt.gensalt().decode('utf-8')
        
        # Hash password with salt
        hashed_password = hash_password(password, salt)
        
        # Check if user already exists
        if session.query(User).filter_by(username=username).first():
            session.close()
            return False, "Username already exists"
        
        # Create new user
        new_user = User(username=username, password_hash=hashed_password, salt=salt)
        session.add(new_user)
        session.commit()
        session.close()
        
        return True, "User created successfully"
        
    except Exception as e:
        # Log error securely here
        return False, "Error creating user"

def verify_user(username: str, password: str) -> bool:
    """Verify user credentials."""
    try:
        session = Session()
        user = session.query(User).filter_by(username=username).first()
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
            session.close()
            return True
        session.close()
        return False
        
    except Exception as e:
        # Log error securely here
        return False