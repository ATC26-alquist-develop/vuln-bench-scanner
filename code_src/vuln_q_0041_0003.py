from typing import Optional
from datetime import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from passlib.hash import argon2
import secrets
import logging
from functools import wraps
from typing import Dict

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='account_management.log'
)

# Database setup
Base = declarative_base()
engine = create_engine('sqlite:///users.db', pool_pre_ping=True)
Session = sessionmaker(bind=engine)

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    salt = Column(String(32), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    last_login = Column(DateTime, nullable=True)
    _deleted = Column(Boolean, default=False)

Base.metadata.create_all(engine)

def rate_limit(max_calls: int = 3, time_window: int = 60):
    """Rate limiting decorator"""
    calls: Dict[str, list] = {}
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            client_ip = kwargs.get('client_ip', 'unknown')
            now = datetime.now()
            
            if client_ip in calls:
                calls[client_ip] = [
                    call_time for call_time in calls[client_ip]
                    if call_time > now - timedelta(seconds=time_window)
                ]
            else:
                calls[client_ip] = []
            
            if len(calls[client_ip]) >= max_calls:
                logging.warning(f"Rate limit exceeded for IP: {client_ip}")
                raise Exception("Rate limit exceeded. Please try again later.")
            
            calls[client_ip].append(now)
            return func(*args, **kwargs)
        return wrapper
    return decorator

@rate_limit(max_calls=3, time_window=60)
def delete_account(user_id: int, client_ip: str) -> None:
    """
    Securely delete a user account
    
    Args:
        user_id: The ID of the user to delete
        client_ip: The IP address of the client making the request
    """
    try:
        # Input validation
        if not isinstance(user_id, int) or user_id <= 0:
            raise ValueError("Invalid user ID")
        
        if not isinstance(client_ip, str) or not client_ip.strip():
            raise ValueError("Invalid IP address")

        # Get user from database with rate limiting
        with Session() as session:
            user = session.query(User).filter_by(id=user_id, _deleted=False).first()
            
            if not user:
                logging.warning(f"Attempted to delete non-existent or deleted account: {user_id}")
                raise ValueError("User not found")

            # Generate a unique deletion token
            deletion_token = secrets.token_urlsafe(16)

            # Update user record
            user._deleted = True
            user.deleted_token = deletion_token
            user.last_deleted = datetime.utcnow()

            # Log the deletion attempt
            logging.info(f"Account deletion requested: {user_id}")

            # Commit changes
            session.commit()

        logging.info(f"Account deletion token generated for user: {user_id}")
        return deletion_token

    except Exception as e:
        logging.error(f"Error deleting account: {str(e)}")
        raise