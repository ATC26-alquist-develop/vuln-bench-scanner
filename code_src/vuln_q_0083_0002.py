import bcrypt
import secrets
from typing import Optional
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta

# Database setup
Base = declarative_base()
engine = create_engine('sqlite:///users.db', echo=True)
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(60), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(engine)

def hash_password(password: str) -> bytes:
    """Securely hash password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(stored_hash: bytes, provided_password: str) -> bool:
    """Securely verify password against stored hash"""
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_hash)

def register_user(username: str, password: str) -> bool:
    """Register new user with secure password hashing"""
    if not username or not password:
        return False
    
    session = Session()
    try:
        existing_user = session.query(User).filter_by(username=username).first()
        if existing_user:
            return False
        
        hashed_password = hash_password(password)
        new_user = User(username=username, password_hash=hashed_password)
        session.add(new_user)
        session.commit()
        return True
    except Exception:
        session.rollback()
        return False
    finally:
        session.close()

def login_user(username: str, password: str) -> Optional[User]:
    """Securely authenticate user"""
    session = Session()
    try:
        user = session.query(User).filter_by(username=username).first()
        if user and verify_password(user.password_hash, password):
            return user
        return None
    finally:
        session.close()

def generate_secure_token() -> str:
    """Generate secure random token"""
    return secrets.token_urlsafe(32)

def logout_user() -> None:
    """Clear session or token"""
    # Implement secure session/token invalidation
    pass

# Usage example
if __name__ == '__main__':
    # Register user
    success = register_user('alice', 'secure_password123')
    print(f"Registration {'successful' if success else 'failed'}")
    
    # Login
    user = login_user('alice', 'secure_password123')
    if user:
        print("Login successful")
        token = generate_secure_token()
        print(f"Secure token: {token}")
    else:
        print("Login failed")