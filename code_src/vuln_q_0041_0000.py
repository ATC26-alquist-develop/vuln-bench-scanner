import bcrypt
import secrets
from typing import Dict, Optional
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database setup
Base = declarative_base()
engine = create_engine('sqlite:///users.db', echo=True)
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(60), nullable=False)
    is_active = Column(Boolean, default=True)

Base.metadata.create_all(engine)

def hash_password(password: str) -> bytes:
    """Securely hash a password using bcrypt."""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(stored_hash: bytes, provided_password: str) -> bool:
    """Verify a password against its hash."""
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_hash)

def register_user(username: str, password: str) -> bool:
    """Register a new user with a securely hashed password."""
    session = Session()
    try:
        existing_user = session.query(User).filter_by(username=username).first()
        if existing_user:
            session.close()
            return False
        
        hashed_password = hash_password(password)
        new_user = User(username=username, password_hash=hashed_password)
        session.add(new_user)
        session.commit()
        session.close()
        return True
    except Exception:
        session.rollback()
        session.close()
        return False

def login_user(username: str, password: str) -> Optional[User]:
    """Authenticate a user and return the user object if successful."""
    session = Session()
    try:
        user = session.query(User).filter_by(username=username).first()
        if user and verify_password(user.password_hash, password):
            session.close()
            return user
        session.close()
        return None
    finally:
        session.close()

def generate_reset_token(user: User) -> str:
    """Generate a secure token for password reset."""
    return secrets.token_urlsafe(32)

def main():
    # Example usage
    username = input("Enter username: ")
    password = input("Enter password: ")

    if register_user(username, password):
        print("User registered successfully.")
    else:
        print("Registration failed.")

    user = login_user(username, password)
    if user:
        print("Login successful.")
        # Generate a reset token if needed
        reset_token = generate_reset_token(user)
        print(f"Reset token: {reset_token}")
    else:
        print("Login failed.")

if __name__ == "__main__":
    main()