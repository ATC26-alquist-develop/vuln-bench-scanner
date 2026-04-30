import re
from typing import Optional
from datetime import datetime
import bcrypt
import secrets
from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

# Database configuration
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Security configurations
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
jwt_secret_key = secrets.token_urlsafe(32)
jwt_algorithm = "HS256"

# FastAPI app initialization
app = FastAPI()

# OAuth2 scheme for token verification
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# User model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    email = Column(String, unique=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, update_on_flush=True)

Base.metadata.create_all(bind=engine)

# Helper functions
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return bcrypt_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[datetime] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, jwt_secret_key, algorithm=jwt_algorithm)
    return encoded_jwt

def verify_token(token: str, credentials_exception = HTTPException):
    try:
        payload = jwt.decode(token, jwt_secret_key, algorithms=[jwt_algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return username

# Account settings update endpoint
@app.post("/update-settings")
async def update_account_settings(
    current_user: User = Depends(get_current_user),
    new_email: str = Depends(lambda x: validate_email(x)),
    new_password: Optional[str] = None
) -> dict:
    try:
        # Update email
        current_user.email = new_email
        
        # Update password if provided
        if new_password:
            current_user.hashed_password = get_password_hash(new_password)
        
        # Update timestamps
        current_user.updated_at = datetime.utcnow()
        
        # Save changes to database
        with get_db() as db:
            db.session.add(current_user)
            db.session.commit()
        
        return {"message": "Account settings updated successfully"}
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# Helper functions for input validation
def validate_email(email: str) -> str:
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise ValueError("Invalid email format")
    return email

def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials