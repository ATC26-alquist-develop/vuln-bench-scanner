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
        self.sessions: Dict[str, str] = {}

    def register_user(self, username: str, password: str) -> bool:
        """Register a new user with secure password hashing."""
        if username in self.users:
            return False
        
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
            return None
        
        if bcrypt.checkpw(password.encode('utf-8'), user.password_hash):
            # Generate a secure session token
            session_token = secrets.token_urlsafe(32)
            self.sessions[session_token] = username
            return session_token
        
        return None

    def validate_session(self, session_token: str) -> Optional[str]:
        """Validate a session token and return the associated username."""
        username = self.sessions.get(session_token)
        if username:
            return username
        return None

    def logout(self, session_token: str) -> None:
        """Invalidate a session token."""
        if session_token in self.sessions:
            del self.sessions[session_token]

# Example usage
auth_system = SecureAuthSystem()

# Register a new user
auth_system.register_user("alice", "secure_password123")

# Authenticate user
session_token = auth_system.authenticate_user("alice", "secure_password123")

if session_token:
    print("Authentication successful")
    
    # Validate session
    username = auth_system.validate_session(session_token)
    if username:
        print(f"Valid session for user: {username}")
    
    # Logout
    auth_system.logout(session_token)
    print("User logged out")
else:
    print("Authentication failed")