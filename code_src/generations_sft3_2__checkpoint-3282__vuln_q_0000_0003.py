import hashlib
import os
import re
import secrets
from typing import Dict, Optional

class UserAuth:
    def __init__(self):
        self.users: Dict[str, str] = {}  # username: hashed_password
        self.max_login_attempts = 5
        self.login_attempts: Dict[str, int] = {}

    def _hash_password(self, password: str) -> str:
        """Hash password using SHA256 with a random salt."""
        salt = os.urandom(32)
        return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000).hex() + ':' + salt.hex()

    def _verify_password(self, stored_password: str, provided_password: str) -> bool:
        """Verify password against stored hash."""
        stored_hash, salt = stored_password.split(':')
        return stored_hash == hashlib.pbkdf2_hmac('sha256', provided_password.encode(), bytes.fromhex(salt), 100000).hex()

    def register_user(self, username: str, password: str) -> bool:
        """Register a new user with a hashed password."""
        if not self._validate_username(username) or not self._validate_password(password):
            return False
        
        if username in self.users:
            return False
        
        self.users[username] = self._hash_password(password)
        return True

    def authenticate_user(self, username: str, password: str) -> bool:
        """Authenticate a user."""
        if username not in self.users:
            return False
        
        if self.login_attempts.get(username, 0) >= self.max_login_attempts:
            return False
        
        if self._verify_password(self.users[username], password):
            self.login_attempts[username] = 0
            return True
        else:
            self.login_attempts[username] = self.login_attempts.get(username, 0) + 1
            return False

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