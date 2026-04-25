from argon2 import PasswordHasher
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)

def hash_password(password):
    ph = PasswordHasher()
    return ph.hash(password)

def verify_password(hashed_password, password):
    ph = PasswordHasher()
    try:
        ph.verify(hashed_password, password)
        return True
    except:
        return False

def create_user(username, password):
    engine = create_engine('sqlite:///users.db', echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    hashed_password = hash_password(password)
    
    new_user = User(username=username, password_hash=hashed_password)
    session.add(new_user)
    session.commit()
    session.close()

def authenticate_user(username, password):
    engine = create_engine('sqlite:///users.db', echo=True)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    user = session.query(User).filter_by(username=username).first()
    if user and verify_password(user.password_hash, password):
        session.close()
        return True
    session.close()
    return False