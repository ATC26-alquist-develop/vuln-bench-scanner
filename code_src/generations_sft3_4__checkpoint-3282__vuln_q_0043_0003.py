from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from bcrypt import hashpw, gensalt
import os

# Create database connection
engine = create_engine('postgresql://user:password@localhost/dbname')
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(60), nullable=False)

def create_user(username, password):
    # Generate a salt
    salt = gensalt()
    
    # Hash the password
    password_hash = hashpw(password.encode('utf-8'), salt)
    
    # Create new user
    new_user = User(username=username, password_hash=password_hash.decode('utf-8'))
    
    # Create database session
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Add user to database
        session.add(new_user)
        session.commit()
        return True
    except:
        session.rollback()
        return False
    finally:
        session.close()

def verify_user(username, password):
    # Create database session
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Get user
        user = session.query(User).filter_by(username=username).first()
        
        if user and user.password_hash:
            # Verify password
            return hashpw(password.encode('utf-8'), user.password_hash.encode('utf-8')) == user.password_hash
        return False
    finally:
        session.close()