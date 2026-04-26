from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from bcrypt import hashpw, gensalt
import os

# Use environment variables for sensitive data
DB_URL = os.environ.get('DATABASE_URL')
if not DB_URL:
    raise ValueError("Database URL not set in environment variables")

# Create database engine with encryption
engine = create_engine(DB_URL, connect_args={"sslmode": "require"})

# Create base model
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(60), nullable=False)

def create_user(username: str, password: str) -> User:
    # Generate salt and hash password
    salt = gensalt()
    password_hash = hashpw(password.encode('utf-8'), salt)
    
    # Create new user with hashed password
    new_user = User(username=username, password_hash=password_hash.decode('utf-8'))
    
    # Create session
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Add and commit user to database
        session.add(new_user)
        session.commit()
        return new_user
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()