import bcrypt
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(60), nullable=False)

def hash_password(password: str) -> bytes:
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode('utf-8'), salt)

def verify_password(stored_hash: bytes, provided_password: str) -> bool:
    # Verify the provided password against the stored hash
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_hash)

# Example usage
engine = create_engine('sqlite:///users.db', echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def register_user(username: str, password: str) -> bool:
    session = Session()
    try:
        # Check if user already exists
        if session.query(User).filter_by(username=username).first():
            return False
            
        # Hash the password
        hashed_password = hash_password(password)
        
        # Create new user
        new_user = User(username=username, password_hash=hashed_password)
        session.add(new_user)
        session.commit()
        return True
    except Exception as e:
        session.rollback()
        raise
    finally:
        session.close()

def authenticate_user(username: str, password: str) -> bool:
    session = Session()
    try:
        user = session.query(User).filter_by(username=username).first()
        if user and verify_password(user.password_hash, password):
            return True
        return False
    finally:
        session.close()