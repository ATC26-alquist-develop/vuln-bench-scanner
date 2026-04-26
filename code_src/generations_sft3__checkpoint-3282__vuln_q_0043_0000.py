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

def generate_salt() -> str:
    """Generate a cryptographically secure random salt."""
    return secrets.token_hex(16)

def hash_password(password: str, salt: str) -> str:
    """Securely hash password using bcrypt with salt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def validate_username(username: str) -> bool:
    """Validate username format."""
    return bool(re.match(r'^[a-zA-Z0-9_]{3,50}$', username))

def validate_password(password: str) -> bool:
    """Validate password strength."""
    return len(password) >= 12 and any(c.isupper() for c in password) and \
           any(c.islower() for c in password) and any(c.isdigit() for c in password)

def register_user(username: str, password: str) -> Tuple[bool, str]:
    """
    Register a new user with secure password hashing.
    Returns: Tuple of (success: bool, message: str)
    """
    try:
        # Input validation
        if not validate_username(username):
            return False, "Invalid username format"
        if not validate_password(password):
            return False, "Password does not meet complexity requirements"

        # Generate salt and hash password
        salt = generate_salt()
        password_hash = hash_password(password, salt)

        # Create user
        session = Session()
        try:
            new_user = User(username=username, password_hash=password_hash, salt=salt)
            session.add(new_user)
            session.commit()
            return True, "User registered successfully"
        finally:
            session.close()

    except Exception as e:
        # Log error securely without exposing sensitive details
        return False, "Registration failed"
    finally:
        # Ensure session is closed
        if 'session' in locals():
            session.close()

    return False, "Unknown error occurred"