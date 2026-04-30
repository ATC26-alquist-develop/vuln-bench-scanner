import bcrypt
import secrets
from typing import Dict, Optional
import re

class UserAuth:
    def __init__(self):
        self.users: Dict[str, bytes] = {}

    def register_user(self, username: str, password: str) -> bool:
        """Register a new user with a securely hashed password."""
        if not self._validate_username(username) or not self._validate_password(password):
            return False
        
        if username in self.users:
            return False
        
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        self.users[username] = hashed_password
        return True

    def authenticate_user(self, username: str, password: str) -> bool:
        """Authenticate a user with their username and password."""
        if not self._validate_username(username) or not self._validate_password(password):
            return False
        
        stored_hash = self.users.get(username)
        if stored_hash is None:
            return False
        
        return bcrypt.checkpw(password.encode('utf-8'), stored_hash)

    def _validate_username(self, username: str) -> bool:
        """Validate username format."""
        return bool(re.match(r'^[a-zA-Z0-9_]{3,20}$', username))

    def _validate_password(self, password: str) -> bool:
        """Validate password strength."""
        return len(password) >= 12 and any(c.isupper() for c in password) and \
               any(c.islower() for c in password) and any(c.isdigit() for c in password) and \
               any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)

# Usage example
auth_system = UserAuth()

# Register a new user
username = "secure_user123"
password = "StrongP@ssw0rd!"
if auth_system.register_user(username, password):
    print("User registered successfully")
else:
    print("Registration failed")

# Authenticate a user
if auth_system.authenticate_user(username, password):
    print("Authentication successful")
else:
    print("Authentication failed")