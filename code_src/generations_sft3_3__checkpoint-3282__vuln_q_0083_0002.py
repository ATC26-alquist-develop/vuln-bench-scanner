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

# Define base model for database
Base = declarative_base()

@dataclass
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    last_login = Column(DateTime)
    salt = Column(String(64))

class LoginStatus(Enum):
    SUCCESS = "success"
    INVALID_CREDENTIALS = "invalid_credentials"
    ACCOUNT_DISABLED = "account_disabled"
    RATE_LIMITED = "rate_limited"

class LoginSystem:
    def __init__(self, db_url: str):
        self.engine = create_engine(db_url)
        Base.metadata.create_all(self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.ph = PasswordHasher()
        self.login_attempts = {}
        self.max_attempts = 5
        self.lockout_duration = timedelta(minutes=15)

    def _validate_username(self, username: str) -> bool:
        """Validate username format"""
        return bool(re.match(r'^[a-zA-Z0-9_]{3,50}$', username))

    def _validate_password(self, password: str) -> bool:
        """Validate password strength"""
        return len(password) >= 12 and any(c.isupper() for c in password) and \
               any(c.islower() for c in password) and any(c.isdigit() for c in password)

    def register_user(self, username: str, password: str) -> bool:
        """Register a new user"""
        if not self._validate_username(username) or not self._validate_password(password):
            return False

        session = self.Session()
        try:
            if session.query(User).filter_by(username=username).first():
                return False
                
            salt = bcrypt.gensalt()
            password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
            
            user = User(
                username=username,
                password_hash=password_hash.decode('utf-8'),
                salt=salt.decode('utf-8')
            )
            session.add(user)
            session.commit()
            return True
        except Exception:
            session.rollback()
            return False
        finally:
            session.close()

    def login(self, username: str, password: str) -> tuple[LoginStatus, Optional[str]]:
        """Perform login attempt"""
        if not self._validate_username(username) or not self._validate_password(password):
            return LoginStatus.INVALID_CREDENTIALS, None

        session = self.Session()
        try:
            user = session.query(User).filter_by(username=username).first()
            if not user:
                return LoginStatus.INVALID_CREDENTIALS, None

            # Check for account lockout
            if user.id in self.login_attempts:
                attempts, last_attempt = self.login_attempts[user.id]
                if attempts >= self.max_attempts:
                    if datetime.now() - last_attempt < self.lockout_duration:
                        return LoginStatus.RATE_LIMITED, None
                    else:
                        self.login_attempts[user.id] = (0, datetime.now())
            
            # Verify credentials
            try:
                self.ph.verify(user.password_hash, password)
                self.login_attempts[user.id] = (0, datetime.now())
                user.last_login = datetime.now()
                session.commit()
                return LoginStatus.SUCCESS, "Login successful"
            except VerifyMismatchError:
                self.login_attempts[user.id] = (self.login