import secrets
import hashlib
import hmac
import re
from typing import Tuple
from datetime import datetime, timedelta
import bcrypt
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

# Database setup with proper connection handling
DB_URL = "sqlite:///users.db"  # Use appropriate database for production
engine = create_engine(DB_URL, connect_args={"check_same_thread": False})
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(60), nullable=False)
    salt = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)

Base.metadata.create_all(engine)

def generate_salt() -> str:
    """Generate a cryptographically secure random salt."""
    return secrets.token_hex(16)

def hash_password(password: str, salt: str) -> str:
    """Securely hash password using bcrypt with salt."""
    return bcrypt.hashpw(password.encode('utf-8'), salt.encode('utf-8')).decode('utf-8')

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
        if not validate_username(username) or not validate_password(password):
            return False, "Invalid username or password format"

        # Generate salt and hash password
        salt = generate_salt()
        password_hash = hash_password(password, salt)

        # Store user with hashed password and salt
        session = sessionmaker(bind=engine)()
        try:
            new_user = User(username=username, password_hash=password_hash, salt=salt)
            session.add(new_user)
            session.commit()
            return True, "User registered successfully"
        except SQLAlchemyError as e:
            session.rollback()
            return False, "Database error occurred"
        finally:
            session.close()

    except Exception as e:
        return False, "Registration failed"

def verify_user(username: str, password: str) -> bool:
    """
    Verify user credentials securely.
    Returns: bool
    """
    try:
        session = sessionmaker(bind=engine)()
        try:
            user = session.query(User).filter_by(username=username).first()
            if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
                user.last_login = datetime.utcnow()
                session.commit()
                return True
            return False
        finally:
            session.close()
    except Exception:
        return False