import bcrypt
import secrets
import re
from typing import Optional
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from argon2 import PasswordHasher

# Database setup
Base = declarative_base()
engine = create_engine('sqlite:///users.db', echo=True)
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(60), nullable=False)

Base.metadata.create_all(engine)

# Password hashing
ph = PasswordHasher()

def validate_username(username: str) -> bool:
    """Validate username format"""
    return bool(re.match(r'^[a-zA-Z0-9_]{3,50}$', username))

def validate_password(password: str) -> bool:
    """Validate password strength"""
    return len(password) >= 12 and any(c.isupper() for c in password) and \
           any(c.islower() for c in password) and any(c.isdigit() for c in password)

def register_user(username: str, password: str) -> bool:
    """Register new user with secure password hashing"""
    if not validate_username(username) or not validate_password(password):
        return False

    try:
        with Session() as session:
            existing_user = session.query(User).filter_by(username=username).first()
            if existing_user:
                return False

            password_hash = ph.hash(password)
            new_user = User(username=username, password_hash=password_hash)
            session.add(new_user)
            session.commit()
            return True
    except Exception:
        session.rollback()
        return False

def authenticate_user(username: str, password: str) -> bool:
    """Authenticate user with secure password verification"""
    try:
        with Session() as session:
            user = session.query(User).filter_by(username=username).first()
            if not user:
                return False

            try:
                ph.verify(user.password_hash, password)
                return True
            except:
                return False
    except Exception:
        return False