import secrets
import hashlib
import re
from typing import Optional
from dataclasses import dataclass
from datetime import datetime
import bcrypt
import logging
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database setup
Base = declarative_base()
engine = create_engine('sqlite:///users.db', echo=True)
Session = sessionmaker(bind=engine)

@dataclass
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(60), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime)

Base.metadata.create_all(engine)

class SecureUserRegistration:
    def __init__(self):
        self.session = Session()
    
    def _validate_username(self, username: str) -> bool:
        """Validate username format."""
        if not re.match(r'^[a-zA-Z0-9_]{3,50}$', username):
            return False
        return True
    
    def _validate_password(self, password: str) -> bool:
        """Validate password strength."""
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
    
    def register_user(self, username: str, password: str) -> Optional[bool]:
        """Register a new user with secure password hashing."""
        try:
            # Validate inputs
            if not self._validate_username(username):
                logger.warning(f"Invalid username format: {username}")
                return None
                
            if not self._validate_password(password):
                logger.warning(f"Invalid password format: {password}")
                return None
                
            # Check if username already exists
            if self.session.query(User).filter_by(username=username).first():
                logger.warning(f"Username already exists: {username}")
                return None
                
            # Generate salt and hash password
            salt = bcrypt.gensalt()
            password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
            
            # Create new user
            new_user = User(username=username, password_hash=password_hash.decode('utf-8'))
            self.session.add(new_user)
            self.session.commit()
            
            logger.info(f"User registered successfully: {username}")
            return True
            
        except Exception as e:
            logger.error(f"Registration failed: {str(e)}")
            self.session.rollback()
            return None
        finally:
            self.session.close()

    def login(self, username: str, password: str) -> Optional[bool]:
        """Authenticate user."""
        try:
            user = self.session.query(User).filter_by(username=username).first()
            if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
                user.last_login = datetime.utcnow()
                self.session.commit()
                logger.info(f"User logged in: {username}")
                return True
            else:
                logger.warning(f"Failed login attempt for user: {username}")
                return False
                
        except Exception as e:
            logger.error(f"Login failed: {str(e)}")
            return False
        finally:
            self.session.close()