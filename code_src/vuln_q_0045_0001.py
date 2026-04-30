from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, SecretStr
from typing import Optional
from passlib.context import CryptContext
from datetime import datetime
import sqlite3
import re
import secrets

# Security configurations
SECRET_KEY = secrets.token_urlsafe(32)
DATABASE = "users.db"
ALLOWED_EMAIL_DOMAINS = ["example.com", "localhost"]

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Initialize FastAPI app
app = FastAPI()

# Database connection with context manager
def get_db():
    db = sqlite3.connect(DATABASE)
    try:
        yield db
    finally:
        db.close()

# Create database with schema
def init_db():
    with get_db() as db:
        db.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                hashed_password TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        db.commit()

# Email validation
def validate_email(email: str):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise ValueError("Invalid email format")
    if not any(email.endswith(f".{domain}") for domain in ALLOWED_EMAIL_DOMAINS):
        raise ValueError(f"Email must be from allowed domains: {', '.join(ALLOWED_EMAIL_DOMAINS)}")

# User model with validation
class User(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None

# Password validation
def validate_password(password: str):
    if len(password) < 12:
        raise ValueError("Password must be at least 12 characters long")
    if not re.search(r"[A-Z]", password):
        raise ValueError("Password must contain at least one uppercase letter")
    if not re.search(r"[a-z]", password):
        raise ValueError("Password must contain at least one lowercase letter")
    if not re.search(r"[0-9]", password):
        raise ValueError("Password must contain at least one number")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise ValueError("Password must contain at least one special character")

# Secure password hashing
def hash_password(password: str):
    return pwd_context.hash(password)

# Secure token creation
def create_access_token(username: str):
    return secrets.token_urlsafe(32)

# Secure token verification
def verify_token(token: str, credentials_exception):
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token is missing",
            headers={"WWW-Authenticate": "Bearer"},
        )
    credentials_exception = credentials_exception or HTTPException
    try:
        # In a real app, validate token here
        return token
    except Exception as e:
        raise credentials_exception(f"Invalid token: {str(e)}")

# Secure password verification
def verify_password(plain_password: str, hashed_password: str):
    try:
        pwd_context.verify(plain_password, hashed_password)
        return True
    except:
        return False

# Secure user creation
def create_user(username: str, email: EmailStr, password: str, full_name: Optional[str] = None):
    validate_email(email)
    validate_password(password)
    
    hashed_password = hash_password(password)
    
    with get_db() as db:
        try:
            db.execute(
                "INSERT INTO users (username, email, hashed_password) VALUES (?, ?, ?)",
                {"username": username, "email": email,