import bcrypt
import secrets
from typing import Dict, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta

@dataclass
class User:
    username: str
    password_hash: bytes
    salt: bytes
    created_at: datetime

class SecureAuthSystem:
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.session_tokens: Dict[str, datetime] = {}

    def register_user(self, username: str, password: str) -> bool:
        """Register a new user with secure password hashing."""
        if username in self.users:
            return False  # User already exists
        
        # Generate a random salt
        salt = bcrypt.gensalt()
        # Hash the password with the salt
        password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)
        
        # Create and store the user
        self.users[username] = User(
            username=username,
            password_hash=password_hash,
            salt=salt,
            created_at=datetime.utcnow()
        )
        return True

    def authenticate_user(self, username: str, password: str) -> Optional[str]:
        """Authenticate a user and return a session token if successful."""
        user = self.users.get(username)
        if not user:
            return None  # User not found
        
        # Check if account is locked
        if user.created_at < datetime.utcnow() - timedelta(hours=1):
            return None  # Account locked
        
        # Verify password
        if bcrypt.checkpw(password.encode('utf-8'), user.password_hash):
            # Generate a secure session token
            token = secrets.token_urlsafe(32)
            self.session_tokens[token] = datetime.utcnow()
            return token
        return None

    def validate_session(self, token: str) -> bool:
        """Validate a session token."""
        if token in self.session_tokens:
            # Check if token has expired (e.g., 1 hour)
            if datetime.utcnow() - self.session_tokens[token] < timedelta(hours=1):
                return True
            else:
                del self.session_tokens[token]
        return False

# Example usage
auth_system = SecureAuthSystem()

# Register a new user
auth_system.register_user("alice", "secure_password123")

# Authenticate user
token = auth_system.authenticate_user("alice", "secure_password123")
if token:
    print("Authentication successful")
    # Validate session
    if auth_system.validate_session(token):
        print("Session is valid")
    else:
        print("Session is invalid or expired")
else:
    print("Authentication failed")