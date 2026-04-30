```python
import os
from typing import Dict
from datetime import datetime
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel, EmailStr
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from passlib.context import CryptContext
from jose import JWTError, jwt
from dotenv import load_dotenv

# Load environment variables securely
load_dotenv()

# Database configuration using environment variables
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("Database URL not found in environment variables")

# Security configurations
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Initialize database
engine = create_engine(DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
Session = Depends(lambda: SessionLocal())

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# JWT token creation
jwt_token = JWTTokenCreator(SECRET_KEY, ALGORITHM)

# Models
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class Tweet(BaseModel):
    content: str
    created_at: datetime
    user_id: int

# FastAPI app initialization
app = FastAPI()

# Security utilities
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def authenticate_user(db: Session, email: str, password: str) -> User:
    user = db.query(User).filter(User.email == email).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user

def create_access_token(data: Dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Tweet creation endpoint
@app.post("/tweets/", response_model=Tweet)
async def create_tweet(tweet: Tweet, db: Session = Depends(SessionLocal)):
    try:
        # Validate input
        if not tweet.content or len(tweet.content) > 280:
            raise HTTPException(status_code=400, detail="Invalid tweet content")

        # Create new tweet
        new_tweet = Tweet(
            content=tweet.content,
            created_at=datetime.utcnow(),
            user_id=1  # In a real app, you'd get the authenticated user's ID
        )
        
        # Store in database
        db.add(new_tweet)
        db.commit()
        db.refresh(new_tweet)
        
        return new_tweet
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# User registration endpoint
@app.post("/users/", response_model=User)
async def create_user(user: User, db: Session = Depends(SessionLocal)):
    try:
        # Validate input
        if not user.email or not user.content:
            raise HTTPException(status_code=400, detail="Invalid user data")

        # Check if user already exists
        if db.query(User).filter(User.email == user.email).first():
            raise HTTPException(status_code