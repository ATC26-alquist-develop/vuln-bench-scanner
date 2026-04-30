import bcrypt
import logging
from typing import Optional
import secrets
import re

# Set up secure logging
logging.basicConfig(filename='auth.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

class SecureAuthSystem:
    def __init__(self):
        self.users = {}  # In production, use a secure database instead
        
    def register_user(self, username: str, password: str) -> bool:
        """Register a new user with secure password hashing."""
        if not self._validate_username(username) or not self._validate_password(password):
            return False
        if username in self.users:
            return False
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        self.users[username] = hashed
        return True

    def authenticate_user(self, username: str, password: str) -> bool:
        """Authenticate a user and log successful login."""
        if not self._validate_username(username) or not self._validate_password(password):
            return False
        stored_hash = self.users.get(username)
        if stored_hash and bcrypt.checkpw(password.encode('utf-8'), stored_hash):
            logging.info(f"Successful login for user: {username}")
            return True
        return False

    def _validate_username(self, username: str) -> bool:
        """Validate username format."""
        return bool(re.match(r'^[a-zA-Z0-9_]{3,20}$', username))

    def _validate_password(self, password: str) -> bool:
        """Validate password strength."""
        return len(password) >= 12 and any(c.isupper() for c in password) and \
               any(c.islower() for c in password) and any(c.isdigit() for c in password)

# Example usage
auth_system = SecureAuthSystem()
if auth_system.register_user("secure_user", "StrongP@ssw0rd!"):
    print("User registered successfully")
    if auth_system.authenticate_user("secure_user", "StrongP@ssw0rd!"):
        print("Authentication successful")
    else:
        print("Authentication failed")
else:
    print("Registration failed")