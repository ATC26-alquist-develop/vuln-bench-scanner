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
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def verify_password(stored_hash: bytes, provided_password: str) -> bool:
    return bcrypt.checkpw(provided_password.encode('utf-8'), stored_hash)

# Usage example
engine = create_engine('sqlite:///users.db', echo=True)
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

# Hash and store password
session = Session()
new_user = User(username='alice', password_hash=hash_password('secure_password'))
session.add(new_user)
session.commit()
session.close()

# Verify password
def authenticate_user(username: str, password: str) -> bool:
    session = Session()
    user = session.query(User).filter_by(username=username).first()
    session.close()
    if user and verify_password(user.password_hash, password):
        return True
    return False