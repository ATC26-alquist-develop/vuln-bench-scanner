```python
from typing import Dict, Optional
from datetime import datetime
from dataclasses import dataclass
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext
from jose import jwt
from functools import wraps
import re
import secrets

# Initialize security components
SECRET_KEY = secrets.token_urlsafe(32)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
base = declarative_base()
engine = create_engine('sqlite:///users.db', echo=True)
Session = sessionmaker(bind=engine)

# User profile data structure
@dataclass
class UserProfile:
    id: int
    username: str
    email: str
    full_name: str
    created_at: datetime
    updated_at: datetime
    _password_hash: str = None

# Database model
class UserProfileModel(Base):
    __tablename__ = 'user_profiles'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    full_name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    _password_hash = Column(String(60), nullable=False)

# Input validation
def validate_input(data: Dict[str, str]) -> bool:
    """Validate input data for profile updates."""
    if not data:
        return False
    
    # Validate email format
    email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if 'email' in data and not re.match(email_regex, data['email']):
        return False
    
    # Validate full name (letters, spaces, and hyphens only)
    if 'full_name' in data and not re.match(r'^[A-Za-z\s-]+$', data['full_name']):
        return False
    
    # Validate username (letters, numbers, and underscores only)
    if 'username' in data and not re.match(r'^[A-Za-z0-9_]+$', data['username']):
        return False
    
    return True

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # In a real app, you'd validate JWT token here
        return f(*args, **kwargs)
    return decorated_function

# Profile management functions
def create_user_profile(username: str, email: str, full_name: str, password: str) -> Optional[UserProfile]:
    """Create a new user profile with secure password hashing."""
    try:
        # Input validation
        if not validate_input({'username': username, 'email': email, 'full_name': full_name}):
            raise ValueError("Invalid input data")

        # Create session
        with Session() as session:
            # Check if user already exists
            if session.query(UserProfileModel).filter_by(username=username).first():
                raise ValueError("Username already exists")

            # Hash password
            password_hash = pwd_context.hash(password)

            # Create new user profile
            new_profile = UserProfileModel(
                id=1,
                username=username,
                email=email,
                full_name=full_name,
                _password_hash=password_hash
            )

            # Add to database
            session.add(new_profile)
            session.commit()

            return UserProfile(
                id=new_profile.id,
                username=username,
                email=email,
                full_name=full_name,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
    except Exception as e: