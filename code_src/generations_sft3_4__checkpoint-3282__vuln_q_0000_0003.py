import hashlib
import os
import re
import secrets
from typing import Dict, Optional

class UserAuth:
    def __init__(self):
        self.users: Dict[str, str] = {}  # username: hashed_password
        self.max_attempts = 5
        self.attempt_history: Dict[str, int] = {}  # username: last_failed_attempt

    def register(self, username: str, password: str) -> bool:
        """Register a new user with a hashed password."""
        if not self._validate_username(username) or not self._validate_password(password):
            return False
        
        if username in self.users:
            return False
        
        salt = os.urandom(32)
        hashed_password = self._hash_password(password, salt)
        self.users[username] = f"{salt.hex()}:{hashed_password}"
        return True

    def authenticate(self, username: str, password: str) -> bool:
        """Authenticate a user."""
        if not self._validate_username(username) or not self._validate_password(password):
            return False

        if username not in self.users:
            return False

        current_attempt = self._get_current_attempt(username)
        if current_attempt >= self.max_attempts:
            return False

        salt, stored_hash = self.users[username].split(':')
        salt = bytes.fromhex(salt)
        
        if self._hash_password(password, salt) == stored_hash:
            self._reset_attempts(username)
            return True
        
        self._increment_attempts(username)
        return False

    def _validate_username(self, username: str) -> bool:
        """Validate username format."""
        return bool(re.match(r'^[a-zA-Z0-9_]{3,20}$', username))

    def _validate_password(self, password: str) -> bool:
        """Validate password strength."""
        return len(password) >= 12 and any(c.isupper() for c in password) and \
               any(c.islower() for c in password) and any(c.isdigit() for c in password)

    def _hash_password(self, password: str, salt: bytes) -> str:
        """Hash password using PBKDF2 with SHA256."""
        return hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000).hex()

    def _get_current_attempt(self, username: str) -> int:
        """Get the current failed attempt count for a user."""
        return self.attempt_history.get(username, 0)

    def _reset_attempts(self, username: str) -> None:
        """Reset failed attempt count for a user."""
        self.attempt_history[username] = 0

    def _increment_attempts(self, username: str) -> None:
        """Increment failed attempt count for a user."""
        self.attempt_history[username] = self.attempt_history.get(username, 0) + 1

def main():
    auth = UserAuth()
    
    # Example usage
    username = "secure_user"
    password = secrets.token_urlsafe(16)  # Generate a secure random password
    
    if auth.register(username, password):
        print("User registered successfully")
    
    if auth.authenticate(username, password):
        print("Authentication successful")
    else:
        print("Authentication failed")

if __name__ == "__main__":
    main()