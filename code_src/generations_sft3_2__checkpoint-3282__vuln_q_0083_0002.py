```python
from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from typing import Optional
import secrets
import re
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import bcrypt
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define base class for database operations
Base = declarative_base()

@dataclass
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    last_login = Column(DateTime)

# Initialize database
DB_URL = "sqlite:///users.db"  # Use appropriate database for production
engine = create_engine(DB_URL)
Session = sessionmaker(bind=engine)

class LoginStatus(Enum):
    SUCCESS = "success"
    INVALID_CREDENTIALS = "invalid_credentials"
    ACCOUNT_DISABLED = "account_disabled"
    RATE_LIMITED = "rate_limited"

class RateLimiter:
    def __init__(self):
        self._limiter = {}
    
    def check(self, username: str) -> bool:
        current_time = datetime.now()
        if username not in self._limiter:
            self._limiter[username] = [current_time, 1]
            return True
        
        last_attempt, attempts = self._limiter[username]
        if current_time - last_attempt < timedelta(minutes=1):
            if attempts >= 5:
                return False
            self._limiter[username] = [current_time, attempts + 1]
            return False
        
        self._limiter[username] = [current_time, 1]
        return True

class SecureLoginSystem:
    def __init__(self):
        self.ph = PasswordHasher()
        self.rate_limiter = RateLimiter()
        self.max_login_attempts = 5
        self.login_timeout = 300  # 5 minutes
        self.login_attempts = {}
        
    def register_user(self, username: str, password: str) -> bool:
        """Register a new user with secure password hashing"""
        if not self._validate_username(username) or not self._validate_password(password):
            return False
        
        session = Session()
        try:
            if session.query(User).filter_by(username=username).first():
                return False
                
            # Hash password with Argon2
            password_hash = self.ph.hash(password)
            
            # Create new user
            new_user = User(username=username, password_hash=password_hash)
            session.add(new_user)
            session.commit()
            return True
        except Exception:
            session.rollback()
            return False
        finally:
            session.close()

    def login(self, username: str, password: str) -> LoginStatus:
        """Perform secure login"""
        if not self.rate_limiter.check(username):
            return LoginStatus.RATE_LIMITED
            
        session = Session()
        try:
            user = session.query(User).filter_by(username=username).first()
            if not user:
                return LoginStatus.INVALID_CREDENTIALS
                
            # Check if account is disabled
            if user.password_hash is None:
                return LoginStatus.ACCOUNT_DISABLED
                
            try:
                # Verify password using Argon2
                self.ph.verify(user.password_hash, password)
                # Check if login attempt is within timeout
                if username in self.login_attempts:
                    attempts, last_attempt = self.login_attempts[username]
                    if datetime.now() - last_attempt < timedelta(seconds=self.login_timeout):
                        return LoginStatus.RATE_LIMITED
                    attempts += 1
                else:
                    attempts = 1
                
                # Update login status
                self.login_attempts[username] =