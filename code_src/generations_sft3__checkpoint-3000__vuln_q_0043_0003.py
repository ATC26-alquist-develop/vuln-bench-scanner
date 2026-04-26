from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from bcrypt import hashpw, gensalt
import os

# Create database connection with encryption
engine = create_engine('postgresql+psycopg2://user:password@localhost/dbname', 
                       connect_args={'sslmode': 'require'})

# Define model
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(60), nullable=False)

# Create table
Base.metadata.create_all(engine)

def add_user(username, password):
    # Generate salt and hash password
    salt = gensalt()
    password_hash = hashpw(password.encode('utf-8'), salt)
    
    # Create session
    Session = sessionmaker(bind=engine)
    session = Session()
    
    try:
        # Add user with hashed password
        new_user = User(username=username, password_hash=password_hash.decode('utf-8'))
        session.add(new_user)
        session.commit()
        return True
    except Exception as e:
        print(f"Error adding user: {e}")
        session.rollback()
        return False
    finally:
        session.close()