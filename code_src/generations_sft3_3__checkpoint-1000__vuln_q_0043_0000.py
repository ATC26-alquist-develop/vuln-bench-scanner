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
class User:
    id: int
    username: str
    password_hash: str
    created_at: datetime
    last_login: Optional[datetime] = None

class UserRegistrationSystem:
    def __init__(self):
        Base.metadata.create_all(engine)
        
    def _validate_username(self, username: str) -> bool:
        """Validate username format."""
        if not re.match(r'^[a-zA-Z0-9_]{3,20}$', username):
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

    def register_user(self, username: str, password: str) -> bool:
        """Register a new user with secure password hashing."""
        try:
            # Input validation
            if not self._validate_username(username):
                logger.warning(f"Invalid username format: {username}")
                return False
            
            if not self._validate_password(password):
                logger.warning(f"Invalid password format: {password}")
                return False

            # Generate a random salt
            salt = bcrypt.gensalt()
            
            # Hash the password with the salt
            password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
            
            # Create new user
            new_user = User(
                username=username,
                password_hash=password_hash.decode('utf-8'),
                created_at=datetime.utcnow()
            )
            
            # Add user to database
            session = Session()
            session.add(new_user)
            session.commit()
            
            logger.info(f"User registered successfully: {username}")
            return True
            
        except Exception as e:
            logger.error(f"Registration failed: {str(e)}")
            return False
        finally:
            session.close()

    def authenticate_user(self, username: str, password: str) -> bool:
        """Authenticate user securely."""
        try:
            session = Session()
            user = session.query(User).filter_by(username=username).first()
            session.close()
            
            if user and bcrypt.checkpw(password.encode('utf-8'), user.password_hash.encode('utf-8')):
                user.last_login = datetime.utcnow()
                session = Session()
                session.commit()
                logger.info(f"User authenticated: {username}")
                return True
            else:
                logger.warning(f"Failed authentication attempt for user: {username}")
                return False
                
        except Exception as e:
            logger.error(f"Authentication failed: {str(e)}")
            return False
        finally:
            session.close()