import hashlib
import os
import secrets
import re
from typing import Dict, Optional

class UserAuth:
    def __init__(self):
        self.users: Dict[str, str] = {}
        self.max_attempts = 5
        self.attempt_count = 0

    def register_user(self, username: str, password: str) -> bool:
        """Register a new user with a hashed password."""
        if not self._validate_username(username) or not self._validate_password(password):
            return False
        
        if username in self.users:
            return False
        
        salt = os.urandom(32)
        hashed_password = self._hash_password(password, salt)
        self.users[username] = f"{salt.hex()}:{hashed_password}"
        return True

    def authenticate_user(self, username: str, password: str) -> bool:
        """Authenticate a user."""
        if not self._validate_username(username) or not self._validate_password(password):
            return False

        if username not in self.users:
            return False

        salt, stored_hash = self.users[username].split(':')
        salt = bytes.fromhex(salt)
        hashed_password = self._hash_password(password, salt)

        if hashed_password == stored_hash:
            self.attempt_count = 0
            return True
        else:
            self.attempt_count += 1
            if self.attempt_count >= self.max_attempts:
                return False
            return False

    def _hash_password(self, password: str, salt: bytes) -> str:
        """Hash the password using PBKDF2 with SHA256."""
        return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000).hex()

    def _validate_username(self, username: str) -> bool:
        """Validate username format."""
        return bool(re.match(r'^[a-zA-Z0-9_]{3,20}$', username))

    def _validate_password(self, password: str) -> bool:
        """Validate password strength."""
        return len(password) >= 12 and any(c.isupper() for c in password) and \
               any(c.islower() for c in password) and any(c.isdigit() for c in password) and \
               any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)

def main():
    auth = UserAuth()
    
    # Example usage
    username = input("Enter username: ")
    password = input("Enter password: ")
    
    if auth.register_user(username, password):
        print("User registered successfully")
    else:
        print("Registration failed")
    
    if auth.authenticate_user(username, password):
        print("Authentication successful")
    else:
        print("Authentication failed")

if __name__ == "__main__":
    main()